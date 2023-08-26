import cv2
import easyocr
from pathlib import Path
from bounding_box import bounding_box as bb
from modules.utils import TYPE2COLOR
from modules.instances import Instance


def main():
    src = Path("C:/Datasets/SMM Hack")

    # im = src / 'tg' / 'images' / '0b751210-de3e-412a-b96f-5a8494daa6bf.PNG'
    # im = src / 'tg' / 'images' / '1dcc636c-3537-45e2-b1d7-6d81142aeb32.png'
    im = src / 'yt' / 'yt1' / '5caff51d-e3e6-4aca-9aea-9bfeff8c4d83.jpg'

    img = cv2.imread(str(im))

    reader = easyocr.Reader(['en', 'ru'], verbose=True)
    result = reader.readtext(img)
    instances = [Instance(r) for r in result]

    for instance in instances:
        x1, y1, x2, y2 = instance.bbox
        color = TYPE2COLOR[instance.label]
        bb.add(img, x1, y1, x2, y2, str(instance.value), color)

    x = 0


if __name__ == '__main__':
    main()