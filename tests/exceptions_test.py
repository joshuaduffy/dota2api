#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from dota2api.src import exceptions


class APIErrorTest(unittest.TestCase):
    def setUp(self):
        import dota2api
        self.api = dota2api.Initialise()

    def wrong_account_id(self):
        self.assertRaises(exceptions.APIError(), self.api.get_match_history(account_id=1))


class APIAuthenticationErrorTest(unittest.TestCase):
    def setUp(self):
        import dota2api
        self.api = dota2api.Initialise("d")

    def wrong_account_id(self):
        self.assertRaises(exceptions.APIAuthenticationError(), self.api.get_match_details())


class APITimeoutErrorTest(unittest.TestCase):
    def setUp(self):
        import dota2api
        self.api = dota2api.Initialise()

    def too_many_requests(self):
        assert True  # Can I do this?
