"""Response template, this is used so we can pass the response as an object"""

import parse

class Dota2Response(object):
    """Generic response"""
    def __init__(self, response, url):
        self.url = url
        self.resp = response

class Dota2MatchDetails(object):
    """Match details"""
    def __init__(self, response, url):
        self.url = url
        self.resp = response
        if 'players' in self.resp:
            self.resp = parse.hero_id(self.resp)
            self.resp = parse.item_id(self.resp)