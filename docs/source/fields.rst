######
Fields
######

This section describes single fields and collections of fields from responses.

***********
Collections
***********

match
=====

player
===========
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
    ``ability_upgrades``, Upgraded abilities in order of choosing; see (ref)
    ``additional_units``, Any additional units owned by the player (only applicable to some heroes); see (ref)

.. _leaver_status:

leaver_status
-------------
.. csv-table::

    TBD

.. _ability_upgrades:

ability_upgrades
----------------
.. csv-table::

    TBD