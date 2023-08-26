from __future__ import annotations
from modules.instances import Instance

from templates.tgstat import SEARCH_LIST as TGSTATS_SEARCH_LIST
from templates.tgstat import search_user as tgstats_search_user

from templates.dzen import SEARCH_LIST as DZEN_SEARCH_LIST
from templates.dzen import search_user as dzen_search_user


def choose_template(instances: list[Instance]):
    for instance in instances:
        if instance.label == 'text' and 'tgstat' in instance.value:
            return 'tgstat', TGSTATS_SEARCH_LIST, tgstats_search_user
        if instance.label == 'text' and ('dzen' in instance.value or 'дзен' in instance.value):
            return 'yandex dzen', DZEN_SEARCH_LIST, dzen_search_user

    return None, None, None

