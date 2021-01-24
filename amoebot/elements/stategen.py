# -*- coding: utf-8 -*-

""" elements/stategen.py
"""

from .bot.agent import Agent
from .bot.manager import AmoebotManager
from ..utils.exceptions import InitializationError
from amoebot.elements.node.manager import NodeManagerBitArray

import time
import json
import numpy as np
from pathlib import Path

STORE = './.dumps'


def config0_reader(config_num: str) -> list:
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

    def __init__(self, node_manager: object = None, config_num: str = None,
                 **kwargs):
        r"""
        Attributes
            node_manager (NodeManager) :: object of class `NodeManager`.

            config_num (str) default: None :: identifier number for the json 
                            configuration file.
        """

        # random placemet when no config_num is assigned
        if config_num is None:
            try:
                self.config_num = self._generate_init0()
                self.manager, config0 = self._random_placement(kwargs['n_bots'],
                                                               node_manager)
            except KeyError:
                raise InitializationError(
                    f"Randomly placed bots require argument `n_bots`."
                )

            self.write(config0)

        # place bots in configuration written in config_num
        else:
            self.config_num = config_num
            # _ = self._generate_init0(config_num=config_num)
            self.manager, config0 = self._config0_placement(node_manager)

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

    def _generate_init0(self, config_num: str = None) -> str:
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

    def _random_placement(self, n_bots: int,
                          node_manager: object) -> (AmoebotManager, list):
        r"""
        Place bots on an instance of `elements.node.core.Node` of the 
        triangular graph randomly.

        Attributes
            n_bots (int) :: number of particles (amoebots) to place.
            node_manager (NodeManager) :: reference to `NodeManager` object.
        
        Return (tuple): a tuple with reference to `AmoebotManager` and a list of
                        the `config0` object.
        """

        manager = AmoebotManager(node_manager.get_nmap, self.config_num)

        n_points, _ = node_manager.grid_points.shape
        rand_ixs = np.random.choice(range(n_points), size=n_bots)

        # add bot to the list at random node position
        for ix, position in enumerate(node_manager.grid_points[rand_ixs]):
            manager._add_bot(np.uint8(ix), head=position)

        # collect state information from the amoebot manager
        vec_collector = np.vectorize(self._collect_amoebot_states)
        config0 = vec_collector(list(manager.amoebots.values()))

        return manager, config0.tolist()

    def _config0_placement(self, node_manager: object) -> (
    AmoebotManager, list):
        r"""
        Collect state information from source place bots on the grid. 

        Attributes
            node_manager (NodeManager) :: reference to `NodeManager` object.

        Return (AmoebotManager): object handler for manager class
        """

        manager = AmoebotManager(config_num=self.config_num)

        try:
            config0 = config0_reader(self.config_num)

        except FileNotFoundError:
            raise InitializationError(
                f"Configuration file looks incorrect."
            )

        # creates a placeholder for the head and tail positions
        points = np.zeros([4, len(config0)])

        # add bot to the list at known position
        for ix, bot in enumerate(config0):  # ix corresponds to bot_id
            head_x, head_y = bot['head_pos']
            tail_x, tail_y = bot['tail_pos']
            manager._add_bot(
                np.uint8(ix),
                head=np.array([head_x, head_y], dtype=np.uint8),
                tail=np.array([head_x, head_y], dtype=np.uint8)
            )

            # Adds head and tail position to corresponding point positions
            positions = (head_x, head_y, tail_x, tail_y)
            points[(0, 1, 2, 3), (ix, ix, ix, ix)] = positions

        manager.load_env(value=NodeManagerBitArray(points=points).nodes)

        return manager, config0
