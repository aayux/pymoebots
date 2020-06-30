import numpy as np
from numpy import uint8, array

from .core import Amoebot

# from ..functional.nwobjects import MessagePipe, Packet, Token
# from ..functional.mesghandler import MessageHandler

class Agent(Amoebot):
    r""" all amoebot algorithms are written as member functions of class `Agent`
    """

    def __init__(self, __bot_id:int, head:object):
        super().__init__(__bot_id, head)

    def execute(self) -> tuple:
        r"""
        Worker function for each amoebot. Intended to manage parallelisation 
        between agents and attach algorithmic modules to the amoebot.

        returns: np.uint8: execution status
        """

        # if the agent is active
        if self.active:

            # run one step of an elementary algorithm
            self.move_agent()

            # reset the poisson clock
            self.active = self._reset_clock(refresh=True)

            return (self, uint8(1))

        else:
            # decrement the clock and get active status
            self.active = self._reset_clock(refresh=False)

            return (self, uint8(0))
    
    def compress_agent(self):
        r"""
        """
        raise NotImplementedError
    
    def move_agent(self, direction:str=None):
        r"""
        Simple (random) movement algorithm for the amoebot model.

        direction : direction of movement (one of port labeling); if no 
                    value provided, movement is performed randomly.

        returns: None
        """

        # contract an expanded particle
        if  self.head is not self.tail:
            pull = self.tail
            self.tail = self.head
            pull.departure()
        
        # expand a contracted particle
        else:
            # get all available ports in scan order
            open_ports = self.get_open_ports


            # select a random direction when none provided
            if direction is None and open_ports: 
                direction = np.random.choice(open_ports)
            
            # move to indicated direction if available
            if direction in open_ports:
                push = self.head.get_neighbor(direction)
                self.head = push
                self.head.arrival(bot=self)

    @property
    def get_open_ports(self) -> list:
        r""" a list of open ports for bot to move to
        """
        open_port_list = list()
        for port in self.head.get_ports:
            
            node = self.head.get_neighbor(port)
            if (node is not None) and (not node.get_occupied):
                open_port_list.append(port)

        return open_port_list
