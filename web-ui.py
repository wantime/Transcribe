
import threading

from flask import Flask, render_template, jsonify, request, send_file
from pydub import AudioSegment
from transcriber import Transcriber
import os

app = Flask(__name__)

# 存储处理结果的字典，键为任务 ID，值为处理结果
results = {}


# 定义音频转文本的方法
def audio2text(file_path, task_id):
    try:
        trans = Transcriber(model_name="large-v3")
        text = trans.transcribe(file_path)
        results[task_id] = text
        # 处理完成后删除临时文件
        os.remove(file_path)
    except Exception as e:
        results[task_id] = f"处理出错: {str(e)}"



    # with sr.AudioFile(audio_path) as source:
    #     audio = r.record(source)
    # try:
    #     text = r.recognize_google(audio, language='zh-CN')
    #     return text
    # except sr.UnknownValueError:
    #     return "无法识别音频内容"
    # except sr.RequestError as e:
    #     return f"请求出错; {e}"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def upload():
    if 'audio_file' not in request.files:
        return jsonify({'error': '没有上传音频文件'}), 400
    file = request.files['audio_file']
    if file.filename == '':
        return jsonify({'文件名不能为空'}), 400
    # 生成唯一任务id
    import uuid
    task_id = str(uuid.uuid4())
    print(f"task_id:{task_id}")
    # 保存上传的文件
    file_path = os.path.join('uploads', file.filename)
    # 检查文件格式，如果是 mp3 则转换为 wav
    if file.filename.endswith('.mp3'):
        audio = AudioSegment.from_mp3(file_path)
        wav_path = os.path.splitext(file_path)[0] + '.wav'
        audio.export(wav_path, format='wav')
        file_path = wav_path

    file.save(file_path)
    print(f"save_path:{file_path}")
    # 创建一个新线程来处理音频文件
    thread = threading.Thread(target=audio2text, args=(file_path, task_id))
    thread.start()

    return jsonify({'task_id': task_id, 'message': '转换已开始，请不要关闭网页'}), 202

    #     # 调用音频转文本的方法
    #     text = audio2text(file_path)
    #
    #     # 删除临时文件
    #     os.remove(file_path)
    #
    # return render_template('index.html', text=text)


@app.route('/check_result/<task_id>', methods=['GET'])
def check_result(task_id):
    result = results.get(task_id)
    if result is None:
        return jsonify({'status': '处理中', 'message': '请稍后再试'}), 202
    else:
        return jsonify({'status': '完成', 'result': result})


@app.route('/download/<task_id>', methods=['GET'])
def download(task_id):
    result = results.get(task_id)
    if result is None:
        return jsonify({'error': '处理未完成或失败'}), 400
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(result)
    return send_file('output.txt', as_attachment=True, download_name='transcription.txt')

    text = request.form.get('text')
    file_path = 'output.txt'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
