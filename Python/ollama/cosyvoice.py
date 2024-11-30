# coding=utf-8

import dashscope
from dashscope.audio.tts_v2 import *
import os

# 获取环境变量
dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")

model = "cosyvoice-v1"
voice = "longxiaochun"


synthesizer = SpeechSynthesizer(model=model, voice=voice)

audio = synthesizer.call("Access to model denied. Please make sure you are eligible for using the model.")
print('requestId: ', synthesizer.get_last_request_id())
with open('output.mp3', 'wb') as f:
    f.write(audio)