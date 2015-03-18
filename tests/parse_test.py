#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Some tests using multiple calls in proper ways"""

import unittest
import os

import dota2api


class ParseTests(unittest.TestCase):
    """Tests relating to the other tests."""
    def setUp(self):
        """Set up test fixtures"""
        self.api_test = dota2api.Initialise(os.environ['D2_API_KEY'])

    def parse_test(self):
        """Do the same as in the UserTest"""
        result = self.api_test.get_match_history(player_id=41231571, matches_requested=10).dict
        # Do we default at 10 responses
        self.assertEquals(len(result['matches']), 10)
        # Can we get each match
        for match in result['matches']:
            self.assertEqual(type(self.api_test.get_match_details(match_id=match['match_id']).dict), type(dict()))
        # Now test the parser