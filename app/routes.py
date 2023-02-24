import demoji
import json
import re
from datetime import datetime

from flask import render_template

from app import app, flatpages, freezer

POST_DIR = app.config["POST_DIR"]
DRAFT_DIR = app.config["DRAFT_DIR"]

STOPWORDS = {
    "the",
    "be",
    "to",
    "of",
    "and",
    "a",
    "in",
    "that",
    "have",
    "I",
    "it",
    "for",
    "not",
    "on",
    "with",
    "he",
    "as",
    "you",
    "do",
    "at",
    "this",
    "but",
    "his",
    "by",
    "from",
    "wikipedia",
    "then",
    "i",
    "an",
    "or",
    "their",
    "what",
    "if",
}


# ----- ROUTES -----#
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@freezer.register_generator
def error_handlers():
    yield "/404.html"


@app.route("/")
def index():
    posts = get_live_posts()
    posts.sort(key=lambda item: item["date"], reverse=True)
    return render_template("posts.html", posts=posts)


@app.route("/<name>.html")
def post(name):
    path = f"{POST_DIR}/{name}"
    post = flatpages.get_or_404(path)
    return render_template("post.html", post=post)


@app.route("/drafts/")
def drafts():
    posts = [post for post in flatpages if post.path.startswith(DRAFT_DIR)]
    posts.sort(key=lambda item: item["date"], reverse=True)
    return render_template("posts.html", posts=posts, filter="drafts")


@app.route("/drafts/<name>.html")
def draft(name):
    path = f"{DRAFT_DIR}/{name}"
    post = flatpages.get_or_404(path)
    return render_template("post.html", post=post, draft=True)


@app.route("/categories.html")
def categories():
    categories = get_all_categories()
    return render_template("categories.html", categories=categories)


@app.route("/category/<category>.html")
def category(category):
    posts = [post for post in get_live_posts() if category == post.meta["category"]]
    posts.sort(key=lambda item: item["date"], reverse=True)
    return render_template("posts.html", posts=posts, filter=category)


@app.route("/tags.html")
def tags():
    tags = get_all_tags()
    return render_template("tags.html", tags=tags)


@app.route("/tag/<tag>.html")
def tagged(tag):
    posts = [post for post in get_live_posts() if tag in get_post_tags(post)]
    posts.sort(key=lambda item: item["date"], reverse=True)
    return render_template("posts.html", posts=posts, filter=tag)


@app.route("/styles.html")
def styles():
    page = flatpages.get_or_404("pages/styles")
    return render_template("page.html", page=page)


@app.route("/about.html")
def about():
    page = flatpages.get_or_404("pages/about")
    return render_template("page.html", page=page)


@app.route("/software.html")
def software():
    page = flatpages.get_or_404("pages/software")
    return render_template("page.html", page=page)


@app.route("/search.html")
def search():
    return render_template("search.html")


@app.route("/search.json")
def json_search():
    posts = get_live_posts()
    posts.sort(key=lambda item: item["date"], reverse=True)
    posts_data = []
    for post in posts:
        body = post.body

        # strip out code blocks
        body = re.sub(r"```([\s\S]*?)\n([\s\S]*?)```", "", body)
        body = re.sub(r"`.*?`", "", body)

        # strip out markdown_div extension tags
        body = re.sub(r"<<<([\s\S]*?)\n", "", body)

        # strip out images
        body = re.sub(r"!\[.*?\]\(.*?\)", "", body)

        # strip out attribute tags
        body = re.sub(r"{:.*?}", "", body)

        # strip out urls (including markdown types)
        body = re.sub(r"\[.*?\]:\s.*\n", "", body)
        body = re.sub(r"\[.*?\]\(.*?\)", "", body)
        body = re.sub(r"\[.*?\]\[.*?\]", "", body)
        # [validation]: https://validator.w3.org/feed/
        body = re.sub(r"\S*https?:\S*", "", body)

        # strip out emoji
        body = demoji.replace(body, "")

        # strip out header tags
        body = re.sub(r"#+\s", " ", body)

        # strip out newlines and extra spaces
        body = re.sub(r"\n", " ", body)
        body = re.sub(r"\s{2,}", " ", body)

        # remove punctuation and get all words in a set minus stopwords
        punctuation = r"!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"  # TODO: remove some items
        body = body.translate(str.maketrans('', '', punctuation)).lower()
        words = set(body.split(" ")) - STOPWORDS - {""}

        # put everything into a dict to send via json
        posts_data.append(
            {
                "title": post.meta["title"],
                "description": post.meta["description"],
                "category": post.meta["category"] or "",
                "tags": post.meta["tags"].split(", "),
                "url": f"https://joshbduncan.com/{post.path.split('/')[-1]}.html",
                "words": " ".join(words),
            }
        )
    return json.dumps(posts_data)


@app.route("/posts.json")
def json_posts():
    posts = get_live_posts()
    posts.sort(key=lambda item: item["date"], reverse=True)
    posts_data = []
    for post in posts:
        # put everything into a dict to send via json
        posts_data.append(
            {
                "title": post.meta["title"],
                "date": post.meta["date"].strftime("%Y-%m-%d"),
                "author": post.meta["author"],
                "description": post.meta["description"],
                "category": post.meta["category"] or "",
                "tags": post.meta["tags"].split(", "),
                "body": post.body,
                "url": f"https://joshbduncan.com/{post.path.split('/')[-1]}.html",
            }
        )
    return json.dumps(posts_data)


@app.route("/tags.json")
def json_tags():
    return json.dumps(get_all_tags())


@app.route("/categories.json")
def json_categories():
    return json.dumps(get_all_categories())


@app.route("/sitemap.xml")
def sitemap():
    posts = get_live_posts()
    categories = get_all_categories()
    tags = get_all_tags() or ""
    posts.sort(key=lambda item: item["date"], reverse=False)
    return render_template("sitemap.xml", posts=posts, categories=categories, tags=tags)


@app.route("/rss.xml")
def rss():
    posts = get_live_posts()
    posts.sort(key=lambda item: item["date"], reverse=True)
    return render_template("rss.xml", posts=posts, build_date=datetime.now())


@app.route("/robots.txt")
def robots():
    return render_template("robots.txt")


# ----- FUNCTIONS -----#
def get_live_posts():
    return [post for post in flatpages if post.path.startswith(POST_DIR)]


def get_draft_posts():
    return [post for post in flatpages if post.path.startswith(DRAFT_DIR)]


def get_all_categories():
    categories = set()
    for post in get_live_posts():
        categories.add(post.meta["category"])
    return sorted(list(categories))


def get_post_tags(post):
    if post.meta["tags"]:
        return sorted(post.meta["tags"].split(", "))


def get_all_tags():
    tags = set()
    for post in get_live_posts():
        for tag in get_post_tags(post):
            tags.add(tag)
    return sorted(list(tags))
