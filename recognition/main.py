import random
import os
import cv2
from mahjong_detector import SiftMahjongDetector
from utils import show


hand = "./images/screenshots/" + random.choice(os.listdir('./images/screenshots'))
im = cv2.imread(hand)
detector = SiftMahjongDetector()
detector._predetect_features()
result = detector.process(im)

for r in result.labels:
    rect, label = r
    x,y,w,h = rect


    loc = (int(x+0.5*w - 10), y+10)
    BLACK = (0, 0, 0)
    cv2.putText(im, label, loc, 0, fontScale=1, color=BLACK, thickness=3)

show(im)

