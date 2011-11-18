
import os
import subprocess
import re
import sys

from docutils import nodes, utils
from sphinx.util.compat import Directive
from docutils.parsers.rst import directives
import docutils.parsers.rst.directives.tables
from sphinx import addnodes
from sphinx.util.nodes import split_explicit_title
from sphinx.locale import _
from sphinx.util import ws_re
import xsphinx

class squeeze(nodes.General, nodes.Element):
    pass


class SqueezeDirective(Directive):

    has_content = False

    def run(self):
        return [squeeze()]

class general_figure(nodes.Element):
    pass

class GeneralFigure(Directive):

    has_content = True

    def run(self):
        fig = general_figure()
        self.state.nested_parse(self.content, self.content_offset, fig)
        if len(fig) < 1 or not isinstance(fig[0],nodes.paragraph):
            print >>sys.stderr, "ERROR: first paragraph of generalfigure should be present for the caption"
            return []

        first_para = fig[0]

        cap = nodes.caption()
        for c in first_para.children:
            cap.append(c.deepcopy())

        txt = cap.astext().strip()
        if re.match('[Tt]he.*',txt):
            print >>sys.stderr, "WARNING: Style: Caption '%s' begins with 'The'" % txt

        fig.remove(first_para)
        fig.append(cap)
        return [fig]



