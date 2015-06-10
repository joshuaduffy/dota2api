#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Parse some of the values from the API, all can be found in the ``response`` returned"""


from exceptions import APIError
from ..obj.detail import DetailMatch
from ..obj.league import LeagueListing, LiveLeagueGames, TournamentPrizePool, Teams
from ..obj.history import HistoryMatches
from ..obj.player import PlayerSummaries
from ..obj.hero import Heroes
from ..obj.item import Items

def parse_result(result):
    if 'match_id' in result and 'radiant_win' in result:
        return DetailMatch(**result)

    if 'matches' in result:
        return HistoryMatches(**result)

    if 'leagues' in result:
        return LeagueListing(**result)

    if 'games' in result:
        return LiveLeagueGames(**result)

    if 'teams' in result:
        return Teams(**result)

    if 'players' in result:
        return PlayerSummaries(**result)

    if 'heroes' in result:
        return Heroes(**result)

    if 'items' in result:
        return Items(**result)

    if 'prize_pool' in result:
        return TournamentPrizePool(**result)

    raise APIError("There are no parser available for the result")
