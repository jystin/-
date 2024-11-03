from paddlespeech.cli.tts.infer import TTSExecutor
tts = TTSExecutor()
tts(text="What is the weather like today?", 
    am="fastspeech2_ljspeech", 
    lang="en", 
    voc="hifigan_ljspeech", 
    # voc_ckpt="~/.paddlespeech/models/fastspeech2_ljspeech-en/1.0/fastspeech2_nosil_ljspeech_ckpt_0.5",
    output="output.wav")
# tts(text="牛逼哈", output="output.wav")
