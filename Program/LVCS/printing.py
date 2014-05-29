# -*- coding: utf-8 -*-

def print_matrix(matrix):
    print '-' * (len(matrix[0]) +2)
    for r in matrix:
        l = ""
        for c in r:
            l += "X" if c else " "

        print '|' + l + '|'
    print '-' * (len(matrix[0]) +2)


def print_matrixes(m1,m2, info=''):
    i = 0
    if len(info) > 0:
        print info
    print '-' * ((len(m1[0]) + 2) * 2)
    for (r1,r2) in zip(m1,m2):

        l = ""
        for c in r1:
            l += "X" if c else " "

        l += '||'

        for c in r2:
            l += "X" if c else " "


        i += 1

        print '|' + l + '|'
    print '-' * ((len(m1[0]) + 2) * 2)

def print_letter_matrix(matrix):

    print '-' * (len(matrix[0]) +2)
    for r in matrix:
        l = ""
        for c in r:
            l += c

        print '|' + l + '|'
    print '-' * (len(matrix[0]) +2)

