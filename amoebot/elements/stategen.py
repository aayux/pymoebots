import time
import json
import numpy as np
from pathlib import Path
from numpy import array, uint8

from .bot.agent import Agent
from .bot.manager import AmoebotManager
from ..utils.exceptions import InitializationError

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
    def __init__(self, node_manager:object, config_num:str=None, **kwargs):

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

        else:
            self.config_num = config_num
            _ = self._generate_init0(config_num=config_num)
            self.manager, config0 = self._config0_placement(node_manager)

    def write(self, config0:list):
        # create a working directory
        (Path(STORE) / Path(f'run-{self.config_num}')).mkdir(
                                                                parents=True, 
                                                                exist_ok=True
                                                            )
        
        # complete path to the state file
        statefile = Path(STORE) / Path(f'run-{self.config_num}/init0.json')

        # write state information to the json file
        with open(statefile, 'w') as f: json.dump(config0, f, indent=4)

    def _generate_init0(self, config_num:str=None) -> str:
        # create a unique time stamp for every run
        if config_num is None:
            config_num = str(int(time.time()))

        return config_num

    def _collect_amoebot_states(self, bot:object) -> dict:
        r""" return state for a single amoebot
        """
        # unpickle the byte-object for reading
        bot = Agent.unpickled(bot)
        state = dict(
                        head_pos=bot.head.tolist(),
                        tail_pos=bot.tail.tolist()
                    )
        return state
    
    def _random_placement(self, n_bots:int, 
                          node_manager:object) -> (AmoebotManager, list):
        r"""
        places bots on an instance of `elements.node.core.Node` of the 
        triangular graph randomly
        """

        manager = AmoebotManager(node_manager.get_nmap, self.config_num)

        n_points, _ = node_manager.grid_points.shape
        rand_ixs = np.random.choice(range(n_points), size=n_bots)

        # add bot to the list at random node position
        for ix, position in enumerate(node_manager.grid_points[rand_ixs]): 
            manager._add_bot(uint8(ix), head=position)

        # collect state information from the amoebot manager
        vec_collector = np.vectorize(self._collect_amoebot_states)
        config0 = vec_collector(list(manager.amoebots.values()))

        return manager, config0.tolist()

    def _config0_placement(self, node_manager:object) -> AmoebotManager:
        r""" 
        Collect state information from source place bots on the grid. 

        returns: AmoebotManager : object handler for manager class
        """
        manager = AmoebotManager(node_manager.get_nmap, self.config_num)

        try:
            config0 = config0_reader(self.config_num)
        except FileNotFoundError:
                raise InitializationError(
                            f"Configuration file looks incorrect."
                )

        # add bot to the list at known position
        for ix, bot in enumerate(config0):
            manager._add_bot(
                                uint8(ix), 
                                head=array(bot['head_pos'], dtype=uint8), 
                                tail=array(bot['tail_pos'], dtype=uint8)
                            )

        return manager, config0

