#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Some tests using multiple calls in proper ways"""

import unittest
import os
from dota2api.src.urls import *

import dota2api
from dota2api.src.exceptions import APIAuthenticationError, APITimeoutError

DEFAULT_MATCHES_SIZE = 100
LANGUAGE_PAR = 'language=en_us'
STEAM_ID_PAR = 'key=' + os.environ.get('D2_API_KEY')


def convert_to_64_bit(number):
    # Yes we should put this in the API - will be used to parse steam names
    return number + 76561197960265728


class RequestMock(object):

    def __init__(self):
        self.status_code = 666

    def json(self):
        return {'result': 'whatever'}

    def configure_success(self):
        self.status_code = 200
        return self

    def configure_authentication_error(self):
        self.status_code = 403
        return self

    def configure_timeout_error(self):
        self.status_code = 503
        return self


class UrlMatcher(object):
    def __init__(self, base_url, *args):
        self.args = args
        self.base_url = base_url

    def __eq__(self, other):
        if type(other) != str:
            raise AssertionError(str(other) + ' should be a string')

        if not other.startswith(self.base_url):
            raise AssertionError(other + ' does not start with ' + self.base_url)

        all_args = str(other).split('?')[1]
        splitted_args = all_args.split("&")

        for arg in self.args:
            if arg in splitted_args:
                splitted_args.remove(arg)
            else:
                raise AssertionError('The parameter ' + arg + ' is not in the url ' + other)

        if splitted_args:
            raise AssertionError("Args left: " + str(splitted_args))
        return True


class ApiMatchTests(unittest.TestCase):

    def setUp(self):
        self.api_test = dota2api.Initialise(os.environ['D2_API_KEY'])

    def test_api_authentication_error(self):
        def executor_mock(url):
            return RequestMock().configure_authentication_error()

        self.api_test.executor = executor_mock
        self.assertRaises(APIAuthenticationError, self.api_test.get_match_history)

    def test_api_timeout_error(self):
        def executor_mock(url):
            return RequestMock().configure_timeout_error()

        self.api_test.executor = executor_mock
        self.assertRaises(APITimeoutError, self.api_test.get_match_history)

    def test_get_match_history_with_no_param(self):
        def executor_mock(url):
            self.assertEqual(url, UrlMatcher(BASE_URL + GET_MATCH_HISTORY, LANGUAGE_PAR, 'account_id=None',
                                             STEAM_ID_PAR, 'format=json'))
            return RequestMock().configure_success()

        self.api_test.executor = executor_mock
        self.api_test.get_match_history()

    def test_get_match_history_with_limited_matches(self):
        def executor_mock(url):
            self.assertEqual(url, UrlMatcher(BASE_URL + GET_MATCH_HISTORY, LANGUAGE_PAR, 'account_id=None',
                                             STEAM_ID_PAR, 'format=json', 'matches_requested=1'))
            return RequestMock().configure_success()

        self.api_test.executor = executor_mock
        self.api_test.get_match_history(matches_requested=1)

    def test_get_match_history_from_only_one_player(self):
        def executor_mock(url):
            self.assertEqual(url, UrlMatcher(BASE_URL + GET_MATCH_HISTORY, LANGUAGE_PAR, 'account_id=88585077',
                                             STEAM_ID_PAR, 'format=json', 'matches_requested=10'))
            return RequestMock().configure_success()

        self.api_test.executor = executor_mock
        self.api_test.get_match_history(account_id=88585077, matches_requested=10)

    def test_get_match_details_test(self):
        def executor_mock(url):
            self.assertEqual(url, UrlMatcher(BASE_URL + GET_MATCH_DETAILS, LANGUAGE_PAR, STEAM_ID_PAR,
                                             'match_id=988604774', 'format=json'))
            return RequestMock().configure_success()

        self.api_test.executor = executor_mock
        self.api_test.get_match_details(match_id=988604774)

    def test_get_league_list(self):
        def executor_mock(url):
            self.assertEqual(url, UrlMatcher(BASE_URL + GET_LEAGUE_LISTING, LANGUAGE_PAR, STEAM_ID_PAR, 'format=json'))
            return RequestMock().configure_success()

        self.api_test.executor = executor_mock
        self.api_test.get_league_listing()

    def test_get_live_league_games(self):
        def executor_mock(url):
            self.assertEqual(url, UrlMatcher(BASE_URL + GET_LIVE_LEAGUE_GAMES, LANGUAGE_PAR, STEAM_ID_PAR,
                                             'format=json'))
            return RequestMock().configure_success()

        self.api_test.executor = executor_mock
        self.api_test.get_live_league_games()

    def test_get_team_info_by_team_id(self):
        def executor_mock(url):
            self.assertEqual(url, UrlMatcher(BASE_URL + GET_TEAM_INFO_BY_TEAM_ID, LANGUAGE_PAR, STEAM_ID_PAR,
                                             'start_at_team_id=None', 'format=json'))
            return RequestMock().configure_success()

        self.api_test.executor = executor_mock
        self.api_test.get_team_info_by_team_id()

    def test_get_team_info_by_team_id_with_parameter(self):
        def executor_mock(url):
            self.assertEqual(url, UrlMatcher(BASE_URL + GET_TEAM_INFO_BY_TEAM_ID, LANGUAGE_PAR, STEAM_ID_PAR,
                                             'start_at_team_id=123', 'format=json'))
            return RequestMock().configure_success()

        self.api_test.executor = executor_mock
        self.api_test.get_team_info_by_team_id(123)

#    def test_get_player_summaries(self):
#        def executor_mock(url):
#            self.assertEqual(url, UrlMatcher(BASE_URL + GET_PLAYER_SUMMARIES, LANGUAGE_PAR, STEAM_ID_PAR,
#                                             'steamids=76561198049003839', 'format=json'))
#            return RequestMock().configure_success()
#
#        self.api_test.executor = executor_mock
#        account_id = 88738111
#        self.api_test.get_player_summaries(convert_to_64_bit(account_id))


class TestRequestExecutor(unittest.TestCase):
    def setUp(self):
        import requests
        self.executor = requests.get

    def test_get_match_history_with_no_param(self):
        request = self.executor(
            BASE_URL + GET_MATCH_HISTORY + request_pars(LANGUAGE_PAR, 'account_id=None', STEAM_ID_PAR, 'format=json'))

        self.assertEqual(request.status_code, 200)

        result = request.json()['result']
        self.assertEqual(type(result), dict)
        self.assertEqual(len(result), 5)
        self.assertEqual(len(result['matches']), DEFAULT_MATCHES_SIZE)

    def test_get_match_history_with_limited_matches(self):
        request = self.executor(
            BASE_URL + GET_MATCH_HISTORY + request_pars(LANGUAGE_PAR, 'account_id=None', STEAM_ID_PAR, 'format=json',
                                                        'matches_requested=1'))

        self.assertEqual(request.status_code, 200)

        result = request.json()['result']
        self.assertEqual(len(result['matches']), 1)

    def test_get_match_history_from_only_one_player(self):
        request = self.executor(
            BASE_URL + GET_MATCH_HISTORY + request_pars(LANGUAGE_PAR, 'account_id=88585077', STEAM_ID_PAR,
                                                        'format=json', 'matches_requested=10'))

        self.assertEqual(request.status_code, 200)

        result = request.json()['result']
        self.assertEqual(len(result['matches']), 10)
        for match in result['matches']:
            player_is_in_match = bool([p for p in match['players'] if p['account_id'] == 88585077])
            self.assertTrue(player_is_in_match, 'Player was not in a match from the result')

    def test_request_match_detail_on_a_non_existent_match(self):
        request = self.executor(
            BASE_URL + GET_MATCH_DETAILS + request_pars(LANGUAGE_PAR, STEAM_ID_PAR, 'format=json', 'match_id=1'))

        self.assertEqual(request.status_code, 200)

        result = request.json()['result']
        self.assertEqual(result['error'], 'Match ID not found')

    def test_request_match_detail_with_no_match_id(self):
        request = self.executor(
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


def request_pars(*args):
    return '?' + '&'.join(args)