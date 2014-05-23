# -*- coding: utf-8 -*-
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import random
import itertools
import string
import math
from PIL import Image
from image.processor import *
from UserString import MutableString

'''
def get_B_23():
    return ([[True, False, False],
             [True, False, False],
             [True, False, False]],
             [[True, False, False],
             [False, True, False],
             [False, False, True]]
            )


def get_B_22():
    return ([[True, False],
             [True, False]],
             [[True, False],
             [False, True]],
            )
'''

#fake version -> B0 all 0
def get_B_23():
    return ([[False, False, False],
             [False, False, False],
             [False, False, False]],
             [[True, False, False],
             [False, True, False],
             [False, False, True]]
            )


def get_B_22():
    return ([[False, False],
             [False, False]],
             [[True, False],
             [False, True]],
            )

# Source: Criptografía Visual Basada en el Esquema de Umbral (2010)
# Mariko Nakano, Enrique Escamilla, Hector Perez, Mitsugu Iwamoto
def get_B_3n(n):
    if n < 3:
        raise ValueError("n should b greater than 2")

    #Bt = one's matrix of (n-2)xn
    rbt = [True] * n
    Bt = [rbt] * (n-2)



    #It is the identity matrix nxn
    It = []
    for i in range(0,n):
        r = []
        for j in range(0,n):
            r.append(False)
        It.append(r)

    for i in reversed(range(0,n)):
        It[i][i] = True


    #B1t = rbt + It
    B1 = transpose(Bt + It)

    #B0 is the complementy of B1
    B0 = []
    for i in range(0,n):
        r = []
        for j in range(0, 2*n -2):
            r.append(not B1[i][j])
        B0.append(r)


    return [B0,B1]




# n = nº de participantes
# m = factor de expansión de cada pixel
# h = umbral para reconocer un 1
# l = umbral para reconocer un 0
# Pre:
#    - h > l
#
def create_B0(n,m, k, h, l):
    #PRE
    if h <= l:
        raise ValueError("h should be greater than l")

    #columns's matrix'
    m = (h-l) * n + l

    print "m=%s"%m

    result = []

    offset = m-h
    ntrues = m-h
    nfalses = h

    for nr in range(0,n):
        result.append(
            generate_truefalse_list(
                nfalses , ntrues, offset
            )
        )


    print_matrix(result)
    return result

# n = nº de participantes
# m = factor de expansión de cada pixel
# h = umbral para reconocer un 1
# l = umbral para reconocer un 0
# Pre:
#    - h > l
#
def create_B1(n,m, k, h, l):
    #PRE
    if h <= l:
        raise ValueError("h should be greater than l")

    #columns's matrix'
    m = (h-l) * n + l

    print "m=%s"%m

    result = []
    off = (h-l) - ((h-l)*(k+1) - (m-l)) / (k+1)
    #off = (h - l) * (k + 1) - (m - l)
    offset = 0
    ntrues = m - h
    nfalses = h - l

    for nr in range(0,n):
        #ntrues=h-l, nfalses=m-(h-l), offset
        result.append(
            generate_truefalse_list(
                nfalses , ntrues, offset
            ) + [False] * l
        )
        offset = offset + off


    print_matrix(result)
    return result

def print_matrix(matrix):
    for r in matrix:
        l = ""
        for c in r:
            l += "X" if c else " "

        print '|' + l + '|'


def print_letter_matrix(matrix):

    print '-' * (len(matrix[0]) +2)
    for r in matrix:
        l = ""
        for c in r:
            l += c

        print '|' + l + '|'
    print '-' * (len(matrix[0]) +2)


# realiza la operacion or sobre todas las permutaciones
# de r filas
def or_operator(matrix, r):
    per = itertools.permutations(matrix,r)

    #return per
    r_final = []
    for p in per:
        result = p[0]

        for r in p:
            aux = []
            for e1,e2 in zip(result, r):

                aux.append(e1 or e2)

            result = aux

        r_final.append(result)

    return r_final

# calcula la distancia de hamming sobre
# cada una de la finas
def h_operator(matrix):

    result = []
    for r in matrix:
        count = 0
        for e in r:
            if e == True:
                count = count + 1

        result.append(count)

    return result

# Genera una lista de booleans con nfalses
# valores a False y ntrues valores a Trues.
# Todos los falses son consecutivos y comienzan
# en la posicion zero_offset. P.e:
#    generate_list(2,6,3)
#    [True,True,True,False,False,True,True,True,True]
#
def generate_truefalse_list(nfalses, ntrues, zero_offset):

    if zero_offset > ntrues:
        raise ValueError(
            "zero_offset (%s) should be less than ntrues (%s)"%
                (zero_offset, ntrues))

    return [True] * zero_offset + \
           [False] * nfalses + \
           [True] * (ntrues - zero_offset)


# h = nº minimo de base (0,1) bits
# l = longitud de la lista
# b = base = 0,1
def generate_binary_list(h, l, b=True):
    #print h
    #print l
    if b == True:
        num1s = random.randint(h, l)
        num0s = l - num1s
    else:
        num0s = random.randint(h, l)
        num1s = l - num0s

    l = [True] * num1s + [False] * num0s

    random.shuffle(l)

    return l

def transpose(matrix):
    return [list(x) for x in zip(*matrix)]

def create_L(b):
    letters = string.ascii_uppercase.replace('I',"")
    r0 = []
    for i in range(0,len(b[0])):
        r0.append(random.choice(letters))

    result = []
    #result.append(r0)
    ri = 0
    upper_case = [letters] * len(b[0])
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

    if k == 3 and n > 2:
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
    '''
    print 'Permutaciones T0'
    for m in t0:
        print_letter_matrix(transpose(m))
    print 'Permutaciones T1'
    for m in t1:
        print_letter_matrix(transpose(m))
    '''
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
            #print create_superpixel(t[i])
            #print t[i]
            result[i].append( create_superpixel(t[i]) )

            #result[i] = result[i] + t[i]
            #for c in t[i]:
            #    result[i] += c
        #print '-----------'

    return result


# Convert a vecto to a superpixel.
# If vector is [A,B,D,E]
# The result is:
#     [[A,B],
#     [D,E]]
def create_superpixel(vector):
    if is_square(len(vector)):
        dim = (int(math.sqrt(int(len(vector)))))

        result = []
        for i in range(0,dim+1,dim):
            result.append(vector[i:i+dim])

        return result

    return [vector]

def is_square(apositiveint):
  x = apositiveint // 2
  seen = set([x])
  while x * x != apositiveint:
    x = (x + (apositiveint // x)) // 2
    if x in seen: return False
    seen.add(x)
  return True


