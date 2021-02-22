# -*- coding: utf-8 -*-

""" elements/node/core.py
"""

from ..core import Core

import numpy as np

class Node(Core):
    r"""
    Manages grid connectivity and the node map for fast lookups.
    
    Attributes

        position  (numpy.ndarray) :: position of node in relation to the grid.
        ports  (numpy.ndarray) :: ports labellings of the node.
        neighbors (dict) :: dictionary identifying neighbouring port locations.
        occupied  (numpy.uint8)::  occupancy status of the current node

                        0 : node is unoccupied, 
                        1 : occupied by a contracted bot (or expanded tail), 
                        2 : occupied by head, 
                        3 : trace particle on node, 
                        4 : node is a wall.
    """

    def __init__(self, position:np.ndarray, wall:bool=False):
        r"""
        Attributes

            position (numpy.ndarray) :: position of node in relation to the grid
                            specified using x and y co-ordinates on the 
                            hexagonal grid system.
            wall (bool) default: False :: set to True if the node object is 
                            blocking, False otherwise.
        """

        # position of node in relation to the grid
        self.position:np.ndarray = position

        # ports labellings of the node
        self.ports:np.ndarray = np.array([
                                            'n', 'ne', 'se', 's', 'sw', 'nw'
                                        ], dtype='<U2')

        # dictionary identifying neighbouring port locations
        self.neighbors:dict = dict(n=None, ne=None, se=None, 
                                   s=None, sw=None, nw=None)

        # occupancy status of the current node
        self.occupied:np.uint8 = np.uint8(4) if wall else np.uint8(0)

    def place_particle(self, particle:str):
        r""" 
        Place particle (amoebot) on the node and mark the node occupancy status 
        during initialisation.

        Attributes

            particle (str) :: part of the particle on the node; accepts one of 
                            "body" or "head".
        """

        particle_map = dict([
                            ('body', np.uint8(1)), 
                            ('head', np.uint8(2))
                        ])

        assert particle in particle_map, \
            LookupError(
                f'invalid particle {particle}'
            )

        self.occupied = particle_map[particle]

    def mark_node(self, movement:str):
        r""" 
        Mark or update the node occupancy status during amoebot activity.

        Attributes

            movement (str) :: the type of movement that will mark node 
                            occupancy, one of

                            "e to" : (expand to the current node), 
                            "c to" : (contract to the current node), 
                            "c fr" : (contract from the current node).
        """

        movement_map = dict([ 
                            ('e to', np.uint8(2)), 
                            ('c to', np.uint8(1)), 
                            ('c fr', np.uint8(0)), 
                        ])

        assert movement in movement_map, \
            LookupError(
                f'invalid action {movement}'
            )
        
        self.occupied = movement_map[movement]
    
    def drop_trace(self):
        r""" 
        drop a trace particle on the inner boundary of a wall
        """
        self.occupied = np.uint8(3)

    def set_neighbor(self, port:str, node_position:np.ndarray):
        r""" 
        Assign a neighbouring node to port.

        Attributes
            port (str) :: port label to assign neighbour to.
        """
        self.neighbors[port] = node_position

    def get_neighbor(self, port:str) -> np.ndarray: 
        r""" 
        Assign a neighbouring node to port.

        Attributes
            port (str) :: port label to assign neighbour to.
        """
        return self.neighbors[port]

    @property
    def get_occupancy_status(self) -> np.uint8: 
        return self.occupied

    @property
    def get_all_ports(self) -> np.ndarray: 
        return self.ports

    @property
    def is_occupied(self) -> bool:
        return np.uint8(1) if self.occupied != 0 else np.uint8(0)

    @property
    def is_trace(self) -> bool:
        return np.uint8(1) if self.occupied == 2 else np.uint8(0)

    @property
    def is_wall(self) -> bool:
        return np.uint8(1) if self.occupied == 3 else np.uint8(0)

