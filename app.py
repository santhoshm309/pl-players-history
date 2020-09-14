from flask import Flask,Response,make_response
from flask_restful import Resource, reqparse, Api
import requests
import json

app = Flask(__name__)
api = Api(app)
app.config['PROPAGATE_EXCEPTIONS'] = True

app.app_context().push()
ELEMENT_SUMMARY_URI="https://fantasy.premierleague.com/api/element-summary/"
class Players(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('player_ids', type=int, action='append')
    def get(self):
        args=self.parser.parse_args()
        try:
            json_response={}
            for element in args["player_ids"]:
                r=requests.get(ELEMENT_SUMMARY_URI+str(element)+"/")
                if r.ok:
                    element_resp=r.json()
                    json_response[element]=element_resp["history"]
                else:
                    return make_response({"message":"Fantasy IPL API error", "statusCode":500},500)

            res=json.dumps(json_response)
            response=Response(res,content_type='application/json')
            response.headers.add('content-length',len(res))
            response.status_code=200
            return response
        except ValueError:
            return make_response({"message":"Fantasy IPL API error", "statusCode":500},500)

api.add_resource(Players, '/')

if __name__=='__main__':
    
    app.run(debug=True)
