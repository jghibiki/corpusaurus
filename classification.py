import tablib
import json
import csv

in_data = tablib.Dataset()
out_data = tablib.Dataset()

def load(opts):
    if opts.input_data == None:
        with open(opts.input_data, "r") as f:
            reader = csv.reader(f)
            in_data_set.headers = next(reader)
            for row in reader:
                in_data_set.append(row)

        if opts.output_headers:
            out_data_set.headers = opts.output_headers.replace(" ", "").split(",")


def register(app, opts):
    pass
