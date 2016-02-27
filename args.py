import argparse

def load():
    parser = argparse.ArgumentParser(description="Classify some dinosaur sized data!")
    parser.add_argument("-p", "--port", default=8000)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("-i", "--input-data")
    parser.add_argument("-o", "--output-data")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--output-headers")
    opts = parser.parse_args()
    return opts

