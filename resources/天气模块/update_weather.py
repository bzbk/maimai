import requests
import xml.etree.ElementTree as ET
import json

text_url = "resources/天气模块/Weather.html"
json_url = "resources/天气模块/cityCode.json"
AIP_url = "http://wthrcdn.etouch.cn/WeatherApi"

def get_city():
    """
    获取城市
    配置文件
    """
    # 读取配置文件
    tree = ET.parse("API_Config.xml")
    cfg =tree.getroot()
    #print(cfg[1].tag)
    gogf=[]
    gogf.append(cfg[1][0][0].text)
    gogf.append(cfg[1][0][1].text)
    gogf.append(cfg[1][0][2].text)
    print("查询城市： "+gogf[0]+" 省 " + gogf[1] + " 市 "+gogf[2] )
    return gogf

def sel_city_code(gogf=["","",""]):
    """
    通过此函数
    查询城市代码模块
    获取城市代码

    """
    city_code = []
    
    file = open(json_url, "rb")
    data=json.load(file)
    for p in data:
        if p['label']== gogf[0]:
            for ss in p['children']:
                if ss['label']==gogf[1]:
                    for s in ss['children']:
                        if s['label']==gogf[2]:
                            city_code.append(s['value'])
    print("城市代码："+city_code[0])
    return city_code[0]

def get_API_Xml(city_code="",time="jin-tian"):

    url=AIP_url+"?citykey="+city_code
    r=requests.get(url=url)
    print(r.status_code)
    #print(r.text)
    f=open("resources/天气模块/data.xml","w")
    f.write(r.text)
    f.close()
    tree = ET.parse("resources/天气模块/data.xml")
    weather=tree.getroot()
    print(weather.tag)
    #输出 0 当前温度 1 湿度 2 风向 3 日期 4 最高温度 5 最低温度 6 白天状态 7 夜间状态 8 舒适度
    out_key=[   weather[2].text,
                weather[4].text,
                weather[5].text,
                weather[11][0][0].text,
                weather[11][0][1].text,
                weather[11][0][2].text,
                "白昼： "+weather[11][0][3][0].text+" "+weather[11][0][3][1].text,
                "夜间： "+weather[11][0][4][0].text+" "+weather[11][0][4][1].text,
                "舒适度： "+weather[12][10][1].text+" "+weather[12][10][2].text ]
    
    print(out_key)
    return out_key


def get_web(in_key=[]):
    gogf=get_city()
    html="""<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" type="text/css" href="weather.css">
    <title>迈迈天气</title>
</head>
<body>
    <h1>迈迈天气</h1>
    <hr>
    <p>"""+gogf[0]+" 省 " + gogf[1] + " 市 "+gogf[2]+" "+in_key[3]+"""</p>
    <p id="a1">当前温度<a id="temperature">"""+in_key[0]+"""</a>℃</p>
    <p>湿度<a id="humidity">"""+in_key[1]+"""</a></p>
    <p>风向<a id="wind">"""+in_key[2]+"""</a></p>
    <p>最高温度：<a id="temperature1">"""+str(in_key[4]).split(' ')[1]+"""</a></p>
    <p>最高温度：<a id="temperature1">"""+str(in_key[5]).split(' ')[1]+"""</a></p>
    <p>白昼：<a id="weather1">"""+str(in_key[6]).split('：')[1]+"""</a></p>
    <p>夜间：<a id="weather1">"""+str(in_key[7]).split('：')[1]+"""</a></p>
    <p><a id="comfort">"""+in_key[8]+"""</a></p>
</body>
</html>"""
    f=open("resources/天气模块/weather.html","w")
    f.write(html)
    f.close()




def update_w(time_str):
    city=get_city()
    cid=sel_city_code(city)
    key=get_API_Xml(cid,time_str)
    get_web(key)
    return True


if  __name__=="__main__":

    update_w("jin-tian")