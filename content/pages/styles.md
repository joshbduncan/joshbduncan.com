---
title: Style Guide
---

**Note:** This website is a work-in-progress. Not all styles are complete so some html elements may still render using the browser defaults.


## Colors
<div id="colors" class="grid">
<span style="color: hsl(var(--hsl-almost-black)) !important" >--hsl-almost-black</span>
<span style="color: hsl(var(--hsl-almost-white)) !important" >--hsl-almost-white</span>
<span style="color: hsl(var(--hsl-black)) !important" >--hsl-black</span>
<span style="color: hsl(var(--hsl-blue)) !important" >--hsl-blue</span>
<span style="color: hsl(var(--hsl-green)) !important" >--hsl-green</span>
<span style="color: hsl(var(--hsl-grey)) !important" >--hsl-grey</span>
<span style="color: hsl(var(--hsl-mint)) !important" >--hsl-mint</span>
<span style="color: hsl(var(--hsl-off-white)) !important" >--hsl-off-white</span>
<span style="color: hsl(var(--hsl-orange)) !important" >--hsl-orange</span>
<span style="color: hsl(var(--hsl-purple)) !important" >--hsl-purple</span>
<span style="color: hsl(var(--hsl-red)) !important" >--hsl-red</span>
<span style="color: hsl(var(--hsl-turquoise)) !important" >--hsl-turquoise</span>
<span style="color: hsl(var(--hsl-violet)) !important" >--hsl-violet</span>
<span style="color: hsl(var(--hsl-white)) !important" >--hsl-white</span>
<span style="color: hsl(var(--hsl-yellow)) !important" >--hsl-yellow</span>
</div>

## Inline Text Elements
<div id="inline-text-elements" class="grid">
  <p><a href="#">Primary Link</a></p>
  <p><a class="secondary" href="#">Secondary Link</a></p>
  <p><a class="contrast" href="#">Contrast Link</a></p>
  <p><b>Bold</b></p>
  <p><em>Italic</em></p>
  <p><u>Underline</u></p>
  <p><del>Deleted</del></p>
  <p><ins>Inserted</ins></p>
  <p><s>Strikethrough</s></p>
  <p><abbr title="Abbreviation">Abbr.</abbr></p>
  <p><kbd>Command + N</kbd></p>
  <p><mark>Highlighted</mark></p>
</div>

## Post Metadata

All pages and posts most contain a [YAML](https://yaml.org/) information section at the top. It can include any information you like but the below format is standard for every post. Values are accessed in [Jinja](https://jinja.palletsprojects.com/) as `{{ post.title }}`.

```yaml
---
title: Post Title
date: 2020-10-23
description: The post description goes here.
author: Author
category: category
tags: tag1, tag2, tag3
---
```

## Markdown Div Plugin

```markdown
<<< #element-id .class1 .class2 data-attribute="test"
This is a paragraph element put inside of an html div.
>>>
```

<<< #element-id .class1 .class2 data-attribute="test"
This is a paragraph element inside of an html div with custom attributes.
>>>

## Callouts

```markdown
<<< .callout
This is a standard callout with a [link](#)!
>>>
```

<<< .callout
This is a standard callout with a [link](#)!
>>>

```markdown
<<< .callout .callout-positive
This is a positive callout with a [link](#)!
>>>
```

<<< .callout .callout-positive
This is a positive callout with a [link](#)!
>>>

```markdown
<<< .callout .callout-negative
This is a negative callout with a [link](#)!
>>>
```

<<< .callout .callout-negative
This is a negative callout with a [link](#)!
>>>

## Headings

You can use up to up to six levels by writing # at the start of a line; the number of hashtags defines the hierarchy of the heading.

# First level heading
## Second level heading
### Third level heading

```
# First level heading
## Second level heading
### Third level heading
```

## Emphasis

*italic*

    *italic*
    
**bold**

    **bold**
    
***bold-italic***

    ***bold-italic***

## Numbered List

1. Numbered list item
2. Numbered list item

```
1. Numbered list item
2. Numbered list item
```

## Bulleted List

- Bulleted list item (also * or +)
- Bulleted list item

```
- Bulleted list item (also * or +)
- Bulleted list item
```
    
## Nested List

* First level
    * Second level

```
* First level
    * Second level
```

1. First level
    1. Second level

```
1. First level
    1. Second level
```

* First level unordered list item
    1. Second level ordered list item

```
* First level unordered list item
    1. Second level ordered list item
```

        
## Blockquotes

> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque porttitor mi sed maximus hendrerit..
>
> – Someone Cool

    > A quoted passage
    >
    > – Someone Cool

## Links

[Google "No Link Description"](https://google.com)  
[Google](https://google.com "Google")

    Inline Link:
    [Link Name](https://google.com) or
    [Link Name](https://google.com "Google")

[Google][]  
[Apple][]  
[Microsoft][]  

[Google]: https://google.com/ "Google"
[Apple]: https://apple.com "Apple"
[Microsoft]: https://microsoft.com "Microsoft"

```
Reference Link:
[Google][]  
[Apple][]  
[Microsoft][]  

[Google]: https://google.com/ "Google"
[Apple]: https://apple.com "Apple"
[Microsoft]: https://microsoft.com "Microsoft"
```

## Images

Both local and web URLs are supported. On export to .docx, currently the image’s alt text is added, but the image is not embedded. Markdown uses the following syntax for images:

![](/static/images/duncan-family.jpg){: loading="lazy" alt="The Duncan Family"}

    ![](http://example.com/image.jpg){: loading="lazy" }
    ![](/image.jpg){: loading="lazy" }

**Note:** Markdown image syntax and HTML image filename rules are different from Content Blocks. When using Markdown syntax, spaces must be encoded as %20, and the leading slash must be omitted because it refers to the root directory of a device.

**Also Note:** To force lazy loading prepend `{: loading="lazy" }` to any Markdown image link as above.

## Code Blocks

To create code blocks, indent every line of the block by at least four spaces or one tab.

    This is a code block (start with 4 blank spaces)

### Fenced Code Block 

The basic Markdown syntax allows you to [create code](https://www.markdownguide.org/basic-syntax#code-blocks) blocks by indenting lines by four spaces or one tab. If you find that inconvenient, try using fenced code blocks. Put with three backticks `(```)` on the lines before and after the code block. The best part? You don’t have to indent any lines!

    ```
    This is a fenced code block
    ```

## Tables

To make a table, use vertical bar characters to denote cells. Start with column headers, separate with a row of cells with hyphens, then add further rows of cells. For example:

<<< .table
| # | Heading | Heading | Heading | Heading | Heading | Heading |
|---|---------|---------|---------|---------|---------|---------|
| 1 | Cell    | Cell    | Cell    | Cell    | Cell    | Cell    |
| 2 | Cell    | Cell    | Cell    | Cell    | Cell    | Cell    |
| 3 | Cell    | Cell    | Cell    | Cell    | Cell    | Cell    |
>>>

## Buttons
<div class="grid">
  <button class="btn" type="button">Primary</button>
  <button class="btn btn-secondary" type="button">Secondary</button>
  <button class="btn btn-contrast" type="button">Contrast</button>
</div>
<div class="grid">
  <button class="btn btn-outline" type="button">Primary outline</button>
  <button class="btn btn-outline-secondary" type="button">Secondary outline</button>
  <button class="btn btn-outline-contrast" type="button">Contrast outline</button>
</div>

## Form Elements
<form>
  <!-- Search -->
  <label for="search">Search</label>
  <input type="search" id="search" name="search" placeholder="Search">

  <!-- Text -->
  <label for="text">Text</label>
  <input type="text" id="text" name="text" placeholder="Text">
  <small>Curabitur consequat lacus at lacus porta finibus.</small>

  <!-- Select -->
  <label for="select">Select</label>
  <select id="select" name="select" required>
    <option value="" selected>Select…</option>
    <option>…</option>
  </select>

  <!-- File browser -->
  <label for="file">File browser
    <input type="file" id="file" name="file">
  </label>

  <!-- Range slider control -->
  <label for="range">Range slider
    <input type="range" min="0" max="100" value="50" id="range" name="range">
  </label>

  <!-- States -->
  <div class="grid">
    <label for="valid">
      Valid
      <input type="text" id="valid" name="valid" placeholder="Valid" aria-invalid="false">
    </label>
    <label for="invalid">
      Invalid
      <input type="text" id="invalid" name="invalid" placeholder="Invalid" aria-invalid="true">
    </label>
    <label for="disabled">
      Disabled
      <input type="text" id="disabled" name="disabled" placeholder="Disabled" disabled>
    </label>
  </div>

  <div class="grid">
    <!-- Date-->
    <label for="date">Date
      <input type="date" id="date" name="date">
    </label>
    <!-- Time-->
    <label for="time">Time
      <input type="time" id="time" name="time">
    </label>
    <!-- Color-->
    <label for="color">Color
      <input type="color" id="color" name="color" value="#0eaaaa">
    </label>
  </div>

  <!-- <div class="grid">
    <fieldset>
      <legend><strong>Checkboxes</strong></legend>
      <label for="checkbox-1">
        <input type="checkbox" id="checkbox-1" name="checkbox-1" checked>
        Checkbox
      </label>
      <label for="checkbox-2">
        <input type="checkbox" id="checkbox-2" name="checkbox-2">
        Checkbox
      </label>
    </fieldset>
    <fieldset>
      <legend><strong>Radio buttons</strong></legend>
      <label for="radio-1">
        <input type="radio" id="radio-1" name="radio" value="radio-1" checked>
        Radio button
      </label>
      <label for="radio-2">
        <input type="radio" id="radio-2" name="radio" value="radio-2">
        Radio button
      </label>
    </fieldset>
    <fieldset>
      <legend><strong>Switches</strong></legend>
      <label for="switch-1">
        <input type="checkbox" id="switch-1" name="switch-1" role="switch" checked>
        Switch
      </label>
      <label for="switch-2">
        <input type="checkbox" id="switch-2" name="switch-2" role="switch">
        Switch
      </label>
    </fieldset>
  </div> -->

  <!-- Buttons -->
  <input type="reset" value="Reset" onclick="event.preventDefault()">
  <input type="submit" value="Submit" onclick="event.preventDefault()">
</form>

## Horizontal Rule

To do so, add three or more asterisks (*), hyphens (-), or underscores (_) on a line by themselves, optionally separated with spaces.

***

    ***, ---, or ___
    
## Comments

Markdown doesn’t have an official syntax for comments. Since HTML is completely valid in Markdown, you can use HTML comments instead:

    <!-- This is a comment -->
    
<!-- This is a comment -->

## “Escaping” formatting characters

If you want to type a formatting character and have Writer treat it as text not formatting, type a backslash first \. This means \* gives *, \_ gives _ etc. Escaping isn’t needed in code blocks.

## YouTube Video Embed

```html
<div class="video-wrapper">
  <iframe src="https://www.youtube.com/embed/Jhh_Dvfs0ro" frameborder="0" allowfullscreen></iframe>
</div>
```

<div class="video-wrapper">
  <iframe src="https://www.youtube.com/embed/Jhh_Dvfs0ro" frameborder="0" allowfullscreen></iframe>
</div>