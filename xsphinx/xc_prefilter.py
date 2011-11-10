import sys, re

# A list of regex substitutions to make
substs =  [ ('port:(\d+)','___port___port___\\1')]


mult_ret_subs = [ ('\{','obrace'),
                  ('\}','cbrace'),
                  (' ','space'),
                  (',','comma'),
                  ('\/\*','ocomment'),
                  ('\*\/','ccomment')]

if __name__ == "__main__":
    """
    This script is run before doxygen (using doxygen's INPUT_FILTER
    property) to handle some awkward XC features. In particular it
    replaces port types with something doxygen can parse.
    """
    in_code_section = False
    fname = sys.argv[1]
    f = open(fname)
    while True:
        x = f.readline()
        x = x.replace('\\code','\\verbatim')
        x = x.replace('\\endcode','\\endverbatim')


        if x == '':
            break
        for pattern, repl in substs:
            x = re.sub(pattern, repl, x)

        m = re.match(r'^\s*\{(.*)\}\s*[^\s\/]',x)
        if m:
            ret_type = m.group(0)
            for pattern, repl in mult_ret_subs:
                ret_type = re.sub(pattern, repl, ret_type)
            x = re.sub(r'\{(.*)\}',"__multret__" + ret_type,x)

        sys.stdout.write(x)
    f.close()
