---
title: Style Guide
---

**Note:** This website is a work-in-progress. Not all styles are complete so some html elements may still render using the browser defaults.


## Colors
<div id="colors" class="grid">
<span style="color: var(--color-body-color) !important">--color-body-color</span>
<span style="color: var(--color-body-bg) !important">--color-body-bg</span>
<span style="color: var(--color-heading-color) !important">--color-heading-color</span>
<span style="color: var(--color-secondary-color) !important">--color-secondary-color</span>
<span style="color: var(--color-secondary-bg) !important">--color-secondary-bg</span>
<span style="color: var(--color-tertiary-color) !important">--color-tertiary-color</span>
<span style="color: var(--color-tertiary-bg) !important">--color-tertiary-bg</span>
<span style="color: var(--color-emphasis-color) !important">--color-emphasis-color</span>
<span style="color: var(--color-border-color) !important">--color-border-color</span>
<span style="color: var(--color-primary) !important">--color-primary</span>
<span style="color: var(--color-primary-bg-subtle) !important">--color-primary-bg-subtle</span>
<span style="color: var(--color-primary-border-subtle) !important">--color-primary-border-subtle</span>
<span style="color: var(--color-primary-text) !important">--color-primary-text</span>
<span style="color: var(--color-success) !important">--color-success</span>
<span style="color: var(--color-success-bg-subtle) !important">--color-success-bg-subtle</span>
<span style="color: var(--color-success-border-subtle) !important">--color-success-border-subtle</span>
<span style="color: var(--color-success-text) !important">--color-success-text</span>
<span style="color: var(--color-danger) !important">--color-danger</span>
<span style="color: var(--color-danger-bg-subtle) !important">--color-danger-bg-subtle</span>
<span style="color: var(--color-danger-border-subtle) !important">--color-danger-border-subtle</span>
<span style="color: var(--color-danger-text) !important">--color-danger-text</span>
<span style="color: var(--color-warning) !important">--color-warning</span>
<span style="color: var(--color-warning-bg-subtle) !important">--color-warning-bg-subtle</span>
<span style="color: var(--color-warning-border-subtle) !important">--color-warning-border-subtle</span>
<span style="color: var(--color-warning-text) !important">--color-warning-text</span>
<span style="color: var(--color-info) !important">--color-info</span>
<span style="color: var(--color-info-bg-subtle) !important">--color-info-bg-subtle</span>
<span style="color: var(--color-info-border-subtle) !important">--color-info-border-subtle</span>
<span style="color: var(--color-info-text) !important">--color-info-text</span>
<span style="color: var(--color-light) !important">--color-light</span>
<span style="color: var(--color-light-bg-subtle) !important">--color-light-bg-subtle</span>
<span style="color: var(--color-light-border-subtle) !important">--color-light-border-subtle</span>
<span style="color: var(--color-light-text) !important">--color-light-text</span>
<span style="color: var(--color-dark) !important">--color-dark</span>
<span style="color: var(--color-dark-bg-subtle) !important">--color-dark-bg-subtle</span>
<span style="color: var(--color-dark-border-subtle) !important">--color-dark-border-subtle</span>
<span style="color: var(--color-dark-text) !important">--color-dark-text</span>
</div>

## Inline Text Elements
<div id="inline-text-elements" class="grid">
  <p><a href="#">Primary Link</a></p>
  <p><a class="secondary" href="#">Secondary Link</a></p>
  <p><a class="tertiary" href="#">Tertiary Link</a></p>
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
  <button class="btn btn-success" type="button">Success</button>
</div>
<div class="grid">
  <button class="btn btn-warning" type="button">Warning</button>
  <button class="btn btn-danger" type="button">Danger</button>
  <button class="btn btn-info" type="button">Info</button>
</div>

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