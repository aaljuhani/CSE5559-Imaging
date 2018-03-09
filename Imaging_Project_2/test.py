from PIL import Image , ImageStat


im = Image.open("112_16_1.jpeg").convert('L')
stat = ImageStat.Stat(im)
print "Read RMS brightness of image: "
print stat.extrema
print stat.count
print stat.sum


black = 0
red = 0

for pixel in im.getdata():
    if pixel == (0, 0, 0): # if your image is RGB (if RGBA, (0, 0, 0, 255) or so
        black += 1
    else:
        red += 1
print('black=' + str(black)+', red='+str(red))