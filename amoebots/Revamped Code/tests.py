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


if __name__ == "__main__":
##### Grid Class Tests ################################################################################################
    # test_grid_initialization()
    # test_grid_create_triangular_grid()
    # test_grid_create_triangular_grid_larger_numbers()
##### End of Grid Class Tests #########################################################################################
    pass
