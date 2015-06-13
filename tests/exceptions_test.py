#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from dota2api.src import exceptions
from dota2api.api import *

class APIErrorTest(unittest.TestCase):
    def setUp(self):
        self.api = Initialise()

    def wrong_account_id(self):
        self.assertRaises(exceptions.APIError(), self.api.get_match_history(account_id=1))


class APIAuthenticationErrorTest(unittest.TestCase):
    def setUp(self):
        self.api = Initialise("d")

    def wrong_account_id(self):
        self.assertRaises(exceptions.APIAuthenticationError(), self.api.get_match_details())


class APITimeoutErrorTest(unittest.TestCase):
    def setUp(self):
        self.api = Initialise()
        self.assertTrue()

    def too_many_requests(self):
        assert True  #Actually you can, but I think that in test cases you should use the instance method,
        #since it gives you more information and you can put a message of what is your intent with that assert
