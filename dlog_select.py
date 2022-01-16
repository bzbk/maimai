"""
本文件通过对话 关键字 检索
将导入的文字先转化为拼音，通过拼音检索

参数

dlog_text       ：  传入的汉字对话
pinyin_text     ：  将汉字转化为拼音检索拼音

通过从拼音中检索关键字，例如“打开”
    将对应拼音“da-kai”在输入的拼音中检索
    如果检索到，执行下一步检索，例如“云图”
        在输入的拼音中继续检索“yun-tu”
        如果检测到则执行动作打开云图计划
        返回一个 真 表明执行成功

"""


import os
import _thread
import pinyin
import random
import snowboydecoder
from resources.天气模块 import update_weather

shutdown_key = 0


def get_text_num(KEY):
    """
    传入关键字段获取一个随机数
    """
    text_num=random.randint(0,len(KEY)-1)
    return text_num


def dlog_select_action(dlog_text=""):
    """
    对话检索判断机

    暴力的关键字查询判断

    为什么要自己写这个，因为调用api要花钱啊，还不能自定义。图灵机器人19一个月，你喜欢你自己去买。

    """
    pinyin_text=pinyin.get(dlog_text, format='strip', delimiter="-")
    print(pinyin_text)

    #关键词 打开
    if pinyin_text.find("da-kai") != -1:
        if pinyin_text.find("yun-tu") != -1:
            try:
                os.system("uengine launch --action=android.intent.action.MAIN --package=com.sunborn.neuralcloud.cn --component=com.sunborn.neuralcloud.cn.GameMainActivity &")
                snowboydecoder.play_audio_file("resources/语音库/云图计划.wav")

            except:
                print("已尝试打开云图计划")

            return True
        
        if pinyin_text.find("fa-pei-ren") != -1:
            try:
                os.system("/opt/apps/com.postman.postman/files/Postman &")
                snowboydecoder.play_audio_file(snowboydecoder.DETECT_SCD[3])

            except:
                print("已尝试打开postman")

            return True

        if pinyin_text.find("Q-Q") != -1:
            try:
                os.system("qq &")
                snowboydecoder.play_audio_file(snowboydecoder.DETECT_SCD[3])

            except:
                print("已尝试打开QQ")

            return True

    #关键词 云母
    if pinyin_text.find("yun-mu") != -1:
        try:
            os.system("microsoft-edge-stable www.ymfm.online &")
            snowboydecoder.play_audio_file(snowboydecoder.DETECT_SCD[2])

        except:
            print("已尝试FM")

        return True
        

    #关键词 天气
    if pinyin_text.find("tian-qi") != -1:
        # 今天
        if pinyin_text.find("jin-tian") != -1:
            
            try:
                update_weather.update_w("jin-tian")
                print("正在打开 迈迈天气")
                os.system("microsoft-edge-stable resources/天气模块/weather.html &")
                snowboydecoder.play_audio_file(snowboydecoder.DETECT_SCD[1])
            except:
                print("已尝试 打开 迈迈天气")

            return True
    global shutdown_key
    #关键词 关机
    if pinyin_text.find("guan-ji") != -1:
        # 关机
        if pinyin_text.find("que-ren") != -1:
        
            if shutdown_key == 1:
                
                try:
                    print("正在关机")
                    os.system("poweroff &")
                    snowboydecoder.play_audio_file(snowboydecoder.DETECT_SCD[1])
                except:
                    print("已尝试 关机")

                return True

        print("请再说一遍 “确认关机”")
        shutdown_key = 1

    return False