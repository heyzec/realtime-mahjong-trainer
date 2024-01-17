import abc
import os
from typing import Tuple, List, Dict, Any
import cv2
import numpy as np

from .edge import EdgeDetector
from .utils import show
from stubs import CVImage, Rect

class MahjongDetector(abc.ABC):
    def __init__(self) -> None:
        pass


    def detect(self, image: CVImage):
        pass


LABELLED_DIR = os.path.join(os.path.dirname(__file__), "./images/labelled")


class MahjongDectectionResult:
    def __init__(self, image: CVImage):
        self.image = image
        self.labels: List[Tuple[Rect, str]] = []

    def add(self, rect: Rect, label_name: str) -> CVImage:
        self.labels.append((rect, label_name))

    def get_debug_image(self) -> CVImage:
        img_height, img_width, _ = self.image.shape
        n_channels = 4
        transparency: CVImage = np.zeros((img_height, img_width, n_channels), dtype=np.uint8)

        for label in self.labels:
            rect, name = label
            x,y,w,h = rect
            cv2.rectangle(transparency, (x, y), (x+w, y+h), (0, 0, 255), thickness=3)
            pos = (x + 5, y + 27)
            cv2.putText(transparency, name, pos, 0, fontScale=1, color=(0,0,255), thickness=2)

        return transparency



    def show(self):
        canvas = self.image.copy()

        overlay = self.get_debug_image()

        alpha = 0.5
        # TODO: Fix by adding alpha channel to canvas first
        cv2.addWeighted(overlay, alpha, canvas, 1 - alpha, 0, canvas)

        show(canvas)



class SiftMahjongDetector(MahjongDetector):
    def __init__(self):
        self.sift = cv2.SIFT_create()
        self.features: Dict[str, Tuple[Any, Any]] = {}
        self._predetect_features()
        if len(self.features) == 0:
            raise Exception("No features processed")


    def _predetect_features(self):
        for basename in os.listdir(LABELLED_DIR):
            filepath = f"{LABELLED_DIR}/{basename}"
            label = basename.split('.')[0]


            img = cv2.imread(filepath)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            keypoints, descriptors = self.sift.detectAndCompute(img, None)
            self.features[label] = (keypoints, descriptors)


    def process(self, image: CVImage) -> MahjongDectectionResult:
        edge_detector = EdgeDetector(image)

        edge_result = edge_detector.detect()

        rects: List[Rect] = edge_result.results



        result = MahjongDectectionResult(image)

        for rect in rects:
            x,y,w,h = rect
            tile_img = image[y:y+h, x:x+w]
            k, d = self.sift.detectAndCompute(tile_img, None)

            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            search_params = dict(checks = 50)
            flann = cv2.FlannBasedMatcher(index_params, search_params)

            # all_draw = []
            best_score = 0
            best_label = None
            for label in self.features.keys():

                matches: List = flann.knnMatch(d,self.features[label][1],k=2)

                # store all the good matches as per Lowe's ratio test.
                good = []
                for m, n in matches:
                    if m.distance < 0.7*n.distance:
                        good.append(m)





                # print(label, len(matches), len(good))
                # score = sum((m.distance for m in matches))
                # actual = cv2.imread('./images/labelled/' + label + '.png')
                # draw = cv2.drawMatches(tile_img, k, actual, self.features[label][0], matches, actual, flags=2)
                # all_draw.append(draw)
                score = len(good)





                if score > best_score:
                    best_score = score
                    best_label = label


            assert best_label is not None
            result.add(rect, best_label)

        # result.image = debug
            # show(tile_img)

        result.get_debug_image = lambda: edge_result.get_debug_image()



        return result
