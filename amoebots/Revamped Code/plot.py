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

            # Creating variables for upper and lower limits for signed ints
            lower_8 = int_limits[8][0]
            upper_8 = int_limits[8][1]
            lower_16 = int_limits[16][0]
            upper_16 = int_limits[16][1]
            lower_32 = int_limits[32][0]
            upper_32 = int_limits[32][1]

            # assigns appropriate x component grid based on size needs
            if start_point_x >= lower_8 and end_point_x <= upper_8:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='int8') for _ in range(y)])
            elif start_point_x >= lower_16 and end_point_x <= upper_16:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='int16') for _ in range(y)])
            elif start_point_x >= lower_32 and end_point_x <= upper_32:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='int32') for _ in range(y)])
            else:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='int64') for _ in range(y)])

        # Start x component is positive.
        else:

            # Creating variables for upper limits for unsigned ints
            upper_8 = uint_limits[8][1]
            upper_16 = uint_limits[16][1]
            upper_32 = uint_limits[32][1]

            # assigns appropriate x component grid based on size needs
            if start_point_x <= upper_8 and end_point_x <= upper_8:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='uint8') for _ in range(y)])
            elif start_point_x <= upper_16 and end_point_x <= upper_16:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='uint16') for _ in range(y)])
            elif start_point_x <= upper_32 and end_point_x <= upper_32:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='uint32') for _ in range(y)])
            else:
                grid_x = array([arange(start_point_x, end_point_x, 2, dtype='uint64') for _ in range(y)])

        # Checks if the start y component is negative
        if start_point_y < 0:

            # Creating variables for upper and lower limits for signed ints
            lower_8 = int_limits[8][0]
            upper_8 = int_limits[8][1]
            lower_16 = int_limits[16][0]
            upper_16 = int_limits[16][1]
            lower_32 = int_limits[32][0]
            upper_32 = int_limits[32][1]

            # Assigns appropriate y component grid based on size needs
            if start_point_y >= lower_8 and end_point_y <= upper_8:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='int8') for i in range(y)])
            elif start_point_y >= lower_16 and end_point_y <= upper_16:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='int16') for i in range(y)])
            elif start_point_y >= lower_32 and end_point_y <= upper_32:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='int32') for i in range(y)])
            else:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='int32') for i in range(y)])

        # Start y component is positive.
        else:

            # Creating variables for upper limits for unsigned ints
            upper_8 = uint_limits[8][1]
            upper_16 = uint_limits[16][1]
            upper_32 = uint_limits[32][1]

            # Assigns appropriate y component grid based on size needs
            if start_point_y <= upper_8 and end_point_y <= upper_8:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='uint8') for i in range(y)])
            elif start_point_y <= upper_16 and end_point_y <= upper_16:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='uint16') for i in range(y)])
            elif start_point_y <= upper_32 and end_point_y <= upper_32:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='uint32') for i in range(y)])
            else:
                grid_y = array([linspace(start_point_y + i, start_point_y + i, x, dtype='uint64') for i in range(y)])

        # loop through rows to offset odd rows by one
        for row in range(y):

            # Creates variable to store result of modulus operation
            odd = row%2

            # checks if row is odd
            if odd:

                # Assign corresponding row itself plus 1
                grid_x[row] += 1

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
