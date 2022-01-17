# 迈迈语音助手

 > 以上海散爆网络公司旗下游戏——《云图计划》，角色“迈迈”为原型制作的语音交互助手,是橱力向作品。

 > 主要功能通过语音交互，简单操作操作系统，由于是开源程序可以高度自定义功能。

 > 项目 __除__ snowboy离线唤醒模块 和 API调用模块（天气 和 语音转文字 asr） 以及 美术资源（音频，视频，模型等）等,之外均默认使用 __CC-0 开源协议__，作者放弃一切权利。美术资源权利归上海散爆网络所有。

###### *第一次写MD文档，第一次用软件仓库，第一次使用开源协议。如有不妥之处往海涵，并及时提醒。万分感谢。

## 借鉴项目

- snowboy 
https://github.com/kitt-ai/snowboy
- 悟空机器人 潘伟洲
https://wukong.hahack.com/#/
- 一个下午制作一个智能语音聊天助手
https://www.bilibili.com/video/BV1Nt411w7FJ

## MMD借物表

- 《云图计划》-迈迈
https://www.aplaybox.com/details/model/k7TgDB1b5SeP


 
## 运行环境

- 统信 UOS家庭版 操作系统（Linux）
https://www.chinauos.com/  
> 优秀的国产操作系统，可以使用wine和uegine兼容Windows和安卓。
  
## 部署方式

### 安装 git

> $ sudo apt install -y git

### 安装 python2 pyhton3 pip3

> $ sudo apt install -y python  

> $ sudo apt install -y python3

> $ sudo apt install -y python3-pip  

### python 库部署


> $ pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple  
更换 清华PIP源

> $ pip3 install requests  
安装请求库

> $ pip3 install pinyin  
安装 拼音库

> $ pip3 install pydub  
安装 音频处理库


### 安装 sox ，ffmpeg

> $ sudo apt-get install -y portaudio19-dev 

> $ sudo apt-get install -y sox 

> $ sudo apt-get install -y pulseaudio

> $ sudo apt-get install -y python-pyaudio  

> $ sudo apt-get install -y python3-pyaudio

> $ sudo apt-get install -y libsox-fmt-all 

> $ sudo apt-get install -y ffmpeg  

### 安装 swig

> $ wget https://wzpan-1253537070.cos.ap-guangzhou.myqcloud.com/misc/swig-3.0.10.tar.gz  

> $ tar xvf swig-3.0.10.tar.gz  

> $ cd swig-3.0.10  

> $ sudo apt-get -y update  

> $ sudo apt-get install -y libpcre3 libpcre3-dev  

> $ ./configure \-\-prefix=/usr \-\-without-clisp \-\-without-maximum-compile-warnings  

> $ make

> $ sudo make install  

> $ sudo install -v -m755 -d /usr/share/doc/swig-3.0.10  

> $ sudo cp -v -R Doc/* /usr/share/doc/swig-3.0.10  

> $ sudo apt-get install -y libatlas-base-dev  

> $ cd ..  

### 安装 雪人（snowboy）

>​ $ wget https://wzpan-1253537070.cos.ap-guangzhou.myqcloud.com/misc/snowboy.tar.bz2  

> $ tar -xvjf snowboy.tar.bz2  

> $ cd snowboy/swig/Python3  

> $ make  

> $ cp _snowboydetect.so <迈迈的根目录的绝对路径>  

> $ cd ~/  




## 项目结构

