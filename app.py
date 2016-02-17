from flask import Flask, request, abort, jsonify
from flask.ext.cors import CORS
from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__, static_url_path='', static_folder='app')
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app, headers=['Content-Type, Authorization'])


