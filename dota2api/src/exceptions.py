#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Not many exceptions exist due to server side validation on the parameters"""


class BaseError(Exception):
    """
    Base error used
    """
    pass


class APIAuthenticationError(BaseError):
    """
    Raised when the API key supplied is invalid

    :param api_key: (str) key used will be displayed upon error
    """
    def __init__(self, api_key=None):
        self.msg = "The following API Key is invalid: {0}".format(api_key)

    def __str__(self):
        return repr(self.msg)


class APITimeoutError(BaseError):
    """
    Raised when too many requests are been made or the server is busy
    """
    def __init__(self,):
        self.msg = "HTTP 503: Please try again later."

    def __str__(self):
        return repr(self.msg)