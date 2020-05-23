import time
import json
import numpy as np

from pathlib import Path

class BotPlacement(object):
    r""" 
    """
    def __init__(self): pass

    def update(self, amoebot_states:dict): raise NotImplementedError

    def _collect_amoebot_states(self, bot:object) -> dict: raise NotImplementedError