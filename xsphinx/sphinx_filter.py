import sys
import re

output = False
seen_exception = False
while True:
    line = sys.stdin.readline()
    if line == '':
        break

    if re.match('Exception.*',line):
        seen_exception = True

    if seen_exception:
        sys.stdout.write(line)
        continue

    if not (re.match('.*WARNING.*',line) or \
            re.match('.*ERROR.*',line) or \
            re.match('.*DEBUG.*',line)):
        continue

    if re.match('.*included in any toctree.*',line):
        continue

    m = re.match(r'.*/([^/:]*):(.*)', line)

    if m:
        line = '%s:%s\n' % (m.groups(0)[0],m.groups(0)[1])

    output = True
    sys.stdout.write(line)

if output:
    print "Full details of errors/warnings can be found in _build/.../sphinx.STDERR"

if seen_exception:
    exit(1)
