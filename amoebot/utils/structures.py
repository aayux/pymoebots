import random
import pickle as pkl

from pathlib import Path
from collections import UserList, defaultdict

from .exceptions import InitializationError

class AnonList(UserList):
    r"""
    Custom container; wraps list object designed so that elements anonimity is
    maintained an indexing is impossible.
    """

    def append(self, item:object):
        raise RuntimeError(f"Can not append to 'AnonList' objects, use the "
                           f"'insert' method.")
    
    def insert(self, item:object, index:int=None):
        r""" inserts into a random index if no index is supplied
        """

        if self.data:
            index = index if index else random.randint(0, len(self.data))
        else: index = 0
        
        super().insert(index, item)

    # uncomment to use a fully anonymised list
    # def __getitem__(self, index:int):
    #     raise RuntimeError(f"Fatal! Can not index into 'AnonList'")

    # def __iter__(self) -> object:
    #     r""" returns an `iter` object over randomised list ordering
    #     """
        
    #     self._copy_data()
    #     random.shuffle(self._data)
    #     return iter(self._data)

    def __repr__(self) -> str:
        r""" returns a shuffled string
        """
        self._copy_data()
        random.shuffle(self._data)
        return str(self._data)
    
    def _copy_data(self):
        self._data = self.data

class PersistentStore(object):
    r"""
    Persistent storage for asynchronous read/write
    """
    def __init__(self, config_num:str):
        # identifying number for current run, created by `StateGenerator`
        self.config_num: str = config_num
        self.persistent = defaultdict(int)
        
        self._generate_persistant(save_as=None)

    def read(self):
        r""" 
        """
        # complete path to the state file
        statefile = Path(self.store) / Path(self.save_as)
        
        if statefile.exists():
            with open(statefile, 'rb') as f: 
                self.persistent = pkl.load(f)

    def write(self):
        r"""
        """
        # complete path to the state file
        statefile = Path(self.store) / Path(self.save_as)

        assert self.persistent is not None, \
               InitializationError("Dictionary has not been initialised.")
        
        with open(statefile, 'wb') as f: 
            pkl.dump(self.persistent, f)

    def _generate_persistant(self, save_as:str=None):
        # create hidden space 
        self.store = './.dumps/persistent'
        Path(self.store).mkdir(parents=True, exist_ok=True)

        # create a unique file for every run using config_num
        save_as = f'run-{self.config_num}'

        self.save_as = f'{save_as}.pkl' 