from flask import Flask, jsonify, request
from pymongo import MongoClient
import json
from bson import ObjectId, json_util


app = Flask(__name__)
app.config['DEBUG'] = False

client = MongoClient("mongodb+srv://test:test@covid-19-0wxmi.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('Drugs')
user_records = db.user_records


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/', methods=['GET','POST'])
def handleRequest():
        if request.method == 'GET':
                records = user_records.find()
                response = []
                for record in records:
                        record.pop('_id', None)
                        response.append(record)
                return json.dumps(response, default=json_util.default)

        if request.method == 'POST':
                req_data = request.get_json()
                user_records.insert_one(req_data)
                return('', 204)

if __name__ == '__main__':
        app.run(host='0.0.0.0', ssl_context='adhoc')






