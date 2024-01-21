import json
import os
import cv2
from dataclasses import dataclass

import numpy as np
from dirs import SCREENSHOTS_DIR
from recognition.stage_result import DetectionResult
from recognition.template_detector import TemplateDetector

from stubs import CVImage
from trainer.trainer import Trainer
from trainer.objects.tile_collection import TileCollection
from recognition.utils import save_image, scale, show

def get_mpsz(detection: DetectionResult):
    tiles = sorted(detection, key=lambda x: x[0][0])
    return ''.join(tile[1] for tile in tiles)



@dataclass
class EngineResult:
    image: CVImage
    analysis: str

    def to_bytes(self) -> bytes:
        image_bytes: bytes = cv2.imencode('.png', self.image)[1].tobytes()
        return (self.analysis.encode() +
            ("\n").encode() +
        image_bytes)

class Engine:
    def __init__(self):
        # self.trainer = Trainer("3568889m238p3678s")
        pass

    def start(self):
        pass


    def process_bytes(self, image_data: bytes) -> EngineResult:
        arr = np.array(image_data)
        image: CVImage = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return self.process(image)

    def process(self, image: CVImage) -> EngineResult:

        save_image(image, 'source')

        detector = TemplateDetector()

        stage = detector.detect(image)
        show(stage.get_display())
        print("number of detections", len(stage.result))

        mpsz = get_mpsz(stage.result)
        print(mpsz)
        hand = TileCollection.from_mpsz(mpsz)

        trainer = Trainer(hand)
        shanten = trainer.get_shanten()



        analysis = {
            "shanten": shanten,
            "hand": mpsz,
            "tiles": stage.result,
        }

        image = stage.get_display()
        border = cv2.copyMakeBorder(
            image,
            top=10,
            bottom=10,
            left=10,
            right=10,
            borderType=cv2.BORDER_CONSTANT,
            value=[0, 255, 0, 255]
        )
        image = border

        json_analysis = json.dumps(analysis)
        return EngineResult(image=image, analysis=json_analysis)

class EngineTester:
    def test(self):
        path = os.path.join(SCREENSHOTS_DIR, os.listdir(SCREENSHOTS_DIR)[0])
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        img = scale(img, 0.99)

        engine = Engine()
        engine.process(img)
        show(img)
