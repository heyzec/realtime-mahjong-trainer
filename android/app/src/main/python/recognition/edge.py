import random
from typing import List, Tuple
import numpy as np
import cv2

from stubs import CVImage, Rect

def extract_tiles_bounds(image: CVImage) -> Tuple[CVImage, List[Rect]]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blur, 150, 400)

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    img_height, img_width, _ = image.shape
    n_channels = 4
    transparency: CVImage = np.zeros((img_height, img_width, n_channels), dtype=np.uint8)

    output: List[Rect] = []

    for contour in contours:
        rect: Rect = cv2.boundingRect(contour)
        area: int = cv2.contourArea(contour)

        if not 16400 <= area < 16800:
            continue

        output.append(rect)

        x,y,w,h = rect
        cv2.drawContours(transparency, [contour], -1, (0, 255, 0), 2)
        cv2.putText(transparency, str(area), (int(x+0.5*w),int(y+random.random()*h)), 0, fontScale=1, color=(0,255,0), thickness=3)


    # show(drawed)
    return transparency, output

