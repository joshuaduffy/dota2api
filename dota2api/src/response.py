"""Response template, this is used so we can pass the response as an object"""

import parse

class Dota2Response(object):
    """Generic response"""
    def __init__(self, response, url):
        self.url = url
        self.dict = response

    def __repr__(self):
        return str(self.dict)

class Dota2MatchDetails(object):
    """Match details"""
    def __init__(self, response, url):
        self.url = url
        self.dict = response
        if 'players' in self.dict:
            self.dict = parse.hero_id(self.dict)
            self.dict = parse.item_id(self.dict)
            self.dict = parse.game_mode(self.dict)

    def __repr__(self):
        return str(self.dict)