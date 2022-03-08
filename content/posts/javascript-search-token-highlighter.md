---
title: Javascript Search Token Highlighter
date: 2021-05-04
description: Building a search results page? Thinking about highlighting the search terms so they standout? Here's how I did it using vanilla Javascript.
author: Josh Duncan
category: development
tags: javascript, python, flask, jinja
---

While building a full-text search engine for a [Flask][flask] project I'm working on, I wanted a way to highlight all of the search terms on the search results page. After dabbling in Javascript for a bit, here's what I come up with.

[flask]: https://flask.palletsprojects.com/

!!!
Just to be clear, I'm not a Javascript programmer. This is something I was able to hack together for my purposes and it seems to work well. Your milage may vary...
!!!

## TL;DR

If you just want the final script, here it is with all of the specifics of my project removed. Supply a query string however you want and the script will highlight those tokens in each article element on the page.

```javascript
// the query of tokens to highlight
var query = "life social page pursuit";
// add regex '|' "or" character in place of spaces
var tokens = query.replace(/ /g, "|");
// regex to find all matching tokens
var match_tokens = new RegExp(tokens, "gi");
// find all articles on the page
var articles = document.querySelectorAll("[id=article]");
// loop through all found articles elements (articles)
for (var i = 0; i < articles.length; i++) {
  // grab the article quote content
  var content = articles[i].innerHTML;
  // loop over the all token matches in content
  content.match(match_tokens).forEach(function (match, i) {
    // replace regex for all whole word token matches
    var replace_tokens = new RegExp(match + "\\b", "gi");
    // actually replace all token matches in content variable
    content = content.replace(replace_tokens, "<mark>" + match + "</mark>");
  });
  // set the innerHTML of the article to the update content
  articles[i].innerHTML = content;
}
```

## From Python To Javascript

After a visitor successfully submits a search query to my Flask app, I'm capturing their input, sanitizing it, and then passing that query to the search results page as the variable `tokens`.

Once, the search results page is rendered, I can access that variable via [Jinja][jinja] inside of my Javascript script.

[jinja]: https://jinja.palletsprojects.com/

```javascript
var tokens = "{{ tokens }}";
```

## Setting Up For Regex

Since, I'll be utilizing [Regular Expressions (regex)][regex] to find the tokens, I'm going to add regex "or" separators between my tokens using the Jinja [Replace Filter][replace-filter].

[regex]: https://en.wikipedia.org/wiki/Regular_expression
[replace-filter]: https://jinja.palletsprojects.com/en/2.11.x/templates/?highlight=replace#replace

```javascript
var tokens = "{{ tokens|replace(' ', '|') }}"; // add regex '|' "or" character
```

This filter is just like the built-in Python string.replace function, in where it replaces each occurrence of the first argument with the second argument.

You could also do this with the Javascript [string replace method][stringreplace] if you are not using Jinja templates.

[stringreplace]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/replace

```javascript
var tokens = query.replace(/ /g, "|");
```

Original query string from Jinja:

```
$ var tokens = "{{ tokens }}";
$ console.log(tokens)
$ "this is a query"
```

Update query string with regex "or" separators added in:

```
$ var tokens = "{{ tokens|replace(' ', '|') }}";
$ console.log(tokens)
$ "this|is|a|query"
```

!!!
So, regex is an entire language that I'm definitely not going to even scratch the surface of here. If you want to learn more, I suggest the great website [regexr.com][regexr].
!!!

[regexr]: https://regexr.com/

## Cleaning Up The Query

The first issue I encountered were HTML encodings in my string that were added when everything was passed to Jinja.

To remove these, I found a nifty little function from [Rob Wu on StackOverflow][stackoverflow] that strips all HTML encoding so I have a raw string to match.

[stackoverflow]: https://gomakethings.com/decoding-html-entities-with-vanilla-javascript/

```javascript
// remove html encoding from the flask search tokens
// hat tip to https://gomakethings.com/decoding-html-entities-with-vanilla-javascript/
var decodeHTML = function (html) {
  var txt = document.createElement("textarea");
  txt.innerHTML = html;
  return txt.value;
};
```

## Define Regex For Matching Tokens

Since I'll be using regex to find all matching tokens on the page, I'm going to setup a new regular expression that I can apply to my content.

```javascript
var re_quotes = new RegExp(tokens, "gi");
```

!!!
The "gi" options are for "global" search, and "case-insensitive" search". This ensures I find every instance of the search tokens.
!!!

## Limit The Highlights

To make sure I only highlight the search tokens in the areas I want, I'll select all "article" objects on the page.

```javascript
var quotes = document.querySelectorAll("[id=article]");
```

## Time To Loop

Now that I have all the elements I want to apply my highlighter to, I'll need to iterate over them, find the matches, and apply the `<mark>` tag.

### Iterating Over Any Found Matches

Now that I know I have the correct elements selected, I can iterate over each of them, apply the regex I created earlier to find all matching tokens, and then iterate over those matches.

```javascript
for (var i = 0; i < quotes.length; i++) {
  var content = quotes[i].innerHTML;
  content.match(re_quotes).forEach(function (match, i) {
    console.log(match);
  });
}
```

### Setting Up The Replacement Regex

To update the found tokens with the correct html tags, I need to setup a replacement regex that I can apply inside of the string replace function.

```javascript
var re_matches = new RegExp(match + "\\b", "gi");
```

The "\\\b" addition to the token string makes sure I only replace whole word matches.

### Updating The Tokens

With my replacement regex setup, I can apply the string.replace method to my content. This adds the opening `<mark>` and closing `</mark>` html tags to each token match.

```javascript
content = content.replace(re_matches, "<mark>" + match + "</mark>");
```

### Applying The Changes On The Page

Lastly, I need to update the page with the newly highlighted content. I can do this by setting the `innerHTML` of the current quote object of the iteration to the `content` variable.

```javascript
quotes[i].innerHTML = content;
```

## The Final Script

Once again, I'm no Javascript programmer but here's the final working script. It could be shortened a bit by combining some lines and functions, but I find this easier to read and keep up with exactly what's going on.

```javascript
// remove html encoding from the flask search tokens
// hat tip to https://gomakethings.com/decoding-html-entities-with-vanilla-javascript/
var decodeHTML = function (html) {
  var txt = document.createElement("textarea");
  txt.innerHTML = html;
  return txt.value;
};

// grab all search query tokens from flask
// add regex '|' "or" character in place of spaces
var tokens = "{{ query| replace(' ', '|')}}";
// remove html encoding mess from tokens using function above
var tokens = decodeHTML(tokens);
// setup regex to find all matching tokens
var re_quotes = new RegExp(tokens, "gi");
// find all articles/quotes on the page
var quotes = document.querySelectorAll("[id=article]");

// loop through all found articles elements (quotes)
for (var i = 0; i < quotes.length; i++) {
  // grab the article quote content
  var content = quotes[i].innerHTML;
  content.match(re_quotes).forEach(function (match, i) {
    // loop over the all token matches in content
    // replace regex for all whole word token matches
    var re_matches = new RegExp(match + "\\b", "gi");
    // actually replace all token matches
    content = content.replace(re_matches, "<mark>" + match + "</mark>");
  });
  // set quote content to with updated highlighting
  quotes[i].innerHTML = content;
}
```

If you would like to give this a try, you can download the script and accompanying files at the gist below.

[View the full script here](https://gist.github.com/joshbduncan/fc230670837c91dad41683d73cc67d09)
