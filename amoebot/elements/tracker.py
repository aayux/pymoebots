import time
import json
import numpy as np

from numpy import array
from pathlib import Path

from ..extras.exceptions import InitializationError

class StateTracker(object):
    r""" 
    Keep track of particle states (configurations) in the current execution. 
    Write state information to JSON file for rendering.
    """
    def __init__(self, manager:object, config_num:str):
        # `AmoebotManager` object for keeping track of the amoebot dictionary
        self.manager: object = manager

        # identifying number for current run, created by `StateGenerator`
        self.config_num: str = config_num

        self._generate_trace(save_as=None)

    def collect_states(self, __bot_id:int, queue:object) -> object:
        r""" 
        Collect a single amoebot's information from the `AmoebotManager`. This 
        function is called asyncronously at the end of each particle activation,
        the state configuration is pushed into a queue.

        :return:    multiprocessing.Manager.Queue()
        """
        config = self._collect_config(self.manager.amoebots[__bot_id])
        queue.put([__bot_id, config])
        return queue

    def update(self, __bot_id:int, config:list):
        # complete path to the state file
        statefile = Path(self.store) / Path(self.save_as)

        # TODO optimize this block
        # read data from json file if it exists
        if statefile.exists():
            with open(statefile, 'r') as f:
                state_dict = json.load(f)
            
            # if current activation is not the newest
            if str(self.activation) in state_dict:
                # remove entries in and after current activation
                remove_keys = [key for key in state_dict.keys() \
                          if int(key) >= self.activation]
                for key in remove_keys: state_dict.pop(key)
        else:
            # map to store current state information
            state_dict = dict()

        state_dict[self.activation] = dict(mov_bot=__bot_id, config=config)

        # append state information to the json file
        with open(statefile, 'w') as f: json.dump(state_dict, f)

        self.activation += 1

        return (
                array(config['head_pos']), 
                array(config['tail_pos']), 
                array(config['port_labels'])
        )

    def _generate_trace(self, save_as:str=None):
        # current activation hashes into the state dictionary
        self.activation = 0

        # create hidden space 
        self.store = './.dumps/tracks'
        Path(self.store).mkdir(parents=True, exist_ok=True)

        # create a unique file for every run using config_num
        save_as = f'run-{self.config_num}'

        self.save_as = f'{save_as}.json'

    def write_terminal_state(self):
        r"""
        Similar to the `StateGenerator`, this function writes a the terminal 
        state of current execution that can be loaded for re-useability.
        """
        # create hidden space 
        term_store = './.dumps/term'
        Path(term_store).mkdir(parents=True, exist_ok=True)

        # create a unique file for every run using config_num
        save_as = f'run-{self.config_num}'
        
        # collect full state information from the amoebot manager
        vec_collector = np.vectorize(self._collect_config)
        config = vec_collector(self.manager.amoebots)

        statefile = Path(term_store) / Path(save_as)

        # append state information to the json file
        with open(statefile, 'w') as f: json.dump(config, f)

    def set_state(self, ix:int):
        r""" reset the state pointer starting at index
        """
        self.activation = ix
    
    def _collect_config(self, bot:object) -> dict:
        r""" return state for a single amoebot
        """
        config = dict(
                        head_pos=bot.head.position.tolist(),
                        tail_pos=bot.tail.position.tolist(),
                        port_labels=bot.port_labels.tolist()
                    )
        return config
