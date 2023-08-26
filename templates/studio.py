from __future__ import annotations
from modules.instances import Instance
from modules.search import get_free_instance_by_name, closest_bottom_instance

SEARCH_LIST = [
    {'key': 'Просмотры', 'search': 'right', 'values': ['number']},
    {'key': 'Средний процент просмотра', 'search': 'right', 'values': ['number']},
    {'key': 'Время просмотра (часы)', 'search': 'right', 'values': ['number']},
    {'key': 'Подписчики', 'search': 'bottom', 'values': ['number']},
]


def search_user(instances: list[Instance], h: int, w: int):
    idx = get_free_instance_by_name(instances, 'ваш канал')
    if idx is not None:
        user_idx = closest_bottom_instance(instances, instances[idx], ['text'])
        if user_idx is not None:
            instances[user_idx].is_user = True
            return instances[user_idx]
    return None