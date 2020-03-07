from dataclasses import dataclass, field

import numpy as np


@dataclass
class Link:
    """This class is responsible for communication between the agents of bots next to each other"""
    test: np.uint8 = field(default=np.uint(0))
    link_id: np.uint8 = field(default=None)
    successor_received: np.uint8 = field(default=np.uint(0))
    predecessor_received: np.uint8 = field(default=np.uint(0))

    def package_received(self, predecessor=None, successor=None, check=None):
        """This method returns the predecessor or successor package received value as 1 """
        if predecessor is not None and check is None:
            self.predecessor_received = np.uint8(1)
        elif successor is not None and check is None:
            self.successor_received = np.uint8(1)
        elif predecessor is not None and check is not None:
            return self.predecessor_received
        elif successor is not None and check is not None:
            return self.successor_received


    def get_test(self):
        return self.test

    def test_signal(self):
        self.test += np.uint(1)