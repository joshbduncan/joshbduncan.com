import os

from dotenv import load_dotenv

from app.md_callouts import MarkdownCallouts

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", "")

    # flatpages configuration
    FLATPAGES_AUTO_RELOAD = "DEBUG"
    FLATPAGES_EXTENSION = ".md"
    FLATPAGES_ROOT = "../content"
    FLATPAGES_MARKDOWN_EXTENSIONS = [
        "codehilite",
        "fenced_code",
        "attr_list",
        "tables",
        MarkdownCallouts(),
    ]
    FLATPAGES_EXTENSION_CONFIGS = {"codehilite": {"guess_lang": False}}

    POST_DIR = "posts"
    DRAFT_DIR = "drafts"

    # freezer static files destination
    FREEZER_DESTINATION = "../build"

    # Ignore MIME warning for type application/xml (sitemap, rss)
    FREEZER_IGNORE_MIMETYPE_WARNINGS = True
