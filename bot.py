import numpy as np

import cv2
import time
import random

#from alexnet import alexnet
from grabscreen import grab_screen
from template_matching import match

like_template = "img/like.png"
nope_template = "img/nope.png"

while True:
    screen = grab_screen(region=(590,120,930,800))
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

    top_left = cv2.cvtColor(grab_screen(region=(560, 160, 700, 230)), cv2.COLOR_RGB2BGR)
    edges = cv2.Canny(top_left, 100, 200)

    matches = match(edges, like_template)

    cv2.imshow('window', matches)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()