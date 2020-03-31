from dataclasses import dataclass, field
from numpy import ndarray, array, arange, linspace
from reuseables import int_limits, uint_limits


@dataclass
class Grid:
    # number of points in the x directions
    x: int

    # number of points in the y directions
    y: int = field(default=None)

    # bottom left most point
    origin: ndarray = field(default=None)

    # Combined (x,y) grid
    grid: ndarray = field(default=None)

    # x component of grid
    grid_x: ndarray = field(default=None)

    # y component of grid
    grid_y: ndarray = field(default=None)

    def create_triangular_grid(self):

        # assigns class variables to method variable
        x = self.x
        y = self.y
        origin = self.origin
        int_grid = pick_int_grid
        uint_grid = pick_uint_grid

        # Makes sure that x is not less than 1 and that x is an int
        if x < 1 or not isinstance(x, int):
            raise Exception('Unable to create graph. Invalid x value.')

        # Makes sure that y is not None
        if y is None:
            y = x

        # Makes sure that y is not less than 1 and that y is an int
        if y < 1 or not isinstance(y, int):
            raise Exception('Unable to create graph. Invalid x value.')

        # Makes sure that origin is not None
        if origin is None:
            origin = array([0, 0])

        # Makes sure that origin is a ndarray
        if not isinstance(origin, ndarray):
            raise Exception('Unable to create graph. Origin is not of type ndarray')

        # Assigns origin x value as the start point component
        start_point_x = origin[0]

        # Assigns origin x value plus two times x
        end_point_x = origin[0] + (x * 2)

        # Assigns origin y value as the start point component
        start_point_y = origin[1]

        # Assigns origin y value plus y
        end_point_y = origin[1] + y

        # Checks if the start x component is negative
        if start_point_x < 0:

            # Uses class method stored in int_grid with corresponding parameters to produce x components of the grid.
            grid_x = int_grid(start=start_point_x, end=end_point_x, rows=y, component='x')

        # Start x component is positive.
        else:

            # Uses class method stored in uint_grid with corresponding parameters to produce x components of the grid.
            grid_x = uint_grid(start=start_point_x, end=end_point_x, rows=y, component='x')

        # Checks if the start y component is negative
        if start_point_y < 0:

            # Uses class method stored in int_grid with corresponding parameters to produce y components of the grid.
            grid_y = int_grid(start=start_point_y, end=end_point_y, rows=y, component='y', columns=x)

        # Start y component is positive.
        else:

            # Uses class method stored in uint_grid with corresponding parameters to produce y components of the grid.
            grid_y = uint_grid(start=start_point_y, end=end_point_y, rows=y, component='y', columns=x)

        # loop through rows to offset odd rows by one
        for row in range(y):

            # Creates variable to store result of modulus operation
            odd = row%2

            # checks if row is odd
            if odd:

                # Assign corresponding row itself plus 1
                grid_x[row] += 1

        # Zips x and y components together into grid points
        grid = array([array([array([grid_x[i][j], grid_y[i][j]]) for j in range(x)]) for i in range(y)])

        # Assign results to class variables
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid = grid

    def get_grid(self):
        return self.grid

    def get_grid_components(self):
        return [self.grid_x, self.grid_y]


# Utility Functions ###################################################################################################

def pick_int_grid(start=None, end=None, rows=None, component=None, columns=None):

    # Creating variables for upper and lower limits for signed ints
    lower_8 = int_limits[8][0]
    upper_8 = int_limits[8][1]
    lower_16 = int_limits[16][0]
    upper_16 = int_limits[16][1]
    lower_32 = int_limits[32][0]
    upper_32 = int_limits[32][1]

    # Checks if we will be working with an x component
    if component == 'x':

        # assigns appropriate x component grid based on size needs
        if start >= lower_8 and end <= upper_8:
            grid = array([arange(start, end, 2, dtype='int8') for _ in range(rows)])
        elif start >= lower_16 and end <= upper_16:
            grid = array([arange(start, end, 2, dtype='int16') for _ in range(rows)])
        elif start >= lower_32 and end <= upper_32:
            grid = array([arange(start, end, 2, dtype='int32') for _ in range(rows)])
        else:
            grid = array([arange(start, end, 2, dtype='int64') for _ in range(rows)])

    # Checks if we will be working with an y component
    elif component == 'y':

        # Assigns appropriate y component grid based on size needs
        if start >= lower_8 and end <= upper_8:
            grid = array([linspace(start + row, start + row, columns, dtype='int8') for row in range(rows)])
        elif start >= lower_16 and end <= upper_16:
            grid = array([linspace(start + row, start + row, columns, dtype='int16') for row in range(rows)])
        elif start >= lower_32 and end <= upper_32:
            grid = array([linspace(start + row, start + row, columns, dtype='int32') for row in range(rows)])
        else:
            grid = array([linspace(start + row, start + row, columns, dtype='int64') for row in range(rows)])

    return grid


def pick_uint_grid(start=None, end=None, rows=None, component=None, columns=None):

    # Creating variables for upper limits for unsigned ints
    upper_8 = uint_limits[8][1]
    upper_16 = uint_limits[16][1]
    upper_32 = uint_limits[32][1]

    # Checks if we will be working with an x component
    if component == 'x':

        # assigns appropriate x component grid based on size needs
        if start <= upper_8 and end <= upper_8:
            grid = array([arange(start, end, 2, dtype='uint8') for _ in range(rows)])
        elif start <= upper_16 and end <= upper_16:
            grid = array([arange(start, end, 2, dtype='uint16') for _ in range(rows)])
        elif start <= upper_32 and end <= upper_32:
            grid = array([arange(start, end, 2, dtype='uint32') for _ in range(rows)])
        else:
            grid = array([arange(start, end, 2, dtype='uint64') for _ in range(rows)])

    # Checks if we will be working with an y component
    elif component == 'y':

        # Assigns appropriate y component grid based on size needs
        if start <= upper_8 and end <= upper_8:
            grid = array([linspace(start + row, start + row, columns, dtype='uint8') for row in range(rows)])
        elif start <= upper_16 and end <= upper_16:
            grid = array([linspace(start + row, start + row, columns, dtype='uint16') for row in range(rows)])
        elif start <= upper_32 and end <= upper_32:
            grid = array([linspace(start + row, start + row, columns, dtype='uint32') for row in range(rows)])
        else:
            grid= array([linspace(start + row, start + row, columns, dtype='uint64') for row in range(rows)])

    return grid

# End of Utility Functions ############################################################################################