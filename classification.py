from flask import session, request, jsonify, abort
import json
import csv
from os import path

data = None
base_route = "/api/classification/"
data_path = None

def load(opts):
    if opts.input_data != None:

        preserve_fields = set()
        # check to see if a data field has been defined else die
        if opts.data_field:
            preserve_fields.add(opts.data_field)
        else:
            raise Exception("--data-field is required when loading from input file.")
        # check to see if there is a list of fields we should preserve
        #  in the output file
        if opts.preserve_fields:
            preserve_fields.update(opts.preserve_fields.split())


        if opts.debug: print("Loading Data")
        with open(opts.input_data, "r") as f:
            global data
            data = json.load(f)

        # clean up un-preserved columns
        bad_keys = set(data[0].keys()) - preserve_fields

        for key in bad_keys:
            for row in data:
                del row[key]

        # add classification field
        for row in data:
            row["classification"] = "none"

        if opts.debug: print("Loaded %s rows of data." % len(data) )

        # load output path
        global data_path
        data_path = opts.output_data if opts.output_data else "out.json"

        # create an base output file
        if not path.exists(data_path):
            if opts.debug: print("Create new output file.")

            with open(data_path, "w") as f:
                json.dump(data, f)

    else:
        if opts.debug: print("Load existing output file.")
        with open(data_path, "r") as f:
            global data
            data = json.load(f)


def register(app, opts):

    @app.route(base_route + "element/count/", methods=["GET"])
    def getNumberOfElements():
        global data
        return jsonify({"result": len(data)})

    @app.route(base_route + "element/", methods=["GET"])
    def getElementInSessionRange():
        if "next" in session:
            nxt = session["next"]
            session["current"] = nxt
            element = data[nxt][opts.data_field]
            resp = jsonify({"result": element})
            session["next"] += 1
            return resp
        else:
            abort(400)

    @app.route(base_route + "element/classify/<classification>/", methods=["POST"])
    def setElementClassification(classification):
        if "current" in session:
            current = session["current"]
            data[current]["classification"] = classification

            # Save every ten elements, should improve performance
            if current % 10 == 0:
                global data_path
                global data
                with open(data_path, "w") as f:
                    json.dump(data, f)

            return jsonify({"response": True})




    @app.route(base_route + "range/<int:start>/<int:end>/", methods=["POST"])
    def setRange(start, end):
        session["start"] = start - 1
        session["end"] = end
        session["next"] = start - 1
        session["current"] = None
        return jsonify({"result": True})


