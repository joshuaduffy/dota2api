#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os
import json

import dota2api
from dota2api.src.response import Dota2Dict
from dota2api.src.exceptions import *
from utils import RequestMock


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