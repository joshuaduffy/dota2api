#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Some tests using multiple calls in proper ways"""

import unittest
import os
from dota2api.src.urls import *
from mock import Mock

import dota2api
from dota2api.src.exceptions import APIAuthenticationError
from dota2api import RequestExecutor

DEFAULT_MATCHES_SIZE = 100
LANGUAGE_PAR = 'language=en_us'
STEAM_ID_PAR = 'key=' + os.environ.get('D2_API_KEY')


class RequestMock(object):

    def __init__(self):
        self.status_code = 666

    def json(self):
        return { 'result': 'whatever'}

    def configure_success(self):
        self.status_code = 200
        return self

class UrlMatcher(object):
    def __init__(self, base_url, *args):
        self.args = args
        self.base_url = base_url

    def __eq__(self, other):
        print other

        if type(other) != str:
            return False

        if not other.startswith(self.base_url):
            return False

        all_args = str(other).split('?')[1]
        splitted_args = all_args.split("&")

        for arg in self.args:
            if arg in splitted_args:
                splitted_args.remove(arg)
            else:
                return False

        if splitted_args:
            raise AssertionError("Args left: " + str(splitted_args))
        return True


def request_pars(*args):
    return '?' + '&'.join(args)


class ApiMatchTests(unittest.TestCase):
    """Tests relating to the Dota 2 API wrapper"""
    def setUp(self):
        """Set up test fixtures"""
        self.executor = RequestExecutor()
        self.api_test = dota2api.Initialise(os.environ['D2_API_KEY'], self.executor)

    def test_get_match_history_with_no_param(self):
        """Test__check_http_err get_match_history"""
        request_return = RequestMock().configure_success()

        self.executor.getJson = Mock(return_value=request_return)

        self.api_test.get_match_history()

        self.executor.getJson.assert_called_with(UrlMatcher(BASE_URL + GET_MATCH_HISTORY, LANGUAGE_PAR, 'account_id=None', STEAM_ID_PAR, 'format=json'))

    def test_get_match_history_with_limited_matches(self):
        request_return = RequestMock().configure_success()
        self.executor.getJson = Mock(return_value=request_return)

        self.api_test.get_match_history(matches_requested=1)

        self.executor.getJson.assert_called_with(UrlMatcher(BASE_URL + GET_MATCH_HISTORY, LANGUAGE_PAR, 'account_id=None', STEAM_ID_PAR, 'format=json', 'matches_requested=1'))

    def test_get_match_history_from_only_one_player(self):
        request_return = RequestMock().configure_success()
        self.executor.getJson = Mock(return_value=request_return)

        self.api_test.get_match_history(account_id=88585077, matches_requested=10)

        self.executor.getJson.assert_called_with(UrlMatcher(BASE_URL + GET_MATCH_HISTORY, LANGUAGE_PAR, 'account_id=88585077', STEAM_ID_PAR, 'format=json', 'matches_requested=10'))

    def test_get_match_details_test(self):
        request_return = RequestMock().configure_success()
        self.executor.getJson = Mock(return_value=request_return)

        self.api_test.get_match_details(match_id=988604774)

        self.executor.getJson.assert_called_with(UrlMatcher(BASE_URL + GET_MATCH_DETAILS, LANGUAGE_PAR, STEAM_ID_PAR, 'match_id=988604774', 'format=json'))


class TestRequestExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = RequestExecutor()

    def test_get_match_history_with_no_param(self):
        request = self.executor.getJson(
            BASE_URL + GET_MATCH_HISTORY + request_pars(LANGUAGE_PAR, 'account_id=None', STEAM_ID_PAR, 'format=json'))

        self.assertEqual(request.status_code, 200)

        result = request.json()['result']
        self.assertEqual(type(result), dict)
        self.assertEqual(len(result), 5)
        self.assertEqual(len(result['matches']), DEFAULT_MATCHES_SIZE)

    def test_get_match_history_with_limited_matches(self):
        request = self.executor.getJson(
            BASE_URL + GET_MATCH_HISTORY + request_pars(LANGUAGE_PAR, 'account_id=None', STEAM_ID_PAR, 'format=json', 'matches_requested=1'))

        self.assertEqual(request.status_code, 200)

        result = request.json()['result']
        self.assertEqual(len(result['matches']), 1)

    def test_get_match_history_from_only_one_player(self):
        request = self.executor.getJson(
            BASE_URL + GET_MATCH_HISTORY + request_pars(LANGUAGE_PAR, 'account_id=88585077', STEAM_ID_PAR, 'format=json', 'matches_requested=10'))

        self.assertEqual(request.status_code, 200)

        result = request.json()['result']
        self.assertEqual(len(result['matches']), 10)
        for match in result['matches']:
            player_is_in_match = bool([p for p in match['players'] if p['account_id'] == 88585077])
            self.assertTrue(player_is_in_match, 'Player was not in a match from the result')

    def test_requet_match_detail_on_a_non_existent_match(self):
        request = self.executor.getJson(
            BASE_URL + GET_MATCH_DETAILS + request_pars(LANGUAGE_PAR, STEAM_ID_PAR, 'format=json', 'match_id=1'))

        self.assertEqual(request.status_code, 200)

        result = request.json()['result']
        self.assertEqual(result['error'], 'Match ID not found')

    def test_requet_match_detail_with_no_match_id(self):
        request = self.executor.getJson(
            BASE_URL + GET_MATCH_DETAILS + request_pars(LANGUAGE_PAR, STEAM_ID_PAR, 'format=json', 'match_id=None'))

        self.assertEqual(request.status_code, 200)

        result = request.json()['result']
        self.assertEqual(result['error'], 'No Match ID specified')


class ApiOtherTests(unittest.TestCase):
    """Tests relating to the other tests."""
    def setUp(self):
        """Set up test fixtures"""
        self.api_test = dota2api.Initialise(os.environ['D2_API_KEY'])

    def get_league_listing_test(self):
        """Test get_league_listing"""
        # Is the response a dictionary
        self.assertEqual(type(self.api_test.get_league_listing().dict),
                         type(dict()))

    def get_live_league_games_test(self):
        """Test get_live_league_games"""
        # Is the response a dictionary
        self.assertEqual(type(self.api_test.get_live_league_games().dict),
                         type(dict()))

    def get_team_info_by_team_id_test(self):
        """Test get_team_info_by_team_id"""
        # Is the response a dictionary
        self.assertEqual(type(self.api_test.get_team_info_by_team_id().dict),
                         type(dict()))

    def get_player_summaries_test(self):
        """Test get_player_summaries"""
        # Is the response a dictionary
        self.assertEqual(type(self.api_test.get_player_summaries().dict),
                         type(dict()))

    def get_heroes_test(self):
        """Test get_heroes"""
        # Is the response a dictionary
        self.assertEqual(type(self.api_test.get_heroes().dict),
                         type(dict()))

    def get_game_items_test(self):
        """Test get_game_items"""
        # Is the response a dictionary
        self.assertEqual(type(self.api_test.get_game_items().dict),
                         type(dict()))

    def get_tournament_prize_pool_test(self):
        """Test get_tournament_prize_pool"""
        # Is the response a dictionary
        self.assertEqual(type(self.api_test.get_tournament_prize_pool().dict),
                         type(dict()))


def invalid_api_key_test():
    """Test invalid_api_key"""
    api_test = dota2api.Initialise("invalid")
    try:
        api_test.get_match_history()
    except APIAuthenticationError:
        assert True
