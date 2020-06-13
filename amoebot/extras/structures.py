import random
from collections import UserList

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
            index = index if ix else random.randint(0, len(self.data))
        else: index = 0
        
        super().insert(ix, item)

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