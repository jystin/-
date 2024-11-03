import whisper

if __name__ == '__main__':
    # list available models
    # ['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large-v3', 'large', 'large-v3-turbo', 'turbo']
    # print(whisper.available_models())

    model = whisper.load_model("large-v3-turbo")
    result = model.transcribe("MP3/jn_seg.mp3", fp16=False, language="English")
    print(result["text"])
