from __future__ import annotations
from .instances import Instance


def get_instance_by_name(instances: list[Instance], target_text: str):
    for idx, instance in enumerate(instances):
        if instance.label == 'text' and instance.value == target_text:
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


def search(instances: list[Instance], search_list: list):
    for s in search_list:
        idx_key = get_instance_by_name(instances, s['key'])
        if idx_key is None:
            continue

        if s['search'] == 'left':
            idx_value = closest_left_instance(instances,
                                              target_instance=instances[idx_key], pred_labels=s['values'])
            if idx_value is not None:
                instances[idx_key].match_instance = instances[idx_value]