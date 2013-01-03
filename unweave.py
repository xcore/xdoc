#!/usr/bin/python
import sys
import re

def unweave(src_lines):
    output_doc = False
    output_code = False
    rst_lines = []

    for line in src_lines:
        finish_output_doc = False

        # A /** at the beginning of the line outputs documentation
        m = re.match('\s*/\*\*\s*(.*)',line)
        if m:
            output_doc = True
            line = m.groups(0)[0]

        # A */ or **/ finishes outputing docs
        m = re.match('(.*?)\*(\*?)/\s*',line)
        if m:
            line = m.groups(0)[0].rstrip()
            finish_output_doc = True
            output_code = (m.groups(0)[1] != "*")
            if output_code:
                if len(line)>0 and line[-1] == ':':
                    line += ':\n'
                else:
                    line += '\n::\n'
            line += '\n'

        if output_doc:
            rst_lines.append(line)
        elif output_code:
            rst_lines.append(" "+line)
        if finish_output_doc:
            output_doc = False

    return rst_lines

if __name__ == "__main__":
    for line in unweave(open(sys.argv[1]).readlines()):
        sys.stdout.write(line)
