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

    def __repr__(self):
        return 'HistoryMatch match_id: {}'.format(self.match_id)


class HistoryPlayer(object):
    def __init__(self, **kwargs):
        self.account_id = kwargs.get('account_id')
        self.player_slot = kwargs['player_slot']
        self.hero = Hero(kwargs['hero_id'])

    def __repr__(self):
        return 'HistoryPlayer account_id: {}'.format(self.account_id)


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


def _load_item(index, **kwargs):
    live_game_item_index = "item" + str(index)
    match_history_item_index = "item_" + str(index)

    item_id = kwargs.get(match_history_item_index, kwargs.get(live_game_item_index))
    return Item(item_id)


class BasePlayer(object):
    def __init__(self, **kwargs):
        self.account_id = kwargs.get("account_id", -1)
        self.player_slot = kwargs["player_slot"]

        self.hero = Hero(kwargs["hero_id"])

        self.items = []
        self.items.append(_load_item(0, **kwargs))
        self.items.append(_load_item(1, **kwargs))
        self.items.append(_load_item(2, **kwargs))
        self.items.append(_load_item(3, **kwargs))
        self.items.append(_load_item(4, **kwargs))
        self.items.append(_load_item(5, **kwargs))

        self.kills = kwargs["kills"]
        self.deaths = kwargs.get("deaths", kwargs.get('death'))
        self.assists = kwargs["assists"]
        self.leaver_status = bool(kwargs.get("leaver_status"))

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

    def __repr__(self):
        return 'Player account_id: {}'.format(self.account_id)


class LiveLeagueGamePlayer(BasePlayer):
    def __init__(self, **kwargs):
        BasePlayer.__init__(self, **kwargs)
        self.ultimate_state = kwargs.get('ultimate_state')
        self.ultimate_cooldown = kwargs.get('ultimate_cooldown')
        self.respawn_timer = kwargs.get('respawn_timer')
        self.position_x = kwargs.get('position_x')
        self.position_y = kwargs.get('position_y')
        self.net_worth = kwargs.get('net_worth')

        # self.abilities = [AbilityLevel(**ability_kwargs) for ability_kwargs in kwargs.get('abilities', [])]


class AdditionalUnit(object):
    def __init__(self, **kwargs):
        self.unit_name = kwargs['unitname']
        self.items = []
        self.items.append(_load_item(0, **kwargs))
        self.items.append(_load_item(1, **kwargs))
        self.items.append(_load_item(2, **kwargs))
        self.items.append(_load_item(3, **kwargs))
        self.items.append(_load_item(4, **kwargs))
        self.items.append(_load_item(5, **kwargs))


class DetailMatchPlayer(BasePlayer):
    def __init__(self, **kwargs):
        BasePlayer.__init__(self, **kwargs)
        self.ability_upgrades = [AbilityUpgrade(**ability_upgrade_kwargs) for ability_upgrade_kwargs in
                                 kwargs.get("ability_upgrades", [])]
        self.additional_units = [AdditionalUnit(**additional_unit) for additional_unit in
                                 kwargs.get('additional_units', [])]


"""
class AbilityLevel(object):
    def __init__(self, **kwargs):
        self.ability_id = kwargs.get('ability_id')
        self.ability_level = kwargs.get('ability_level')
        self.ability_name = ability_name(self.ability_id)
"""


class Item(object):
    def __init__(self, item_id):
        item_json_map = item_map(item_id)
        self.id = item_id
        if item_json_map:
            import urls

            self.localized_name = item_json_map['localized_name']
            self.name = item_json_map['name']
            self.is_recipe = bool(item_json_map['recipe'])
            self.in_secret_shop = bool(item_json_map['secret_shop'])
            self.cost = item_json_map['cost']
            self.in_side_shop = bool(item_json_map['side_shop'])
            self.url_image = urls.BASE_ITEMS_IMAGES_URL + self.name.replace('item_', '') + '_lg.png'
        else:
            self.localized_name = ''
            self.name = ''
            self.is_recipe = False
            self.in_secret_shop = False
            self.cost = 0
            self.in_side_shop = 0
            self.url_image = ''

    def __repr__(self):
        return 'Item id: {} name: {}'.format(self.id, self.localized_name)


class AbilityUpgrade(object):
    def __init__(self, **kwargs):
        self.ability = kwargs['ability']
        self.ability_name = ability_name(self.ability)
        self.time = kwargs['time']
        self.level = kwargs['level']

    def __repr__(self):
        return 'AbilityUpgrade ability: {} name: {} level: {}'.format(self.ability, self.ability_name, self.level)


class LeagueListing(list):
    def __init__(self, **kwargs):
        map(self.append, [League(**league_kwargs) for league_kwargs in kwargs['leagues']])


class League(object):
    def __init__(self, **kwargs):
        self.league_id = kwargs.get('leagueid')
        self.name = kwargs.get('name')
        self.tournament_url = kwargs.get('tournament_url')
        self.description = kwargs.get('description')
        self.itemdef = kwargs.get('itemdef')

    def __repr__(self):
        return 'League id: {} name: {}'.format(self.league_id, self.name)


class LiveLeagueGames(list):
    def __init__(self, **kwargs):
        map(self.append, [LiveLeagueGame(**live_game_kwargs) for live_game_kwargs in kwargs['games']])


class LiveLeagueGame(object):
    def __init__(self, **kwargs):
        if 'radiant_team' in kwargs:
            self.radiant_team = LiveLeagueGameTeam(**kwargs.get('radiant_team'))
        if 'dire_team' in kwargs:
            self.dire_team = LiveLeagueGameTeam(**kwargs.get('dire_team'))
        self.lobby_id = kwargs.get('lobby_id')
        self.match_id = kwargs.get('match_id')
        self.spectators = kwargs.get('spectators')
        self.league_id = kwargs.get('league_id')
        self.stream_delay_s = kwargs.get('stream_delay_s')
        self.radiant_series_wins = kwargs.get('radiant_series_wins')
        self.dire_series_wins = kwargs.get('dire_series_wins')
        self.series_type = kwargs.get('series_type')
        self.league_tier = kwargs.get('league_tier')
        self.scoreboard = LiveLeagueGameScoreboard(**kwargs.get('scoreboard'))
        # should we load player list on the top of the result?
        # there are almost the same information on the scoreboard

    def __repr__(self):
        return 'LiveLeagueGame match_id: {} league_id: {}'.format(self.match_id, self.league_id)


class LiveLeagueGameScoreboard(object):
    def __init__(self, **kwargs):
        self.duration = kwargs.get('duration')
        self.roshan_respawn_timer = kwargs.get('roshan_respawn_timer')
        self.radiant = LiveLeagueGameTeamScoreboard(**kwargs.get('radiant'))
        self.dire = LiveLeagueGameTeamScoreboard(**kwargs.get('dire'))

    def __repr__(self):
        return 'LiveGameScoreboard duration: {} radiant kills: {} dire kills: {}'.format(self.duration,
                                                                                         self.radiant.score,
                                                                                         self.dire.score)


class LiveLeagueGameTeamScoreboard(object):
    def __init__(self, **kwargs):
        self.score = kwargs.get('score')
        self.tower_state = kwargs.get('tower_state')
        self.barracks_state = kwargs.get('barracks_state')

        self.picks = [Hero(args.get('hero_id')) for args in kwargs.get('picks', [])]
        self.bans = [Hero(args.get('hero_id')) for args in kwargs.get('bans', [])]

        # here we have a problem, the abilities lvls when the result is from the live game
        # are different json objects with the same names, when it gets converted
        # to python dicts, only the last result stands, and I think it would be great to
        # have this information in the Player object, instead of another list on LiveGameTeamScoreboard
        self.players = [LiveLeagueGamePlayer(**player_args) for player_args in kwargs.get('players')]

    def __repr__(self):
        return 'Scoreboard kills: {}'.format(self.score)


class LiveLeagueGameTeam(object):
    def __init__(self, **kwargs):
        self.team_name = kwargs.get('team_name')
        self.team_id = kwargs.get('team_id')
        self.team_logo = kwargs.get('team_logo')
        self.complete = kwargs.get('complete')

    def __repr__(self):
        return 'LiveGameTeam team_id: {} team_name: {}'.format(self.team_id, self.team_name)


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

    def __repr__(self):
        return 'Team id: {} name: {}'.format(self.team_id, self.name)


class PlayerSummaries(list):
    def __init__(self, **kwargs):
        map(self.append, [PlayerSummary(**summary_kwargs) for summary_kwargs in kwargs['players']])


class PlayerSummary(object):
    def __init__(self, **kwargs):
        self.steam_id = kwargs.get('steamid')
        self.community_visibility_state = kwargs.get('communityvisibilitystate')
        self.profile_state = kwargs.get('profilestate')
        self.persona_name = kwargs.get('personaname')
        self.last_logoff = kwargs.get('lastlogoff')
        self.profile_url = kwargs.get('profileurl')
        self.url_avatar = kwargs.get('avatar')
        self.url_avatar_medium = kwargs.get('avatarmedium')
        self.url_avatar_full = kwargs.get('avatarfull')
        self.persona_state = kwargs.get('personastate')
        self.primary_clan_id = kwargs.get('primaryclanid')
        self.time_created = kwargs.get('timecreated')
        self.persona_state_flags = kwargs.get('personastateflags')

    def __repr__(self):
        return 'Player steam_id: {} name: {}'.format(self.steam_id, self.persona_name)


class Heroes(list):
    def __init__(self, **kwargs):
        map(self.append, [Hero(hero_kwargs['id']) for hero_kwargs in kwargs['heroes']])


class Hero(object):
    def __init__(self, hero_id):
        import urls

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


class Items(list):
    def __init__(self, **kwargs):
        map(self.append, [Item(item_kwargs['id']) for item_kwargs in kwargs['items']])


class TournamentPrizePool(object):
    def __init__(self, **kwargs):
        self.prize_pool = kwargs.get('prize_pool')
        self.league_id = kwargs.get('league_id')

    def __repr__(self):
        return 'TournamentPrize league_id: {} prize: {}'.format(self.league_id, self.prize_pool)


def parse_result(result):
    if 'match_id' in result and 'radiant_win' in result:
        return DetailMatch(**result)

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


def ability_name(ability_id):
    ability = [ability['name'] for ability in abilities['abilities'] if ability['id'] == str(ability_id)]
    if ability:
        return ability[0]
    else:
        import logging

        logging.warning("It was not possible to parse ability id: {}".format(ability_id))
        return "UNKNOW"


def hero_map(hero_id):
    """
    Parse the lobby, will be available as ``hero_name``
    """

    hero_maps = [hero for hero in heroes['heroes'] if hero['id'] == hero_id]
    if hero_maps:
        return hero_maps[0]
    else:
        return None


def item_map(item_id):
    """
    Parse the item ids, will be available as ``item_0_name``, ``item_1_name``,
    ``item_2_name`` and so on
    """
    item_maps = [item for item in items['items'] if item['id'] == item_id]
    if item_maps:
        return item_maps[0]
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
