from numpy import uint8, ndarray, array
from collections import defaultdict

from .core import Node
from ..manager import Manager

class NodeManager(Manager):
    def __init__(self, points:ndarray):

        # [dictionary of dictionary] of nodes
        self.nmap:defaultdict = defaultdict(dict)

        # numpy array of plotted points
        self.grid_points:ndarray = array(points)

        # call to grid builder
        self.grid_builder()

    def grid_builder(self):
        r""" 
        create nodes at grid positions and link the nodes into a full grid
        """
        # rows and cols in the plotted points on the grid
        nrows, ncols, dim = self.grid_points.shape
        self.grid_points = self.grid_points.reshape(nrows * ncols, dim)

        # place nodes on the grid
        for point in self.grid_points:
            # add node to node manager
            self._add_node(point=point)

        # calls function to link adjacent nodes on the hexagonal grid
        self._hex_connect()

    def _add_node(self, point:array):
        r"""
        add individual nodes to node lookup
        """
        # creates node and assigns it a place in the node dictionary
        self.nmap[point[0]][point[1]] = Node(position=point)

    def _hex_connect(self):
        r"""
        """
        # iterate over the rows
        for ix in self.nmap:
            for jx in self.nmap[ix]:
                # current node
                node = self.nmap[ix][jx]

                # if data isn't already available
                if node.neighbors['n'] is None and (jx + 2) in self.nmap[ix]:
                    # update the node's neighbour to the north
                    node.neighbors['n'] = array([ix, jx + 2], dtype=uint8)

                    # update the neighbour's neighbour to the south
                    self.nmap[ix][jx + 2].neighbors['s'] = array(
                                                                    [ix, jx], 
                                                                    dtype=uint8
                                                                )

                # also ensure node is in the grid
                if node.neighbors['ne'] is None and (ix + 1) in self.nmap \
                                            and (jx + 1) in self.nmap[ix + 1]:
                    if jx + 1 in self.nmap[ix + 1]:
                        # update the node's neighbour to the north east
                        node.neighbors['ne'] = array(
                                                        [ix + 1, jx + 1], 
                                                    dtype=uint8)

                        # update the neighbour's neighbour to the south west
                        self.nmap[ix + 1][jx + 1].neighbors['sw'] = \
                                                array([ix, jx], dtype=uint8)

                if node.neighbors['se'] is None and (ix + 1) in self.nmap \
                                            and (jx - 1) in self.nmap[ix + 1]:
                        # update the node's neighbour to the south east
                        node.neighbors['se'] = array(
                                                        [ix + 1, jx - 1], 
                                                    dtype=uint8)

                        # update the neighbour's neighbour to the north west
                        self.nmap[ix + 1][jx - 1].neighbors['nw'] = \
                                                    array([ix, jx], dtype=uint8)

                if node.neighbors['s'] is None and (jx - 2) in self.nmap[ix]:
                    # update the node's neighbour to the south
                    node.neighbors['s'] = array([ix, jx - 2], dtype=uint8)

                    # update the neighbour's neighbour to the north
                    self.nmap[ix][jx - 2].neighbors['n'] = \
                                                array([ix, jx], dtype=uint8)

                if node.neighbors['sw'] is None and (ix - 1) in self.nmap \
                                        and (jx - 1) in self.nmap[ix - 1]:
                        # update the node's neighbour to the south west
                        node.neighbors['sw'] = array(
                                                        [ix - 1, jx - 1], 
                                                    dtype=uint8)

                        # update the neighbour's neighbour to the north east
                        self.nmap[ix - 1][jx - 1].neighbors['ne'] = \
                                                array([ix, jx], dtype=uint8)

                if node.neighbors['nw'] is None and (ix - 1) in self.nmap \
                                        and (jx + 1) in self.nmap[ix - 1]:
                        # update the node's neighbour to the north west
                        node.neighbors['nw'] = array(
                                                        [ix - 1, jx + 1], 
                                                    dtype=uint8)

                        # update the neighbour's neighbour to the south east
                        self.nmap[ix - 1][jx + 1].neighbors['se'] = \
                                                array([ix, jx], dtype=uint8)

                self.nmap[ix][jx] = node

    def get_node(self, position:array) -> Node: 
        return self.nmap[position[0]][position[1]]

    @property
    def get_nmap(self) -> dict: return self.nmap

    @property
    def get_num_nodes(self) -> int: 
        nrows, ncols, _ = self.grid_points.shape
        return nrows * ncols
