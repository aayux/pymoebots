from numpy import array
from dataclasses import dataclass, field

class StateTracker(object):
    r""" keeps track of states in the current execution
    """
    def __init__(self):
        self._generate_trace()

    def gather(self): raise NotImplementedError

    def update(self):
        # gather state information
        # write json at newest pointer
        # update pointer
        pass

    def previous_state(self): raise NotImplementedError

    def _generate_trace(self):
        # create hidden temp space 
        # create an updateable time object
        # point to newest json file
        pass

    def _get_pointer(self): raise NotImplementedError
    def _set_pointer(self): raise NotImplementedError
