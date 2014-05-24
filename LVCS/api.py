# -*- coding: utf-8 -*-
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import random
import itertools
import string
import math
from image.processor import *
from basis_matrix import *
from printing import *
from utils import *

def create_L(b):
    bad_letters = "IJEFCOQL"
    letters = string.ascii_uppercase

    for bl in bad_letters:
        letters = letters.replace(bl, "")

    r0 = []
    for i in range(0,len(b[0])):
        l = random.choice(letters)
        r0.append(l)
        letters = letters.replace(l, "")

    upper_case = [letters] * len(b[0])

    result = []
    #result.append(r0)
    ri = 0

    #for (uc,ch) in zip(upper_case,r0):
    #    uc = uc.replace(ch,"")

    for r in b[0:]:
        rc = 0
        rnew = []
        #print r
        for c in r:
            letter = random.choice(upper_case[rc]) \
                         if b[ri][rc] else r0[rc]
            upper_case[rc] = upper_case[rc].replace(letter, "")
            rnew.append(letter)

            rc += 1

        result.append(rnew)
        ri += 1

    return result

def LVCS_DVCS(image, channel=0, thresold = 125, k=2, n=3):
    if k == 2 and n == 3:
        b0 = get_B_23()[0]
        b1 = get_B_23()[1]

    if k == 2 and n == 2:
        b0 = get_B_22()[0]
        b1 = get_B_22()[1]

    if k == 3 and n == 3:
        b0 = get_B_33()[0]
        b1 = get_B_33()[1]

    elif k == 3 and n > 2:
        b0 = get_B_3n(n)[0]
        b1 = get_B_3n(n)[1]

    print_matrix(b0)
    print_matrix(b1    )

    sdata = image.getdata()

    result = []
    for i in range(0,len(b0)):
        result.append([])
    #result = [MutableString()] * len(b0)
    #result = [''] * len(b0)

    for p in sdata:
        l0 = create_L(b0)
        l1 = create_L(b1)
        t0 = list(itertools.permutations(transpose(l0)))
        t1 = list(itertools.permutations(transpose(l1)))

        lc = t1 if  p[channel] < thresold else t0

        #get a random matrix
        m = lc[random.randint(0,len(lc)-1)]

        #transpose
        t = transpose( m )

        for i in range(0,len(result)):
            sp = create_superpixel(t[i])
            result[i].append( sp )

    return result


# Convert a vecto to a superpixel.
# If vector is [A,B,D,E]
# The result is:
#     [ [A,B] ,
#       [D,E] ]
def create_superpixel(vector):
    if is_square(len(vector)):
        dim = (int(math.sqrt(int(len(vector)))))

        result = []
        for i in range(0,dim+1,dim):
            result.append(vector[i:i+dim])

        return result

    elif len(vector)%2 == 0:
        rows = int(len(vector) / 2)
        cols = len(vector) / rows

        result = []
        for i in range(0,len(vector), cols):
            result.append(vector[i:i+cols])

        return result

    return [vector]



