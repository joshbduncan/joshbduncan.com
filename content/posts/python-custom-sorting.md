---
title: Custom Sorting in Python
date: 2021-08-17
description: I recently found myself needing to sort a list by cardinal directions. Here's a super simple solution to do custom sorting in Python.
author: Josh Duncan
category: development
tags: python, sort, sorting
---

While working on my new Python project [Word-Search-Generator](https://github.com/joshbduncan/word-search-generator), I needed a way to do a custom sort based on [cardinal directions](https://en.wikipedia.org/wiki/cardinal_direction) (think compass). I knew I could do it with a custom function and some looping but I wanted to use a Python [built-in function](https://docs.python.org/3/library/functions.html#built-in-functions) if possible.

## The Problem

Depending on the level of the puzzle, words can go in two, four, or eight cardinal directions... But, due to the number of words provided and how they fit into the puzzle, not all directions for each level are always used.

I needed a way to sort all of the directions actually used by words during puzzle generation so that they display in the same order as a compass.

## What I'm Working With

So, I have an answer key for each puzzle that's a dictionary of all contained words along with their start location and direction.

```pycon
>>> key
{"CAT": {"start": (1, 34), "direction": "SE"},
 "CHICKEN": {"start": (46, 26), "direction": "E"},
 "DOG": {"start": (32, 45), "direction": "NE"},
 "ROOSTER": {"start": (32, 12), "direction": "N"},
 "SHEEP": {"start": (30, 2), "direction": "S"},
 "GOAT": {"start": (29, 48), "direction": "W"},
 "HORSE": {"start": (16, 26), "direction": "SE"},
 "LAMB": {"start": (25, 10), "direction": "N"}}
```

## The Solution

First, I need to get all the directions from the dictionary.

```pycon
>>> dirs = {v["direction"] for v in key.values()}
["NE", "N", "S", "W", "SE", "E"]
```

You'll notice that only six of the eight possible cardinal directions were used in this particular puzzle, and if I use the default `sorted()` method they aren't in the order I need them.

```pycon
>>> sorted(dirs)
["E", "N", "NE", "S", "SE", "W"]
```

### A Little Helper

To help out, I setup a new variable which has all eight possible cardinal directions in the order they are on a compass (starting at the top and going clockwise).

```pycon
>>> sort_by = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
```

Now, when we I call `sorted()`, I can provide the [key parameter](https://docs.python.org/3/howto/sorting.html#key-functions) that lets Python know how I want the sorting performed. But I can't just provide `sort_by` as they key. Python requires a "function or other callable".

### Enter Lambdas

The key I'm using to sort by is the [lambda function](https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions) `key=lambda d: sort_by.index(d)`.

!!!!callout
Lambdas are "small anonymous functions" that run a single expression against a provided argument.
!!!!


My lambda takes each direction from `dirs` as variable `d`, looks up its [index](https://docs.python.org/3/tutorial/datastructures.html#data-structures) in `sort_by` and returns that number. Python then uses that number to determine the sorting placement.

## The Result

Finally, if I supply Python's `sorted()` function with my new `key` I get exactly what I was looking for.

```pycon
>>> sorted(dirs, key=lambda d: sort_by.index(d))
["N", "NE", "E", "SE", "S", "W"]
```

👌 Perfecto! If you follow a compass clockwise, you'll find each direction in the correct order.

# Extra Credit

Need a weighted sort based on how many times an item is present?

```pycon
# list to sort by count
>>> dirs = ["W", "N", "E", "W", "E", "W"]
# ascending
>>> sorted(set(dirs), key=lambda d: dirs.count(d))
["N", "E", "W"]
# descending
>>> sorted(set(dirs), key=lambda d: dirs.count(d), reverse=True)
["W", "E", "N"]
```

How about sorting by word length?

```pycon
>>> words = ["nine", "one", "twelve", "seventeen"]
>>> sorted(set(words), key=lambda word: len(word))
["one", "nine", "twelve", "seventeen"]
```

And, if your information is formatted correctly you can use the [Operator Module Functions](https://docs.python.org/3/howto/sorting.html#operator-module-functions) `itemgetter` and `attrgetter`.

```pycon
>>> from operator import itemgetter, attrgetter
>>> student_grades = (("Ella", 76), ("Dave", 92), ("Jess", 97), ("Bob", 84))
# sort students by grade from highest to lowest using itemgetter
>>> sorted(student_grades, key=itemgetter(1), reverse=True)
[("Jess", 97), ("Dave", 92), ("Bob", 84), ("Ella", 76)]
```

Now, using `attrgetter` to sort by a specific object attribute.

```pycon
# setup a Pet class to structure the objects
>>> class Pet:
...     def __init__(self, name, age, weight):
...         self.name = name
...         self.age = age
...         self.weight = weight
...     def __repr__(self):
...         return repr((self.name, self.age, self.weight))
# create some pets
>>> pets = [
...     Pet("Maddie", 8, 62),
...     Pet("Harper", 13, 15),
...     Pet("Greta", 10, 9),
>>> ]
# sort the pets by weight
>>> sorted(pets, key=attrgetter("weight"))
[("Greta", "10", 9), ("Harper", "13", 15), ("Maddie", "8", 62)]
# sort the pets from oldest to youngest
>>> sorted(pets, key=attrgetter("age"), reverse=True)
[("Harper", 13, 15), ("Greta", 10, 9), ("Maddie", 8, 62)]
```

# Final Thoughts

There are many other ways to do sorting in Python but I think these few are pretty slick. Check out the [Python Docs on Sorting](https://docs.python.org/3/howto/sorting.html) for more information and examples. ✌️
