import pytest
import random

from .. amoebot.grid.trigrid import TriangularGrid
from .. amoebot.elements.node.manager import NodeManager
from .. amoebot.elements.bot.manager import AmoebotManager


@pytest.fixture
def large_integer():
    r""" 
    it is hard to say what entails as sufficiently large, so might as well go 
    all the way
    """
    import sys
    return sys.maxint


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
    x = y = large_integer()
    g = TriangularGrid(x, y)
    points = g._get_grid()

    assert points.shape == (x, y, 2)

def test_nodemanager_add_single_node():
    r"""
    """
    from .. amoebot.elements.node.core import Node

    point = [0, 0]
    nm = NodeManager(point)
    nm._add_node(point)
    
    assert ((len(nm.node_dict) == 1) and isinstance(nm.node_dict[0], Node))

def test_nodemanager_grid_builder():
    r"""
    """
    from .. amoebot.elements.node.core import Node

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

def test_agent_random_movement():
    r"""
    """
    x = y = 16
    n_bots = 4
    n_rounds = 50

    g = TriangularGrid(x, y)
    points = g._get_grid()

    nm = NodeManager(points)
    nm.grid_builder()
    nodes = nm._get_node_dict()

    am = AmoebotManager()
    am.random_placement(n_bots, list(nodes.values()))

    _round = 0
    while _round < n_rounds:
        _ = am.m_activate()
        _round += 1

    assert True

def test_tracker_random_movement():
    r"""
    """

    from .. amoebot.functional.tracker import StateTracker

    x = y = 16
    n_bots = 4
    n_rounds = 50

    g = TriangularGrid(x, y)
    points = g._get_grid()

    nm = NodeManager(points)
    nm.grid_builder()
    nodes = nm._get_node_dict()

    am = AmoebotManager()
    am.random_placement(n_bots, list(nodes.values()))

    # intialise the tracking object
    t = StateTracker()

    _round = 0
    while _round < n_rounds:

        _ = am.m_activate()
        t.collect_states(am)

        _round += 1

    assert True