import os
import numpy as np
import speech_recognition as sr
import whisper
import torch

from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform
import ollama
from paddlespeech.cli.tts.infer import TTSExecutor
import soundfile as sf
import sounddevice as sd
from dashscope.audio.tts_v2 import *
import os
import pyaudio

# 获取环境变量
dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")

class Callback(ResultCallback):
    _player = None
    _stream = None
    interrupt_output = False  # 标志位，用于控制是否中断播放

    def on_open(self):
        self._player = pyaudio.PyAudio()
        self._stream = self._player.open(
            format=pyaudio.paInt16, channels=1, rate=22050, output=True
        )

    def on_data(self, data: bytes) -> None:
        if not self.interrupt_output:
            # print("Write data to stream.")
            # 清空stream，防止播放过程中有新的数据写入
            self._stream.write(data)

    def on_close(self):
        # print("Close the stream.")
        self._stream.stop_stream()
        self._stream.close()
        self._player.terminate()

def get_speech(model="medium", language="zh", record_timeout=4, phrase_timeout=1):
    phrase_time = None
    data_queue = Queue()
    recorder = sr.Recognizer()
    recorder.energy_threshold = 1000
    recorder.dynamic_energy_threshold = False

    callback = Callback()
    synthesizer = SpeechSynthesizer(
        model="cosyvoice-v1",
        voice="longxiaochun",
        format=AudioFormat.PCM_22050HZ_MONO_16BIT,
        callback=callback,
    )

    mic_name = "pipewire"
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if mic_name in name:
            source = sr.Microphone(sample_rate=16000, device_index=index)
            break

    if model != "large" and language == "en":
        model = model + ".en"
    audio_model = whisper.load_model(model)

    transcription = []
    responses = []

    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio: sr.AudioData) -> None:
        data = audio.get_raw_data()
        data_queue.put(data)
        callback.interrupt_output = True  # 检测到话筒输入时中断播放

    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

    print("Model loaded.\n")

    while True:
        try:
            now = datetime.utcnow()
            if not data_queue.empty():
                phrase_complete = False
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    phrase_complete = True
                phrase_time = now

                audio_data = b''.join(data_queue.queue)
                data_queue.queue.clear()

                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                if language == "zh":
                    result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available(), language='Chinese')
                else:   
                    result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                text = result['text'].strip()

                if phrase_complete:
                    text = text.strip()
                    if text == "":
                        continue
                    else:
                        transcription.append(text)
                        response = ollama.chat(model='qwen2.5:0.5b', messages=[
                            {
                                'role': 'user',
                                'content': text,
                            },
                            ])
                              
                        responses.append(response['message']['content'])
                        os.system('cls' if os.name=='nt' else 'clear')
                        for i, line in enumerate(transcription):
                            print("YOU: ", line)
                            print("CHAT: ", responses[i])

                        callback.interrupt_output = False  # 恢复播放
                        synthesizer.streaming_call(responses[-1])
                        print('', end='', flush=True)
            else:
                sleep(0.25)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    get_speech()