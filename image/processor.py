# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def addtext(text, image, cols, font_size = 16):
    rows = int(len(text) / cols) + 1
    black = (0,0,0)
    if image is None:
        # create image
        image = createimage(rows, cols, font_size)

    else:
        # check the size
        (wn, hn) = (rows * font_size, cols * font_size)
        (w, h) = image.size

        #canvas resizing if it is neccesary
        print (w, h)
        print (wn, hn)
        if w < wn or h < hn:
            img = createimage(rows, cols, font_size)
            img.paste(image, (0, 0, w, h))
            image = img

    #load font
    font = ImageFont.truetype("DejaVuSans.ttf", font_size)

    #draw object to write the text
    draw = ImageDraw.Draw(image)
    index = 0


    for r in range(0,rows):
        for c in range(0,cols):
            char = text[index]

            draw.text((c * font_size, r * font_size),char,black,font=font)
            index = index + 1

            if( index >= len(text) ):
                return image


    return image


def createimage(rows, cols, font_size = 16):
    # use a (r, g, b) tuple to represent colors
    #red = (255,0,0)
    white = (255,255,255)

    # create a new image surface
    # make the background white (default bg=black)
    return Image.new("RGB", [cols * font_size, (rows + 1) * font_size], white)