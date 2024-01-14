import random
import os
import cv2
from mahjong_detector import SiftMahjongDetector


hand = "./images/screenshots/" + random.choice(os.listdir('./images/screenshots'))
im = cv2.imread(hand)
detector = SiftMahjongDetector()
detector._predetect_features()
detector.process(im)


