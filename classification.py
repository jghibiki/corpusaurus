from flask import session, request, jsonify, abort
import json
import csv
from os import path
from math import floor

data = None
data_path = None
base_route = "/api/classification/"

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

        print("Finished Initializing Output File.")
        exit()

    else:
        if opts.debug: print("Load existing output file.")

        # load output path
        global data_path
        data_path = opts.output_data if opts.output_data else "out.json"

        with open(data_path, "r") as f:
            global data
            data = json.load(f)


def register(app, opts):

    @app.route(base_route + "element/count/", methods=["GET"])
    def getNumberOfElements():
        global data
        return jsonify(result=len(data))

    @app.route(base_route + "element/id/<int:element_id>", methods=["GET"])
    def getElement(element_id):
        element = data[element_id][opts.data_field]
        resp = jsonify(element)
        session["next"] += 1
        return resp

    @app.route(base_route + "element/<string:key_type>/<int:key>/classify/", methods=["POST"])
    def setElementClassification(key_type, key):
        if key_type == "index":
            data[key]["classification"] = request.json["classification"]
        else:
            try:
                for x in data:
                    if key_type in x and x[key_type] == key:
                        data[data.index(x)]["classification"] = request.json["classification"]
            except:
                raise Exception("Invalid key_type in url request.")


        return jsonify(result=True)


    @app.route(base_route + "save/", methods=["GET"])
    def save():
        global data_path
        global data
        with open(data_path, "w") as f:
            json.dump(data, f)
        return jsonify(result=True)


    @app.route(base_route + "element/", defaults={"page": 0, "mask":""}, methods=["GET"])
    @app.route(base_route + "element/page/<int:page>/", defaults={"mask":""}, methods=["GET"])
    @app.route(base_route + "element/mask/<string:mask>/", defaults={"page":0},  methods=["GET"])
    @app.route(base_route + "element/mask/<string:mask>/page/<int:page>/",  methods=["GET"])
    def getElements(page, mask):
        """
            Get a page of elements
        """
        global data
        page_size = 100

        # Apply mask if nessisary
        if mask != "":
            masked_data = [ x for x in data if x["classification"] == mask ]
        else:
            masked_data = data

        max_page = floor(len(masked_data)/page_size)

        if page > max_page:
            page = 0

        start = page_size * page
        end = start + page_size

        page_data = masked_data[start:end]

        return jsonify(data=page_data, page=page, max_page=max_page, page_size=100, mask=mask)


