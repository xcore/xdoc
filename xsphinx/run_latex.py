#!/usr/bin/python

import sys
import subprocess
import re

cmd = ['pdflatex'] + sys.argv[1:]

n = 1
while True:
    print >>sys.stderr, "Running Latex %d" % n
    n=n+1
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    lines = process.stdout.readlines()

    found_rerun = False
    for line in lines:
        #print >>sys.stderr,line
        if re.match('.*[rR]e-?run.*',line):
            found_rerun = True

    if not found_rerun:
        break

for i in range(len(lines)):
    if lines[i][0] == '!':
        print >>sys.stderr,''.join(lines[i:i+6])

print ''.join(lines)
