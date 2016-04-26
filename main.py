#! /usr/bin/python

import cv2
import sys
from getopt import getopt
import numpy as np


def scale_img(img, (w, h)):
    ih, iw = img.shape
    scale = min(float(w)/iw, float(h)/ih)
    ow, oh = (int(iw*scale), int(ih*scale))
    mat = cv2.getRotationMatrix2D(
        (0, 0),
        0,
        scale
    )
    return cv2.warpAffine(
        img,
        mat,
        (ow, oh),
        cv2.INTER_CUBIC
    )

args, _ = getopt(sys.argv[2:], 'w:h:')
ws = filter(lambda ((a, _)): a == '-w', args)
hs = filter(lambda ((a, _)): a == '-w', args)
out_size = (
    ws[0][1] if len(ws) else 30,
    hs[0][1] if len(hs) else 30
)

impath = sys.argv[1]
img = cv2.imread(impath)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = 4 * (1 - gray / float(gray.max()))

fist = u'\u270a'

def get_skin_tone(i):
    return unichr(0x1f3fb + i)

to_fist = np.vectorize(
    lambda a: (
        lambda y: fist + get_skin_tone(y)
    )(int(round(a)))
)

f = open('out.txt', 'w')
f.write(
    reduce(
        lambda o, l: '%s\n%s'%(o, reduce(lambda a, b: a + b, l)),
        to_fist(scale_img(gray, out_size)),
        ''
    ).encode('utf8')
)
f.close()
