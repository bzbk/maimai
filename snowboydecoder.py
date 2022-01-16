#!/usr/bin/env python

import collections
import pyaudio
import snowboydetect
import time
import wave
import os
import logging
import dialogue
from ctypes import *
from contextlib import contextmanager

logging.basicConfig()
logger = logging.getLogger("迈迈察觉到")
logger.setLevel(logging.INFO)
TOP_DIR = os.path.dirname(os.path.abspath(__file__))

#资源设置定义模块

RESOURCE_FILE = os.path.join(TOP_DIR, "resources/common.res")
DETECT_DING = os.path.join(TOP_DIR, "resources/ding.wav")
DETECT_DONG = os.path.join(TOP_DIR, "resources/dong.wav")



DETECT_WORK = []
"""
加载 交互语音 文件
参数
WORK_DLOG_TEXT  ：  对话文本
DETECT_WORK     ：  对话音频设置
"""
for td in dialogue.WORK_DLOG_TEXT:
    DETECT_WORK.append(os.path.join(TOP_DIR, "resources/语音库/交互（干活）/"+td+".wav"))


DETECT_PLAY = []
"""
加载 互动语音 文件
参数
PLAY_DLOG_TEXT  ：  对话文本
DETECT_PLAY    ：  对话音频设置
"""
for td in dialogue.PLAY_DLOG_TEXT:
    DETECT_PLAY.append(os.path.join(TOP_DIR, "resources/语音库/互动（玩）/"+td+".wav"))


DETECT_SCD = []
"""
加载 成功相应 文件
参数
SCD_DLOG_TEXT  ：  对话文本
DETECT_SCD     ：  对话音频设置
"""
for td in dialogue.SCD_DLOG_TEXT:
    DETECT_SCD.append(os.path.join(TOP_DIR, "resources/语音库/反馈/成功/"+td+".wav"))


DETECT_FAIL = []
"""
加载 失败相应 文件
参数
FAIL_DLOG_TEXT  ：  对话文本
DETECT_FAIL     ：  对话音频设置
"""
for td in dialogue.FAIL_DLOG_TEXT:
    DETECT_FAIL.append(os.path.join(TOP_DIR, "resources/语音库/反馈/失败/"+td+".wav"))



def py_error_handler(filename, line, function, err, fmt):
    pass


ERROR_HANDLER_FUNC = CFUNCTYPE(
    None, c_char_p, c_int, c_char_p, c_int, c_char_p)

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)


@contextmanager
def no_alsa_error():
    try:
        asound = cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(c_error_handler)
        yield
        asound.snd_lib_error_set_handler(None)
    except:
        yield
        pass


class RingBuffer(object):
    """
    环形缓冲区，用于保存来自 PortAudio 的音频
    """

    def __init__(self, size=4096):
        self._buf = collections.deque(maxlen=size)

    def extend(self, data):
        """
        将数据添加到缓冲区的队尾
        """
        self._buf.extend(data)

    def get(self):
        """
        从缓冲区的队首检索数据并将其清除
        """
        tmp = bytes(bytearray(self._buf))
        self._buf.clear()
        return tmp


def play_audio_file(fname=DETECT_DING):
    """
    简单的回调函数，播放音频文件。默认情况下，它播放
    默认音频，无修改是“叮”的声音。

    参数 
    str fname ： 默认音频文件的名称
    返回值 ： 空
    """
    if fname==DETECT_DING :
        ding_wav = wave.open(fname, 'rb')
        ding_data = ding_wav.readframes(ding_wav.getnframes())
        with no_alsa_error():
            audio = pyaudio.PyAudio()
        stream_out = audio.open(
            format=audio.get_format_from_width(ding_wav.getsampwidth()),
            channels=ding_wav.getnchannels(),
            rate=ding_wav.getframerate(), input=False, output=True)
        stream_out.start_stream()
        stream_out.write(ding_data)
        time.sleep(0.3)
    elif fname==DETECT_DONG : 
        ding_wav = wave.open(fname, 'rb')
        ding_data = ding_wav.readframes(ding_wav.getnframes())
        with no_alsa_error():
            audio = pyaudio.PyAudio()
        stream_out = audio.open(
            format=audio.get_format_from_width(ding_wav.getsampwidth()),
            channels=ding_wav.getnchannels(),
            rate=ding_wav.getframerate(), input=False, output=True)
        stream_out.start_stream()
        stream_out.write(ding_data)
        time.sleep(0.3)
    else:
        dlog_text=str(fname).split('/')
        print("迈迈： "+dlog_text[len(dlog_text)-1].split('.')[0])
        ding_wav = wave.open(fname, 'rb')
        ding_data = ding_wav.readframes(ding_wav.getnframes())
        with no_alsa_error():
            audio = pyaudio.PyAudio()
        stream_out = audio.open(
            format=audio.get_format_from_width(ding_wav.getsampwidth()),
            channels=ding_wav.getnchannels(),
            rate=ding_wav.getframerate(), input=False, output=True)
        stream_out.start_stream()
        stream_out.write(ding_data)
        time.sleep(0.3)
    
    stream_out.stop_stream()
    stream_out.close()
    audio.terminate()


class HotwordDetector(object):
    """
    雪人 将通过读取关键字段 `decoder_model` 【你训练的唤醒模型路径】
    来检测关键词是否通过麦克风输入

    参数
    decoder_model: 唤醒模型的路径
    resource: 资源文件路径
    sensitivity: 对关键词的敏感度 浮点型【值越大，越敏感，超级的敏感，全与你有关。传参为空使用默认灵敏度】
    audio_gain: 回应的音量大小
    apply_frontend: 说什么前端之类的，我看不懂
    """

    def __init__(self, decoder_model,
                 resource=RESOURCE_FILE,
                 sensitivity=[],
                 audio_gain=1,
                 apply_frontend=False):

        tm = type(decoder_model)
        ts = type(sensitivity)
        if tm is not list:
            decoder_model = [decoder_model]
        if ts is not list:
            sensitivity = [sensitivity]
        model_str = ",".join(decoder_model)

        self.detector = snowboydetect.SnowboyDetect(
            resource_filename=resource.encode(), model_str=model_str.encode())
        self.detector.SetAudioGain(audio_gain)
        self.detector.ApplyFrontend(apply_frontend)
        self.num_hotwords = self.detector.NumHotwords()

        if len(decoder_model) > 1 and len(sensitivity) == 1:
            sensitivity = sensitivity * self.num_hotwords
        if len(sensitivity) != 0:
            assert self.num_hotwords == len(sensitivity), \
                "number of hotwords in decoder_model (%d) and sensitivity " \
                "(%d) does not match" % (self.num_hotwords, len(sensitivity))
        sensitivity_str = ",".join([str(t) for t in sensitivity])
        if len(sensitivity) != 0:
            self.detector.SetSensitivity(sensitivity_str.encode())

        self.ring_buffer = RingBuffer(
            self.detector.NumChannels() * self.detector.SampleRate() * 5)

    def start(self, detected_callback=play_audio_file,
              interrupt_check=lambda: False,
              sleep_time=0.03,
              audio_recorder_callback=None,
              silent_count_threshold=15,
              recording_timeout=100):
        """
        启动语音检测器。对于每"sleep_time"秒，它会检查
        用于触发关键字的音频缓冲区。如果检测到，则启动
        "detected_callback"中的对应函数，可以是单个
        函数（单个模型）或回调函数列表（多个模型）。
        每个循环它也调用"interrupt_check" - 如果它返回
        True，然后脱离循环并返回。

        参数
        detected_callback       :       函数或函数列表。数量项目必须与 中的模型数量匹配"decoder_model"。
        interrupt_check         :       如果主循环返回 True 的函数需要停止。
        float sleep_time        :       每个循环每秒等待多少时间。
        audio_recorder_callback :       如果指定，这将在一个关键字已被说出，并且在紧跟在关键字后面的短语具有
                                        已录制。该函数将是传递了文件的名称，其中短语已录制。
        silent_count_threshold  :       指示必须听到多长时间的静音以标记短语的结尾，该短语正在录制。
        recording_timeout       :       限制录制文件的最大长度。
        eturn: None
        """
        self._running = True

        def audio_callback(in_data, frame_count, time_info, status):
            self.ring_buffer.extend(in_data)
            play_data = chr(0) * len(in_data)
            return play_data, pyaudio.paContinue

        with no_alsa_error():
            self.audio = pyaudio.PyAudio()
        self.stream_in = self.audio.open(
            input=True, output=False,
            format=self.audio.get_format_from_width(
                self.detector.BitsPerSample() / 8),
            channels=self.detector.NumChannels(),
            rate=self.detector.SampleRate(),
            frames_per_buffer=2048,
            stream_callback=audio_callback)

        if interrupt_check():
            logger.debug("detect voice return")
            return

        tc = type(detected_callback)
        if tc is not list:
            detected_callback = [detected_callback]
        if len(detected_callback) == 1 and self.num_hotwords > 1:
            detected_callback *= self.num_hotwords

        assert self.num_hotwords == len(detected_callback), \
            "Error: hotwords in your models (%d) do not match the number of " \
            "callbacks (%d)" % (self.num_hotwords, len(detected_callback))

        logger.debug("detecting...")

        state = "PASSIVE"
        while self._running is True:
            if interrupt_check():
                logger.debug("detect voice break")
                break
            data = self.ring_buffer.get()
            if len(data) == 0:
                time.sleep(sleep_time)
                continue

            status = self.detector.RunDetection(data)
            if status == -1:
                logger.warning(
                    "Error initializing streams or reading audio data")

            #small state machine to handle recording of phrase after keyword
            if state == "PASSIVE":
                if status > 0:  # 关键词检测成功
                    self.recordedData = []
                    self.recordedData.append(data)
                    silentCount = 0
                    recordingCount = 0
                    message = "关键词 " + str(status) +" “"+dialogue.HOT_WORD[int(status)-1]+ "” 生效时间: \t"
                    message += time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
                    logger.info(message)
                    callback = detected_callback[status-1]
                    
                    if callback is not None:
                        callback()
                    if int(status)==1:
                        if audio_recorder_callback is not None:
                            state = "ACTIVE"
                            play_audio_file()
                            print("开始录制！")
                    else:
                        print("____________________________________________________________________")
                    continue

            elif state == "ACTIVE":
                stopRecording = False
                if recordingCount > recording_timeout:
                    stopRecording = True
                elif status == -2:  # silence found
                    if silentCount > silent_count_threshold:
                        stopRecording = True
                    else:
                        silentCount = silentCount + 1
                elif status == 0:  # voice found
                    silentCount = 0

                if stopRecording == True:
                    fname = self.saveMessage()
                    play_audio_file(DETECT_DONG)
                    print("录制结束！")
                    audio_recorder_callback(fname)

                    state = "PASSIVE"
                    continue

                recordingCount = recordingCount + 1
                self.recordedData.append(data)
        
        logger.debug("finished.")

    def saveMessage(self):
        """
        Save the message stored in self.recordedData to a timestamped file.
        """
        filename = 'temp/output' + str(int(time.time())) + '.wav'
        data = b''.join(self.recordedData)

        #use wave to save data
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(
            self.audio.get_format_from_width(
                self.detector.BitsPerSample() / 8)))
        wf.setframerate(self.detector.SampleRate())
        wf.writeframes(data)
        wf.close()
        logger.debug("finished saving: " + filename)
        return filename

    def terminate(self):
        """
        Terminate audio stream. Users can call start() again to detect.
        :return: None
        """
        self.stream_in.stop_stream()
        self.stream_in.close()
        self.audio.terminate()
        self._running = False
