import abc
from .stage import DetectionResult, Stage

from utils.stubs import CVImage

class Detector(abc.ABC):
    # @abc.abstractmethod
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def detect(self, image: CVImage) -> Stage[DetectionResult]:
        pass

