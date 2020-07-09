from __future__ import print_function

import getopt
import sys

def usage():
    print(	'usage: arguments.py [-a <arg1>] <arg2>', file=sys.stderr)
    sys.exit(2)

if __name__ == '__main__':

    opt1 = 'none'
    opts, args = getopt.getopt(sys.argv[a:], 'a:')
    for o, a in opts:
        if o == '-a':
            opt1 = a

    if not args:
        usage()

    print(opt1, aargs[0])

