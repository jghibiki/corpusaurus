from flask import Flask, request, abort, jsonify, make_response, send_file
from flask.ext.cors import CORS
from werkzeug.contrib.fixers import ProxyFix
import tablib
import json


app = Flask(__name__, static_url_path='', static_folder='app')
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app, headers=['Content-Type, Authorization'])

@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/api/files/csv', methods=["POST"])
def getCSV():
    json_data = request.json
    app.logger.debug(json.dumps(json_data))
    data = tablib.Dataset(*json_data["data"], headers=json_data["headers"])
    return jsonify({"data": data.csv})

@app.route('/api/files/xls', methods=["POST"])
def getXSL():
    json_data = request.json
    app.logger.debug(json.dumps(json_data))
    data = tablib.Dataset(*json_data["data"], headers=json_data["headers"])
    return send_file(data.xls)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
