import random
from typing import List, Tuple
import numpy as np
import cv2

from stubs import CVImage, Rect

class StageResult:
    def __init__(self, image: CVImage) -> None:
        self.image = image
        self.results = []

    def add_results(self, results):
        self.results.extend(results)

    def get_debug_image(self) -> CVImage:
        return self.image


class EdgeDetector:
    def __init__(self, image: CVImage) -> None:
        self.image = image
        self.contours = []

    def detect(self) -> StageResult:
        self.get_contours()
        result = StageResult(self.image)
        rects = []
        for contour in self.contours:
            if self.filt(contour):
                rects.append(cv2.boundingRect(contour))
        result.add_results(rects)

        def get_debug_image():
            print("getting debug image")
            img_height, img_width, _ = self.image.shape
            n_channels = 4
            transparency: CVImage = np.zeros((img_height, img_width, n_channels), dtype=np.uint8)

            for contour in self.contours:
                rect: Rect = cv2.boundingRect(contour)
                area: int = cv2.contourArea(contour)

                x,y,w,h = rect

                if self.filt(contour):
                    color = (0, 0, 255, 255)
                else:
                    color = (0, 255, 0, 255)
                cv2.drawContours(transparency, [contour], -1, color, 2)
                cv2.putText(transparency, str(area), (int(x+0.5*w),int(y+random.random()*h)), 0, fontScale=1, color=(0,255,0, 255), thickness=3)

            return transparency

        result.get_debug_image = get_debug_image

        return result



    def get_contours(self):
        image = self.image

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(blur, 150, 400)

        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = contours

    def filt(self, contour) -> bool:
        area: int = cv2.contourArea(contour)
        return 13000 <= area <= 14000
        # return 16400 <= area < 16800


    def extract_tiles_bounds(self):
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

