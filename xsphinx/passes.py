from docutils import nodes
from xsphinx import miniparse

def format_references(app, doctree, docname):
    for node in doctree.traverse(nodes.reference):
        text = node[0].astext()
        node.pop(0)
        node += miniparse(text)

