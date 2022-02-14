---
title: RSS Feeds Using Flask-FlatPages
date: 2020-11-11
description: Need to generate a valid RSS feed for your Flask website? Using Flask-FlatPages? Well, it's really quite simple.
author: Josh Duncan
category: development
tags: python, flask, jinja, flask-flatpages
---

After learning how easy it was to [generate a sitemap][sitemap] with [Flask][flask] and [Flask-FlatPages][flatpages], I decided to use the same technique to generate a valid RSS feed too.

[sitemap]: https://joshd.xyz/flask-flatpages-sitemap.html
[flask]: https://flask.palletsprojects.com/
[flatpages]: https://pythonhosted.org/Flask-FlatPages/

## Getting Every Blog Post

Just like in the [sitemap][sitemap] tutorial, I'm grabbing all of my blog posts from Flask-FlatPages using the get_all_posts() function I wrote.

```python
def get_all_posts():
    return [post for post in flatpages if post.path.startswith(POST_DIR)]
```

Running the function gets me a list of every blog posts as a [Page object][page-object].

[page-object]: https://pythonhosted.org/Flask-FlatPages/#flask_flatpages.Page

```pycon
>>> get_all_posts()
[<Page 'posts/post1.html'>, <Page 'posts/post2.html'>]
```

## Adding a New Route

Now I needed a new Flask route to serve requests at '/rss.xml'.

```python
@app.route('/rss.xml')
def rss():
    posts = get_all_posts()
    posts.sort(key=lambda item: item['date'], reverse=True)
    return render_template('rss.xml', posts=posts, build_date=datetime.now())
```

Once I retrieve my blog posts, I sort them newest to oldest, then send them to my rss.xml template along with the current date and time from Python's [datetime module][datetime].

[datetime]: https://docs.python.org/3/library/datetime.html

## RSS Basics

[RSS][rss] or Really Simple Syndication, is a web feed that allows users and applications to access updates to websites in a standardized, computer-readable format.

[rss]: https://en.wikipedia.org/wiki/RSS

As with a sitemap, there's not much to a valid RSS feed. Provide the encoding and rss version, then include your website/feed information, and finally provide your blog posts as xml items.

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>RSS Title</title>
  <description>This is an example of an RSS feed</description>
  <link>http://www.example.com/main.html</link>
  <lastBuildDate>Mon, 06 Sep 2010 00:01:00 +0000</lastBuildDate>
    <item>
    <title>Example entry</title>
    <description>Here is some text containing an interesting description.</description>
    <link>http://www.example.com/blog/post/1</link>
    <guid isPermaLink="false">7bd204c6-1655-4c27-aeee-53f933c5395f</guid>
    <pubDate>Sun, 06 Sep 2009 16:20:00 +0000</pubDate>
    </item>
</channel>
</rss>
```

## RSS Jinja Template

To generate the final RSS xml document I needed to create a Jinja template that could format the page objects I sent through the render_template function.

```xml
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>joshd.xyz</title>
  <atom:link href="https://joshd.xyz/rss.xml" rel="self" type="application/rss+xml" />
  <link>https://joshd.xyz</link>
  <description>just some random thoughts published on the internet...</description>
  <lastBuildDate>{{ build_date.strftime('%a, %d %b %Y %T') }} EST</lastBuildDate>
  <language>en-US</language>
  {% for post in posts %}
  <item>
  <title>{{ post.meta['title'] }}</title>
  <link>https://joshd.xyz/{{ post.path.split('/')[-1] }}.html</link>
  <description>{{ post.meta['description'] }}</description>
  <pubDate>{{ post.meta['date'].strftime('%a, %d %b %Y %T') }} EST</pubDate>
  </item>
  {% endfor %}
</channel>
</rss>
```

As you can see, the first section is my website and feed information. All of this is hardcoded except for the lastBuildDate which is the current date and time that I passed in my Flask route.

> The dates and times in your RSS feed need to match the [RFC822 standard][rfc822]. I have Jinja format the date and time information from Python into the correct format using the [strftime][strftime] (string from time) function.

[rfc822]: https://www.w3.org/Protocols/rfc822/#z28
[strftime]: https://jinja.palletsprojects.com/en/2.11.x/api/

Next, I have Jinja iterate through all of the page objects that I provided via my route to create each xml item. Each item entry needs to include a title, permalink, description, and publication date.

## Rendered RSS Feed

Once rendered, my rss.xml feed looks like this.

```xml
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>joshd.xyz</title>
  <atom:link href="https://www.url.com/rss.xml" rel="self" type="application/rss+xml" />
  <link>https://www.url.com</link>
  <description>just some random thoughts published on the internet...</description>
  <lastBuildDate>Tue, 03 Nov 2020 17:11:23 EST</lastBuildDate>
  <language>en-US</language>
  <item>
    <title>Post 2 Title</title>
    <link>https://www.url.com/pots2.html</link>
    <description>Post 2 Description</description>
    <pubDate>Mon, 02 Nov 2020 17:11:23 EST</pubDate>
  </item>
  <item>
    <title>Post 1 Title</title>
    <link>https://www.url.com/pots1.html</link>
    <description>Post 1 Description</description>
    <pubDate>Tue, 03 Nov 2020 17:11:23 EST</pubDate>
  </item>
</channel>
</rss>
```

After my website/feed info, each individual post (post2.html, post1.html...) is listed one after another. Every time I add a new blog post it will automatically get added to top of the list.

## Validation

To make sure my new RSS feed gets along with all of the RSS apps and services, I need to validate it. It's really simple using the [W3C Feed Validation Service][validation].

[validation]: https://validator.w3.org/feed/

![Valid RSS Feed](https://validator.w3.org/feed/images/valid-rss-rogers.png){: class="blog-img-left" loading="lazy" }

Boom, I'm valid! I even got this cute little badge!

## Final Thoughts

Eventually, I may limit the number of posts listed in my RSS feed (thinking maybe 10 or so), but since I'm just starting this website I’m going to leave them all in there for now.

[View my actual RSS feed here.][rss]

[rss]: https://joshd.xyz/rss.xml
