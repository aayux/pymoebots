# -*- coding: utf-8 -*-

""" elements/nodenv.py
"""

from .extras import *
from .manager import Manager
from ..utils.exceptions import MovementError

import numpy as np
import typing
from collections import defaultdict


class NodeEnvManager(Manager):
    r"""
    The class represents the node space as an `numpy.ndarray` and provides an
    API to manipulate it.

    TODO figure out the best way to implement a yield function
    """

    __slots__ = [
                    '__bot_id',
                    '__node_array',
                    '__points_dict',
            ]

    def __init__(
                    self,
                    _bot_id:int=-1,
                    points:np.ndarray=None,
                    node_array:np.ndarray=None,
            ):

        self.points_dict = dict()
        self._bot_id = _bot_id

        points = np.array([]) if points is None else points
        node_array = np.array([]) if node_array is None else node_array

        # intialise the node array
        if len(node_array) == 0:
            self.node_array = np.zeros([NUM_ATTRIBS, 1], dtype=np.int8)
        else:
            self.node_array = node_array
            # TODO create a dictionary of nodes
            self.points_dict = create_points_dict_init0(
                                                            node_array, 
                                                            self.points_dict
                                                        )

        if len(points) > 0:
            # NOTE `points` only contains coordinates of *active* sites
            self.node_array = add_new_points(
                                                self.node_array, 
                                                points, 
                                                self.points_dict
                                            )

    def is_occupied(self, point:np.ndarray) -> bool:
        r"""
        Attributes
            point (numpy.ndarray) ::
        
        Returns (bool): 
        """

        _, _node = self._get_node(point)
        occupied = _node[3]
        return True if occupied else False

    def is_contracted(self, actv_nodes:np.ndarray) -> bool:
        r"""
        """
        return len(actv_nodes) == 1

    def _get_actv_node_index(self) -> tuple:
        r"""
        Returns (tuple) : 
        """
        col_ix = np.where(self.node_array[4] == self._bot_id)[0]

        assert len(col_ix) in [1, 2], ValueError
        
        # if particle is contracted
        if len(col_ix) == 1:
            return (col_ix[0],)
        # else if particle is expanded
        elif len(col_ix) == 2:
            occ_statuses = self.node_array[17][col_ix]

            # if the first of the two entries is a head
            if occ_statuses[0] == 1:
                return (col_ix)
            # else the first entry must be a tail
            return (col_ix[::-1])

    def _get_current_node_position(self) -> np.ndarray:
        r"""
        """
        actv_nodes = self._get_actv_node_index()

        # if particle is contracted
        if self.is_contracted(actv_nodes):
            _node = self.node_array[0:, actv_nodes[0]]
            point = np.array([_node[1:3], _node[1:3]])
        else:
            _h_node = self.node_array[0:, actv_nodes[0]]
            _t_node = self.node_array[0:, actv_nodes[1]]
            point = np.array([_h_node[1:3], _t_node[1:3]])
        
        return point

    def _get_open_ports(self) -> list:
        r"""
        Returns (list[set[int], set[int]]): 
        """

        all_open_ports = [set(), set()]
        actv_nodes = self._get_actv_node_index()

        # if particle is contracted
        if self.is_contracted(actv_nodes):

            # collect all neigbours around the particle
            neighbors = self.node_array[NEIGHBOR_ROWS, actv_nodes[0]]

            for ix, neighbor in enumerate(neighbors):
                # collect uninstantiated neighbour port's index
                if neighbor == -1: 
                    all_open_ports[0] |= {ix}
                # collect unoccupied neighbour port's index
                else:
                    _neighbor_node_array = self.node_array[
                                                    :, neighbor:(neighbor + 1)
                                                ]
                    _neighbor_occ = _neighbor_node_array[3]
                    if not _neighbor_occ:
                        all_open_ports[0] |= {ix}
        # now consider expanded particles
        else:
            h_neighbors = self.node_array[NEIGHBOR_ROWS, actv_nodes[0]]
            t_neighbors = self.node_array[NEIGHBOR_ROWS, actv_nodes[1]]

            for ix in range(6):
                h_neighbor, t_neighbor = h_neighbors[ix], t_neighbors[ix]
                # collect uninstantiated neighbour port's index
                if h_neighbor == -1: 
                    all_open_ports[0] |= {ix}
                else:
                    _h_neighbor_node_array = self.node_array[
                                            :, h_neighbor[ix]:(h_neighbor + 1)
                                        ]
                    _h_neighbor_point = _h_neighbor_node_array[1:3].flatten()
                    if not self.is_occupied(_h_neighbor_point):
                        all_open_ports[0] |= {ix}

                if t_neighbor == -1: 
                    all_open_ports[1] |= {ix}

                # collect unoccupied neighbour port's index
                else:
                    _t_neighbor_node_array = self.node_array[
                                            :, t_neighbor[ix]:(t_neighbor + 1)
                                        ]
                    _t_neighbor_point = _t_neighbor_node_array[1:3].flatten()
                    if not self.is_occupied(_t_neighbor_point):
                        all_open_ports[1] |= {ix}

        return all_open_ports

    def _get_occupied_neighbors(self) -> np.ndarray:
        r"""
        Returns (numpy.ndarray[set[numpy.ndarray], set[numpy.ndarray]]): 
        """
        actv_nodes = self._get_actv_node_index()

        if self.is_contracted(actv_nodes):
            occ_neighbors_set, self.node_array = get_occupied_neighbors(
                                            self.node_array, self.points_dict, 
                                            actv_node_ix=actv_nodes[0]
                                        )
            return np.array([occ_neighbors_set, set()])
        else:
            h_occ_neighbors_set, self.node_array = get_occupied_neighbors(
                                            self.node_array, self.points_dict, 
                                            actv_node_ix=actv_nodes[0], 
                                            skip_ix=actv_nodes[1]
                                        )
            t_occ_neighbors_set, self.node_array = get_occupied_neighbors(
                                            self.node_array, self.points_dict, 
                                            actv_node_ix=actv_nodes[1], 
                                            skip_ix=actv_nodes[0]
                                        )

            return np.array([h_occ_neighbors_set, t_occ_neighbors_set])

    def _get_occ_neighbors_at_ix(self, node_ix:int) -> set:
        r"""
        Attributes
            node_ix (int) :: 
        Returns (set[numpy.ndarray]): 
        """
        occ_neighbors_set, self.node_array = \
                                        get_occupied_neighbors(
                                            self.node_array, self.points_dict, 
                                            actv_node_ix=node_ix
                                        )
        return occ_neighbors_set

    def _expand_to(self, port:int) -> np.ndarray:
        r"""
        Attributes
            port (int) ::

        Returns (numpy.ndarray) :: 
        """

        rel_x, rel_y = GRID_LAYOUT[DEFAULT_LAYOUT][port]['relative_point']
        actv_nodes = self._get_actv_node_index()
        head_ix = actv_nodes[0]

        # ensure particle is contracted,
        assert self.is_contracted(actv_nodes), \
                MovementError("Particle is already expanded.")

        _node = self.node_array[:, head_ix:head_ix + 1]
        _x, _y = _node[(1, 2,), (0,)]
        target_point = (_x + rel_x, _y + rel_y)

        if self.is_occupied(point=target_point): 
            return self.node_array

        target_ix, target_node = self._get_node(point=target_point)

        target_node[(3, 4), (0,)] = 1, _node[(4,), (0,)]
        target_node[(17,), (0,)] = 1
        _node[(17,), (0,)] = 2
        self.node_array[:, head_ix:head_ix + 1] = _node
        self.node_array[:, target_ix:target_ix + 1] = target_node

        return self.node_array

    def _contract_forward(self):
        r"""
        """
        actv_nodes = self._get_actv_node_index()
        assert not self.is_contracted(actv_nodes), MovementError
        
        _ = contract_node(
                            self.node_array, 
                            head_ix=actv_nodes[0], 
                            tail_ix=actv_nodes[1], 
                            option='fw'
                        )

    def _contract_backward(self):
        r"""
        """
        actv_nodes = self._get_actv_node_index()
        assert not self.is_contracted(actv_nodes), MovementError
        
        _ = contract_node(
                            self.node_array, 
                            head_ix=actv_nodes[0], 
                            tail_ix=actv_nodes[1], 
                            option='bw'
                        )

    def _get_node(self, point:np.ndarray) -> tuple:
        r"""
        Attributes
            point (numpy.ndarray) ::
        
        Returns (tuple[int numpy.ndarray]): 
        """
        if point_exists(point, self.points_dict):
            node_ix = get_node_ix(point, self.points_dict)
        # else add the node into the array (without amoebot)
        else:
            node_ix, self.node_array = add_point_no_amoebot(
                                            point, 
                                            self.node_array, 
                                            self.points_dict
                                        )
        return node_ix, self.node_array[:, node_ix:node_ix + 1]

    @property
    def node_array(self) -> np.ndarray:
        return self.__node_array

    @node_array.setter
    def node_array(self, value:np.ndarray):
        r"""
        Sets self.__nodes value.

        Attributes
            value (numpy.ndarray) ::
        
        Returns: None
        """

        _n_attribs = value.shape[0]
        _subtype = value.dtype.type
        _numpy_int_types = NUMPY_INT_LEVELS['np.int']

        assert (_n_attribs == NUM_ATTRIBS), \
            ValueError(f'Received {_n_attribs}, expected {NUM_ATTRIBS}')
        
        assert _subtype in _numpy_int_types, \
            TypeError(f"Received {_subtype}, expected one of {_numpy_int_types}")

        self.__node_array = value

    @node_array.deleter
    def node_array(self):
        r""" 
        Deletes node-array by replacing it with an (NUM_ATTRIBS x 1) numpy array.
        """

        self.node_array = np.zeros((NUM_ATTRIBS, 1), dtype=np.int8)

    @property
    def points_dict(self) -> dict:
        r"""
        Returns (dict[int, dict[int, int]]): 
        """
        return self.__points_dict

    @points_dict.setter
    def points_dict(self, value:dict):
        r"""
        Sets self.__points_dict value.

        Attributes
            value (dict[int, dict[int, int]]) ::
        
        Returns: None
        """
        self.__points_dict = value

    @points_dict.deleter
    def points_dict(self):
        r""" deletes all existing nodes
        """
        self.points_dict = dict()

    @property
    def _bot_id(self) -> int:
        return self.__bot_id

    @_bot_id.setter
    def _bot_id(self, value:int):
        r"""
        """
        assert value >= -1, ValueError("_bot_id must be greater than -1.")
        self.__bot_id = value

    @_bot_id.deleter
    def _bot_id(self):
        r"""
        """
        self._bot_id = -1