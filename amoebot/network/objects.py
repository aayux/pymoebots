import numpy as np
from numpy import uint8, array, ndarray
from dataclasses import dataclass, field

@dataclass
class MessagePipe(object):
    r"""
    A "network object" class that handles communication between the agents of 
    neighbouring particles or bots.
    """

    token:object = field(default=None)
    p_agent: object = field(default=None)
    s_agent: object = field(default=None)

    def __post_init__(self):
        self.test = uint8(0)

    def set_predecessor_agent(self, agent:object):
        self.p_agent = agent

    def set_successor_agent(self, agent:object):
        self.s_agent = agent

@dataclass
class Packet(object):
    r"""
    A "network object" class that wraps token into a message packet 
    shared between particles or bots.
    """
    raise NotImplementedError

@dataclass
class Token(Packet):
    r"""
    A "network object" class, inherits from Packet. Contains actual information 
    content shared between particles or bots.
    """
    raise NotImplementedError