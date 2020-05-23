import sys
import time
import json
import numpy as np

from numpy import array
from pathlib import Path

from ..extras.exceptions import InitializationError

class StateTracker(object):
    r""" 
    Keep track of particle states in the current execution. Write state 
    information to JSON file for rendering.
    """
    def __init__(self):
        self._generate_trace(save_as=None)

    def collect_states(self, manager:object):
        # collect state information from the amoebot manager
        vec_collect = np.vectorize(self._collect_amoebot_states)
        amoebot_states = vec_collect(manager.amoebots)
        self.update(amoebot_states.tolist())

    def update(self, amoebot_states:dict):
        # complete path to the state file
        statefile = Path(self.store) / Path(self.save_as)

        # TODO optimize this block
        # read data from json file if it exists
        if statefile.exists():
            with open(statefile, 'r') as f: 
                state_dict = json.load(f)
            
            # if current _round is not the newest
            if str(self._round) in state_dict:
                # remove entries in and after current _round
                remove_keys = [key for key in state_dict.keys() \
                          if int(key) >= self._round]
                for key in remove_keys: state_dict.pop(key)
        else:
            # map to store current state information
            state_dict = dict()

        state_dict[self._round] = amoebot_states

        # append state information to the json file
        with open(statefile, 'w') as f: json.dump(state_dict, f)

        self._round += 1

    def _generate_trace(self, save_as:str=None):
        # current _round hashes into the state dictionary
        self._round = 0

        # create hidden temp space 
        self.store = './.dumps/tracking'
        Path(self.store).mkdir(parents=True, exist_ok=True)

        # create a unique time stamp for every run
        if save_as is None:
            timestamp = int(time.time())
            save_as = f'run-{timestamp}'

        self.save_as = f'{save_as}.json'

    def get_last_state(self) -> dict:
        return self.get_state(self._round - 1)

    def get_state(self, ix:int) -> dict:
        r""" get the state information at index
        """
        # complete path to the state file
        statefile = Path(self.store) / Path(self.save_as)

        try:
            with open(statefile, 'r') as f:
                state_dict = json.load(f)
        except FileNotFoundError:
            raise InitializationError(
                                f"Amoebots have not been initialized ",
                                f"correctly, check file and retry. Exiting!"
            )
            sys.exit(0)

        assert str(ix) in state_dict, \
            IndexError(
                    f"Invalid _round index, execution is ",
                    f"at _round {self._round}"
            )

        return state_dict[str(ix)]

    def set_state(self, ix:int):
        r""" reset the state pointer starting at index
        """
        self._round = ix
    
    def _collect_amoebot_states(self, bot:object) -> dict:
        r""" return state for a single amoebot
        """
        state = dict(
                        head_pos=bot.head.position.tolist(),
                        tail_pos=bot.tail.position.tolist(),
                        port_labels=bot.port_labels.tolist()
                    )
        return state
