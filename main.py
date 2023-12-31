import cv2
import easyocr
from pathlib import Path
from bounding_box import bounding_box as bb
from modules.utils import TYPE2COLOR
from modules.instances import Instance
from modules.search import search
from templates import choose_template


def main():
    src = Path("D:/GitHub/dataset")

    # im = src / 'tg' / 'images' / '0b751210-de3e-412a-b96f-5a8494daa6bf.PNG'
    # im = src / 'tg' / 'images' / '1dcc636c-3537-45e2-b1d7-6d81142aeb32.png'
    # im = src / 'zn' / 'images' / '6a930d50-ea2c-4ddd-ba1c-0378474eb215.png'
    # im = src / 'yt' / 'yt1' / '5caff51d-e3e6-4aca-9aea-9bfeff8c4d83.jpg'
    # im = src / 'vk' / 'images' / '2fded890-faca-4e9b-b07e-bb568c4a735c.jpg'
    im = src / 'tg' / 'images' / '0f00b0e7-e7eb-4797-ab76-9050b56fb319.png'
    # im = src / 'tg' / 'images' / '1a5f00c5-03d4-4b57-98fb-812343df61da.png'
    # im = src / 'tg' / 'images' / '2f405198-99fc-469a-ada9-446dcad47112.jpg'
    im = src / 'od_stat.jpg'

    img = cv2.imread(str(im))
    h, w, _ = img.shape

    reader = easyocr.Reader(['en', 'ru'], verbose=True)
    result = reader.readtext(img)
    instances = [Instance(r) for r in result]

    platform, search_list, search_user = choose_template(instances)

    search(instances, search_list)
    matched_instances = [ins for ins in instances if ins.match_instance is not None]
    user_instance = search_user(instances, h, w)

    for instance in instances:
        if not instance.is_user:
            x1, y1, x2, y2 = instance.bbox
            color = TYPE2COLOR[instance.label]
            bb.add(img, x1, y1, x2, y2, str(instance.value), color)

    # for key_instance in matched_instances:
    #     k_x1, k_y1, k_x2, k_y2 = key_instance.bbox
    #     v_x1, v_y1, v_x2, v_y2 = key_instance.match_instance.bbox
    #     start_point = (int(k_x1 + k_x2) // 2, int(k_y2))
    #     end_point = (int(v_x1 + v_x2) // 2, int(v_y2))
    #     img = cv2.arrowedLine(img, start_point, end_point, (255, 0, 0), 3)

    # if user_instance is not None:
    #     x1, y1, x2, y2 = user_instance.bbox
    #     color = 'orange'
    #     bb.add(img, x1, y1, x2, y2, str(user_instance.value), color)

    x = 0


if __name__ == '__main__':
    main()