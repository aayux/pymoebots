from dataclasses import dataclass, field
from numpy import uint8, ndarray, array, random

import numpy as np


@dataclass
class Package:
    access: object = field(default=None)
    link: object = field(default=None)
    # objects: ndarray = field(default=None)
    # package_id: ndarray = field(default=None)

    def authorize(self, bot=None):
        if self.access is bot:
            return True
        return False

    def get_link(self):
        return self.link

    def store_link(self, access=None, link=None):

        # stores bot that can access package and link
        self.access = access
        self.link = link

@dataclass
class Token:
    delimiter: uint8 = field(default=None)
    identifer: uint8 = field(default=None)
    token_id: ndarray = field(default=None)

    def is_delimiter(self):
        return self.delimiter