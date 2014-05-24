# -*- coding: utf-8 -*-
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from api import *
import itertools
from image.processor import *
from PIL import Image

#print generate_truefalse_list(4,1,6)

'''
b1 = create_B1(n=3,m=9,k=3,h=6,l=4)

b0 = create_B0(n=3,m=9,k=3,h=6,l=4)

print "H(OR(B1,3)) = %s"%h_operator(or_operator(b1,3))
print "H(OR(B1,3)) = %s"%h_operator(or_operator(b0,3))

print "H(OR(B1,2)) = %s"%h_operator(or_operator(b1,2))
print "H(OR(B1,2)) = %s"%h_operator(or_operator(b0,2))



b0 = get_B_23()[0]
b1 = get_B_23()[1]


print_matrix(b0)
print_letter_matrix(create_L(b0))

print_matrix(b1)
print_letter_matrix(create_L(b1))

per = itertools.permutations(transpose(create_L(b1)))
for p in  per:
    print print_letter_matrix(transpose(p))
'''


#print_matrix (get_B_3n(3)[0])
#print_matrix (get_B_3n(3)[1])

img = Image.open('resources/images/li.png')
(w,h) = img.size


shades = LVCS_DVCS(img, m=9, n=3, k=3)
print len(shades[0])
#print shades[0]
print h
wr =  int(w*3)
img1 = addtext(shades[0], None, w, rows = h)
img1.save('resources/results/shade1.png', 'PNG')
img2 = addtext(shades[1], None, w, rows = h)
img2.save('resources/results/shade2.png', 'PNG')
result = overlaping(img1,img2)
img3 = addtext(shades[2], None, w, rows = h)
img3.save('resources/results/shade3.png', 'PNG')
result = overlaping(result,img3)

overlaping(img1,img3).save('resources/results/subresult.png', 'PNG')
result.save('resources/results/result.png', 'PNG')
