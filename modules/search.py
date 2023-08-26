from __future__ import annotations
from .instances import Instance


def get_free_instance_by_name(instances: list[Instance], target_text: str):
    for idx, instance in enumerate(instances):
        if instance.label == 'text' and instance.value == target_text.lower().strip() and instance.match_instance is None:
            return idx
    return None


def closest_left_instance(instances: list[Instance], target_instance: Instance, pred_labels: list[str]):
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
        if instances[idx].label in pred_labels:
            x1, y1, x2, y2 = instances[idx].bbox
            if x2 < tx1:
                if best_idx is None:
                    best_idx = idx
                else:
                    bx1, by1, bx2, by2 = instances[best_idx].bbox
                    if bx2 < x2:
                        best_idx = idx

    return best_idx


def closest_top_instance(instances: list[Instance], target_instance: Instance, pred_labels: list[str]):
    tx1, ty1, tx2, ty2 = target_instance.bbox

    # фильтрация горизонтальных
    line_instances_idx = []
    for idx, instance in enumerate(instances):
        x1, y1, x2, y2 = instance.bbox
        ix1, ix2 = max(tx1, x1), min(tx2, x2)
        i_width = max(ix2 - ix1 + 1, 0)
        if i_width > 0:
            line_instances_idx.append(idx)

    # находим самый левый
    best_idx = None
    for idx in line_instances_idx:
        if instances[idx].label in pred_labels:
            x1, y1, x2, y2 = instances[idx].bbox
            if y2 < ty1:
                if best_idx is None:
                    best_idx = idx
                else:
                    bx1, by1, bx2, by2 = instances[best_idx].bbox
                    if by2 < y2:
                        best_idx = idx

    return best_idx


def closest_bottom_instance(instances: list[Instance], target_instance: Instance, pred_labels: list[str]):
    tx1, ty1, tx2, ty2 = target_instance.bbox

    # фильтрация горизонтальных
    line_instances_idx = []
    for idx, instance in enumerate(instances):
        x1, y1, x2, y2 = instance.bbox
        ix1, ix2 = max(tx1, x1), min(tx2, x2)
        i_width = max(ix2 - ix1 + 1, 0)
        if i_width > 0:
            line_instances_idx.append(idx)

    # находим самый левый
    best_idx = None
    for idx in line_instances_idx:
        if instances[idx].label in pred_labels:
            x1, y1, x2, y2 = instances[idx].bbox
            if y1 > ty2:
                if best_idx is None:
                    best_idx = idx
                else:
                    bx1, by1, bx2, by2 = instances[best_idx].bbox
                    if by1 > y1:
                        best_idx = idx

    return best_idx


def closest_right_instance(instances: list[Instance], target_instance: Instance, pred_labels: list[str]):
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
        if instances[idx].label in pred_labels:
            x1, y1, x2, y2 = instances[idx].bbox
            if x1 > tx2:
                if best_idx is None:
                    best_idx = idx
                else:
                    bx1, by1, bx2, by2 = instances[best_idx].bbox
                    if bx1 > x1:
                        best_idx = idx

    return best_idx


def closest_instance(instances: list[Instance], target_instance: Instance, pred_labels: list[str]):
    # находим самый ближний
    best_idx = None
    for idx, instance in enumerate(instances):
        if not (instance is target_instance) and instance.label in pred_labels:
            if best_idx is None:
                best_idx = idx
            else:
                x1, y1, x2, y2 = instance.bbox
                bx1, by1, bx2, by2 = instances[best_idx].bbox
                tx1, ty1, tx2, ty2 = target_instance.bbox

                r1 = ((x1 - tx1) ** 2 + (y1 - ty1) ** 2) ** 0.5
                r2 = ((bx1 - tx1) ** 2 + (by1 - ty1) ** 2) ** 0.5
                if r2 > r1:
                    best_idx = idx

    return best_idx


def search(instances: list[Instance], search_list: list):

    # Дефолтное поведение
    if search_list is None:
        for instance in instances:
            if instance.label == 'number' or instance.label == 'date':
                idx_value = closest_instance(instances, instance, ['text'])
                if idx_value is not None:
                    instance.match_instance = instances[idx_value]
        return

    # Шаблон найден
    for s in search_list:
        for _ in range(3):
            idx_key = get_free_instance_by_name(instances, s['key'])
            if idx_key is None:
                break

            if s['search'] == 'left':
                idx_value = closest_left_instance(instances,
                                                  target_instance=instances[idx_key], pred_labels=s['values'])
                if idx_value is not None:
                    instances[idx_key].match_instance = instances[idx_value]
            if s['search'] == 'top':
                idx_value = closest_top_instance(instances,
                                                 target_instance=instances[idx_key], pred_labels=s['values'])
                if idx_value is not None:
                    instances[idx_key].match_instance = instances[idx_value]
            if s['search'] == 'bottom':
                idx_value = closest_bottom_instance(instances,
                                                    target_instance=instances[idx_key], pred_labels=s['values'])
                if idx_value is not None:
                    instances[idx_key].match_instance = instances[idx_value]
            if s['search'] == 'right':
                idx_value = closest_right_instance(instances,
                                                   target_instance=instances[idx_key], pred_labels=s['values'])
                if idx_value is not None:
                    instances[idx_key].match_instance = instances[idx_value]
