import cv2
import easyocr

from bounding_box import bounding_box as bb
from modules.utils import TYPE2COLOR
from modules.instances import Instance
from modules.search import search
from templates import TGSTAT_SEARCH_LIST, tgstat_search_user


def inference(img):
    h, w, _ = img.shape

    reader = easyocr.Reader(['en', 'ru'], verbose=True)
    result = reader.readtext(img)
    instances = [Instance(r) for r in result]
    search(instances, TGSTAT_SEARCH_LIST)
    matched_instances = [ins for ins in instances if ins.match_instance is not None]
    user_instance = tgstat_search_user(instances, h, w)

    for instance in instances:
        if not instance.is_user:
            x1, y1, x2, y2 = instance.bbox
            color = TYPE2COLOR[instance.label]
            bb.add(img, x1, y1, x2, y2, str(instance.value), color)

    img_det = img.copy()

    for key_instance in matched_instances:
        k_x1, k_y1, k_x2, k_y2 = key_instance.bbox
        v_x1, v_y1, v_x2, v_y2 = key_instance.match_instance.bbox
        start_point = (int(k_x1 + k_x2) // 2, int(k_y1 + k_y2) // 2)
        end_point = (int(v_x1 + v_x2) // 2, int(v_y1 + v_y2) // 2)
        img = cv2.arrowedLine(img, start_point, end_point, (255, 0, 0), 3)

    x1, y1, x2, y2 = user_instance.bbox
    color = 'orange'
    bb.add(img, x1, y1, x2, y2, str(user_instance.value), color)

    return img_det, img, matched_instances, user_instance
