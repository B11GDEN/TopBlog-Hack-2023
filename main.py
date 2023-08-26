import cv2
import easyocr
from pathlib import Path
from bounding_box import bounding_box as bb
from modules.utils import TYPE2COLOR
from modules.instances import Instance
from modules.search import search
from templates import TGSTAT_SEARCH_LIST


def main():
    src = Path("C:/Datasets/SMM Hack")

    # im = src / 'tg' / 'images' / '0b751210-de3e-412a-b96f-5a8494daa6bf.PNG'
    im = src / 'tg' / 'images' / '1dcc636c-3537-45e2-b1d7-6d81142aeb32.png'
    # im = src / 'yt' / 'yt1' / '5caff51d-e3e6-4aca-9aea-9bfeff8c4d83.jpg'

    img = cv2.imread(str(im))

    reader = easyocr.Reader(['en', 'ru'], verbose=True)
    result = reader.readtext(img)
    instances = [Instance(r) for r in result]
    search(instances, TGSTAT_SEARCH_LIST)
    matched_instances = [ins for ins in instances if ins.match_instance is not None]

    for instance in instances:
        x1, y1, x2, y2 = instance.bbox
        color = TYPE2COLOR[instance.label]
        bb.add(img, x1, y1, x2, y2, str(instance.value), color)

    for key_instance in matched_instances:
        k_x1, k_y1, k_x2, k_y2 = key_instance.bbox
        v_x1, v_y1, v_x2, v_y2 = key_instance.match_instance.bbox
        start_point = (int(k_x1 + k_x2) // 2, int(k_y1 + k_y2) // 2)
        end_point = (int(v_x1 + v_x2) // 2, int(v_y1 + v_y2) // 2)
        img = cv2.arrowedLine(img, start_point, end_point, (255, 0, 0), 3)

    x = 0


if __name__ == '__main__':
    main()