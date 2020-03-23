from dataclasses import dataclass, field
from numpy import uint8, array, ndarray, random
import numpy as np


@dataclass
class Link:
    """
    This class is responsible for communication between the agents of bots next to each other
    """

    # Used to test link connection between two agents
    test: uint8 = field(default=None)

    # link_id: uint8 = field(default=None)
    # link_id: ndarray = field(default=None)
    token: object = field(default=None)
    delimiter: object = field(default=None)
    package: object = field(default=None)
    successor_received: uint8 = field(default=None)
    predecessor_received: uint8 = field(default=None)
    predecessor_agent: object = field(default=None)
    successor_agent: object = field(default=None)

    # def package_received(self, predecessor=None, successor=None, check=None):
    # """
    # This method returns the predecessor or successor package received value as 1
    # """
    #     if predecessor is not None and check is None:
    #         self.predecessor_received = np.uint8(1)
    #     elif successor is not None and check is None:
    #         self.successor_received = np.uint8(1)
    #     elif predecessor is not None and check is not None:
    #         return self.predecessor_received
    #     elif successor is not None and check is not None:
    #         return self.successor_received

    def get_delimiter(self):
        return self.delimiter

    def get_predecessor_candidacy(self):
        return self.predecessor_agent.candidate

    def get_test(self):
        return self.test

    def initialize(self):

        # Initializes link
        self.test = uint8(0)
        self.successor_received = uint8(0)
        self.predecessor_received = uint8(0)

        return

    def load_delimiter(self, delimiter=None):
        self.delimiter = delimiter

    def load_token(self, token=None):
        self.token = token

    def remove_delimiter(self):
        self.delimiter = None

    def set_predecessor_agent(self, agent):

        # sets links predecessor agent to given agent
        self.predecessor_agent = agent

        return

    def set_successor_agent(self, agent):

        # sets links predecessor agent to given agent
        self.successor_agent = agent

        return

    def test_signal(self):

        # Add one to the test variable
        self.test += uint8(1)

        return