# -*- coding: utf-8 -*-

""" elements/bot/manager.py
"""

from ..core import Core

import pickle
import numpy as np
from collections import defaultdict

# global wait time for agents
WAIT_TIME: np.uint8 = 64

class Amoebot(Core):
    r"""
    Core amobeot functionalities, extended using algorithmic modules.

    Attributes

        __id (numpy.uint8) :: unique particle identifier.
        head (numpy.ndarray) :: position (x and y co-ordinates) of amoebot head.
        tail (numpy.ndarray) :: position (x and y co-ordinates) of amoebot tail.
        labels (numpy.ndarray) :: lookup directions in grid from port labels.
        h_neigbor_status (dict) :: status of the amoebot's neighbourhood around
                        its head.
        t_neigbor_status (dict) :: status of the amoebot's neighbourhood around
                        its tail.
        mu (numpy.uint8) :: rate parameter for Poisson clock.
        tau0 (numpy.float16) :: temperature parameter for compression.
        cflag (numpy.uint8) :: status flag for compression algorithm.
        active (bool) :: activation status of the amoebot
        clock (numpy.uint8) :: time on the Poisson clock.

    """

    def __init__(self, __id:np.uint8, head:np.ndarray, tail:np.ndarray=None):
        r"""
        Attributes

        __id (numpy.uint8) :: unique particle identifier.
        head (numpy.ndarray) :: position (x and y co-ordinates) of amoebot head.
        tail (numpy.ndarray) default: None :: position (x and y co-ordinates) of 
                        amoebot tail.
        """

        # bots should be locally indistinguishable, this name-mangled
        # variable is accesible only to the `AmoebotManager` instance.
        self.__id:np.uint8 = __id

        # head of the bot
        self.head:np.ndarray = head

        # tail of the bot, initially same as head
        self.tail:np.ndarray = head if tail is None else tail

        # lookup/map for port labels to the general grid direction
        self.labels:dict = self._reset_neighbourhood_map()

        # status of the bot's neighbourhood
        self.h_neighbor_status:dict = self._reset_neighbourhood_map()
        self.t_neighbor_status:dict = self._reset_neighbourhood_map()

        # rate parameter for Poisson clock
        self.mu:np.uint8 = np.uint8(1)

        # temperature parameter for compression
        self.tau0:np.float16 = np.float16(1.)

        # status flag for compression algorithm
        self.cflag:np.uint8 = np.uint8(0)

        # activation status, true means the bot is active
        # self.active, self.clock = self._reset_clock(refresh=True)

        # wait timer for agents
        # self.wait: uint8 = WAIT_TIME

    def orient(self, __nmap:defaultdict=None):
        r""" 
        Orients bot in clockwise ordering of ports starting at random by
        labelling each port.

        NOTE this construction violates the basic constraint of the amoebot 
        model that particles have no sense of direction; but is kept for 
        convenience.

        Attributes
            __nmap (defaultdict) default: None :: a dictionary of dictionaries 
                        used to index nodes using x and y co-odrinates.
        """

        # ports labellings of the node
        node_ports = np.array(['n', 'ne', 'se', 's', 'sw', 'nw'], dtype='<U2')

        # choose a port at random
        choice = np.random.choice(node_ports)
        choice_ix = node_ports.tolist().index(choice)

        # map the neighbouring nodes to the dictionary of labels
        for ix in range(6):
            self.labels[ix] = node_ports[choice_ix % 6]
            choice_ix += 1

        # if __nmap is not None: self.generate_neighbourhood_map(__nmap)

    def generate_neighbourhood_map(self, __nmap:defaultdict):
        r""" 
        Creates a dictionary of neighbourhood statuses around the head 
        (and tail) particles.

        Attributes
            __nmap (defaultdict) :: a dictionary of dictionaries 
                        used to index nodes using x and y co-ordinates.
        """

        # map the neighbourhood around the particle head
        for port in self.h_neighbor_status:
            node = __nmap[self.head[0]][self.head[1]]

            # get the position of neighbour on current port
            n_position = node.neighbors[self.labels[port]]

            # mark the neighbourhood status except own tail
            if np.any(n_position != self.tail):
                if n_position is not None:
                    neighbor = __nmap[n_position[0]][n_position[1]]
                    self.h_neighbor_status[port] = neighbor.get_occupancy_status
            # mark own tail with (-1)
            else: self.h_neighbor_status[port] = np.int8(-1)

        # if this is an expanded particle, also map the tail
        if not self._is_contracted:
            for port in self.t_neighbor_status:
                node = __nmap[self.tail[0]][self.tail[1]]

                # get the position of neighbour on current port
                n_position = node.neighbors[self.labels[port]]

                # mark the neighbourhood status except own tail
                if np.any(n_position != self.head):
                    if n_position is not None:
                        neighbor = __nmap[n_position[0]][n_position[1]]
                        self.t_neighbor_status[port] = \
                                        neighbor.get_occupancy_status
                # mark own head with (-1)
                else: self.t_neighbor_status[port] = np.int8(-1)
        # else clear the tail neigbourhood status flags
        else: self.t_neighbor_status = self._reset_neighbourhood_map()

    def _neighborhood_contraction_status(
                                            self, 
                                            scan_tail:bool=False
                                        ) -> np.ndarray:
        r""" 
        Find the contraction status of the neighbourhood, a list that is
        1 when a neighbouring node is unoccupied, contracted or occupied by a 
        tail and 0 when occupied by an expanded head particle.

        Attributes
            scan_tail (bool) :: if true, scan the tail; else scan the particle 
                        head.

        Return (np.ndarray): a list of contraction statuses in neighbouring 
                        positions.
        """

        scan = self.t_neighbor_status if scan_tail else self.h_neighbor_status
        return np.array([status != 2 for _, status in scan.items()])

    def open_ports(self, scan_tail:bool=False) -> np.ndarray:
        r"""
        Scan the particle neighbourhood for ports to expand into.

        Attributes
            scan_tail (bool) default: False :: if true, scan the tail; else scan
                            the particle head.

        Return (numpy.ndarray): a list of open or available ports.
        """

        open_port_list = list()
        scan = self.t_neighbor_status if scan_tail else self.h_neighbor_status

        for port in scan:
            status = scan[port]
            # nodes with status 0 are unoccupied
            if status == np.uint8(0):
                open_port_list.append(port)

        return np.array(open_port_list)
    
    def _reset_neighbourhood_map(self) -> dict:
        r"""
        Return (dict): dictionary with port labels as keys and `None` values.
        """
        return dict([(ix, None) for ix in range(6)])

    def _reset_clock(self, refresh:bool) -> tuple:
        r"""
        Set or reset the amoebots Poisson clock whenever the particle execution
        occurs.

        Attributes
            refresh (bool) :: refresh the clock activation if true.
        
        Returns (tuple): 2-tuple with activation status (bool) and value of the
                        Poisson clock.
        """
        if refresh:
            self.clock = np.uint8(np.random.poisson(lam=self.mu))
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
    
    def _move(self, **kwargs): raise NotImplementedError
    
    def _compress(self, **kwargs): raise NotImplementedError
