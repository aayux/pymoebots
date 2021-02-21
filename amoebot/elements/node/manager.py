# -*- coding: utf-8 -*-

""" elements/node/manager.py
"""

# from amoebot.elements.node.core import Node
# from amoebot.elements.manager import Manager
from amoebot.elements.node.manager_utils import *
from amoebot.elements.node.core import Node
from numpy import ndarray, where
from typing import Union, List, Tuple

import numpy as np
import typing


# from collections import defaultdict


# class NodeManager(Manager):
#     r"""
#     Manages grid connectivity and the node map for fast lookups.
#
#     Attributes
#
#         __nmap (defaultdict) :: a dictionary of dictionaries used to index nodes
#                         using x and y co-odrinates.
#         grid_points (numpy.ndarray) :: "matrix" of the points on the grid.
#     """
#
#     def __init__(self, points: np.ndarray):
#         r"""
#         Attributes
#
#             points (numpy.ndarray) :: list of grid points returned by
#                                 `make_triangular_grid`.
#         """
#         # [dictionary of dictionary] of nodes
#         self.__nmap: defaultdict = defaultdict(dict)
#
#         # numpy array of plotted points
#         self.grid_points: np.ndarray = np.array(points)
#
#         # call to grid builder
#         self.grid_builder()
#
#     def grid_builder(self):
#         r"""
#         Create nodes at grid positions and link the nodes into a full grid.
#         """
#
#         # rows and cols in the plotted points on the grid
#         nrows, ncols, dim = self.grid_points.shape
#         self.grid_points = self.grid_points.reshape(nrows * ncols, dim)
#
#         # place nodes on the grid
#         for point in self.grid_points:
#             # add node to node manager
#             self._add_node(point=point)
#
#         # calls function to link adjacent nodes on the hexagonal grid
#         self._hex_connect()
#
#     def _add_node(self, point: np.ndarray):
#         r"""
#         Add individual nodes to node lookup.
#
#         Attributes:
#             points (numpy.arrray) :: list containing the x and y grid
#                                 co-ordinates.
#         """
#
#         # creates node and assigns it a place in the node dictionary
#         self.__nmap[point[0]][point[1]] = Node(position=point)
#
#     def _hex_connect(self):
#         r"""
#         Link adjacent nodes on the hexagonal grid.
#         """
#
#         # TODO dynamically optimise this function
#
#         # iterate over the rows
#         for ix in self.__nmap:
#             for jx in self.__nmap[ix]:
#                 # current node
#                 node = self.__nmap[ix][jx]
#
#                 # if data isn't already available
#                 if node.neighbors['n'] is None and (jx + 2) in self.__nmap[ix]:
#                     # link the node's neighbour to the north
#                     node.set_neighbor('n', np.array([
#                         ix, jx + 2
#                     ], dtype=np.uint8)
#                                       )
#
#                     # back link to the current node
#                     self.__nmap[ix][jx + 2].set_neighbor('s',
#                                                          np.array([ix, jx],
#                                                                   dtype=np.uint8)
#                                                          )
#
#                 # also ensure node is in the grid systems
#                 if node.neighbors['ne'] is None and (ix + 1) in self.__nmap \
#                         and (jx + 1) in self.__nmap[ix + 1]:
#                     if (jx + 1) in self.__nmap[ix + 1]:
#                         # link the node's neighbour to the north east
#                         node.set_neighbor('ne', np.array([
#                             ix + 1, jx + 1
#                         ], dtype=np.uint8)
#                                           )
#
#                         # back link to the current node
#                         self.__nmap[ix + 1][jx + 1].set_neighbor('sw',
#                                                                  np.array(
#                                                                      [ix, jx],
#                                                                      dtype=np.uint8)
#                                                                  )
#
#                 if node.neighbors['se'] is None and (ix + 1) in self.__nmap \
#                         and (jx - 1) in self.__nmap[ix + 1]:
#                     # link the node's neighbour to the south east
#                     node.set_neighbor('se', np.array([
#                         ix + 1, jx - 1
#                     ], dtype=np.uint8)
#                                       )
#
#                     # back link to the current node
#                     self.__nmap[ix + 1][jx - 1].set_neighbor('nw',
#                                                              np.array([ix, jx],
#                                                                       dtype=np.uint8)
#                                                              )
#
#                 if node.neighbors['s'] is None and (jx - 2) in self.__nmap[ix]:
#                     # link the node's neighbour to the south
#                     node.set_neighbor('s', np.array([
#                         ix, jx - 2
#                     ], dtype=np.uint8)
#                                       )
#
#                     # back link to the current node
#                     self.__nmap[ix][jx - 2].set_neighbor('n',
#                                                          np.array([ix, jx],
#                                                                   dtype=np.uint8)
#                                                          )
#
#                 if node.neighbors['sw'] is None and (ix - 1) in self.__nmap \
#                         and (jx - 1) in self.__nmap[ix - 1]:
#                     # link the node's neighbour to the south west
#                     node.set_neighbor('sw', np.array([
#                         ix - 1, jx - 1
#                     ], dtype=np.uint8)
#                                       )
#
#                     # back link to the current node
#                     self.__nmap[ix - 1][jx - 1].set_neighbor('ne',
#                                                              np.array([ix, jx],
#                                                                       dtype=np.uint8)
#                                                              )
#
#                 if node.neighbors['nw'] is None and (ix - 1) in self.__nmap \
#                         and (jx + 1) in self.__nmap[ix - 1]:
#                     # link the node's neighbour to the north west
#                     node.set_neighbor('nw', np.array([
#                         ix - 1, jx + 1
#                     ], dtype=np.uint8)
#                                       )
#
#                     # back link to the current node
#                     self.__nmap[ix - 1][jx + 1].set_neighbor('se',
#                                                              np.array([ix, jx],
#                                                                       dtype=np.uint8)
#                                                              )
#
#                 self.__nmap[ix][jx] = node
#
#     def get_node(self, position: np.ndarray) -> Node:
#         r"""
#         Get `Node` object at `position`.
#
#         Atrributes:
#             position (numpy.ndarray) :: list containing x and y co-ordinates of
#                             node to look up in the `__nmap` dictionary.
#
#         Return (Node): object of class `Node` at the specified lookup
#                         `position`.
#         """
#
#         return self.__nmap[position[0]][position[1]]
#
#     @property
#     def get_nmap(self) -> dict:
#         return self.__nmap
#
#     @property
#     def get_num_nodes(self) -> int:
#         nrows, ncols, _ = self.grid_points.shape
#         return nrows * ncols


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
            self.nodes = np.zeros([NUMBER_OF_ATTRIBUTES, 1], dtype=int8)

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
        occupied = self.get_node(x=x, y=y)[3]
        return True if occupied else False

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

    def get_occupied_neighbors_of(self, node_index: int) -> typing.Union[
        set, typing.Set[int]]:
        nodes = self.nodes
        nodes_by_point = self.nodes_by_point
        neighbors_set, nodes = get_occupied_neighbors_ver_0(
            working_node=node_index,
            nodes=nodes,
            nodes_by_point=nodes_by_point)
        self.nodes = nodes
        return neighbors_set

    def add_bots(self, points: ndarray) -> None:
        # TODO: Implement add_bots
        # localize required function.
        get_node = self.get_node

        # split points to separate two sets x and y values for head and tail.
        head_x_values, head_y_values, tail_x_values, tail_y_values = points

        # get next bot id
        next_bot_id = self.__get_next_bot_id()

        # loop through values
        for i in range(head_x_values.size):
            head_x, head_y = head_x_values[i], head_y_values[i]
            tail_x, tail_y = tail_x_values[i], tail_y_values[i]
            # Using point (x, y) data, we pull the associated node data and
            # creates node a node object from it.
            head_node = Node(get_node(x=head_x, y=head_y))

            # TODO: add contraction status handling
            # TODO: add tail with different coordinates than head
            # TODO: add head tail validation to make sure they are within
            #  relative range of each other.
            tail_node = None

            if head_x != tail_x or head_y != tail_y:
                relative_x = head_x - tail_x
                relative_y = head_y - tail_y
                relative_p_existence_dict = get_relative_point_existence_dict()
                if relative_x not in relative_p_existence_dict:
                    message = f"The x values between head in tail. The values" \
                              f" that caused this error at head x value " \
                              f"{head_x} and tail x value {tail_x}."
                    raise Exception(message)
                elif relative_y not in relative_p_existence_dict[relative_x]:
                    message = f"The y values between head in tail. The values" \
                              f" that caused this error at head y value " \
                              f"{head_y} and tail y value {tail_y}."
                    raise Exception(message)

                tail_node = Node(get_node(x=tail_x, y=tail_y))

            # if the node is occupied, we can't place a bot here, so we
            # through up an error stating this.
            if head_node.occupied:
                message = f"Unable to place bot because point " \
                          f"({head_node.get_point()}) is occupied."
                raise Exception(message)

            # Switch occupancy on
            # head_node.toggle_occupied()

            # Add bot_id to current_node
            head_node.bot_id = next_bot_id

            if tail_node is not None:
                # if the node is occupied, we can't place a bot here, so we
                # through up an error stating this.
                if tail_node.occupied:
                    message = f"Unable to place bot because point " \
                              f"({tail_node.get_point()}) is occupied."
                    raise Exception(message)

                # Switch occupancy on
                # tail_node.toggle_occupied()

                # Add bot_id to current_node
                tail_node.bot_id = next_bot_id

                head_node.toggle_head_on_node()
                tail_node.toggle_tail_on_node()

            else:
                head_node.toggle_contracted_on_node()

            # Increment bot id. NOTE: This is assuming that we never delete
            # bots.
            next_bot_id += 1

    def add_walls(self, points: ndarray) -> None:
        """
        Adds given points as walls (2) type objects in the node space.

        :param ndarray points: A 2d array with x and y values in their own array
        :returns: nothing
        """

        # localize required function.
        get_node = self.get_node

        # split points to separate x and y values.
        x_values, y_values = points

        # loop through values
        for i in range(x_values.size):

            # Using point (x, y) data, we pull the associated node data and
            # creates node a node object from it.
            node = Node(get_node(x=x_values[i], y=y_values[i]))

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
        get_node = self.get_node
        nodes = self.nodes
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
        for _ in range(depth):
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

            # Check if current node already has a signal coming from our
            # specified direction.
            if head.get_signal_status(port=port):
                # Marks that we found a signal and breaks search.
                found_something = signal
                break

            # Checks if current node is a wall.
            if head.is_wall():
                # Marks that we found a wall and breaks search.
                found_something = wall
                break

        # If what we found was a wall, go back through the stack and set the
        # signal variable in the specified direction as true (1).
        if found_something == wall:

            # Initialize signals of readability.
            on = uint8(1)

            # localize calls to pop for the same stack
            pop = node_stack.pop

            # While there are still nodes in the stack continue.
            while node_stack:
                # Pops node off node_stack and sets the signal in the specified
                # direction as true (1).
                pop().set_signal_on_port(value=on, port=port)

        # If we found something return true (1) else false (0).
        return uint8(1) if found_something else uint8(0)

    def __get_next_bot_id(self):
        i = 0
        while True:
            id_existence = where(self.__get_bot_id_data() == i)[0]
            if id_existence.size == 0:
                break
            i += 1
        return int_primitive_to_numpy_dtype(i)

    def __get_bot_id_data(self, index: UNSIGNED_INT = None):
        if index is None:
            return self.__nodes[4]
        return self.__nodes[4, index]


    def __get_next_open_index(self):
        # TODO: Determine if needed
        open_spots = where(self.__get_enabled_type_data() == 0)[0]
        return int8(-1) if open_spots.size == 0 else open_spots[0]

    def __get_enabled_type_data(self, index: UNSIGNED_INT = None):
        # TODO: Determine if needed
        if index is None:
            return self.__nodes[0]
        return self.__nodes[0, index]

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

    def __get_node_data(
            self, index: UNSIGNED_INT) -> ndarray:
        """
        Grabs all node data at a specified index.

        :param typing.Union[uint8, uint16, uint32, uint64] index: Column in the
            node ndarray where the node is found.
        :returns: ndarray filled with node data.
        """
        return self.__nodes[0:, index:index + 1]


if __name__ == '__main__':
    x1 = np.array(
        [[0, 2, 4, 6, 8], [0, 0, 0, 0, 0], [0, 2, 4, 6, 8], [0, 0, 0, 0, 0]])

    x2 = NodeManagerBitArray(points=x1)
    print(x2.is_occupied_ver_1(node_index=0))
    print(x2.is_occupied_ver_1(node_index=6))
    # x3 = x2.nodes
    # x2 = NodeManagerBitArray(bot_id=0, nodes=x3)
    # x2.move_to(port=2)
    # x3 = x2.get_occupied_neighbors()
    # x3 = x3[0] | x3[1]
    # x4 = set()
    # for i in x3:
    #     x4 |= x2.get_occupied_neighbors_of(node_index=i.item())
    # print(x3)
    # print(x4)
    # print(x2.nodes)

    # x2.move_to(port=2)
    # x3 = x2.get_occupied_neighbors()
    # print(x3)
