import collections
import numpy as np
from numpy import uint8

from .exceptions import ShapeError

def two_dim_binary_search(data:list, key:object, lo:int=0, hi:int=None) -> int:
    dim_l, dim_w = data.shape
    if hi is None: hi = dim_l - 1

    assert dim_w == len(key) == 2, \
        ShapeError(
            f"`data` has width {dim_w} but `key` is of length {len(key)}"
        )

    while lo < hi:
        md = (lo + hi) // 2
        search = data[md].tolist()
        # check first dimension
        if search[0] < key[0]:
            lo = md + 1
        elif search[0] > key[0]: 
            hi = md
        # if first dimensions are equal, check next
        elif search[1] < key[1]:
            lo = md + 1
        elif search[1] > key[1]: 
            hi = md
        else:
            return md

    return -1

class GraphAlgorithms(object):
    r"""
    """

    def __init__(self, graph_dict:dict):
        self.graph_dict = graph_dict

    def bfs(self, root:int) -> uint8:
        r"""
        """

        visited = np.zeros(len(self.graph_dict), dtype=uint8)
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

        visited = np.zeros(len(self.graph_dict), dtype=uint8)
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