👨‍💻 [joshd.xyz](https://joshd.xyz/)

## Resources

[Jinja — Jinja Documentation (3.0.x)](https://jinja.palletsprojects.com/en/3.0.x/)

[Template Designer Documentation — Jinja Documentation (3.0.x)](https://jinja.palletsprojects.com/en/3.0.x/templates/#builtin-filters)

# 2022-02-14

- html formatting cleanup
- small css updates
- byline on each post
    - will show "Updated" if updated in post meta else "Published"
    - will show post category
- simplified tags on post and tag/categories pages
- added categories to menu
- added author to post meta

# 2022-02-10

- got rid of the git worktree workflow and moved to github actions
- disabled drafts endpoints until I can figure out how to [ignore certain endpoints when freezing](https://github.com/Frozen-Flask/Frozen-Flask/pull/111)

## 2022-02-01

- combined build and app repos into one using git worktree ([Git for Static Sites](http://blog.jenkster.com/2016/02/git-for-static-sites.html))

```
# Create the orphan build branch
$ git checkout --orphan build

# Create at least one commit.
...

# Connect local build to the remote version.
$ git push -u origin build

# Head back to master.
$ git checkout master

# Check out the the orphan build branch in its own directory.
$ git worktree add ../build build


# Finally, from now on, to publish both the source and the release it's just.
$ git push
```

- see comment at bottom of page for cloning (Just to be clear: when you clone this repo from Github, you'll have to manually reinstate the directory structure & worktree)

```
$ git clone https://github.com/USER/REPO app
$ cd app
$ git checkout build
$ git checkout main
$ take build
$ git worktree add ../build build
```

- updated toggle `<input id="toggle" type="checkbox" autocomplete="off" />` so that menu is closed after clicking back button

## 2022-01-21

- complete css/html rewrite
- moved codehilite css to separate file
- cleaned up css and site structure
- cleaned up open graph and meta tags

## 2022-01-20

- cleaned up site structure `<nav> <header> <content> <footer>`
- moved drafts div to post page

## 2022-01-19

- added nav menu
    - add dev specific menu items
- cleaned up css more
- switch classes to ids where possible
- fixed hamburger menu clickable area
- added robots.txt file

## 2022-01-18: Updates

- Updated CSS Tag Buttons [Link](https://codepen.io/wbeeftink/pen/dIaDH)
- Updated jinja tags and categories
- Removed unused render_template data in routes.py
- Cleaned up CSS a bit
- Rewrote dev if statements in base.html
- Added watermark for dev drafts
- Added new header for dev server
- Rebuilt VENV and cleaned up requirements.txt
- Added correct YAML `--- blah ---` to each .md file
- fixed clickable area on header image
- changed classes to ids where correct
- changes post tage to ul/li
