.. NOTE: that headings have to have the exact number of
   underlines as the length of their preceding line

Agent Class
===========

This class represents a thread, of which a bot can have up to three.
These agents operate on a bot based on how many boundaries the bot is on,
and run algorithms entirely separate from each other, even if two of
them are on the same boundary. No data is shared between these agents while
inside a bot.

An example is shown below regarding how bots initialize these agents based on
how many boundaries of the system they are on.

TODO: diagram of bots.

Class Definition
----------------

.. autoclass:: agent.Agent
   :members:
