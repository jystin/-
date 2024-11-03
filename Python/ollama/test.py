import ollama
import cv2
import time

import speech_recognition as sr
import pyaudio


# response = ollama.chat(model='llama3.2:3b', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])

# print(response['message']['content'])

if __name__ == '__main__':

    cv2.namedWindow("camera", 1)
    # 开启ip摄像头
    # admin是账号，admin是密码
    video = "http://admin:admin@192.168.1.13:8081/"  # 此处@后的ipv4 地址需要修改为自己的地址
    capture = cv2.VideoCapture(video)

    # 创建一个Recognizer对象
    r = sr.Recognizer() 


    num = 0
    while True:
        success, img = capture.read()
        img = cv2.resize(img, (640, 480))
        # 图片逆时针旋转90度
        img = cv2.transpose(img)
        img = cv2.flip(img, -1)

        # 打开麦克风进行录音
        with sr.Microphone() as source:
            print("请开始说话...")
            audio = r.listen(source)

        # 将录音转化为文本
        try:
            text = r.recognize_google(audio, language='zh-CN')
            print("识别结果：", text)
        except sr.UnknownValueError:
            print("抱歉，无法识别。")
        except sr.RequestError:
            print("抱歉，请求出错。")


        cv2.imshow("camera", img)

        # 按键处理，注意，焦点应当在摄像头窗口，不是在终端命令行窗口
        key = cv2.waitKey(10)

        if key == 27:
            # esc键断开连接
            print("esc break...")
            break
        if key == ord(' '):
            # 保存一张图像到工作目录
            num = num + 1
            filename = "frames_%s.jpg" % num
            cv2.imwrite(filename, img)

    capture.release()
    cv2.destroyWindow("camera")

