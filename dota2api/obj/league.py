#!/usr/bin/env python
# -*- coding: utf-8 -*-

from basics import BasePlayer
from hero import Hero


class LiveLeagueGamePlayer(BasePlayer):
    def __init__(self, **kwargs):
        super(LiveLeagueGamePlayer, self).__init__(**kwargs)
        self.ultimate_state = kwargs.get('ultimate_state')
        self.ultimate_cooldown = kwargs.get('ultimate_cooldown')
        self.respawn_timer = kwargs.get('respawn_timer')
        self.position_x = kwargs.get('position_x')
        self.position_y = kwargs.get('position_y')
        self.net_worth = kwargs.get('net_worth')

        # self.abilities = [AbilityLevel(**ability_kwargs) for ability_kwargs in kwargs.get('abilities', [])]


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
        else:
            self.radiant_team = None
        if 'dire_team' in kwargs:
            self.dire_team = LiveLeagueGameTeam(**kwargs.get('dire_team'))
        else:
            self.dire_team = None

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


class TournamentPrizePool(object):
    def __init__(self, **kwargs):
        self.prize_pool = kwargs.get('prize_pool')
        self.league_id = kwargs.get('league_id')

    def __repr__(self):
        return 'TournamentPrize league_id: {} prize: {}'.format(self.league_id, self.prize_pool)

"""
class AbilityLevel(object):
    def __init__(self, **kwargs):
        self.ability_id = kwargs.get('ability_id')
        self.ability_level = kwargs.get('ability_level')
        self.ability_name = ability_name(self.ability_id)
"""

