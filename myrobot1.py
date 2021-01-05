# -*- coding: utf-8 -*-#
# -------------------------------
# Name:SpeechRobot
# Author:congco
# Date:2021/01/05 16:51
# 用python3实现自己的语音对话机器人
# -------------------------------

from aip import AipSpeech
import requests
import json
import speech_recognition as sr
import win32com.client  # pywin32

# 初始化语音
speaker = win32com.client.Dispatch("SAPI.SpVoice")


# 1、语音生成音频文件,录音并以当前时间戳保存到voices文件中
# Use SpeechRecognition to record 使用语音识别录制
def my_record(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        audio = r.listen(source)

    with open("./voices/myvoices.wav", "wb") as f:
        f.write(audio.get_wav_data())


# 2、音频文件转文字：采用百度的语音识别python-SDK
# 导入我们需要的模块名，然后将音频文件发送给出去，返回文字。
# 百度语音识别API配置参数
APP_ID = '10563438'
API_KEY = 'gDz0samrO2cB7gMGuqHw2skN'
SECRET_KEY = '1950a96adb7d349c62f7d2a907ef13ec'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
path = './voices/myvoices.wav'


# 将语音转文本STT
def listen():
    # 读取录音文件
    with open(path, 'rb') as fp:
        voices = fp.read()
    try:
        # 参数dev_pid：1536普通话(支持简单的英文识别)、1537普通话(纯中文识别)、1737英语、1637粤语、1837四川话、1936普通话远场
        result = client.asr(voices, 'wav', 16000, {'dev_pid': 1537, })
        # result = CLIENT.asr(get_file_content(path), 'wav', 16000, {'lan': 'zh', })
        # print(result)
        # print(result['result'][0])
        # print(result)
        result_text = result["result"][0]
        print("you said: " + result_text)
        return result_text
    except KeyError:
        print("KeyError")
        speaker.Speak("我没有听清楚，请再说一遍...")


# 3、与机器人对话：调用的是图灵机器人
# 图灵机器人的API_KEY、API_URL
turing_api_key = "e9c53ad2f0834d0bbe93f0c5e5cc64ac"
api_url = "http://openapi.tuling123.com/openapi/api/v2"  # 图灵机器人api网址
headers = {'Content-Type': 'application/json;charset=UTF-8'}


# 图灵机器人回复
def Turing(text_words=""):
    req = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": text_words
            },

            "selfInfo": {
                "location": {
                    "city": "上海",
                    "province": "上海",
                    "street": "青浦"
                }
            }
        },
        "userInfo": {
            "apiKey": turing_api_key,  # 你的图灵机器人apiKey
            "userId": "Nieson"  # 用户唯一标识(随便填, 非密钥)
        }
    }

    req["perception"]["inputText"]["text"] = text_words
    response = requests.request("post", api_url, json=req, headers=headers)
    response_dict = json.loads(response.text)

    result = response_dict["results"][0]["values"]["text"]
    print("AI Robot said: " + result)
    return result


# 语音合成，输出机器人的回答
while True:
    my_record()
    request = listen()
    response = Turing(request)
    speaker.Speak(response)
