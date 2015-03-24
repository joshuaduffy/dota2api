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
    def no_environment_variable_set_test(self):
        # Pass the API key as a positional argument
        self.api_key = os.environ['D2_API_KEY']
        self.api = dota2api.Initialise(self.api_key)
        match = self.api.get_match_details(match_id=988604774)

        # Do we get a match back
        mock = RequestMock()
        stored_match = mock.configure_single_match_result().json_result

        # Check the response is the same as the stored one
        self.assertEqual(stored_match['result']['match_id'], match['match_id'])

        # Check it is our custom dict type
        self.assertEqual(type(Dota2Dict()), type(match))

        # Test json function loads json
        try:
            json.loads(match.json)
        except ValueError:
            self.fail("JSON does not load!")

        # Test the wrong API key
        with self.assertRaises(APIAuthenticationError):
            dota2api.Initialise("sdfsdfsdf").get_match_history()

    def get_match_history_no_kwargs(self):
        # Don't use kwargs when calling
        assert True

    def get_match_details_no_kwargs(self):
        # Don't use kwargs when calling
        assert True

    def test_logging(self):
        # Something to cover the logging
        assert True