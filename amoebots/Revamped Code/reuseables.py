from numpy import int8, int16, int32, uint8, uint16, uint32, uint64

int_limits = {int8(8): [int8(-128), int8(127)],
              int8(16): [int16(-32768), int16(32767)],
              int8(32): [int32(-2147483648), int32(2147483647)]
              }

uint_limits = {uint8(8): [uint8(0), uint8(255)],
               uint8(16): [uint8(0), uint16(65535)],
               uint8(32): [uint8(0), uint32(4294967295)]
               }


def increase_index(index):
    # Creating variables for upper limits for unsigned ints
    upper_8 = uint_limits[int8(8)][1]
    upper_16 = uint_limits[int8(16)][1]
    upper_32 = uint_limits[int8(32)][1]

    # Increments index by appropriate amount and type
    if index < upper_8:
        index += uint8(1)
    elif index < upper_16:
        index += uint16(1)
    elif index < upper_32:
        index += uint32(1)
    else:
        index += uint64(1)

    return index
