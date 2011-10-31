#!/usr/bin/python

import sys
import subprocess
import os

paths = sys.argv[1:]
mapfile = open('.linked_dirs/map','w')
for path in ['.'] + paths:
    process = subprocess.Popen(["git","config","--get","remote.origin.url"],
                               cwd=path,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    err_lines = process.stderr.readlines()
    lines = process.stdout.readlines()


    if lines == []:
            rpath = ""
    else:
            url = lines[0][:-1]
            url = os.path.basename(url)
            rpath = url

    process = subprocess.Popen(["git","rev-parse","--show-prefix"],
                                   cwd=os.path.realpath(path),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

    err_lines = process.stderr.readlines()
    lines = process.stdout.readlines()

    if lines != []:
        rpath = os.path.join(rpath,lines[0][:-2])

    if path == '.':
        mapfile.write(rpath + "\n")
    else:
        mapfile.write(os.path.basename(os.path.abspath(path)) + "," + rpath + "\n")

mapfile.close()

