from flask import Flask
from flask_restful import Api, Resource
import json
from thesetta import matcher, searcher, pfs_matcher, pfs_searcher

app = Flask(__name__)
api = Api(app)

with open('/home/scottcarlson/api/api.json', 'r') as destiny:
    makes = json.load(destiny)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Maker(Resource):
    def get(self, key, name):
        if key == '0103':
            for make in makes:
                if(name == make["name"]):
                    if make['type'] == 'primary':
                        resp = make["name"]
                        return resp, 200
                    elif make['type'] == 'variant':
                        resp = make["use"]
                        return resp, 200
            return "User not found", 404
        else:
            return "API key incorrect", 401


class Matcher(Resource):
    def get(self, key, name):
        if key == '0103':
            diggity = matcher(name)
            return diggity.strip('"'), 200
        else:
            return "API key incorrect", 401


class Searcher(Resource):
    def get(self, key, name):
        if key == '0103':
            ziggity = searcher(name)
            return ziggity, 200
        else:
            return "API key incorrect", 401


class PFS_Matcher(Resource):
    def get(self, key, name):
        if key == '0103':
            diggity = pfs_matcher(name)
            return diggity.strip('"'), 200
        else:
            return "API key incorrect", 401


class PFS_Searcher(Resource):
    def get(self, key, name, ratio):
        if key == '0103':
            ziggity = pfs_searcher(name, ratio)
            return ziggity, 200
        else:
            return "API key incorrect", 401


api.add_resource(HelloWorld, '/')

api.add_resource(Maker, "/make/<string:key>|<path:name>")

api.add_resource(Matcher, "/matcher/<string:key>|<path:name>")

api.add_resource(Searcher, "/searcher/<string:key>|<path:name>")

api.add_resource(PFS_Matcher, "/pfs_matcher/<string:key>|<path:name>")

api.add_resource(PFS_Searcher, "/pfs_searcher/<string:key>|<string:ratio>|<path:name>")

if __name__ == '__main__':
    app.run
