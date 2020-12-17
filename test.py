import requests
import json
from aip import AipSpeech
import wave
import pyaudio
import pygame
import time
urls = 'http://openapi.tuling123.com/openapi/api/v2'   # 图灵接口的url
api_key = "e9c53ad2f0834d0bbe93f0c5e5cc64ac"

count = 1  # 用来计数输入的次数
def record(seconds,filename):
    RATE=8000#采样率
    CHANNELS=2#采样管道数
    FORMAT=pyaudio.paInt16#量化位数
    SECONDS=seconds#录音时长
    #第一步：创建PyAudio的实例对象
    p = pyaudio.PyAudio()
    #第二步：调用PyAudio实例对象的open方法创建流Stream
    stream=p.open(rate=RATE,channels=CHANNELS,format=FORMAT,input=True)
    frames=[]#存储所有读取到的数据
    print("录音开始,还有",seconds,"秒")
    #第三步：根据需求，调用Stream的write或者read方法
    data=stream.read(RATE*SECONDS)
    frames.append(data)
    #第四步：调用Stream的stop方法停止播放音频或者是录制音频
    stream.stop_stream()
    print("录音结束！！！")
    #第五步：调用Stream的close方法，关闭流
    stream.close()
    #第六步：调用pyaudio.PyAudio.terminate() 关闭会话
    p.terminate()
    #写入到wav文件里面
    wf=wave.open(filename,"wb")
    wf.setnchannels(CHANNELS)
    wf.setframerate(RATE)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.writeframes(b''.join(frames))
    wf.close()
    return filename
""" 你的 APPID AK SK """
APP_ID = '10563438'
API_KEY = 'gDz0samrO2cB7gMGuqHw2skN'
SECRET_KEY = '1950a96adb7d349c62f7d2a907ef13ec'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
# 语音识别
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 回复
def Turing(data,n):
    data_dict = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": data
            },
        },
        "userInfo": {
            "apiKey": api_key,
            "userId": "630194"
        }
    }
    result = requests.post(urls, json=data_dict)
    content = result.text
    # print(content)
    ans = json.loads(content)
    text = ans['results'][0]['values']['text']
    print('Niubility:',text)  # 机器人取名就叫Niubility
    result2 = client.synthesis(text, 'zh', 1, {
        'vol': 5, 'spd': 4, 'per': 1
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result2, dict):
        with open('./auido{}.mp3'.format(n), 'wb') as f:
            f.write(result2)
    pygame.mixer.init()
    pygame.mixer.music.load("./auido{}.mp3".format(n))
    pygame.mixer.music.play()
    time.sleep(10)
    f.close()
if __name__ == "__main__":
    print("Niubility：主人您好，我是Niubility，爱你哦~")
    for n in range(1,51):
        record(5,'./auido.wav')
        result = client.asr(get_file_content('./auido.wav'), 'wav', 16000, {
            'dev_pid': 1537,
        })
        mm = result['result'][0]
        data = input('{}//你：'.format(count)+mm)  # 输入对话内容
        Turing(mm,n)
        count+=1