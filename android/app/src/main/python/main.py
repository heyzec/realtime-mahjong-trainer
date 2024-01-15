import cv2
import numpy as np
import os
import random
from engine import Engine

path = "./recognition/images/screenshots/" + random.choice(os.listdir('./recognition/images/screenshots'))

engine = Engine()

with open(path, 'rb') as f:
    image_data = f.read()
image_data = np.frombuffer(image_data, np.uint8)
# # arr = np.array(b)
# image = cv2.imdecode(ar, cv2.IMREAD_COLOR)

# # image = cv2.imread(path)
# # print(image)

engine.process(image_data)




