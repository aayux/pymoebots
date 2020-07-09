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
            self.move_agent(contr_to_head=True)

            # reset the poisson clock
            self.active = self._reset_clock(refresh=True)

            return (self, uint8(1))

        else:
            # decrement the clock and get active status
            self.active = self._reset_clock(refresh=False)

            return (self, uint8(0))
    
    def compress_agent(self, async_mode=True):
        r"""
        async_mode : if True, execute the local, distributed, asynchronous 
                     algorithm for compression else run sequential algorithm.
        returns : None
        """

        # get all available ports in scan order
        open_ports = self.get_open_ports()

        # execute the sequential Markov Chain algorithm M
        if not async_mode: self._compress_agent_sequential(open_ports)
        # execute the asynchronous algorithm for compression
        else: self._compress_agent_async(open_ports)

    def move_agent(self, contr_to_head:bool, direction:str=None):
        r"""
        Simple (random) movement algorithm for the amoebot model.

        direction : direction of movement (one of port labeling); if no 
                    value provided, movement is performed randomly.

        returns : None
        """

        if  self.head is not self.tail:
            # contract an expanded particle to its head
            if contr_to_head:
                pull = self.tail
                self.tail = self.head
                pull.departure()
            # contract an expanded particle to its tail
            else:
                pull = self.head
                self.head = self.tail
                pull.departure()

        # expand a contracted particle
        else:
            # get all available ports in scan order
            open_ports = self.get_open_ports()

            # select a random direction when none provided
            if direction is None and open_ports: 
                direction = np.random.choice(open_ports)

            # move to indicated direction if available
            if direction in open_ports:
                push = self.head.get_neighbor(direction)
                self.head = push
                self.head.arrival(bot=self)

    def _compress_agent_sequential(self, open_ports:array): 
        raise NotImplementedError

    def _compress_agent_async(self, open_ports:array):
        r"""
        """

        if self._is_contracted:
            # choose a neigbouring location uniformly at random
            direction = np.random.choice(self.port_labels)

            # list of contracted statuses in neighbouring positions
            if self.head.neighbors[direction] is not None:
                c_nbrs = self._neighborhood_contraction_status(
                                                self.head.neighbors[direction]
                                            )

            # port is unoccupied and particle has no expanded neighbour
            if (direction in open_ports) and np.all(c_nbrs):
                self.move_agent(direction)

                # if there are no expanded particles adjacent to head/tail
                c_h_nbrs = self._neighborhood_contraction_status(self.head)
                c_t_nbrs = self._neighborhood_contraction_status(self.tail)
                if np.all(c_h_nbrs) and np.all(c_t_nbrs): 
                    # set the status flag
                    self.cflag = uint8(1)
                # unset the status flag
                else: self.cflag = uint8(0)
        else:
            q = np.random.uniform()
            e_head, e_tail = self._num_neighbors(count_exp_heads=False)
            # if compression conditions are satisfied contract to head
            if self._verify_compression_conditions(e_head, e_tail, q):
                self.move_agent(contr_to_head=True)
            # else contract back to the tail
            else: self.move_agent(contr_to_head=False)


    def _neighborhood_contraction_status(self, port:object=None) -> array:
        r""" returns a list of contracted statuses in neighbouring positions
        """
        if port is None: port = self.head
        return array([n.bot._is_contracted if n.bot is not None else True \
                                    for _, n in port.neighbors.items()])

    def _num_neighbors(self, count_exp_heads:bool=True) -> tuple:
        r"""
        """
        open_port_head = self.get_open_ports(scan_tail=False)
        # neighbouring particles of head except its own tail
        e_head = uint8(6 - len(open_port_head) - 1)

        # if particle is expaned, also scan the tail
        if not self._is_contracted:
            open_port_tail = self.get_open_ports(scan_tail=True)
            # neighbouring particles of tail except its own head
            e_tail = uint8(6 - len(open_port_tail) - 1)

            # if expanded heads are considered in the count, return
            if count_exp_heads: return e_head, e_tail

            for p in self.port_labels:
                # check occupied ports around the head, ignore contracted
                if p not in open_port_head and \
                        not self.head.neighbors[p].bot._is_contracted:
                    # subtract from `e` if neigbouring port is an expanded head
                    if np.all(self.head.neighbors[p].position == \
                              self.head.neighbors[p].bot.head.position):
                        e_head -= 1

                # also check occupied ports around the head, ignore contracted
                if p not in open_port_tail and \
                        not self.tail.neighbors[p].bot._is_contracted:
                    # subtract from `e` if neigbouring port is an expanded head
                    # except if it is the particle's own head
                    if np.all(self.tail.neighbors[p].position == \
                              self.tail.neighbors[p].bot.head.position) and \
                    np.all(self.tail.neighbors[p].position != \
                           self.head.position):
                        e_tail -= 1

            return e_head, e_tail

        return e_head
    
    def _verify_compression_conditions(
                                    self, 
                                    e_head:uint8, 
                                    e_tail:uint8, 
                                    q:float
                                ) -> bool:
        raise NotImplementedError