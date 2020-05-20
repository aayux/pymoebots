import sys
import numpy as np

from concurrent import futures
from numpy import ndarray, uint8

from .core import Amoebot
from ...extras.structures import AnonList
from ..node.core import Node
from ...extras.exceptions import InitializationError
from ..manager import Manager

class AmoebotManager(Manager):
    r"""
    manages thread assignment to agents and allocates functionals to bots
    """

    def __init__(self):
        # holds all `Amoebot` objects created anonymously
        self.amoebots:AnonList = AnonList()

        # truth values signalling execution status of each bot, 1 when complete
        self.status: dict = {0: list(), 1: list()}

    def _add_bot(self, node:Node):
        r"""
        adds individual amoebots to the `AnonList`
        """

        bot = Amoebot(head=node)
        self.amoebots.insert(bot)

    # TODO: move placement to separate class
    def random_placement(self, n_bots:int, node_list:list):
        r"""
        places bots on an instance of `elements.node.core.Node` of the 
        triangular graph randomly
        """

        node_list = np.asarray(node_list)
        np.random.shuffle(node_list)

        # add bot to the list at random node position
        for ix in range(n_bots): self._add_bot(node_list[ix])

    def _activate(self, amoebot:Amoebot):
        r"""
        execute one timestep of `elements.bots.core.Amoebot.execute()`
        """
        # TODO: required? copy variables and methods to avoid contention
        status = self.status

        try:
            # execute the amoebot algorithms and update execution status
            status[amoebot.execute()] = amoebot
        except IndexError:
            raise InitializationError(
                                f"Amoebots have not been initialized "
                                f"correctly, check file and retry. Exiting!"
            )
            sys.exit(0)

        self.status = status

    def m_activate(self) -> uint8:
        r"""
        sets up threaded calls to activation methods for all bots

        returns: np.uint8:   execution status
        """
        # TODO: required? copy variables and methods to avoid contention
        activate = self._activate

        with futures.ThreadPoolExecutor() as executor:

            # maps range to active method
            executor.map(activate, self.amoebots)

        status = self.status

        # return 1 if everything ran successfully
        if len(status[0]) == 0: return uint8(1)

        return uint8(0)

    def s_activate(self) -> uint8:
        r"""
        Sequential bot activations; activations are arbitrary as long as each 
        amoebot gets a chance to run during a cycle.

        returns: np.uint8:   execution status
        """

        # one cycle of activation per amoebot
        for amoebot in self.amoebots: self._activate(amoebot)

        status = self.status

        # return 1 if everything ran successfully
        if len(status[0]) == 0: return uint8(1)

        return uint8(0)