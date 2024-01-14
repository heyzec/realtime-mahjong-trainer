import abc
import os
import cv2
from utils import show, join_vertical, convert_cv_to_pil
from edge import extract_tiles_bounds

class MahjongDetector(abc.ABC):
    def __init__(self) -> None:
        pass


    def detect(self, image):
        pass


LABELLED_DIR = "./images/labelled"

class SiftMahjongDetector(MahjongDetector):
    def __init__(self):
        self.sift = cv2.xfeatures2d.SIFT_create()
        self.features = {}

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

        bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
        for rect in rects:
            x,y,w,h = rect
            tile_img = image[y:y+h, x:x+w]
            k, d = self.sift.detectAndCompute(tile_img, None)

            all_draw = []
            best_score = 0
            best_label = None
            for label in self.features.keys():
                matches = bf.match(d, self.features[label][1])
                score = sum((m.distance for m in matches))
                actual = cv2.imread('./images/labelled/' + label + '.png')
                draw = cv2.drawMatches(tile_img, k, actual, self.features[label][0], matches, actual, flags=2)
                all_draw.append(draw)





                if score > best_score:
                    best_score = score
                    best_label = label


            print(best_label)
            show(join_vertical([convert_cv_to_pil(im) for im in all_draw]))


            # actual = cv2.imread('./tiles/labelled/' + best_label + '.png')
            # show(actual)
            # matches = cv2.drawMatches(actual, self.features[best_label][0], tile_img, k, matches, tile_img, flags=2)
            # show(matches)
