#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Dota 2 API wrapper and parser in Python - http://dota2api.readthedocs.org"""

__author__ = "Joshua Duffy"
__date__ = "29/10/2014"
__version__ = "0.9.0"
__licence__ = "GPL"

import requests
import urllib
import os

import src.urls
import src.exceptions
import src.response


class Initialise(object):
    """When calling this you need to provide the ``api_key``
    You can also specify a ``language``

    :param api_key: (str) string with the ``api key``
    :param language: (str, optional) string that defaults to ``en_us`` if
        not set
    """
    def __init__(self, api_key=None, language=None):
        if api_key:
            self.api_key = api_key
        elif os.environ['D2_API_KEY']:
            self.api_key = os.environ['D2_API_KEY']
        else:
            raise src.exceptions.APIAuthenticationError()

        if not language:
            self.language = "en_us"
        else:
            self.language = language
        self.__format = "json"

    def get_match_history(self, account_id=None, **kwargs):
        """Returns a dictionary containing a list of the most recent dota matches

        :param hero_id: (int, optional)
        :param game_mode: (int, optional) see ``ref/modes.json``
        :param skill: (int, optional) see ``ref/skill.json``
        :param date_min: (int, optional) unix timestamp rounded to the
            nearest day
        :param date_max: (int, optional) unix timestamp rounded to the
            nearest day
        :param min_players: (int, optional) only return matches with minimum
            amount of players
        :param league_id: (int, optional) for ids use ``get_league_listing()``
        :param start_at_match_id: (int, optional) start at matches equal to or
            older than this match id
        :param matches_requested: (int, optional) defaults to ``100``
        :param tournament_games_only: (str, optional) limit results to
            tournament matches only
        :return: dictionary of matches see ``examples``
        """
        if 'account_id' not in kwargs:
            kwargs['account_id'] = account_id
        url = self.__build_url(src.urls.GET_MATCH_HISTORY, **kwargs)
        req = requests.get(url)
        if not self.__check_http_err(req.status_code):
            return src.response.Dota2Response(req.json()['result'], url)

    def get_match_details(self, match_id=None, **kwargs):
        """Returns a dictionary containing the details for a dota 2 match

        :param match_id: (int, optional)
        :return: dictionary of matches see ``examples``
        """
        if 'match_id' not in kwargs:
            kwargs['match_id'] = match_id
        url = self.__build_url(src.urls.GET_MATCH_DETAILS, **kwargs)
        req = requests.get(url)
        if not self.__check_http_err(req.status_code):
            return src.response.Dota2MatchDetails(req.json()['result'], url)

    def get_league_listing(self):
        """Returns a dictionary containing a list of all ticketed leagues

        :param match_id: (int, optional)
        :return: dictionary of ticketed leagues see ``examples``
        """
        url = self.__build_url(src.urls.GET_LEAGUE_LISTING)
        req = requests.get(url)
        if not self.__check_http_err(req.status_code):
            return src.response.Dota2Response(req.json()['result'], url)

    def get_live_league_games(self):
        """Returns a dictionary containing a list of ticked games in progress

        :return: dictionary of live games see ``examples``
        """
        url = self.__build_url(src.urls.GET_LIVE_LEAGUE_GAMES)
        req = requests.get(url)
        if not self.__check_http_err(req.status_code):
            return src.response.Dota2Response(req.json()['result'], url)

    def get_team_info_by_team_id(self, start_at_team_id=None, **kwargs):
        """Returns a dictionary containing a in-game teams

        :param start_at_team_id: (int, optional)
        :param teams_requested: (int, optional)
        :return: dictionary of teams see ``examples``
        """
        if 'start_at_team_id' not in kwargs:
            kwargs['start_at_team_id'] = start_at_team_id
        url = self.__build_url(src.urls.GET_TEAM_INFO_BY_TEAM_ID, **kwargs)
        req = requests.get(url)
        if not self.__check_http_err(req.status_code):
            return src.response.Dota2Response(req.json()['result'], url)

    def get_player_summaries(self, steamids=None, **kwargs):
        """Returns a dictionary containing a player summaries

        :param steamids: (list) list of ``64-bit`` steam ids
        :return: dictionary of player summaries see ``examples``
        """
        if 'steamids' not in kwargs:
            kwargs['steamids'] = steamids
        url = self.__build_url(src.urls.GET_PLAYER_SUMMARIES, **kwargs)
        req = requests.get(url)
        if not self.__check_http_err(req.status_code):
            return src.response.Dota2Response(req.json()['response'], url)

    def get_heroes(self):
        """Returns a dictionary of in-game heroes, used to parse ids into localised names

        :return: dictionary of heroes see ``examples``
        """
        url = self.__build_url(src.urls.GET_HEROES)
        req = requests.get(url)
        if not self.__check_http_err(req.status_code):
            return src.response.Dota2Response(req.json()['result'], url)

    def get_game_items(self):
        """Returns a dictionary of in-game items, used to parse ids into localised names

        :return: dictionary of items see ``examples``
        """
        url = self.__build_url(src.urls.GET_GAME_ITEMS)
        req = requests.get(url)
        if not self.__check_http_err(req.status_code):
            return src.response.Dota2Response(req.json()['result'], url)

    def get_tournament_prize_pool(self, leagueid=None, **kwargs):
        """Returns a dictionary that includes community funded tournament prize pools

        :param leagueid: (int, optional)
        :return: dictionary of prize pools see ``examples``
        """
        if 'leagueid' not in kwargs:
            kwargs['leagueid'] = leagueid
        url = self.__build_url(src.urls.GET_TOURNAMENT_PRIZE_POOL)
        req = requests.get(url)
        if not self.__check_http_err(req.status_code):
            return src.response.Dota2Response(req.json()['result'], url)

    def __build_url(self, api_call, **kwargs):
        """Builds the api query"""
        kwargs['key'] = self.api_key
        if 'language' not in kwargs:
            kwargs['language'] = self.language
        if 'format' not in kwargs:
            kwargs['format'] = self.__format
        api_query = urllib.urlencode(kwargs)

        return "{0}{1}?{2}".format(src.urls.BASE_URL,
                                   api_call,
                                   api_query)

    def __check_http_err(self, status_code):
        """Raises an exception if we get a http error"""
        if status_code == 403:
            raise src.exceptions.APIAuthenticationError(self.api_key)
        elif status_code == 503:
            raise src.exceptions.APITimeoutError()
        else:
            return False
