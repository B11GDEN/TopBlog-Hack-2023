from __future__ import annotations
from modules.instances import Instance

SEARCH_LIST = [
    {'key': 'ERR', 'search': 'left', 'values': ['number']},
    {'key': 'ERR24', 'search': 'left', 'values': ['number']},
    {'key': 'ИНДЕКС ЦИТИРОВАНИЯ', 'search': 'left', 'values': ['number']},
    # {'key': 'СРЕДНИЙ РЕКЛАМНЫЙ', 'search': 'left', 'values': ['number']},
    {'key': 'ПУБЛИКАЦИИ', 'search': 'left', 'values': ['text']},
    {'key': 'СРЕДНИЙ ОХВАТ', 'search': 'left', 'values': ['number']},
    {'key': 'канал создан', 'search': 'top', 'values': ['date']},
    {'key': 'добавлен в TGStat', 'search': 'top', 'values': ['date']},
    {'key': 'подписчиков читают посты', 'search': 'top', 'values': ['number']},
    {'key': 'подписчиков читают', 'search': 'top', 'values': ['number']},
    {'key': 'читают посты', 'search': 'top', 'values': ['number']},

    {'key': 'подписки', 'search': 'left', 'values': ['number']},
    {'key': 'отписки', 'search': 'left', 'values': ['number']},

    # {'key': 'сегодня', 'search': 'left', 'values': ['number']},
    # {'key': 'вчера', 'search': 'left', 'values': ['number']},
    # {'key': 'за неделю', 'search': 'left', 'values': ['number']},
    # {'key': 'за месяц', 'search': 'left', 'values': ['number']},
    #
    # {'key': 'за 12 часов', 'search': 'left', 'values': ['number']},
    # {'key': 'за 24 часа', 'search': 'left', 'values': ['number']},
    # {'key': 'за 48 часов', 'search': 'left', 'values': ['number']},

    {'key': 'уп. каналов', 'search': 'left', 'values': ['number']},
    {'key': 'упоминаний', 'search': 'left', 'values': ['number']},
    {'key': 'репостов', 'search': 'left', 'values': ['number']},

    {'key': 'вовлеченность', 'search': 'left', 'values': ['number']},
]


def search_user(instances: list[Instance], h: int, w: int):
    user_instance = None
    for instance in instances:
        if user_instance is None:
            user_instance = instance
            continue
        x1, y1, x2, y2 = user_instance.bbox
        r1 = ((w - x2)**2 + (y1)**2)**(1/2)
        x1, y1, x2, y2 = instance.bbox
        r2 = ((w - x2) ** 2 + (y1) ** 2) ** (1 / 2)
        if r2 < r1:
            user_instance = instance

    user_instance.is_user = True

    return user_instance
