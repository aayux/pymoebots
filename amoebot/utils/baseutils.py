from numpy import int8, int16, int32, uint8, uint16, uint32, uint64

int_limits = {int8(8): [int8(-128), int8(127)],
              int8(16): [int16(-32768), int16(32767)],
              int8(32): [int32(-2147483648), int32(2147483647)]
              }

uint_limits = {uint8(8): [uint8(0), uint8(255)],
               uint8(16): [uint8(0), uint16(65535)],
               uint8(32): [uint8(0), uint32(4294967295)]
               }


def increment_index(ix:object) -> object:
    # variables for limits of unsigned intsegers
    lo_8 = uint_limits[int8(8)][1]
    lo_16 = uint_limits[int8(16)][1]
    lo_32 = uint_limits[int8(32)][1]

    if ix < lo_8: ix += uint8(1)
    elif ix < lo_16: ix += uint16(1)
    elif ix < lo_32: ix += uint32(1)
    else: ix += uint64(1)

    return ix