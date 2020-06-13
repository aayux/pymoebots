import numpy as np

from dataclasses import dataclass, field
from numpy import array, ndarray, uint8
from ...functional.agent import Agent
from ..core import Core

@dataclass
class Amoebot(Core):
    r"""
    core amobeot functionalities, extended using functional modules
    """

    # bots should be locally indistinguishable this name-mangled
    # variable is used only for optimizing the frontend load
    __bot_id: int = field(default=None)

    # stores unique ordering of ports
    port_labels: ndarray = field(default=None)

    # head of the bot
    head: object = field(default=None)

    # tail of the bot
    tail: object = field(default=None)

    # number of parallel agents the bot is running
    n_agents: uint8 = field(default=None)

    # the ameobot's worker agent
    agent: Agent = field(default=None)

    # count of ports scanned
    n_ports_scanned: uint8 = field(default=None)

    # 1 if port scan returns an empty space
    empty_flag: uint8 = field(default=None)

    # activation status, true means the bot is active
    active: uint8 = field(default=None)

    def __post_init__(self):
        self.active = True

        self.head.arrival(bot=self)
        self.tail = self.head

        self.n_ports_scanned = uint8(0)
        self.port_labels = np.empty(0, dtype='<U2')

        self.empty_flag = uint8(0)

        self.orient()

    def execute(self) -> uint8:
        r"""
        Worker function for each amoebot. Manages parallelisation between agents
        and attaches functional modules to the amoebot.

        returns: np.uint8:   execution status
        """
        # if the bot is active
        if self.active:

            self.agent = Agent(bot=self, agent_id=0)
            self.agent.move()

            return uint8(1)
        
        else: return uint8(0)
    
    def orient(self) -> uint8:
        r""" 
        orients with a random clockwise ordering of ports around the bot

        returns: np.uint8: execution status
        """

        ports = self.head._get_ports()
        n_ports = uint8(len(ports))

        # choose a port at random
        choice = np.random.choice(ports)
        choice_ix = uint8(np.where(ports == choice))

        for _ in range(n_ports):
            self.port_labels = np.append(self.port_labels, 
                                        ports[choice_ix % uint8(6)])
            choice_ix += uint8(1)

        return uint8(1)

    def _get_id(self): raise NotImplementedError

    def _get_head(self): return self.head
