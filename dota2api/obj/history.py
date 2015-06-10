#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hero import Hero
from basics import lobby_name


class HistoryMatches(object):
    def __init__(self, **kwargs):
        self.num_results = kwargs.get('num_results')
        self.total_results = kwargs.get('total_results')
        self.results_remaining = kwargs.get('results_remaining')
        self.matches = [HistoryMatch(**match) for match in kwargs['matches']]


class HistoryMatch(object):
    def __init__(self, **kwargs):
        self.match_id = kwargs['match_id']
        self.match_seq_num = kwargs['match_seq_num']
        self.start_time = kwargs['start_time']
        self.lobby_type = kwargs['lobby_type']
        self.lobby_name = lobby_name(self.lobby_type)
        self.radiant_team_id = kwargs.get('radiant_team_id')
        self.dire_team_id = kwargs.get('dire_team_id')

        self.players = [HistoryPlayer(**player) for player in kwargs['players']]

    def __repr__(self):
        return 'HistoryMatch match_id: {}'.format(self.match_id)


class HistoryPlayer(object):
    def __init__(self, **kwargs):
        self.account_id = kwargs.get('account_id')
        self.player_slot = kwargs['player_slot']
        self.hero = Hero(kwargs['hero_id'])


    def __repr__(self):
        return 'HistoryPlayer account_id: {}'.format(self.account_id)
