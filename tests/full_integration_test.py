
from unittest import TestCase
import dota2api
import utils
from dota2api.src.urls import *


class APITest(TestCase):
    def setUp(self):
        self.executor = utils.RequestMock()
        self.api = dota2api.Initialise(executor=self.executor)

    def test_get_match_history_test(self):
        matcher = utils.UrlMatcher(BASE_URL + GET_MATCH_HISTORY,
                     utils.LANGUAGE_PAR,
                     'account_id=None',
                     utils.STEAM_ID_PAR,
                     'format=json')
        self.executor.url_matcher = matcher
        self.executor.configure_get_match_history_result()

        history = self.api.get_match_history()

        self.api.executor.assert_called()
        
        self.assertEqual(history.num_results, 10)
        self.assertEqual(history.total_results, 500)
        self.assertEqual(history.results_remaining, 490)
        self.assertEqual(len(history.matches), 10)

        self.assertEqual(history.matches[0].match_id, 1356101552)
        self.assertEqual(history.matches[0].match_seq_num, 1216063230)
        self.assertEqual(history.matches[0].start_time, 1427552454)
        self.assertEqual(history.matches[0].lobby_type, 7)
        self.assertEqual(history.matches[0].lobby_name, 'Ranked')
        self.assertEqual(history.matches[0].radiant_team_id, 0)
        self.assertEqual(history.matches[0].dire_team_id, 0)

        self.assertEqual(history.matches[0].players[0].account_id, 140250400)
        self.assertEqual(history.matches[0].players[0].hero_id, 22)
        self.assertEqual(history.matches[0].players[0].hero_name, 'Zeus')

    def test_get_match_history_by_sequence_num(self):
        matcher = utils.UrlMatcher(BASE_URL + GET_MATCH_HISTORY_BY_SEQ_NUM,
                     utils.LANGUAGE_PAR,
                     'start_at_match_seq_num=None',
                     utils.STEAM_ID_PAR,
                     'format=json')

        self.executor.url_matcher = matcher
        self.executor.configure_get_match_history_by_sequence_num_result()

        history = self.api.get_match_history_by_seq_num()

        self.executor.assert_called()

        self.assertEqual(len(history.matches), 100)

        self.assertEqual(history.matches[0].match_id, 496)
        self.assertEqual(history.matches[0].match_seq_num, 240)
        self.assertEqual(history.matches[0].start_time, 1299121489)
        self.assertEqual(history.matches[0].lobby_type, 0)
        self.assertEqual(history.matches[0].lobby_name, 'Public matchmaking')
        self.assertEqual(history.matches[0].radiant_team_id, None)
        self.assertEqual(history.matches[0].dire_team_id, None)

        self.assertEqual(history.matches[0].players[0].account_id, 4294967295)
        self.assertEqual(history.matches[0].players[0].hero_id, 18)
        self.assertEqual(history.matches[0].players[0].hero_name, 'Sven')

    def test_get_match_details(self):
        matcher = utils.UrlMatcher(BASE_URL + GET_MATCH_DETAILS,
                     utils.LANGUAGE_PAR,
                     'match_id=123',
                     utils.STEAM_ID_PAR,
                     'format=json')

        self.executor.url_matcher = matcher
        self.executor.configure_single_match_result()

        history = self.api.get_match_details(123)

        self.executor.assert_called()

        self.assertEqual(history.players[0].hero_name, "Nature's Prophet")
        self.assertEqual(history.players[1].hero_name, "Naga Siren")
        self.assertEqual(history.players[2].hero_name, "Death Prophet")
        self.assertEqual(history.players[3].hero_name, "Weaver")
        self.assertEqual(history.players[4].hero_name, "Undying")
        self.assertEqual(history.players[5].hero_name, "Ember Spirit")
        self.assertEqual(history.players[6].hero_name, "Pudge")
        self.assertEqual(history.players[7].hero_name, "Meepo")
        self.assertEqual(history.players[8].hero_name, "Lich")
        self.assertEqual(history.players[9].hero_name, "Kunkka")

        self.assertEqual(history.players[0].items[0], (50, 'Phase Boots'))
        self.assertEqual(history.players[0].items[1], (152, 'Shadow Blade'))
        self.assertEqual(history.players[0].items[2], (204, 'Dagon'))
        self.assertEqual(history.players[0].items[3], (65, 'Hand of Midas'))
        self.assertEqual(history.players[0].items[4], (46, 'Town Portal Scroll'))
        self.assertEqual(history.players[0].items[5], (0, ''))

        self.assertEqual(history.lobby_name, u"Public matchmaking")

        self.assertEqual(history.game_mode_name, u"All Pick")

        self.assertEqual(history.cluster_name, "Europe West")

    def test_get_league_listing(self):
        matcher = utils.UrlMatcher(BASE_URL + GET_LEAGUE_LISTING,
                     utils.LANGUAGE_PAR,
                     utils.STEAM_ID_PAR,
                     'format=json')

        self.executor.url_matcher = matcher
        self.executor.configure_get_league_listing_result()

        history = self.api.get_league_listing()

        self.executor.assert_called()

        self.assertEqual(len(history), 931)

        self.assertEqual(history[0].leagueid, 1212)
        self.assertEqual(history[0].name, 'Dota 2 Just For Fun')
        self.assertEqual(history[0].tournament_url, 'https://binarybeast.com/xDOTA21404228/')
        self.assertEqual(history[0].description, '64 of the best Brazilian amateur teams compete to become the winner of the first Dota 2 Just For Fun tournament. ')
        self.assertEqual(history[0].itemdef, 10541)

    def test_get_live_league_games(self):
        matcher = utils.UrlMatcher(BASE_URL + GET_LIVE_LEAGUE_GAMES,
                     utils.LANGUAGE_PAR,
                     utils.STEAM_ID_PAR,
                     'format=json')

        self.executor.url_matcher = matcher
        self.executor.configure_get_live_league_games_result()

        history = self.api.get_live_league_games()

        self.executor.assert_called()

        self.assertEqual(len(history), 5)
        self.assertEqual(history[0].radiant_team.team_name, 'Stroy Bat')
        self.assertEqual(history[0].radiant_team.team_id, 1734383)
        self.assertEqual(history[0].radiant_team.team_logo, 46500877983858209)
        self.assertEqual(history[0].radiant_team.complete, False)

        self.assertEqual(history[0].scoreboard.roshan_respawn_timer, 0)
        self.assertEqual(history[0].scoreboard.duration, 2335.81787109375)

        self.assertEqual(history[0].scoreboard.radiant.picks[0][0], 95)
        self.assertEqual(history[0].scoreboard.radiant.picks[0][1], 'Troll Warlord')

        self.assertEqual(history[0].scoreboard.radiant.bans[0][0], 17)
        self.assertEqual(history[0].scoreboard.radiant.bans[0][1], 'Storm Spirit')

        self.assertEqual(history[0].scoreboard.radiant.players[0].player_slot, 1)
        self.assertEqual(history[0].scoreboard.radiant.players[0].items[0], (0, ''))
        self.assertEqual(history[0].scoreboard.radiant.players[0].items[1], (60, 'Point Booster'))
        self.assertEqual(history[0].scoreboard.radiant.players[0].items[2], (46, 'Town Portal Scroll'))

        self.assertEqual(history[0].scoreboard.radiant.players[0].respawn_timer, 0)
        self.assertEqual(history[0].scoreboard.radiant.players[0].net_worth, 7166)

        self.assertEqual(history[0].scoreboard.radiant.players[0].respawn_timer, 0)

