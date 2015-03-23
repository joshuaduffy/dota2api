import unittest
from dota2api.src.urls import *
from tests.utils import *
from dota2api.src import response
from dota2api.src.exceptions import *
import requests


class TestBuildDota2Dict(unittest.TestCase):
    def setUp(self):
        self.executor = requests.get

    def test_get_match_history_with_no_param(self):
        url = BASE_URL + GET_MATCH_HISTORY + request_pars(LANGUAGE_PAR, 'account_id=None', STEAM_ID_PAR,
                                                          'format=json')
        request = self.executor(url)

        self.assertEqual(request.status_code, 200)

        dota2dict = response.build(request, url)

        self.assertEqual(len(dota2dict), 5)
        self.assertEqual(len(dota2dict['matches']), DEFAULT_MATCHES_SIZE)

    def test_get_match_history_with_limited_matches(self):
        url = BASE_URL + GET_MATCH_HISTORY + request_pars(LANGUAGE_PAR, 'account_id=None', STEAM_ID_PAR,
                                                          'format=json', 'matches_requested=1')
        request = self.executor(url)

        self.assertEqual(request.status_code, 200)
        dota2dict = response.build(request, url)
        self.assertEqual(len(dota2dict['matches']), 1)

    def test_get_match_history_from_only_one_player(self):
        url = BASE_URL + GET_MATCH_HISTORY + request_pars(LANGUAGE_PAR, 'account_id=88585077', STEAM_ID_PAR,
                                                          'format=json', 'matches_requested=10')
        request = self.executor(url)

        self.assertEqual(request.status_code, 200)

        dota2dict = response.build(request, url)

        self.assertEqual(len(dota2dict['matches']), 10)
        for match in dota2dict['matches']:
            player_is_in_match = bool([p for p in match['players'] if p['account_id'] == 88585077])
            self.assertTrue(player_is_in_match, 'Player was not in a match from the result')

    def test_request_match_detail_on_a_non_existent_match(self):
        url = BASE_URL + GET_MATCH_DETAILS + request_pars(LANGUAGE_PAR, STEAM_ID_PAR, 'format=json', 'match_id=1')
        request = self.executor(url)

        self.assertEqual(request.status_code, 200)
        self.assertRaises(APIError, response.build, request, url)

    def test_request_match_detail_with_no_match_id(self):
        url = BASE_URL + GET_MATCH_DETAILS + request_pars(LANGUAGE_PAR, STEAM_ID_PAR, 'format=json', 'match_id=None')
        request = self.executor(url)

        self.assertEqual(request.status_code, 200)
        self.assertRaises(APIError, response.build, request, url)

    def test_parse_hero_names_in_response(self):
        build = response.build(RequestMock().configure_single_match_result(), 'SomeUrl')

        self.assertEqual(build['players'][0]['hero_name'], "Nature's Prophet")
        self.assertEqual(build['players'][1]['hero_name'], "Naga Siren")
        self.assertEqual(build['players'][2]['hero_name'], "Death Prophet")
        self.assertEqual(build['players'][3]['hero_name'], "Weaver")
        self.assertEqual(build['players'][4]['hero_name'], "Undying")
        self.assertEqual(build['players'][5]['hero_name'], "Ember Spirit")
        self.assertEqual(build['players'][6]['hero_name'], "Pudge")
        self.assertEqual(build['players'][7]['hero_name'], "Meepo")
        self.assertEqual(build['players'][8]['hero_name'], "Lich")
        self.assertEqual(build['players'][9]['hero_name'], "Kunkka")

    def test_parse_items_names_in_response(self):
        build = response.build(RequestMock().configure_single_match_result(), 'SomeUrl')

        self.assertEqual(build['players'][0]['item_0_name'], "Phase Boots")
        self.assertEqual(build['players'][0]['item_1_name'], "Invis Sword") #invis sword? rip Lothar's Edge :D
        self.assertEqual(build['players'][0]['item_2_name'], "Dagon 5")
        self.assertEqual(build['players'][0]['item_3_name'], "Hand Of Midas")
        self.assertEqual(build['players'][0]['item_4_name'], "Tp Scroll")
        self.assertEqual(build['players'][0]['item_5_name'], "Empty")

    def test_parse_lobby_name_in_response(self):
        build = response.build(RequestMock().configure_single_match_result(), 'SomeUrl')

        self.assertEqual(build['lobby_name'], "Public matchmaking")

    def test_parse_lobby_name_in_response(self):
        build = response.build(RequestMock().configure_single_match_result(), 'SomeUrl')

        self.assertEqual(build['game_mode_name'], "All pick")

    def test_parse_lobby_name_in_response(self):
        build = response.build(RequestMock().configure_single_match_result(), 'SomeUrl')

        self.assertEqual(build['cluster_name'], "Europe West")
