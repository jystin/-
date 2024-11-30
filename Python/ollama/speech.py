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

# 获取环境变量
dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")

model = "cosyvoice-v1"
voice = "longxiaochun"


synthesizer = SpeechSynthesizer(model=model, voice=voice)




def get_speech(model="medium", language="zh", record_timeout=4, phrase_timeout=1):
    # The last time a recording was retrieved from the queue.
    phrase_time = None
    # Thread safe Queue for passing data from the threaded recording callback.
    data_queue = Queue()
    # We use SpeechRecognizer to record our audio because it has a nice feature where it can detect when speech ends.
    recorder = sr.Recognizer()
    recorder.energy_threshold = 1000
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramatically to a point where the SpeechRecognizer never stops recording.
    recorder.c = False

    # prepare tts
    tts = TTSExecutor()

    # Important for linux users.
    # Prevents permanent application hang and crash by using the wrong Microphone
    mic_name = "pipewire"
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if mic_name in name:
            source = sr.Microphone(sample_rate=16000, device_index=index)
            break

    # Load / Download model
    if model != "large" and language == "en":
        model = model + ".en"
    audio_model = whisper.load_model(model)

    transcription = []
    responses = []

    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio:sr.AudioData) -> None:
        """
        Threaded callback function to receive audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        data = audio.get_raw_data()
        data_queue.put(data)

    # Create a background thread that will pass us raw audio bytes.
    # We could do this manually but SpeechRecognizer provides a nice helper.
    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

    # Cue the user that we're ready to go.
    print("Model loaded.\n")

    while True:
        try:
            now = datetime.utcnow()
            # Pull raw recorded audio from the queue.
            if not data_queue.empty():
                phrase_complete = False
                # If enough time has passed between recordings, consider the phrase complete.
                # Clear the current working audio buffer to start over with the new data.
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    phrase_complete = True
                # This is the last time we received new audio data from the queue.
                phrase_time = now
                
                # Combine audio data from queue
                audio_data = b''.join(data_queue.queue)
                data_queue.queue.clear()
                
                # Convert in-ram buffer to something the model can use directly without needing a temp file.
                # Convert data from 16 bit wide integers to floating point with a width of 32 bits.
                # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                # Read the transcription.
                if language == "zh":
                    result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available(), language='Chinese')
                else:   
                    result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                text = result['text'].strip()

                # If we detected a pause between recordings, add a new item to our transcription.
                # Otherwise edit the existing one. 
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
                        # Clear the console to reprint the updated transcription.
                        os.system('cls' if os.name=='nt' else 'clear')
                        for i, line in enumerate(transcription):
                            print("You: ", line)
                            print("CHAT: ", responses[i])

                        auido_array = tts.get_audio(text=response['message']['content'], 
                                            # am="fastspeech2_ljspeech", 
                                            # lang="en", 
                                            # voc="hifigan_ljspeech", 
                                            # voc_ckpt="~/.paddlespeech/models/fastspeech2_ljspeech-en/1.0/fastspeech2_nosil_ljspeech_ckpt_0.5",
                                            output="output.wav")
                        play_audio(auido_array, data_queue)
                                
                        # Flush stdout.
                        print('', end='', flush=True)
            else:
                # Infinite loops are bad for processors, must sleep.
                sleep(0.25)
        except KeyboardInterrupt:
            break

def play_audio(auido_array, data_queue, fs=24000):
    # 播放音频
    sd.play(auido_array, samplerate=fs)
    while sd.get_stream().active:
        # 这里可以添加一个检查麦克风输入的逻辑
        if mic_input_detected(data_queue):
            sd.stop()  # 停止音频播放
            break
    return 

# 检测麦克风输入的函数
def mic_input_detected(data_queue) -> bool:
    # 在这里实现你自己的检测逻辑
    # 例如，使用 sounddevice 读取麦克风数据并进行简单分析
    # 这里只是示例，返回 False
    # 如果data_queue中有数据，说明检测到了麦克风输入
    if not data_queue.empty():
        return True
    else:
        return False


if __name__ == "__main__":
    get_speech()
