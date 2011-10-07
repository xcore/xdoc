from docutils import nodes
from sphinx.util.compat import Directive
from docutils.parsers.rst import directives
import os, subprocess


class squeeze(nodes.General, nodes.Element):
    pass


class SqueezeDirective(Directive):

    has_content = False

    def run(self):
        return [squeeze()]
