---
title: Markdown Reference
---

## Markdown

### Post Metadata

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

### Headings

You can use up to up to six levels by writing # at the start of a line; the number of hashtags defines the hierarchy of the heading.

# First level heading
## Second level heading
### Third level heading

```
# First level heading
## Second level heading
### Third level heading
```

### Emphasis

*italic*

    *italic*
    
**bold**

    **bold**
    
***bold-italic***

    ***bold-italic***

### Numbered List

1. Numbered list item
2. Numbered list item

```
1. Numbered list item
2. Numbered list item
```

### Bulleted List

- Bulleted list item (also * or +)
- Bulleted list item

```
- Bulleted list item (also * or +)
- Bulleted list item
```
    
### Nested List

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

        
### Blockquotes

> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque porttitor mi sed maximus hendrerit..
>
> – Someone Cool

    > A quoted passage
    >
    > – Someone Cool

### Links

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

### Images

Both local and web URLs are supported. On export to .docx, currently the image’s alt text is added, but the image is not embedded. Markdown uses the following syntax for images:

![](https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png){: loading="lazy" }

    ![](http://example.com/image.jpg){: loading="lazy" }
    ![](/image.jpg){: loading="lazy" }

**Note:** Markdown image syntax and HTML image filename rules are different from Content Blocks. When using Markdown syntax, spaces must be encoded as %20, and the leading slash must be omitted because it refers to the root directory of a device.

**Also Note:** To force lazy loading prepend `{: loading="lazy" }` to any Markdown image link as above.

### Code Blocks

To create code blocks, indent every line of the block by at least four spaces or one tab.

    This is a code block (start with 4 blank spaces)

#### Fenced Code Block 

The basic Markdown syntax allows you to [create code](https://www.markdownguide.org/basic-syntax#code-blocks) blocks by indenting lines by four spaces or one tab. If you find that inconvenient, try using fenced code blocks. Put with three backticks `(```)` on the lines before and after the code block. The best part? You don’t have to indent any lines!

    ```
    This is a fenced code block
    ```

### Tables

To make a table, use vertical bar characters to denote cells. Start with column headers, separate with a row of cells with hyphens, then add further rows of cells. For example:

| # | Heading | Heading | Heading | 
|---|---------|---------|---------|
| 1 | Cell    | Cell    | Cell    |
| 2 | Cell    | Cell    | Cell    |
| 3 | Cell    | Cell    | Cell    |

### Horizontal Rule

To do so, add three or more asterisks (*), hyphens (-), or underscores (_) on a line by themselves, optionally separated with spaces.

***

    ***, ---, or ___
    
### Comments

Markdown doesn’t have an official syntax for comments. Since HTML is completely valid in Markdown, you can use HTML comments instead:

    <!-- This is a comment -->
    
<!-- This is a comment -->

### “Escaping” formatting characters

If you want to type a formatting character and have Writer treat it as text not formatting, type a backslash first \. This means \* gives *, \_ gives _ etc. Escaping isn’t needed in code blocks.

### YouTube Video Embed

```html
<div class="video-wrapper">
  <iframe src="https://www.youtube.com/embed/Jhh_Dvfs0ro" frameborder="0" allowfullscreen></iframe>
</div>
```

<div class="video-wrapper">
  <iframe src="https://www.youtube.com/embed/Jhh_Dvfs0ro" frameborder="0" allowfullscreen></iframe>
</div>