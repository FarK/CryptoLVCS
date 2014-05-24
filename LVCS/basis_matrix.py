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

########################################################
# GETTERS METHODS
#######################################################
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

def get_B_33():
    return ([[False, True, False, True, False, False],
             [True, True, False, True, False, True],
             [True, False, False, True, False, True]],
            [[True, True, False, False, False, False],
             [False, False, True, True, False, False],
             [False, False, False, False, True, True]]
            )

#difference factor 3
'''
def get_B_33():
    return ([[False, True, True, True, True, False, False, True, False],
             [False, True, True, True, False, False, True, False, False],
             [False, True, True, True, False, False, False, True, False]],
             [[False, True, True, True, True, False, True, False, False],
              [True, False, False, False, False,True, False, True, True],
              [False, False, True, True, True, False, True, False, False],]
            )
'''
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


# Return a matrix nxm of random
# True, False values
def get_random_matrix(n,m):

    result = []
    for r in range(0,n):
        row = []
        for c in range(0,m):
            row.append(random.choice([True, False]))

        result.append(row)

    return result


#########################################################
# DVCS RESTRICCTIONS
#########################################################
# realiza la operacion or sobre todas las permutaciones
# de r filas
def get_diff_factor(b0,b1, k):
    h0 = h_(or_(b0,k))
    h1 = h_(or_(b1,k))

    r = []
    for (v0,v1) in zip(h0,h1):
        r.append(v1-v0)

    return r


def validate(b0, b1, k):
    h0 = h_(or_(b0,k))
    h1 = h_(or_(b1,k))


    #print '%s >= %s'%(h0,h1)
    for (vh0,vh1) in zip(h0,h1):
        if vh0 > vh1:
            return False

    for r in range(2,k):
        h0 = h_(or_(b0,r))
        h1 = h_(or_(b1,r))
        if h0 != h1:
            #print '%s != %s'%(h0,h1)
            return False

    return True



def or_(matrix, r):
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
def h_(matrix):

    result = []
    for r in matrix:
        count = 0
        for e in r:
            if e == True:
                count = count + 1

        result.append(count)

    return result
