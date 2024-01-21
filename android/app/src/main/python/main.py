import os
import random
import cv2
from dirs import SCREENSHOTS_DIR

from engine import Engine, EngineTester

def main():
    path = SCREENSHOTS_DIR + random.choice(os.listdir(SCREENSHOTS_DIR))

    engine = Engine()
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    engine.process(img)

def test_engine():
    tester = EngineTester()
    tester.test()


# test_match()
# main()
test_engine()
