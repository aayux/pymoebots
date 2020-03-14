from numpy import array

def adding_to_array():
    a = array([[[0,0],[2,0],[4,0]],[[0,1],[2,1],[4,1]],[[0,2],[2,2],[4,2]]])
    print(f'{a[0::2]+1}')
    print(f'{a}')

# Grid Class Tests ####################################################################################################

from plot import Grid


def test_grid_initialization():

    # initializes grid as Grid Class
    grid = Grid(x=2)
    print(grid)


def test_grid_create_triangular_grid():

    # initializes grid as Grid Class
    grid = Grid(x=2)

    # calls method to create triangular grid
    grid.create_triangular_grid()
    print(grid)


def test_grid_create_triangular_grid_larger_numbers():

    # initializes grid as Grid Class
    grid = Grid(x=1000)

    # calls method to create triangular grid
    grid.create_triangular_grid()
    print(grid)

# End of Grid Class Tests #############################################################################################

# NodeManager Class Tests #############################################################################################

from node_manager import NodeManager


def test_nodemanager_initialization():

    # initializes node_manager as NodeManager Class
    node_manager = NodeManager()
    print(node_manager)

    # Uses NodeManager Class's initialize method to set default values
    node_manager.initialize()
    print(node_manager)


def test_nodemanager_check_duplicates():

    # initializes node_manager_a as NodeManager Class
    node_manager_a = NodeManager()

    # initializes node_manager_a as NodeManager Class
    node_manager_b = NodeManager()

    # checks if node_manager_a and node_manager_b are the same
    same = node_manager_a is node_manager_b
    print(f"Node managers are the same: {same}")

    # checks if node_manager_a.next_index and node_manager_b.next_index are the same
    same = node_manager_a.next_index is node_manager_b.next_index
    print(f"Next indices are the same: {same}")

    # checks if node_manager_a.plotted_points and node_manager_b.plotted_points are the same
    same = node_manager_a.plotted_points is node_manager_b.plotted_points
    print(f"Next plotted points are the same: {same}")

    # checks if node_manager_a.node_dict and node_manager_b.node_dict are the same
    same = node_manager_a.node_dict is node_manager_b.node_dict
    print(f"Node dictionary points are the same: {same}")

    # Uses NodeManager Class's initialize method to set default values
    node_manager_a.initialize()

    # Uses NodeManager Class's initialize method to set default values
    node_manager_b.initialize()

    # checks if node_manager_a and node_manager_b are the same
    same = node_manager_a is node_manager_b
    print(f"Node managers are the same: {same}")

    # checks if node_manager_a.next_index and node_manager_b.next_index are the same
    same = node_manager_a.next_index is node_manager_b.next_index
    print(f"Next indices are the same: {same}")

    # checks if node_manager_a.plotted_points and node_manager_b.plotted_points are the same
    same = node_manager_a.plotted_points is node_manager_b.plotted_points
    print(f"Next plotted points are the same: {same}")

    # checks if node_manager_a.node_dict and node_manager_b.node_dict are the same
    same = node_manager_a.node_dict is node_manager_b.node_dict
    print(f"Node dictionary points are the same: {same}")

def test_nodemanager_add_node():

    # initializes node_manager as NodeManager Class
    node_manager = NodeManager()

    # Uses NodeManager Class's initialize method to set default values
    node_manager.initialize()

    # Creates artificial point
    point = [0,0]

    # Uses NodeManager Class's add_node method with position variable to add node to node manager
    node_manager.add_node(position=point)
    print(node_manager)


def test_nodemanager_add_node_multiple():

    # initializes node_manager as NodeManager Class
    node_manager = NodeManager()

    # Uses NodeManager Class's initialize method to set default values
    node_manager.initialize()

    # Creates artificial point
    point = [0, 0]

    # Creates arbitrary number
    num = 5

    # loops through to add multiple nodes
    for i in range(num):
        # Uses NodeManager Class's add_node method with position variable to add node to node manager
        node_manager.add_node(position=point)

        # Creates copy of point
        point = point[:]

        # Increments point's x value by one
        point[0] += 1

    print(node_manager)

def test_nodemanager_add_node_multiple_with_Grid():

    # initializes node_manager as NodeManager Class
    node_manager = NodeManager()

    # Uses NodeManager Class's initialize method to set default values
    node_manager.initialize()

    # initializes grid as Grid Class
    grid = Grid(x=3)

    # calls method to create triangular grid
    grid.create_triangular_grid()

    # calls method to retrieve plot from Grid class
    points = grid.get_grid()

    # Creates variable for the rows in points
    rows = len(points)

    # Creates variable for the columns in points
    columns = len(points[0])

    # loops through the number of rows to add nodes
    for i in range(rows):

        # loops through the number of columns to add nodes
        for j in range(columns):

            # Creates point based on data at point[i][j]
            point = points[i][j]

            # Uses NodeManager Class's add_node method with position variable to add node to node manager
            node_manager.add_node(position=point)

    print(node_manager)

def test_nodemanager_create_node_structure():

    # initializes node_manager as NodeManager Class
    node_manager = NodeManager()

    # Uses NodeManager Class's initialize method to set default values
    node_manager.initialize()

    # initializes grid as Grid Class
    grid = Grid(x=2, y=3)

    # calls method to create triangular grid
    grid.create_triangular_grid()

    # calls method to retrieve plot from Grid class
    points = grid.get_grid()

    # Use node manager's method, set_plotted_points, to transfer grid points
    node_manager.set_plotted_points(plotted_points=points)

    # Use node manager's method, create_node_structure, to build and connect all the node across the grid
    node_manager.create_node_structure()

    return

# End of NodeManager Class Tests ######################################################################################

# Node Class Tests ####################################################################################################

from node_skeleton import Node

# End of Node Class Tests #############################################################################################

# BotManager Class Tests ##############################################################################################

from bot_manager import BotManager

def test_bot_manager_initialization():

    # initializes bot_manager as BotManager Class
    bot_manager = BotManager()

    # Uses BotManager Class's initialize method to set default values
    bot_manager.initialize()

    return


# End of BotManager Class Tests #######################################################################################


if __name__ == "__main__":
    # adding_to_array()
##### Grid Class Tests ################################################################################################
    # test_grid_initialization()
    # test_grid_create_triangular_grid()
    # test_grid_create_triangular_grid_larger_numbers()
##### End of Grid Class Tests #########################################################################################
# NodeManager Class Tests #############################################################################################
    # test_nodemanager_initialization()
    # test_nodemanager_check_duplicates()
    # test_nodemanager_add_node()
    # test_nodemanager_add_node_multiple()
    # test_nodemanager_add_node_multiple_with_Grid()
    #test_nodemanager_create_node_structure()
# End of NodeManager Class Tests ######################################################################################
# Node Class Tests ####################################################################################################
# End of Node Class Tests #############################################################################################
# BotManager Class Tests ##############################################################################################
    #test_bot_manager_initialization()
# End of BotManager Class Tests #######################################################################################
    pass
