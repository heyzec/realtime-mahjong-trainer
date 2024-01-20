import numpy as np
from typing import Tuple, Any
from PIL import Image

Rect = Tuple[int, int, int, int]
PILImage = Image.Image


try:
    import numpy.typing as npt
    CVImage = npt.NDArray[np.uint8]
except ImportError:
    CVImage = Any