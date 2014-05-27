# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def get_image(data, w, h, image=None, alpha = False):
    black = '#000000'

    wr = w * len(data[0])
    hr = h * len(data[0][0])
     
    if image is None:
        # create image
        image = createimage(wr, hr, 1, alpha)
  
    index = 0
    rf = 0
    
    for r in range(0, w):
        cf = 0
        for c in range(0, h):
            superpixel = data[index]

            if len(superpixel[0]) > 1:
                srf = 0
                for l in superpixel:
                   for p in l:
                       
		       if p:
			   image.putpixel((cf, rf+srf), (0, 0, 0))
 
		       	   #print "X (%s,%s)"%(rf+srf, cf) 
		       else:

		       	   #print "  (%s,%s)"%(rf+srf, cf) 
			   if alpha:
			   	image.putpixel((cf, rf+srf), (0, 0, 0, 0))
			   else:
			   	image.putpixel((cf, rf+srf), (255, 255, 255)) 
                       cf += 1

                   srf += 1
                   cf -= len(l)

                cf += len(superpixel[0])

            else:
		if data[index]:
		    rdata.append((0, 0, 0))
		else:
		    rdata.append((255,255,255))
            index = index + 1

            if(index >= len(data)):
                pass

        rf += len(data[0])

    return image


def addtext(text, image, cols, font_size = 16, rows = None, alpha = False):
    red = (255,0,0,255)
    green = (0,255,0,255)
    blue = (0,0,255,255)
    black = '#000000'
    red = '#FF0000'

    if rows is None:
        rows = int(len(text) / cols) + 1

    #load font
    #font = ImageFont.truetype("/media/windows/Projects/CryptoLVCS/image/DejaVuSans.ttf", font_size)
    font = ImageFont.truetype("image/DejaVuSans.ttf", font_size)

    #reduce space between letters
    font_size -= int(font_size * 0.3)

    if image is None:
        # create image
        image = createimage(rows * len(text[0]),
                            cols * len(text[0][0]),
                            font_size, alpha)

    else:
        # check the size
        (wn, hn) = (rows * font_size, cols * font_size)
        (w, h) = image.size

        #canvas resizing if it is neccesary
        #print (w, h)
        #print (wn, hn)
        if w < wn or h < hn:
            img = createimage(rows, cols, font_size)
            img.paste(image, (0, 0, w, h))
            image = img



    #draw object to write the text
    draw = ImageDraw.Draw(image)
    index = 0

    rf = 0
    for r in range(0, rows):
        cf = 0
        for c in range(0, cols):
            superpixel = text[index]

            if len(superpixel[0]) > 1:
                srf = 0
                for rsp in superpixel:

                    for char in rsp:
                        draw.text((cf * (font_size),
                                  (rf + srf) * (font_size)),
                                   char, fill=black, font=font)

                        cf += 1

                    srf += 1
                    cf -= len(rsp)


                cf += len(superpixel[0])

            else:
                draw.text((c * font_size, r * font_size),
                          superpixel, fill=black, font=font)

            index = index + 1

            if(index >= len(text)):
                return image

        rf += len(text[0])

    del draw
    return image

def overlaping(img1, img2, channel=0, thresold=200):
    white = (255,255,255)
    black = (0,0,0,0)
    red = (255,0,0)
    data1 = img1.getdata()
    data2 = img2.getdata()
    #data = [filter(lambda x: x in data1, sublist) for sublist in data2]

    newData = []
    for (p1,p2) in zip(data1,data2):
        if p1[channel] < thresold or p2[channel] < thresold:
            newData.append(black)
        else:
            newData.append(white)

    result = Image.new("RGB", img1.size, white)
    result.putdata(newData)

    return result


def createimage(rows, cols, font_size = 16, alpha = False):
    # use a (r, g, b) tuple to represent colors
    #red = (255,0,0)
    white = (255,255,255,255)
    
    # create a new image surface
    # make the background white (default bg=black)
    if alpha:
    	return Image.new("RGBA", (cols * font_size, (rows + 1) * font_size), (0, 0, 0, 0))
    else:
    	return Image.new("RGB", (cols * font_size, (rows + 1) * font_size), (255,255,255))
