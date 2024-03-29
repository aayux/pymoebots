# -*- coding: utf-8 -*-

""" simulator.py
"""

import time
import psutil

from amoebot.utils.trigrid import make_triangular_grid
from amoebot.elements.node.manager import NodeManagerBitArray
from amoebot.elements.stategen import StateGenerator

# number of cpu cores available
N_CORES = psutil.cpu_count(logical=True)

class AmoebotSimulator(object):
    r"""
    Acts as the first layer of abstaction from the software functionalities. 
    Initialise the simulator by supplying arguments to this class. In future, 
    this module will also act as the entry point for attaching algorithmic 
    modules to the particles.

    Attributes

        generator (StateGenerator) :: object handle for `StateGenerator` class.
        max_rnds (int) :: maximum number of full rounds before termination.
        n_cores (int) :: number of processor cores to use.

    """

    def __init__(
                    self, 
                    algorithm:str,
                    shape:tuple=(64, 64), 
                    max_rnds:int=1000, 
                    n_bots:int=2, 
                    n_cores:int=N_CORES, 
                    config_num:str=None
                ):
        r"""
        Attributes

            algorithm (str) :: algorithm being performed in current step, one 
                                of "random_move", "compress".
            shape (tuple) default: (64, 64) :: number of grid points in 
                                x and y-directions respectively.
            max_rnds (int) default: 1000 :: maximum number of full rounds before 
                                termination.
            n_bots (int) default: 5 :: number of particles on the grid, unused 
                                if config_num is given.
            n_cores (int) default: N_CORES :: number of processor cores to use.
            config_num (str) default: N_CORES :: numeric identifier for the
                                configuration file with the initial system 
                                state. If not provided, randomly plave `n_bots` 
                                on the grid.
        """

        # generate the amoebot states and create storage dumps
        if config_num:
            self.generator = StateGenerator(config_num=config_num)
        else: raise NotImplementedError

        self.algorithm = algorithm
        self.max_rnds = max_rnds
        self.n_cores = n_cores

    def exec_sequential(self, time_it:bool=True) -> float:
        r""" 
        Execute algorithm(s) sequentially.

        Attributes

            time_it (bool) default: True :: set to True if execution is timed.
        
        Returns (float): total execution if `time_it` is True.
        """
        if time_it: t0 = time.time()

        x1, x2 = self.max_rnds, self.algorithm
        self.generator.manager.exec_sequential(max_rnds=x1, algorithm=x2)

        if time_it:
            return time.time() - t0

    def exec_async(self, time_it:bool=True) -> float:
        r""" 
        Execute algorithm(s) asynchronously.

        Attributes

            time_it (bool) default: True :: set to True if execution is timed.
        
        Returns (float): total execution if `time_it` is True.
        """
        if time_it: t0 = time.time()
        
        self.generator.manager.exec_async(
                                            n_cores=self.n_cores, 
                                            max_rnds=self.max_rnds,
                                            algorithm=self.algorithm
                                        )

        if time_it:
            return time.time() - t0

if __name__ == '__main__':

    sim = AmoebotSimulator('random_move')
    elapsed = sim.exec_sequential()

    print(f"time elapsed: {elapsed: .3f}s")