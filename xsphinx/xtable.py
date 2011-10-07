from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.tables import RSTTable

class Table(RSTTable):

    option_spec = {'class': directives.class_option}

    def run(self):
        x = RSTTable.run(self)
        return x
