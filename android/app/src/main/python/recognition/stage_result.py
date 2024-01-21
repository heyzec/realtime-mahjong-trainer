from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple, TypeVar, Generic, Any

from stubs import CVImage, Rect

T = TypeVar("T")
U = TypeVar("U")

@dataclass
class Stage(Generic[T]):
    result: T
    image: CVImage
    prev: Optional[Stage[Any]] = None
    display_callback: Optional[Callable[..., CVImage]] = None

    @classmethod
    def first_image(cls, image: CVImage):
        return Stage(result=None, image=image)

    def next(self, result: U, display_callback: Optional[Callable[..., CVImage]], image: Optional[CVImage] = None):
        if image is None:
            image = self.image
        return Stage(result=result, prev=self, display_callback=display_callback, image=image)

    def get_display(self) -> CVImage:
        if self.display_callback is None:
            return self.image
        return self.display_callback()

DetectionResult = List[Tuple[Rect, str]]

# class StgeResult:
#     def __init__(self, image: CVImage) -> None:
#         self.image = image
#         self.results = []

#     def add_results(self, results):
#         self.results.extend(results)

#     def get_debug_image(self) -> CVImage:
#         return self.image

# class MahjongDectectionResult:
#     def __init__(self, image: CVImage):
#         self.image = image
#         self.labels: List[Tuple[Rect, str]] = []

#     def add(self, rect: Rect, label_name: str) -> CVImage:
#         self.labels.append((rect, label_name))

#     def get_debug_image(self) -> CVImage:
#         img_height, img_width, _ = self.image.shape
#         n_channels = 4
#         transparency: CVImage = np.zeros((img_height, img_width, n_channels), dtype=np.uint8)

#         for label in self.labels:
#             rect, name = label
#             x,y,w,h = rect
#             cv2.rectangle(transparency, (x, y), (x+w, y+h), (0, 0, 255), thickness=3)
#             pos = (x + 5, y + 27)
#             cv2.putText(transparency, name, pos, 0, fontScale=1, color=(0,0,255), thickness=2)

#         return transparency



#     def show(self):
#         canvas = self.image.copy()

#         overlay = self.get_debug_image()

#         alpha = 0.5
#         # TODO: Fix by adding alpha channel to canvas first
#         cv2.addWeighted(overlay, alpha, canvas, 1 - alpha, 0, canvas)

#         show(canvas)
