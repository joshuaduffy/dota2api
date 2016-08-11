dota2api: wrapper and parser
============================

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/joshuaduffy/dota2api
   :target: https://gitter.im/joshuaduffy/dota2api?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. image:: https://travis-ci.org/joshuaduffy/dota2api.svg
    :target: https://travis-ci.org/joshuaduffy/dota2api
.. image:: https://readthedocs.org/projects/dota2api/badge/?version=latest
    :target: https://readthedocs.org/projects/dota2api/?badge=latest

Wrapper and parser in Python created for interacting and getting data easily from Valve's Dota 2 API. It supports Python versions ``2.6 to 2.7+``, ``3.2 to 3.5+`` along with ``PyPy/PyPy3``

This library parses some ID's into the dictionary keys like ``hero_name`` and so on. See ``src.parse`` for details.

This also comes with a growing set of tests and some documentation for the API itself.

Look how easy it is...

.. code-block:: python

    >>> import dota2api
    >>> api = dota2api.Initialise("API_KEY")
    >>> hist = api.get_match_history(account_id=41231571)
    >>> match = api.get_match_details(match_id=1000193456)
    >>> match['radiant_win']
    False

You can even store your API key as an environment variable instead of passing it through ``Initialise()`` to save some finger work.

.. code-block:: bash

    $  export D2_API_KEY=83247983248793298732


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


Documentation
-------------
Documentation is available at http://dota2api.readthedocs.org/


Supported API calls
-------------------
- get_match_history
- get_match_history_by_seq_num
- get_match_details
- get_player_summaries
- get_league_listing
- get_live_league_games
- get_team_info_by_team_id
- get_heroes
- get_tournament_prize_pool
- get_game_items
- get_top_live_games


Unsupported
-----------
- EconomySchema

Run the tests
-------------

Using nose and nose-cov:

.. code-block:: bash

    $ nosetests --with-cov --cov-report html dota2api tests

To install them do the following:

.. code-block:: bash

    $ pip install nose nose-cov
