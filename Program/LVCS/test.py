# -*- coding: utf-8 -*-
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from api import *
import itertools
from image.processor import *
from PIL import Image

img = Image.open('resources/images/retina32.png')
(w,h) = img.size

print_matrix(get_basis_matrix(n=3,k=3, m=9)[0]) 
print_matrix(get_basis_matrix(n=3,k=3, m=9)[1]) 

shades = DVCS(img, n=3, k=3, m=6)
img1 = get_image(shades[0], w=w, h=h)
img1.save('resources/results/shade1.png', 'PNG')
img2 = get_image(shades[1], w=w, h=h)
img2.save('resources/results/shade2.png', 'PNG')
img3 = get_image(shades[2], w=w, h=h)
img3.save('resources/results/shade3.png', 'PNG')
subresult13 = overlaping(img1,img3)
subresult13.save('resources/results/subresult13.png', 'PNG')
subresult23 = overlaping(img2,img3)
subresult23.save('resources/results/subresult23.png', 'PNG')
subresult12 = overlaping(img1,img2)
subresult12.save('resources/results/subresult12.png', 'PNG')


result = overlaping(img3,subresult12)
result.save('resources/results/result.png', 'PNG')

'''
shades = LVCS_DVCS(img, n=3, k=3, m=9)
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
'''
