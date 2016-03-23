#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Parse some of the values from the API, all can be found in the ``response`` returned"""

import json
import os
from .urls import BASE_ITEMS_IMAGES_URL, BASE_HERO_IMAGES_URL

try:
    from itertools import izip as zip
except ImportError:
    pass


def hero_id(response):
    """
    Parse the lobby, will be available as ``hero_name``
    """
    for player in response['players']:
        for hero in heroes['heroes']:
            if hero['id'] == player['hero_id']:
                player['hero_name'] = hero['localized_name']

    return response


def leaver(response):
    """
    Parse the lobby, will be available as ``hero_name``
    """
    for player in response['players']:
        for leaver in leavers:
            if leaver['id'] == player['leaver_status']:
                player['leaver_status_name'] = leaver['name']
                player['leaver_status_description'] = leaver['description']

    return response


def item_id(response):
    """
    Parse the item ids, will be available as ``item_0_name``, ``item_1_name``,
    ``item_2_name`` and so on
    """
    dict_keys = ['item_0', 'item_1', 'item_2',
                 'item_3', 'item_4', 'item_5']
    new_keys = ['item_0_name', 'item_1_name', 'item_2_name',
                'item_3_name', 'item_4_name', 'item_5_name']

    for player in response['players']:
        for key, new_key in zip(dict_keys, new_keys):
            for item in items['items']:
                if item['id'] == player[key]:
                    player[new_key] = item['localized_name']

    return response


def lobby_type(response):
    """
    Parse the lobby, will be available as ``lobby_type``
    """
    for lobby in lobbies['lobbies']:
        if lobby['id'] == response['lobby_type']:
            response['lobby_name'] = lobby['name']

    return response


def game_mode(response):
    """
    Parse the lobby, will be available as ``game_mode_name``
    """
    for mode in modes['modes']:
        if mode['id'] == response['game_mode']:
            response['game_mode_name'] = mode['name']

    return response


def cluster(response):
    """
    Parse the lobby, will be available as ``cluster_name``
    """
    for reg in regions['regions']:
        if reg['id'] == response['cluster']:
            response['cluster_name'] = reg['name']

    return response


def load_json_file(file_name):
    inp_file = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..",
        "ref",
        file_name))
    return inp_file


def parse_items_images_urls(resp):
    for item in resp['items']:
        item['url_image'] = BASE_ITEMS_IMAGES_URL + item['name'].replace('item_', '') + '_lg.png'


def parse_heroes_images(resp):
    for hero in resp['heroes']:
        base_images_url = BASE_HERO_IMAGES_URL + hero['name'].replace('npc_dota_hero_', '')

        hero['url_small_portrait'] = base_images_url + '_sb.png'
        hero['url_large_portrait'] = base_images_url + '_lg.png'
        hero['url_full_portrait'] = base_images_url + '_full.png'
        hero['url_vertical_portrait'] = base_images_url + '_vert.jpg'

# Load the files into memory as a response
with open(load_json_file("heroes.json")) as heroes_json:
    heroes = json.load(heroes_json)
with open(load_json_file("items.json")) as items_json:
    items = json.load(items_json)
with open(load_json_file("abilities.json")) as abilities_json:
    abilities = json.load(abilities_json)
with open(load_json_file("lobbies.json")) as lobbies_json:
    lobbies = json.load(lobbies_json)
with open(load_json_file("modes.json")) as modes_json:
    modes = json.load(modes_json)
with open(load_json_file("regions.json")) as regions_json:
    regions = json.load(regions_json)
with open(load_json_file("leaver.json")) as leaver_json:
    leavers = json.load(leaver_json)
