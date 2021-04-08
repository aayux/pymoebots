# -*- coding: utf-8 -*-

""" elements/node/manager.py
"""

from amoebot.elements.node.core import Node
from amoebot.elements.manager import Manager
from amoebot.elements.node.manager_utils import *

from numpy import ndarray, where, uint8
from typing import List, Tuple

import numpy as np
import typing
from collections import defaultdict

# @pedantic.pedantic_class
class NodeManagerBitArray:
    # TODO: Write docstrings for all current methods
    # TODO: Figure out best way to implement a yield function

    __slots__ = [
        '__nodes_by_point',
        '__nodes',
        '__bot_id',
        '__working_nodes',
        '__weakref__',
        '__pedantic_a42__'
    ]

    def __init__(
            self,
            bot_id: int = -1,
            points: np.ndarray = np.array([]),
            nodes: np.ndarray = np.array([]),
    ) -> None:
        """
        The class is used to handle the node space as an numpy.ndarray.

        :param int bot_id:
        :param ndarray points:
        :param ndarray nodes:
        """

        self.nodes_by_point = nodes_by_point = {}
        if nodes.size == 0:
            self.nodes = np.zeros([NUMBER_OF_ATTRIBUTES, 1], dtype=np.int8)

        else:
            self.nodes = nodes
            # TODO: Create dictionary of nodes
            map_node_array_ver_0(nodes=nodes, nodes_by_point=nodes_by_point)

        if bot_id != -1:
            self.working_nodes = get_working_node_index_ver_0(nodes=nodes,
                                                              bot_id=bot_id)
            # self.working_node = self.__internal_retrieve_working_node_index()
        else:
            self.working_nodes = ()

        self.bot_id = bot_id

        if points.size > 0:
            self.nodes = add_points_ver_0(nodes=self.nodes, points=points,
                                          nodes_by_point=nodes_by_point)

    @property
    def nodes(self) -> np.ndarray:
        """

        :return ndarray: returns numpy array of nodes organized attributes x
         number
        """
        return self.__nodes

    @nodes.setter
    def nodes(self, value: np.ndarray) -> None:
        """
        Sets self.__nodes value

        :param ndarray value:
        """
        x = value.shape[0]
        y = value.dtype.type
        z = NUMPY_INT_LEVELS['ints']
        if x != NUMBER_OF_ATTRIBUTES:
            raise ValueError(f'Received {x}, expected {NUMBER_OF_ATTRIBUTES}')
        elif y not in z:
            raise TypeError(f"Received {y}, expected one of these {z}")
        self.__nodes = value

    @nodes.deleter
    def nodes(self) -> None:
        """
        Deletes current nodes by replacing array with an NUMBER_OF_ATTRIBUTES
         by 1 numpy array.

        """
        self.nodes = np.zeros((NUMBER_OF_ATTRIBUTES, 1), dtype=np.int8)

    @property
    def nodes_by_point(self) -> typing.Dict[int, typing.Dict[int, int]]:
        """

        :return typing.Dict[int, typing.Dict[int, int]]:
        """
        return self.__nodes_by_point

    @nodes_by_point.setter
    def nodes_by_point(self,
                       value: typing.Dict[int, typing.Dict[int, int]]) -> None:
        """

        :param typing.Dict[int, typing.Dict[int, int]] value:
        """
        self.__nodes_by_point = value

    @nodes_by_point.deleter
    def nodes_by_point(self) -> None:
        """
        deletes all existing nodes
        """
        self.nodes_by_point = {}

    @property
    def bot_id(self) -> int:
        return self.__bot_id

    @bot_id.setter
    def bot_id(self, value: int) -> None:
        if value >= -1:
            self.__bot_id = value
        else:
            raise ValueError("Bot id must be greater than -1")

    @bot_id.deleter
    def bot_id(self) -> None:
        self.bot_id = -1

    @property
    def working_nodes(self) -> typing.Union[tuple, typing.Tuple[int]]:
        return self.__working_nodes

    @working_nodes.setter
    def working_nodes(self,
                      value: typing.Union[tuple, typing.Tuple[int]]) -> None:
        for i in value:
            if not isinstance(i, int):
                x = type(int)
                raise TypeError(f"working_nodes expected {x}, got {type(i)}")

        self.__working_nodes = value

    @working_nodes.deleter
    def working_nodes(self) -> None:
        self.working_nodes = (-1,)

    def get_node(
            self, x: typing.Union[int, float], y: typing.Union[int, float],
    ) -> np.ndarray:
        nodes_by_point = self.nodes_by_point
        f1 = check_points_existence_ver_0
        exists = f1(nodes_by_point=nodes_by_point, x=x, y=y)
        if exists:
            f1 = get_node_index_ver_0
            index = f1(x=x, y=y, nodes_by_point=nodes_by_point)
        else:
            f1 = add_point_ver_1
            x1, x2 = self.nodes, nodes_by_point
            index, self.nodes = f1(x=x, y=y, nodes=x1, nodes_by_point=x2)
        return self.nodes[0:, index:index + 1]

    def is_occupied(
            self, x: typing.Union[int, float], y: typing.Union[int, float]
    ) -> bool:
        node = self.get_node(x=x, y=y)
        return True if node[0] == 2 or node[3] else False 

    def move_to(self, port: int, ) -> bool:
        relative_x, relative_y = NODE_LAYOUT[LAYOUT][port]['relative_point']
        working_nodes = self.working_nodes
        if len(working_nodes) == 1:
            nodes = self.nodes
            current_node = get_node_via_index_ver_0(nodes, working_nodes[0])
            current_x = current_node[(1,), (0,)].item()
            current_y = current_node[(2,), (0,)].item()
            target_x, target_y = current_x + relative_x, current_y + relative_y

            if self.is_occupied(x=target_x, y=target_y):
                return False

            target_node = self.get_node(x=target_x, y=target_y)

            target_node[(3, 4), (0, 0)] = 1, current_node[(4,), (0,)]
            target_node[(17,), (0,)] = 1
            current_node[(17,), (0,)] = 2
            x1, x2, x3 = target_x, target_y, self.nodes_by_point
            head_index = get_node_index_ver_0(x=x1, y=x2, nodes_by_point=x3)
            self.working_nodes = (head_index, working_nodes[0])
            return True
        raise ValueError("You are trying to move the head while bot is "
                         "expanded, compress this bot first")


    def contract_forward(self) -> bool:
        working_nodes = self.working_nodes
        if len(working_nodes) == 1:
            return False
        elif len(working_nodes) == 2:
            x1, x2, x3 = self.nodes, working_nodes[0], working_nodes[1]
            x4, x5 = "forward", contract_ver_0
            x6 = x5(nodes=x1, head_node_index=x2, tail_node_index=x3, option=x4)
            self.working_nodes = x6
            return True
        else:
            raise ValueError("Looks like there is in an issue with the number "
                             "of working nodes")

    def contract_backward(self) -> bool:
        working_nodes = self.working_nodes
        if len(working_nodes) == 1:
            return False
        elif len(working_nodes) == 2:
            x1, x2, x3 = self.nodes, working_nodes[0], working_nodes[1]
            x4, x5 = "backward", contract_ver_0
            x6 = x5(nodes=x1, head_node_index=x2, tail_node_index=x3, option=x4)
            self.working_nodes = x6
            return True
        else:
            raise ValueError("Looks like there is in an issue with the number "
                             "of working nodes")

    def open_ports(self) -> typing.Union[list, typing.List[typing.Set[int]]]:
        # Check compression
        working_nodes = self.working_nodes
        nodes = self.nodes
        is_occupied = self.is_occupied
        contracted = len(working_nodes) == 1
        head_tail_empty_ports = list()

        # grab neighbor attributes of associated working nodes
        if contracted:

            # grabs completely empty uncreated node positions
            neighbors = self.nodes[NEIGHBOR_RANGE, self.working_nodes[0]]
            empty_ports = set(np.where(neighbors == -1)[0])

            # check whether or not existing nodes are empty
            for i in range(6):
                is_neighbor_occupied(nodes, empty_ports, i, neighbors,
                                     is_occupied)
            # add to return value
            head_tail_empty_ports.append(empty_ports)
            head_tail_empty_ports.append(set())

        else:
            head_neighbors = self.nodes[NEIGHBOR_RANGE, self.working_nodes[0]]
            head_empty_ports = set(np.where(head_neighbors == -1)[0])
            tail_neighbors = self.nodes[NEIGHBOR_RANGE, self.working_nodes[1]]
            tail_empty_ports = set(np.where(tail_neighbors == -1)[0])

            for i in range(6):
                is_neighbor_occupied(nodes, head_empty_ports, i, head_neighbors,
                                     is_occupied)
                is_neighbor_occupied(nodes, tail_empty_ports, i, tail_neighbors,
                                     is_occupied)

            head_tail_empty_ports.append(head_empty_ports)
            head_tail_empty_ports.append(tail_empty_ports)

        return head_tail_empty_ports

    def current_position(self) -> np.ndarray:
        working_nodes = self.working_nodes
        nodes = self.nodes

        if len(working_nodes) == 1:
            node = nodes[0:, working_nodes[0]]

            return np.array(
                [[node[1], node[2]], [node[1], node[2]]]
            )
        elif len(working_nodes) == 2:
            head_node = nodes[0:, working_nodes[0]]
            tail_node = nodes[0:, working_nodes[1]]
            return np.array(
                [
                    [head_node[1], head_node[2]],
                    [tail_node[1], tail_node[2]]
                ]
            )

    def get_occupied_neighbors(self) -> np.ndarray:
        working_nodes = self.working_nodes
        nodes = self.nodes
        nodes_by_points = self.nodes_by_point
        contracted = len(working_nodes) == 1

        if contracted:
            neighbors_set, nodes = get_occupied_neighbors_ver_0(
                working_node=working_nodes[0],
                nodes=nodes,
                nodes_by_point=nodes_by_points)
            self.nodes = nodes
            return np.array([neighbors_set, set()])
        else:
            head_neighbors_set, nodes = get_occupied_neighbors_ver_0(
                working_node=working_nodes[0],
                nodes=nodes,
                nodes_by_point=nodes_by_points,
                do_not_count=working_nodes[1],
            )
            tail_neighbors_set, nodes = get_occupied_neighbors_ver_0(
                working_node=working_nodes[1],
                nodes=nodes,
                nodes_by_point=nodes_by_points,
                do_not_count=working_nodes[0],
            )

            self.nodes = nodes
            return np.array([head_neighbors_set, tail_neighbors_set])

    def get_occupied_neighbors_of(self, node_index: int) -> typing.Union[set, typing.Set[int]]:
        nodes = self.nodes
        nodes_by_point = self.nodes_by_point
        neighbors_set, nodes = get_occupied_neighbors_ver_0(
            working_node=node_index,
            nodes=nodes,
            nodes_by_point=nodes_by_point)
        self.nodes = nodes
        return neighbors_set

    def add_wall(self, point: tuple) -> None:
        """
        Adds given points as walls (2) type objects in the node space.

        :param ndarray points: A tuple with x and y co-ordinates
        :returns: nothing
        """

        # localize required function.
        get_node = self.get_node  # TODO: rewrite method to utilize node class.

        # split points to separate x and y values
        wall_x, wall_y = point

        # Using point (x, y) data, we pull the associated node data and
        # creates node a node object from it.
        node = Node(get_node(x=wall_x, y=wall_y))

        # if the node is occupied, we can't place a wall here, so we
        # through up an error stating this.
        if node.occupied:
            raise Exception(f"Unable to place wall because point "
                            f"({node.get_point()}) is occupied.")

        # makes current node a wall.
        node.toggle_wall()

    def ping_for_wall(self, port: uint8, depth: uint8) -> uint8:
        """
        Sends a ping in a specified directions that travels across head
        objects in the same direction for a limited distance.

        :param uint8 port: Specified direction to use
        :param uint8 depth: Number of nodes to travel before signal dies.
        :returns: uint8 0 - false or 1 - true
        """
        # localize necessary components
        get_node = self.get_node  # TODO: rewrite method to utilize node class.
        get_node_data = self.__get_node_data

        # Grab the node associated with the head position
        head = self.__get_working_nodes()[0]

        # Grab directional points relative to origin.
        relative_x, relative_y = get_relative_points_direction(port)

        # Initialize signals of readability
        nothing = 0
        wall = 1
        signal = 2

        # Flag to signal that a wall was found during search or a signal was
        # felt.
        found_something = nothing

        # Used to travel backwards and update nodes if wall was found.
        node_stack = []

        # Walks through the specified number of nodes (depth) from origin in the
        # direction specified (port).
        k = 0
        for k in range(depth):
            # Add current position to stack.
            node_stack.append(head)

            # Grab neighbor index associated with the port.
            neighbor_index = head.get_neighbor_index(port=port)

            # Initialize signals of readability.
            node_not_created = -1

            # Check if the node at the neighbor index has been created.
            if neighbor_index == node_not_created:
                # Since the node has not been created, we create the node by
                # using get_node.

                # create the neighbor node x value
                next_x = head.x + relative_x

                # create the neighbor node y value
                next_y = head.y + relative_y

                # create node by using get_node with updated x and y values. We
                # then covert the node data provided by get_node to create a
                # Node object.
                head = Node(node_data=get_node(x=next_x, y=next_y))
            else:
                # Since the neighbor has been created, we just grab the
                # neighbor's node data and create a Node object.
                head = Node(node_data=get_node_data(index=neighbor_index))

            # print(f"{head.x}, {head.y}, {head.is_wall()}")

            # Checks if current node is a wall.
            if head.is_wall():
                # Marks that we found a wall and breaks search.
                found_something = wall
                break

        # ...
        return k + 1

    def __get_node_data(
            self, index: UNSIGNED_INT) -> ndarray:
        """
        Grabs all node data at a specified index.

        :param Union[uint8, uint16, uint32, uint64] index: Column in the node
            ndarray where the node is found.
        :returns: ndarray filled with node data.
        """
        return self.__nodes[0:, index:index + 1]

    def __get_working_nodes(self) -> List[Node]:
        """
        Gets node objects from node indices

        :returns: List of Node objects
        """
        # localize necessary components
        get_node_data = self.__get_node_data

        # Grab indices associated with bot id
        indices = self.__get_working_nodes_indices()

        # Create array of Node objects and return it.
        return [Node(node_data=get_node_data(index=i)) for i in indices]

    def __get_working_nodes_indices(self) -> Tuple[UNSIGNED_INT, UNSIGNED_INT]:
        """
        Find indices in node array associated with bot id

        :returns: Pair of ints as a tuple.
        """
        # localize necessary components
        nodes = self.nodes
        bot_id = self.bot_id

        # Grab positions (indices) where the bot id appears in the bot id field
        indices = where(nodes[4] == bot_id)[0]

        # Check if no indices are returned because this means a bot with that
        # particular id is not present in the environment
        if indices.size == 0:
            raise Exception("Bot does not appear to be on any existing node")

        # If the bot is contracted only one index should be preset.
        elif indices.size == 1:
            return indices[0], indices[0]

        # If the bot is expanded the number of nodes occupied should be two,
        # therefore the number of indices should be two.
        elif indices.size == 2:
            # Grab the head/tail/contracted flag in the nodes at the indices
            # given
            head_or_tail_statuses = nodes[17][indices]

            # Check if the first number in the head/tail array is head (1)
            if head_or_tail_statuses[0] == 1:
                # return head and tail in current order
                return indices[0], indices[1]

            # Check failed, so the first index belongs to the tail.
            # Return flip-flop version of indices.
            return indices[1], indices[0]

        # If none of the previous conditions were hit, then the bot recorded to
        # be spread across too many nodes.
        else:
            raise Exception("Bot is located on too many nodes")
