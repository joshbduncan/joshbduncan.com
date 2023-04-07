---
title: Progress Spinners Using Python Generators and Context Managers
date: 2022-04-01
description: Making neat little progress spinners that let you know things are working in your cli apps is quite simple using Python generators and context manager.
author: Josh Duncan
category: development
tags: python, cli, generators
---

Often with long running scripts, it's nice to know that everything is working as it should. Now, I could easily just print to stdout...

```pycon
>>> for step in steps:
...    print(f"processing {step} of {len(steps)}...")
...    long_running_process()
processing step 1 of 300 steps
processing step 2 of 300 steps
...
processing step 300 of 300 steps
```

But that mucks up my terminal and causes a lot of scrolling.

So, below are three ways I've found to do this, from simple to over engineered... They all write to [stdout](https://docs.python.org/3/library/sys.html#sys.stdout) using the `\r` carriage return so that they keep updating the same line and keep my terminal clean.

## Quick and Simple

My first attempt at this utilized a basic generator that yields defined "ticks" which simulate a spinning line.

```python
import sys

def spinner(msg="working..."):
    i = 0
    ticks = ["-", "\\", "|", "/"]
    while True:
        tick = ticks[i % len(ticks)]
        yield sys.stdout.write(f"\r{tick} {msg}")
        i += 1
```

And I would setup and invoke the generator like below.

```python
jobs = ["sample job", "another job"]
for job in jobs:
    s = spinner(f"processing {job}...")
    try:
        for i in long_running_iteration:
            next(s)
    finally:
        s.close()
```

![Simple Python Spinner](/static/images/spinner-simple-1.gif){: loading="lazy" }

This works, but I see two problems. First, the second job overwrites the first job, and once a job is done, the spinner just ends at the last yielded "tick" which isn't a good look.

### Exiting The Generator

To fix both issues, I'm going to catch the [GeneratorExit](https://docs.python.org/3/library/exceptions.html#GeneratorExit) exception, then place a "✔" before the completed job and jump down a line so that any following output doesn't overwrite the previous output.

```python
import sys

def spinner(msg="working..."):
    i = 0
    ticks = ["-", "\\", "|", "/"]
    try:
        while True:
            tick = ticks[i % len(ticks)]
            yield sys.stdout.write(f"\r{tick} {msg}")
            i += 1
    except GeneratorExit:
        sys.stdout.write("\r✔\n")
    finally:
        sys.stdout.flush()
```

![Simple Python Spinner](/static/images/spinner-simple-2.gif){: loading="lazy" }

### Catching Errors

But what happens when there is an exception?

```console
$ python spinner_simple.py
✔ processing sample job...
✔ processing another job...
✔ processing job with an exception...
Traceback (most recent call last):
  File "/Users/jbd/Dropbox/DEV/projects/progress-spinner/spinner_simple.py", line 31, in <module>
    raise ValueError("test exception")
ValueError: test exception
```

As you can see, even though there was an exception while processing the third job, my spinner still put a "✔" and that's not right.

To fix this, I need to now catch any Exception that is not a GeneratorExit. This allows me to put an "𝘅" at the start of the line for the job that errored and still provide the exception information.

```python
def spinner(msg="working..."):
    ...
    except Exception:
        sys.stdout.write("\r𝘅\n")
        raise
    except GeneratorExit:
        sys.stdout.write("\r✔\n")
    ...
```

![Simple Python Spinner](/static/images/spinner-simple-3.gif){: loading="lazy" }

That looks much better!

Checkout the full [Simple Spinner](https://gist.github.com/joshbduncan/a6a01583292cc7564236a3a1898ce173) script on Github.

## Context Manager

Building on the simple example, I can easily create a [context manager](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager) that generates a progress spinner while being used.

First, I can pull the generator out as a separate function...

```python
def spinner_indicator(msg):
    ticks = ["-", "\\", "|", "/"]
    i = 0
    while True:
        tick = ticks[i % len(ticks)]
        yield sys.stdout.write(f"\r{tick} {msg}")
        i += 1
```

Then, I can and handle all of the setup, exception catching, and tear down inside of the context manager and only call the generator when I need it.

```python
@contextmanager
def spinner(msg="working..."):
    error = False
    try:
        yield spinner_indicator(msg)
    except Exception:
        error = True
        raise
    except GeneratorExit:
        sys.stdout.write("\r✔\n")
    finally:
        if error:
            sys.stdout.write("\r𝘅\n")
        else:
            sys.stdout.write("\r✔\n")
        sys.stdout.flush()
```

This version allows me to do something like below.

```python
jobs = ["sample job", "another job", "job with an exception"]
for job in jobs:
    with spinner(f"processing {job}...") as s:
        for i in long_running_iteration:
            next(s)
```

Not necessarily any better than the simple option, just a different solution.

![Spinner Context Manager](/static/images/spinner-ctx-manager.gif){: loading="lazy" }

Checkout the full [Spinner Context Manager ](https://gist.github.com/joshbduncan/d47726aa351e467d849748e3de607943) script on Github.

## Over The Top

Now, to get extra fancy, I'm going combine what I did above into a Python [Class](https://docs.python.org/3/tutorial/classes.html). The Spinner class will allow me to choose different spinners and also allow me to update the progress message while running.

### Spinners Galore

There are tons of spinners you can come up with but here are the four I'm going to have available for use.

```python
spinners = {
    "angles": ["◢", "◣", "◤", "◥"],
    "circle": ["◜", "◠", "◝", "◞", "◡", "◟"],
    "dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
    "ticks": ["-", "\\", "|", "/"],
}
```

### Class Structure

I have setup the Spinner class so that it can be used both as a standard generator or a context manager.

```python
class Spinner:
    def __init__(self, style=None, text=None):
        if style is None:
            style = "ticks"
        if text is None:
            text = "Processing..."
        self.style = style
        self.text = text
        self._error = False
        self.spinner = self.frame_generator()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            sys.stdout.write("\r𝘅\n")
        else:
            sys.stdout.write("\r✔\n")
        self.spinner.close()
        self._cleanup()

    def frame_generator(self):
        frames = spinners[self.style]
        i = 0
        while True:
            yield frames[i % len(frames)]
            i += 1

    def update(self, text=None):
        if text is not None:
            self.text = text
        sys.stdout.write(f"\r{next(self.spinner)} {self.text}")

    def error(self, error):
        self._error = True
        sys.stdout.write("\r𝘅\n")
        raise

    def close(self):
        if not self._error:
            sys.stdout.write("\r✔\n")
        self.spinner.close()
        self._cleanup()

    @staticmethod
    def _cleanup():
        sys.stdout.flush()
```

<<< .callout
You'll notice a few special dunder methods above, like `__enter__` and `__exit__`. These allow the Spinner class to be used as a [context manager](https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers).
>>>

#### Using Spinner As A Simple Generator

The most basic usage of the Spinner class is to create an instance of it and then update it each iteration. You can specify the spinner style and the spinner text.

```python
import time

jobs = ["dots spinner", "spinner with exception"]
for job in jobs:
    style = job.split(" ")[0] if "exception" not in job else None
    s = Spinner(style=style, text=job)
    steps = 10
    try:
        for i in range(steps):
            s.update()
            time.sleep(0.25)
            if "exception" in job and i == 6:
                raise ValueError("test exception")
    except Exception as e:
        s.error(e)
    finally:
        s.close()
```

![Python Spinner Class](/static/images/spinner-object-3.gif){: loading="lazy" }

You could even update the text at a special place in your job progress.

```python
...
if i == steps // 2:
    s.update("half way through")
...
```

#### Using Spinner As A Context Manager

The Spinner class can also be implemented as a context manager using the standard `with` syntax.

```python
with Spinner() as spinner:
    for i in long_running_iteration:
        spinner.update()
```

![Python Spinner Class](/static/images/spinner-object-1.gif){: loading="lazy" }

And, just as above, you can update the spinner text as you go...

```python
jobs = ["angles spinner", "circle spinner"]
for job in jobs:
    style = job.split(" ")[0]
    with Spinner(style=style) as spinner:
        for i in long_running_iteration:
            spinner.update(f"processing {job} (step {i} of {len(long_running_iteration)})...")
```

![Python Spinner Class](/static/images/spinner-object-2.gif){: loading="lazy" }

Checkout the [full script](https://gist.github.com/joshbduncan/0df382217b6ab761f106e45479708b6c) on Github.

## Final Thoughts

There are much better solutions to this problem like [tqdm](https://github.com/tqdm/tqdm), but since I'm still learning, I like to try and figure out how to do things myself. I definitely learn something each time I do.

Cheers 🍻
