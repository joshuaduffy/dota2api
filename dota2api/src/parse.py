import json
import os
import itertools


def hero_id(response):
    """Parse the hero id"""
    for player in response['players']:
        for hero in heroes['heroes']:
            if hero['id'] == player['hero_id']:
                player[u'hero_name'] = hero['localized_name']

    return response


def item_id(response):
    """Parse the item ids"""
    dict_keys = ['item_0', 'item_1', 'item_2',
                 'item_3', 'item_4', 'item_5']
    new_keys = ['item_0_name', 'item_1_name', 'item_2_name',
                'item_3_name', 'item_4_name', 'item_5_name']

    for player in response['players']:
        for key, newkey in itertools.izip(dict_keys, new_keys):
            for item in items['items']:
                if item['id'] == player[key]:
                    player[unicode(newkey)] = item['name'].replace('_',
                                                                   ' ').title()

    return response


def game_mode(response):
    """Parse the game mode"""
    for mode in modes['modes']:
        if mode['id'] == response['game_mode']:
            response[u'game_mode_name'] = mode['name']

    return response


def load_json_file(file_name):
    """Load the static data"""
    inp_file = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..",
                                                    "ref",
                                                    file_name))
    return inp_file
    
# Load the files into memory as a dict
with open(load_json_file("heroes.json")) as heroes_json:
    heroes = json.load(heroes_json)
with open(load_json_file("items.json")) as items_json:
    items = json.load(items_json)
with open(load_json_file("lobbies.json")) as lobbies_json:
    lobbies = json.load(lobbies_json)
with open(load_json_file("modes.json")) as modes_json:
    modes = json.load(modes_json)
with open(load_json_file("regions.json")) as regions_json:
    regions = json.load(regions_json)