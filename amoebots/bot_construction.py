import random as rd


class Bot:
    def __init__(self):
        self.__bot_id = None
        self.__head = None
        self.__tail = None
        self.__choices = ['right', 'bottom right', 'bottom left', 'left', 'top left', 'top right']
        self.__path = []



    def __move(self, value=None):
        """
        Moves bot

        If no value is given, the bot will move randomly.

        :param str value:
        :return:
        """
        if value is None:
            self.__head = self.__head.get_node(rd.choice(self.__choices))


class BotManager:
    def __init__(self):
        self.__bots = []

    def add_bots(self, position = None):
        pass