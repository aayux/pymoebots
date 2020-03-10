from dataclasses import dataclass, field

import bot_skeleton as bs
import numpy as np
import concurrent.futures as cf

@dataclass
class BotManager:
    """
    Manages the system of Bots and keeps track of
    where they are on the field.

    Keeps track of and assigns threads for bots to take action on.
    (Aka their engine).

    :param bot_list: Array of bots currently being managed. Defaults to None.
    :type bot_list: Array of bot_skeleton.Bot

    :param next_index: Keeps track of the next available integer to assign as a bot id. Defaults to 0.
    :type next_index: uint

    :param bot_statuses: Bit array representing each bot's status in the timestep. 1 for complete, 0 for incomplete. Index of number is bot's id.
    :type bot_statuses: Array of uint8
    """
    bot_list: dict = field(default=None)
    next_index: np.uint8 = field(default=np.uint8(0))
    bot_statuses: np.ndarray = field(default=None)

    def activate(self, i):
        """
        Represents a bot_skeleton.Bot running one timestep. Runs the bot's engine function.

        :param i: Bot ID.
        :type i: uint

        :return: None
        """
        self.bot_statuses[i] = self.bot_list[i].engine()

    def activate_mf(self):
        """
        Sets up threaded calls to all Bots activation methods.

        :return: None
        """
        with cf.ThreadPoolExecutor() as executor:
            executor.map(self.activate, range(len(self.bot_list)))

    def activate_si(self):
        """
        Sequential bot activations. Bot activations are arbitrary as long as
        each one gets equal time to run during each time step,
        so they just run in the order that they were created.

        Initializes self.bot_statuses.

        Once all bot_statuses are 1, this method returns 1.

        :return: uint 0|1
        """
        if self.bot_statuses is None:
            self.bot_statuses = np.empty(len(self.bot_list), dtype="uint8")
        for i in range(len(self.bot_list)):
            self.activate(i=i)
        if np.all(self.bot_statuses):
            return np.uint8(1)
        return np.uint8(0)


    def add_bot(self, node=None):
        """
        Adds individual bot to bot list.

        :return: None
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
        """
        Places each bots on an instance of a node_skeleton.Node
        in the graph randomly.

        :return: None
        """
        converted_list = np.array(list(node_list.values()))
        np.random.shuffle(converted_list)
        for i in range(number_of_bots):
            self.add_bot(node=converted_list[i])


if __name__ == "__main__":
    pass
