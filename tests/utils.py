import os
from dota2api.src.parse import load_json_file
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

    def configure_single_match_result(self):
        abs_dir = os.path.abspath(os.path.dirname(__file__))
        join = os.path.join(abs_dir, "ref", "get_match_details_result.json")
        with open(join) as match_json:
            self.json_result = json.load(match_json)
        return self

    def configure_get_match_history_result(self):
        abs_dir = os.path.abspath(os.path.dirname(__file__))
        join = os.path.join(abs_dir, "ref", "get_match_history_result.json")
        with open(join) as match_json:
            self.json_result = json.load(match_json)
        return self

    def configure_get_match_history_by_sequence_num_result(self):
        abs_dir = os.path.abspath(os.path.dirname(__file__))
        join = os.path.join(abs_dir, "ref", "get_match_history_by_sequence_num_result.json")
        with open(join) as match_json:
            self.json_result = json.load(match_json)
        return self

    def configure_get_league_listing_result(self):
        abs_dir = os.path.abspath(os.path.dirname(__file__))
        join = os.path.join(abs_dir, "ref", "get_league_listing_result.json")
        with open(join) as match_json:
            self.json_result = json.load(match_json)
        return self

    def configure_get_live_league_games_result(self):
        abs_dir = os.path.abspath(os.path.dirname(__file__))
        join = os.path.join(abs_dir, "ref", "get_live_league_games_result.json")
        with open(join) as match_json:
            self.json_result = json.load(match_json)
        return self

    def configure_get_team_info_by_team_id(self):
        abs_dir = os.path.abspath(os.path.dirname(__file__))
        join = os.path.join(abs_dir, "ref", "get_team_info_by_team_id_result.json")
        with open(join) as match_json:
            self.json_result = json.load(match_json)
        return self

    def __call__(self, url):
        print url
        if self.url_matcher:
            self.url_matcher.compare(url)
        self.called = True
        return self

    def assert_called(self):
        if not self.called:
            raise AssertionError("The url was not called")

    def configure_get_player_summaries(self):
        abs_dir = os.path.abspath(os.path.dirname(__file__))
        join = os.path.join(abs_dir, "ref", "get_player_summaries_result.json")
        with open(join) as match_json:
            self.json_result = json.load(match_json)
        return self

    def configure_get_heroes(self):
        abs_dir = os.path.abspath(os.path.dirname(__file__))
        join = os.path.join(abs_dir, "ref", "get_heroes_result.json")
        with open(join) as match_json:
            self.json_result = json.load(match_json)
        return self

    def configure_get_game_items(self):
        abs_dir = os.path.abspath(os.path.dirname(__file__))
        join = os.path.join(abs_dir, "ref", "get_game_items_result.json")
        with open(join) as match_json:
            self.json_result = json.load(match_json)
        return self

    def configure_get_tournament_prize_pool(self):
        abs_dir = os.path.abspath(os.path.dirname(__file__))
        join = os.path.join(abs_dir, "ref", "get_tournament_prize_pool_result.json")
        with open(join) as match_json:
            self.json_result = json.load(match_json)
        return self


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
