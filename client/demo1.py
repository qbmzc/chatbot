from tkinter import *
import time
from aip import AipSpeech
import requests
import json
import speech_recognition as sr
import win32com.client  # pywin32

path = 'E://git/chatbot/voices/myvoices.wav'
# 初始化语音
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# 2、音频文件转文字：采用百度的语音识别python-SDK
# 导入我们需要的模块名，然后将音频文件发送给出去，返回文字。
# 百度语音识别API配置参数
APP_ID = '10563438'
API_KEY = 'gDz0samrO2cB7gMGuqHw2skN'
SECRET_KEY = '1950a96adb7d349c62f7d2a907ef13ec'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 3、与机器人对话：调用的是图灵机器人
# 图灵机器人的API_KEY、API_URL
turing_api_key = "e9c53ad2f0834d0bbe93f0c5e5cc64ac"
api_url = "http://openapi.tuling123.com/openapi/api/v2"  # 图灵机器人api网址
headers = {'Content-Type': 'application/json;charset=UTF-8'}

flag = 1


# 1、语音生成音频文件,录音并以当前时间戳保存到voices文件中
# Use SpeechRecognition to record 使用语音识别录制
def my_record(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        audio = r.listen(source)

    with open(path, "wb") as f:
        f.write(audio.get_wav_data())


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
        strMsg = '我:' + time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime()) + '\n '
        print(strMsg + result_text)
        return result_text
    except KeyError:
        print("KeyError")
        speaker.Speak("我没有听清楚，请再说一遍...")


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
    responseMsg = '小枀:' + time.strftime("%Y-%m-%d %H:%M:%S",
                                        time.localtime()) + '\n '
    print(responseMsg + result)
    return result


def main():
    def start_chat():
        while flag == 1:
            my_record()
            request = listen()
            response = Turing(request)
            speaker.Speak(response)
            sendMsg(request, response)

    def sendMsg(request, response):  # 发送消息

        print(request)
        strMsg = '我:' + time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime()) + '\n '
        txtMsgList.insert(END, strMsg, 'greencolor')
        # txtMsgList.insert(END, txtMsg.get('0.0', END))
        txtMsgList.insert(END, request + '\n ')
        # 机器人回复
        responseMsg = '小枀:' + time.strftime("%Y-%m-%d %H:%M:%S",
                                            time.localtime()) + '\n '
        txtMsgList.insert(END, responseMsg, 'greencolor')
        txtMsgList.insert(END, response + '\n ')
        txtMsg.delete('0.0', END)
        print(response)

    def cancelMsg():  # 取消消息
        flag = 0

    # txtMsg.delete('0.0', END)

    def sendMsgEvent(event):  # 发送消息事件
        if event.keysym == "Return":
            sendMsg()

    # 创建窗口
    t = Tk()
    t.title('与python聊天中')

    # 创建frame容器
    frmLT = Frame(width=500, height=320, bg='white')
    frmLC = Frame(width=500, height=150, bg='white')
    frmLB = Frame(width=500, height=30)
    frmRT = Frame(width=200, height=500)

    # 创建控件
    txtMsgList = Text(frmLT)
    txtMsgList.tag_config('greencolor', foreground='#008C00')  # 创建tag
    txtMsg = Text(frmLC)
    txtMsg.bind("<KeyPress-Return>", start_chat)
    btnSend = Button(frmLB, text='开始聊天', width=8, command=start_chat)
    btnCancel = Button(frmLB, text='结束对话', width=8, command=cancelMsg)
    imgInfo = PhotoImage(file="bg.png")
    lblImage = Label(frmRT, image=imgInfo)
    lblImage.image = imgInfo

    # 窗口布局
    frmLT.grid(row=0, column=0, columnspan=2, padx=1, pady=3)
    frmLC.grid(row=1, column=0, columnspan=2, padx=1, pady=3)
    frmLB.grid(row=2, column=0, columnspan=2)
    frmRT.grid(row=0, column=2, rowspan=3, padx=2, pady=3)
    # 固定大小
    frmLT.grid_propagate(0)
    frmLC.grid_propagate(0)
    frmLB.grid_propagate(0)
    frmRT.grid_propagate(0)

    btnSend.grid(row=2, column=0)
    btnCancel.grid(row=2, column=1)
    lblImage.grid()
    txtMsgList.grid()
    txtMsg.grid()

    # 主事件循环
    t.mainloop()


if __name__ == '__main__':
    main()
