class Agent:
    """
    Agent class which can be one of three running inside a particle at the same time.
    """
    def __init__(self, predecessor, successor, token_value, candidacy, parent, angle):
        # Port keyword of successor
        self.__predecessor = predecessor

        # Port keyword of successor
        self.__successor = successor

        # Reference to parent bot for information passing
        self.__parent = parent

        # Result of this agent's value in c.seg
        self.token_value = token_value

        # Boolean am i on a candidate particle?
        self.candidacy = candidacy

        # Number of empty regions between predecessor and successor
        self.angle = angle

        # Active status
        self.active = True

    def publish_to_parent(self, info):
        """
        Information to pass to parent bot

        :param: info: any valid information structure understood by parent and agent
        """

        return

    def pull_from_parent(self):
        """
        Pulls any relevant information addressed to it from parent.
        """
        return

    def compare(self):
        """
        Compare value of self token and data pulled from parent
        """
        return

    def activate(self):
        """
        Activates the agent
        """
        return

    def deactivate(self):
        """
        Deactivates the agent
        """
        return

    def wait(self):
        """
        Nothing possible to do this timestep (waiting on acknowledgement etc.)
        """
        return
