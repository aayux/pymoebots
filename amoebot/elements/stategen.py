import time
import json
import numpy as np

from pathlib import Path
from numpy import array, uint8

from .bot.manager import AmoebotManager
from ..utils.exceptions import InitializationError
from ..utils.algorithms import binary_search

STORE = './.dumps'

def config0_reader(config_num:str) -> list:
    r""" read a configuration with given config_num
    """

    # complete path to the state file
    statefile = Path(STORE) / Path(f'run-{config_num}/init0.json')
    try:
        with open(statefile, 'r') as f: config0 = json.load(f)
    
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
    """
    def __init__(self, node_list:list, config_num:str=None, **kwargs):

        if config_num is None:
            try: 
                self.config_num = self._generate_init0()
                self.manager, config0 = self._random_placement(kwargs['n_bots'], 
                                                               node_list)
            except KeyError:
                raise InitializationError(
                            f"Randomly placed bots require argument `n_bots`."
                )
            
            self.write(config0)

        else:
            self.config_num = config_num
            try: 
                _ = self._generate_init0(config_num=config_num)
                self.manager, config0 = self._config0_placement(node_list)
            except KeyError:
                raise InitializationError(
                            f"Bots from config require argument `points`."
                )

    def write(self, config0:list):
        # complete path to the state file
        statefile = Path(STORE) / Path(f'run-{self.config_num}/init0.json')

        # write state information to the json file
        with open(statefile, 'w') as f: json.dump(config0, f, indent=4)

    def _generate_init0(self, config_num:str=None) -> str:
        # create a unique time stamp for every run
        if config_num is None:
            config_num = str(time.time())

        return config_num

    def _collect_amoebot_states(self, bot:object) -> dict:
        r""" return state for a single amoebot
        """
        state = dict(
                        head_pos=bot.head.position.tolist(),
                        tail_pos=bot.tail.position.tolist()
                    )
        return state
    
    def _random_placement(self, n_bots:int, 
                          node_list:list) -> (AmoebotManager, list):
        r"""
        places bots on an instance of `elements.node.core.Node` of the 
        triangular graph randomly
        """

        manager = AmoebotManager(self.config_num)

        node_list = np.asarray(node_list)
        np.random.shuffle(node_list)

        # add bot to the list at random node position
        for ix in range(n_bots): manager._add_bot(ix, node_list[ix])

        # collect state information from the amoebot manager
        vec_collector = np.vectorize(self._collect_amoebot_states)
        config0 = vec_collector(manager.amoebots)

        return manager, config0.tolist()

    def _config0_placement(self, node_list:list) -> AmoebotManager:
        r""" 
        Collect state information from source place bots on the grid. 

        returns: AmoebotManager : object handler for manager class
        """
        manager = AmoebotManager(self.config_num)

        try:
            config0 = config0_reader(self.config_num)
        except FileNotFoundError:
                raise InitializationError(
                            f"Configuration file looks incorrect."
                )

        node_list_pos = array([node.position for node in node_list], 
                                                            dtype=uint8)

        # add bot to the list at known position
        for ix, bot in enumerate(config0):
            node_ix = binary_search(node_list_pos, key=bot['head_pos'])
            # NOTE we assume head and tail positions are same at config0
            manager._add_bot(ix, node_list[node_ix])

        return manager, config0

