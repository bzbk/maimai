# coding=utf-8

import re
import sys
import json
import base64
import time
import xml.etree.ElementTree as ET



IS_PY3 = sys.version_info.major == 3

if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    timer = time.perf_counter
else:
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode
    if sys.platform == "win32":
        timer = time.clock
    else:
        # On most other platforms the best timer is time.time()
        timer = time.time



class DemoError(Exception):
    pass


def parse_response(response):
    """
    此模块用于将json文档转化为数组输出
    参数
    response        :   传入的josn文件或字符串
    json_data       :   转换后的json字典

    返回值
    text_code       :   输出的数组
    """
    text_code=[]
    json_data=json.loads(response)
    
    #print(json_data['err_no'])
    text_code.append(json_data['err_no'])
    #print(json_data['result'][0])
    text_code.append(json_data['result'][0])
    return text_code

    


"""  TOKEN 验证 """

TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'

def fetch_token(API_KEY="",SECRET_KEY="",SCOPE=""):
    """
    百度的TOKEN身份识别
    """
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode( 'utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        #print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str =  result_str.decode()

    #print(result_str)
    result = json.loads(result_str)
    #print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        #print(SCOPE)
        if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
            raise DemoError('scope is not correct')
        #print('SUCCESS WITH TOKEN: %s  EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


def get_dlog_text(AUDIO_FILE):
    """
    获取对话文字
    参数
    AUDIO_FILE      :   音频文件路径
    返回值
    text            :   [0]请求代码：0 成功  [1]识别到的文字
    """
    #从配置文档获取信息
    # 读取配置文件
    tree = ET.parse("API_Config.xml")
    # 获取配置元素对象
     
    cfg =tree.getroot()

    #print("root_tag:",cfg.tag)
    #print(cfg[0].tag+" : "+cfg[0].text)
    API_KEY=str(cfg[0][0].text)
    #print(cfg[1].tag+" : "+cfg[1].text)
    SECRET_KEY=str(cfg[0][1].text)
    #print(cfg[2].tag+" : "+cfg[2].text)
    CUID=str(cfg[0][2].text)
    #print(cfg[3].tag+" : "+cfg[3].text)
    DEV_PID=str(cfg[0][3].text)
    #print(cfg[4].tag+" : "+cfg[4].text)
    ASR_URL=str(cfg[0][4].text)
    #print(cfg[5].tag+" : "+cfg[5].text)
    SCOPE=str(cfg[0][5].text)
    #print(cfg[6].tag+" : "+cfg[6].text)
    RATE=str(cfg[0][6].text)

    FORMAT = AUDIO_FILE[-3:]  # 文件后缀只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式


    #获取token认证
    token = fetch_token(API_KEY=API_KEY,SECRET_KEY=SECRET_KEY,SCOPE=SCOPE) 

    #创建对话数组
    speech_data = []

    #读取音频文件
    with open(AUDIO_FILE, 'rb') as speech_file:
        speech_data = speech_file.read()
    
    length = len(speech_data)

    if length == 0:
        raise DemoError('文件 %s 的长度为0字节' % AUDIO_FILE)
    speech = base64.b64encode(speech_data)

    if (IS_PY3):
        speech = str(speech, 'utf-8')

    #准备发送字段
    params = {'dev_pid': DEV_PID,
              'format': FORMAT,
              'rate': RATE,
              'token': token,
              'cuid': CUID,
              'channel': 1,
              'speech': speech,
              'len': length
              }
    post_data = json.dumps(params, sort_keys=False)

    #开始请求
    req = Request(ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')

    try:
        begin = timer()
        f = urlopen(req)
        result_str = f.read()
        print ("请求时间 %f" % (timer() - begin))
    except URLError as err:
        print('asr 请求失败 http 代码 : ' + str(err.code))
        result_str = err.read()

    if (IS_PY3):
        result_str = str(result_str, 'utf-8')

    #将收到的json文件处理为字符串组
    #print(result_str)
    text=parse_response(result_str)
    #print(text)
    return text
    #print(result_str)
    #with open("result.txt","w") as of:
    #    of.write(result_str)

