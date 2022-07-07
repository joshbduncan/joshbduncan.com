from .extension import MarkdownAlerts


def makeExtension(**kwargs):
    return MarkdownAlerts(**kwargs)