import pickle as pkl
from pathlib import Path

STORE = './.dumps'

class SharedObjects(object):
    def __init__(self, config_num:str, datalist:list=None):
        # length of the shared list
        self.length = None
        
        # complete path to the shared file
        self.sharedfile = Path(STORE) / Path(f'run-{config_num}/shared.pkl')

        if datalist is not None: self.save(datalist)

    def save(self, datalist:list):
        r"""
        """

        with open(self.sharedfile, 'wb') as f:
            pkl.dump(datalist, f, protocol=pkl.HIGHEST_PROTOCOL)

        self.length = len(datalist)

        # mark for garbage collection
        del datalist

    def load(self) -> list:
        r"""
        """

        try:
            with open(self.sharedfile, 'rb') as f:
                sh_data = pkl.load(f)

            return sh_data

        except FileNotFoundError:
            raise FileNotFoundError(
                f"could not find {self.sharedfile}, call `save` before `load`."
            )

    def iwrite(self, index:int, data:object):
        r"""
        """

        try:
            with open(self.sharedfile, 'rb') as f:
                sh_data = pkl.load(f)
            sh_data[index] = data
            with open(self.sharedfile, 'wb') as f:
                pkl.dump(sh_data, f, protocol=pkl.HIGHEST_PROTOCOL)

            # mark for garbage collection
            del sh_data

        except FileNotFoundError:
            raise FileNotFoundError(
                f"could not find {self.sharedfile}, call `save` before `iwrite`."
            )

    def ifetch(self, index:int) -> object:
        r"""
        """
        try:
            with open(self.sharedfile, 'rb') as f:
                sh_data = pkl.load(f)

            return sh_data[index]
        except FileNotFoundError:
            raise FileNotFoundError(
                f"could not find {self.sharedfile}, call `save` before `iread.`"
            )




