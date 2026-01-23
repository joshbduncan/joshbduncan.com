from .extension import MarkdownDiv

__all__ = ["MarkdownDiv"]


def makeExtension(**kwargs):
    return MarkdownDiv(**kwargs)
