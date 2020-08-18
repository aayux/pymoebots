import time
import psutil

# number of cpu cores available
N_CORES = psutil.cpu_count(logical=True)

from .grid.trigrid import TriangularGrid
from .elements.node.manager import NodeManager
from .elements.stategen import StateGenerator

class AmoebotSimulator(object):
    def __init__(
                    self, 
                    xdim:int=64, 
                    ydim:int=64, 
                    max_iter:int=500, 
                    n_bots:int=2, 
                    n_cores:int=N_CORES, 
                    config_num:str=None
                ):
        # generate the triangular grid
        g = TriangularGrid(xdim, ydim)
        
        # launch a node manager instance
        nm = NodeManager(g.get_grid_points)

        # generate the amoebot states and create storage dumps
        if config_num:
            self.generator = StateGenerator(nm, config_num=config_num)
        else: 
            self.generator = StateGenerator(nm, n_bots=n_bots)

        self.max_iter = max_iter
        self.n_cores = n_cores

    def exec_async(self, time_it:bool=True) -> float:
        if time_it: t0 = time.time()
        
        self.generator.manager.exec_async(
                                            n_cores=self.n_cores, 
                                            max_iter=self.max_iter
                                        )

        if time_it:
            return time.time() - t0