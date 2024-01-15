import abc
import os
import cv2
import numpy as np
from .edge import extract_tiles_bounds
from .utils import show

class MahjongDetector(abc.ABC):
    def __init__(self) -> None:
        pass


    def detect(self, image):
        pass


LABELLED_DIR = os.path.join(os.path.dirname(__file__), "./images/labelled")


class MahjongDectectionResult:
    def __init__(self, image: np.ndarray):
        self.image = image
        self.labels = []

    def add(self, rect, label_name):
        self.labels.append((rect, label_name))

    def show(self):
        canvas = self.image.copy()

        for label in self.labels:
            rect, name = label
            x,y,w,h = rect
            cv2.rectangle(canvas, (x, y), (x+w, y+h), (0, 0, 255), thickness=3)
            pos = (x + 5, y + 27)
            cv2.putText(canvas, name, pos, 0, fontScale=1, color=(0,0,255), thickness=2)

        show(canvas)



class SiftMahjongDetector(MahjongDetector):
    def __init__(self):
        self.sift = cv2.SIFT_create()
        self.features = {}
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


    def process(self, image):
        rects = extract_tiles_bounds(image)

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

                matches = flann.knnMatch(d,self.features[label][1],k=2)

                # store all the good matches as per Lowe's ratio test.
                good = []
                for m,n in matches:
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


            # print(best_label)
            # show(join_vertical([convert_cv_to_pil(im) for im in all_draw]))


            # actual = cv2.imread('./tiles/labelled/' + best_label + '.png')
            # show(actual)
            # matches = cv2.drawMatches(actual, self.features[best_label][0], tile_img, k, matches, tile_img, flags=2)
            # show(matches)
            # print(best_label)
            # print(best_label)
            result.add(rect, best_label)
            # show(tile_img)
        return result
