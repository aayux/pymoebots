import logging
import numpy as np
import multiprocessing
from collections import defaultdict
from numpy import int8, uint8, float16, array

from .core import Amoebot
from ...utils.algorithms import GraphAlgorithms

# from ..functional.nwobjects import MessagePipe, Packet, Token
# from ..functional.mesghandler import MessageHandler

class Agent(Amoebot):
    r""" all amoebot algorithms are written as member functions of class `Agent`
    """

    def __init__(self, __id:uint8, head:array, tail:array=None):
        # initialise the super class
        super().__init__(__id, head, tail)

        # does not share id with super class
        self.__id = __id

    def execute(
                self, 
                nmap:defaultdict, 
                logger=logging.RootLogger, 
                lock:object=None
            ) -> tuple:
        r"""
        Worker function for each amoebot. Intended to manage parallelisation 
        between agents and attach algorithmic modules to the amoebot.

        returns: np.uint8: execution status
        """

        # get the current process name for logging
        cpname = multiprocessing.current_process().name

        # generate a pre-execution log message
        log_message = (
                        f'pre/{cpname} :: < agent {self.__id} {self} >\n'
                        f'\t\tclock {self.clock} active {int(self.active)} '
                        f'head{self.head} tail {self.tail}.'
                    )

        # log the state information
        logging.info(log_message)

        # if the agent is active
        if self.active:

            log_message = (
                f'pre/{cpname} :: nmap {nmap}'
                f'head{self.head} tail {self.tail}.'
            )

            # run one step of an elementary algorithm
            # nmap = self.compress_agent(nmap, async_mode=True)
            nmap = self.move_agent(nmap, contr_to_tail=False)

            log_message = (
                f'pre/{cpname} :: < agent {self.__id} {self} >\n'
                f'clock {self.clock} active {int(self.active)} '
                f'head{self.head} tail {self.tail}.'
            )

            # reset the poisson clock
            self.active, self.clock = self._reset_clock(refresh=True)

            return (self, nmap)

        else:
            # decrement the clock and get active status
            self.active, self.clock = self._reset_clock(refresh=False)

            return (self, None)
    
    def compress_agent(self, nmap:defaultdict, async_mode:bool=True):
        r"""
        nmap    : ...
        async_mode  : if True, execute the local, distributed, asynchronous 
                     algorithm for compression else run sequential algorithm.
        returns : None
        """
        # execute the sequential Markov Chain algorithm M
        if not async_mode: nmap = self._compress_agent_sequential()
        # execute the asynchronous algorithm for compression
        else:
            if self._is_contracted: 
                nmap = self._compress_agent_async_contracted(nmap)
            else: nmap = self._compress_agent_async_expanded(nmap)

        return nmap

    def move_agent(
                    self, 
                    nmap:defaultdict, 
                    contr_to_tail:bool, 
                    port:uint8=None, 
                ):
        r"""
        Simple (random) movement algorithm for the amoebot model.

        contr_to_tail   :
        port            : port to move to; if no value provided, movement is 
                          performed randomly.

        returns : None
        """

        # reset head and tail orientations
        self.generate_neighbourhood_map(nmap)

        if  not self._is_contracted:
            # contract an expanded particle to its head
            if not contr_to_tail:
                pull = self.tail
                self.tail = self.head
                nmap[self.head[0]][self.head[1]].update_node_status(
                                                        action='contract to'
                                                    )
                nmap[pull[0]][pull[1]].update_node_status(
                                                        action='contract from'
                                                    )

            # contract an expanded particle to its tail
            else:
                pull = self.head
                self.head = self.tail
                nmap[pull[0]][pull[1]].update_node_status(
                                                        action='contract from'
                                                    )
                nmap[self.tail[0]][self.tail[1]].update_node_status(
                                                            action='contract to'
                                                        )

        # expand a contracted particle
        else:
            # select a random direction when none provided
            if port is None and len(self.open_ports()) > 0: 
                port = np.random.choice(self.open_ports())
            elif len(self.open_ports()) == 0: return nmap

            # move to indicated direction if available
            if port in self.open_ports():
                head_node = nmap[self.head[0]][self.head[1]]
                push = head_node.neighbors[self.labels[port]]
                self.head = push

                nmap[self.head[0]][self.head[1]].update_node_status(
                                                        action='expand to'
                                                    )
                nmap[self.tail[0]][self.tail[1]].update_node_status(
                                                        action='expand from'
                                                    )

        # reset head and tail orientations
        self.generate_neighbourhood_map(nmap)

        return nmap

    def _compress_agent_sequential(self): 
        raise NotImplementedError

    def _compress_agent_async_contracted(self, nmap:defaultdict):
        r"""
        A local, distributed, asynchronous Markov chain algorithm for 
        compression in SOPS based on 
        
        Sarah Cannon, Joshua J. Daymude, Dana Randall, and Andréa W. Richa
        A Markov chain algorithm for compressionin self-organizing particle 
        systems (2016); full text at arxiv.org/abs/1603.07991
        """

        # choose a neigbouring location uniformly at random
        port = np.random.randint(6)

        # list of contracted statuses in neighbouring positions
        c_h_nbrs = self._neighborhood_contraction_status(scan_tail=False)

        # port is unoccupied and particle has no expanded neighbours
        if (port in self.open_ports()) and np.all(c_h_nbrs):

            # reset head and tail orientations
            self.generate_neighbourhood_map(nmap)
            
            nmap = self.move_agent(nmap, contr_to_tail=False, 
                                   port=port)
            
            # reset head and tail orientations
            self.generate_neighbourhood_map(nmap)

            c_h_nbrs = self._neighborhood_contraction_status(scan_tail=False)
            c_t_nbrs = self._neighborhood_contraction_status(scan_tail=True)

            # if there are no expanded particles adjacent to head/tail
            if np.sum(c_h_nbrs) + np.sum(c_t_nbrs) == 10: 
                # set the status flag
                self.cflag = uint8(1)
            # else unset the status flag
            else: self.cflag = uint8(0)
        
        return nmap

    def _compress_agent_async_expanded(self, nmap:defaultdict):

            # TODO check if any block in neighbourhood
            # if yes, then set trace and contract

            q = np.random.uniform()

            # if compression conditions are satisfied contract to head
            if self._verify_compression_conditions(nmap, q):
                return self.move_agent(nmap, contr_to_tail=False)
            # else contract back to the tail
            else: return self.move_agent(nmap, contr_to_tail=True)

    def _neighborhood_contraction_status(self, scan_tail:bool=False) -> array:
        r""" returns a list of contraction statuses in neighbouring positions
        """
        scan = self.t_neighbor_status if scan_tail else self.h_neighbor_status
        return array([(status not in [2, 3]) for _, status in scan.items()])

    def _verify_compression_conditions(
                                        self, 
                                        nmap:defaultdict, 
                                        q:float16
                                    ) -> bool:
        r"""
        """
        # list of conditional truth values
        conditions = np.zeros(4, dtype=uint8)

        # collect neighbouring positions around head and tail
        h_neighbors, t_neighbors = [set() for _ in range(2)]

        # reset head and tail orientations
        self.generate_neighbourhood_map(nmap)

        for port, status in self.h_neighbor_status.items():
            # check occupied ports around the head ignore own tail
            if status in [1, 2]:
                head_node = nmap[self.head[0]][self.head[1]]
                n_position = head_node.neighbors[self.labels[port]]
                h_neighbors |= {n_position.tostring()}

        # also check occupied ports around the tail
        for port, status in self.t_neighbor_status.items():
            # check occupied ports around the tail ignore own head
            if status in [1, 2]:
                tail_node = nmap[self.tail[0]][self.tail[1]]
                n_position = tail_node.neighbors[self.labels[port]]
                t_neighbors |= {n_position.tostring()}

        e_head, e_tail = len(h_neighbors), len(t_neighbors)

        # does not leave behind a hole
        if e_tail != 5: conditions[0] = uint8(1)

        # satisfy property 1 or 2
        common_neighbors = h_neighbors & t_neighbors
        if len(common_neighbors) in [1, 2]: 
            conditions[1] = self._verify_compression_property1(nmap, h_neighbors, 
                                                               t_neighbors)
        elif len(common_neighbors) == 0: 
            conditions[1] = self._verify_compression_property2(nmap, h_neighbors, 
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
                                        nmap:defaultdict, 
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

        # reset head and tail orientations
        self.generate_neighbourhood_map(nmap)

        # construct a graph dictionary using the indexed lookup
        for n, ix in ix_lookup.items():
            # recover the numpy array from the byte-string
            node = np.frombuffer(n, dtype=uint8)

            # neighbors of the current node
            node_neighbors = list(nmap[node[0]][node[1]].neighbors.values())
            
            # cast as byte-strings
            node_neighbors = [_n.tostring() for _n in node_neighbors]

            # construct the graph dictionary
            G[ix] = [ix_lookup[_n] for _n in node_neighbors \
                                          if _n in neighborhood]

        graph = GraphAlgorithms(G)
        for n in common_neighbors:
            # bfs each common neighbour to find a path in the union
            connectivity += graph.bfs(root=ix_lookup[n])

        if connectivity == len(common_neighbors): return uint8(1)
        else: return uint8(0)

    def _verify_compression_property2(
                                        self, 
                                        nmap:defaultdict, 
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

        # construct a graph dictionary using the indexed lookup
        for n, ix in ix_lookup_h.items():
            # recover the numpy array from the byte-string
            node = np.frombuffer(n, dtype=uint8)

            # neighbors of the current node
            node_neighbors = list(nmap[node[0]][node[1]].neighbors.values())
            
            # cast as byte-strings
            node_neighbors = [_n.tostring() for _n in node_neighbors]

            # construct the graph dictionary
            G_h[ix] = [ix_lookup_h[_n] for _n in node_neighbors \
                                          if _n in h_neighbors]

        # reset head and tail orientations
        self.generate_neighbourhood_map(nmap)

        for n, ix in ix_lookup_t.items():
            node = np.frombuffer(n, dtype=uint8)
            node_neighbors = list(nmap[node[0]][node[1]].neighbors.values())
            node_neighbors = [_n.tostring() for _n in node_neighbors]
            G_t[ix] = [ix_lookup_t[_n] for _n in node_neighbors \
                                          if _n in t_neighbors]

        graph_h, graph_t = GraphAlgorithms(G_h), GraphAlgorithms(G_t)
        for graph in [graph_h, graph_t]:
            # dfs each subgraph and find a path connecting it
            connectivity += graph.dfs(root=0)

        if connectivity == 2: return uint8(1)
        else: return uint8(0)
