from __future__ import annotations
from modules.instances import Instance

from templates.tgstat import SEARCH_LIST as TGSTATS_SEARCH_LIST
from templates.tgstat import search_user as tgstats_search_user


def choose_template(instances: list[Instance]):
    for instance in instances:
        if instance.label == 'text' and 'tgstat' in instance.value:
            return 'tgstat', TGSTATS_SEARCH_LIST, tgstats_search_user

    return None, None

