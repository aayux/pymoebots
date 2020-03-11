from dataclasses import dataclass, field
from numpy import ndarray, array, arange, linspace


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

    # creates triangular version grid
    def create_triangular_grid(self):

        # assigns class variables to method variable
        x = self.x
        y = self.y
        origin = self.origin

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

            # assigns appropriate x component grid based on size needs
            if start_point_x > -129 and end_point_x < 127:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='int8') for _ in range(y)])
            elif start_point_x > -32769 and end_point_x < 32767:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='int16') for _ in range(y)])
            elif start_point_x > -2147483649 and end_point_x < 2147483647:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='int32') for _ in range(y)])
            else:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='int64') for _ in range(y)])

        # Start x component is positive.
        else:

            # assigns appropriate x component grid based on size needs
            if start_point_x < 256 and end_point_x < 256:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='uint8') for _ in range(y)])
            elif start_point_x < 65536 and end_point_x < 65536:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='uint16') for _ in range(y)])
            elif start_point_x < 4294967296 and end_point_x < 4294967296:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='uint32') for _ in range(y)])
            else:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='uint64') for _ in range(y)])

        # Checks if the start y component is negative
        if start_point_y < 0:

            # Assigns appropriate y component grid based on size needs
            if start_point_y > -129 and end_point_y < 127:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='int8') for i in range(y)])
            elif start_point_y > -32769 and end_point_y < 32767:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='int16') for i in range(y)])
            elif start_point_y > -2147483649 and end_point_y < 2147483647:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='int32') for i in range(y)])
            else:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='int32') for i in range(y)])

        # Start y component is positive.
        else:

            # Assigns appropriate y component grid based on size needs
            if start_point_y < 256 and end_point_y < 256:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='uint8') for i in range(y)])
            elif start_point_y < 65536 and end_point_y < 65536:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='uint16') for i in range(y)])
            elif start_point_y < 4294967296 and end_point_y < 4294967296:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='uint32') for i in range(y)])
            else:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='uint64') for i in range(y)])

        # Zip x and y components together into grid points
        grid = array([array([array([grid_x[i][j], grid_y[i][j]]) for j in range(y)]) for i in range(y)])

        # Assign results to class variables
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid = grid

    # returns entire grid
    def get_grid(self):
        return self.grid

    # returns grid components as a list of lists
    def get_grid_components(self):
        return [self.grid_x, self.grid_y]
