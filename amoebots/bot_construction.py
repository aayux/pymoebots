import random as rd


class Bot:
    def __init__(self):
        # This section deals with the bots position on the grid
        self.__head = None
        self.__tail = None

        # This section deals with ports
        self.__choices = ['right', 'bottom right', 'bottom left', 'left', 'top left', 'top right']
        self.__scan_order = []
        self.__port_scan_results = [[],[],[]]

        # This section deals with the bots traveling
        self.__path = []

        self.__debug = False

    def engine(self):
        self.__orientate()

    def __move(self, value=None):
        """
        Moves bot

        If no value is given, the bot will move randomly.

        :param str value:
        :return:
        """
        if value is None:
            self.__head = self.__head.get_node(rd.choice(self.__choices))

    def __orientate(self):
        """
        Orientates bot on grid. Currently, randomly gives bot random orientation.

        :return:
        """
        choice = rd.choice(self.__choices)
        choice_index = self.__choices.index(choice)
        for _ in range(len(self.__choices)):
            if not self.__scan_order:
                self.__scan_order.append(choice)
                choice_index += 1
            else:
                self.__scan_order.append(self.__choices[choice_index%6])
                choice_index += 1

    def scan_for_spaces(self):
        """
        Scan for spaces and spawn threads (agents) when found.

        :return:
        """
        pass

    def toogle_debug(self):
        """
        Toogles debug mode for bots. This will most likely be offloaded to a class on it's own so that it can be added
        only when it is necessary.

        :return:
        """
        self.__debug = not self.__debug

    def get_scan_order(self):
        """
        Gets current bots scan order.

        :return: list self.__scan_order
        """
        if self.__debug:
            return self.__scan_order
        else:
            print("Unable to return scan order. This bot is not in debug mode")


class BotManager:
    def __init__(self):
        self.__bots = []

    def add_bots(self, position = None):
        pass


if __name__ == '__main__':
    bot = Bot()
    bot.engine()
    bot.toogle_debug()
    print(f" This is the scan order {bot.get_scan_order()}")

