from __future__ import annotations
import traceback
from typing import Dict

import json
import os
import cv2
import time

import numpy as np

from utils.image import save_image, show
from dirs import LABELLED_DIR

from .engine_result import EngineResult
from recognition.stage import DetectionResult
from recognition.template_detector import TemplateDetector
from utils.stubs import CVImage
from trainer.trainer import Trainer
from trainer.objects.tile_collection import TileCollection

def get_mpsz(detection: DetectionResult):
    tiles = sorted(detection, key=lambda x: x[0][0])
    return ''.join(tile[1] for tile in tiles)

class Engine:
    def __init__(self):
        # self.trainer = Trainer("3568889m238p3678s")
        pass

    def start(self):
        pass

    def load_target_images(self):
        labels = [basename.split('.')[0] for basename in os.listdir(LABELLED_DIR)]

        output: Dict[str, CVImage] = {}
        for label in labels:
            path = os.path.join(LABELLED_DIR, f"{label}.png")
            image: CVImage = cv2.imread(path)
            image: CVImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            output[label] = image

        return output


    def process_bytes(self, image_data: bytes) -> EngineResult:
        arr = np.array(image_data)
        image: CVImage = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return self.process(image)

    def process(self, image: CVImage) -> EngineResult:
        try:
            print("=============================BEGIN Process")
            start_time = time.time()
            print(image.shape)

            target_set = self.load_target_images()

            detector = TemplateDetector(target_set)
            stage = detector.detect(image)
            mpsz = get_mpsz(stage.result)
            hand = TileCollection.from_mpsz(mpsz)

            trainer = Trainer(hand)
            shanten = trainer.get_shanten()

            analysis = {
                "shanten": shanten,
                "hand": mpsz,
                "tiles": stage.result,
            }

            image = stage.display
            # border = cv2.copyMakeBorder(
            #     image,
            #     top=10,
            #     bottom=10,
            #     left=10,
            #     right=10,
            #     borderType=cv2.BORDER_CONSTANT,
            #     value=(0, 255, 0, 255)
            # )
            # image = border

            json_analysis = json.dumps(analysis)
            res = EngineResult(image=image, analysis=json_analysis, stage=stage)
            print("=============================END Process")
            print(analysis)
            print(image.shape)
            print(f"Processed in {time.time() - start_time}")
            return res
        except Exception as e:
            traceback.print_exc()
