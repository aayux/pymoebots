import numpy as np
from numpy import uint8, array

from .core import Amoebot
from ..utils.graphalg import GraphAlgorithms

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
        A local, distributed, asynchronous Markov chain algorithm for 
        compression in SOPS based on 
        
        Sarah Cannon, Joshua J. Daymude, Dana Randall, and Andréa W. Richa
        A Markov chain algorithm for compressionin self-organizing particle 
        systems (2016); available arxiv.org/abs/1603.07991
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
        # neighbouring particles of head except its own tail
        e_head = uint8(6 - len(self._open_port_head) - 1)

        # if particle is expaned, also scan the tail
        if not self._is_contracted:
            # neighbouring particles of tail except its own head
            e_tail = uint8(6 - len(self._open_port_tail) - 1)

            # if expanded heads are considered in the count, return
            if count_exp_heads: return e_head, e_tail

            for p in self.port_labels:
                # check occupied ports around the head, ignore contracted
                if p not in self._open_port_head and \
                        not self.head.neighbors[p].bot._is_contracted:
                    # subtract from `e` if neigbouring port is an expanded head
                    if np.all(self.head.neighbors[p].position == \
                              self.head.neighbors[p].bot.head.position):
                        e_head -= 1

                # also check occupied ports around the head, ignore contracted
                if p not in self._open_port_tail and \
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
        conditions = np.zeros(4, dtype=uint8)

        # does not leave behind a hole
        if e_head != 5: conditions[0] = uint8(1)

        # property 1 or 2 is satisfied
        h_neighbors, t_neighbors = [set() for _ in range(2)]

        for p in self.port_labels:
            # check occupied ports around the head
            if p not in self._open_port_head:
                # ignore any heads of expanded neighbours and own tail
                if not np.all(self.head.neighbors[p].position == \
                              self.head.neighbors[p].bot.head.position) and \
                np.all(self.head.neighbors[p].position != self.tail.position):
                    h_neighbors.append(self.head.neighbors[p])

            # also check occupied ports around the tail
            if p not in self._open_port_tail:
                # ignore any heads of expanded neighbours
                if not np.all(self.tail.neighbors[p].position == \
                              self.tail.neighbors[p].bot.head.position) and \
                np.all(self.tail.neighbors[p].position != self.head.position):
                    t_neighbors.append(self.tail.neighbors[p])

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
        if q < self.lam ** (e_head - e_tail): conditions[2] = uint8(1)

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

        # neighbourhood of particles except heads of expanded particles
        neighborhood = h_neighbors.union(t_neighbors)

        # neighbours in the intersection of head and tail
        common_neighbors = h_neighbors.intersection(t_neighbors)

        # indexer for the neighbourhood particles
        ix_lookup = [dict(n, ix) for ix, n in enumerate(neighborhood)]

        # construct a graph dictionary using the indexed lookup
        for n, ix in ix_lookup.items():
            G[ix] = [ix_lookup[_n] for _n in n.tail.neighbors.values() \
                                        if _n in ix_lookup.keys()]

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
        ix_lookup_h = [dict(n, ix) for ix, n in enumerate(h_neighbors)]
        ix_lookup_t = [dict(n, ix) for ix, n in enumerate(t_neighbors)]

        # construct graph dictionaries using the indexed lookup
        for n, ix in ix_lookup_h.items():
            G_h[ix] = [ix_lookup_h[_n] for _n in n.tail.neighbors.values() \
                                            if _n in ix_lookup_h.keys()]

        for n, ix in ix_lookup_t.items():
            G_t[ix] = [ix_lookup_t[_n] for _n in n.tail.neighbors.values() \
                                            if _n in ix_lookup_t.keys()]


        graph_h, graph_t = GraphAlgorithms(G_h), GraphAlgorithms(G_t)
        for graph in [graph_h, graph_t]:
            # dfs each subgraph and find a path connecting it
            connectivity += graph.dfs(root=0)

        if connectivity == 2: return uint8(1)
        else: return uint8(0)
