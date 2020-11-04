# -*- coding: utf-8 -*-

""" elements/bot/functional.py

A generalised functional module for basic SOPS movements and utilities.
"""

from ..core import Core
from ...utils.graphs import GraphAlgorithms

import numpy as np
from collections import defaultdict

def contract_particle(
                        agent:Core, 
                        __nmap:defaultdict, 
                        backward:bool=False
                    ) -> defaultdict:
    r"""
    Contract an expanded particle to head or tail.

    Attributes

        agent (Core) :: instance of class `Agent`
        __nmap (defaultdict) :: a dictionary of dictionaries used to index nodes 
                        using x and y co-ordinates.
        backward (bool) default: False :: contract to tail if true, else 
                        contract to head.

    Return (defaultdict): `__nmap` dictionary.
    """

    head, tail = agent.head, agent.tail

    # contract an expanded particle to its head
    if not backward:
        _tail, tail[:] = tail.copy(), head

        __nmap[head[0]][head[1]].mark_node(movement='c to')
        __nmap[_tail[0]][_tail[1]].mark_node(movement='c fr')

    # contract an expanded particle to its tail
    else:
        _head, head[:] = head.copy(), tail

        __nmap[_head[0]][_head[1]].mark_node(movement='c fr')
        __nmap[tail[0]][tail[1]].mark_node(movement='c to')

    return __nmap

def expand_particle(
                        agent:Core, 
                        __nmap:defaultdict, 
                        port:np.uint8=None
                    ) -> defaultdict:
    r"""
    Contract an expanded particle to head or tail.

    Attributes

        agent (Core) :: instance of class `Agent`
        __nmap (defaultdict) :: a dictionary of dictionaries used to index nodes 
                        using x and y co-ordinates.
        port (numpy.uint8) default: None :: port number to move to; if no 
                        value provided, choose a port at random.

    Return (defaultdict): the updated `__nmap` dictionary.
    """

    open_ports = agent.open_ports_head
    head = agent.head

    # select a random direction when none provided
    if port is None and len(open_ports) > 0:
        port = np.random.randint(6, dtype=np.uint8)

    elif len(open_ports) == 0: return __nmap

    # move to indicated direction if available
    if port in open_ports:
        head_node = __nmap[head[0]][head[1]]
        head[:] = head_node.neighbors[agent.labels[port]]
        __nmap[head[0]][head[1]].mark_node(movement='e to')

    return __nmap

def compress_agent_sequential(agent:Core, __nmap:defaultdict):
    r"""
    A centralized Markov chain algorithm for compression in SOPS based on 
    
    Sarah Cannon, Joshua J. Daymude, Dana Randall, and Andréa W. Richa
    A Markov chain algorithm for compressionin self-organizing particle 
    systems (2016); full text at arxiv.org/abs/1603.07991

    Attributes

        agent (Core) :: instance of class `Agent`
        __nmap (defaultdict) :: a dictionary of dictionaries used to index nodes 
                        using x and y co-ordinates.

    Return (defaultdict): the updated `__nmap` dictionary.
    """

    # choose a neigbouring location uniformly at random
    port = np.random.randint(6)

    # set head and tail orientations
    agent.generate_neighbourhood_map(__nmap)

    # if port is unoccupied
    if (port in agent.open_ports_head):
        # expand to occupy port
        __nmap = expand_particle(agent, __nmap, port=port)

        # reset head and tail orientations
        agent.generate_neighbourhood_map(__nmap)
    
    # if compression conditions are satisfied contract to head
    if _verify_compression_conditions(agent, __nmap, async_mode=False):
        return contract_particle(agent, __nmap, backward=False)
    
    # else contract back to the tail
    else: return contract_particle(agent, __nmap, backward=True)

def compress_agent_async_contracted(
                                    agent:Core, 
                                    __nmap:defaultdict
                                ) -> defaultdict:
    r"""
    A local, distributed, asynchronous Markov chain algorithm for 
    compression in SOPS based on 
    
    Sarah Cannon, Joshua J. Daymude, Dana Randall, and Andréa W. Richa
    A Markov chain algorithm for compressionin self-organizing particle 
    systems (2016); full text at arxiv.org/abs/1603.07991

    This function is executed by a contracted particle.

    Attributes

        agent (Core) :: instance of class `Agent`
        __nmap (defaultdict) :: a dictionary of dictionaries used to index nodes 
                        using x and y co-ordinates.

    Return (defaultdict): the updated `__nmap` dictionary.
    """

    # choose a neigbouring location uniformly at random
    port = np.random.randint(6)

    # list of contracted statuses in neighbouring positions
    c_h_nbrs = agent._neighborhood_contraction_status(scan_tail=False)

    # port is unoccupied and particle has no expanded neighbours
    if (port in agent.open_ports_head) and np.all(c_h_nbrs):

        # reset head and tail orientations
        # TODO we may need these more (or less) frequently
        agent.generate_neighbourhood_map(__nmap)

        __nmap = expand_particle(agent, __nmap, port=port)
        
        # reset head and tail orientations
        agent.generate_neighbourhood_map(__nmap)

        c_h_nbrs = agent._neighborhood_contraction_status(scan_tail=False)
        c_t_nbrs = agent._neighborhood_contraction_status(scan_tail=True)

        # if there are no expanded particles adjacent to head/tail
        if np.sum(c_h_nbrs) + np.sum(c_t_nbrs) == 10:
            # set the status flag
            return np.uint8(1), __nmap
        # else unset the status flag
        else: return np.uint8(0), __nmap

def compress_agent_async_expanded(agent:Core, __nmap:defaultdict) -> defaultdict:
    r"""
    A local, distributed, asynchronous Markov chain algorithm for 
    compression in SOPS based on 
    
    Sarah Cannon, Joshua J. Daymude, Dana Randall, and Andréa W. Richa
    A Markov chain algorithm for compressionin self-organizing particle 
    systems (2016); full text at arxiv.org/abs/1603.07991

    This function is executed by a expanded particle.

    Attributes

        agent (Core) :: instance of class `Agent`
        __nmap (defaultdict) :: a dictionary of dictionaries used to index nodes 
                        using x and y co-ordinates.

    Return (defaultdict): the updated `__nmap` dictionary.
    """

    # TODO check if any block in neighbourhood
    # if yes, then set trace and contract

    # if compression conditions are satisfied contract to head
    if _verify_compression_conditions(agent, __nmap, async_mode=True):
        return contract_particle(agent, __nmap, backward=False)
    
    # else contract back to the tail
    else: return contract_particle(agent, __nmap, backward=True)

def _verify_compression_conditions(
                                    agent:Core, 
                                    __nmap:defaultdict, 
                                    async_mode:bool=True
                                ) -> bool:
    r"""
    Verify all compression agorithm for the amoebot model based on 

    Sarah Cannon, Joshua J. Daymude, Dana Randall, and Andréa W. Richa
    A Markov chain algorithm for compressionin self-organizing particle 
    systems (2016); full text at arxiv.org/abs/1603.07991

    Attributes

        agent (Core) :: instance of class `Agent`
        __nmap (defaultdict) :: a dictionary of dictionaries used to index nodes 
                    using x and y co-ordinates.
        async_mode (bool) :: if True, execute the local, distributed, 
                    asynchronous algorithm for compression else run sequential 
                    algorithm.

    Return (bool): True if all conditions are verified, else False.
    """

    # draw a number from U[0,1]
    q = np.random.uniform()

    # list of conditional truth values
    conditions = np.zeros(4, dtype=np.uint8)

    # collect neighbouring positions around head and tail
    h_neighbors, t_neighbors = [set() for _ in range(2)]

    # reset head and tail orientations
    agent.generate_neighbourhood_map(__nmap)

    head, tail = agent.head, agent.tail

    for port, status in agent.h_neighbor_status.items():
        # check occupied ports around the head ignore own tail
        if status in [1, 2]:
            head_node = __nmap[head[0]][head[1]]
            n_position = head_node.neighbors[agent.labels[port]]
            h_neighbors |= {n_position.tostring()}

    # also check occupied ports around the tail
    for port, status in agent.t_neighbor_status.items():
        # check occupied ports around the tail ignore own head
        if status in [1, 2]:
            tail_node = __nmap[tail[0]][tail[1]]
            n_position = tail_node.neighbors[agent.labels[port]]
            t_neighbors |= {n_position.tostring()}

    e_head, e_tail = len(h_neighbors), len(t_neighbors)

    # does not leave behind a hole
    if e_tail != 5: conditions[0] = np.uint8(1)

    # satisfy property 1 or 2
    common_neighbors = h_neighbors & t_neighbors
    if len(common_neighbors) in [1, 2]: 
        conditions[1] = _verify_compression_property_1(
                                                        __nmap, 
                                                        h_neighbors, 
                                                        t_neighbors
                                                    )
    elif len(common_neighbors) == 0: 
        conditions[1] = _verify_compression_property_2(
                                                        __nmap, 
                                                        h_neighbors, 
                                                        t_neighbors
                                                    )
    else:
        raise ValueError

    # the Metropolis filter
    if q < np.exp((int(e_head) - int(e_tail)) / agent.tau0): 
        conditions[2] = np.uint8(1)

    # not a condition in async_mode
    if not async_mode: 
        conditions[3] = np.uint8(1)
    # in async_mode verify status flag is set
    elif agent.cflag:
        conditions[3] = np.uint8(1)

    return np.all(conditions)

def _verify_compression_property_1(
                                    nmap:defaultdict, 
                                    h_neighbors:set, 
                                    t_neighbors:set
                                ) -> np.uint8: 
    r"""
    |S| ∈ {1, 2} and every particle in N(ℓ ∪ ℓ′) is connected to a particle 
    in S by a path through N(ℓ ∪ ℓ′).

    Attributes

        __nmap (defaultdict) :: a dictionary of dictionaries used to index nodes 
                    using x and y co-ordinates.
       h_neighbors (set) :: coordinates of neighbouring positions around head
       t_neighbors (set) :: coordinates of neighbouring positions around head

    Return (bool): True if condition is verified, else False.
    """

    # graph dictionary
    G = dict()

    # connectivity counter for each neigbour in intersection
    connectivity = np.uint8(0)

    # entire neighbourhood of particles except heads of expanded particles
    neighborhood = h_neighbors | t_neighbors

    # neighbours in the intersection of head and tail
    common_neighbors = h_neighbors & t_neighbors

    # indexer for the neighbourhood particles
    ix_lookup = dict([(n, ix) for ix, n in enumerate(neighborhood)])

    # construct a graph dictionary using the indexed lookup
    for n, ix in ix_lookup.items():
        # recover the numpy array from the byte-string
        node = np.frombuffer(n, dtype=np.uint8)

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

    if connectivity == len(common_neighbors): return np.uint8(1)
    else: return np.uint8(0)

def _verify_compression_property_2(
                                    nmap:defaultdict, 
                                    h_neighbors:set, 
                                    t_neighbors:set
                                ) -> np.uint8:
    r"""
    |S| = 0, ℓ and ℓ′ each have at least one neighbor, all particles in 
    N(ℓ)\{ℓ′} are connected by paths within this set, and all particles in
    N(ℓ′)\{ℓ} are connected by paths within this set.

    Attributes

        __nmap (defaultdict) :: a dictionary of dictionaries used to index nodes 
                    using x and y co-ordinates.
       h_neighbors (set) :: 
       t_neighbors (set) :: 

    Return (bool): True if condition is verified, else False.
    """

    # if either has no neighbours then this is an invalid move
    if len(h_neighbors) == 0 or len(t_neighbors) == 0: return np.uint8(0)

    # graph dictionaries
    G_h, G_t = [dict() for _ in range(2)]

    # common connectivity counter for head and tail
    connectivity = np.uint8(0)

    # indexer for the neighbourhood of head and tail particles
    ix_lookup_h = dict([(n, ix) for ix, n in enumerate(h_neighbors)])
    ix_lookup_t = dict([(n, ix) for ix, n in enumerate(t_neighbors)])

    # construct a graph dictionary using the indexed lookup
    for n, ix in ix_lookup_h.items():
        # recover the numpy array from the byte-string
        node = np.frombuffer(n, dtype=np.uint8)

        # neighbors of the current node
        node_neighbors = list(nmap[node[0]][node[1]].neighbors.values())
        
        # cast as byte-strings
        node_neighbors = [_n.tostring() for _n in node_neighbors]

        # construct the graph dictionary
        G_h[ix] = [ix_lookup_h[_n] for _n in node_neighbors \
                                        if _n in h_neighbors]

    for n, ix in ix_lookup_t.items():
        node = np.frombuffer(n, dtype=np.uint8)
        node_neighbors = list(nmap[node[0]][node[1]].neighbors.values())
        node_neighbors = [_n.tostring() for _n in node_neighbors]
        G_t[ix] = [ix_lookup_t[_n] for _n in node_neighbors \
                                        if _n in t_neighbors]

    graph_h, graph_t = GraphAlgorithms(G_h), GraphAlgorithms(G_t)
    for graph in [graph_h, graph_t]:
        # dfs each subgraph and find a path connecting it
        connectivity += graph.dfs(root=0)

    if connectivity == 2: return np.uint8(1)
    else: return np.uint8(0)
