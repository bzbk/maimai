"""
迈迈主程序

"""

import os
import asr
import signal
import random
import dialogue
import dlog_select
import snowboydecoder
from pydub import AudioSegment

# Demo code for listening to two hotwords at the same time

interrupted = False

#关键词随机数
text_num = 0


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

def get_text_num(KEY):
    """
    传入关键字段获取一个随机数
    """
    global text_num
    text_num=random.randint(0,len(KEY)-1)
    dialogue.DLOG_NUM=text_num
    return text_num

def audioRecorderCallback(fname):
    """
    录音完成回调函数

    参数

    fname   ：  录制完成的音频位置
    """
    get_dlog=False
    print("录制文件位置"+fname)
    wav=AudioSegment.from_wav(fname)
    #裁剪音频
    wav[2200:].export(fname, format="wav")
    print("开始语音转文字")
    try:
        data=asr.get_dlog_text(fname)
        if data[0] == 0:
            print(data[1])
            get_dlog=True
    except:
        print("语音转文字失败")
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_FAIL[get_text_num(snowboydecoder.DETECT_FAIL)])

    if get_dlog:
        if dlog_select.dlog_select_action(data[1]):
            print("执行操作成功")
            
        else:
            print("执行操作失败")
            snowboydecoder.play_audio_file(snowboydecoder.DETECT_FAIL[get_text_num(snowboydecoder.DETECT_FAIL)])
    
    os.remove(fname)
    print("____________________________________________________________________")





"""
唤醒部分
"""
#唤醒词设置
models = ["resources/models/你好迈迈.pmdl","resources/models/迈迈.pmdl"]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_WORK[get_text_num(snowboydecoder.DETECT_WORK)]),
             lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_PLAY[get_text_num(snowboydecoder.DETECT_PLAY)])]

data=open("logo.txt",encoding="utf-8")

print("\033[0;36m")
print(data.read())
print("\033[0m")
data.close()

print("____________________________________________________________________")
print('聆听中... 按下 Ctrl+C 退出程序')

# 主循环
# 通过定义的多个模型开始识别
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               audio_recorder_callback=audioRecorderCallback,
               sleep_time=0.03)

detector.terminate()
