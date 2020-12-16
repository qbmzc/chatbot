import speech_recognition as  sr


## 录音
def my_record(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("请讲话，录音开始......")
        audio = r.listen(source)

    with open("./voices/myvioces.wav","wb") as f:
        f.write(audio.get_wav_data())
    print("录音完成！")


my_record()