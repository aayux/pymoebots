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

    def __init__(self, graph_dict: dict):
        r"""
        Attributes
            graph_dict (dict) :: 
        """

        self.graph_dict = graph_dict

    def bfs(self, root: int) -> np.uint8:
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

        return visited

    def dfs(self, root: int) -> np.uint8:
        r"""
        Attributes
            root (int) :: 

        """
        graph_dict = self.graph_dict
        visited = {k: 0 for k in graph_dict}
        stack = [root]
        visited[root] = 1

        while stack:
            v = stack.pop()
            for u in graph_dict[v]:
                if not visited[u]:
                    visited[u] = 1
                    stack.append(u)
        return visited

