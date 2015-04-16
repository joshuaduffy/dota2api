#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Parse some of the values from the API, all can be found in the ``response`` returned"""

import json
import os
from exceptions import APIError


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


class HistoryPlayer(object):
    def __init__(self, **kwargs):
        self.account_id = kwargs.get('account_id')
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

        self.items = []
        self.items.append(self.load_item(0, **kwargs))
        self.items.append(self.load_item(1, **kwargs))
        self.items.append(self.load_item(2, **kwargs))
        self.items.append(self.load_item(3, **kwargs))
        self.items.append(self.load_item(4, **kwargs))
        self.items.append(self.load_item(5, **kwargs))

        self.kills = kwargs["kills"]
        self.deaths = kwargs.get("deaths", kwargs.get('death'))
        self.assists = kwargs["assists"]
        self.leaver_status = kwargs.get("leaver_status")

        self.gold = kwargs["gold"]
        self.last_hits = kwargs["last_hits"]
        self.denies = kwargs["denies"]
        self.gold_per_min = kwargs["gold_per_min"]
        self.xp_per_min = kwargs["xp_per_min"]
        self.gold_spent = kwargs.get("gold_spent")
        self.hero_damage = kwargs.get("hero_damage")
        self.tower_damage = kwargs.get("tower_damage")
        self.hero_healing = kwargs.get("hero_healing")
        self.level = kwargs["level"]

        # live player status
        self.ultimate_state = kwargs.get('ultimate_state')
        self.ultimate_cooldown = kwargs.get('ultimate_cooldown')
        self.respawn_timer = kwargs.get('respawn_timer')
        self.position_x = kwargs.get('position_x')
        self.position_y = kwargs.get('position_y')
        self.net_worth = kwargs.get('net_worth')

        self.ability_upgrades = [AbilityUpgrade(**ability_upgrade_kwargs) for ability_upgrade_kwargs in
                                 kwargs.get("ability_upgrades", [])]

        self.abilities = [AbilityLevel(**ability_kwargs) for ability_kwargs in kwargs.get('abilities', [])]

    def load_item(self, index, **kwargs):
        live_game_item_index = "item" + str(index)
        match_history_item_index = "item_" + str(index)

        item_id = kwargs.get(match_history_item_index, kwargs.get(live_game_item_index))
        return item_id, item_name(item_id)


class AbilityUpgrade(object):
    def __init__(self, **kwargs):
        self.ability = kwargs['ability']
        self.time = kwargs['time']
        self.level = kwargs['level']


class LeagueListing(list):
    def __init__(self, **kwargs):
        map(self.append, [League(**league_kwargs) for league_kwargs in kwargs['leagues']])


class League(object):
    def __init__(self, **kwargs):
        self.leagueid = kwargs.get('leagueid')
        self.name = kwargs.get('name')
        self.tournament_url = kwargs.get('tournament_url')
        self.description = kwargs.get('description')
        self.itemdef = kwargs.get('itemdef')


class LiveLeagueGames(list):
    def __init__(self, **kwargs):
        map(self.append, [LiveLeagueGame(**live_game_kwargs) for live_game_kwargs in kwargs['games']])


class LiveLeagueGame(object):
    def __init__(self, **kwargs):
        if 'radiant_team' in kwargs:
            self.radiant_team = LiveGameTeam(**kwargs.get('radiant_team'))
        if 'dire_team' in kwargs:
            self.dire_team = LiveGameTeam(**kwargs.get('dire_team'))
        self.lobby_id = kwargs.get('lobby_id')
        self.match_id = kwargs.get('match_id')
        self.spectators = kwargs.get('spectators')
        self.league_id = kwargs.get('league_id')
        self.stream_delay_s = kwargs.get('stream_delay_s')
        self.radiant_series_wins = kwargs.get('radiant_series_wins')
        self.dire_series_wins = kwargs.get('dire_series_wins')
        self.series_type = kwargs.get('series_type')
        self.league_tier = kwargs.get('league_tier')
        self.scoreboard = LiveGameScoreboard(**kwargs.get('scoreboard'))
        # should we load player list on the top of the result?
        #there are almost the same information on the scoreboard


class LiveGameScoreboard(object):
    def __init__(self, **kwargs):
        self.duration = kwargs.get('duration')
        self.roshan_respawn_timer = kwargs.get('roshan_respawn_timer')
        self.radiant = LiveGameTeamScoreboard(**kwargs.get('radiant'))
        self.dire = LiveGameTeamScoreboard(**kwargs.get('dire'))


class LiveGameTeamScoreboard(object):
    def __init__(self, **kwargs):
        self.score = kwargs.get('score')
        self.tower_state = kwargs.get('tower_state')
        self.barracks_state = kwargs.get('barracks_state')
        self.picks = [(args.get('hero_id'), hero_name(args.get('hero_id'))) for args in kwargs.get('picks', [])]
        self.bans = [(args.get('hero_id'), hero_name(args.get('hero_id'))) for args in kwargs.get('bans', [])]
        # here we have a problem, the abilities lvls when the result is from the live game
        #are different json objects with the same names, when it gets converted
        #to python dicts, only the last result stands, and I think it would be great to
        #have this information in the Player object, instead of another list on LiveGameTeamScoreboard
        self.players = [Player(**player_args) for player_args in kwargs.get('players')]


class LiveGameTeam(object):
    def __init__(self, **kwargs):
        self.team_name = kwargs.get('team_name')
        self.team_id = kwargs.get('team_id')
        self.team_logo = kwargs.get('team_logo')
        self.complete = kwargs.get('complete')


class AbilityLevel(object):
    def __init__(self, **kwargs):
        self.ability_id = kwargs.get('ability_id')
        self.ability_level = kwargs.get('ability_level')


class Teams(list):
    def __init__(self, **kwargs):
        map(self.append, [Team(**team_args) for team_args in kwargs['teams']])


class Team(object):
    def __init__(self, **kwargs):
        self.team_id = kwargs.get('team_id')
        self.name = kwargs.get('name')
        self.tag = kwargs.get('tag')
        self.time_created = kwargs.get('time_created')
        self.rating = kwargs.get('rating')
        self.logo = kwargs.get('logo')
        self.logo_sponsor = kwargs.get('logo_sponsor')
        self.country_code = kwargs.get('country_code')
        self.url = kwargs.get('url')
        self.games_played_with_current_roster = kwargs.get('games_played_with_current_roster')
        self.player_0_account_id = kwargs.get('player_0_account_id')
        self.player_1_account_id = kwargs.get('player_1_account_id')
        self.player_2_account_id = kwargs.get('player_2_account_id')
        self.player_3_account_id = kwargs.get('player_3_account_id')
        self.player_4_account_id = kwargs.get('player_4_account_id')
        self.player_5_account_id = kwargs.get('player_5_account_id')
        self.player_6_account_id = kwargs.get('player_6_account_id')
        self.admin_account_id = kwargs.get('admin_account_id')


class PlayerSummaries(list):
    def __init__(self, **kwargs):
        map(self.append, [PlayerSummary(**summary_kwargs) for summary_kwargs in kwargs['players']])


class PlayerSummary(object):
    def __init__(self, **kwargs):
        self.steamid = kwargs.get('steamid')
        self.communityvisibilitystate = kwargs.get('communityvisibilitystate')
        self.profilestate = kwargs.get('profilestate')
        self.personaname = kwargs.get('personaname')
        self.lastlogoff = kwargs.get('lastlogoff')
        self.profileurl = kwargs.get('profileurl')
        self.avatar = kwargs.get('avatar')
        self.avatarmedium = kwargs.get('avatarmedium')
        self.avatarfull = kwargs.get('avatarfull')
        self.personastate = kwargs.get('personastate')
        self.primaryclanid = kwargs.get('primaryclanid')
        self.timecreated = kwargs.get('timecreated')
        self.personastateflags = kwargs.get('personastateflags')


class Heroes(list):
    def __init__(self, **kwargs):
        map(self.append, [Hero(**hero_kwargs) for hero_kwargs in kwargs['heroes']])


class Hero(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.id = kwargs.get('id')
        self.localized_name = kwargs.get('localized_name')


class Items(list):
    def __init__(self, **kwargs):
        map(self.append, [Item(**item_kwargs) for item_kwargs in kwargs['items']])


class Item(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.cost = kwargs.get('cost')
        self.secret_shop = kwargs.get('secret_shop')
        self.side_shop = kwargs.get('side_shop')
        self.recipe = kwargs.get('recipe')
        self.localized_name = kwargs.get('localized_name')


class TournamentPrizePool(object):
    def __init__(self, **kwargs):
        self.prize_pool = kwargs.get('prize_pool')
        self.league_id = kwargs.get('league_id')


def parse_result(result):
    if 'match_id' in result and 'radiant_win' in result:
        return Match(**result)

    if 'matches' in result:
        return HistoryMatches(**result)

    if 'leagues' in result:
        return LeagueListing(**result)

    if 'games' in result:
        return LiveLeagueGames(**result)

    if 'teams' in result:
        return Teams(**result)

    if 'players' in result:
        return PlayerSummaries(**result)

    if 'heroes' in result:
        return Heroes(**result)

    if 'items' in result:
        return Items(**result)

    if 'prize_pool' in result:
        return TournamentPrizePool(**result)

    raise APIError("There are no parser available for the result")


def hero_name(hero_id):
    """
    Parse the lobby, will be available as ``hero_name``
    """
    # print 'parsing hero' + str(hero_id)

    name = [hero['localized_name'] for hero in heroes['heroes'] if hero['id'] == hero_id]
    if name:
        return name[0]
    else:
        return ''


def item_name(item_id):
    """
    Parse the item ids, will be available as ``item_0_name``, ``item_1_name``,
    ``item_2_name`` and so on
    """
    # print 'parsing item' + str(item_id)
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