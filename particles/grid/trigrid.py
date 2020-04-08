from dataclasses import dataclass, field
from numpy import ndarray, array, arange, linspace
from .helpers import make_int_grid, make_uint_grid


@dataclass
class TriangularGrid(object):
    # number of points in the x directions
    x: int

    # number of points in the y directions
    y: int

    # bottom left most point
    origin: ndarray = field(default=array([0, 0]))

    # combined (x,y) grid
    grid: ndarray = field(default=None)

    # x component of grid
    grid_x: ndarray = field(default=None)

    # y component of grid
    grid_y: ndarray = field(default=None)

    def __post_init__(self):
        x = self.x
        y = self.y
        origin = self.origin

        # basic sanity checks
        if x < 1 or not isinstance(x, int):
            raise Exception(f"Unable to create graph. "
                            f"Variable y must be of type integer.")

        if y is None: y = x
        elif y < 1 or not isinstance(y, int):
            raise Exception(f"Unable to create graph. "
                            f"Variable y must be of type integer.")

        if not isinstance(origin, ndarray):
            if isinstance(origin, list): origin = array(origin) 
            else:
                raise Exception(f"Unable to create graph. "
                                f"Variable origin must be of type list "
                                f"or a numpy array.")

        # set the start points
        start_point_x = origin[0]
        start_point_y = origin[1]

        # set the end points
        end_point_x = origin[0] + (x * 2)
        end_point_y = origin[1] + y

        if start_point_x < 0:   # start x is negative

            # produce signed x components of the grid
            grid_x = make_int_grid(start=start_point_x, end=end_point_x, 
                                   rows=y, component='x')
        else:                   # start x is positive.
            # produce unsigned x components of the grid
            grid_x = make_uint_grid(start=start_point_x, end=end_point_x, 
                                    rows=y, component='x')

        if start_point_y < 0:
            grid_y = make_int_grid(start=start_point_y, end=end_point_y, 
                                   rows=y, component='y', columns=x)
        else:
            grid_y = make_uint_grid(start=start_point_y, end=end_point_y, 
                                    rows=y, component='y', columns=x)

        # offset odd rows by one
        for row in range(y): 
            if row % 2: grid_x[row] += 1

        # zip x and y components together into grid array
        grid = array([array([array([grid_x[ix][jx], 
                                    grid_y[ix][jx]]) for jx in range(x)]) \
                                                     for ix in range(y)])

        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid = grid

    def get_grid(self): return self.grid

    def get_grid_components(self): return [self.grid_x, self.grid_y]