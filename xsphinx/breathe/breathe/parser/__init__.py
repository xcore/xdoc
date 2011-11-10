
import breathe.parser.doxygen.index
import breathe.parser.doxygen.compound
import os
import sys

class Parser(object):

    pass


class DoxygenIndexParser(Parser):

    def parse(self, project_info):

        filename = os.path.join(project_info.path(), "index.xml")
        try:
            return breathe.parser.doxygen.index.parse(filename)
        except:
            sys.stderr.write("ERROR: cannot find doxygen information\n")
            exit(1)



class DoxygenCompoundParser(Parser):

    def __init__(self, project_info):

        self.project_info = project_info

    def parse(self, refid):

        filename = os.path.join(self.project_info.path(), "%s.xml" % refid)
        return breathe.parser.doxygen.compound.parse(filename)


class DoxygenParserFactory(object):

    def __init__(self):

        pass

    def create_compound_parser(self, project_info):

        return DoxygenCompoundParser(project_info)



