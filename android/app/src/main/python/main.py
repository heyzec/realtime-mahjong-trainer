import os
import random
import cv2
import numpy as np

from engine import Engine, EngineTester
from recognition.matcher_tester import MatcherTester
from recognition.template_detector import TemplateDetector
# from recognition.matcher import Matcher
# from recognition.matcher_tester import MatcherTester
from stubs import CVImage


def main():
    path = "./recognition/images/screenshots/" + random.choice(os.listdir('./recognition/images/screenshots'))

    engine = Engine()

    # with open(path, 'rb') as f:
    #     b = f.read()

    # byte_array: cvimage = np.frombuffer(b, np.uint8)

    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    engine.process(img)



def test_match():
    matcher = TemplateDetector()
    tester = MatcherTester(matcher)
    # tester.test_and_show_within_suit('m')
    # matcher.test_random(10)
    tester.test_all()

def test_engine():
    tester = EngineTester()
    tester.test()


# test_match()
main()
# test_engine()
