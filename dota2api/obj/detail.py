#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from basics import BasePlayer, cluster_name, lobby_name, game_mode_name, ability_name
from item import load_item
from ..src.utils import load_json_file


class DetailMatch(object):
    def __init__(self, **kwargs):
        self.is_radiant_win = bool(kwargs["radiant_win"])
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
        self.league_id = kwargs['leagueid']
        self.positive_votes = kwargs['positive_votes']
        self.negative_votes = kwargs['negative_votes']
        self.game_mode = kwargs['game_mode']
        self.game_mode_name = game_mode_name(self.game_mode)

        self.players = [DetailMatchPlayer(**player_kwargs) for player_kwargs in kwargs['players']]

    def __repr__(self):
        return 'Match match_id: {}'.format(self.match_id)


class DetailMatchPlayer(BasePlayer):
    def __init__(self, **kwargs):
        super(DetailMatchPlayer, self).__init__(**kwargs)
        self.ability_upgrades = [AbilityUpgrade(**ability_upgrade_kwargs) for ability_upgrade_kwargs in
                                 kwargs.get("ability_upgrades", [])]
        self.additional_units = [AdditionalUnit(**additional_unit) for additional_unit in
                                 kwargs.get('additional_units', [])]
        if kwargs.get("leaver_status") is not None:  
            self.leaver_status = Leaver(kwargs.get("leaver_status"))

class AbilityUpgrade(object):
    def __init__(self, **kwargs):
        self.ability = kwargs['ability']
        self.ability_name = ability_name(self.ability)
        self.time = kwargs['time']
        self.level = kwargs['level']

    def __repr__(self):
        return 'AbilityUpgrade ability: {} name: {} level: {}'.format(self.ability, self.ability_name, self.level)


class AdditionalUnit(object):
    def __init__(self, **kwargs):
        self.unit_name = kwargs['unitname']
        self.items = []
        self.items.append(load_item(0, **kwargs))
        self.items.append(load_item(1, **kwargs))
        self.items.append(load_item(2, **kwargs))
        self.items.append(load_item(3, **kwargs))
        self.items.append(load_item(4, **kwargs))
        self.items.append(load_item(5, **kwargs))


class Leaver(object):
    def __init__(self, id):
        leaver = leaver_map(id)
        self.id = leaver['id']
        self.name = leaver['name']
        self.description = leaver['description']


def leaver_map(leaver_id):
    return [l for l in leaver if l['id'] == leaver_id][0]


with open(load_json_file("leaver.json")) as leaver_json:
    leaver = json.load(leaver_json)