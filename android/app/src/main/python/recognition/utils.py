import os

import cv2
from PIL import Image

def convert_cv_to_pil(cv_image):
    color_converted = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(color_converted)

def show(img):
    if not isinstance(img, Image.Image):
        img = convert_cv_to_pil(img)
    img.save("temp.png")
    os.system("qimgv temp.png")

def join_horizontal(images: list[Image.Image]):
    MARGIN = 10

    width = sum((im.size[0] for im in images))
    height = max((im.size[1] for im in images))

    pos = 0
    dst = Image.new('RGB', (width, height), (255,0,0))
    for i in range(len(images)):
        dst.paste(images[i], (pos, 0))
        pos += images[i].size[0] + MARGIN

    return dst

def join_vertical(images: list[Image.Image]):
    MARGIN = 10

    width = max((im.size[0] for im in images))
    height = sum((im.size[1] for im in images))

    pos = 0
    dst = Image.new('RGB', (width, height), (255,0,0))
    for i in range(len(images)):
        dst.paste(images[i], (0, pos))
        pos += images[i].size[1] + MARGIN

    return dst
