from numpy import ndarray, array, arange, linspace
from ..utils.limits import int_limits, uint_limits

def make_int_grid(start:int, end:int, nrows:int, component:str,
                  ncols:int=None) -> array:
    r""" assign appropriate signed integer subtype to grid component
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
            grid = array([arange(start, end, 2, 
                                 dtype='int8') for _ in range(nrows)])
        elif start >= lower_16 and end <= upper_16:
            grid = array([arange(start, end, 2, 
                                 dtype='int16') for _ in range(nrows)])
        elif start >= lower_32 and end <= upper_32:
            grid = array([arange(start, end, 2, 
                                 dtype='int32') for _ in range(nrows)])
        else:
            grid = array([arange(start, end, 2, 
                                 dtype='int64') for _ in range(nrows)])

    elif component == 'y':  # working with an y component
        if start >= lower_8 and end <= upper_8:
            grid = array([linspace(start + row, start + row, ncols, 
                                   dtype='int8') for row in range(nrows)])
        elif start >= lower_16 and end <= upper_16:
            grid = array([linspace(start + row, start + row, ncols, 
                                   dtype='int16') for row in range(nrows)])
        elif start >= lower_32 and end <= upper_32:
            grid = array([linspace(start + row, start + row, ncols, 
                                   dtype='int32') for row in range(nrows)])
        else:
            grid = array([linspace(start + row, start + row, ncols, 
                                   dtype='int64') for row in range(nrows)])
    return grid


def make_uint_grid(start:int, end:int, nrows:int, component:str,
                   ncols:int=None) -> array:
    r""" assign appropriate unsigned integer subtype to grid component
    """

    # limits for unsigned int
    lim_8 = uint_limits[8][1]
    lim_16 = uint_limits[16][1]
    lim_32 = uint_limits[32][1]

    if component == 'x':
        if start <= lim_8 and end <= lim_8:
            grid = array([arange(start, end, 2, 
                                 dtype='uint8') for _ in range(nrows)])
        elif start <= lim_16 and end <= lim_16:
            grid = array([arange(start, end, 2, 
                                 dtype='uint16') for _ in range(nrows)])
        elif start <= lim_32 and end <= lim_32:
            grid = array([arange(start, end, 2, 
                                 dtype='uint32') for _ in range(nrows)])
        else:
            grid = array([arange(start, end, 2, 
                                 dtype='uint64') for _ in range(nrows)])
    elif component == 'y':
        if start <= lim_8 and end <= lim_8:
            grid = array([linspace(start + row, start + row, ncols, 
                                   dtype='uint8') for row in range(nrows)])
        elif start <= lim_16 and end <= lim_16:
            grid = array([linspace(start + row, start + row, ncols, 
                                   dtype='uint16') for row in range(nrows)])
        elif start <= lim_32 and end <= lim_32:
            grid = array([linspace(start + row, start + row, ncols, 
                                   dtype='uint32') for row in range(nrows)])
        else:
            grid= array([linspace(start + row, start + row, ncols, 
                                  dtype='uint64') for row in range(nrows)])
    return grid