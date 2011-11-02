from xsphinx import miniparse
from docutils import nodes
import sys

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


def command(role, rawtext, text, lineno, inliner, options={}, content={}):
    node = nodes.inline()
    node['classes'].append('cmd')
    node += miniparse(text)
    return [node],[]

def tt(role, rawtext, text, lineno, inliner, options={}, content={}):
    node = nodes.inline()
    node['classes'].append('tt')
    node += miniparse(rawtext[5:-1])
    return [node],[]

