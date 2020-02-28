from dataclasses import dataclass, field

import numpy as np


@dataclass
class Grid:
    x: int = field(default=np.uint8(2))
    y: int = field(default=None)
    origin: tuple = field(default=None)
    grid: np.ndarray = field(default=None)
    grid_x: np.ndarray = field(default=None)
    grid_y: np.ndarray = field(default=None)
    
    def create_triangular_grid(self):
        if not self.y:
            self.y = self.x
        
        if not self.origin:
            self.origin = (np.uint8(0), np.uint8(0))

        if self.x+self.origin[0] < np.uint8(128) and self.y+self.origin[1] < np.uint8(128):
            t_grid_x = np.empty((self.y, self.x), dtype="uint8")
            t_grid_y = np.empty((self.y, self.x), dtype="uint8")
            t_grid = np.empty((self.y, self.x, 2), dtype=tuple)
        elif self.x+self.origin[0] < np.uint16(32767) and self.y+self.origin[1] < np.uint16(32767):
            t_grid_x = np.empty((self.y, self.x), dtype="uint16")
            t_grid_y = np.empty((self.y, self.x), dtype="uint16")
            t_grid = np.empty((self.y, self.x, 2), dtype=tuple)

        for i in range(self.y):
            if i < np.uint8(128):
                if i % np.uint8(2):
                    t_grid_x[np.uint8(i)] = np.arange(self.origin[np.uint8(0)]+np.uint8(1),self.x*np.uint8(2),
                                                      np.uint8(2))
                    t_grid_y[np.uint8(i)] = np.linspace(self.origin[np.uint8(1)]+np.uint8(i),
                                                        self.origin[np.uint8(1)]+np.uint8(i), self.x)
                    t_grid[np.uint8(i)] = np.array([j for j in zip(t_grid_x[np.uint8(i)], t_grid_y[np.uint8(i)])])

                else:
                    t_grid_x[np.uint8(i)] = np.arange(self.origin[np.uint8(0)],self.x*np.uint8(2), np.uint8(2))
                    t_grid_y[np.uint8(i)] = np.linspace(self.origin[np.uint8(1)] + np.uint8(i),
                                                        self.origin[np.uint8(1)] + np.uint8(i), self.x)
                    t_grid[np.uint8(i)] = np.array([j for j in zip(t_grid_x[np.uint8(i)], t_grid_y[np.uint8(i)])])
            else:
                raise Exception("i is greater than 128 in plot.create_trangular_grid function")

        self.grid_x = t_grid_x
        self.grid_y = t_grid_y
        self.grid = t_grid

    def get_grid(self):
        return self.grid

    def get_grid_components(self):
        return [self.grid_x, self.grid_y]
            

if __name__ == "__main__":
    def test_initialization():
        grid = Grid()
        print(grid)
        
    def test_create_triangular_grid():
        grid = Grid()
        grid.create_triangular_grid()
        print(grid)
    
    def test_create_triangular_grid_larger_numbers():
        grid = Grid(x=np.uint8(15), y=13)
        grid.create_triangular_grid()
        print(grid)
        print(grid.grid_x.shape)
        print(grid.grid_y.shape)
        print(grid.grid)
        
    # test_initialization()
    # test_create_triangular_grid()
    test_create_triangular_grid_larger_numbers()
