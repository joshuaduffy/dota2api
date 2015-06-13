#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from dota2api.api import *
from dota2api.src.exceptions import *
from utils import *
from dota2api.src.urls import *


class APITest(unittest.TestCase):
    def setUp(self):
        self.api = Initialise()

    def test_no_environment_variable_set_test(self):
        api = Initialise("SOME KEY")
        self.assertEqual(api.api_key, "SOME KEY")



    def test_json_loads_test(self):
            # Test json function loads json
            match = self.api.get_match_details(match_id=988604774)
            try:
                json.loads(match.json)
            except ValueError:
                self.fail("JSON does not load!")

    def test_wrong_api_key_test(self):
            # Test the wrong API key
            try:
                Initialise("sdfsdfsdf").get_match_history()
            except APIAuthenticationError:
                assert True

    def test_update_heroes_test(self):
        self.api.update_heroes()
        try:
            self.api.get_match_details(988604774)
        except:
            self.fail("JSON Heroes update failed!")

    def test_update_game_items_test(self):
        self.api.update_game_items()
        try:
            self.api.get_match_details(988604774)
        except:
            self.fail("JSON Items update failed!")

    def test_should_convert_steam_id_to_64b_if_it_is_not_in_that_base(self):
        mock = RequestMock()
        mock.url_matcher = UrlMatcher(BASE_URL + GET_PLAYER_SUMMARIES,
                                   LANGUAGE_PAR,
                                   STEAM_ID_PAR,
                                   'format=json',
                                   'steamids=%5B76561198049003839%5D')
        mock.configure_get_player_summaries()
        self.api.executor = mock

        self.api.get_player_summaries(88738111)
        mock.assert_called()

    def test_should_construct_correctly_url_with_list_parameter_on_player_summary(self):
        mock = RequestMock()
        mock.url_matcher = UrlMatcher(BASE_URL + GET_PLAYER_SUMMARIES,
                                   LANGUAGE_PAR,
                                   STEAM_ID_PAR,
                                   'format=json',
                                    'steamids=%5B76561198049003839%2C+76561198049490285%2C+76561197982571868%5D')
        mock.configure_get_player_summaries()
        self.api.executor = mock

        self.api.get_player_summaries(88738111, 89224557, 22306140)
        mock.assert_called()