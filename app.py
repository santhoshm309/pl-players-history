from flask import Flask,Response,make_response
from flask_restful import Resource, reqparse, Api
import requests
import json

app = Flask(__name__, static_folder="data", static_url_path='/static')
api = Api(app)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.app_context().push()
ELEMENT_SUMMARY_URI="https://fantasy.premierleague.com/api/element-summary/"
class Players(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('pid', type=int, action='append')
    def get(self):
        args=self.parser.parse_args()
        try:
            json_response={}
            if args is None or args["pid"] is None:
                return make_response({"message":"No valid query params given", "statusCode":400},400)
            for element in args["pid"]:
                r=requests.get(ELEMENT_SUMMARY_URI+str(element)+"/")
                if r.ok:
                    element_resp=r.json()
                    json_response[element]=element_resp["history"]
                else:
                    return make_response({"message":"Fantasy IPL API error", "statusCode":500},500)
            
            return make_response(json_response,200)
        except ValueError:
            return make_response({"message":"Fantasy IPL API error", "statusCode":500},500)

api.add_resource(Players, '/')

if __name__=='__main__':
    
    app.run(debug=True)
