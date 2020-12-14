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

    def update(self, config:list):
        r"""
        Update the state tracker file when called.

        Attributes
            config (list[dict]) :: list containing current system configuation.
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

        # insert into the tracks list
        tracks.append(config)

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
