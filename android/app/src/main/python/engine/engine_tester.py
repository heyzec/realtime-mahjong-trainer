import os

import cv2

from dirs import SCREENSHOTS_DIR
from utils.image import scale, show
from .engine_result import EngineResult
from .engine import Engine


class EngineTester:
    def test(self):
        path = os.path.join(SCREENSHOTS_DIR, os.listdir(SCREENSHOTS_DIR)[0])
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        img = scale(img, 0.99)

        engine = Engine()
        result = engine.process(img)
        print("dumping")
        pic = result.dumps()

        result = EngineResult.loads(pic)

        show(result.stage.image)


