import os
import json
DEFAULT_MATCHES_SIZE = 100
LANGUAGE_PAR = 'language=en_us'
STEAM_ID_PAR = 'key=' + os.environ.get('D2_API_KEY')


def convert_to_64_bit(number):
    # Yes we should put this in the API - will be used to parse steam names
    return number + 76561197960265728


def request_pars(*args):
    return '?' + '&'.join(args)


class RequestMock(object):
    def __init__(self, url_matcher=None):
        self.status_code = 666
        self.url_matcher = url_matcher
        self.called = False
        self.json_result = None

    def configure_success(self):
        self.status_code = 200
        return self

    def configure_authentication_error(self):
        self.status_code = 403
        return self

    def configure_timeout_error(self):
        self.status_code = 503
        return self

    def json(self):
        if self.json_result:
            return self.json_result
        return {'result': {}}

    def __call__(self, url):
        if self.url_matcher:
            self.url_matcher.compare(url)
        self.called = True
        return self

    def assert_called(self):
        if not self.called:
            raise AssertionError("The url was not called")

    def configure_single_match_result(self):
        self._load_json_file("get_match_details_result.json")

    def configure_get_match_history_result(self):
        self._load_json_file("get_match_history_result.json")

    def configure_get_match_history_by_sequence_num_result(self):
        self._load_json_file("get_match_history_by_sequence_num_result.json")

    def configure_get_league_listing_result(self):
        self._load_json_file("get_league_listing_result.json")

    def configure_get_live_league_games_result(self):
        self._load_json_file("get_live_league_games_result.json")

    def configure_get_team_info_by_team_id(self):
        self._load_json_file("get_team_info_by_team_id_result.json")


    def configure_get_player_summaries(self):
        self._load_json_file("get_player_summaries_result.json")

    def configure_get_heroes(self):
        self._load_json_file("get_heroes_result.json")

    def configure_get_game_items(self):
        self._load_json_file("get_game_items_result.json")

    def configure_get_tournament_prize_pool(self):
        self._load_json_file("get_tournament_prize_pool_result.json")

    def _load_json_file(self, json_file_name):
        abs_dir = os.path.abspath(os.path.dirname(__file__))
        join = os.path.join(abs_dir, "ref", json_file_name)
        with open(join) as match_json:
            self.json_result = json.load(match_json)


class UrlMatcher(object):
    def __init__(self, base_url, *args):
        self.args = args
        self.base_url = base_url

    def compare(self, url):
        if type(url) != str:
            raise AssertionError(str(url) + ' should be a string')

        if not url.startswith(self.base_url):
            raise AssertionError(url + ' does not start with ' + self.base_url)

        all_args = str(url).split('?')[1]
        splitted_args = all_args.split("&")

        for arg in self.args:
            if arg in splitted_args:
                splitted_args.remove(arg)
            else:
                raise AssertionError('The parameter ' + arg + ' is not in the url ' + url)

        if splitted_args:
            raise AssertionError("Args left: " + str(splitted_args))
        return True
