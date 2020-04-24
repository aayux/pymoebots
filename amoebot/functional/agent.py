import numpy as np
from numpy import uint8, array
from dataclasses import dataclass, field

from ..network.objects import MessagePipe, Packet, Token
from ..network.handler import MessageHandler

@dataclass
class Agent(object):
    r"""
    all amoebot algorithms are written as member functions of class `Agent`
    """

    # agent's assigned particle (or bot)
    bot: object = field(default=None)

    # the agent's identifier on its bot
    agent_id: uint8 = field(default=None)

    # current node position on the grid, object of type `Node`
    position: object = field(default=None)

    # agent's predecessor node direction
    predecessor: str = field(default=None)

    # agent's successor node direction
    successor: str = field(default=None)

    # reference to agent's successor node
    s_node: object = field(default=None)

    # reference to agent's predecessor node
    p_node: object = field(default=None)

    # reference to agent's predecessor node
    s_bot: object = field(default=None)

    # The reference to the predecessor bot
    p_bot: object = field(default=None)

    # agent's wait timer
    wait_clock: uint8 = field(default=None)

    # constant wait time for each agent
    WAIT_TIME: uint8 = 64

    def __post_init__(self, bot, agent, position, predecessor, successor):
        self.bot = bot
        self.agent_id = agent
        self.position = position

        self.predecessor = predecessor
        self.successor = successor

        self.p_node = self.position._get_neighbor(port=predecessor)
        self.s_node = self.position._get_neighbor(port=successor)

        self.p_bot = self.predecessor_node._get_bot()
        self.s_bot = self.successor_node._get_bot()
    
    def compression(self): raise NotImplementedError
