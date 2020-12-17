from aip import AipSpeech
""" 你的百度 APPID AK SK
https://console.bce.baidu.com/ai/#/ai/speech/app/list       应用列表
http://ai.baidu.com/docs#/TTS-Online-Python-SDK/top         API
"""
APP_ID = '10563438'
API_KEY = 'gDz0samrO2cB7gMGuqHw2skN'
SECRET_KEY = '1950a96adb7d349c62f7d2a907ef13ec'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
text111 = "春江潮水连海平 海上明月共潮升。"
result  = client.synthesis(text111, 'zh', 0, {
    'vol': 5,
})
## 百度语音合成
print(result)
# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('./auido.mp3', 'wb') as f:
        f.write(result)