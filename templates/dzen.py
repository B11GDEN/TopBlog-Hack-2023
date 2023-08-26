from __future__ import annotations
from modules.instances import Instance

SEARCH_LIST = [
    {'key': 'Показы', 'search': 'bottom', 'values': ['number']},
    {'key': 'Дочитывания', 'search': 'bottom', 'values': ['number']},
    {'key': 'Общее время', 'search': 'bottom', 'values': ['number']},
    {'key': 'Подписки', 'search': 'bottom', 'values': ['number']},
]


def search_user(instances: list[Instance], h: int, w: int):
    return None