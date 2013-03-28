# -*- coding: utf-8 -*-
import os
import sys
from os import path
import re
import codecs

def do_code_rst_includes(app, docname, source):
    lines = source[0].split('\n')
    for i in range(0,len(lines)):
        line = lines[i]
        m = re.match('.. code_rst_include::\s*([^\s]*)\s*([^\s]*)',line)
        if not m:
            continue

        filename = m.groups(0)[0].strip()
        section = m.groups(0)[1].strip()
        env = app.env
        docdir = path.dirname(env.doc2path(env.docname, base=None))
        dirs = [docdir,os.path.join(docdir,'_build','.sources')]
        if os.path.exists(os.path.join('_build','.sources')):
            dirs += [os.path.join(docdir,'_build','.sources',x) for x in os.listdir(os.path.join('_build','.sources'))]

        fns = [path.join(x, filename) for x in dirs]

        encoding = env.config.source_encoding
        codec_info = codecs.lookup(encoding)
        srclines = None
        for fn in fns:
            if srclines == None:
                try:
                    f = codecs.StreamReaderWriter(open(fn, 'U'),
                                                  codec_info[2], 
                                                  codec_info[3], 'strict')
                    srclines = f.readlines()
                    f.close()
                except (IOError, OSError):
                    pass
                except UnicodeError:
                    return [document.reporter.warning(
                            'Encoding %r used for reading included file %r'
                            'seems to '
                            'be wrong, try giving an :encoding: option' %
                            (encoding, filename))]

        captured = []
        capture = False
        for srcline in srclines:
            if re.match('\/\*\*\*\*%s'%section,srcline):
                capture = True
                continue
            if re.match('.\*\*\*\*\/',srcline):
                capture = False
            if capture:
                captured.append(srcline)

        print ''.join(captured)
        lines[i] = ''.join(captured)

    source[0] = '\n'.join(lines)

