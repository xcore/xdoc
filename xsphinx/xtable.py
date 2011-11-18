from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.tables import RSTTable
import sys
import re

from docutils import nodes

class Table(RSTTable):

    option_spec = {'class': directives.class_option,
                   'position': directives.unchanged}

    def run(self):
        content = ''
        for x in self.content:
            content += x + "\n"

        if len(self.arguments) > 0 and re.match('[Tt]he.*',self.arguments[0]):
            print >>sys.stderr, "WARNING: Style: Caption '%s' begins with 'The'" % self.arguments[0]

        if content.find('.. raw::') != -1:
            table = nodes.table()
            table['classes'] = ['raw']

            content_split = re.split('.. raw:: (.*)',content)
            content_split = content_split[1:]
            raw_nodes = []
            while content_split != []:
                format = content_split[0]
                text = content_split[1]
                content_split = content_split[2:]

                raw = nodes.raw('',text+"\n",format=format)
                raw_nodes.append(raw)


            table['caption'] = self.arguments[0]

            if 'position' in self.options:
                table['position'] = self.options['position']

            caption = nodes.title()
            caption.append(nodes.Text(self.arguments[0]))

            table.append(caption)
            table += raw_nodes
            return [table]
        else:
           x = RSTTable.run(self)
           return x
