#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
from hero import Hero
from item import load_item
from ..src.utils import load_json_file
from dota2api.src import exceptions

class BasePlayer(object):
    def __init__(self, **kwargs):
        self.account_id = kwargs.get("account_id", -1)
        self.player_slot = kwargs["player_slot"]

        self.hero = Hero(kwargs["hero_id"])

        self.items = []
        self.items.append(load_item(0, **kwargs))
        self.items.append(load_item(1, **kwargs))
        self.items.append(load_item(2, **kwargs))
        self.items.append(load_item(3, **kwargs))
        self.items.append(load_item(4, **kwargs))
        self.items.append(load_item(5, **kwargs))

        self.kills = kwargs["kills"]
        self.deaths = kwargs.get("deaths", kwargs.get('death'))
        self.assists = kwargs["assists"]

        self.gold = kwargs.get("gold", 0)
        self.last_hits = kwargs["last_hits"]
        self.denies = kwargs["denies"]
        self.gold_per_min = kwargs["gold_per_min"]
        self.xp_per_min = kwargs["xp_per_min"]
        self.gold_spent = kwargs.get("gold_spent")
        self.hero_damage = kwargs.get("hero_damage")
        self.tower_damage = kwargs.get("tower_damage")
        self.hero_healing = kwargs.get("hero_healing")
        self.level = kwargs["level"]

    def __repr__(self):
        return 'Player account_id: {}'.format(self.account_id)


def lobby_name(lobby_id):
    """
    Parse the lobby, will be available as ``lobby_type``
    """
    lobby = [lobby['name'] for lobby in lobbies['lobbies'] if lobby['id'] == lobby_id]
    if lobby:
        return lobby[0]

    raise exceptions.APIError("It was not possible to parse lobby " + lobby_id)


def cluster_name(region_id):
    """
    Parse the lobby, will be available as ``cluster_name``
    """
    region = [region['name'] for region in regions['regions'] if region['id'] == region_id]
    if region:
        return region[0]

    raise exceptions.APIError("It was not possible to parse cluster " + region_id)


def game_mode_name(mode_id):
    """
    Parse the lobby, will be available as ``game_mode_name``
    """
    mode = [mode['name'] for mode in modes['modes'] if mode['id'] == mode_id]
    if mode:
        return mode[0]

    raise exceptions.APIError("It was not possible to parse game mode " + mode_id)


def ability_name(ability_id):
    ability = [ability['name'] for ability in abilities['abilities'] if ability['id'] == str(ability_id)]
    if ability:
        return ability[0]
    else:
        logging.getLogger('dota2api').warning("It was not possible to parse ability id: {}".format(ability_id))
        return "UNKNOW"

with open(load_json_file("abilities.json")) as abilities_json:
    abilities = json.load(abilities_json)

with open(load_json_file("regions.json")) as regions_json:
    regions = json.load(regions_json)

with open(load_json_file("lobbies.json")) as lobbies_json:
    lobbies = json.load(lobbies_json)

with open(load_json_file("modes.json")) as modes_json:
    modes = json.load(modes_json)
