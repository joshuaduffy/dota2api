########
Tutorial
########

This section covers basic usage of the library.

******************
Getting an API Key
******************

Get one from `Valve`_.

*******************************
D2_API_KEY environment variable
*******************************

You can set the ``D2_API_KEY`` environment variable to save entering it all the time.

For example, in Linux:

.. code-block:: bash

    $  export D2_API_KEY=83247983248793298732

************
Initialising
************

If you've set the API Key as an environment variable, initialise the module like so:

.. code-block:: python

    >>> import dota2api
    >>> api = dota2api.Initialise()

If not you'll need to pass it into the constructor:

.. code-block:: python

    >>> import dota2api
    >>> api = dota2api.Initialise("45735474375437457457")


Official DOTA2 web API would response identifiers for records like heroes, items, lobby type, game mode, etc. By default, this dota2api would translate most dota2 identifiers into human readable strings.
But you can disable our translation by enabling raw mode:

.. code-block:: python

    >>> import dota2api
    >>> api = dota2api.Initialise("45735474375437457457", raw_mode=True)

By default, you'll get {"hero_name": "axe"} for axe but when raw_mode is on, it will be replaced by {"hero_id", 2}.

*********
API calls
*********

The functions are mapped to API calls:

.. code-block:: python

    >>> match = api.get_match_details(match_id=1000193456)

The responses are then returned in a ``dict``:

.. code-block:: python

    >>> match['radiant_win']
    False

Parameters can be used to filter the results. They're all listed in the :doc:`Library Reference </reference>`

*****************
Get match history
*****************

You can use the ``account_id`` parameter to filter the results for a specific user.

.. code-block:: python

    >>> hist = api.get_match_history(account_id=76482434)

*****************
Get match details
*****************

.. code-block:: python

    >>> match = api.get_match_details(match_id=1000193456)

***************
Other API calls
***************

Listed in the :doc:`Library Reference </reference>`

**********
Exceptions
**********

``APIError`` will be raised if an error message is returned by the API.

``APITimeoutError`` will be raised you're making too many requests or the API itself is down.

``APIAuthenticationError`` will be raised if you're using an invalid API key.


.. _`Valve`: https://steamcommunity.com/dev/apikey