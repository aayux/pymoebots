import sys
import numpy as np

from concurrent import futures
from dataclasses import dataclass, field
from collections import defaultdict
from numpy import array, ndarray, uint8

from .core import Amoebot
from .helpers import AnonList
from ..node.core import Node
from ..utils.baseutils import increment_index
from ..utils.exceptions import InitializationError
from ..manager import Manager

@dataclass
class AmoebotManager(Manager):
    r"""
    manages thread assignment to agents and allocates functionals to bots
    """

    # holds all `Amoebot` objects created anonymously
    amoebots:AnonList = field(default_factory=AnonList)

    # truth values signalling execution status of each bot, 1 when complete
    status: dict = field(default_factory=dict)

    def __post_init__(self):
        self.status = {0: list(), 1: list()}

    def _add_bot(self, node:Node):
        r"""
        adds individual amoebots to the `AnonList`
        """

        bot = Amoebot(head=node)
        self.amoebots.insert(bot)


    # TODO: move placement to separate class
    def random_placement(self, n_bots:int, node_list:list):
        r"""
        places bots on an instance of a `elements.node.core.Node` of the 
        triangular graph randomly
        """

        node_list = ndarray(node_list)
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
            raise InitializationError(f"Amoebots have not been initialized "
                                      f"correctly, check file and retry. Exiting!")
            sys.exit(0)

        self.status = status

    def m_activate(self) -> uint8:
        r"""
        sets up threaded calls to activation methods for all bots
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
        """

        # one cycle of activation per amoebot
        for amoebot in self.amoebots: self._activate(amoebot)

        status = self.status

        # return 1 if everything ran successfully
        if len(status[0]) == 0: return uint8(1)

        return uint8(0)