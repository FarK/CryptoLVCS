# -*- coding: utf-8 -*-
from processor import *


img1 = addtext('EstoesuntextoEstoesuntextoEstoesuntextoEstoesuntextoEstoesuntextoEstoesuntexto', None, 5)
img1.save('test1.jpg')

img2 = addtext('Estaesuntextoesuntextoesuntextoesuntextoesuntextoesuntextoesuntextoesuntextoesuntexto', None, 5)
img2.save('test2.jpg')

img3 = addtext('EstetextoesmaslargoEstoesuntextoEstoesuntextoEstoesuntextoEstoesuntextoEstoesuntexto', img2, 5)
img3.save('test3.jpg')

img4 = overlaping(img1, img2)
img4.save('test4.jpg')

