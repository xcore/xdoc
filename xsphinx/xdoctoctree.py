from docutils.parsers.rst import Directive, directives
from sphinx.directives.other import TocTree
import re
import os

class XdocTocTree(TocTree):

    def run(self):
        config = self.state.document.settings.env.config

        try:
            linked_dirs = os.environ['OTHER_DOC_DIRS_ABS'].split(' ')
        except:
            linked_dirs = []

        linked_dirs = ['.linked_dirs/'+os.path.split(x)[1] for x in linked_dirs]

        for i in range(len(self.content)):
            path = self.content[i]
            if os.path.exists(self.content[i]+'.rst'):
                continue

            for ld in linked_dirs:
                if os.path.exists(os.path.join(ld, path + '.rst')):
                    print "Found %s in %s" % (path,ld)
                    self.content[i] = os.path.join(ld, path)

        return TocTree.run(self)


