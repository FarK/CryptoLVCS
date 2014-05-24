# -*- coding: utf-8 -*-
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import random
import itertools
import copy
from printing import *



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

def search_matrix(n,m, k = 2, mindf = 1):
    matrix = []
    for i in range(0, 2):
        matrix.append([])

    matrix_list = []
    #obtain initial matrix 2xn
    search_matrix_aux(matrix, 0, 0, 2, m, k, mindf, matrix_list)
    #filter using partial validation
    b0b1list = itertools.combinations(matrix_list, 2)

    b0b1pairs = []
    for (b0, b1) in b0b1list:
        if security_restriction(b0, b1, 2):
            #print_matrixes(b0, b1, 'Cumple seguridad')
            b0b1pairs.append([b0, b1])
        #else:
        #    print_matrixes(b0, b1, 'NO Cumple seguridad')

    #print n
    for naux in range(2, n):
        matrix_dict = {}
        b0b1pairsaux = []
        for (b0, b1) in b0b1pairs:
            b0 = copy.deepcopy(b0)
            b1 = copy.deepcopy(b1)
            b0.append([])
            b1.append([])

            b0ml = []
            b1ml = []
            #print_matrix(b0)
            b0bin = matrix_to_binary(b0)
            b1bin = matrix_to_binary(b1)

            #print_matrixes(b0, b1, 'Process')
            if b0bin in matrix_dict.keys():
                b0ml = matrix_dict[b0bin]
                #print 'Recover from dict %s'%b0bin
            else:
                search_matrix_aux(b0, naux, 0, naux + 1, m, k, mindf, b0ml)
                matrix_dict[b0bin] = copy.deepcopy(b0ml)

            if b1bin in matrix_dict.keys():
                b1ml = matrix_dict[b1bin]
                #print 'Recover from dict %s'%b1bin
            else:
                search_matrix_aux(b1, naux, 0, naux + 1, m, k, mindf, b1ml)
                matrix_dict[b1bin] = copy.deepcopy(b1ml)


            #print_matrix( b0ml[0])
            for b0 in b0ml:
                for b1 in b1ml:
                    if security_restriction(b0, b1, naux):
                        #print_matrixes(b0,b1,'Cumple seguridad')
                        b0b1pairsaux.append([b0, b1])
                    #else:
                    #    print_matrixes(b0,b1,'NO Cumple seguridad')

            #print 'Finish processing'

        b0b1pairs = copy.deepcopy(b0b1pairsaux)

    result = []
    for (b0, b1) in b0b1pairs:
        if validate(b0, b1, k):
            #print_matrixes(b0,b1,'Valida: %s'%get_diff_factor(b0,b1,k))
            result.append([b0, b1])

    return result


def matrix_to_binary(m):
    binary = 0
    for r in m:
        for c in r:
            val = 1 if c else 0
            binary = (binary | val) << 1

    return binary


def search_matrix_aux(matrix, i, j, n, m, k, mindf, result):
    m1 = copy.deepcopy(matrix)
    m2 = copy.deepcopy(matrix)

    m1[i].append(True)
    m2[i].append(False)

    #print m1
    #print m2
    if j < m - 1:
        j += 1
        search_matrix_aux(m1, i, j, n, m, k, mindf, result)
        search_matrix_aux(m2, i, j, n, m, k, mindf, result)
    elif i < n -1:
        i += 1
        j = 0
        search_matrix_aux(m1, i, j, n, m, k, mindf, result)
        search_matrix_aux(m2, i, j, n, m, k, mindf, result)
    else:
        result.append(m1)
        result.append(m2)

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

def contrast_restriction(b0, b1, k):
    h0 = h_(or_(b0,k))
    h1 = h_(or_(b1,k))

    #print '%s >= %s'%(h0,h1)
    for (vh0,vh1) in zip(h0,h1):
        if vh0 >= vh1:
            return False

    return True


def security_restriction(b0,b1, k):
    for r in range(2,k):
        h0 = h_(or_(b0,r))
        h1 = h_(or_(b1,r))
        if h0 != h1:
            #print '%s != %s'%(h0,h1)
            return False

    return True

def validate(b0, b1, k):
    if not contrast_restriction(b0,b1,k):
        return False

    if not security_restriction(b0,b1,k):
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
