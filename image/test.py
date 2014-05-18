# -*- coding: utf-8 -*-
from processor import *

img = addtext('Estoesuntexto', None, 5)
img.save('test1.jpg')

img = addtext('Estaesuntexto', img, 5)
img.save('test2.jpg')

img = addtext('Estetextoesmaslargo', img, 5)
img.save('test3.jpg')

