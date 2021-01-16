import numpy as np
import typing

NUMPY_INT_LEVELS = {
    'ints': {np.int8, np.int16, np.int32, np.int64},
    'int8': (-128, 127),
    'int16': (-32768, 32767),
    'int32': (-2147483648, 2147483647)
}

NUMBER_OF_ATTRIBUTES = 18
LAYOUT = 0
NODE_LAYOUT = {
    0: {  # Horizontal Layout
        0: {'relative_point': (-2, 0), 'direction': 'w'},
        1: {'relative_point': (-1, 1), 'direction': 'nw'},
        2: {'relative_point': (1, 1), 'direction': 'ne'},
        3: {'relative_point': (2, 0), 'direction': 'e'},
        4: {'relative_point': (1, -1), 'direction': 'se'},
        5: {'relative_point': (-1, -1), 'direction': 'sw'},
    },
    1: {  # Vertical Layout
        0: {'relative_point': (-1, 1), 'direction': 'nw'},
        1: {'relative_point': (0, 2), 'direction': 'n'},
        2: {'relative_point': (1, 1), 'direction': 'ne'},
        3: {'relative_point': (1, -1), 'direction': 'se'},
        4: {'relative_point': (0, -2), 'direction': 'se'},
        5: {'relative_point': (-1, -1), 'direction': 'sw'},
    },

}

NEIGHBOR_RANGE = np.arange(5, 11, dtype=int)

VERTICAL_LAYOUT = False


def add_point_ver_0(
        x: typing.Union[int, float],
        y: typing.Union[int, float],
        bot_id: int,
        current_index: int,
        nodes: np.ndarray,
        nodes_by_point,
):
    """
    Used with initial array set up. add_points checks and reconfigures the size
    of array

    :param x:
    :param y:
    :param bot_id:
    :param current_index:
    :param nodes:
    :param nodes_by_point:
    :return:
    """
    if check_points_existence_ver_0(nodes_by_point=nodes_by_point, x=x, y=y):
        return current_index

    x1 = current_index
    nodes[0:, x1:x1 + 1] = create_node_ver_0(x=x, y=y, bot_id=bot_id)
    x1, x2, x3 = current_index, nodes_by_point, nodes
    link_existing_nodes_ver_0(current_index=x1, nodes_by_point=x2, nodes=x3)
    x2 = nodes_by_point
    insert_point_into_dict_ver_0(x=x, y=y, current_index=x1, nodes_by_point=x2)
    return current_index + 1


def add_point_ver_1(
        x: typing.Union[int, float],
        y: typing.Union[int, float],
        nodes: np.ndarray,
        nodes_by_point,
):
    """
    add point without adding bot to the point, does not check points existence,
    does resize nodes if necessary.

    :param x:
    :param y:
    :param nodes:
    :param nodes_by_point:
    :return:
    """
    current_index = get_current_index_ver_0(nodes)

    if current_index == -1:
        nodes = increase_array_size_ver_0(size=nodes[0].size + 1, nodes=nodes)
        current_index = get_current_index_ver_0(nodes)

    x1 = current_index
    nodes[0:, x1:x1 + 1] = create_node_ver_1(x=x, y=y)
    x1, x2, x3 = current_index, nodes_by_point, nodes
    link_existing_nodes_ver_0(current_index=x1, nodes_by_point=x2, nodes=x3)
    x2 = nodes_by_point
    insert_point_into_dict_ver_0(x=x, y=y, current_index=x1, nodes_by_point=x2)
    return current_index, nodes


def add_points_ver_0(nodes: np.ndarray, points: np.ndarray,
                     nodes_by_point: typing.Dict[
                         int, typing.Dict[int, int]]) -> np.ndarray:
    points_size = points[0].size

    current_index = get_current_index_ver_0(nodes=nodes)
    nodes_size = nodes[0].size

    if nodes_size - current_index < points_size:
        size = current_index + 1 + points_size
        nodes = increase_array_size_ver_0(size=size, nodes=nodes)
    # nodes_by_point = nodes_by_point

    item = points.item
    for i in range(points_size):
        x, y, bot_id = item((0, i)), item((1, i)), i
        current_index = add_point_ver_0(x=x, y=y, bot_id=bot_id,
                                        current_index=current_index,
                                        nodes=nodes,
                                        nodes_by_point=nodes_by_point)

    return nodes


def check_points_existence_ver_0(
        nodes_by_point,
        x: typing.Union[int, float],
        y: typing.Union[int, float],
):
    if x in nodes_by_point:
        if y in nodes_by_point[x]:
            return True
    return False


def compress_ver_0(nodes, head_node_index, tail_node_index, option):
    head_node = get_node_via_index_ver_0(nodes, head_node_index)
    tail_node = get_node_via_index_ver_0(nodes, tail_node_index)

    if option == "forward":
        tail_node[(3, 4, 17), (0, 0, 0)] = 0, -1, 0
        head_node[17] = 3
        return (head_node_index,)

    if option == "backward":
        head_node[(3, 4, 17), (0, 0, 0)] = 0, -1, 0
        tail_node[17] = 3
        return (tail_node_index,)

def create_node_ver_0(
        x: typing.Union[int, float],
        y: typing.Union[int, float],
        bot_id: int,
):
    new_node = np.zeros([NUMBER_OF_ATTRIBUTES, 1])
    new_node[(0, 3), (0, 0)] += 1
    new_node[(1, 2, 4), (0, 0, 0)] = x, y, bot_id
    new_node[5:11, 0] += -1
    return new_node


def create_node_ver_1(
        x: typing.Union[int, float],
        y: typing.Union[int, float],
):
    new_node = np.zeros([NUMBER_OF_ATTRIBUTES, 1])
    new_node[(0,), (0,)] += 1
    new_node[(1, 2,), (0, 0,)] = x, y
    new_node[4:11, 0] += -1
    return new_node


def get_current_index_ver_0(nodes: np.array):
    open_spots = np.where(nodes[0] == 0)[0]

    return -1 if open_spots.size == 0 else open_spots.item(0)


def get_node_index_ver_0(
        x: typing.Union[int, float],
        y: typing.Union[int, float],
        nodes_by_point: typing.Dict[int, typing.Dict[int, int]],
):
    if x in nodes_by_point:
        nodes_by_point_x = nodes_by_point[x]
        if y in nodes_by_point_x:
            return nodes_by_point_x[y]
    return -1


def get_node_via_index_ver_0(nodes, index):
    return nodes[0:, index:index + 1]


def get_working_node_index_ver_0(nodes: np.ndarray, bot_id: int) -> tuple:
    index = np.where(nodes[4] == bot_id)[0]

    if index.size == 0:
        raise ValueError("Bot does not appear to be on any existing node")
    elif index.size == 1:
        return (index.item(0),)
    elif index.size == 2:
        head_tail_results = nodes[17][index]
        head_test = head_tail_results.item(0)
        tail_test = head_tail_results.item(1)
        if head_test == 1:
            return (index.item(0), index.item(1))
        return (index.item(1), index.item(0))
    else:
        raise ValueError("Bot is located on too many nodes")


def increase_array_size_ver_0(nodes: np.ndarray, size: int, ):
    binary_str = len(np.binary_repr(size))
    twod_size = [NUMBER_OF_ATTRIBUTES, 2 ** binary_str]
    new_array = np.zeros(twod_size, dtype=nodes.dtype)
    new_array[4:11, 0:] -= 1

    new_array[0:, 0:nodes[0].size] = nodes
    return new_array


def insert_point_into_dict_ver_0(
        x: typing.Union[int, float],
        y: typing.Union[int, float],
        nodes_by_point: typing.Dict[int, typing.Dict[int, int]],
        current_index: int
):
    if x in nodes_by_point:
        nodes_by_point[x][y] = current_index
    else:
        nodes_by_point[x] = {y: current_index}


def link_existing_nodes_ver_0(
        nodes: np.ndarray, current_index: int, nodes_by_point: dict
):
    current_x, current_y = nodes[(1, 2), (current_index, current_index)]
    current_layout = NODE_LAYOUT[LAYOUT]
    for k, v in current_layout.items():
        relative_point = v['relative_point']
        x1, x2 = current_x + relative_point[0], current_y + relative_point[1]
        x3 = nodes_by_point
        neighbor_index = get_node_index_ver_0(x=x1, y=x2, nodes_by_point=x3)
        exists = neighbor_index != -1
        if exists:
            x1, x2 = NEIGHBOR_RANGE[k], NEIGHBOR_RANGE[(k + 3) % 6]
            x3, x4 = current_index, neighbor_index
            nodes[(x1, x2), (x3, x4)] = x4, x3


def map_node_array_ver_0(nodes: np.ndarray, nodes_by_point: typing.Dict[
    int, typing.Dict[int, int]]) -> None:
    number_of_nodes = get_current_index_ver_0(nodes=nodes)
    if number_of_nodes == -1:
        number_of_nodes = nodes[0].size

    item = nodes.item
    for current_index in range(number_of_nodes):
        x1, x2 = current_index, nodes_by_point
        x = item((1, x1))
        y = item((2, x1))
        x3 = insert_point_into_dict_ver_0
        x3(x=x, y=y, nodes_by_point=x2, current_index=x1)
