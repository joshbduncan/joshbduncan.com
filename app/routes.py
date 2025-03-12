import os
import time
from datetime import datetime
from pathlib import Path

import html

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from zoneinfo import ZoneInfo
import xml.etree.cElementTree as ET

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
    # get data for the sitemap
    posts = get_live_posts()
    categories = get_all_categories()
    tags = get_all_tags() or []

    # sort posts by date (oldest first)
    posts.sort(key=lambda item: item["date"], reverse=False)

    # define the XML namespace
    NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
    XHTML_NS = "http://www.w3.org/1999/xhtml"

    # create the root <urlset> element with namespaces
    urlset = ET.Element("urlset", {"xmlns": NS, "xmlns:xhtml": XHTML_NS})

    # helper function to add a URL entry
    def add_url(loc: str, changefreq: str = None):
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = loc
        if changefreq:
            ET.SubElement(url, "changefreq").text = changefreq

    # add the base website URL
    add_url(url_for("index", _external=True), "weekly")

    # add static pages
    add_url(url_for("about", _external=True), "monthly")
    add_url(url_for("software", _external=True), "monthly")

    # add posts
    for post in posts:
        post_url = url_for(
            "post", name=post.path.replace(post.folder, ""), _external=True
        )
        add_url(post_url)

    # add categories
    for category in categories:
        category_url = url_for("category", category=category, _external=True)
        add_url(category_url)

    # add tags
    for tag in tags:
        tag_url = url_for("tagged", tag=tag, _external=True)
        add_url(tag_url)

    # convert the XML tree to a string
    xml_string = ET.tostring(urlset, encoding="utf-8", xml_declaration=True).decode(
        "utf-8"
    )

    return xml_string, 200, {"Content-Type": "application/xml"}


@app.route("/rss.xml")
def rss() -> str:
    def get_rss_pubdate(date: datetime | None = None) -> str:
        """Format a datetime object to RFC-822 format for an RSS `pubDate`.

        Args:
            date (datetime | None): The datetime to format. Defaults to the current time in America/New_York.

        Returns:
            str: RFC-822-compliant date string.
        """
        zone = ZoneInfo("America/New_York")

        if date is None:
            date = datetime.now(zone)
        elif date.tzinfo is None:
            date = date.replace(tzinfo=zone)  # localize if naive

        return date.strftime("%a, %d %b %Y %H:%M:%S %z")

    def make_links_absolute(
        html: str, base_url: str = url_for("index", _external=True)
    ) -> str:
        """Convert all relative links in HTML to absolute URLs."""
        if not html:
            return html  # Return as-is if empty

        soup = BeautifulSoup(html, "html.parser")

        # convert relative <a href=""> links
        for a in soup.find_all("a", href=True):
            a["href"] = urljoin(base_url, a["href"])

        # convert relative <img src=""> links
        for img in soup.find_all("img", src=True):
            img["src"] = urljoin(base_url, img["src"])

        return str(soup)

    def escape_xml(text: str) -> str:
        """Escape special XML characters to prevent parsing errors."""
        if text:
            return html.escape(text)  # Escapes &, <, >, " and '
        return text

    # get all posts sorted by date
    posts = sorted(get_live_posts(), key=lambda item: item["date"], reverse=True)

    # define namespaces
    ATOM_NS = "http://www.w3.org/2005/Atom"
    CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"

    # register namespaces
    ET.register_namespace("atom", ATOM_NS)
    ET.register_namespace("content", CONTENT_NS)

    # create root RSS element with required attributes
    root = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(root, "channel")

    # add site metadata
    ET.SubElement(channel, "title").text = "Josh Duncan - Blog"

    # correct `atom:link` (namespace handling)
    ET.SubElement(
        channel,
        f"{{{ATOM_NS}}}link",
        {
            "href": url_for("rss", _external=True),
            "rel": "self",
            "type": "application/rss+xml",
        },
    )

    ET.SubElement(channel, "link").text = url_for("index", _external=True)
    ET.SubElement(
        channel, "description"
    ).text = "just some random thoughts published on the internet..."
    ET.SubElement(channel, "lastBuildDate").text = get_rss_pubdate()
    ET.SubElement(channel, "language").text = "en-US"

    # add the last 10 posts
    for post in posts[:10]:
        post_url = url_for(
            "post", name=post.path.replace(post.folder, ""), _external=True
        )
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = escape_xml(post.meta["title"])
        ET.SubElement(item, "link").text = post_url
        pub_date = datetime.combine(
            post.meta["date"], datetime.min.time(), ZoneInfo("America/New_York")
        )
        ET.SubElement(item, "pubDate").text = get_rss_pubdate(pub_date)
        ET.SubElement(item, "guid").text = post_url

        # convert links to absolute in description & content
        description_html = make_links_absolute(post.meta["description"])
        content_html = make_links_absolute(post.html)

        # add description (wrapped in CDATA)
        ET.SubElement(item, "description").text = f"<![CDATA[{description_html}]]>"

        # add content:encoded (wrapped in CDATA)
        content_encoded = ET.SubElement(
            item, "{http://purl.org/rss/1.0/modules/content/}encoded"
        )
        content_encoded.text = f"<![CDATA[{content_html}]]>"

    # convert XML to string
    xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")

    # fix the escaping of CDATA sections
    xml_string = xml_string.replace("&lt;![CDATA[", "<![CDATA[").replace(
        "]]&gt;", "]]>"
    )

    # ensure HTML inside CDATA remains untouched
    xml_string = (
        xml_string.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    )

    return xml_string, 200, {"Content-Type": "application/rss+xml"}


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
