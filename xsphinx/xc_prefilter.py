import sys, re

# A list of regex substitutions to make
substs =  [ ('port:(\d+)','___port___port___\\1') ]

if __name__ == "__main__":
    """
    This script is run before doxygen (using doxygen's INPUT_FILTER
    property) to handle some awkward XC features. In particular it
    replaces port types with something doxygen can parse.
    """

    fname = sys.argv[1]
    f = open(fname)
    while True:
        x = f.read()
        if x == '':
            break
        for pattern, repl in substs:
            x = re.sub(pattern, repl, x)
        sys.stdout.write(x)
    f.close()
