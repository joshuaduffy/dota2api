#########
Responses
#########

This section describes the dictionary structure of each response.

Every response has a number of attributes you can use. For example:

.. code-block:: python

    >>> match = api.get_match_details(match_id=1000193456)

The following will return the URL constructed by the library:

.. code-block:: python

    >>> match.url

The following will return the response as raw json:

.. code-block:: python

    >>> match.json

*******************
get_match_history()
*******************
Returns a dictionary with a list of ``players`` within.

``lobby_type`` -- see :ref:`lobby_type`.

``player_slot`` -- see :ref:`player_slot`.

.. code-block:: text

    {
        num_results             - Number of matches within a single response
        total_results           - Total number of matches for this query
        results_remaining       - Number of matches remaining to be retrieved with subsequent API calls
        [matches]               - List of matches for this response
        {
            match_id            - Unique match ID
            match_seq_num       - Number indicating position in which this match was recorded
            start_time          - Unix timestamp of beginning of match
            lobby_type          - See lobby_type table
            [players]           - list of players in the match
            {
                account_id      - Unique account ID
                player_slot     - Player's position within the team
                hero_id         - Unique hero ID
            }
        }
    }

.. _player_slot:

player_slot
=============

The player slot is an 8-bit representation of the player's team and the slot (0-4) within the team.

.. code-block:: text

    ┌─────────────── Team (false if Radiant, true if Dire).
    │ ┌─┬─┬─┬─────── Not used.
    │ │ │ │ │ ┌─┬─┬─ The position of a player within their team (0-4).
    │ │ │ │ │ │ │ │
    0 0 0 0 0 0 0 0

******************************
get_match_history_by_seq_num()
******************************

Returns a dictionary with a list of ``matches`` within. See :ref:`get_match_details()` for structure of matches.

.. code-block:: text

    {
        status
            1 - Success
            8 - matches_requested must be greater than 0
        statusDetail        - Message explaining a status that is not equal to 1
        [matches]           - See get_match_details()
    }

.. _get_match_details():

*******************
get_match_details()
*******************

Returns a dictionary with a list of ``matches`` with ``players``.

For dynamic values such as kills or gold, if the match is live, then the value is current as of
the API call. For matches that have finished, these values are simply the value at the end of the 
match for the player.

``lobby_type`` -- see :ref:`lobby_type`.

``game_mode`` and ``game_mode_name`` -- see :ref:`game_mode`

.. code-block:: text

    {
        season                  - Season the game was played in
        radiant_win             - Win status of game (True for Radiant win, False for Dire win)
        duration                - Elapsed match time in seconds
        start_time              - Unix timestamp for beginning of match
        match_id                - Unique match ID
        match_seq_num           - Number indicating position in which this match was recorded
        tower_status_radiant    - Status of Radiant towers
        tower_status_dire       - Status of Dire towers
        barracks_status_radiant - Status of Radiant barracks
        barracks_status_dire    - Status of Dire barracks
        cluster                 - The server cluster the match was played on, used in retrieving replays
        cluster_name            - ?
        first_blood_time        - Time elapsed in seconds since first blood of the match
        lobby_type              - See lobby_type table
        lobby_name              - See lobby_type table
        human_players           - Number of human players in the match 
        leagueid                - Unique league ID   
        positive_votes          - Number of positive/thumbs up votes
        negative_votes          - Number of negative/thumbs down votes
        game_mode               - See game_mode table
        game_mode_name          - See game_mode table
        [players]
        {
            account_id          - Unique account ID
            player_slot         - Player's position within the team   
            hero_id             - Unique hero ID
            hero_name           - Hero's name
            item_#              - Item ID for item in slot # (0-5)     
            item_#_name         - Item name for item in slot # (0-5)
            kills               - Number of kills by player
            deaths              - Number of player deaths 
            assists             - Number of player assists
            leaver_status       - Connection/leaving status of player
            gold                - Gold held by player
            last_hits           - Number of last hits by player (creep score)
            denies              - Number of denies
            gold_per_min        - Average gold per minute
            xp_per_min          - Average XP per minute
            gold_spent          - Total amount of gold spent
            hero_damage         - Amount of hero damage dealt by player
            tower_damage        - Amount of tower damage dealt by player
            hero_healing        - Amount of healing done by player
            level               - Level of player's hero
            [ability_upgrades]  - Order of abilities chosen by player
            {
                ability         - Ability chosen
                time            - Time *since match start* that ability was upgraded
                level           - Level of player at time of upgrading
            }

            [additional_units]  - Only available if the player has a additional unit
            {
                unitname        - Name of unit
                item_#          - ID of item in slot # (0-5)
            }
        }
        // These fields are only available for team matches //
        radiant_name            - team name for Radiant
        radiant_logo            - team logo for Radiant
        radiant_team_complete   - ?
        dire_name               - team name for Dire
        dire_logo               - team logo for Dire
        dire_team_complete      - ?
    }



********************
get_league_listing()
********************

Returns a dictionary with a list of ``leagues`` within; can be viewed with DotaTV.

.. code-block:: text

    {
        [league]
        {
            name            - name of the league
            leagueid        - Unique league ID
            description     - Description of the league
            tournament_url  - League website information
        }
    }
    

***********************
get_live_league_games()
***********************

Returns a dictionary with a list of ``leagues`` within.

``tower_state`` -- see :ref:`towers_and_barracks`.

.. code-block:: text

    {
        [league]
        {
            [players]               - list of all players in the match
            {
                account_id          - 32-bit account ID
                name                - in-game display name
                hero_id             - Hero ID
                team                - Team the player is o
            }
            radiant_team            - information about the Radiant team
            dire_team               - information about the Dire team
            lobby_id                - ID for the match's lobby
            spectators              - number of spectators (at time of request)
            tower_state             - state of *all* towers
            league_id               - ID for the league in which the match is being played
        }
    }

**************************
get_team_info_by_team_id()
**************************

Returns a dictionary with a list of ``teams`` within.

.. code-block:: text

    {
        [team]
        {
            team_id                             - Unique team ID
            name                                - team's name
            tag                                 - team's tag
            time_created                        - Unix timestamp of team creation
            rating                              - ?
            logo                                - UGC ID for the team logo
            logo_sponsor                        - UGC ID for the team sponsor logo
            country_code                        - ISO 3166-1 country code
            url                                 - team-provided URL
            games_played_with_current_roster    - number of games played by team with current team members
            player_#_account_id                 - account ID for player # (0-5)
            admin_account_id                    - account ID for team admin
        }
    }


**********************
get_player_summaries()
**********************

Returns a dictionary with a list of ``players`` within.

.. code-block:: text

    {
        [player]
        {
            avatarfull
            avatarmedium
            commentpermission
            communityvisibilitystate
            lastlogoff
            loccityid
            loccountrycode
            locstatecode
            personaname
            personastate
            personastateflags
            primaryclanid
            profilestate
            profileurl
            realname
            steamid
            timecreated
        }
    }

************
get_heroes()
************

.. code-block:: text

    {
        count               - number of results
        status              - ?
        [heroes]
        {
            id              - unique hero ID
            name            - hero's name
            localized_name  - localized version of hero's name
        }
    }

****************
get_game_items()
****************

.. code-block:: text

    {
        count               - number of results
        status              - ?
        [items]
        {
            id              - Unique item ID
            name            - item's name
            cost            - item's gold cost
            localized_name  - item's localized name
            recipe          - true if item is a recipe item, false otherwise
            secret_shop     - true if item is bought at the secret shop, false otherwise
            side_shop       - true if item is bought at the side shop, false otherwise
        }
    }

***************************
get_tournament_prize_pool()
***************************

.. code-block:: text

    {
        league_id   - unique league ID
        prizepool   - Current prize pool if the league includes a community-funded pool, otherwise 0
        status      - ?
    }

.. _towers_and_barracks:

***************************
Towers and Barracks
***************************

Combined status
===============

The overall match tower and barracks status uses 32 bits for representation and should be interpreted as follows:

.. code-block:: text

    ┌─┬─┬─┬─┬─┬─┬─┬─┬─┬───────────────────────────────────────────── Not used.
    │ │ │ │ │ │ │ │ │ │ ┌─────────────────────────────────────────── Dire Ancient Top
    │ │ │ │ │ │ │ │ │ │ │ ┌───────────────────────────────────────── Dire Ancient Bottom
    │ │ │ │ │ │ │ │ │ │ │ │ ┌─────────────────────────────────────── Dire Bottom Tier 3
    │ │ │ │ │ │ │ │ │ │ │ │ │ ┌───────────────────────────────────── Dire Bottom Tier 2
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌─────────────────────────────────── Dire Bottom Tier 1
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌───────────────────────────────── Dire Middle Tier 3
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌─────────────────────────────── Dire Middle Tier 2
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌───────────────────────────── Dire Middle Tier 1
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌─────────────────────────── Dire Top Tier 3
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌───────────────────────── Dire Top Tier 2
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌─────────────────────── Dire Top Tier 1 
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌───────────────────── Radiant Ancient Top
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌─────────────────── Radiant Ancient Bottom
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌───────────────── Radiant Bottom Tier 3
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌─────────────── Radiant Bottom Tier 2
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌───────────── Radiant Bottom Tier 1
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌─────────── Radiant Middle Tier 3
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌───────── Radiant Middle Tier 2
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌─────── Radiant Middle Tier 1
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌───── Radiant Top Tier 3
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌─── Radiant Top Tier 2
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌─ Radiant Top Tier 1
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

Single team tower status
========================

The tower status for a single team uses 16 bits for representation and should be interpreted as follows:

.. code-block:: text

    ┌─┬─┬─┬─┬─────────────────────── Not used.
    │ │ │ │ │ ┌───────────────────── Ancient Bottom
    │ │ │ │ │ │ ┌─────────────────── Ancient Top
    │ │ │ │ │ │ │ ┌───────────────── Bottom Tier 3
    │ │ │ │ │ │ │ │ ┌─────────────── Bottom Tier 2
    │ │ │ │ │ │ │ │ │ ┌───────────── Bottom Tier 1
    │ │ │ │ │ │ │ │ │ │ ┌─────────── Middle Tier 3
    │ │ │ │ │ │ │ │ │ │ │ ┌───────── Middle Tier 2
    │ │ │ │ │ │ │ │ │ │ │ │ ┌─────── Middle Tier 1
    │ │ │ │ │ │ │ │ │ │ │ │ │ ┌───── Top Tier 3
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌─── Top Tier 2
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ┌─ Top Tier 1
    │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0   

Single team barracks status
===========================

The barracks status uses 8 bits for representation and should be interpreted as follows:

.. code-block:: text
    
    ┌─┬───────────── Not used.
    │ │ ┌─────────── Bottom Ranged
    │ │ │ ┌───────── Bottom Melee
    │ │ │ │ ┌─────── Middle Ranged
    │ │ │ │ │ ┌───── Middle Melee
    │ │ │ │ │ │ ┌─── Top Ranged
    │ │ │ │ │ │ │ ┌─ Top Melee
    │ │ │ │ │ │ │ │
    0 0 0 0 0 0 0 0

.. _status_code_mappings:

***************************
Status code mappings
***************************

These tables outline various codes/status in responses and their meaning.

See ``dota2api.parse`` for various parsing utilities.

.. _game_mode:

game_mode
=========
.. csv-table::
    :header: "Value", "Description"

    0, None
    1, All Pick
    2, Captain's Mode
    3, Random Draft
    4, Single Draft
    5, All Random
    6, Intro
    7, Diretide
    8, Reverse Captain's Mode
    9, The Greeviling
    10, Tutorial
    11, Mid Only
    12, Least Played
    13, New Player Pool
    14, Compendium Matchmaking
    16, Captains Draft

.. _lobby_type:

lobby_type
==========
.. csv-table::
    :header: "Status", "Description"

    -1, invalid
    0, Public matchmaking
    1, Practice
    2, Tournament
    3, Tutorial
    4, Co-op with AI
    5, Team match
    6, Solo queue
    7, Ranked matchmaking
    8, 1v1 solo mid

.. _leaver_status:

leaver_status
=============
.. csv-table::
    :header: "ID", "Value", "Description"

    0, "NONE", "finished match, no abandon"
    1, "DISCONNECTED", "player DC, no abandon"
    2, "DISCONNCECTED_TOO_LONG", "player DC > 5min, abandon"
    3, "ABANDONED", "player dc, clicked leave, abandon"
    4, "AFK", "player AFK, abandon"
    5, "NEVER_CONNECTED", "never connected, no abandon"
    6, "NEVER_CONNECTED_TOO_LONG", "too long to connect, no abandon"

.. _team_id:

team_id
=======
.. csv-table::
    :header: "Value", "Description"

    0, Radiant
    1, Dire
    2, Broadcaster
    3+, unassigned (?)