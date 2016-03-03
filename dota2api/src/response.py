#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Response template, this is used so we can pass the response as an object"""

import json
from .parse import *
from .exceptions import *


class Dota2Dict(dict):
    pass


def build(req, url):
    req_resp = req.json()
    if 'result' in req_resp:
        if 'error' in req_resp['result']:
            raise APIError(req_resp['result']['error'])
        if 'status' in req_resp['result']:
            if not (1 == req_resp['result']['status'] == 200):
                try:
                    raise APIError(req_resp['result']['statusDetail'])
                except KeyError:
                    pass
        resp = Dota2Dict(req_resp['result'])
    elif 'response' in req_resp:
        resp = Dota2Dict(req_resp['response'])
    else:
        resp = Dota2Dict(req_resp)

    try:
        if 'players' in resp:
            resp = hero_id(resp)
            resp = item_id(resp)
            resp = lobby_type(resp)
            resp = game_mode(resp)
            resp = cluster(resp)
    except KeyError:
        pass  # Only do the above for matches

    resp.url = url
    resp.json = json.dumps(resp, ensure_ascii=False)

    return resp