from dataclasses import dataclass, field

import numpy as np


@dataclass
class Package:
    access: object = field(default=None)
    link: object = field(default=None)
    objects: np.ndarray = field(default=None)

    def authorize(self, bot=None):
        if self.access is bot:
            return True
        return False

    def get_link(self):
        return self.link

    def store_link(self, access=None, link=None):
        self.access = access
        self.link = link
