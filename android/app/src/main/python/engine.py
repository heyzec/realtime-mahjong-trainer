import json
import cv2
from dataclasses import dataclass

import numpy as np

from stubs import CVImage
from trainer.trainer import Trainer
from trainer.objects.tile_collection import TileCollection
from recognition.mahjong_detector import SiftMahjongDetector, MahjongDectectionResult
from recognition.utils import save_image, show

def get_mpsz(result: MahjongDectectionResult):
    tiles = sorted(result.labels, key=lambda x: x[0][0])
    return ''.join(tile[1] for tile in tiles)



@dataclass
class EngineResult:
    image: bytes
    analysis: str

    def to_bytes(self) -> bytes:
        return (self.analysis.encode() +
            ("\n").encode() +
        self.image)

class Engine:
    def __init__(self):
        # self.trainer = Trainer("3568889m238p3678s")
        pass

    def start(self):
        pass

    def process(self, image_data) -> EngineResult:
        image: CVImage = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        save_image(image, 'source')

        detector = SiftMahjongDetector()

        detection_result = detector.process(image)
        # show(detection_result.get_debug_image())
        save_image(detection_result.get_debug_image(), 'contour')
        print("number of detections", len(detection_result.labels))
        # detection_result.show()

        mpsz = get_mpsz(detection_result)
        hand = TileCollection.from_mpsz(mpsz)

        trainer = Trainer(hand)
        shanten = trainer.get_shanten()



        analysis = {
            "shanten": shanten,
            "hand": mpsz,
            "tiles": detection_result.labels,
        }

        image = detection_result.get_debug_image()
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

        image_bytes: bytes = cv2.imencode('.png', image)[1].tobytes()
        json_analysis = json.dumps(analysis)
        return EngineResult(image=image_bytes, analysis=json_analysis)

