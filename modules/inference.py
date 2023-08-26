import cv2
import easyocr
from pathlib import Path
from bounding_box import bounding_box as bb
from modules.utils import TYPE2COLOR, text_cls


def main(img):
    # src = Path("C:/Datasets/SMM Hack")
    # im = src / 'tg' / 'images' / '0b751210-de3e-412a-b96f-5a8494daa6bf.PNG'

    # img = cv2.imread(str(im))

    reader = easyocr.Reader(['en', 'ru'], verbose=True)
    result = reader.readtext(img)

    for r in result:
        bbox, text, prob = r
        x1, y1 = bbox[0]
        x2, y2 = bbox[2]
        type = text_cls(text)
        bb.add(img, x1, y1, x2, y2, text, TYPE2COLOR[type])

    x = 0

    return img
