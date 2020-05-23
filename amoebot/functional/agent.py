import numpy as np
from numpy import uint8, array

# from ..network.objects import MessagePipe, Packet, Token
# from ..network.handler import MessageHandler

# constant wait time for each agent
WAIT_TIME: uint8 = 64

class Agent(object):
    r"""
    all amoebot algorithms are written as member functions of class `Agent`
    """
    def __init__(self, bot:object, agent_id:uint8):
        
        # agent's assigned particle (or bot)
        self.bot: object = bot

        # the agent's identifier on its bot
        self.agent_id: uint8 = agent_id

        # agent's wait timer
        self.wait_clock: uint8 = None

    def compression(self): raise NotImplementedError
    
    def move(self, direction:str=None):
        r"""
        Simple (random) movement algorithm for the amoebot model.

        :param direction: direction of movement (one of port labeling); if no 
                          value provided, movement is performed randomly.
        :type: str

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
                push = self.bot.head._get_neighbor(np.random.choice(open_ports))
                self.bot.head = push
                self.bot.head.arrival(bot=self.bot)

    def _scan_ports(self, mode:str='open') -> object:
        r"""
        :param mode : (open) returns a list of open ports for bot to move to
        :type: str

        :return: None
        """
        if mode == 'open':
            open_ports = list()
            for port in self.bot.head._get_ports():
                
                node = self.bot.head._get_neighbor(port)
                if (node is not None) and (not node._get_occupied()):
                    open_ports.append(port)

            return open_ports
        else: return None
