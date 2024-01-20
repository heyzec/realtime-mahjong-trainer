from typing import List
import numpy as np
from datetime import datetime
import subprocess
import cv2
from PIL import Image

from stubs import CVImage, PILImage

def try_convert_cv_to_pil(img: CVImage) -> PILImage:
    if not isinstance(img, Image.Image):
        img = convert_cv_to_pil(img)
    return img

def convert_cv_to_pil(cv_image: CVImage) -> PILImage:
    return Image.fromarray(cv_image)

def convert_pil_to_cv(pil_image: PILImage) -> CVImage:
    open_cv_image = np.array(pil_image)
    if len(open_cv_image.shape) == 2:
        return open_cv_image
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    return open_cv_image

def show(image: CVImage):
    img: CVImage | PILImage = image
    if not isinstance(img, Image.Image):
        img = convert_cv_to_pil(img)
    img.save("temp.png")

    try:
        if subprocess.call(['sh', '-c', 'pgrep qimgv &>/dev/null']) != 0:
            subprocess.call(['sh', '-c', 'nohup qimgv temp.png &>/dev/null &'])
    except KeyboardInterrupt:
        exit()

def join_horizontal(images: List[Image.Image]):
    images = [try_convert_cv_to_pil(im) for im in images]

    MARGIN = 1

    width = sum((im.size[0] for im in images)) + (len(images) - 1) * MARGIN
    height = max((im.size[1] for im in images))

    pos = 0
    dst = Image.new('RGB', (width, height), (0,0,0))
    for i in range(len(images)):
        dst.paste(images[i], (pos, 0))
        pos += images[i].size[0] + MARGIN

    return dst

def join_vertical(images: List[Image.Image]):
    images = [try_convert_cv_to_pil(im) for im in images]

    MARGIN = 1

    width = max((im.size[0] for im in images)) + (len(images) - 1) * MARGIN
    height = sum((im.size[1] for im in images))

    pos = 0
    dst = Image.new('RGB', (width, height), (0,0,0))
    for i in range(len(images)):
        dst.paste(images[i], (0, pos))
        pos += images[i].size[1] + MARGIN

    return dst

def save_image(image: CVImage, tag: str):
    filepath = f"/storage/emulated/0/Android/data/com.example.realtime_mahjong_trainer/files/{datetime.now()}_{tag}.png"
    try:
        image_bytes: bytes = cv2.imencode('.png', image)[1].tobytes()
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
    except Exception as e:
        print(e)
