#!/usr/bin/python
import sys
import subprocess
import re
import os
from xdoc_subprocess import call, Popen
def runlatex(path,args):
    cmd = ['pdflatex'] + args

    n = 1
    while True:
        print >>sys.stderr, "Running Latex %d" % n
        n=n+1
        process = Popen(cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        cwd=path)
        lines = process.stdout.readlines()

        found_rerun = False
        for line in lines:
            #print >>sys.stderr,line
            if re.match('.*[rR]e-?run to get.*',line):
                found_rerun = True

        if not found_rerun:
            break

    for i in range(len(lines)):
        if lines[i][0] == '!':
            print >>sys.stderr,''.join(lines[i:i+6])

    return (lines)

if __name__ == "__main__":
    print ''.join(runlatex('.',sys.argv[1:]))
