import mimetypes

from flask import Flask
from flask_flatpages import FlatPages  # type: ignore

from config import Config

from .flask_frozen import Freezer

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)

app.config.from_object(Config)

mimetypes.add_type("application/manifest+json", ".webmanifest")

from . import routes  # noqa: F401 E402
