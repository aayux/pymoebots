from dataclasses import dataclass, field

import numpy as np


@dataclass
class Link:
    test: np.uint8 = field(default=np.uint(0))
    link_id: bytes = field(default=None)

    def get_test(self):
        return self.test

    def test_signal(self):
        self.test += np.uint(1)