from xsphinx import miniparse
from docutils import nodes

def subscript(role, rawtext, text, lineno, inliner, options={}, content={}):
    sub = nodes.subscript()
    sub += miniparse(text)
    return [sub],[]


def superscript(role, rawtext, text, lineno, inliner, options={}, content={}):
    sup = nodes.superscript()
    sup += miniparse(text)
    return [sup],[]

def normal(role, rawtext, text, lineno, inliner, options={}, content={}):
    return [nodes.Text(text)], []
