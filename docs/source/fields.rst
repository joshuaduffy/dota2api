######
Fields
######

This section describes top-level fields, sub-fields, and possible collections of fields from API responses.

.. _league:

league
=========
Contains information about league games. Can be basic (summary) information, or a more detailed form with unique player
identification.


.. _match:

match
=========
A response with a single ``match`` or list of matches will contain overall information about the state of the match, as well as
some amount of information regarding the players in the match. There can be two forms: detailed and basic.

match (Detailed)
-----------------
.. csv-table::

    ``status``                  , (?) Current status of the match
    ``[ player ]``               , List of players within the match; see :ref:`player`
    ``season``                  , Season match was played in
    ``radiant_win``             , Winning team of the match (Dire == false)
    ``duration``                , Current or completed duration of the match
    ``start_time``              , Start time of the match
    ``match_id``                , Unique match identifier
    ``match_seq_num``           , (?)
    ``tower_status_radiant``    , Tower status for Radiant; see (ref)
    ``tower_status_dire``       , Tower status for Dire; see (ref)
    ``barracks_status_radiant`` , Barracks status for Radiant; see (ref)
    ``barracks_status_radiant`` , Barracks status for Dire; see (ref)
    ``cluster``                 , (?)
    ``cluster_name``            , (?)
    ``first_blood_time``        , Timestamp of first blood
    ``lobby_type``              , Lobby type
    ``lobby_name``              , Lobby name
    ``human_players``           , List of human players in the game
    ``leagueid``                , League ID; see :ref:`league`
    ``positive_votes``          , (?)
    ``game_mode``               , (?)
    ``game_mode_name``          , (?)

Additional fields for team (ranked) matches:

.. csv-table::

    ``radiant_name``            ,
    ``radiant_logo``            ,
    ``radiant_team_complete``   , 
    ``dire_name``               ,
    ``dire_logo``               , 
    ``dire_team_complete``      ,

match (Basic)
--------------
.. note::
    The basic form of ``match`` is used in a multi-part response from the ``get_match_history()`` function. This is why there are
    fields referring to the current number of results and total results.

.. csv-table::

    ``num_results``         , Number of results in this response
    ``total_results``       , Total number of results in this response
    ``results_remaining``   , Number of remaining results that can be requested
    ``[matches]``           , List of "basic form" matches in the format below

Each individual ``match`` in the list of ``matches`` contains the following fields:

.. csv-table::

    ``match_id``        , Unique ID of the match
    ``match_seq_num``   , (?)
    ``start_time``      , Start time in UTC
    ``lobby_type``      , (?)
    ``[ players ]``     , List of players in this match in basic form; see :ref:`player_basic`

.. _player:

player
===========
Much like ``match``, the ``player`` field can take two forms: detailed or basic. The detailed version provides additional information about 
things like inventory and building/player stats. The basic version provides enough information to uniquely identify 
the player and has inner fields that can be used in other API calls for additional information.

player (Detailed)
-------------------
.. csv-table::

    ``account_id``      , Steam ID for the player
    ``player_slot``     , Position (0-4) of the player in the team
    ``hero_id``         , ID for the hero being played
    ``hero_name``       , Name of the hero being played
    ``item_#``          , Item in slot #; up to 6 (index 0 through 5)
    ``item_#_name``     , Name of item in slot #
    ``kills``           , Number of kills this match
    ``deaths``          , Number of deaths this match
    ``assists``         , Number of assists this match
    ``leaver_status``   , Status if player has left the game; see :ref:`leaver_status`.
    ``gold``            , (?) Current or final gold of the player
    ``last_hits``       , Number of last hits (CS)
    ``denies``          , (?) Number of denies
    ``gold_per_min``    , Average gold per minute in the match
    ``xp_per_min``      , Average XP per minute in the match
    ``gold_spent``      , Total gold spent during the match
    ``hero_damage``     , Total damage done to other Heroes during the match
    ``tower_damage``    , Total damage done to buildings during the match
    ``hero_healing``    , Total healing done by Hero during match
    ``level``           , (?) Current or final level of the hero
    ``[ ability_upgrades ]``, List of upgraded abilities in order of choosing; see `ability_upgrades`
    ``[ additional_units ]``, Any additional units owned by the player (only applicable to some heroes); see `additional_units`

.. _leaver_status:

leaver_status
^^^^^^^^^^^^^
This describes whether or not the player has ever disconnected, and if so, why.

.. csv-table::
    :header: "ID", "Value", "Description"

    0, "NONE", "finished match, no abandon"
    1, "DISCONNECTED", "player DC, no abandon"
    2, "DISCONNCECTED_TOO_LONG", "player DC > 5min, abandon"
    3, "ABANDONED", "player dc, clicked leave, abandon"
    4, "AFK", "player AFK, abandon"
    5, "NEVER_CONNECTED", "never connected, no abandon"
    6, "NEVER_CONNECTED_TOO_LONG", "too long to connect, no abandon"

.. _ability_upgrades:

ability_upgrades
^^^^^^^^^^^^^^^^
See ``dota2api/ref/abilities.json``

.. _additional_units:

additional_units
^^^^^^^^^^^^^^^^
Only available if the player has an additional unit.

.. csv-table::

    ``unitname`` , Name of the unit
    ``item#``    , Items unit has in inventory, up to 6 (indexed 0-5)

.. _player_basic:

player (Basic)
---------------
.. csv-table::

    ``account_id``      , Steam ID for the player
    ``player_slot``     , Position (0-4) of the player in the team
    ``hero_id``         , ID for the hero being played