# -*- coding: utf-8 -*-

""" elements/extras.py
"""

import numpy as np

""" constants 
"""

NUMPY_INT_LEVELS = {
                    'np.int': (np.int8, np.int16, np.int32, np.int64),
                    'range_int8': (-128, 127),
                    'range_int16': (-32768, 32767),
                    'range_int32': (-2147483648, 2147483647)
                }

_OCC_STATUS_CODES = {'w': 0, 'h': 1, 't': 2, 'c': 3}

# number of attributes of the node environment
# also the number of rows in the node-array/matrix
NUM_ATTRIBS = 18

# the layout of the 2-dimensional gridlines around any node
GRID_LAYOUT = {
                # horizontal major axis
                0: {
                        0: {
                                'relative_point': (-2, 0), 
                                'direction': 'w'
                        },
                        1: {
                                'relative_point': (-1, 1), 
                                'direction': 'nw'
                        },
                        2: {
                                'relative_point': (1, 1), 
                                'direction': 'ne'
                        },
                        3: {
                                'relative_point': (2, 0), 
                                'direction': 'e'
                        },
                        4: {
                                'relative_point': (1, -1), 
                                'direction': 'se'
                        },
                        5: {
                                'relative_point': (-1, -1), 
                                'direction': 'sw'
                        },
                    },
                    
                # vertical major axis
                1: {
                        0: {
                                'relative_point': (-1, 1), 
                                'direction': 'nw'
                        },
                        1: {
                                'relative_point': (0, 2), 
                                'direction': 'n'
                        },
                        2: {
                                'relative_point': (1, 1), 
                                'direction': 'ne'
                        },
                        3: {
                                'relative_point': (1, -1), 
                                'direction': 'se'
                        },
                        4: {
                                'relative_point': (0, -2), 
                                'direction': 's'
                        },
                        5: {
                                'relative_point': (-1, -1), 
                                'direction': 'sw'
                        },
                    },
            }

# set vertical layout by default
DEFAULT_LAYOUT = 1

# row indices for neighbour nodes in the node-array/matrix
NEIGHBOR_ROWS = np.arange(5, 11, dtype=np.uint8)


""" adders 
"""

def _add_point_init0(
                        point:np.ndarray,
                        _bot_id:int,
                        node_array:np.ndarray,
                        points_dict:dict,
                        cur_ix:int,
                        status:str='c'
                    ) -> int:
    r"""
    Initial array set up; preceded by `add_points` for checking and 
    reconfiguring the size of array.

    Attributes
        point (numpy.ndarray) :: 
        _bot_id (int) :: 
        cur_ix (int) :: 
        node_array (numpy.ndarray) :: 
        points_dict (dict) :: 
        status (str) default: 'c' :: occupancy status of the current node.
                        lookup information held in `dict` _OCC_STATUS_CODES

                        w : (0) node is a wall, 
                        h : (1) occupied by head, 
                        t : (2) occupied by an expanded tail , 
                        c : (3) occupied by a contracted bot.

    Returns (int) : 
    """
    # if the point exists, return the current index
    if point_exists(point, points_dict):
        return cur_ix
    
    node_array[:, cur_ix:cur_ix + 1] = _create_node_array_init0(
                                                        point, 
                                                        _bot_id=_bot_id, 
                                                        status=status
                                                    )

    _link_current_node_graph(node_array, points_dict, cur_ix=cur_ix)
    _update_points_dict(point, points_dict, cur_ix=cur_ix)

    return cur_ix + 1


def _add_point_null_nodes(
                            node_array:np.ndarray, 
                            points_dict:dict, 
                            actv_node_ix:int, 
                            null_nodes:np.ndarray
                        ):
    r"""
    Returns (numpy.ndarray) :: 
    """
    _node = node_array[0:, actv_node_ix]
    layout = GRID_LAYOUT[DEFAULT_LAYOUT]

    for ix in range(len(null_nodes)):
        rel_x, rel_y = layout[null_nodes[ix]]['relative_point']
        point = (_node[1] + rel_x, _node[2] + rel_y)
        _, node_array = add_point_no_amoebot(point, node_array, points_dict)
    
    return node_array


def add_point_no_amoebot(
                point:np.ndarray, 
                node_array:np.ndarray, 
                points_dict:dict) -> tuple:
    r"""
    Add point without adding bot to the point, does not check points existence,
    does resize nodes if necessary.

    Attributes
        point (numpy.ndarray) :: 
        node_array (numpy.ndarray) :: 
        points_dict (dict) :: 

    Returns (tuple[int, numpy.ndarray]) : 
    """
    cur_ix = _get_current_node_ix(node_array)

    # if the node-array has insufficient columns, we need to extend the array
    if cur_ix == -1:
        node_array = _extend_array_width(node_array)
        cur_ix = _get_current_node_ix(node_array)

    node_array[:, cur_ix:cur_ix + 1] = _create_unocc_node(point)
    _link_current_node_graph(node_array, points_dict, cur_ix=cur_ix)
    _update_points_dict(point, points_dict, cur_ix=cur_ix)
    return cur_ix, node_array


def add_new_points(
                    node_array:np.ndarray, 
                    points:np.ndarray,
                    points_dict: dict
            ):

    n_amoebots = len(points)

    cur_ix = _get_current_node_ix(node_array)
    _, ncols = node_array.shape

    # ensure we have enough slots in the array
    if ncols - cur_ix < n_amoebots:
        node_array = _extend_array_width(
                                            node_array, 
                                            min_width=(cur_ix + n_amoebots + 1)
                                    )

    for _bot_id, ht_points in enumerate(points):
        # extract the head and tail co-ordinates
        head, tail = ht_points[:2], ht_points[2:]

        # if particle is contracted
        if np.all(head == tail):
            cur_ix = _add_point_init0(
                                    point=head, 
                                    _bot_id=_bot_id, 
                                    node_array=node_array, 
                                    points_dict=points_dict, 
                                    cur_ix=cur_ix
                                )
        # else, ie., the particle is expanded
        else:
            cur_ix = _add_point_init0(
                                    point=head, 
                                    _bot_id=_bot_id, 
                                    node_array=node_array, 
                                    points_dict=points_dict, 
                                    cur_ix=cur_ix,
                                    status='h'
                                )
            
            cur_ix = _add_point_init0(
                                    point=tail, 
                                    _bot_id=_bot_id, 
                                    node_array=node_array, 
                                    points_dict=points_dict, 
                                    cur_ix=cur_ix,
                                    status='t'
                                )
    return node_array


""" creators 
"""


def create_points_dict_init0(node_array:np.ndarray, points_dict:dict):
    r"""
    Attributes
        node_array (numpy.ndarray) ::
        points_dict (dict) :: 

    Returns: None
    """

    cur_ix = _get_current_node_ix(node_array)
    if cur_ix == -1:
        cur_ix = node_array.shape[1]

    for ix in range(cur_ix):
        point = node_array[(1, 2), ix]
        _update_points_dict(point, points_dict, cur_ix=ix)

    return points_dict


def _create_node_array_init0(
                                point:np.ndarray, 
                                _bot_id:int, 
                                status:str
                            ) -> np.ndarray:
    r"""
    Attributes
        point (np.ndarray) :: 
        _bot_id (int) :: 
        status (str) ::
    
    Returns (np.ndarray) : 
    """

    (x, y) = point

    # initialise a zeros matrix
    _node_array = np.zeros([NUM_ATTRIBS, 1], dtype=np.int64)

    # initialise row and set occupancy status
    _node_array[(0, 3), 0] = 1

    # update the x and y coordinates
    _node_array[(1, 2), 0] = x, y

    # assign the unique amoebot identifier to current row
    _node_array[4, 0] = _bot_id

    # update occupancy status for node
    _node_array[17, 0] = _OCC_STATUS_CODES[status]

    # unset neighbour node identifier
    _node_array[NEIGHBOR_ROWS, 0] = -1

    return _node_array


def _create_unocc_node(point:np.ndarray) -> np.ndarray:
    r"""
    Attributes
        point (numpy.ndarray) ::

    Returns (numpy.ndarray) : 
    """
    (x,y) = point
    _node_array = np.zeros([NUM_ATTRIBS, 1], dtype=np.int64)
    _node_array[0, 0] = 1
    _node_array[(1, 2), 0] = x, y
    _node_array[4, 0] = -1
    _node_array[NEIGHBOR_ROWS, 0] = -1
    return _node_array


""" getters
"""


def _get_current_node_ix(node_array:np.ndarray) -> int:
    r"""
    Attributes
        node_array (numpy.ndarray) :: 

    Returns (int) : 
    """
    # see if node-array/matrix has any uninitialised slots
    open_slots = np.where(node_array[0] == 0)[0]

    return -1 if len(open_slots) == 0 else open_slots[0]


def get_node_ix(point:np.ndarray, points_dict:dict) -> int:
    r"""
    Attributes
        point (numpy.ndarray) ::
        points_dict (dict[int, dict[int, int]]) :: 

    Returns (int) : 
    """
    (x, y) = point
    if x in points_dict.keys():
        if y in points_dict[x]:
            return points_dict[x][y]
    return -1

def get_occupied_neighbors(
                                    node_array:np.ndarray, 
                                    points_dict:dict, 
                                    actv_node_ix:int,
                                    skip_ix:int=None
                                ) -> set:
    r"""
    Returns (tuple[set[int], numpy.ndarray])
    """
    null_nodes = _null_nodes_search(node_array, actv_node_ix)
    if len(null_nodes) != 0:
        node_array = _add_point_null_nodes(
                                node_array, 
                                points_dict, 
                                actv_node_ix, 
                                null_nodes
                            )

    neighbors = node_array[NEIGHBOR_ROWS, actv_node_ix]
    occ_neighbors_set = set(neighbors[np.where(node_array[3, neighbors] == 1)])

    if skip_ix is not None:
        occ_neighbors_set.remove(skip_ix)

    return occ_neighbors_set, node_array


""" searchers
"""


def point_exists(point:np.ndarray, points_dict:dict) -> bool:
    r"""
    Attributes
        point (np.ndarray) ::
        points_dict (dict) ::
    
    Returns (bool) : 
    """
    (x, y) = point
    
    if x in points_dict.keys():
        if y in points_dict[x]:
            return True
    return False


def _null_nodes_search(node_array, actv_node_ix) -> np.ndarray:
    r"""
    Returns (numpy.ndarray) :: 
    """
    neighbors = node_array[NEIGHBOR_ROWS, actv_node_ix]
    return np.where(neighbors == -1)[0]


""" updaters
"""


def _extend_array_width(
                            node_array:np.ndarray, 
                            min_width:int=None
                        ) -> np.ndarray:
    r"""
    Attributes
        node_array (numpy.ndarray) ::
        min_width (int) ::
    
    Returns (numpy.ndarray) : 
    """
    _, ncols = node_array.shape
    
    if min_width is None:
        min_width = ncols + 1

    _node_array = np.zeros(
                            [NUM_ATTRIBS, 2 ** len(np.binary_repr(min_width))], 
                            dtype=np.int64
                        )
    # unset bot identifiers
    _node_array[4, :] = -1

    # unset neighbour node identifier
    _node_array[NEIGHBOR_ROWS, :] = -1

    # copy values from `node_array`
    _node_array[:, :ncols] = node_array
    return _node_array


def _update_points_dict(point:np.ndarray, points_dict:dict, cur_ix:int):
    r"""
    Attributes
        point (numpy.ndaray) :: 
        points_dict (dict[int, dict[int, int]]) :: 
        cur_ix (int) :: 
    
    Returns (dict) : 
    """

    (x, y) = point
    if x in points_dict.keys():
        points_dict[x][y] = cur_ix
    else: points_dict[x] = {y: cur_ix}


def _link_current_node_graph( 
                                node_array:np.ndarray, 
                                points_dict:dict, 
                                cur_ix:int
                            ):
    r"""
    Attributes
        node_array (numpy.ndarray) ::
        points_dict (dict) :: 
        cur_ix (int) :: 
    
    Returns (numpy.ndarray) : 
    """

    (cur_x, cur_y) = node_array[(1, 2), cur_ix]
    layout = GRID_LAYOUT[DEFAULT_LAYOUT]
    for k, v in layout.items():
        relative_point = v['relative_point']
        
        # get absolute position of neighbour from relative coordinates
        point = (cur_x + relative_point[0], cur_y + relative_point[1])

        # get the index for the neighbouring node
        neighbor_ix = get_node_ix(point, points_dict)

        # if it exists, update neigbour information for both nodes
        if (neighbor_ix != -1):
            cur_row, neigbor_row = NEIGHBOR_ROWS[k], NEIGHBOR_ROWS[(k + 3) % 6]
            node_array[(cur_row, neigbor_row), 
                       (cur_ix, neighbor_ix)] = neighbor_ix, cur_ix


def contract_node(
                    node_array:np.ndarray, 
                    head_ix:int, 
                    tail_ix:int, 
                    option:str
                ) -> tuple:
    r"""
    Attributes
        node_array (numpy.ndarray) ::
        head_ix (int) :: 
        tail_ix (int) :: 
        option (str) :: 

    Returns (tuple[int]): 
    """
    h_node = node_array[:, head_ix:head_ix + 1]
    t_node = node_array[:, tail_ix:tail_ix + 1]

    assert option in ['fw', 'bw'], ValueError

    if option == "fw":
        t_node[(3, 4, 17), 0] = 0, -1, 0
        h_node[17] = _OCC_STATUS_CODES['c']
        return (head_ix,)

    elif option == "bw":
        h_node[(3, 4, 17), (0, 0, 0)] = 0, -1, 0
        t_node[17] = _OCC_STATUS_CODES['c']
        return (tail_ix,)

if __name__ == '__main__': pass