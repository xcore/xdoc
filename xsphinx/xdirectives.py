import os
import subprocess
import re


from docutils import nodes, utils
from sphinx.util.compat import Directive
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.util.nodes import split_explicit_title
from sphinx.locale import _
from sphinx.util import ws_re

class squeeze(nodes.General, nodes.Element):
    pass


class SqueezeDirective(Directive):

    has_content = False

    def run(self):
        return [squeeze()]


