
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
        self.executor.configure_get_match_history_by_sequence_num_result()
        history = self.api.get_match_history_by_seq_num()

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