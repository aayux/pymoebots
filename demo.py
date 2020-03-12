from dataclasses import dataclass, field
from numpy import uint8, ndarray, array, int8

@dataclass
class Demo:
    intbit: int8 = field(default=None)

    def add_int8(self):
        self.intbit += uint8(1)

def test_int8():
    a = Demo(int8(-128))
    a.add_int8()
    return a.intbit

if __name__ == '__main__':
    print(f'{test_int8()}')