import os
import time
from datetime import datetime
from pathlib import Path

from flask import Response, abort, jsonify, render_template, send_file, url_for
from flask_flatpages import Page  # type: ignore
from jinja2.filters import do_wordcount

from app import app, flatpages, freezer

POST_DIR = app.config["POST_DIR"]
DRAFT_DIR = app.config["DRAFT_DIR"]
PAGE_DIR = app.config["PAGE_DIR"]
PLAYGROUND_DIR = app.config["PLAYGROUND_DIR"]


##########
# ROUTES #
##########


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@freezer.register_generator
def error_handlers():
    yield "/404.html"


@freezer.register_generator
def playground_pages():
    for p in Path().rglob(f"content/{PLAYGROUND_DIR}/**/*"):
        path = str(p).removeprefix("content")
        if p.is_dir():
            path = path + "/"
        yield path


@app.route("/")
def index():
    posts = get_live_posts()
    posts.sort(key=lambda item: item["date"], reverse=True)
    return render_template("posts.html", posts=posts)


@app.route("/<name>.html")
def post(name: str) -> str:
    path = f"{POST_DIR}/{name}"
    post = flatpages.get_or_404(path)
    return render_template("post.html", post=post)


################################
# PLAYGROUND STATIC HTML PAGES #
################################


def playground_path(path: str | Path) -> Path:
    return Path(str(path).removeprefix(f"content/{PLAYGROUND_DIR}/"))


def playground_path_mtime(path: str | Path) -> str:
    return time.ctime(os.path.getmtime(path))


def playground_path_size(path: str | Path) -> str:
    if not isinstance(path, Path):
        path = Path(path)
    return "-" if path.is_dir() else str(os.path.getsize(path))


app.add_template_filter(playground_path)
app.add_template_filter(playground_path_mtime)
app.add_template_filter(playground_path_size)


@app.route("/playground/")
def playground() -> str:
    path = Path(f"content/{PLAYGROUND_DIR}")
    paths = sorted(path.iterdir())
    return render_template("paths.html", base_dir=path, paths=paths)


@app.route("/playground/<path:path>")
def playground_page(path: str) -> str | Response:
    _path = Path(f"content/{PLAYGROUND_DIR}/{path}")
    if not _path.exists():
        abort(404)
    if _path.is_dir():
        return render_template(
            "paths.html",
            base_dir=_path,
            parent_dir=_path.parent.name,
            paths=sorted(_path.iterdir()),
        )
    return send_file(f"../{_path}")


#########
# PAGES #
#########


@app.route("/styles.html")
def styles() -> str:
    path = f"{PAGE_DIR}/styles"
    page = flatpages.get_or_404(path)
    return render_template("page.html", page=page)


@app.route("/about.html")
def about() -> str:
    path = f"{PAGE_DIR}/about"
    page = flatpages.get_or_404(path)
    return render_template("page.html", page=page)


@app.route("/software.html")
def software() -> str:
    path = f"{PAGE_DIR}/software"
    page = flatpages.get_or_404(path)
    return render_template("page.html", page=page)


@app.route("/search.html")
def search() -> str:
    posts = get_live_posts()
    posts.sort(key=lambda item: item["date"], reverse=True)
    return render_template("search.html", posts=posts)


###############
# DRAFT POSTS #
###############


@app.route("/drafts/")
def drafts() -> str:
    posts = [post for post in flatpages if post.path.startswith(DRAFT_DIR)]
    posts.sort(key=lambda item: item["date"], reverse=True)
    return render_template("posts.html", posts=posts, filter="drafts")


@app.route("/drafts/<name>.html")
def draft(name: str) -> str:
    path = f"{DRAFT_DIR}/{name}"
    post = flatpages.get_or_404(path)
    return render_template("post.html", post=post, draft=True)


##############
# META PAGES #
##############


@app.route("/categories.html")
def categories() -> str:
    categories = get_all_categories()
    return render_template("categories.html", categories=categories)


@app.route("/category/<category>.html")
def category(category: str) -> str:
    posts = [post for post in get_live_posts() if category == post.meta["category"]]
    posts.sort(key=lambda item: item["date"], reverse=True)
    return render_template("posts.html", posts=posts, filter=category)


@app.route("/tags.html")
def tags() -> str:
    tags = get_all_tags()
    return render_template("tags.html", tags=tags)


@app.route("/tag/<tag>.html")
def tagged(tag: str) -> str:
    posts = [post for post in get_live_posts() if tag in get_post_tags(post)]
    posts.sort(key=lambda item: item["date"], reverse=True)
    return render_template("posts.html", posts=posts, filter=tag)


#############
# JSON DATA #
#############


@app.route("/posts.json")
def json_posts() -> Response:
    posts = get_live_posts()
    posts.sort(key=lambda item: item["date"], reverse=True)
    posts_data = []
    for post in posts:
        post_path = Path(post.path)
        posts_data.append(
            {
                "title": post.meta["title"],
                "date": datetime.fromisoformat(
                    post.meta["date"].isoformat()
                ).isoformat(),
                "updated": (
                    datetime.fromisoformat(post.meta["updated"].isoformat()).isoformat()
                    if post.meta.get("updated")
                    else None
                ),
                "author": post.meta["author"],
                "description": post.meta["description"],
                "category": post.meta["category"] or "",
                "tags": post.meta["tags"].split(", "),
                "read_time": int(round(do_wordcount(post.body) / (200 / 60))),
                "url": url_for("post", name=post_path.name, _external=True),
                "url_internal": url_for("post", name=post_path.name),
            }
        )
    return jsonify(posts_data)


@app.route("/tags.json")
def json_tags() -> Response:
    return jsonify(get_all_tags())


@app.route("/categories.json")
def json_categories() -> Response:
    return jsonify(get_all_categories())


############
# XML DATA #
############


@app.route("/sitemap.xml")
def sitemap() -> str:
    posts = get_live_posts()
    categories = get_all_categories()
    tags = get_all_tags() or ""
    posts.sort(key=lambda item: item["date"], reverse=False)
    return render_template("sitemap.xml", posts=posts, categories=categories, tags=tags)


@app.route("/rss.xml")
def rss() -> str:
    posts = get_live_posts()
    posts.sort(key=lambda item: item["date"], reverse=True)
    return render_template("rss.xml", posts=posts, build_date=datetime.now())


##########
# ROBOTS #
##########


@app.route("/robots.txt")
def robots() -> str:
    return render_template("robots.txt")


#############
# FUNCTIONS #
#############


def get_pages() -> list[Page]:
    return [page for page in flatpages if page.path.startswith(PAGE_DIR)]


def get_live_posts() -> list[Page]:
    return [post for post in flatpages if post.path.startswith(POST_DIR)]


def get_draft_posts() -> list[Page]:
    return [post for post in flatpages if post.path.startswith(DRAFT_DIR)]


def get_all_categories() -> list[str]:
    categories = set()
    for post in get_live_posts():
        categories.add(post.meta["category"])
    return sorted(list(categories))


def get_post_tags(post: Page) -> list[str]:
    tags = post.meta.get("tags", "")
    return sorted(tags.split(", "))


def get_all_tags():
    tags = set()
    for post in get_live_posts():
        tags.update(set(get_post_tags(post)))
    return sorted(list(tags))
