# -*- coding: utf-8 -*-

""" shared_objects.py
"""

import pickle
import numpy as np
from pathlib import Path

STORE = './.dumps'

class SharedObjects(object):
    r"""
    A class for custom shared memory objects for data dumps that can be indexed, 
    pickled and unpickled much like Redis. Useful in true multiprocessing 
    implementations.

    Attributes

        sharedfile (Path) :: path to the shared data dump.
        keys (list) :: keys of the data dictionary.
    """
    def __init__(self, config_num:str, data:dict=None):
        r"""
        Attributes

            config_num (str) :: identifier number for the configuration.
            data (dict) :: the data dictionary to be stored.
        """
        # keys in the shared dictionary
        self.keys = None
        
        # complete path to the shared file
        self.sharedfile = Path(STORE) / Path(f'run-{config_num}/shared.pickle')

        if data is not None: self.save(data)

    def save(self, data:dict):
        r"""
        Save the data dictionary to pre-specified data dump.

        Attributes

            data (dict) :: the data dictionary to be stored.
        """

        with open(self.sharedfile, 'wb') as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

        self.keys = list(data.keys())

        # mark for garbage collection
        del data

    def load(self) -> list:
        r"""
        Load the data values from the dump as as a list.
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
        Indexed write to the data.

        Attributes

            key (numpy.uint8) :: the key to index into the data dictionary.
            data (object) :: object to be written into index position given by
                            `key`.
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
        Indexed read from the data.

        Attributes

            key (numpy.uint8) :: the key to index into the data dictionary.
        """
        try:
            with open(self.sharedfile, 'rb') as f:
                sh_data = pickle.load(f)

            return sh_data[key]
        except FileNotFoundError:
            raise FileNotFoundError(
                f"could not find {self.sharedfile}, call `save` before `iread.`"
            )




