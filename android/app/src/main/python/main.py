import os
import random
import cv2
import numpy as np

from engine import Engine
from recognition.matcher import Matcher
from stubs import CVImage


def main():
    path = "./recognition/images/screenshots/" + random.choice(os.listdir('./recognition/images/screenshots'))

    engine = Engine()

    with open(path, 'rb') as f:
        b = f.read()

    byte_array: CVImage = np.frombuffer(b, np.uint8)

    image = cv2.imread(path)

    engine.process(byte_array)



def test_match():
    matcher = Matcher()
    matcher.test_and_show_within_suit('m')
    # matcher.test_random(10)
    # matcher.test_all()


test_match()
# main()
