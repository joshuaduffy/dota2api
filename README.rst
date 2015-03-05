dota2api: wrapper and parser
============================

.. image:: https://travis-ci.org/joshuaduffy/dota2api.svg
    :target: https://travis-ci.org/joshuaduffy/dota2api
.. image:: https://readthedocs.org/projects/dota2api/badge/?version=latest
    :target: https://readthedocs.org/projects/dota2api/?badge=latest

Wrapper and parser in Python created for interacting and getting data easily from Valve's Dota 2 API.

This library parses some ID's into the dictionary keys like ``hero_name`` and so on. See ``src.parse`` for details.

This also comes with a growing set of tests and some documentation for the API itself.
 
Look how easy it is...

.. code-block:: python

    >>> import dota2api
    >>> api = dota2api.Initialise("API_KEY")
    >>> hist = api.get_match_history(account_id=41231571)
    >>> match = api.get_match_details(match_id=1000193456).dict
    >>> match['radiant_win']
    False

You can even store your API key as an environment variable instead of passing it through ``Initialise()`` to save some finger work.

.. code-block:: bash

    $  export D2_API_KEY=83247983248793298732

Supported API calls
-------------------
- get_match_history
- get_match_details
- get_player_summaries
- get_league_listing
- get_live_league_games
- get_team_info_by_team_id
- get_heroes
- get_tournament_prize_pool
- get_game_items

Unsupported
-----------
- EconomySchema
- GetMatchHistoryBySequenceNum


Documentation
-------------
Documentation is available at http://dota2api.readthedocs.org/

Install
-------

Install via pip...
.. code-block:: bash

    $ pip install dota2api


Or the old fashioned way...
.. code-block:: bash

    $ git clone https://github.com/joshuaduffy/dota2api.git
    $ cd dota2api
    $ python setup.py install
