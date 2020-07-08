from numpy import ndarray, array, arange, linspace
from .helpers import make_int_grid, make_uint_grid

class TriangularGrid(object):
    def __init__(self, x, y):
        # number of points in the x directions
        self.x: int = x

        # number of points in the y directions
        self.y: int = y

        # bottom left most point
        self.origin: ndarray = array([0, 0])

        # basic sanity checks
        if self.x < 1 or not isinstance(self.x, int):
            raise Exception(f"Unable to create graph. "
                            f"Variable y must be of type integer.")

        if self.y is None: self.y = self.x
        elif self.y < 1 or not isinstance(self.y, int):
            raise Exception(f"Unable to create graph. "
                            f"Variable y must be of type integer.")

        if not isinstance(self.origin, ndarray):
            if isinstance(self.origin, list): self.origin = array(self.origin) 
            else:
                raise Exception(f"Unable to create graph. "
                                f"Variable origin must be of type list "
                                f"or a numpy array.")

        # set the start points
        start_point_x = self.origin[0]
        start_point_y = self.origin[1]

        # set the end points
        end_point_x = self.origin[0] + (self.x * 2)
        end_point_y = self.origin[1] + self.y

        if start_point_x < 0:   # start x is negative

            # produce signed x components of the grid
            grid_x = make_int_grid(start=start_point_x, end=end_point_x, 
                                   nrows=self.y, component='x')
        else:                   # start x is positive.
            # produce unsigned x components of the grid
            grid_x = make_uint_grid(start=start_point_x, end=end_point_x, 
                                    nrows=self.y, component='x')

        if start_point_y < 0:
            grid_y = make_int_grid(start=start_point_y, end=end_point_y, 
                                   nrows=self.y, component='y', ncols=self.x)
        else:
            grid_y = make_uint_grid(start=start_point_y, end=end_point_y, 
                                    nrows=self.y, component='y', ncols=self.x)

        # offset odd rows by one
        for row in range(self.y): 
            if row % 2: grid_x[row] += 1

        # zip x and y components together into grid array
        grid = array([array([array([grid_y[ix][jx], 
                                    grid_x[ix][jx]]) for jx in range(self.x)]) \
                                                     for ix in range(self.y)])

        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid = grid

    @property
    def get_grid(self): return self.grid

    @property
    def get_grid_components(self): return (self.grid_x, self.grid_y)