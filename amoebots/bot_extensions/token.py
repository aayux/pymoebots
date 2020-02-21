class Token:
    """
    Representation of a token passed by candidates
    """
    def __init__(self, token_value, delim):
        # Token data value
        ## NOTE for pos/neg token comparisons in solitude verif, this should be
        ## available to use as a dictionary of lists
        self.value = value
        # Is this token a delimiter.
        self.delim = delim
        # Starts deactivated
        self.active = False

    def activate(self):
        """
        Turn on for comparisons
        """
        self.active = True
        return

    def deactivate(self):
        """
        Turn off from comparisons
        """
        self.active = False
        return

    def compare(value_to_compare):
        """
        Does calculation with passed in value to decide whether or not to deactivate
        """
        return
