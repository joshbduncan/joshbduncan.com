import sys
from datetime import datetime

from app import Config, app, flatpages, freezer


@app.context_processor
def inject_year():
    return dict(year=datetime.now().year)


@app.shell_context_processor
def make_shell_context():
    return {
        "app": app,
        "config": Config,
        "freezer": freezer,
        "flatpages": flatpages,
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "--build":
                freezer.freeze()
            case "--run":
                freezer.run()
            case _:
                exit
    else:
        app.run()
