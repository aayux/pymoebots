class Link:
    """
    One instance of shared memory shared between two particles.
    Only bot_from may publish to it,
    and only bot_to may pull from it.
    Each of the methods require the caller to pass some form of ID to confirm
    that no memory gets read by the wrong party or deleted early.
    """
    def __init__(self, bot_from, bot_to):
        # ID of bot_from.
        ## Can this be an instance of the bot itself? Might be too much memory?
        self.__bot_from = bot_from

        # ID of bot_to
        self.__bot_to   = bot_to

        # Any valid data structure understood by bots/agents.
        self.data       = None

        # Upon receiving the information, bot_to sets this to True
        # and the Link takes this is confirmation it has copied the info,
        # If called by bot_from, the shared memory is deleted and this
        # bit set back to False
        self.acknowledgement = False

    def publish_to(self, caller, info):
        """
        Only accessible by bot_from. Pass information into the shared space.
        """
        if caller == bot_to or this.acknowledgement:
            return
        else:
            # Do stuff
            return

    def pull_from(self, caller):
        """
        Only accessible by bot_to. Copy memory to bot_to.
        """
        if caller == bot_from or not this.acknowledgement:
            return
        else:
            # Do stuff
            return

    def acknowledge(self, caller):
        """
        Allows bot_to to set the acknowledgement bit.
        If called by bot_from, and ack bit is set, clears memory.
        """
        if caller == bot_from and not this.acknowledgement:
            return
        elif caller == bot_to and not this.acknowledgement:
            self.acknowledgement = True
        else: # caller == bot_from and this.acknowledgement
            self.data = None
            self.acknowledgement = False
        return
