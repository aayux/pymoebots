import math

import amoebot.elements.node.manager as manager
import numpy as np
import random

single_bot_10_diameter_wall = {
    "bots": [[11, 21]],
    "bot tails": [[11, 21]],
    "walls": [
        [11, 11], [6, 16], [6, 26], [11, 31], [16, 26], [16, 16], [15, 15],
        [14, 14], [13, 13], [12, 12], [10, 12], [9, 13], [8, 14], [7, 15],
        [6, 18], [6, 20], [6, 22], [6, 24], [7, 27], [8, 28], [9, 29], [10, 30],
        [12, 30], [13, 29], [14, 28], [15, 27], [16, 24], [16, 22], [16, 20],
        [16, 18]
    ]
}

empty_1_bot = {
    "bots": [[11, 21]],
    "bot tails": [[11, 21]],
    "walls": [
    ]
}

def convert_walls_to_dictionary(data):
    d = {}
    for wall in data:
        if wall[0] not in d:
            d[wall[0]] = {wall[1]: True}
        elif wall[1] not in d[wall[0]]:
            d[wall[0]][wall[1]] = True

    return d

def existence(x, y, d):
    if x not in d:
        return False

    if y not in d[x]:
        return False

    return True

def get_loaded_nodes(data):
    points = np.zeros([4, len(data['bots'])])

    for ix, bot in enumerate(data['bots']):
        head_x, head_y = bot

        # Adds head and tail position to corresponding point positions
        positions = (head_x, head_y, head_x, head_y)
        points[(0, 1, 2, 3), (ix, ix, ix, ix)] = positions

    nm = manager.NodeManagerBitArray(
        points=points
    )

    for wall in data['walls']:
        wall_x, wall_y = wall
        nm.add_wall(point=(wall_x, wall_y))

    # print(nm.nodes)

    return nm.nodes


def get_nm_with_bot_0(data):
    return manager.NodeManagerBitArray(bot_id=0, nodes=get_loaded_nodes(data))

layout = {
    0: (-1, 1),
    1: (0, 2),
    2: (1, 1),
    3: (1, -1),
    4: (0, -2),
    5: (-1, -1),
}


def test_depth_validation():
    """
    Test the depth being returned.
    """
    nm = get_nm_with_bot_0(empty_1_bot)
    # Arbitrarily large number of loops
    _range = 2**9
    for i in range(_range):
        # picks random depth from 1 to number of loops
        depth = random.randint(1, _range + 2)

        # Checks if ping return is the same as depth.
        assert nm.ping_for_wall(port=depth % 6, depth=depth) == depth


def test_distance_calculation():
    """
    Test the ping function distance calculation
    """
    nm = get_nm_with_bot_0(single_bot_10_diameter_wall)
    a = []
    for i in range(6):
        a.append(nm.ping_for_wall(i, depth=10))
        assert nm.ping_for_wall(i, depth=10) == 5

    validation = convert_walls_to_dictionary(data=single_bot_10_diameter_wall["walls"])
    for _ in range(1000):
        # Randomly selects direction to move
        i = random.randint(0, 5)
        nm.move_to(i)
        nm.contract_forward()

        # Checks ping in all directions
        for j in range(6):
            direction = layout[j]
            cp = nm.current_position()
            cp_x = cp.item(0)
            cp_y = cp.item(1)
            test = 0
            # Add relative direction to current position until it's found in
            # validation dictionary
            while not existence(cp_x, cp_y, validation):
                cp_x += direction[0]
                cp_y += direction[1]
                test += 1

            # See if test count is the same as ping value
            assert nm.ping_for_wall(j, depth=10) == test
