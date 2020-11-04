# -*- coding: utf-8 -*-

""" elements/tracker.py
"""

from ..utils.exceptions import InitializationError

import json
import numpy as np
from pathlib import Path

STORE = './.dumps'

class StateTracker(object):
    r""" 
    Keep track of particle states (configurations) in the current execution. 
    Write state information to JSON file for rendering.

    Attributes
        config_num (str) :: identifier number for the json configuration file.
    """
    def __init__(self, config_num:str):
        r"""
        Attributes
            config_num (str) :: identifier number for the json configuration 
                            file.
        """

        # identifying number for current run, created by `StateGenerator`
        self.config_num: str = config_num

    def collect_states(self, state:tuple) -> dict:
        r""" 
        Collect a single amoebot's information from the core `Amoebot` class. 
        This function is called asyncronously at the end of each particle 
        activation, the state configuration is pushed into a queue.

        Attributes
            state (tuple): state tuple for given `Amoebot` object.

        Return (dict): configuration of the amoebot.
        """

        config = self._collect_config(state)
        return config

    def update(self, __id:np.uint8, state:tuple):
        r"""
        Update the state tracker file upon particle (amoebot) movement.

        Attributes
            __id (np.uint8) :: unique particle identifier.
            state (tuple) :: state tuple for given `Amoebot` object.
        """

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
        tracks.append(dict(mov_bot=int(__id), config=config))

        # append state information to the json file
        with open(statefile, 'w') as f: 
            json.dump(tracks, f, indent=4)

    def checkpoint_terminal_state(self):
        r"""
        Similar to the `StateGenerator.write`, this function checkpoints the 
        terminal state of current execution that can be loaded later for 
        re-useability.
        """
        raise NotImplementedError

    def _collect_config(self, state:tuple) -> dict:
        r""" 
        State configuration objects of a single amoebot.

        Attributes
            state (tuple) :: state tuple for given `Amoebot` object.
        
        Return (dict): configuration of the amoebot.
        """

        head, tail, _ = state

        config = dict(
                    head_pos=head.tolist(), 
                    tail_pos=tail.tolist()
                )

        return config
