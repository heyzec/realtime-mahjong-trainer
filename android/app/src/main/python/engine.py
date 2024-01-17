import json
import cv2
from dataclasses import dataclass

from stubs import CVImage
from trainer.trainer import Trainer
from trainer.objects.tile_collection import TileCollection
from recognition.mahjong_detector import SiftMahjongDetector, MahjongDectectionResult

def get_mpsz(result: MahjongDectectionResult):
    tiles = sorted(result.labels, key=lambda x: x[0][0])
    return ''.join(tile[1] for tile in tiles)



@dataclass
class EngineResult:
    image: bytes
    analysis: str

class Engine:
    def __init__(self):
        # self.trainer = Trainer("3568889m238p3678s")
        pass

    def start(self):
        pass

    def process(self, image_data) -> str:
        image: CVImage = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        detector = SiftMahjongDetector()

        detection_result = detector.process(image)
        print("number of detections", len(detection_result.labels))
        # detection_result.show()

        mpsz = get_mpsz(detection_result)
        hand = TileCollection.from_mpsz(mpsz)

        trainer = Trainer(hand)
        shanten = trainer.get_shanten()

        s = json.dumps({"shanten": shanten})
        print(s)

        # return image.tobytes()
        # To demostrate it is possible to send large amounts of data

        # image = detection_result.get_debug_image()

        image_bytes = cv2.imencode('.png', image)[1].tobytes()
        print("Image bytes length", len(image_bytes))
        return image_bytes

