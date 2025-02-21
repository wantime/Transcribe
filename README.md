# 基于faster-whisper的会议录音转文字系统

![img](static\img.png)

使用方式

```
pip install -r requirements.txt
python web-ui.py
```

或者docker部署

如使用本地模型，请在根目录下创建对应的文件夹

```
large-v3(存放large-v3模型与相关文件)
	->model.bin
	->.gitattributes
	->config.json
	->preprocessor_config.json
	->tokenizer.json
	->vocabulary.json
static
	->style.css
templates
	index.html
transcriber.py
web-ui.py
```

模型下载地址

```
large-v3：https://huggingface.co/Systran/faster-whisper-large-v3/tree/main
large-v2：https://huggingface.co/guillaumekln/faster-whisper-large-v2/tree/main
large-v2：https://huggingface.co/guillaumekln/faster-whisper-large-v1/tree/main
medium：https://huggingface.co/guillaumekln/faster-whisper-medium/tree/main
small：https://huggingface.co/guillaumekln/faster-whisper-small/tree/main
base：https://huggingface.co/guillaumekln/faster-whisper-base/tree/main
tiny：https://huggingface.co/guillaumekln/faster-whisper-tiny/tree/main
```





