from flask import Flask, request, abort, jsonify, make_response, send_file
from flask.ext.cors import CORS
from werkzeug.contrib.fixers import ProxyFix

def load():
    app = Flask(__name__, static_url_path='', static_folder='app')
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.secret_key = 'F12Z2r47xj\3ylX R~X@H!jmM]Lwf/,?KT'
    CORS(app, headers=['Content-Type, Authorization'])

    # Add root->index.html alias
    @app.route('/')
    def root():
        return app.send_static_file('index.html')

    return app

