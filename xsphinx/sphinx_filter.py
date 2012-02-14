import sys
import re

class XSphinxFilter(object):

    def __init__(self, stdout, stderr, logfile_path):
        self.output = False
        self.seen_exception = False
        self.seen_debug = False
        self.stdout = stdout
        self.stderr = stderr
        self.logfile = open(logfile_path,"w")
        self.logfile_path = logfile_path

    def finish(self):
        self.logfile.close()
        if self.output:
            self.stdout.write("Full details of errors/warnings can be found in %s\n" % self.logfile_path)

        return self.stdout, self.stderr

    def flush(self):
        self.stdout.flush()

    def write(self, line):
        self.logfile.write(line)
#        self.stdout.write(line)
#        return
        if re.match('Exception.*',line) or re.match('IOError.*',line) or re.match('Configuration error.*',line):
            self.seen_exception = True

        if re.match('.*DEBUG.*',line):
            self.seen_debug = True

        if self.seen_exception or self.seen_debug:
            self.stdout.write(line)
            return

        if not (re.match('.*WARNING.*',line) or \
                re.match('.*ERROR.*',line) or \
                re.match('.*SEVERE.*',line)):
            return

        if re.match('.*included in any toctree.*',line):
            return

        m = re.match(r'.*/([^/:]*):(.*)', line)

        if m:
            line = '%s:%s\n' % (m.groups(0)[0],m.groups(0)[1])

        self.output = True
        self.stdout.write(line)



if __name__ == "__main__":
    filt = XSphinxFilter(sys.stdout,sys.stderr,sys.argv[1])
    while True:
        line = sys.stdin.readline()
        if line == '':
            break
        filt.write(line)
    filt.finish()
    if filt.seen_exception:
        exit(1)
