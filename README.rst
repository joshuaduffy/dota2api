dota2api: wrapper and parser
============================
.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/joshuaduffy/dota2api
   :target: https://gitter.im/joshuaduffy/dota2api?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

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
    >>> match = api.get_match_details(match_id=1000193456)
    >>> match.is_radiant_win
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
All responses have 3 default attributes:
- url: the URL constructed by the api
- json: the JSON dictionary returned from request
- resp: the response returned from request
 
**get_match_history(account_id, ** kwargs):**

:optionals: hero_id, game_mode, skill, date_min, date_max, min_players, league_id, start_at_match_id, matches_requested, tournament_games_only
:returns: HistoryMatches

   - num_results
   - total_results
   - results_remaining
   - matches: list[HistoryMatch]
      - match_id
      - match_seq_num
      - start_time
      - lobby_type
      - lobby_name
      - radiant_team_id
      - dire_team_id
      - players: list[HistoryPlayer]
         - account_id
         - player_slot
         - hero: Hero object

**get_match_history_by_seq_num(start_at_match_seq_num,  **kwargs):**

:optionals: start_at_match_seq_num, matches_requested
:returns: list[HistoryMatch]

** get_match_details(match_id, ** kwargs):**

:returns: DetailMatch

  - is_radiant_win
  - duration
  - start_time
  - match_id
  - match_seq_num
  - tower_status_radiant
  - tower_status_dire
  - barracks_status_radiant
  - barracks_status_dire
  - cluster
  - cluster_name
  - first_blood_time
  - lobby_type
  - lobby_name
  - human_players
  - league_id
  - positive_votes
  - negative_votes
  - game_mode
  - game_mode_name
  - players: list[DetailMatchPlayer]

    - account_id
    - player_slot
    - hero: Hero
    - kills
    - deaths
    - assists
    - leaver_status: LeaverStatus

      - id
      - name
      - description
    - gold
    - last_hits
    - denies
    - gold_per_min
    - xp_per_min
    - gold_spent
    - hero_damage
    - tower_damage
    - hero_healing
    - level
    - items: list[Item]
    - ability_upgrades: list[AbilityUpgrade]

      - ability
      - ability_name
      - time
      - level
    - additional_units: list[AdditionalUnit]

      - unit_name
      - items: list of Item's

**get_player_summaries(*steamids, **kwargs):**

You can use this method with 32b numbers (same value of account_id returned from the other calls).
The api will take care to convert those to 64b base.

:returns: list[PlayerSummary]

    - steam_id
    - community_visibility_state
    - profile_state
    - persona_name
    - last_logoff
    - profile_url
    - url_avatar
    - url_avatar_medium
    - url_avatar_full
    - persona_state
    - primary_clan_id
    - time_created
    - persona_state_flags


**get_league_listing()**

:returns: list[League]

    - league_id
    - name
    - tournament_url
    - description
    - itemdef

**get_live_league_games()**

:returns: list[LiveLeagueGame]
    - radiant_team: LiveLeagueGameTeam
        - team_name
        - team_id
        - team_logo
        - complete
    - dire_team: LiveLeagueGameTeam
    - lobby_id
    - match_id
    - spectators
    - league_id
    - stream_delay_s
    - radiant_series_wins
    - dire_series_wins
    - series_type
    - league_tier
    - scoreboard: LiveLeagueGameScoreboard
        - duration
        - roshan_respawn_timer
        - radiant: LiveLeagueGameTeamScoreboard
        - score
        - tower_state
        - barracks_state
        - picks: list[Hero]
        - bans: list[Hero]
        - players: list[LiveLeagueGamePlayer]
            - account_id
            - player_slot
            - hero: Hero
            - kills
            - deaths
            - assists
            - leaver_status: LeaverStatus
            - gold
            - last_hits
            - denies
            - gold_per_min
            - xp_per_min
            - gold_spent
            - hero_damage
            - tower_damage
            - hero_healing
            - level
            - ultimate_state
            - ultimate_cooldown
            - respawn_timer
            - position_x
            - position_y
            - net_worth
            - the api can't parse the abilities yet :(
        - dire: list of LiveLeagueGamePlayer


**get_team_info_by_team_id()**

:optionals: start_at_team_id, teams_requested
:return: list[Team]

    - team_id
    - name
    - tag
    - time_created
    - rating
    - logo
    - logo_sponsor
    - country_code
    - url
    - games_played_with_current_roster
    - player_0_account_id
    - player_1_account_id
    - player_2_account_id
    - player_3_account_id
    - player_4_account_id
    - player_5_account_id
    - player_6_account_id
    - admin_account_id

**get_heroes()**

:return: list[Hero]

    - localized_name
    - name
    - url_small_portrait
    - url_large_portrait
    - url_full_portrait
    - url_vertical_portrait

**get_tournament_prize_pool(leagueid, **kwargs):**

:return: TournamentPrizePool

    - prize_pool
    - league_id

**get_game_items()**

:return: list[Item]

    - localized_name
    - name
    - is_recipe
    - in_secret_shop
    - cost
    - in_side_shop
    - url_image

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

TODO
---------
- Parse abilities from live league games
  - http://dev.dota2.com/showthread.php?t=156783

