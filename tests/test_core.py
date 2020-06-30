import pytest

from .. amoebot.grid.trigrid import TriangularGrid
from .. amoebot.elements.node.manager import NodeManager
from .. amoebot.elements.stategen import StateGenerator


import sys
# it is hard to say what entails as sufficiently large
LARGE_INT = sys.maxsize

# set the number of cores for multiprocessing
N_CORES = 2

@pytest.fixture
def incr_recursionlimit():
    sys.setrecursionlimit(25000)

def test_trigrid_small():
    r""" test the triangular grid creation for small grids
    """
    x = y = 4
    g = TriangularGrid(x, y)
    points = g._get_grid()

    assert points.shape == (x, y, 2)


def test_trigrid_large():
    r""" test the triangular grid creation for large grids
    """
    x = y = LARGE_INT
    g = TriangularGrid(x, y)
    points = g._get_grid()

    assert points.shape == (x, y, 2)

def test_nodemanager_add_single_node():
    r"""
    """
    from amoebot.elements.node.core import Node

    point = [0, 0]
    nm = NodeManager(point)
    nm._add_node(point)
    
    assert ((len(nm.node_dict) == 1) and isinstance(nm.node_dict[0], Node))

def test_nodemanager_grid_builder():
    r"""
    """
    from amoebot.elements.node.core import Node

    x = y = 4
    g = TriangularGrid(x, y)
    points = g._get_grid()

    nm = NodeManager(points)
    nm.grid_builder()

    assert ((len(nm.node_dict) == x * y) and \
            (not any([not isinstance(v, Node) for _,v in nm.node_dict.items()])))

def test_amoebotmanager_add_single_bot():
    r"""
    """
    assert True

def test_amoebotmanager_activate_and_launch_agent():
    r"""
    """
    assert True

def test_agent_out_of_bounds():
    r"""
    """
    assert True

def test_agent_random_movement_async(incr_recursionlimit):
    r"""
    """

    incr_recursionlimit()

    x = y = 16
    n_bots = 2
    max_iter = 5

    g = TriangularGrid(x, y)
    points = g._get_grid()

    nm = NodeManager(points)
    nm.grid_builder()

    node_list = list(nm.get_node_dict.values())

    gen = StateGenerator(node_list, n_bots=n_bots)
    gen.manager.exec_async(n_cores=N_CORES, max_iter=max_iter)

    assert True

def test_agent_random_movement_sequential():
    r"""
    """

    x = y = 16
    n_bots = 2
    max_iter = 5

    g = TriangularGrid(x, y)
    points = g._get_grid()

    nm = NodeManager(points)
    nm.grid_builder()

    node_list = list(nm.get_node_dict.values())

    gen = StateGenerator(node_list, n_bots=n_bots)
    gen.manager.exec_sequential(max_iter=max_iter)

    assert True
