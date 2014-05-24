# -*- coding: utf-8 -*-

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

