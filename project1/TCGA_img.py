import os
import cv2
import numpy as np
import glob
from tqdm import tqdm
from tiler import WholeSlideTiler


#one file for now
files = glob.glob('img/*.svs')
print(files)

for slidepath in tqdm(files):
    basename = os.path.splitext(os.path.basename(slidepath))[0]
    print(basename)
    basepath = os.path.join('/output', basename)
    print(basepath)
    WholeSlideTiler(slidepath, basepath, 'jpeg',149 , 75 , True, True, 100,  12, True).run()

    


#TODO: Normalizing


#TODO: Display outcomes