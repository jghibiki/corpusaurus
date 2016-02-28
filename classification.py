from flask import session, request, jsonify, abort
import tablib
import json
import csv
from os import path

in_data = tablib.Dataset()
out_data = tablib.Dataset()
base_route = "/api/classification/"
out_data_path = None

def load(opts):
    if opts.input_data != None:
        if opts.debug: print("Loading Data")
        with open(opts.input_data, "r") as f:
            reader = csv.reader(f)
            in_data.headers = next(reader)
            for row in reader:
                in_data.append(row)
        if opts.debug: print("Loaded %s rows of data." % len(in_data) )

        if opts.output_header:
            header = opts.output_header
        else:
            header = "data"

        out_data.headers = [ header, "example", "nonexample", "unknown" ]
        fake_row = [ "", 0, 0, 0]

        global out_data_path
        out_data_path = opts.output_data if opts.output_data else "out.csv"

        if not path.exists(out_data_path):
            if opts.debug: print("Create new output file.")
            for row in range(len(in_data)):
                out_data.append(fake_row)

            with open(out_data_path, "w") as f:
                f.write(out_data.csv)
        else:
            if opts.debug: print("Load existing output file.")
            with open(out_data_path, "r") as f:
                reader = csv.reader(f)
                headers = next(reader)
                out_data.headers = headers
                for row in reader:
                    out_data.append((row[0], int(row[1]), int(row[2]), int(row[3])))


def register(app, opts):

    @app.route(base_route + "element/count/", methods=["GET"])
    def getNumberOfElements():
        return jsonify({"result": len(in_data)})

    @app.route(base_route + "element/", methods=["GET"])
    def getElementInSessionRange():
        if "next" in session:
            nxt = session["next"]
            session["current"] = nxt
            element = in_data["tweet"][nxt]
            resp = jsonify({"result": element})
            session["next"] += 1
            return resp
        else:
            abort(400)

    @app.route(base_route + "element/classify/<classification>/", methods=["POST"])
    def setElementClassification(classification):
        if "current" in session:
            current = session["current"]
            element = in_data[current]
            out_element = out_data[current]

            if classification == "example":
                out_data[current] = (element[4], out_element[1]+1, out_element[2], out_element[3])
            elif classification == "nonexample":
                out_data[current] = (element[4], out_element[1], out_element[2]+1, out_element[3])
            elif classification == "unknown":
                out_data[current] = (element[4], out_element[1], out_element[2], out_element[3]+1)

            global out_data_path
            with open(out_data_path, "w") as f:
                f.write(out_data.csv)

            return jsonify({"response": True})




    @app.route(base_route + "range/<int:start>/<int:end>/", methods=["POST"])
    def setRange(start, end):
        session["start"] = start - 1
        session["end"] = end
        session["next"] = start - 1
        session["current"] = None
        return jsonify({"result": True})


