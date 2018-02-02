from __future__ import division

import glob

import cv2
import numpy as np
from tqdm import tqdm


def safe_ln(x, minval=0.0000000001):
    return np.log(x.clip(min=minval))


def normalize_staining(I=None):
    I = I.astype(np.float64)
    Io = 240
    beta = 0.15
    alpha = 1
    HERef = np.array([[0.5626, 0.2159], [0.7201, 0.8012], [0.4062, 0.5581]])
    maxCRef = np.array([1.9705, 1.0308])

    (h, w, c) = np.shape(I)
    I = np.reshape(I, (h * w, c), order='F')

    # Step 1. Convert RGB to OD.
    OD = - np.log((I + 1) / Io) # optical density where each channel in the image is normalized to values between [0, 1]

    # Step 2. Remove data with OD intensity less than beta
    ODhat = (OD[(np.logical_not((OD < beta).any(axis=1))), :])

    # Step 3. Calculate SVD on the OD tuples
    cov = np.cov(ODhat, rowvar=False)
    (W, V) = np.linalg.eig(cov)

    # Step 4. create plane from the SVD directions
    # corresponding to the two largest singular values
    Vec = - np.transpose(np.array([V[:, 1], V[:, 0]]))

    # Step 5. Project data onto the plane and normalize to unit Length
    That = np.dot(ODhat, Vec)

    # Step 6. Calculate angle of each point w.r.t the first SVD direction
    phi = np.arctan2(That[:, 1], That[:, 0])

    # Step 7. Find robust extremes (some alpha th and (100 - alpha th) percentiles of the angle
    minPhi = np.percentile(phi, alpha)
    maxPhi = np.percentile(phi, 100 - alpha)
    vMin = np.dot(Vec, np.array([np.cos(minPhi), np.sin(minPhi)]))
    vMax = np.dot(Vec, np.array([np.cos(maxPhi), np.sin(maxPhi)]))
    if vMin[0] > vMax[0]:
        HE = np.array([vMin, vMax])
    else:
        HE = np.array([vMax, vMin])

    HE = np.transpose(HE)

    # Step 8. Convert extreme values back to OD space
    Y = np.transpose(np.reshape(OD, (h * w, c)))
    C = np.linalg.lstsq(HE, Y,rcond=None)
    maxC = np.percentile(C[0], 99, axis=1)
    C = C[0] / maxC[:, None]
    C = C * maxCRef[:, None]
    Inorm = Io * np.exp(- np.dot(HERef, C))
    Inorm = np.reshape(np.transpose(Inorm), (h, w, c), order='F')
    Inorm = np.clip(Inorm, 0, 255)
    Inorm = np.array(Inorm, dtype=np.uint8)

    return Inorm  # ,H,E


def main():
    filename = "/Users/arunimasrivastava/Desktop/Imaging_class/openslide-svs-tiler-master/output/Test_Image-TCGA-E9-A1NF/slide/15/23_112_4.jpeg"
    fileout = "/Users/arunimasrivastava/Desktop/Imaging_class/openslide-svs-tiler-master/output/Test_Image-TCGA-E9-A1NF/slide/15/23_112_4_normed.jpeg"
    img = cv2.imread(filename)
    img = img.astype(np.float64)

    img = normalize_staining(img)

    cv2.imwrite(fileout, img)


if __name__ == '__main__':
    main()
