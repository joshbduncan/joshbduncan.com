from .extension import MarkdownContainer


def makeExtension(**kwargs):
    return MarkdownContainer(**kwargs)