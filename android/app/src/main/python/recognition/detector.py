import abc
from recognition.stage_result import DetectionResult, Stage

from stubs import CVImage

class Detector(abc.ABC):
    # @abc.abstractmethod
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def detect(self, image: CVImage) -> Stage[DetectionResult]:
        pass

