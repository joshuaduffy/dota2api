#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Dota 2 API wrapper and parser in Python"""

__author__ = "Joshua Duffy, Evaldo Bratti"
__date__ = "29/10/2014"
__version__ = "1.3.1"
__licence__ = "GPL"

import json
import collections

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

import os
import requests

from .src import urls, exceptions, response, parse


class Initialise(object):
    """When calling this you need to provide the ``api_key``
    You can also specify a ``language``

    :param api_key: (str) string with the ``api key``
    :param logging: (bool, optional) set this to True for logging output
    """

    def __init__(self, api_key=None, executor=None, language=None, logging=None):
        if api_key:
            self.api_key = api_key
        elif 'D2_API_KEY' in os.environ:
            self.api_key = os.environ['D2_API_KEY']
        else:
            raise exceptions.APIAuthenticationError()

        if not language:
            self.language = "en_us"
        else:
            self.language = language

        if not executor:
            self.executor = requests.get
        else:
            self.executor = executor

        if logging:
            self.logger = _setup_logger()
        else:
            self.logger = None

        self.__format = "json"

    def get_match_history(self, account_id=None, **kwargs):
        """Returns a dictionary containing a list of the most recent Dota matches

        :param account_id: (int, optional)
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
        :return: dictionary of matches, see :doc:`responses </responses>`
        """
        if 'account_id' not in kwargs:
            kwargs['account_id'] = account_id
        url = self.__build_url(urls.GET_MATCH_HISTORY, **kwargs)
        req = self.executor(url)
        if self.logger:
            self.logger.info('URL: {0}'.format(url))
        if not self.__check_http_err(req.status_code):
            return response.build(req, url)

    def get_match_history_by_seq_num(self, start_at_match_seq_num=None, **kwargs):
        """Returns a dictionary containing a list of Dota matches in the order they were recorded

        :param start_at_match_seq_num: (int, optional) start at matches equal to or
            older than this match id
        :param matches_requested: (int, optional) defaults to ``100``
        :return: dictionary of matches, see :doc:`responses </responses>`
        """
        if 'start_at_match_seq_num' not in kwargs:
            kwargs['start_at_match_seq_num'] = start_at_match_seq_num
        url = self.__build_url(urls.GET_MATCH_HISTORY_BY_SEQ_NUM, **kwargs)
        req = self.executor(url)
        if self.logger:
            self.logger.info('URL: {0}'.format(url))
        if not self.__check_http_err(req.status_code):
            return response.build(req, url)

    def get_match_details(self, match_id=None, **kwargs):
        """Returns a dictionary containing the details for a Dota 2 match

        :param match_id: (int, optional)
        :return: dictionary of matches, see :doc:`responses </responses>`
        """
        if 'match_id' not in kwargs:
            kwargs['match_id'] = match_id
        url = self.__build_url(urls.GET_MATCH_DETAILS, **kwargs)
        req = self.executor(url)
        if self.logger:
            self.logger.info('URL: {0}'.format(url))
        if not self.__check_http_err(req.status_code):
            return response.build(req, url)

    def get_league_listing(self):
        """Returns a dictionary containing a list of all ticketed leagues

        :return: dictionary of ticketed leagues, see :doc:`responses </responses>`
        """
        url = self.__build_url(urls.GET_LEAGUE_LISTING)
        req = self.executor(url)
        if self.logger:
            self.logger.info('URL: {0}'.format(url))
        if not self.__check_http_err(req.status_code):
            return response.build(req, url)

    def get_live_league_games(self):
        """Returns a dictionary containing a list of ticked games in progress

        :return: dictionary of live games, see :doc:`responses </responses>`
        """
        url = self.__build_url(urls.GET_LIVE_LEAGUE_GAMES)
        req = self.executor(url)
        if self.logger:
            self.logger.info('URL: {0}'.format(url))
        if not self.__check_http_err(req.status_code):
            return response.build(req, url)

    def get_team_info_by_team_id(self, start_at_team_id=None, **kwargs):
        """Returns a dictionary containing a in-game teams

        :param start_at_team_id: (int, optional)
        :param teams_requested: (int, optional)
        :return: dictionary of teams, see :doc:`responses </responses>`
        """
        if 'start_at_team_id' not in kwargs:
            kwargs['start_at_team_id'] = start_at_team_id
        url = self.__build_url(urls.GET_TEAM_INFO_BY_TEAM_ID, **kwargs)
        req = self.executor(url)
        if self.logger:
            self.logger.info('URL: {0}'.format(url))
        if not self.__check_http_err(req.status_code):
            return response.build(req, url)

    def get_player_summaries(self, steamids=None, **kwargs):
        """Returns a dictionary containing a player summaries

        :param steamids: (list) list of ``32-bit`` or ``64-bit`` steam ids, notice
                                that api will convert if ``32-bit`` are given
        :return: dictionary of player summaries, see :doc:`responses </responses>`
        """
        if not isinstance(steamids, collections.Iterable):
            steamids = [steamids]

        base64_ids = list(map(convert_to_64_bit, filter(lambda x: x is not None, steamids)))

        if 'steamids' not in kwargs:
            kwargs['steamids'] = base64_ids
        url = self.__build_url(urls.GET_PLAYER_SUMMARIES, **kwargs)
        req = self.executor(url)
        if self.logger:
            self.logger.info('URL: {0}'.format(url))
        if not self.__check_http_err(req.status_code):
            return response.build(req, url)

    def get_heroes(self, **kwargs):
        """Returns a dictionary of in-game heroes, used to parse ids into localised names

        :return: dictionary of heroes, see :doc:`responses </responses>`
        """
        url = self.__build_url(urls.GET_HEROES, **kwargs)
        req = self.executor(url)
        if self.logger:
            self.logger.info('URL: {0}'.format(url))
        if not self.__check_http_err(req.status_code):
            return response.build(req, url)

    def get_game_items(self, **kwargs):
        """Returns a dictionary of in-game items, used to parse ids into localised names

        :return: dictionary of items, see :doc:`responses </responses>`
        """
        url = self.__build_url(urls.GET_GAME_ITEMS, **kwargs)
        req = self.executor(url)
        if self.logger:
            self.logger.info('URL: {0}'.format(url))
        if not self.__check_http_err(req.status_code):
            return response.build(req, url)

    def get_tournament_prize_pool(self, leagueid=None, **kwargs):
        """Returns a dictionary that includes community funded tournament prize pools

        :param leagueid: (int, optional)
        :return: dictionary of prize pools, see :doc:`responses </responses>`
        """
        if 'leagueid' not in kwargs:
            kwargs['leagueid'] = leagueid
        url = self.__build_url(urls.GET_TOURNAMENT_PRIZE_POOL, **kwargs)
        req = self.executor(url)
        if self.logger:
            self.logger.info('URL: {0}'.format(url))
        if not self.__check_http_err(req.status_code):
            return response.build(req, url)

    def update_game_items(self):
        """
        Update the item reference data via the API
        """
        _save_dict_to_file(self.get_game_items(), "items.json")

    def update_heroes(self):
        """
        Update the hero reference data via the API
        """
        _save_dict_to_file(self.get_heroes(), "heroes.json")

    def __build_url(self, api_call, **kwargs):
        """Builds the api query"""
        kwargs['key'] = self.api_key
        if 'language' not in kwargs:
            kwargs['language'] = self.language
        if 'format' not in kwargs:
            kwargs['format'] = self.__format
        api_query = urlencode(kwargs)

        return "{0}{1}?{2}".format(urls.BASE_URL,
                                   api_call,
                                   api_query)

    def __check_http_err(self, status_code):
        """Raises an exception if we get a http error"""
        if status_code == 403:
            raise exceptions.APIAuthenticationError(self.api_key)
        elif status_code == 503:
            raise exceptions.APITimeoutError()
        else:
            return False


def convert_to_64_bit(number):
    min64b = 76561197960265728
    if number < min64b:
        return number + min64b
    return number


def _setup_logger():
    import logging
    logging.basicConfig(level=logging.NOTSET)  # Will log all
    return logging.getLogger(__name__)


def _save_dict_to_file(json_dict, file_name):
    out_file = open(parse.load_json_file(file_name), "w")
    json.dump(json_dict, out_file, indent=4)
    out_file.close()
