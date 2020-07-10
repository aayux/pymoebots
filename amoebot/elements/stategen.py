import time
import json
import numpy as np

from pathlib import Path

from .bot.manager import AmoebotManager
from ..utils.exceptions import InitializationError

STORE = './.dumps/init0'

def config0_reader(node_list:list, config_num:str) -> list:
    r""" read a config0 with given config_num
    """

    # complete path to the state file
    statefile = Path(STORE) / Path(f'run-{config_num}.json')
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
    def __init__(self, node_list:list, config0:list=None, **kwargs):

        self.config_num: str = self._generate_init0(save_as=None)

        if config0 is None:
            try: 
                self.manager, config0 = self._random_placement(kwargs['n_bots'], 
                                                               node_list)
            except KeyError:
                raise InitializationError(
                            f"Randomly placed bots require argument `n_bots`."
                )

        else:
            self.manager = self.collect_states(node_list, config0)
        
        self.write(config0)

    def collect_states(self, node_list:list, 
                       config0:dict) -> AmoebotManager:
        r""" 
        Collect state information from source place bots on the grid. 

        returns: AmoebotManager : object handler for manager class
        """
        raise NotImplementedError

    def write(self, config0:list):
        # complete path to the state file
        statefile = Path(STORE) / Path(self.save_as)

        # write state information to the json file
        with open(statefile, 'w') as f: json.dump(config0, f, indent=4)

    def _generate_init0(self, save_as:str=None) -> str:
        # create hidden space 
        Path(STORE).mkdir(parents=True, exist_ok=True)

        # create a unique time stamp for every run
        if save_as is None:
            config_num = int(time.time())
            save_as = f'run-{config_num}'

        self.save_as = f'{save_as}.json'

        return config_num

    def _collect_amoebot_states(self, bot:object) -> dict:
        r""" return state for a single amoebot
        """
        state = dict(
                        head_pos=bot.head.position.tolist(),
                        tail_pos=bot.tail.position.tolist(),
                        port_labels=bot.port_labels.tolist()
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
