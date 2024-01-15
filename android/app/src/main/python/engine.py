import numpy as np
import cv2
from trainer.trainer import Trainer

class Engine:
    def __init__(self):
        self.trainer = Trainer("3568889m238p3678s")

    def start(self):
        pass

    def process(self, b: bytes):
        print("we got an bytes")

        print(type(b))
        cv2_img_flag=0
        im = cv2.imdecode(b, cv2_img_flag)

        print("decoded")
        print(type(im))
