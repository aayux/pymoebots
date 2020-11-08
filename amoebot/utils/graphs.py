# -*- coding: utf-8 -*-

""" utils/graphs.py
"""

from .exceptions import ShapeError

import collections
import numpy as np

class GraphAlgorithms(object):
    r"""
    Attributes
        graph_dict (dict) :: 
    """

    def __init__(self, graph_dict:dict):
        r"""
        Attributes
            graph_dict (dict) :: 
        """

        self.graph_dict = graph_dict

    def bfs(self, root:int) -> np.uint8:
        r"""
        Attributes
            root (int) :: 
        """

        visited = np.zeros(len(self.graph_dict), dtype=np.uint8)
        queue = collections.deque([root])
        visited[root] = np.uint8(1)

        while queue:

            # dequeue a vertex from queue
            v = queue.popleft()

            # mark visited and enqueue
            for u in self.graph_dict[v]:
                if visited[u] != np.uint8(1):
                    visited[u] = np.uint8(1)
                    queue.append(u)

        if np.all(visited): return np.uint8(1)
        return np.uint8(0)

    def dfs(self, root:int) -> np.uint8:
        r"""
        Attributes
            root (int) :: 

        """

        visited = np.zeros(len(self.graph_dict), dtype=np.uint8)
        stack = collections.deque([root])
        visited[root] = np.uint8(1)

        while stack:

            # pop a vertex from stack
            v = stack.pop()

            # mark visited and add to stack
            for u in self.graph_dict[v]:
                if visited[u] != np.uint8(1):
                    visited[u] = np.uint8(1)
                    stack.append(u)

        if np.all(visited): return np.uint8(1)
        return np.uint8(0)