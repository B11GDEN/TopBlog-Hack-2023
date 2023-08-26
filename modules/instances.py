from datetime import datetime


class Instance:
    def __init__(self, prediction: list):
        bbox, text, prob = prediction
        (x1, y1), (x2, y2) = bbox[0], bbox[2]
        self.prob = prob
        self.bbox = [x1, y1, x2, y2]
        self.value, self.label = self.get_cls(text)

    @staticmethod
    def get_cls(value: str):
        # проверка на число с процентом
        if value.endswith('%'):
            try:
                num = float(value[:-1])
                return num, 'number'
            except Exception:
                pass

        # если это предложение
        if len(value.split(' ')) > 1:
            return value, 'text'

        # проверка на обычное число
        try:
            num = float(value)
            return num, 'number'
        except Exception:
            pass

        # проверка на дату и время
        try:
            date = datetime.strptime(value, '%d.%m.%Y')
            return date, 'date'
        except:
            pass

        return value, 'text'


def get_instance_by_name(instances, target_text):
    for idx, instance in enumerate(instances):
        if instance.label == 'text' and instance.value == target_text:
            return idx
    return None


def closest_left_instance(instances: list, target_instance: Instance, pred_labels: list):
    tx1, ty1, tx2, ty2 = target_instance.bbox

    # фильтрация горизонтальных
    line_instances_idx = []
    for idx, instance in enumerate(instances):
        x1, y1, x2, y2 = instance.bbox
        iy1, iy2 = max(ty1, y1), min(ty2, y2)
        i_height = max(iy2 - iy1 + 1, 0)
        if i_height > 0:
            line_instances_idx.append(idx)

    # находим самый левый
    best_idx = None
    for idx in line_instances_idx:
        x1, y1, x2, y2 = instances[idx].bbox
        if x2 < tx1:
            if best_idx is None:
                best_idx = idx
            else:
                bx1, by1, bx2, by2 = instances[best_idx].bbox
                if bx2 < x2:
                    best_idx = idx

    return best_idx
