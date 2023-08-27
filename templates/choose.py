from __future__ import annotations
from modules.instances import Instance

from templates.tgstat import SEARCH_LIST as TGSTATS_SEARCH_LIST
from templates.tgstat import search_user as tgstats_search_user

from templates.dzen import SEARCH_LIST as DZEN_SEARCH_LIST
from templates.dzen import search_user as dzen_search_user

from templates.studio import SEARCH_LIST as STUDIO_SEARCH_LIST
from templates.studio import search_user as studio_search_user

from templates.livedune import SEARCH_LIST as LIVEDUNE_SEARCH_LIST
from templates.livedune import search_user as livedune_search_user


def choose_template(instances: list[Instance]):
    for instance in instances:
        if instance.label == 'text' and 'tgstat' in instance.value:
            return 'telegram tgstat', TGSTATS_SEARCH_LIST, tgstats_search_user
        if instance.label == 'text' and ('dzen' in instance.value or 'дзен' in instance.value):
            return 'yandex dzen', DZEN_SEARCH_LIST, dzen_search_user
        if instance.label == 'text' and 'studiо' == instance.value:
            return 'youtube studio', STUDIO_SEARCH_LIST, studio_search_user
        if instance.label == 'text' and 'livedune' in instance.value:
            return 'telegram livedune', None, livedune_search_user
        if instance.label == 'text' and 'вконтакте' in instance.value:
            return 'вконтакте', None, lambda i, h, w: None

    return 'unknown', None, lambda i, h, w: None

