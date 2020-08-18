import pickle
import numpy as np
from collections import defaultdict
from numpy import array, ndarray, int8, uint8, float16

from ..core import Core

# global wait time for agents
WAIT_TIME: uint8 = 64

class Amoebot(Core):
    r""" core amobeot functionalities, extended using algorithmic modules
    """

    def __init__(self, __id:uint8, head:array, tail:array=None):

        # bots should be locally indistinguishable, this name-mangled
        # variable is accesible only to the manager
        self.__id:uint8 = __id

        # head of the bot
        self.head:array = head

        # tail of the bot, initially same as head
        self.tail:array = head if tail is None else tail

        # lookup/map for port labels to the general grid direction
        self.labels:dict = dict([(uint8(ix), None) for ix in range(6)])

        # status of the bot's neighbourhood
        self.h_neighbor_status = dict([(uint8(ix), None) for ix in range(6)])
        self.t_neighbor_status = dict([(uint8(ix), None) for ix in range(6)])

        # rate parameter for poisson clock
        self.mu:uint8 = uint8(1)

        # compression parameter
        self.lam:float16 = float16(5.)

        # status flag for compression algorithm
        self.cflag:uint8 = uint8(0)

        # activation status, true means the bot is active
        self.active, self.clock = self._reset_clock(refresh=True)

        # wait timer for agents
        # self.wait: uint8 = WAIT_TIME

    def orient(self, nmap:defaultdict=None):
        r""" orients bot in clockwise ordering of ports starting at random
        """

        # ports labellings of the node
        node_ports = array(['n', 'ne', 'se', 
                            's', 'sw', 'nw'
                            ], dtype='<U2')

        # choose a port at random
        choice = np.random.choice(node_ports)
        choice_ix = node_ports.tolist().index(choice)

        # map the neighbouring nodes to the dictionary of labels
        for ix in range(6):
            self.labels[ix] = node_ports[choice_ix % 6]
            choice_ix += 1

        if nmap is not None: self.generate_neighbourhood_map(nmap)

    def generate_neighbourhood_map(self, nmap:defaultdict):
        r""" 
        Creates a dictionary of neighbourhood statuses around the head 
        (and tail) particles.
        """
        for port in self.h_neighbor_status:
            node = nmap[self.head[0]][self.head[1]]
            n_position = node.neighbors[self.labels[port]]

            # mark the neighbourhood status except own tail
            if np.any(n_position != self.tail):
                if n_position is not None:
                    neighbor = nmap[n_position[0]][n_position[1]]
                    self.h_neighbor_status[port] = neighbor.get_occupancy_status
                else: self.h_neighbor_status[port] = int8(5)
            else: self.h_neighbor_status[port] = int8(-1)

        # if this is an expanded particle, also map the tail
        if not self._is_contracted:
            for port in self.t_neighbor_status:
                node = nmap[self.tail[0]][self.tail[1]]
                n_position = node.neighbors[self.labels[port]]

                # mark the neighbourhood status except own tail
                if np.any(n_position != self.head):
                    if n_position is not None:
                        neighbor = nmap[n_position[0]][n_position[1]]
                        self.t_neighbor_status[port] = \
                                        neighbor.get_occupancy_status
                    else: self.t_neighbor_status[port] = int8(5)
                else: self.t_neighbor_status[port] = int8(-1)
        # else reset the tail to null state
        else: self.t_neighbor_status = dict([(ix, None) for ix in range(6)])
    
    def open_ports(self, scan_tail:bool=False) -> list:
        r""" a list of open ports for bot to move to
        """
        open_port_list = list()
        scan = self.t_neighbor_status if scan_tail else self.h_neighbor_status

        for port in scan:
            status = scan[port]
            if status == 0:
                open_port_list.append(port)

        return array(open_port_list)

    def _reset_clock(self, refresh:bool) -> bool:
        r"""
        """
        if refresh:
            self.clock = uint8(np.random.poisson(lam=self.mu))

        else: self.clock -= 1

        return (False, self.clock) if self.clock else (True, self.clock)

    @property
    def _open_port_head(self) -> list:
        return self.open_ports(scan_tail=False)

    @property
    def _open_port_tail(self) -> list:
        return self.open_ports(scan_tail=True)

    @property
    def _is_contracted(self):
        return np.all(self.head == self.tail)

    @property
    def pickled(self): return pickle.dumps(self)

    @classmethod
    def unpickled(cls, data:bytes): return pickle.loads(data)

    def execute(self): raise NotImplementedError
    
    def move_agent(self, **kwargs): raise NotImplementedError
    
    def compress_agent(self, **kwargs): raise NotImplementedError
