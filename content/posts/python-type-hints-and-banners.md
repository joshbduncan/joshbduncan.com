---
title: Python Type Hints and Fancy Banners
date: 2021-01-22
description: While leaning about Python Type Hints, I wrote a nifty little function to display cool banners and help remind me about the concepts of type hinting.
category: development
tags: python, type-hints
---

When learning new things in Python, I like to write snippets that I can refer to later when I need a quick refresher.

Recently, while reading about [Python Type Hints][python-type-hints], I wrote a nifty little function to display banners in the terminal.

[python-type-hints]: https://docs.python.org/3/library/typing.html

## Backstory

Back in December, while working on the [2020 Advent of Code][aoc] challenge, I needed an easy way to print what I'm calling "banners" while debugging.

[aoc]: https://adventofcode.com/

If you've participated in an Advent of Code challenge, you know that while solving the challenges, you print lots of information out to the terminal. And, sometimes you need easily recognizable breaks (what I'm calling "banners") in the output (e.g. new branches in a recursion tree).

I usually do something like this...

```pycon
>>> print('*' * 40)
>>> print("Thing I'm looking for")
>>> print('*' * 40)
****************************************
Thing I'm looking for
****************************************
```

Now, there's nothing wrong with this, but it's certainly not pretty.

## Let's Make a Function

First, I'll make a new function 'make_banner()' so it's easy to print new banners when needed.

```python
def make_banner(txt):
    print('*' * 40)
    print(txt)
    print('*' * 40)
```

Now, you just call the function make_banner() and supply your banner text as an argument.

```pycon
>>> make_banner('Provided as an argument')
****************************************
Provided as an argument
****************************************
```

## Adding Styling

Wouldn't it be nice to have the text centered? That's simple enough...

```python
def make_banner(txt):
    print('*' * 40)
    print(' ' * ((40 - len(txt)) // 2) + txt)
    print('*' * 40)
```

Here, I've subtracted the length of the provided text from 40 (the amount of stars), divided that by 2, and added that many spaces before printing the text.

```pycon
>>> make_banner('This is a banner')
****************************************
            This is a banner
****************************************
```

This works, but I notice a few problems.

### Problem #1:

If the supplied text is longer than 40 characters, the border stars '\*' will end before the text.

```pycon
>>> make_banner('This is a really really really long banner!')
****************************************
This is a really really really long banner!
****************************************
```

### Problem #2:

If the supplied text length is a negative number, then the padding on the left and right of the text can't be equal.

```pycon
>>> make_banner('This is a banner!')
****************************************
           This is a banner!
****************************************
```

Notice there are 11 stars '\*' on the left, and 12 on the right. Now, that might not bother you, but as a designer, I just can't 🙈.

### Solution:

The fix for Problem #1 is simple enough and as you'll see and it solves Problem #2 as well.

I'll just take the length of the provided string into account when calculating how many stars to print.

```python
def make_banner(txt):
    print('*' * len(txt))
    print(txt)
    print('*' * len(txt))
```

Running the function give us a better version that works for any length of text and eliminates the centering problem.

```pycon
>>> make_banner('This is a really really really long banner!')
*******************************************
This is a really really really long banner!
*******************************************
```

## Type Hints

Next, I'll make this function super extra fancy with Python's newish type hints ([PEP 484][pep484]).

[pep484]: https://www.python.org/dev/peps/pep-0484/

> It is important for the user to be able to define types in a form that can be understood by type checkers. The goal of this PEP is to propose such a systematic way of defining types for type annotations of variables and functions using PEP 3107 syntax. These annotations can be used to avoid many kind of bugs, for documentation purposes, or maybe even to increase speed of program execution.

Among many things, type hints allow me to specify the type of object my function is expecting to receive. As noted above, this can help with debugging and act as documentation too.

I'll start by specifying that the txt argument should be a string.

```python
def make_banner(txt: str):
    print('*' * len(txt))
    print(txt)
    print('*' * len(txt))
```

By adding ': str' to the function argument, I'm letting myself/user/type checker/IDE know that the function expects a string to be supplied as the argument. Not a list, or an integer, a string. Now, you could provide something other than a string, but that's not what is expected and doing so could cause problems with the function operation.

At this point, I haven't changed the functionality of make_banner(), but I could definitely add some bell and whistles to make it better.

### Optional Arguments

I think the banner would look nicer with padding on each side of the text.

```python
def make_banner(txt: str, padding: int = 5):
    print('*' * (len(txt) + padding * 2))
    print(' ' * padding + txt)
    print('*' * (len(txt) + padding * 2))
```

So, I've added the new argument 'padding' and specified it as an integer with the type hint 'int'. I've also added something else, a default value of 5 '= 5'. This way, if a padding isn't specified in the function call, everything will still look nice.

```pycon
>>> make_banner('A banner with some padding!')
*************************************
     A banner with some padding!
*************************************
```

Since I didn't specify any padding, I get the default of five stars '\*' on each side of the text.

```pycon
>>> make_banner('A banner with MORE padding!', 10)
***********************************************
          A banner with MORE padding!
***********************************************
```

Here, I specified a padding value of 10, so I get ten stars '\*' on each side of my banner text.

Let's keep going by adding an optional argument for the border character.

```python
def make_banner(txt: str, padding: int = 5, border: str = '*'):
    print(border * (len(txt) + padding * 2))
    print(' ' * padding + txt)
    print(border * (len(txt) + padding * 2))
```

This new option allows me to change the border character to anything I want. Like before, I set a default of '\*', so if nothing is specified, I'll get stars. Let's try it...

```pycon
>>> make_banner('A banner with some padding!', 3, '-')
---------------------------------
   A banner with some padding!
---------------------------------
```

Nice! How about a few more?

```pycon
>>> make_banner('A banner with some padding!', 3, '#')
#################################
   A banner with some padding!
#################################

>>> make_banner('A banner with some padding!', 12, '+')
+++++++++++++++++++++++++++++++++++++++++++++++++++
            A banner with some padding!
+++++++++++++++++++++++++++++++++++++++++++++++++++
```

**A few things to note...** If you specify a border that's more than one character, the alignment will be thrown off.

And, even though the 'padding' and 'border' arguments are optional, they must be provided in the order they are defined in the function. If you want to change the border then you must also provide a padding value. So, txt, padding, border, in that order. If you try something like:

```pycon
>>> make_banner('A banner with some padding!', '+')
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

You'll get a TypeError as the function is trying to use the '+' for the padding amount. The workaround for this is simple, just specify which argument you are providing to the function.

```pycon
>>> make_banner(txt='A banner with some padding!', border='+')
+++++++++++++++++++++++++++++++++++++
     A banner with some padding!
+++++++++++++++++++++++++++++++++++++
```

By providing the arguments this way, the order actually doesn't matter at all.

```pycon
>>> make_banner(border='+', padding=10, txt='This is craziness!')
++++++++++++++++++++++++++++++++++++++
          This is craziness!
++++++++++++++++++++++++++++++++++++++
```

### Return Values

You can also specify the return value of your function using type hints. This helps the user know what to expect when running the function.

```python
def make_banner(txt: str, padding: int = 5, border: str = '*') -> str:
    return (
        f'{border * (len(txt) + padding * 2)}\n'
        f'{" " * padding}{txt}\n'
        f'{border * (len(txt) + padding * 2)}'
    )
```

You can see the addition of '-> str:' to the end of the function. This is the letting the user/type checker/IDE know a string will be returned.

To make the function correct, I need to return the banner as a string now instead of just printing it out. This is good practice anyway, as I may want to store a banner as a variable instead of printing it right away. I accomplish this by using Python 3's [f-Strings][f-strings].

[f-strings]: https://docs.python.org/3/reference/lexical_analysis.html#f-strings

Now, to store the banner as a variable I can run:

```pycon
>>> banner = make_banner('Banner as a variable', 4, '#')
```

Then, to print out the new banner I can run:

```pycon
>>> print(banner)
##############################
    Banner as a variable
##############################
```

Or, if I want to print the banner right away I can just put the function call inside of a print statement.

```pycon
>>> print(make_banner('Print me now! :)', 4, '#'))
########################
    Print me now! :)
########################
```

## Taking It Further

This function could definitely be expansed upon... Maybe implementing some coloring, or vertical padding, but I'll save that for another day.

[View the full script here](https://gist.github.com/joshbduncan/f2b7a817b1a3b1e45a131a4fc27d8754)
