import easyocr

from bounding_box import bounding_box as bb
from modules.utils import TYPE2COLOR
from modules.instances import Instance


def inference(img):

    reader = easyocr.Reader(['en', 'ru'], verbose=True)
    result = reader.readtext(img)
    instances = [Instance(r) for r in result]

    for instance in instances:
        x1, y1, x2, y2 = instance.bbox
        color = TYPE2COLOR[instance.label]
        bb.add(img, x1, y1, x2, y2, str(instance.value), color)

    return img
