import fnmatch
import os
import sys
import re

explicit_title_re = re.compile(r'^(.+?)\s*(?<!\x00)<(.*?)>$', re.DOTALL)

paths = ['.']

master = sys.argv[1] + '.rst'
docnum = sys.argv[2]
webgen = (sys.argv[3] == '1')
search_paths = ['.']
if len(sys.argv) > 4:
    for path in sys.argv[4:]:
        path = os.path.join('.linked_dirs',os.path.basename(os.path.abspath(path)))
        search_paths.append(path)


f = open(master);lines = f.readlines();f.close()

toc = []
in_toc = False
toc_indent = None
for line in lines:
    if line[0:12] == '.. toctree::':
        in_toc = True
    elif in_toc and line != '\n':
        indent = len(re.match('( *)',line).groups(0)[0])
        if not toc_indent:
            toc_indent = indent
        if indent != toc_indent:
            break

        line = line.strip()
        m = re.match('.*:part:(.*)',line)
        if m:
            continue
        m = explicit_title_re.match(line)
        if m:
            line = m.group(2)
        toc.append(line)


i = 0
for entry in toc:
    print entry + "___%s" % i
    i += 1



