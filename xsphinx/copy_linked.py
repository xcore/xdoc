#!/usr/bin/python

import sys
import os
import shutil
paths = sys.argv[1:]

def ignore_me(src, names):
    ignore = set()
    for name in names:
        if os.path.samefile(os.path.join(src,name),'.'):
            ignore.add(name)
    return ignore

for path in paths:
    name = os.path.basename(os.path.abspath(path))
    shutil.copytree(path,os.path.join('.linked_dirs',name),ignore=ignore_me)

