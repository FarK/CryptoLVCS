# -*- coding: utf-8 -*-
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from image.processor import *
from api import *


import sys, getopt

def main(argv):

    try:
        opts, args = getopt.getopt(argv, "m:n:k:f:r:", [])

    except getopt.GetoptError:
        print 'generate_matrix.py -m <number> -n <number> -k <number < n> -f <f> -r <0 or 1>'
        sys.exit(2)

    ran = False
    for opt, arg in opts:
        if opt == '-m':
            m = int(arg)
        elif opt == '-n':
            n = int(arg)
        elif opt == '-k':
            k = int(arg)
        elif opt == '-f':
            df = int(arg)
        elif opt == '-r':
            if arg == '1':
                ran = True
                print 'Random mode'

    if ran:
        generate(m, n, k, df)
    else:
        for (b0,b1) in search_matrix(n,m,k, df):
            factor = get_diff_factor(b0,b1,k)
            valid = True
            for (f,v) in zip(factor,[df] * len(factor)):
                if f < v:
                    valid =False

            if valid:
                print_matrixes(b0,b1)





def generate(m=6,n=3,k=3, df = 2):
    found = False

    while not found:
        (b0, b1) = (get_random_matrix(n, m),
                    get_random_matrix(n, m))


        #(b0,b1) = get_B_3n(3)
        found = validate(b0, b1, k)

        if found:
            factor = get_diff_factor(b0,b1,k)
            for (f,v) in zip(factor,[df] * len(factor)):
                if f < v:
                    found = False


    print 'Difference factors of the permutations: %s'%get_diff_factor(b0, b1, k)
    print_matrix(b0)
    print_matrix(b1)

    print '[['
    for r in b0:
        print '    ',r,','

    print '],['
    for r in b1:
        print '    ',r,','
    print ']]'


if __name__ == "__main__":
   main(sys.argv[1:])

