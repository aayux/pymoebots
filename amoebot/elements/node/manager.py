# -*- coding: utf-8 -*-

""" elements/node/manager.py
"""

from .core import Node
from ..manager import Manager

import numpy as np
from collections import defaultdict

class NodeManager(Manager):
    r"""
    Manages grid connectivity and the node map for fast lookups.
    
    Attributes

        __nmap (defaultdict) :: a dictionary of dictionaries used to index nodes
                        using x and y co-odrinates.
        grid_points (numpy.ndarray) :: "matrix" of the points on the grid.
    """

    def __init__(self, points:np.ndarray):
        r"""
        Attributes

            points (numpy.ndarray) :: list of grid points returned by 
                                `make_triangular_grid`.
        """
        # [dictionary of dictionary] of nodes
        self.__nmap:defaultdict = defaultdict(dict)

        # numpy array of plotted points
        self.grid_points:np.ndarray = np.array(points)

        # call to grid builder
        self.grid_builder()

    def grid_builder(self):
        r"""
        Create nodes at grid positions and link the nodes into a full grid.
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

    def _add_node(self, point:np.ndarray):
        r"""
        Add individual nodes to node lookup.

        Attributes:
            points (numpy.arrray) :: list containing the x and y grid 
                                co-ordinates.
        """

        # creates node and assigns it a place in the node dictionary
        self.__nmap[point[0]][point[1]] = Node(position=point)

    def _hex_connect(self):
        r"""
        Link adjacent nodes on the hexagonal grid.
        """

        # TODO dynamically optimise this function

        # iterate over the rows
        for ix in self.__nmap:
            for jx in self.__nmap[ix]:
                # current node
                node = self.__nmap[ix][jx]

                # if data isn't already available
                if node.neighbors['n'] is None and (jx + 2) in self.__nmap[ix]:
                    # link the node's neighbour to the north
                    node.set_neighbor('n', np.array([
                                                        ix, jx + 2
                                                    ], dtype=np.uint8)
                                    )

                    # back link to the current node
                    self.__nmap[ix][jx + 2].set_neighbor('s', 
                                        np.array([ix, jx], dtype=np.uint8)
                                    )

                # also ensure node is in the grid systems
                if node.neighbors['ne'] is None and (ix + 1) in self.__nmap \
                                        and (jx + 1) in self.__nmap[ix + 1]:
                    if (jx + 1) in self.__nmap[ix + 1]:
                        # link the node's neighbour to the north east
                        node.set_neighbor('ne', np.array([
                                                            ix + 1, jx + 1
                                                        ], dtype=np.uint8)
                                    )

                        # back link to the current node
                        self.__nmap[ix + 1][jx + 1].set_neighbor('sw', 
                                        np.array([ix, jx], dtype=np.uint8)
                                    )

                if node.neighbors['se'] is None and (ix + 1) in self.__nmap \
                                        and (jx - 1) in self.__nmap[ix + 1]:
                        # link the node's neighbour to the south east
                        node.set_neighbor('se', np.array([
                                                            ix + 1, jx - 1
                                                        ], dtype=np.uint8)
                                    )

                        # back link to the current node
                        self.__nmap[ix + 1][jx - 1].set_neighbor('nw', 
                                        np.array([ix, jx], dtype=np.uint8)
                                    )

                if node.neighbors['s'] is None and (jx - 2) in self.__nmap[ix]:
                    # link the node's neighbour to the south
                    node.set_neighbor('s', np.array([
                                                        ix, jx - 2
                                                    ], dtype=np.uint8)
                                    )

                    # back link to the current node
                    self.__nmap[ix][jx - 2].set_neighbor('n', 
                                        np.array([ix, jx], dtype=np.uint8)
                                    )

                if node.neighbors['sw'] is None and (ix - 1) in self.__nmap \
                                        and (jx - 1) in self.__nmap[ix - 1]:
                        # link the node's neighbour to the south west
                        node.set_neighbor('sw', np.array([
                                                            ix - 1, jx - 1
                                                        ], dtype=np.uint8)
                                    )

                        # back link to the current node
                        self.__nmap[ix - 1][jx - 1].set_neighbor('ne', 
                                        np.array([ix, jx], dtype=np.uint8)
                                    )

                if node.neighbors['nw'] is None and (ix - 1) in self.__nmap \
                                        and (jx + 1) in self.__nmap[ix - 1]:
                        # link the node's neighbour to the north west
                        node.set_neighbor('nw', np.array([
                                                            ix - 1, jx + 1
                                                        ], dtype=np.uint8)
                                    )

                        # back link to the current node
                        self.__nmap[ix - 1][jx + 1].set_neighbor('se', 
                                            np.array([ix, jx], dtype=np.uint8)
                                    )

                self.__nmap[ix][jx] = node

    def get_node(self, position:np.ndarray) -> Node: 
        r"""
        Get `Node` object at `position`.

        Atrributes:
            position (numpy.ndarray) :: list containing x and y co-ordinates of 
                            node to look up in the `__nmap` dictionary.

        Return (Node): object of class `Node` at the specified lookup 
                        `position`.
        """

        return self.__nmap[position[0]][position[1]]

    @property
    def get_nmap(self) -> dict: 
        return self.__nmap

    @property
    def get_num_nodes(self) -> int: 
        nrows, ncols, _ = self.grid_points.shape
        return nrows * ncols
