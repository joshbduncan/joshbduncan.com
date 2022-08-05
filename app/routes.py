from datetime import datetime

from flask import render_template

from app import app, flatpages, freezer

POST_DIR = app.config["POST_DIR"]
DRAFT_DIR = app.config["DRAFT_DIR"]


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
    return render_template(
        "posts.html", posts=posts, filter=category)


@app.route("/tags.html")
def tags():
    tags = get_all_tags()
    return render_template("tags.html", tags=tags)


@app.route("/tag/<tag>.html")
def tagged(tag):
    posts = [post for post in get_live_posts() if tag in get_post_tags(post)]
    posts.sort(key=lambda item: item["date"], reverse=True)
    return render_template("posts.html", posts=posts, filter=tag)


@app.route("/about.html")
def about():
    page = flatpages.get_or_404("pages/about")
    return render_template("page.html", page=page)


@app.route("/search.html")
def search():
    categories = get_all_categories()
    tags = get_all_tags()
    return render_template("search.html", categories=categories, tags=tags)


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
