# -*- coding: utf-8 -*-

""" elements/node/core.py
"""

from numpy import ndarray, uint8, uint16, uint32, uint64
from typing import Union

UNSIGNED_INT = Union[uint8, uint16, uint32, uint64]

# from ..core import Core
#
# import numpy as np
#
# class Node(Core):
#     r"""
#     Manages grid connectivity and the node map for fast lookups.
#
#     Attributes
#
#         position  (numpy.ndarray) :: position of node in relation to the grid.
#         ports  (numpy.ndarray) :: ports labellings of the node.
#         neighbors (dict) :: dictionary identifying neighbouring port locations.
#         occupied  (numpy.uint8)::  occupancy status of the current node
#
#                         0 : node is unoccupied,
#                         1 : occupied by a contracted bot (or expanded tail),
#                         2 : occupied by head,
#                         3 : trace particle on node,
#                         4 : node is a wall.
#     """
#
#     def __init__(self, position:np.ndarray, wall:bool=False):
#         r"""
#         Attributes
#
#             position (numpy.ndarray) :: position of node in relation to the grid
#                             specified using x and y co-ordinates on the
#                             hexagonal grid system.
#             wall (bool) default: False :: set to True if the node object is
#                             blocking, False otherwise.
#         """
#
#         # position of node in relation to the grid
#         self.position:np.ndarray = position
#
#         # ports labellings of the node
#         self.ports:np.ndarray = np.array([
#                                             'n', 'ne', 'se', 's', 'sw', 'nw'
#                                         ], dtype='<U2')
#
#         # dictionary identifying neighbouring port locations
#         self.neighbors:dict = dict(n=None, ne=None, se=None,
#                                    s=None, sw=None, nw=None)
#
#         # occupancy status of the current node
#         self.occupied:np.uint8 = np.uint8(4) if wall else np.uint8(0)
#
#     def place_particle(self, particle:str):
#         r"""
#         Place particle (amoebot) on the node and mark the node occupancy status
#         during initialisation.
#
#         Attributes
#
#             particle (str) :: part of the particle on the node; accepts one of
#                             "body" or "head".
#         """
#
#         particle_map = dict([
#                             ('body', np.uint8(1)),
#                             ('head', np.uint8(2))
#                         ])
#
#         assert particle in particle_map, \
#             LookupError(
#                 f'invalid particle {particle}'
#             )
#
#         self.occupied = particle_map[particle]
#
#     def mark_node(self, movement:str):
#         r"""
#         Mark or update the node occupancy status during amoebot activity.
#
#         Attributes
#
#             movement (str) :: the type of movement that will mark node
#                             occupancy, one of
#
#                             "e to" : (expand to the current node),
#                             "c to" : (contract to the current node),
#                             "c fr" : (contract from the current node).
#         """
#
#         movement_map = dict([
#                             ('e to', np.uint8(2)),
#                             ('c to', np.uint8(1)),
#                             ('c fr', np.uint8(0)),
#                         ])
#
#         assert movement in movement_map, \
#             LookupError(
#                 f'invalid action {movement}'
#             )
#
#         self.occupied = movement_map[movement]
#
#     def drop_trace(self):
#         r"""
#         drop a trace particle on the inner boundary of a wall
#         """
#         self.occupied = np.uint8(3)
#
#     def set_neighbor(self, port:str, node_position:np.ndarray):
#         r"""
#         Assign a neighbouring node to port.
#
#         Attributes
#             port (str) :: port label to assign neighbour to.
#         """
#         self.neighbors[port] = node_position
#
#     def get_neighbor(self, port:str) -> np.ndarray:
#         r"""
#         Assign a neighbouring node to port.
#
#         Attributes
#             port (str) :: port label to assign neighbour to.
#         """
#         return self.neighbors[port]
#
#     @property
#     def get_occupancy_status(self) -> np.uint8:
#         return self.occupied
#
#     @property
#     def get_all_ports(self) -> np.ndarray:
#         return self.ports
#
#     @property
#     def is_occupied(self) -> bool:
#         return np.uint8(1) if self.occupied != 0 else np.uint8(0)
#
#     @property
#     def is_trace(self) -> bool:
#         return np.uint8(1) if self.occupied == 2 else np.uint8(0)
#
#     @property
#     def is_wall(self) -> bool:
#         return np.uint8(1) if self.occupied == 3 else np.uint8(0)

class Node:
    __slots__ = [
        '__node_data',
        '__enabled_type',
        '__x',
        '__y',
        '__occupied',
        '__bot_id',
        '__neighbor_0_index',
        '__neighbor_1_index',
        '__neighbor_2_index',
        '__neighbor_3_index',
        '__neighbor_4_index',
        '__neighbor_5_index',
        '__signal_0',
        '__signal_1',
        '__signal_2',
        '__signal_3',
        '__signal_4',
        '__signal_5',
        '__bot_contraction_status',
    ]

    def __init__(self, node_data: ndarray):

        self.__node_data = node_data

        self.__enabled_type = node_data[0, 0]
        self.__x = node_data[1, 0]
        self.__y = node_data[2, 0]
        self.__occupied = node_data[3, 0]
        self.__bot_id = node_data[4, 0]
        self.__neighbor_0_index = node_data[5, 0]
        self.__neighbor_1_index = node_data[6, 0]
        self.__neighbor_2_index = node_data[7, 0]
        self.__neighbor_3_index = node_data[8, 0]
        self.__neighbor_4_index = node_data[9, 0]
        self.__neighbor_5_index = node_data[10, 0]
        self.__signal_0 = node_data[11, 0]
        self.__signal_1 = node_data[12, 0]
        self.__signal_2 = node_data[13, 0]
        self.__signal_3 = node_data[14, 0]
        self.__signal_4 = node_data[15, 0]
        self.__signal_5 = node_data[16, 0]
        self.__bot_contraction_status = node_data[17, 0]

    @property
    def occupied(self):
        return self.__occupied

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def bot_id(self):
        return self.__bot_id

    @bot_id.setter
    def bot_id(self, value: UNSIGNED_INT):
        self.__toggle_occupied()
        self.__node_data[4, 0] = value
        self.__occupied = value

    def get_neighbor_index(self, port):
        if port == uint8(0):
            return self.__neighbor_0_index
        if port == uint8(1):
            return self.__neighbor_1_index
        if port == uint8(2):
            return self.__neighbor_2_index
        if port == uint8(3):
            return self.__neighbor_3_index
        if port == uint8(4):
            return self.__neighbor_4_index
        if port == uint8(5):
            return self.__neighbor_5_index
        raise Exception("Invalid port")

    def get_point(self):
        return self.__x, self.__y

    def get_all_neighbor_indices(self):
        return [
            self.__neighbor_0_index,
            self.__neighbor_1_index,
            self.__neighbor_2_index,
            self.__neighbor_3_index,
            self.__neighbor_4_index,
            self.__neighbor_5_index,
        ]

    def get_signal_status(self, port):
        if port == uint8(0):
            return self.__signal_0
        if port == uint8(1):
            return self.__signal_1
        if port == uint8(2):
            return self.__signal_2
        if port == uint8(3):
            return self.__signal_3
        if port == uint8(4):
            return self.__signal_4
        if port == uint8(5):
            return self.__signal_5
        raise Exception("Invalid port")

    def is_node(self):
        return uint8(1) if self.__enabled_type == 1 else uint8(0)

    def is_wall(self):
        return uint8(1) if self.__enabled_type == 2 else uint8(0)

    def set_signal_on_port(self, value, port):
        if port == 0:
            self.__node_data[11, 0] = value
            self.__signal_0 = value
        elif port == 1:
            self.__node_data[12, 0] = value
            self.__signal_1 = value
        elif port == 2:
            self.__node_data[13, 0] = value
            self.__signal_2 = value
        elif port == 3:
            self.__node_data[14, 0] = value
            self.__signal_3 = value
        elif port == 4:
            self.__node_data[15, 0] = value
            self.__signal_4 = value
        elif port == 5:
            self.__node_data[16, 0] = value
            self.__signal_5 = value

    def toggle_contracted_on_node(self):
        contracted = uint8(3)
        if self.__bot_contraction_status == contracted and self.__occupied:
            raise Exception("Bot is already contracted")
        elif self.__occupied == 0:
            raise Exception("There is no bot on this node")
        self.__node_data[17, 0] = contracted
        self.__bot_contraction_status = contracted

    def toggle_head_on_node(self):
        head = uint8(1)
        if self.__bot_contraction_status == head and self.__occupied:
            message = "Bot currently expanded, use toggle_contracted_on_node"
            raise Exception(message)
        elif self.__occupied == 0:
            raise Exception("There is no bot on this node")
        self.__node_data[17, 0] = head
        self.__bot_contraction_status = head

    def __toggle_occupied(self):
        off = uint8(0)
        on = uint8(1)
        if self.__occupied == 1:
            self.__node_data[3, 0] = off
            self.__occupied = off
        else:
            self.__node_data[3, 0] = on
            self.__occupied = on

    def toggle_tail_on_node(self):
        tail = uint8(2)
        if self.__bot_contraction_status == tail and self.__occupied:
            message = "Bot currently expanded, use toggle_contracted_on_node"
            raise Exception(message)
        elif self.__occupied == 0:
            raise Exception("There is no bot on this node")
        self.__node_data[17, 0] = tail
        self.__bot_contraction_status = tail

    def toggle_wall(self):
        wall = uint8(2)
        node = uint8(1)
        if self.__enabled_type == 1:
            self.__node_data[0, 0] = wall
            self.__enabled_type = wall
        else:
            self.__node_data[0, 0] = node
            self.__enabled_type = node
