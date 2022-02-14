import sys

from app import app, freezer

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--build":
            freezer.freeze()
        else:
            exit
    else:
        app.run()
