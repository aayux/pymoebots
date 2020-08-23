# -*- coding: utf-8 -*-

""" trigrid.py
"""

from .utils.limits import int_limits, uint_limits

import numpy as np

def int_grid_points(
                    start:int, 
                    end:int, 
                    component:str,
                    nrows:int, 
                    ncols:int=None
                ) -> np.array:
    r""" 
    Assign the correct signed integer subtype values to grid component.

    Attributes
        start (int) :: the starting point.
        end (int) :: the stopping point.
        component (str) :: one of `x' or 'y' indicating the grid direction for
                        generating current set of points.
        nrows (int) ::  number of rows in generation.
        ncols (int) default: None :: number of coulmns in generation.
    
    Returns (numpy.array): list of points in the direction of `component`
    """

    # upper and lower limits for signed int
    lower_8 = int_limits[8][0]
    upper_8 = int_limits[8][1]

    lower_16 = int_limits[16][0]
    upper_16 = int_limits[16][1]

    lower_32 = int_limits[32][0]
    upper_32 = int_limits[32][1]

    if component == 'x':    # working with an x component
        if start >= lower_8 and end <= upper_8:
            grid = np.array([np.arange(start, end, 2, 
                                 dtype='int8') for _ in range(nrows)])
        elif start >= lower_16 and end <= upper_16:
            grid = np.array([np.arange(start, end, 2, 
                                 dtype='int16') for _ in range(nrows)])
        elif start >= lower_32 and end <= upper_32:
            grid = np.array([np.arange(start, end, 2, 
                                 dtype='int32') for _ in range(nrows)])
        else:
            grid = np.array([np.arange(start, end, 2, 
                                 dtype='int64') for _ in range(nrows)])

    elif component == 'y':  # working with an y component
        if start >= lower_8 and end <= upper_8:
            grid = np.array([np.linspace(start + row, start + row, ncols, 
                                   dtype='int8') for row in range(nrows)])
        elif start >= lower_16 and end <= upper_16:
            grid = np.array([np.linspace(start + row, start + row, ncols, 
                                   dtype='int16') for row in range(nrows)])
        elif start >= lower_32 and end <= upper_32:
            grid = np.array([np.linspace(start + row, start + row, ncols, 
                                   dtype='int32') for row in range(nrows)])
        else:
            grid = np.array([np.linspace(start + row, start + row, ncols, 
                                   dtype='int64') for row in range(nrows)])
    return grid

def uint_grid_points(
                        start:int, 
                        end:int, 
                        component:str, 
                        nrows:int, 
                        ncols:int=None
                    ) -> np.array:
    r"""
    Assign the correct unsigned integer subtype values to grid component.

    Attributes
        start (int) :: the starting point.
        end (int) :: the stopping point.
        component (str) :: one of `x' or 'y' indicating the grid direction for
                        generating current set of points.
        nrows (int) :: number of rows in generation.
        ncols (int) default: None :: number of coulmns in generation.

    Returns (numpy.array): list of points in the direction of `component`
    """

    # limits for unsigned int
    lim_8 = uint_limits[8][1]
    lim_16 = uint_limits[16][1]
    lim_32 = uint_limits[32][1]

    if component == 'x':
        if start <= lim_8 and end <= lim_8:
            grid = np.array([np.arange(start, end, 2, 
                                 dtype='uint8') for _ in range(nrows)])
        elif start <= lim_16 and end <= lim_16:
            grid = np.array([np.arange(start, end, 2, 
                                 dtype='uint16') for _ in range(nrows)])
        elif start <= lim_32 and end <= lim_32:
            grid = np.array([np.arange(start, end, 2, 
                                 dtype='uint32') for _ in range(nrows)])
        else:
            grid = np.array([np.arange(start, end, 2, 
                                 dtype='uint64') for _ in range(nrows)])
    elif component == 'y':
        if start <= lim_8 and end <= lim_8:
            grid = np.array([np.linspace(start + row, start + row, ncols, 
                                   dtype='uint8') for row in range(nrows)])
        elif start <= lim_16 and end <= lim_16:
            grid = np.array([np.linspace(start + row, start + row, ncols, 
                                   dtype='uint16') for row in range(nrows)])
        elif start <= lim_32 and end <= lim_32:
            grid = np.array([np.linspace(start + row, start + row, ncols, 
                                   dtype='uint32') for row in range(nrows)])
        else:
            grid = np.array([np.linspace(start + row, start + row, ncols, 
                                  dtype='uint64') for row in range(nrows)])
    return grid

def make_triangular_grid(x:int, y:int=None, origin:object=None) -> np.array:
    r"""
    Generate points on the triangular grid.

    Attributes
        x (int) ::  number of grid points in x-direction
        y (int) default: None :: number of grid points in y-direction. Set equal
                        to `x` if None.
        origin (list or numpy.array) default: None :: anchor point for the grid,
                        typically a corner point
    
    Returns (numpy.array): list of points on the triangular grid.
    """

    # basic sanity checks
    if x < 1 or not isinstance(x, int):
        raise Exception(f"Unable to create graph. "
                        f"Variable x must be of type integer.")

    if y is None: y = x
    elif y < 1 or not isinstance(y, int):
        raise Exception(f"Unable to create graph. "
                        f"Variable y must be of type integer.")

    # set the origin if not set
    if origin is None:
        origin = np.array([0, 0])
    else:     
        if not isinstance(origin, np.ndarray):
            if isinstance(origin, list): 
                origin = np.array(origin) 
            else:
                raise Exception(
                            f"Unable to create graph. Variable `origin` must be"
                            f" of type list or a numpy array."
                )

    # set the start points
    start_point_x, start_point_y = origin

    # set the end points
    end_point_x = origin[0] + (x * 2)
    end_point_y = origin[1] + y

    # start x is negative
    if start_point_x < 0:

        # produce signed x components of the grid
        grid_x = int_grid_points(start=start_point_x, end=end_point_x, 
                                nrows=y, component='x')
    # start x is positive
    else:
        # produce unsigned x components of the grid
        grid_x = uint_grid_points(start=start_point_x, end=end_point_x, 
                                nrows=y, component='x')

    if start_point_y < 0:
        grid_y = int_grid_points(start=start_point_y, end=end_point_y, 
                                nrows=y, component='y', ncols=x)
    else:
        grid_y = uint_grid_points(start=start_point_y, end=end_point_y, 
                                nrows=y, component='y', ncols=x)

    # offset odd columns by one
    for row in range(y):
        if row % 2: grid_x[row] += 1

    # zip x and y components together into grid array
    grid = np.array([np.array([
                                np.array([grid_y[ix][jx], 
                                grid_x[ix][jx]]) for jx in range(x)]) \
                                                 for ix in range(y)])

    return grid