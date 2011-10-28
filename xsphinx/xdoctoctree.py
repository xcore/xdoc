from docutils.parsers.rst import Directive, directives
from sphinx.directives.other import TocTree
import re
import os


explicit_title_re = re.compile(r'^(.+?)\s*(?<!\x00)<(.*?)>$', re.DOTALL)

class XdocTocTree(TocTree):

    def run(self):
        config = self.state.document.settings.env.config

        try:
            linked_dirs = os.environ['OTHER_DOC_DIRS_ABS'].split(' ')
        except:
            linked_dirs = []

        linked_dirs = ['.linked_dirs/'+os.path.split(x)[1] for x in linked_dirs]

        for i in range(len(self.content)):
            line = self.content[i]
            m = explicit_title_re.match(line)
            if m:
                path = m.group(2)
            else:
                path = line

            if os.path.exists(self.content[i]+'.rst'):
                continue

            for ld in linked_dirs:
                if os.path.exists(os.path.join(ld, path + '.rst')):
                    print "Found %s in %s" % (path,ld)
                    if m:
                        self.content[i] = m.group(1) + " <" + os.path.join(ld, path) + ">"
                    else:
                        self.content[i] = os.path.join(ld, path)

        return TocTree.run(self)


