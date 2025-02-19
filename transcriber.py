import faster_whisper


class Transcriber:
    """
    转录为文字的类
    """

    def __init__(self,
                 model_name="base",
                 backend="faster_whisper",
                 beam_size=5,
                 language="zh"):
        self.model_name = model_name
        if backend == "faster_whisper":
            self.model = faster_whisper.WhisperModel(self.model_name)
            # 这里可以加载本地model
        self.beam_size = beam_size

        # todo 检测传入的语言是否在语言list里
        self.language = language

    def transcribe(self, audio_data: object) -> object:
        # todo segments是否要形成一个类
        segments, info = self.model.transcribe(audio_data,
                                               beam_size=self.beam_size,
                                               language=self.language)
        # todo 翻译完毕的文本是否要进行校准
        text = ""
        for segment in segments:
            text += segment.text + "."

        return text

