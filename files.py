import tablib
import json
import csv

def register(app, opts):

    if(opts.debug): print("Registering File Routes.")

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

    @app.route('/api/files/json', methods=["POST"])
    def getJSON():
        json_data = request.json
        app.logger.debug(json.dumps(json_data))
        data = tablib.Dataset(*json_data["data"], headers=json_data["headers"])
        return send_file(data.json)
