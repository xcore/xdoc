from docutils.parsers.rst import Directive, directives
from sphinx.directives.other import TocTree
import re
import os
import sys

explicit_title_re = re.compile(r'^(.+?)\s*(?<!\x00)<(.*?)>$', re.DOTALL)

class XdocTocTree(TocTree):

    def run(self):
        config = self.state.document.settings.env.config

        try:
            linked_dirs = os.environ['OTHER_DOC_DIRS_ABS'].split(' ')
        except:
            linked_dirs = []

        linked_dirs = ['_build/.linked_dirs/'+os.path.split(x)[1] for x in linked_dirs]

        linked_dirs.append('_build/.linked_dirs')

        partmap = {}
        part = None
        to_remove = 0
        for i in range(len(self.content)):
            line = self.content[i]
            if re.match('\s*$',line):
                self.content = self.content[i:i+1] + self.content[:i] + self.content[i+1:]
                to_remove = to_remove + 1
                continue

            m = re.match('.*:part:(.*)',line)
            if m:
                part = m.groups(0)[0].strip()
                self.content = self.content[i:i+1] + self.content[:i] + self.content[i+1:]
                to_remove = to_remove + 1
                continue

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
                    path = os.path.join(ld, path)
                    if m:
                        self.content[i] = m.group(1) + " <" + path + ">"
                    else:
                        self.content[i] = path

            if part:
                partmap[path] = part
                part = None

        self.content = self.content[to_remove:]
        config = self.state.document.settings.env.partmap = partmap
        return TocTree.run(self)


