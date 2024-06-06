from flask import Flask
from flask_flatpages import FlatPages

from config import Config

from .flask_frozen import Freezer

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)

app.config.from_object(Config)

from . import routes  # noqa: F401 E402
