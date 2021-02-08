# -*- coding: utf-8 -*-

""" elements/bot/functional.py

A generalised functional module for basic SOPS movements and utilities.
"""

from ..core import Core
from ..nodenv import NodeEnvManager
from ...utils.graphs import GraphAlgorithms

import numpy as np
from collections import defaultdict


def compress_agent_sequential(
                                agent:Core, 
                                __node_array:np.ndarray, 
                                __id:int=None
                            ) -> np.ndarray:
    r"""
    A centralized Markov chain algorithm for compression in SOPS based on 
    
    Sarah Cannon, Joshua J. Daymude, Dana Randall, and Andréa W. Richa
    A Markov chain algorithm for compressionin self-organizing particle 
    systems (2016); full text at arxiv.org/abs/1603.07991

    Attributes

        agent (Core) :: instance of class `Agent`
        __node_array (numpy.ndarray) ::
        __id (int) :: (is accessible through agent, but explicit sharing is advised)

    Return (numpy.ndarray): 
    """

    nenvm = NodeEnvManager(_bot_id=__id, node_array=__node_array)
    h_open_ports, _ = nenvm._get_open_ports()

    # choose a neigbouring location uniformly at random
    port = np.random.randint(6)

    if port in h_open_ports:
        __node_array = nenvm._expand_to(port=port)
        agent.head, agent.tail = nenvm._get_current_node_position()

    # return if the particle did not expand
    if np.all(agent.head == agent.tail): return __node_array

    # if compression conditions are satisfied contract to head
    if _verify_compression_conditions(agent, nenvm, async_mode=False):
        nenvm._contract_forward()
    # else contract back to the tail
    else: nenvm._contract_backward()

    agent.head, agent.tail = nenvm._get_current_node_position()

    __node_array = nenvm.node_array

    # mark object for garbage collection
    del nenvm

    return __node_array


def compress_agent_async_contracted(agent:Core):
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

    raise NotImplementedError


def compress_agent_async_expanded(agent:Core):
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

    raise NotImplementedError


def _verify_compression_conditions(
                                    agent:Core, 
                                    nenvm:NodeEnvManager, 
                                    async_mode:bool=True
                                ) -> bool:
    r"""
    Verify all compression agorithm for the amoebot model based on 

    Sarah Cannon, Joshua J. Daymude, Dana Randall, and Andréa W. Richa
    A Markov chain algorithm for compressionin self-organizing particle 
    systems (2016); full text at arxiv.org/abs/1603.07991

    Attributes

        agent (Core) :: instance of class `Agent`
        nenvm (NodeEnvManager) :: 
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
    h_neighbors, t_neighbors = nenvm._get_occupied_neighbors()

    # number of edges formed by head and tail particles
    e_head, e_tail = len(h_neighbors), len(t_neighbors)

    # does not leave behind a hole
    if e_tail != 5: conditions[0] = np.uint8(1)

    # satisfy property 1 or 2
    common_neighbors = h_neighbors & t_neighbors
    assert len(common_neighbors) in [0, 1, 2], ValueError

    if len(common_neighbors) in [1, 2]:
        conditions[1] = _verify_compression_property_1(
                                                        nenvm, 
                                                        h_neighbors, 
                                                        t_neighbors
                                                    )
    elif len(common_neighbors) == 0:
        conditions[1] = _verify_compression_property_2(
                                                        nenvm,
                                                        h_neighbors,
                                                        t_neighbors
                                                    )

    # the Metropolis filter
    if q < np.exp((e_head - e_tail) / agent.tau0):
        conditions[2] = np.uint8(1)

    # not a condition in async_mode
    if not async_mode: conditions[3] = np.uint8(1)
    # in async_mode verify status flag is set
    elif agent.cflag: conditions[3] = np.uint8(1)

    return np.all(conditions)


def _verify_compression_property_1(
                                    nenvm:NodeEnvManager, 
                                    h_neighbors: set,
                                    t_neighbors: set
                                ) -> np.uint8:
    r"""
    |S| ∈ {1, 2} and every particle in N(ℓ ∪ ℓ′) is connected to a particle 
    in S by a path through N(ℓ ∪ ℓ′).

    Attributes

       nenvm (NodeEnvManager) :: 
       h_neighbors (set) :: coordinates of neighbouring positions around head.
       t_neighbors (set) :: coordinates of neighbouring positions around tail.

    Return (bool): True if condition is verified, else False.
    """

    # graph dictionary
    G = dict()

    # entire neighbourhood of particles except heads of expanded particles
    neighborhood = h_neighbors | t_neighbors

    # neighbours in the intersection of head and tail
    common_neighbors = h_neighbors & t_neighbors

    # Grabs occupied neighbors of neighboring nodes
    for neighbor_ix in neighborhood:
        node_neighbors_set = nenvm._get_occ_neighbors_at_ix(neighbor_ix.item())
        G[neighbor_ix] = {jx for jx in node_neighbors_set if jx in neighborhood}

    # an dict to store visited status for each neighbour
    connectivity = {k: 0 for k in G}

    graph = GraphAlgorithms(G)
    for n in common_neighbors:
        traversal = graph.dfs(n)
        for k, v in traversal.items():
            if v: connectivity[k] = 1

    return np.uint8(all(connectivity.values()))

def _verify_compression_property_2(
                                    nenvm:NodeEnvManager, 
                                    h_neighbors: set,
                                    t_neighbors: set
                                ) -> np.uint8:
    r"""
    |S| = 0, ℓ and ℓ′ each have at least one neighbor, all particles in 
    N(ℓ)\{ℓ′} are connected by paths within this set, and all particles in
    N(ℓ′)\{ℓ} are connected by paths within this set.

    Attributes

        nenvm (NodeEnvManager) ::
       h_neighbors (set) :: coordinates of neighbouring positions around head.
       t_neighbors (set) :: coordinates of neighbouring positions around tail.

    Return (bool): True if condition is verified, else False.
    """

    # if either has no neighbours then this is an invalid move
    if len(h_neighbors) == 0 or len(t_neighbors) == 0: return np.uint8(0)

    # graph dictionaries
    G_h, G_t = [dict() for _ in range(2)]

    for h_neighbor_ix in h_neighbors:
        h_neighbors_set = nenvm._get_occ_neighbors_at_ix(h_neighbor_ix.item())
        G_h[h_neighbor_ix] = {jx for jx in h_neighbors_set if jx in h_neighbors}
    
    for t_neighbor_ix in t_neighbors:
        t_neighbors_set = nenvm._get_occ_neighbors_at_ix(t_neighbor_ix.item())
        G_t[t_neighbor_ix] = {jx for jx in t_neighbors_set if jx in t_neighbors}

    connectivity_count = 0
    connectivity = [{k: 0 for k in G_h}, {k: 0 for k in G_t}]
    for ix, graph in enumerate([GraphAlgorithms(G_h), GraphAlgorithms(G_t)]):
        # dfs each subgraph and find a path connecting it
        traversal = graph.dfs(root=list(graph.graph_dict.keys())[0])

        for k,v in traversal.items():
            if v: connectivity[ix][k] = 1

        connectivity_count += np.uint8(all(connectivity[ix].values()))

    if connectivity_count == 2: return np.uint8(1)

    return np.uint8(0)


if __name__ == '__main__': pass
