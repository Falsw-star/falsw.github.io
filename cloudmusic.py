import cloudmusic
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
app = Flask(__name__)
api = Api(app)

class url(Resource):
    def get(self):
        get_data = request.args.to_dict()
        songid = str(get_data.get('id'))
        music = cloudmusic.getMusic(songid)
        data = music.url
        return data, 200
api.add_resource(url, '/url')

if __name__ == '__main__':
    app.run()
