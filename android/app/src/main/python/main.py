import os
import random
import cv2
import numpy as np

from engine import Engine
from stubs import CVImage

path = "./recognition/images/screenshots/" + random.choice(os.listdir('./recognition/images/screenshots'))

engine = Engine()

with open(path, 'rb') as f:
    b = f.read()

byte_array: CVImage = np.frombuffer(b, np.uint8)

image = cv2.imread(path)

engine.process(byte_array)




