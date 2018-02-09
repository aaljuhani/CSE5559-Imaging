import re

import time

import PIL
import cv2
from PIL import Image
from openslide import open_slide, ImageSlide
from openslide.deepzoom import DeepZoomGenerator
import config as cfg
import numpy as np

def get_cnt_sum(contours, topn):
        res = 0
        cnts = sorted(contours, key=lambda x: cv2.contourArea(x))[-topn:]
        return sum([cv2.contourArea(cnt) for cnt in cnts])



img = cv2.imread('output/TCGA-3C-AALJ-01A-03-TSC.272FA991-8382-409A-A00A-9A3BAA6EE041/slide/18/81_5_1.jpeg')
#img = cv2.imread('output/TCGA-3C-AALJ-01A-03-TSC.272FA991-8382-409A-A00A-9A3BAA6EE041/slide/18/100_0_1.jpeg')


img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(img, (5, 5), 0)
ret3, th3 = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)
im2, contours, hierarchy = cv2.findContours(th3, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

#cv2.imshow('blur',blur)
#cv2.imshow('original',img)
#cv2.imshow('Adaptive threshold',im2)
#cv2.imshow('ret3',ret3)
#cv2.imshow('th3',th3)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

print(get_cnt_sum(contours, 2))
print(cfg.MAX_WHITE_SIZE)
print(get_cnt_sum(contours, 2) < cfg.MAX_WHITE_SIZE)

