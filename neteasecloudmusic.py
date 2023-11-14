import cloudmusic
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
from flask_cors import *
import requests
import json
import urllib.request
from urllib.parse import urlparse
from urllib import parse
import os
app = Flask(__name__)
api = Api(app)


CORS(app, supports_credentials = True)

class url(Resource):
    def get(self):
        get_data = request.args.to_dict()
        songid = str(get_data.get('id'))
        try:
            music = cloudmusic.getMusic(songid)
            name = music.name
        except:
            print('-----查无此曲xwx-----')
            name = '没有这首歌啦qwq'
        nmapi = requests.get('http://127.0.0.1:3000/song/v1/url?id=' + songid)
        nmapi = nmapi.text
        nmapi = json.loads(nmapi)
        print('开始解析：' + name)
        data = music.url
        result = data.replace('"','')
        try:
            apiurl = nmapi['data'][0]['url']
            result = apiurl
        except:
            print('api调用失败，将调用爬虫')
        print(result)
        a = urlparse(result)
        file_name = os.path.basename(a.path)
        _,file_suffix = os.path.splitext(file_name)
        print(file_name)
        print(file_suffix)
        audiodir = '/Volumes/Little_1/audios/'
        name = name.replace('/','\\')
        songfile = audiodir + name + '-' + songid + file_suffix
        print(songfile)
        print(os.path.exists(songfile))
        if (os.path.exists(songfile)==True):
            netfile = 'http://ncm.falsw.top/' + parse.quote(name) + '-' + songid + file_suffix
            print('文件已存在，正在返回链接……')
            print(name)
            print(file_suffix)
            print(netfile)
            return netfile, 200
        else:
            urllib.request.urlretrieve(result, songfile)
            netfile = 'http://ncm.falsw.top/' + parse.quote(name) + '-' + songid + file_suffix
            print('正在返回链接……')
            print(name)
            print(file_suffix)
            print(netfile)
            return netfile, 200

class pic(Resource):
    def get(self):
        get_data = request.args.to_dict()
        songid = str(get_data.get('id'))
        print(songid)
        try:
            music = cloudmusic.getMusic(songid)
            picurl = music.picUrl
        except:
            print('查无此曲🤔')
            picurl = 'None'
        print('正在返回链接：' + picurl)
        return picurl, 200


api.add_resource(url, '/url')
api.add_resource(pic, '/pic')

if __name__ == '__main__':
    app.run()
