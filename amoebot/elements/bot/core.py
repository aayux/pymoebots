import numpy as np

from numpy import array, ndarray, uint8, float16

from ..core import Core

# global wait time for agents
WAIT_TIME: uint8 = 64

class Amoebot(Core):
    r""" core amobeot functionalities, extended using algorithmic modules
    """

    def __init__(self, __bot_id:int, head:object):

        # bots should be locally indistinguishable this name-mangled
        # variable is used only for optimizing the frontend load
        self.__bot_id:int = __bot_id

        # head of the bot
        self.head:object = head
        self.head.arrival(bot=self)

        # tail of the bot, initially same as head
        self.tail:object = self.head

        # rate parameter for poisson clock
        self.mu:uint8 = uint8(1)

        # compression parameter
        self.lam:float16 = float16(5.)

        # count of ports scanned
        self.n_ports_scanned:uint8 = uint8(0)

        # stores unique ordering of ports
        self.port_labels = np.empty(0, dtype='<U2')

        # status flag for compression algorithm
        self.cflag:uint8 = uint8(0)

        # activation status, true means the bot is active
        self.active:bool = self._reset_clock(refresh=True)

        # wait timer for agents
        self.wait: uint8 = WAIT_TIME

        self.orient()

    def orient(self) -> uint8:
        r""" 
        orients with a random clockwise ordering of ports around the bot

        returns: np.uint8: execution status
        """

        ports = self.head.get_ports
        n_ports = uint8(len(ports))

        # choose a port at random
        choice = np.random.choice(ports)
        choice_ix = uint8(np.where(ports == choice))

        for _ in range(n_ports):
            self.port_labels = np.append(self.port_labels, 
                                        ports[choice_ix % uint8(6)])
            choice_ix += uint8(1)

        return uint8(1)

    def _reset_clock(self, refresh:bool) -> bool:
        r"""
        """
        if refresh:
            self.clock = uint8(np.random.poisson(lam=self.mu))
        
        else: self.clock -= 1

        return False if self.clock else True
    
    def get_open_ports(self, scan_tail=False) -> list:
        r""" a list of open ports for bot to move to
        """
        open_port_list = list()
        scan = self.tail if scan_tail else self.head

        for port in scan.get_ports:
            node = scan.get_neighbor(port)
            if (node is not None) and (not node.get_occupied):
                open_port_list.append(port)

        return open_port_list
    
    @property
    def _open_port_head(self) -> list:
        return self.get_open_ports(scan_tail=False)

    @property
    def _open_port_tail(self) -> list:
        return self.get_open_ports(scan_tail=True)

    @property
    def _is_contracted(self):
        return np.all(self.head.position == self.tail.position)


    def execute(self): raise NotImplementedError
    
    def move_agent(self, **kwargs): raise NotImplementedError
    
    def compress_agent(self, **kwargs): raise NotImplementedError
