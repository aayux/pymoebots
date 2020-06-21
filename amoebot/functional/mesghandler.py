import numpy as np
from numpy import uint8, array, ndarray
from dataclasses import dataclass, field

@dataclass
class MessageHandler(object): 
    r"""
    A "network handler" class for handling message passing between particles or
    bots. `MessageHandler` is also responsible for ensuring that the particle 
    system stays connected as it moves.
    """
    raise NotImplementedError