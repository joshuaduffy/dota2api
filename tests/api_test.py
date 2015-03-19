#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os

import dota2api
from dota2api.src.response import Dota2Dict
from dota2api.src.exceptions import *


class APITest(unittest.TestCase):
    def no_environment_variable_set(self):
        # Pass the API key as a positional argument
        self.api_key = os.environ['D2_API_KEY']
        # Remove API key from env
        del os.environ['D2_API_KEY']
        self.api = dota2api.Initialise(self.api_key)
        match = self.api.get_match_details(match_id=988604774)
        self.assertEqual(type(Dota2Dict), match)
        self.assertRaises(APIAuthenticationError(), dota2api.Initialise())
        # Put the key back
        os.environ['D2_API_KEY'] = str(self.api_key)

    def get_match_history_no_kwargs(self):
        # Don't use kwargs when calling
        assert True

    def get_match_details_no_kwargs(self):
        # Don't use kwargs when calling
        assert True

    def test_logging(self):
        # Something to cover the logging
        assert True