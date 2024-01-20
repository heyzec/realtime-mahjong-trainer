import os
import math
import numpy as np
import random
import cv2
from recognition.utils import convert_cv_to_pil, convert_pil_to_cv, join_horizontal, join_vertical, show
import glob
from PIL import Image



from stubs import CVImage
from dirs import LABELLED_DIR

from dataclasses import dataclass

@dataclass
class MatchResult:
    score: float
    display_callback: object

    def get_display(self):
        return self.display_callback()

class Matcher:
    def __init__(self) -> None:
        self.sift = cv2.SIFT_create()

        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)
        self.flann = cv2.FlannBasedMatcher(index_params, search_params)

    @staticmethod
    def scale(img, factor):
        print("sacaling")
        assert 0.1 < factor < 100
        width, height = img.size
        new_size = (int(factor * width), int(factor * height))
        return img.resize(new_size, Image.LANCZOS)

    @staticmethod
    def get_random_image(pattern, scale=1):
        print("oh no")
        files = glob.glob(os.path.join(LABELLED_DIR, f'{pattern}.*'))
        path = random.choice(files)

        img = Image.open(path)

        # scramble = random.choice([True, False])
        img = Matcher.scale(img, scale)

        image = convert_pil_to_cv(img)
        return image

    @staticmethod
    def preprocess_image(img: CVImage):
        MARGIN_FRAC = 0.05
        h, w, _ = img.shape

        bounds = (slice(int(h * MARGIN_FRAC), int(h * (1-MARGIN_FRAC))),
            slice(int(w * MARGIN_FRAC), int(w * (1-MARGIN_FRAC))))
        cropped = img[bounds].copy()

        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        threshold = cv2.adaptiveThreshold(blurred, 255,
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY,
                                          11, 2)
        return threshold

    def randomly_test(self, n):
        pass
            # if random.random() > P_SAME:
            #     image1 = Matcher.get_random_image()
            #     image2 = Matcher.get_random_image()
            # else:
            #     image1 = Matcher.get_random_image()
            #     image2 = image1.copy()


    def test_and_show(self, test_input, show_size):

        to_show = []
        for file_pattern1, file_pattern2 in test_input:
            print(file_pattern1, file_pattern2)
            image1 = Matcher.get_random_image(file_pattern1, scale=1.5)
            image2 = Matcher.get_random_image(file_pattern2, scale=1)

            result = self.compare_and_score(image1, image2)

            display = result.get_display()

            cv2.putText(display, f"{result.score:.2f}", (80, 100), fontFace=1, fontScale=3, color=(0,0,0), thickness=5)
            to_show.append(display)

        rows, cols = show_size
        combined = join_vertical([join_horizontal(to_show[i*cols:(i+1)*cols]) for i in range(0, rows)])
        show(combined)

    def test_and_show_within_suit(self, suit: str):
        assert suit in 'mpsz', f"{suit} is not a valid suit"

        N = 81
        show_size = (9, 9)

        test_input = []
        for k in range(N):
            i = k // 9 + 1
            j = k % 9 + 1

            file_pattern1 = f"{i}{suit}"
            file_pattern2 = f"{j}{suit}"
            test_input.append((file_pattern1, file_pattern2))

        self.test_and_show(test_input, show_size)



    def test_random(self, n):
        test_input = []
        for _ in range(n):
            file_pattern1 = f"*"
            file_pattern2 = f"*"
            test_input.append((file_pattern1, file_pattern2))

        show_size = (n, 1)
        self.test_and_show(test_input, show_size)






    def test_all(self):
        paths = [os.path.join(LABELLED_DIR, file) for file in os.listdir(LABELLED_DIR)]

        for i in range(len(paths)):
            for j in range(len(paths)):
                # for scale in (0.8, 0.9, 1.1, 1.2):
                for scale in (1.1,):
                    image1 = Image.open(paths[i])
                    image2 = Image.open(paths[j])

                    image1 = convert_pil_to_cv(Matcher.scale(image1, 1.5))
                    image2 = convert_pil_to_cv(Matcher.scale(image2, 1))




                    result = self.compare_and_score(image1, image2)

                    if i == j and result.score < 0.9:
                        print(result.score)
                        show(result.get_display())
                        raise Exception()
                    if i != j and result.score > 0.9:
                        raise Exception()
                    print(i, j, result.score)






    def extract_features(self, img: CVImage):
        keypoints, descriptors = self.sift.detectAndCompute(img, None)
        return keypoints, descriptors

    def match_features(self, ft1, ft2):
        kp1, des1 = ft1
        kp2, des2 = ft2



        matches = self.flann.knnMatch(des1, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        is_good = [True] * len(matches)
        for i, (m, n) in enumerate(matches):
            if m.distance < 0.7 * n.distance:
                pass
            else:
                is_good[i] = False

        return matches, is_good

        # matchesMask = mask.ravel().tolist()



        # return good_matches, matchesMask

    def compare(self, image1, image2) -> bool:
        SCORE_THRESHOLD = 0.9
        result = self.compare_and_score(image1, image2)
        return result.score > SCORE_THRESHOLD

    def compare_and_score(self, image1: CVImage, image2: CVImage) -> MatchResult:
        image1 = Matcher.preprocess_image(image1)
        image2 = Matcher.preprocess_image(image2)
        kp1, des1 = self.extract_features(image1)
        kp2, des2 = self.extract_features(image2)

        matches, is_good = self.match_features((kp1, des1), (kp2, des2))
        good_matches = [match for (i, match) in enumerate(matches) if is_good[i]]
        n_good_matches = sum(is_good)
        pts1 = np.float32([ kp1[m[0].queryIdx].pt for m in good_matches ]).reshape(-1,1,2)
        pts2 = np.float32([ kp2[m[0].trainIdx].pt for m in good_matches ]).reshape(-1,1,2)


        def display_callback():
            return self.draw_matches(matches, None, image1, kp1, image2, kp2)

        result = MatchResult(score=0, display_callback=display_callback)

        if n_good_matches < 4:
            return result

        M, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, ransacReprojThreshold=5.0)


        if M is None:
            return result

        det = np.linalg.det(M)
        print('det', det)
        if det < 1:
            scale_factor = math.sqrt(abs(det))
        else:
            scale_factor = math.sqrt(abs(det))
        print("scalefactor", scale_factor)


        if not 0.5 < scale_factor < 2:
            return result

        image3 = convert_pil_to_cv(Matcher.scale(convert_cv_to_pil(image2), 1/scale_factor))



        kp3, des3 = self.extract_features(image3)
        matches, is_good = self.match_features((kp1, des1), (kp3, des3))


        n_good = len(list(filter(lambda x: x, mask)))
        score = n_good / len(matches)

        def display_callback():
            cvmask = [([1, 0] if x else [0, 0]) for x in is_good]
            return self.draw_matches(matches, cvmask, image1, kp1, image3, kp3)

        return MatchResult(score=score, display_callback=display_callback)


    def draw_matches(self, matches, mask, img1, kp1, img2, kp2):
        draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = mask,
                   flags = 0)
        return cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, img2, **draw_params)



