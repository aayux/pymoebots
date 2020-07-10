import collections
import numpy as np

from numpy import uint8

class GraphAlgorithms(object):
    r"""
    """

    def __init__(self, graph_dict:dict):
        self.graph_dict = graph_dict

    def bfs(self, root:int) -> uint8:
        r"""
        """

        visited = np.zeros_like(self.graph_dict, dtype=uint8)
        queue = collections.deque([root])
        visited[root] = uint8(1)

        while queue:

            # dequeue a vertex from queue
            v = queue.popleft()

            # mark visited and enqueue
            for u in self.graph_dict[v]:
                if u not in visited:
                    visited[u] = uint8(1)
                    queue.append(u)

        if np.all(visited): return uint8(1)
        return uint8(0)

    def dfs(self, root:int) -> uint8:
        r"""
        """

        visited = np.zeros_like(self.graph_dict, dtype=uint8)
        stack = collections.deque([root])
        visited[root] = uint8(1)

        while stack:

            # pop a vertex from stack
            v = stack.pop()

            # mark visited and add to stack
            for u in self.graph_dict[v]:
                if u not in visited:
                    visited[u] = uint8(1)
                    stack.append(u)

        if np.all(visited): return uint8(1)
        return uint8(0)