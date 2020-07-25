import json
import numpy as np

from pathlib import Path
from numpy import array, uint8

from ..utils.exceptions import InitializationError

STORE = './.dumps'

class StateTracker(object):
    r""" 
    Keep track of particle states (configurations) in the current execution. 
    Write state information to JSON file for rendering.
    """
    def __init__(self, config_num:str):
        # identifying number for current run, created by `StateGenerator`
        self.config_num: str = config_num

    def collect_states(self, state:tuple) -> dict:
        r""" 
        Collect a single amoebot's information from the core `Amoebot` class. 
        This function is called asyncronously at the end of each particle 
        activation, the state configuration is pushed into a queue.

        returns (dict) : configuration of the amoebot
        """
        config = self._collect_config(state)
        return config

    def update(self, __id:int, state:tuple):
        # complete path to the state file
        statefile = Path(STORE) / Path(f'run-{self.config_num}/tracks.json')

        # read data from json file if it exists
        if statefile.exists():
            with open(statefile, 'r') as f:
                tracks = json.load(f)

        else:
            # tracks the most recent state change in sequential order
            tracks = list()

        config = self._collect_config(state)

        tracks.append(dict(mov_bot=__id, config=config))

        # append state information to the json file
        with open(statefile, 'w') as f: 
            json.dump(tracks, f, indent=4)

    def checkpoint_terminal_state(self, manager:object):
        r"""
        Similar to the `StateGenerator.write`, this function checkpoints the 
        terminal state of current execution that can be loaded later for 
        re-useability.
        """
        # collect full state information from the amoebot manager
        vec_collector = np.vectorize(self._collect_config)
        config = vec_collector(tuple(manager.persistent.values())).tolist()

        # reference a checkpoint file in the current run
        statefile = Path(STORE) / Path(f'run-{self.config_num}/chkpt.json')

        # append state information to the json file
        with open(statefile, 'w') as f: json.dump(config, f, indent=4)

    def _collect_config(self, state:tuple) -> dict:
        r""" state configuration objects of a single amoebot
        """

        head, tail, _ = state

        config = dict(
                    head_pos=head.position.tolist(), 
                    tail_pos=tail.position.tolist()
                )

        return config
