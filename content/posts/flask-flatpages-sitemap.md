---
title: Generating a Sitemap with Flask and Flask-FlatPages
date: 2020-10-31
description: If you're using Flask-FlatPages, it's really simple to generate a sitemap that plays nice with search engines and helps your website get noticed.
author: Josh Duncan
category: development
tags: python, flask, jinja, flask-flatpages
---

After creating this [Flask][flask] based site, I needed an easy way to generate a sitemap that plays nice with search engines and web crawlers.

[flask]: https://flask.palletsprojects.com/

Since I was using [Flask-FlatPages][flatpages], it was quite simple.

[flatpages]: https://pythonhosted.org/Flask-FlatPages/

## Getting Every Blog Post

First, I created a simple function to return all of my blog posts from Flask-FlatPages. This function only returns blog posts but it could be adapted to return pages as well.

```python
def get_all_posts():
    return [post for post in flatpages if post.path.startswith(POST_DIR)]
```

When I run the function, I get a list of [Page objects][page-objects] for each blog post.

[page-objects]: https://pythonhosted.org/Flask-FlatPages/#flask_flatpages.Page

```pycon
>>> get_all_posts()
[<Page 'posts/post1.html'>, <Page 'posts/post2.html'>]
```

## Adding a New Route

Now I needed a new Flask route to serve requests at '/sitemap.xml'.

```python
@app.route('/sitemap.xml')
def sitemap():
    posts = get_all_posts()
    posts.sort(key=lambda item: item['date'], reverse=False)
    return render_template('sitemap.xml', posts=posts)
```

Once I retrieve my blog posts using the get_all_posts() function, I sort them oldest to newest, then send them to my sitemap.xml template (that I still needed to create).

## Sitemap Basics

A basic sitemap.xml is pretty straightforward. I only need the encoding, a urlset, and then a list of the urls for each of my posts.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>http://www.example.com/</loc>
  </url>
</urlset>
```

!!!!
There are many other xml tags you can include in your file. You can view the entire protocol at [sitemaps.org][sitemaps-protocol].
!!!!

[sitemaps-protocol]: https://www.sitemaps.org/protocol.html

## Sitemap Jinja Template

Here's my final sitemap.xml Jinja template.

```xml
<?xml version="1.0" encoding="utf-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
  <loc>https://www.url.com</loc>
  </url>
  <url>
  <loc>https://www.url.com/about.html</loc>
  </url>
  {% for post in posts %}
  <url>
  <loc>https://www.url.com/{{ post.path }}.html</loc>
  </url>
  {% endfor %}
</urlset>
```

Since my website is simple, I just hardcoded the home and about pages first. Next, I have Jinja iterate through all of the page objects that I provided via my route and the render_template() function.

## Rendered Sitemap

Once rendered, my sitemap.xml looks like this.

```xml
<?xml version="1.0" encoding="utf-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
  <loc>https://www.url.com</loc>
  </url>
  <url>
  <loc>https://www.url.com/about.html</loc>
  </url>
  <url>
  <loc>https://www.url.com/post1.html</loc>
  </url>
  <url>
  <loc>https://www.url.com/post2.html</loc>
  </url>
</urlset>
```

After my home and about pages, each individual post (post1.html, post2.html...) is listed one after another. Every time I add a new blog post it will automatically get added to the bottom.

Well, that wasn't hard at all! Now off, to submit my sitemap.xml to [Google][google].

[google]: https://support.google.com/webmasters/answer/7451001

[View my actual sitemap.xml here.][sitemap]

[sitemap]: https://joshbduncan.com/sitemap.xml
