import numpy as np
from numpy import uint8, array
from dataclasses import dataclass, field

# from ..network.objects import MessagePipe, Packet, Token
# from ..network.handler import MessageHandler

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
    
    def move(self, direction:str=None):
        r"""
        Simple (random) movement algorithm for the amoebot model.
        
        :param direction: direction of movement (one of port labeling); if no 
                          value provided, movement is performed randomly.
        :type value: str
        
        :return: None
        """
        # contract and expanded particle
        if self.bot.head is not self.bot.tail:
            pull = self.bot.tail
            self.bot.tail = self.bot.head
            pull.departure()
        
        # select a random direction all available ports in scan order
        elif direction is None:
            open_ports = self._scan_ports(mode='open')
            if open_ports:
                push = self.bot.head.get_node(np.random.choice(open_ports))
                self.bot.head = push
                self.bot.head.arrival(bot=self.bot)
        
        # collect state for tracker
    
    def _scan_ports(self, mode='open') -> object:
        r"""
        mode : (open) returns a list of open ports for bot to move to
        """
        if mode == 'open':
            open_ports = list()
            for port in self.bot.head._get_ports():
                
                node = self.bot.head._get_neighbor(port)
                if (node is not None) and (not node._get_occupied()):
                    open_ports.append(port)

            return open_ports
        else: return None
