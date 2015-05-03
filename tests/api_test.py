#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os
import json

from dota2api.api import *
from dota2api.src.exceptions import *
from utils import RequestMock
from dota2api.src.parse import *


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
