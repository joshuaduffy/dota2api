import json

import os

DEFAULT_MATCHES_SIZE = 100
LANGUAGE_PAR = 'language=en_us'
STEAM_ID_PAR = 'key=' + os.environ.get('D2_API_KEY')


def convert_to_64_bit(number):
    min64b = 76561197960265728
    if number < min64b:
        return number + min64b
    return number


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
        join = os.path.join(abs_dir, "ref", "single_match_result.json")
        with open(join) as match_json:
            self.json_result = json.load(match_json)
        return self

    def __call__(self, url):
        if self.url_matcher:
            self.url_matcher.compare(url)
        self.called = True
        return self

    def assert_called(self):
        if not self.called:
            raise AssertionError("The url was not called")


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
        split_args = all_args.split("&")

        for arg in self.args:
            if arg in split_args:
                split_args.remove(arg)
            else:
                raise AssertionError('The parameter ' + arg + ' is not in the url ' + url)

        if split_args:
            raise AssertionError("Args left: " + str(split_args))
        return True
