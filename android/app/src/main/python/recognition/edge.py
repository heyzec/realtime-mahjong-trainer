import numpy as np
import cv2
import random

def extract_tiles_bounds(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blur, 150, 400)

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    drawed = np.zeros_like(image)

    output = []

    for contour in contours:
        rect = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)

        if not 16400 <= area < 16800:
            continue

        output.append(rect)

        x,y,w,h = rect
        cv2.drawContours(drawed, [contour], -1, (0, 255, 0), 2)
        cv2.putText(drawed, str(area), (int(x+0.5*w),int(y+random.random()*h)), 0, fontScale=1, color=(0,255,0), thickness=3)


    # show(drawed)
    return output

