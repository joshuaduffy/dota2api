#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest

import os

import dota2api
from dota2api.src.exceptions import *
from dota2api.src.response import Dota2Dict
from .utils import RequestMock


class APITest(unittest.TestCase):
    def setUp(self):
        self.api = dota2api.Initialise()

    def no_environment_variable_set_test(self):
        # Pass the API key as a positional argument
        self.api_key = os.environ['D2_API_KEY']
        api = dota2api.Initialise(self.api_key)
        match = api.get_match_details(match_id=988604774)
        # Do we get a match back
        mock = RequestMock()
        stored_match = mock.configure_single_match_result().json_result
        # Check the response is the same as the stored one
        self.assertEqual(stored_match['result']['match_id'], match['match_id'])
        # Check it is our custom dict type
        self.assertEqual(type(Dota2Dict()), type(match))

    def json_loads_test(self):
        # Test json function loads json
        match = self.api.get_match_details(match_id=988604774)
        try:
            json.loads(match.json)
        except ValueError:
            self.fail("JSON does not load!")

    def wrong_api_key_test(self):
        # Test the wrong API key
        try:
            dota2api.Initialise("sdfsdfsdf").get_match_history()
        except APIAuthenticationError:
            assert True

    def update_heroes_test(self):
        self.api.update_heroes()
        try:
            self.api.get_match_details(988604774)
        except:
            self.fail("JSON Heroes update failed!")

    def update_game_items_test(self):
        self.api.update_game_items()
        try:
            self.api.get_match_details(988604774)
        except:
            self.fail("JSON Items update failed!")

    def test_parse_heroes_urls(self):
        heroes = self.api.get_heroes()

        try:
            anti_mage = filter(lambda h: h['name'] == 'npc_dota_hero_antimage', heroes['heroes'])[0]
            self.assertEqual('http://cdn.dota2.com/apps/dota2/images/heroes/antimage_full.png', anti_mage['url_full_portrait'])
            self.assertEqual('http://cdn.dota2.com/apps/dota2/images/heroes/antimage_sb.png', anti_mage['url_small_portrait'])
            self.assertEqual('http://cdn.dota2.com/apps/dota2/images/heroes/antimage_lg.png', anti_mage['url_large_portrait'])
            self.assertEqual('http://cdn.dota2.com/apps/dota2/images/heroes/antimage_vert.jpg', anti_mage['url_vertical_portrait'])

        except TypeError:
            anti_mage = filter(lambda h: h['name'] == 'npc_dota_hero_antimage', heroes['heroes'])



    def test_parse_items_urls(self):
        items = self.api.get_game_items()

        try:
            blink_dagger = filter(lambda i: i['name'] == 'item_blink', items['items'])[0]
            self.assertEqual('http://cdn.dota2.com/apps/dota2/images/items/blink_lg.png', blink_dagger['url_image'])

        except TypeError:
            blink_dagger = filter(lambda i: i['name'] == 'item_blink', items['items'])

