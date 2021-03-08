# -*- coding: utf-8 -*-
from numpy import ndarray, uint8

""" elements/node/core.py
"""


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
        """
        :param ndarray node_data: A single column of node data (attributes
            states)
        """

        self.__node_data = node_data

    @property
    def enabled_type(self):
        """
        :returns: Enabled type attribute.
        """
        return self.__node_data[0, 0]

    @enabled_type.setter
    def enabled_type(self, value: uint8):
        """
        :param uint8 value: value that correlates to inactive (0), node (1),
            wall (2).
        """
        self.__node_data[0, 0] = value

    @property
    def neighbor_0_index(self):
        """
        :returns: Index of neighbor in port 0
        """
        return self.__node_data[5, 0]

    @property
    def neighbor_1_index(self):
        """
        :returns: Index of neighbor in port 1
        """
        return self.__node_data[6, 0]

    @property
    def neighbor_2_index(self):
        """
        :returns: Index of neighbor in port 2
        """
        return self.__node_data[7, 0]

    @property
    def neighbor_3_index(self):
        """
        :returns: Index of neighbor in port 3
        """
        return self.__node_data[8, 0]

    @property
    def neighbor_4_index(self):
        """
        :returns: Index of neighbor in port 4
        """
        return self.__node_data[9, 0]

    @property
    def neighbor_5_index(self):
        """
        :returns: Index of neighbor in port 5
        """
        return self.__node_data[10, 0]

    @property
    def occupied(self):
        """
        :returns: Occupied attribute.
        """
        return self.__node_data[3, 0]

    @property
    def signal_0(self):
        """
        :returns: Signal value in the direction port 0
        """
        return self.__node_data[11, 0]

    @signal_0.setter
    def signal_0(self, value: uint8):
        """
        :param uint8 value: value that correlates to false (0) or true (1)
        """
        self.__node_data[11, 0] = value

    @property
    def signal_1(self):
        """
        :returns: Signal value in the direction port 1
        """
        return self.__node_data[12, 0]

    @signal_1.setter
    def signal_1(self, value: uint8):
        """
        :param uint8 value: value that correlates to false (0) or true (1)
        """
        self.__node_data[12, 0] = value

    @property
    def signal_2(self):
        """
        :returns: Signal value in the direction port 2
        """
        return self.__node_data[13, 0]

    @signal_2.setter
    def signal_2(self, value: uint8):
        """
        :param uint8 value: value that correlates to false (0) or true (1)
        """
        self.__node_data[13, 0] = value

    @property
    def signal_3(self):
        """
        :returns: Signal value in the direction port 3
        """
        return self.__node_data[14, 0]

    @signal_3.setter
    def signal_3(self, value: uint8):
        """
        :param uint8 value: value that correlates to false (0) or true (1)
        """
        self.__node_data[14, 0] = value

    @property
    def signal_4(self):
        """
        :returns: Signal value in the direction port 4
        """
        return self.__node_data[15, 0]

    @signal_4.setter
    def signal_4(self, value: uint8):
        """
        :param uint8 value: value that correlates to false (0) or true (1)
        """
        self.__node_data[15, 0] = value

    @property
    def signal_5(self):
        """
        :returns: Signal value in the direction port 5
        """
        return self.__node_data[16, 0]

    @signal_5.setter
    def signal_5(self, value: uint8):
        """
        :param uint8 value: value that correlates to false (0) or true (1)
        """
        self.__node_data[16, 0] = value

    @property
    def x(self):
        """
        :returns: X attribute.
        """
        return self.__node_data[1, 0]

    @property
    def y(self):
        """
        :returns: Y attribute.
        """
        return self.__node_data[1, 0]

    def get_neighbor_index(self, port: uint8):
        """
        Gets the neighbors index in the chosen direction.

        :param uint8 port: direction to get index.
        :returns: The index that belongs to the neighboring node within the node
            array.
        """
        return self.__get_from_neighbor(port=port, item="index")

    def get_signal_status(self, port: uint8):
        """
        Gets the signal status in the chosen direction.

        :param uint8 port: direction to get signal status.
        :returns: The signal status that is in the chosen direction.
        """
        return self.__get_from_neighbor(port=port, item="signal")

    def get_point(self):
        """
        :returns: X and y attribute in the point (x, y) format.
        """
        return self.x, self.y

    def is_node(self):
        """
        :returns: If node type is a general node.
        """
        return uint8(1) if self.enabled_type == 1 else uint8(0)

    def is_wall(self):
        """
        :returns: If node type is a wall type.
        """
        return uint8(1) if self.enabled_type == 2 else uint8(0)

    def set_signal_on_port(self, value: uint8, port: uint8):
        """
        :param uint8 value: value that correlates to false (0) or true (1)
        :param uint8 port: direction to set value
        """
        if port == 0:
            self.signal_0 = value
        elif port == 1:
            self.signal_1 = value
        elif port == 2:
            self.signal_2 = value
        elif port == 3:
            self.signal_3 = value
        elif port == 4:
            self.signal_4 = value
        elif port == 5:
            self.signal_5 = value

    def toggle_wall(self):
        """
        Converts node to a wall type.
        """
        # Initialize signals of readability.
        wall = 2

        # Checks if node is already a wall and raises Exception if it is.
        if self.enabled_type == wall:
            message = "Node is already a wall type."
            raise Exception(message)

        # Checks if node is currently occupied by a bot and raises Exception if
        # it is.
        elif self.occupied:
            raise Exception("Unable to convert an occupied node to a wall.")

        # Converts node to a wall type
        self.enabled_type = uint8(wall)

    def __get_from_neighbor(self, port: uint8, item: str):
        """
        :param uint8 port: direction to look in.
        :param str item: what item to get.
        :returns: An index or signal.
        """
        if port == 0:
            if item == "index":
                return self.neighbor_0_index

            elif item == "signal":
                return self.signal_0

        elif port == 1:
            if item == "index":
                return self.neighbor_1_index

            elif item == "signal":
                return self.signal_1

        elif port == 2:
            if item == "index":
                return self.neighbor_2_index

            elif item == "signal":
                return self.signal_2

        elif port == 3:
            if item == "index":
                return self.neighbor_3_index

            elif item == "signal":
                return self.signal_3

        elif port == 4:
            if item == "index":
                return self.neighbor_4_index

            elif item == "signal":
                return self.signal_4

        elif port == 5:
            if item == "index":
                return self.neighbor_5_index

            elif item == "signal":
                return self.signal_5

        raise Exception("Invalid port")
