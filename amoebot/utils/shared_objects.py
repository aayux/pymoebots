import pickle
import numpy as np
from pathlib import Path

STORE = './.dumps'

class SharedObjects(object):
    def __init__(self, config_num:str, data:dict=None):
        # keys in the shared dictionary
        self.keys = None
        
        # complete path to the shared file
        self.sharedfile = Path(STORE) / Path(f'run-{config_num}/shared.pickle')

        if data is not None: self.save(data)

    def save(self, data:dict):
        r"""
        """

        with open(self.sharedfile, 'wb') as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

        self.keys = list(data.keys())

        # mark for garbage collection
        del data

    def load(self) -> list:
        r"""
        """

        try:
            with open(self.sharedfile, 'rb') as f:
                sh_data = pickle.load(f)

            return sh_data

        except FileNotFoundError:
            raise FileNotFoundError(
                f"could not find {self.sharedfile}, call `save` before `load`."
            )

    def iwrite(self, key:np.uint8, data:object):
        r"""
        """

        try:
            with open(self.sharedfile, 'rb') as f:
                sh_data = pickle.load(f)
            sh_data[key] = data
            with open(self.sharedfile, 'wb') as f:
                pickle.dump(sh_data, f, protocol=pickle.HIGHEST_PROTOCOL)

            # mark for garbage collection
            del sh_data

        except FileNotFoundError:
            raise FileNotFoundError(
                f"could not find {self.sharedfile}, call `save` before `iwrite`."
            )

    def ifetch(self, key:np.uint8) -> object:
        r"""
        """
        try:
            with open(self.sharedfile, 'rb') as f:
                sh_data = pickle.load(f)

            return sh_data[key]
        except FileNotFoundError:
            raise FileNotFoundError(
                f"could not find {self.sharedfile}, call `save` before `iread.`"
            )




