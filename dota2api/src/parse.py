#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Parse some of the values from the API, all can be found in the ``response`` returned"""

import json
import os
from exceptions import APIError


class HistoryMatches(object):
    def __init__(self, **kwargs):
        self.num_results = kwargs['num_results']
        self.total_results = kwargs['total_results']
        self.results_remaining = kwargs['results_remaining']
        self.matches = [HistoryMatch(**match) for match in kwargs['matches']]


class HistoryMatch(object):
    def __init__(self, **kwargs):
        self.match_id = kwargs['match_id']
        self.match_seq_num = kwargs['match_seq_num']
        self.start_time = kwargs['start_time']
        self.lobby_type = kwargs['lobby_type']
        self.lobby_name = lobby_name(self.lobby_type)
        self.radiant_team_id = kwargs['radiant_team_id']
        self.dire_team_id = kwargs['dire_team_id']

        self.players = [HistoryPlayer(**player) for player in kwargs['players']]


class HistoryPlayer(object):
    def __init__(self, **kwargs):
        self.account_id = kwargs['account_id']
        self.player_slot = kwargs['player_slot']
        self.hero_id = kwargs['hero_id']
        self.hero_name = hero_name(self.hero_id)


class Match(object):
    def __init__(self, **kwargs):
        self.radiant_win = kwargs["radiant_win"]
        self.duration = kwargs["duration"]
        self.start_time = kwargs["start_time"]
        self.match_id = kwargs["match_id"]
        self.match_seq_num = kwargs["match_seq_num"]
        self.tower_status_radiant = kwargs['tower_status_radiant']
        self.tower_status_dire = kwargs['tower_status_dire']
        self.barracks_status_radiant = kwargs['barracks_status_radiant']
        self.barracks_status_dire = kwargs['barracks_status_dire']
        self.cluster = kwargs['cluster']
        self.cluster_name = cluster_name(self.cluster)
        self.first_blood_time = kwargs['first_blood_time']
        self.lobby_type = kwargs['lobby_type']
        self.lobby_name = lobby_name(self.lobby_type)
        self.human_players = kwargs['human_players']
        self.leagueid = kwargs['leagueid']
        self.positive_votes = kwargs['positive_votes']
        self.negative_votes = kwargs['negative_votes']
        self.game_mode = kwargs['game_mode']
        self.game_mode_name = game_mode_name(self.game_mode)

        self.players = [Player(**player_kwargs) for player_kwargs in kwargs['players']]


class Player(object):
    def __init__(self, **kwargs):
        self.account_id = kwargs["account_id"]
        self.player_slot = kwargs["player_slot"]

        self.hero_id = kwargs["hero_id"]
        self.hero_name = hero_name(self.hero_id)

        self.item_0 = kwargs["item_0"]
        self.item_0_name = item_name(self.item_0)

        self.item_1 = kwargs["item_1"]
        self.item_1_name = item_name(self.item_1)

        self.item_2 = kwargs["item_2"]
        self.item_2_name = item_name(self.item_2)

        self.item_3 = kwargs["item_3"]
        self.item_3_name = item_name(self.item_3)

        self.item_4 = kwargs["item_4"]
        self.item_4_name = item_name(self.item_4)

        self.item_5 = kwargs["item_5"]
        self.item_5_name = item_name(self.item_5)

        self.kills = kwargs["kills"]
        self.deaths = kwargs["deaths"]
        self.assists = kwargs["assists"]
        self.leaver_status = kwargs["leaver_status"]

        self.gold = kwargs["gold"]
        self.last_hits = kwargs["last_hits"]
        self.denies = kwargs["denies"]
        self.gold_per_min = kwargs["gold_per_min"]
        self.xp_per_min = kwargs["xp_per_min"]
        self.gold_spent = kwargs["gold_spent"]
        self.hero_damage = kwargs["hero_damage"]
        self.tower_damage = kwargs["tower_damage"]
        self.hero_healing = kwargs["hero_healing"]
        self.level = kwargs["level"]

        self.ability_upgrades = [AbilityUpgrade(**ability_upgrade_kwargs) for ability_upgrade_kwargs in
                                 kwargs["ability_upgrades"]]


class AbilityUpgrade(object):
    def __init__(self, **kwargs):
        self.ability = kwargs['ability']
        self.time = kwargs['time']
        self.level = kwargs['level']


def parse_result(result):
    if 'match_id' in result and 'radiant_win' in result:
        return Match(**result)

    if 'matches' in result:
        return HistoryMatches(**result)
    
    raise APIError("There are no parser available for the result")


def hero_name(hero_id):
    """
    Parse the lobby, will be available as ``hero_name``
    """
    return [hero['localized_name'] for hero in heroes['heroes'] if hero['id'] == hero_id][0]


def item_name(item_id):
    """
    Parse the item ids, will be available as ``item_0_name``, ``item_1_name``,
    ``item_2_name`` and so on
    """
    name = [item['localized_name'] for item in items['items'] if item['id'] == item_id]
    if name:
        return name[0]
    else:
        return ''


def lobby_name(lobby_id):
    """
    Parse the lobby, will be available as ``lobby_type``
    """
    return [lobby['name'] for lobby in lobbies['lobbies'] if lobby['id'] == lobby_id][0]


def game_mode_name(mode_id):
    """
    Parse the lobby, will be available as ``game_mode_name``
    """
    return [mode['name'] for mode in modes['modes'] if mode['id'] == mode_id][0]


def cluster_name(region_id):
    """
    Parse the lobby, will be available as ``cluster_name``
    """
    return [region['name'] for region in regions['regions'] if region['id'] == region_id][0]


def load_json_file(file_name):
    inp_file = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..",
                                                    "ref",
                                                    file_name))
    return inp_file
    
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