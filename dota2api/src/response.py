#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Response template, this is used so we can pass the response as an object"""

import parse


class Dota2Dict(dict):
    pass


def build(req, url):
    req_resp = req.json()
    if 'result' in req_resp:
        resp = Dota2Dict(req_resp['result'])
    elif 'response' in req_resp:
        resp = Dota2Dict(req_resp['response'])
    else:
        resp = Dota2Dict(req_resp)
    try:
        if 'players' in resp:
            resp = parse.hero_id(resp)
            resp = parse.item_id(resp)
            resp = parse.lobby_type(resp)
            resp = parse.game_mode(resp)
            resp = parse.cluster(resp)
    except KeyError:
        pass

    resp.url = url

    return resp