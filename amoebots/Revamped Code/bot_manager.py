from dataclasses import dataclass, field

import bot_skeleton as bs
import numpy as np
import concurrent.futures as cf

@dataclass
class BotManager:
    bot_list: dict = field(default=None)
    next_index: np.uint8 = field(default=np.uint8(0))
    bot_statuses: np.ndarray = field(default=None)

    def activate(self, i):
        self.bot_statuses[i] = self.bot_list[i].engine()

    def activate_mf(self):
        with cf.ThreadPoolExecutor() as executor:
            executor.map(self.activate, range(len(self.bot_list)))

    def activate_si(self):
        if self.bot_statuses is None:
            self.bot_statuses = np.empty(len(self.bot_list), dtype="uint8")
        for i in range(len(self.bot_list)):
            self.activate(i=i)
        if np.all(self.bot_statuses):
            return np.uint8(1)
        return np.uint8(0)


    def add_bot(self, node=None):
        """
        Adds individual nodes to node list
        """
        if not self.bot_list:
            self.bot_list = {}
        self.bot_list[self.next_index] = bs.Bot(head=node, bot_id=self.next_index)
        if self.next_index < 255:
            self.next_index += np.uint8(1)
        elif self.next_index < 65534:
            self.next_index += np.uint16(1)
        elif self.next_index < 429496728:
            self.next_index += np.uint32(1)

    def random_bot_placement(self, number_of_bots=None, node_list=None):
        converted_list = np.array(list(node_list.values()))
        np.random.shuffle(converted_list)
        for i in range(number_of_bots):
            self.add_bot(node=converted_list[i])


if __name__ == "__main__":
    pass