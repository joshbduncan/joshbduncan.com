from flask import Flask
from flask_flatpages import FlatPages
from flask_frozen import Freezer

from config import Config

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)

app.config.from_object(Config)

from . import routes
