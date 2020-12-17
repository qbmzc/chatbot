import pyaudio
import wave


def record(seconds, filename):
    RATE = 8000  # 采样率
    CHANNELS = 2  # 采样管道数
    FORMAT = pyaudio.paInt16  # 量化位数
    SECONDS = seconds  # 录音时长
    p = pyaudio.PyAudio()
    stream = p.open(rate=RATE, channels=CHANNELS, format=FORMAT, input=True)
    frames = []  # 存储所有读取到的数据
    print("录音开始,还有", seconds, "秒")
    data = stream.read(RATE*SECONDS)
    frames.append(data)
    stream.stop_stream()
    print("录音结束！！！")
    stream.close()
    p.terminate()  # 关闭会话
    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setframerate(RATE)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.writeframes(b''.join(frames))
    wf.close()
    return filename


record(5, './auido.wav')
