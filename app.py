
from flask import Flask

app: Flask = Flask(__name__, template_folder='template', static_folder='static')