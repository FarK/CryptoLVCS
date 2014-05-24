# -*- coding: utf-8 -*-
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from image.processor import *
from api import *


import sys, getopt

def main(argv):

    try:
        opts, args = getopt.getopt(argv, "m:n:k:f:", [])

    except getopt.GetoptError:
        print 'generate_matrix.py -m <m> -n <n> -k <k>'
        sys.exit(2)

    print opts
    for opt, arg in opts:
        if opt == '-m':
            m = int(arg)
        elif opt == '-n':
            n = int(arg)
        elif opt == '-k':
            k = int(arg)
        elif opt == '-f':
            df = int(arg)

    generate(m, n, k, df)


def generate(m=6,n=3,k=3, df = 2):
    found = False

    while not found:
        (b0, b1) = (get_random_matrix(n, m),
                    get_random_matrix(n, m))


        #(b0,b1) = get_B_3n(3)
        found = validate(b0, b1, k)

        if found:
            factor = get_diff_factor(b0,b1,k)
            if factor < [df] * len(factor):
                found = False


    print get_diff_factor(b0, b1, k)
    print_matrix(b0)
    print_matrix(b1)

    print [b0, b1]


if __name__ == "__main__":
   main(sys.argv[1:])

