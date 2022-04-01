---
title: Unpacking Tuples in a For Loop
date: 2020-09-28
description: Have you ever noticed as you learn more and more of a programming language, you often forgo the basics for a more complex solution? Well, today I was reminded of the KISS principle when I needed to unpack a bunch of tuples.
author: Josh Duncan
category: development
tags: python, automation
---

Have you ever noticed as you learn more and more of a programming language, you often forgo the basics for a more complex solution? It's the old KISS (Keep It Simple Stupid) principle.

Well, I have to constantly remind myself of this, and here's a real life example...

## Backstory

The other day I was provided a text file full of employee information in tuples.

```
('http://www.url.com/1.png', 'J. DOE', 'DEPT 1', '2020-01-01')
('http://www.url.com/2.png', 'D. JONES', 'DEPT 2', '2020-02-01')
('http://www.url.com/3.png', 'B. SMITH', 'DEPT 3', '2020-03-01')
('http://www.url.com/4.png', 'L. BLUE', 'DEPT 4', '2020-04-01')
```

So, I loaded the file and appended each tuple to a list leaving me with something like this.

```python
employees = [
    ('http://www.url.com/1.png', 'J. DOE', 'DEPT 1', '2020-01-01'),
    ('http://www.url.com/2.png', 'D. JONES', 'DEPT 2', '2020-02-01'),
    ('http://www.url.com/3.png', 'B. SMITH', 'DEPT 3', '2020-03-01'),
    ('http://www.url.com/4.png', 'L. BLUE', 'DEPT 4', '2020-04-01')
]
```

My task was to download each employee picture from the url in the tuple and then save them locally using the remaining information for the file name.

There were 500+ employees, so this would be torture to do manually 😩.

!!!!
I originally started learning Python from the book [Automate the Boring Stuff with Python][automate], and this is a great example of what the it teaches. Enter Python 🐍.
!!!!

[automate]: https://automatetheboringstuff.com/

My first thought was to iterate over the list of tuples and make a dictionary so I could easily access each variable by name... But that's an extra step I didn't need to take.

I could just unpack the tuple values to proper named variables right inside of my for loop.

```pycon
>>> for url, name, dept, date in employees:
...     print(f'Downloading {name} image...')
Downloading J. DOE image...
Downloading D. JONES image...
Downloading B. SMITH image...
Downloading L. BLUE image...
```

As you can see, it's quite easy and definitely more Pythonic to have easily identifiable variable names _(e.g., url, name, dept, date)_.

After re-learning this basic idea, I wondered if this also worked with the [enumerate][enumerate] method. Well, it certainly does.

[enumerate]: https://docs.python.org/3/library/functions.html?highlight=enumerate#enumerate

```pycon
>>> for i, (url, name, dept, date) in employees:
...     print(f'Record {I}: {name} image located @ {url}')
Record 0: J. DOE located @ https://www.url.com/1
Record 1: D. JONES located @ https://www.url.com/2
Record 2: B. SMITH located @ https://www.url.com/3
Record 3: L. BLUE located @ https://www.url.com/4
```

Boom! I've got a built-in iteration counter now too. I'll just pass this information over to my requests function and save myself a few hundred clicks.
