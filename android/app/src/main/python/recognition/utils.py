from typing import List
from datetime import datetime
import os
import cv2
from PIL import Image

from stubs import CVImage, PILImage

def convert_cv_to_pil(cv_image: CVImage) -> PILImage:
    color_converted = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(color_converted)

def show(image: CVImage):
    img: CVImage | PILImage = image
    if not isinstance(img, Image.Image):
        img = convert_cv_to_pil(img)
    img.save("temp.png")
    os.system("qimgv temp.png")

def join_horizontal(images: List[Image.Image]):
    MARGIN = 10

    width = sum((im.size[0] for im in images))
    height = max((im.size[1] for im in images))

    pos = 0
    dst = Image.new('RGB', (width, height), (255,0,0))
    for i in range(len(images)):
        dst.paste(images[i], (pos, 0))
        pos += images[i].size[0] + MARGIN

    return dst

def join_vertical(images: List[Image.Image]):
    MARGIN = 10

    width = max((im.size[0] for im in images))
    height = sum((im.size[1] for im in images))

    pos = 0
    dst = Image.new('RGB', (width, height), (255,0,0))
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
