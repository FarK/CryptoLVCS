# -*- coding: utf-8 -*-
import random

def int_permutation(n):
    result = [0]

    for num in range(0, n):
        i = random.randint(0, num)

        result = result[0:i+1] + [num] + result[i + 1:]


    return result[1:]


def is_square(apositiveint):
  x = apositiveint // 2
  seen = set([x])
  while x * x != apositiveint:
    x = (x + (apositiveint // x)) // 2
    if x in seen: return False
    seen.add(x)
  return True


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
