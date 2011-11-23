import sys
import re

output = False
seen_exception = False
seen_debug = False
while True:
    line = sys.stdin.readline()
    if line == '':
        break

    if re.match('Exception.*',line) or re.match('Configuration error.*',line):
        seen_exception = True

    if re.match('.*DEBUG.*',line):
        seen_debug = True

    if seen_exception or seen_debug:
        sys.stdout.write(line)
        continue

    if not (re.match('.*WARNING.*',line) or \
            re.match('.*ERROR.*',line) or \
            re.match('.*SEVERE.*',line)):
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
