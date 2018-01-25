import os
import cv2
import numpy as np
import glob
from tqdm import tqdm
from openslide import open_slide, ImageSlide
from openslide.deepzoom import DeepZoomGenerator

#one file for now
files = glob.glob('img/*.svs')
print(files)

for slidepath in tqdm(files):
    basename = os.path.splitext(os.path.basename(slidepath))[0]
    print(basename)
    basepath = os.path.join('/output', basename)
    print(basepath)
    WholeSlideTiler


#TODO: Normalizing

#TODO: Tilling

#TODO: Display outcomes