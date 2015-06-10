#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..src import urls
from ..src.utils import load_json_file
import json

with open(load_json_file("heroes.json")) as heroes_json:
    heroes = json.load(heroes_json)


def hero_map(hero_id):
    """
    Parse the lobby, will be available as ``hero_name``
    """

    hero_maps = [hero for hero in heroes['heroes'] if hero['id'] == hero_id]
    if hero_maps:
        return hero_maps[0]
    else:
        return None


class Heroes(list):
    def __init__(self, **kwargs):
        map(self.append, [Hero(hero_kwargs['id']) for hero_kwargs in kwargs['heroes']])

class Hero(object):
    def __init__(self, hero_id):
        self.id = hero_id
        hero_json_map = hero_map(hero_id)
        if hero_json_map:
            self.localized_name = hero_json_map['localized_name']
            self.name = hero_json_map['name']
            internal_name = self.name.replace('npc_dota_hero_', '')
            base_images_url = urls.BASE_HERO_IMAGES_URL + internal_name

            self.url_small_portrait = base_images_url + '_sb.png'
            self.url_large_portrait = base_images_url + '_lg.png'
            self.url_full_portrait = base_images_url + '_full.png'
            self.url_vertical_portrait = base_images_url + '_vert.jpg'
        else:
            self.localized_name = ''
            self.name = ''
            self.url_small_portrait = ''
            self.url_large_portrait = ''
            self.url_full_portrait = ''
            self.url_vertical_portrait = ''

    def __repr__(self):
        return 'Item id: {} name: {}'.format(self.id, self.localized_name)






