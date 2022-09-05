---
title: Search & Filter HTML Table Data With JavaScript
date: 2022-03-06
description: Searching through HTML tables is super simple using  Vanilla JavaScript, a few query selectors, and some neat methods.
author: Josh Duncan
category: development
tags: javascript, html, search, filter
---

Recently, after building a quick and dirty database reporting portal, a few users requested the ability to easily search/filter the table live on the webpage. Turns out, this is super simple using  Vanilla JavaScript, a few query selectors, and some neat JavaScript methods.

## The Problem

When working with HTML tables that have lots of rows, finding something particular can be a struggle that involves a lot of scrolling. And, not everyone knows you can do Find within the browser.

## The Simple Solution

My first attempt was basic. I typically  start all projects and scripts this way... Start simple, get it working, then add features and/or complexity.

Here's the sample HTML table I'll work from...

```html
<table id="search-table">
  <thead>
    <tr>
      <th>Company</th>
      <th>Contact</th>
      <th>Country</th>
    </tr>
  </thead>
  <tbody>
   <tr>
      <td>Apple</td>
      <td>Steve Jobs</td>
      <td>USA</td>
    </tr>
    <tr>
      <td>Microsoft</td>
      <td>Bill Gates</td>
      <td>USA</td>
    </tr>
    <tr>
      <td>Tesla</td>
      <td>Elon Musk</td>
      <td>Mars</td>
    </tr>
  </tbody>
</table>
```

<<< .callout
Need a refresher on HTML tables? <a href="https://www.w3schools.com/html/html_tables.asp">Check this out</a>.
>>>

### Setup

First, I'll need an input field with the id `search-input` for the user query. Then I'll add the id `search-input` to the table I want to filter. These ids make it easy to select the correct elements in my script. 

```html
<input class="form-control" type="text" id="search-input">
<table id="search-table">
  ...
</table>
```

Now, I can select those two elements inside of my script along with the rows in the table.

```javascript
const searchInput = document.getElementById("search-input");
const searchTable = document.getElementById("search-table");
const rows = searchTable.querySelectorAll("tbody tr");
```

I will also go ahead and setup a custom CSS selector to make it easy to hide any rows that don't match the search query.

```css
.hide {
  display: none;
}
```

### Input Listener

Now that I have everything set up and all key elements selected, I need to listen for input in the `search-input` field. After every keyup, I can set the variable `q` to what the user has typed.

```javascript
searchInput.addEventListener("keyup", function (e) {
  const q = e.target.value.toLowerCase();  
}
```

And, to make searching through the table easier, I converted the user query to lower case using [toLowerCase()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/toLowerCase).

### Iterate Over Every Row

With the user input set to variable `q`, I can iterate over each row using the [.forEach()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach) function to check and see if it contains `q`.

```javascript
rows.forEach((row) => {
  // do something with each row
});
```

### Checking The Text

How do I check all of the text in the row? The simplest solution I could come up with was to combine the text from each cell in the row into a single string. To do that, I grab each `td` element in the row using `row.querySelectorAll("td")`.

Now that I have a NodeList of each cell in the row, I can [map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) the textContent of each cell to a new array called `matchString`.

```javascript
rows.forEach((row) => {
  const cells = row.querySelectorAll("td");
  const matchString = [...cells].map((n) => n.textContent.toLowerCase()).join(" ");
  const match = matchString.includes(q);
  row.classList.toggle("hide", !match);
});
```

<<< .callout
I used the [Spread operator (`...`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to convert the NodeList into an array that JavaScript can apply map() to. This was a new trick I learned during this project. You'll see it used again later in the script.
>>>

You'll notice I did two extra things that I didn't mention above. First, I converted the entire string to lower case to match what I did on the user input. Second I [joined](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/join) the resulting array so that I get a single string of all the content separated by the space character.

Now, I can use the [includes()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/includes) method to check whether the user input is found anywhere in the row.

```javascript
rows.forEach((row) => {
  const cells = row.querySelectorAll("td");
  const matchString = [...cells].map((n) => n.textContent.toLowerCase()).join(" ");
  const match = matchString.includes(q);
});
```

### CSS To The Rescue

Last step, is to hide the rows that don't match using the `.hide` class I created in the beginning.

Using the [toggle()](https://developer.mozilla.org/en-US/docs/Web/API/DOMTokenList/toggle) method, I can add or remove "toggle" a class on any element based off of a variable. I am using the `match` variable here. So, if the row doesn't match the query (`!match`) then toggle on the `.hide` class, if it does match, then toggle off the `.hide` class.

Best part is, this helps me remove the class when the user query changes and a row now matches that previously didn't.

```javascript
rows.forEach((row) => {
  const cells = row.querySelectorAll("td");
  const matchString = [...cells].map((n) => n.textContent.toLowerCase()).join(" ");
  const match = matchString.includes(q);
  row.classList.toggle("hide", !match);
});
```

As is, this script works great for a simple page. Just embed the script at the bottom of a webpage and go on about your day.

[Try it out on CodePen.](https://codepen.io/joshbduncan/pen/wvPYRJb)

But I needed a little more control...

## The Fancy Solution

The portal I was building had lots of pages, and posed two main challenges to the simple script above.

1. Some pages didn't have any tables or an input causing a console error.
2. Some tables had columns that needed to be ignored when filtering.

### No Errors For Me

Getting rid of the script querySelector error is simple. Just wrap everything except the first line in an if statement.

```javascript
const searchInput = document.getElementById("search-input");
if (searchInput != null) {
  ...
}
```

So, if there is no search input just stop, as there is no need to continue.

### Ignoring Columns

Ignoring columns isn't a hard feature addition, I just couldn't decide how I wanted to go about it. I definitely knew I wanted to use [data-attributes](https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes)...

So, I decided that `data-attribute-search-ignore-cols` would be a comma separated list of index ids ([zero based](https://en.wikipedia.org/wiki/Zero-based_numbering)) for the columns that should be ignored (e.g. `data-attribute-search-ignore-cols="0,2,7"`)

<<< .callout
FYI, JavaScript removes the "-" in data-attributes names and coverts the string to camel case <a href="https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes#javascript_access">read more</a>. So `data-attribute-sample-name-with-dashes` becomes `sampleNameWithDashes`.
>>>

```javascript
const ignoreCols = searchTable.dataset.searchIgnoreCols
  ? searchTable.dataset.searchIgnoreCols.split(",").map(Number)
  : false;
```

The above allows me to grab the data-attribute if it is present (doesn't have to be if I want all columns searchable), and convert each column id to an integer using the [map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) method.

Now, while iterating over each row and grabbing the textContent, I can check and make sure if any columns should be ignored using the same [spread synrax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) as above and but paired with the [filter()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter) method this time.

```javascript
const filteredCols = ignoreCols
  ? [...cols].filter((_, n) => ignoreCols && !ignoreCols.includes(n))
  : [...cols];
```

<<< .callout
I mostly program in Python, so maps and filters are a bit new to me but they are very similar to list comprehensions once you get your head around them.
>>>

This filter says, if data-attribute-search-ignore-cols was specified and if the column id `n` is in that array, don't include it in the `filteredCols` array.

### The Home Stretch

With "non-ignored" searchable text now in the array `filteredCols` we can join everything into a string just as before.

```javascript
const colsText = filteredCols
  .map((n) => n.textContent.toLowerCase())
  .join(" ");
```

And, then check to see if the query is contained within the string.

```javascript
row.classList.toggle("hide", !colsText.includes(q));
```

### Putting It All Together

I setup a [full working example](https://codepen.io/joshbduncan/pen/wvPYRJb) over on CodePen if you want to check it out.

```javascript
const searchInput = document.getElementById("search-input");
if (searchInput != null) {
  const searchTable = document.getElementById("search-table");
  const ignoreCols = searchTable.dataset.searchIgnoreCols ? searchTable.dataset.searchIgnoreCols.split(",").map(Number) : false;
  const rows = searchTable.querySelectorAll("tbody tr");
  searchInput.addEventListener("keyup", function (e) {
    const q = e.target.value.toLowerCase();
    rows.forEach((row) => {
      const cols = row.querySelectorAll("td");
      const filteredCols = ignoreCols ? [...cols].filter((_, n) => ignoreCols && !ignoreCols.includes(n)) : [...cols];
      const colsText = filteredCols.map((n) => n.textContent.toLowerCase()).join(" ");
      row.classList.toggle("hide", !colsText.includes(q));
    });
  });
}
```

## Final Thoughts

I'm no JavaScript wizard but this little script has been very handy lately. Hopefully, you can find use for it in one of your projects.

[View the full script with comments on Github.](https://gist.github.com/joshbduncan/87df03c4108c7572155d605a1da00960)
