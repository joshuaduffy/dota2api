#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest

from dota2api.src.urls import *
from dota2api import Initialise
from dota2api.src import exceptions
from tests.utils import *


class UrlsMatchTests(unittest.TestCase):
    def setUp(self):
        self.api = Initialise(os.environ['D2_API_KEY'])

    def test_api_authentication_error(self):
        self.api.executor = RequestMock().configure_authentication_error()
        self.assertRaises(exceptions.APIAuthenticationError, self.api.get_match_history)
        self.api.executor.assert_called()

    def test_api_timeout_error(self):
        self.api.executor = RequestMock().configure_timeout_error()
        self.assertRaises(exceptions.APITimeoutError, self.api.get_match_history)
        self.api.executor.assert_called()

    def test_get_match_history_with_no_param(self):
        matcher = UrlMatcher(BASE_URL + GET_MATCH_HISTORY,
                             LANGUAGE_PAR,
                             'account_id=None',
                             STEAM_ID_PAR,
                             'format=json')

        self.api.executor = RequestMock(matcher).configure_success()
        self.api.get_match_history()

        self.api.executor.assert_called()

    def test_get_match_history_with_limited_matches(self):
        matcher = UrlMatcher(BASE_URL + GET_MATCH_HISTORY, LANGUAGE_PAR, 'account_id=None', STEAM_ID_PAR,
                             'format=json', 'matches_requested=1')

        self.api.executor = RequestMock(matcher).configure_success()
        self.api.get_match_history(matches_requested=1)

        self.api.executor.assert_called()

    def test_get_match_history_from_only_one_player(self):
        matcher = UrlMatcher(BASE_URL + GET_MATCH_HISTORY, LANGUAGE_PAR, 'account_id=88585077',
                             STEAM_ID_PAR, 'format=json', 'matches_requested=10')

        self.api.executor = RequestMock(matcher).configure_success()
        self.api.get_match_history(account_id=88585077, matches_requested=10)
        self.api.executor.assert_called()

    def test_get_match_details_test(self):
        matcher = UrlMatcher(BASE_URL + GET_MATCH_DETAILS, LANGUAGE_PAR, STEAM_ID_PAR,
                             'match_id=988604774', 'format=json')

        self.api.executor = RequestMock(matcher).configure_success()
        self.api.get_match_details(match_id=988604774)
        self.api.executor.assert_called()

    def test_get_league_list(self):
        matcher = UrlMatcher(BASE_URL + GET_LEAGUE_LISTING, LANGUAGE_PAR, STEAM_ID_PAR, 'format=json')

        self.api.executor = RequestMock(matcher).configure_success()
        self.api.get_league_listing()
        self.api.executor.assert_called()

    def test_get_live_league_games(self):
        matcher = UrlMatcher(BASE_URL + GET_LIVE_LEAGUE_GAMES, LANGUAGE_PAR, STEAM_ID_PAR, 'format=json')

        self.api.executor = RequestMock(matcher).configure_success()
        self.api.get_live_league_games()
        self.api.executor.assert_called()

    def test_get_team_info_by_team_id(self):
        matcher = UrlMatcher(BASE_URL + GET_TEAM_INFO_BY_TEAM_ID, LANGUAGE_PAR, STEAM_ID_PAR, 'start_at_team_id=None',
                             'format=json')

        self.api.executor = RequestMock(matcher).configure_success()
        self.api.get_team_info_by_team_id()
        self.api.executor.assert_called()

    def test_get_team_info_by_team_id_with_parameter(self):
        matcher = UrlMatcher(BASE_URL + GET_TEAM_INFO_BY_TEAM_ID, LANGUAGE_PAR, STEAM_ID_PAR,
                             'start_at_team_id=123', 'format=json')

        self.api.executor = RequestMock(matcher).configure_success()
        self.api.get_team_info_by_team_id(123)
        self.api.executor.assert_called()

    def test_get_player_summaries(self):
        matcher = UrlMatcher(BASE_URL + GET_PLAYER_SUMMARIES, LANGUAGE_PAR, STEAM_ID_PAR,
                             'steamids=76561198049003839', 'format=json')

        self.api.executor = RequestMock(matcher).configure_success()
        account_id = 88738111
        self.api.get_player_summaries(convert_to_64_bit(account_id))
        self.api.executor.assert_called()

    def test_get_heroes(self):
        matcher = UrlMatcher(BASE_URL + GET_HEROES, STEAM_ID_PAR, LANGUAGE_PAR, 'format=json')

        self.api.executor = RequestMock(matcher).configure_success()
        self.api.get_heroes()
        self.api.executor.assert_called()

    def test_get_game_items(self):
        matcher = UrlMatcher(BASE_URL + GET_GAME_ITEMS, STEAM_ID_PAR, LANGUAGE_PAR, 'format=json')

        self.api.executor = RequestMock(matcher).configure_success()
        self.api.get_game_items()
        self.api.executor.assert_called()

    def test_get_tournament_prize_pool(self):
        matcher = UrlMatcher(BASE_URL + GET_TOURNAMENT_PRIZE_POOL, STEAM_ID_PAR, LANGUAGE_PAR,
                             'leagueid=1', 'format=json')

        self.api.executor = RequestMock(matcher).configure_success()
        self.api.get_tournament_prize_pool(1)
        self.api.executor.assert_called()



