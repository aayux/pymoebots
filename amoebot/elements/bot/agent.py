import logging
import numpy as np
import multiprocessing

from numpy import uint8, float16, array

from .core import Amoebot
from ...utils.algorithms import GraphAlgorithms

# from ..functional.nwobjects import MessagePipe, Packet, Token
# from ..functional.mesghandler import MessageHandler

class Agent(Amoebot):
    r""" all amoebot algorithms are written as member functions of class `Agent`
    """

    def __init__(self, __id:int, head:object):
        # initialise the super class
        super().__init__(__id, head)

        # does not share id with super class
        self.__id = __id

    def execute(self, logger=logging.RootLogger, lock:object=None) -> tuple:
        r"""
        Worker function for each amoebot. Intended to manage parallelisation 
        between agents and attach algorithmic modules to the amoebot.

        returns: np.uint8: execution status
        """

        # get the current process name for logging
        cpname = multiprocessing.current_process().name

        # generate a pre-execution log message
        log_message = (
                        f'pre/{cpname} :: < agent {self.__id} {self} '
                        f'clock {self.clock} active {int(self.active)} >\n'
                        f'\thead {self.head} at {self.head.position}\n'
                        f'\ttail {self.tail} at {self.tail.position}.'
                    )

        # log the state information
        logging.info(log_message)


        # if the agent is active
        if self.active:

            # run one step of an elementary algorithm
            self.compress_agent(async_mode=True)
            # self.move_agent(contr_to_tail=False)

            # reset the poisson clock
            self.active, self.clock = self._reset_clock(refresh=True)

            return (self, uint8(1))

        else:
            # decrement the clock and get active status
            self.active, self.clock = self._reset_clock(refresh=False)

            return (self, uint8(0))
    
    def compress_agent(self, async_mode:bool=True):
        r"""
        async_mode : if True, execute the local, distributed, asynchronous 
                     algorithm for compression else run sequential algorithm.
        returns : None
        """
        # execute the sequential Markov Chain algorithm M
        if not async_mode: self._compress_agent_sequential()
        # execute the asynchronous algorithm for compression
        else:
            if self._is_contracted: self._compress_agent_async_contracted()
            else: self._compress_agent_async_expanded()

    def move_agent(
                    self, 
                    contr_to_tail:bool, 
                    direction:str=None, 
                ):
        r"""
        Simple (random) movement algorithm for the amoebot model.

        contr_to_tail   :
        direction       : direction of movement (one of port labeling); if no 
                        value provided, movement is performed randomly.

        returns : None
        """

        if  not self._is_contracted:
            # contract an expanded particle to its head
            if not contr_to_tail:
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
            # select a random direction when none provided
            if direction is None and len(self.get_open_ports()) > 0: 
                direction = np.random.choice(self.get_open_ports())
            elif len(self.get_open_ports()) == 0: return

            # move to indicated direction if available
            if direction in self.get_open_ports():
                push = self.head.get_neighbor(direction)
                self.head = push
                self.head.arrival(bot=self)

    def _compress_agent_sequential(self): 
        raise NotImplementedError

    def _compress_agent_async_contracted(self):
        r"""
        A local, distributed, asynchronous Markov chain algorithm for 
        compression in SOPS based on 
        
        Sarah Cannon, Joshua J. Daymude, Dana Randall, and Andréa W. Richa
        A Markov chain algorithm for compressionin self-organizing particle 
        systems (2016); full text at arxiv.org/abs/1603.07991
        """

        # choose a neigbouring location uniformly at random
        direction = np.random.choice(self.port_labels)

        # list of contracted statuses in neighbouring positions
        c_h_nbrs = self._neighborhood_contraction_status(self.head)

        # port is unoccupied and particle has no expanded neighbours
        if (direction in self.get_open_ports()) and np.all(c_h_nbrs):
            self.move_agent(contr_to_tail=False, direction=direction)

            # if there are no expanded particles adjacent to head/tail
            c_h_nbrs = self._neighborhood_contraction_status(self.head)
            c_t_nbrs = self._neighborhood_contraction_status(self.tail)

            # if there are no expanded neighbours
            if np.sum(c_h_nbrs) + np.sum(c_t_nbrs) == 10: 
                # set the status flag
                self.cflag = uint8(1)
            # else unset the status flag
            else: self.cflag = uint8(0)

    def _compress_agent_async_expanded(self):

            # TODO check if any block in neighbourhood
            # if yes, then place marker and contract

            q = np.random.uniform()

            # if compression conditions are satisfied contract to head
            if self._verify_compression_conditions(q):
                self.move_agent(contr_to_tail=False)
            # else contract back to the tail
            else: self.move_agent(contr_to_tail=True)


    def _neighborhood_contraction_status(self, port:object=None) -> array:
        r""" returns a list of contracted statuses in neighbouring positions
        """
        if port is None: port = self.head
        return array([n.bot._is_contracted if n.bot is not None else True \
                                    for _, n in port.neighbors.items()])

    def _verify_compression_conditions(self, q:float16) -> bool:
        r"""
        """
        # list of conditional truth values
        conditions = np.zeros(4, dtype=uint8)

        # collect neighbouring particles around head and tail
        h_neighbors, t_neighbors = [set() for _ in range(2)]

        for p in self.port_labels:
            # check occupied ports around the head
            if p not in self._open_port_head:
                # ignore any heads of expanded neighbours and own tail
                if not self.head.neighbors[p].bot._is_contracted:
                    if not (self.head.neighbors[p] is \
                            self.head.neighbors[p].bot.head) and \
                    not (self.head.neighbors[p] is self.tail.position):
                        h_neighbors |= {self.head.neighbors[p]}
                else: 
                    h_neighbors |= {self.head.neighbors[p]}

            # also check occupied ports around the tail
            if p not in self._open_port_tail:
                # ignore any heads of expanded neighbours
                if not self.tail.neighbors[p].bot._is_contracted:
                    if not (self.tail.neighbors[p] is \
                            self.tail.neighbors[p].bot.head) and \
                    not (self.tail.neighbors[p] is self.head.position):
                        t_neighbors |= {self.tail.neighbors[p]}
                else: t_neighbors |= {self.tail.neighbors[p]}

        e_head, e_tail = len(h_neighbors), len(t_neighbors)

        # does not leave behind a hole
        if e_tail != 5: conditions[0] = uint8(1)

        # satisfy property 1 or 2
        common_neighbors = h_neighbors.intersection(t_neighbors)
        if len(common_neighbors) in [1, 2]: 
            conditions[1] = self._verify_compression_property1(h_neighbors, 
                                                               t_neighbors)
        elif len(common_neighbors) == 0: 
            conditions[1] = self._verify_compression_property2(h_neighbors, 
                                                               t_neighbors)
        else:
            raise ValueError

        # the Metropolis filter
        if q < self.lam ** (int(e_head) - int(e_tail)): conditions[2] = uint8(1)

        # verify status flag is set
        if self.cflag: conditions[3] = uint8(1)

        return np.all(conditions)

    def _verify_compression_property1(
                                        self, 
                                        h_neighbors:set, 
                                        t_neighbors:set
                                    ) -> uint8: 
        r"""
        |S| ∈ {1, 2} and every particle in N(ℓ ∪ ℓ′) is connected to a particle 
        in S by a path through N(ℓ ∪ ℓ′).
        """

        # graph dictionary
        G = dict()

        # connectivity counter for each neigbour in intersection
        connectivity = uint8(0)

        # entire neighbourhood of particles except heads of expanded particles
        neighborhood = h_neighbors | t_neighbors

        # neighbours in the intersection of head and tail
        common_neighbors = h_neighbors & t_neighbors

        # indexer for the neighbourhood particles
        ix_lookup = dict([(n, ix) for ix, n in enumerate(neighborhood)])

        # construct a graph dictionary using the indexed lookup
        for n, ix in ix_lookup.items():
            G[ix] = [ix_lookup[_n] for _n in n.bot.tail.neighbors.values() \
                                        if _n in neighborhood]

        graph = GraphAlgorithms(G)
        for n in common_neighbors:
            # bfs each common neighbour to find a path in the union
            connectivity += graph.bfs(root=ix_lookup[n])

        if connectivity == len(common_neighbors): return uint8(1)
        else: return uint8(0)

    def _verify_compression_property2(
                                        self, 
                                        h_neighbors:set, 
                                        t_neighbors:set
                                    ) -> uint8:
        r"""
        |S| = 0, ℓ and ℓ′ each have at least one neighbor, all particles in 
        N(ℓ)\{ℓ′} are connected by paths within this set, and all particles in
        N(ℓ′)\{ℓ} are connected by paths within this set.
        """

        # if either has no neighbours then this is an invalid move
        if len(h_neighbors) == 0 or len(t_neighbors) == 0: return uint8(0)

        # graph dictionaries
        G_h, G_t = [dict() for _ in range(2)]

        # common connectivity counter for head and tail
        connectivity = uint8(0)

        # indexer for the neighbourhood of head and tail particles
        ix_lookup_h = dict([(n, ix) for ix, n in enumerate(h_neighbors)])
        ix_lookup_t = dict([(n, ix) for ix, n in enumerate(t_neighbors)])

        # construct graph dictionaries using the indexed lookup
        for n, ix in ix_lookup_h.items():
            G_h[ix] = [ix_lookup_h[_n] for _n in n.bot.tail.neighbors.values() \
                                            if _n in h_neighbors]

        for n, ix in ix_lookup_t.items():
            G_t[ix] = [ix_lookup_t[_n] for _n in n.bot.tail.neighbors.values() \
                                            if _n in t_neighbors]


        graph_h, graph_t = GraphAlgorithms(G_h), GraphAlgorithms(G_t)
        for graph in [graph_h, graph_t]:
            # dfs each subgraph and find a path connecting it
            connectivity += graph.dfs(root=0)

        if connectivity == 2: return uint8(1)
        else: return uint8(0)
