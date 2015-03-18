#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest

from dota2api.src.urls import *

DEFAULT_MATCHES_SIZE = 100
LANGUAGE_PAR = 'language=en_us'
STEAM_ID_PAR = 'key=' + os.environ.get('D2_API_KEY')


def convert_to_64_bit(number):
    # Yes we should put this in the API - will be used to parse steam names
    return number + 76561197960265728


class RequestMock(object):

    def __init__(self):
        self.status_code = 666

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


class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def test_one(self):
        assert True


def request_pars(*args):
    return '?' + '&'.join(args)
