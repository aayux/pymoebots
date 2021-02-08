# -*- coding: utf-8 -*-

""" elements/stategen.py
"""

from .bot.agent import Agent
from .bot.manager import AmoebotManager
from .nodenv import NodeEnvManager
from ..utils.exceptions import InitializationError

import time
import json
import numpy as np
from pathlib import Path

STORE = './.dumps'


def config0_reader(config_num:str) -> list:
    r""" 
    Read a configuration with given config_num.

    Attributes

        config_num (str) :: identifier number for the json configuration file.
    
    Return (list): configuration data for each particle.
    """

    # complete path to the state file
    statefile = Path(STORE) / Path(f'run-{config_num}/init0.json')
    try:
        with open(statefile, 'r') as f:
            config0 = json.load(f)

    except FileNotFoundError:
        raise FileNotFoundError(
            f"{statefile} refers to a non-existent configuration file."
        )

    return config0


class StateGenerator(object):
    r"""
    Generate the initial configuration of the particle system states 
    for the current execution. Either read source input or generate a random 
    placement configuration of particles. The confi0 file is a one time write.

    This generator class also provides access to the `AmoebotManager` object.

    Attributes
        
        config_num (str) :: identifier number for the json configuration file.

        manager (AmoebotManager) :: object of class `AmoebotManager`.

    """

    def __init__(self, config_num:str=None, **kwargs):
        r"""
        Attributes
            config_num (str) default: None :: identifier number for the json 
                            configuration file.
        """

        # random placemet when no config_num is assigned
        if config_num is None:
            try:
                self.config_num = self._generate_init0()
                # currently throws `NotImplementedError`
                self._random_placement(kwargs['n_bots'])

            except KeyError:
                raise InitializationError(
                    f"Randomly placed bots require argument `n_bots`."
                )

            # self.write(config0)

        # place bots in configuration written in config_num
        else:
            self.config_num = config_num
            self.manager = self._config0_placement()

    def write(self, config0: list):
        r"""
        Dump `config0` to the json file.

        Attributes
            config0 (list) :: configuration state of the set of particles.
        """

        # create a working directory
        (Path(STORE) / Path(f'run-{self.config_num}')).mkdir(
                                                                parents=True, 
                                                                exist_ok=True
                                                            )

        # complete path to the state file
        statefile = Path(STORE) / Path(f'run-{self.config_num}/init0.json')

        # write state information to the json file
        with open(statefile, 'w') as f: json.dump(config0, f, indent=4)

    def _generate_init0(self, config_num:str = None) -> str:
        r"""
        Initialise the configuration essentials.

        Attributes
            config_num (str) :: identifier number for the json  configuration 
                            file.
        Return (str): configuration number for the current store.

        """
        # create a unique time stamp for every run
        if config_num is None:
            config_num = str(int(time.time()))

        return config_num

    def _collect_amoebot_states(self, bot: object) -> dict:
        r""" 
        Return state for a single amoebot

        Attributes
            bot (Amoebot) :: object of class `Amoebot`
        
        Return (dict): state dictionary for given object of class `Amoebot`.
        """
        # unpickle the byte-object for reading
        bot = Agent.unpickled(bot)

        state = dict(
                        head_pos=bot.head.tolist(),
                        tail_pos=bot.tail.tolist()
                )

        return state

    def _random_placement(self, n_bots:int) -> (AmoebotManager, list):
        r"""
        Place bots on an instance of `elements.node.core.Node` of the 
        triangular graph randomly.

        Attributes
            n_bots (int) :: number of particles (amoebots) to place.

        Return (tuple): a tuple with reference to `AmoebotManager` and a list of
                        the `config0` object.
        
        TODO rewrite this function for NodeManagerBitArray update
        """

        raise NotImplementedError

    def _config0_placement(self) -> AmoebotManager:
        r"""
        Collect state information from source place bots on the grid. 

        Return (AmoebotManager): object handler for manager class
        """

        manager = AmoebotManager(config_num=self.config_num)

        try:
            config0 = config0_reader(self.config_num)

        except FileNotFoundError:
            raise InitializationError(
                f"Configuration file not found."
            )

        # creates a placeholder for the particle position
        points = np.zeros([len(config0), 4])

        # add bot ix to the list at known position
        for ix, bot in enumerate(config0):
            h_point = bot['head_pos']
            t_point = bot['tail_pos']

            # ...
            assert np.all(h_point == t_point), \
                InitializationError(
                                "Ensure head and tail coordinates are the same "
                                "in configuration file.")

            x, y = h_point


            manager._add_bot(
                                np.uint8(ix),
                                point=np.array([x, y], dtype=np.uint8),
            )

            # populate points array with the correct head and tail co-ordinates
            points[ix, :] = (x, y, x, y)

        # intialise the node environment and set up points
        nenvm = NodeEnvManager(points=points)
        manager._copy_node_array(node_array=nenvm.node_array)

        return manager
