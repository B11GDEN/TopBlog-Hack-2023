from __future__ import annotations
from modules.instances import Instance
from modules.search import get_free_instance_by_name_in, closest_top_instance


SEARCH_LIST = [
    {'key': 'ERViews', 'search': 'bottom', 'values': ['number']},
    # {'key': 'реакций (ср)', 'search': 'bottom', 'values': ['number']},
]


def search_user(instances: list[Instance], h: int, w: int):
    idx = get_free_instance_by_name_in(instances, 'обновлен')
    if idx is not None:
        user_idx = closest_top_instance(instances, instances[idx], ['text'])
        if user_idx is not None:
            instances[user_idx].is_user = True
            return instances[user_idx]
    return None
