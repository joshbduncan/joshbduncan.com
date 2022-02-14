import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", "")

    # flatpages configuration
    FLATPAGES_AUTO_RELOAD = "DEBUG"
    FLATPAGES_EXTENSION = ".md"
    FLATPAGES_ROOT = "../content"
    FLATPAGES_MARKDOWN_EXTENSIONS = ["codehilite", "fenced_code", "attr_list", "tables"]
    FLATPAGES_EXTENSION_CONFIGS = {"codehilite": {"guess_lang": False}}

    POST_DIR = "posts"
    DRAFT_DIR = "drafts"

    # freezer static files destination
    FREEZER_DESTINATION = "../build"

    # Ignore MIME warning for type application/xml (sitemap, rss)
    FREEZER_IGNORE_MIMETYPE_WARNINGS = True
