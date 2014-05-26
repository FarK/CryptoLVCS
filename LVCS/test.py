# -*- coding: utf-8 -*-
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from api import *
import itertools
from image.processor import *
from PIL import Image

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
