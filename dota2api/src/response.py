#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Response template, this is used so we can pass the response as an object"""

import json
import parse
from exceptions import *

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
        resp = req_resp['result']
    elif 'response' in req_resp:
        resp = req_resp['response']
    else:
        resp = req_resp

    parsed = parse.parse_result(resp)
    parsed.url = url
    parsed.json = json.dumps(resp, ensure_ascii=False)

    return parsed
