import random as rd


class Bot:
    def __init__(self):
        # This section deals with the bots position on the grid
        self.__head = None
        self.__tail = None
        self.__bot_id = None

        # This section deals with ports
        self.__choices = ['right', 'bottom right', 'bottom left', 'left', 'top left', 'top right']
        self.__scan_order = []
        self.__port_scan_results = [None, None, None]

        # This section deals with the bots traveling
        self.__head_path_x = []
        self.__head_path_y = []
        self.__tail_path_x = []
        self.__tail_path_y = []

        self.__debug = False

    def engine(self, turns=None):
        """
        This method is intended to run the bot's algorithm
        :param turns:
        :return:
        """
        if not self.__head_path_x:
            self.__orientate()
        for _ in range(turns):
            self.__move()

    def configure(self, node=None, id=None):
        """
        The method configures the bots position and id.

        :param node:
        :param id:
        :return:
        """
        if node:
            self.__set_position(value=node)
        if id is not None:
            self.__set_id(value=id)


    # def set_position(self, value):
    #     """
    #     Method sets the bot's position.
    #
    #     :param value:
    #     :return:
    #     """
    #     self.__head = value
    #     self.__tail = self.__head

    def __set_position(self, value):
        """
        Method sets the bot's position.

        :param value:
        :return:
        """
        self.__head = value
        self.__tail = self.__head
        
    def __collect_path(self):
        """
        Records the current position of the head and tail
        """
        self.__head_path_x.append(self.__head.get_position()[0])
        self.__head_path_y.append(self.__head.get_position()[1])
        self.__tail_path_x.append(self.__tail.get_position()[0])
        self.__tail_path_y.append(self.__tail.get_position()[1])

    def __move(self, value=None):
        """
        Moves bot

        If no value is given, the bot will move randomly.

        :param str value:
        :return:
        """
        if self.__head is not self.__tail:
            self.__tail.departure()
            self.__tail = self.__head

        elif value is None:
            while True:
                available_ports = self.__scan_for_open_ports()
                if available_ports:
                    temp = self.__head.get_node(rd.choice(available_ports))
                    self.__head = temp
                    self.__head.arrival(bot=self)
                    break
                else:
                    break

        self.__collect_path()

    def __scan_for_open_ports(self):
        available_choice = []
        for port in self.__scan_order:
            node = self.__head.get_node(port)
            if node is not None and not node.get_occupied():
                available_choice.append(port)
        return available_choice

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
        self.__collect_path()
        self.__head.arrival(bot=self)
        
    def scan_for_spaces(self):
        """
        Scan for spaces and spawn threads (agents) when found.

        :return:
        """
        flag = 0
        port = 0
        agents = 0
        spaces = []

        while True:
            if not self.__head.get_node(self.__scan_order[port%6]).get_occupied():
                if not flag and self.__head.get_node(self.__scan_order[port-1%6]).get_occupied():
                    space = [self.__scan_order[(port-1)%6]]
                    flag = 1
                port += 1
            elif self.__head.get_node(self.__scan_order[port%6]).get_occupied():
                if flag:
                    space.append(self.__scan_order[port%6])
                    flag = 0
                    agents += 1
                    spaces.append(space)
                port += 1
            if port > 5 and not flag:
                break
        if self.__debug:
            return [agents, spaces]

    def get_path(self):
        return [self.__head_path_x, self.__head_path_y, self.__tail_path_x, self.__tail_path_y]

    # def set_id(self, value):
    #     self.__bot_id = value

    def __set_id(self, value):
        self.__bot_id = value

    def toggle_debug(self):
        """
        Toogles debug mode for bots. This will most likely be offloaded to a class on it's own so that it can be added
        only when it is necessary.

        :return:
        """
        self.__debug = not self.__debug
        print("This bot is now in debug mode")

    def get_scan_order(self):
        """
        Gets current bots scan order.

        :return: list self.__scan_order
        """
        if self.__debug:
            return self.__scan_order
        else:
            print("Unable to return scan order. This bot is not in debug mode")

    def set_head_node(self, value):
        """
        Debug option to set head manually.

        :param value:
        :return:
        """
        if self.__debug:
            self.__head = value
        print("Cannot run set_head_node method. Bot is not in debug mode")

    def get_head(self):
        return self.__head

    def get_position(self):
        return self.__head.get_position(), self.__tail.get_position()

    def create_on_the_move(self, value=None):
        if self.__debug:
            if self.__head is not self.__tail:
                self.__tail = self.__head

            elif value is None:
                while True:
                    choice = rd.choice(self.__choices)
                    temp = self.__head.get_node(choice)
                    if temp is None:
                        self.__head.create_node(node=self.__head, choice=choice)
                        temp = self.__head.get_node(choice)
                        break
                    if temp:
                        break
                self.__head = temp

            self.__collect_path()
        else:
            print("Cannot use method create_on_the_move. Bot not in debug mode")

    def orientate(self):
        """
        Orientates bot on grid. Currently, randomly gives bot random orientation.

        :return:
        """
        if self.__debug:
            self.__orientate()
        else:
            print("Cannot use method orientate. Bot not in debug mode")

    def __str__(self):
        return str(self.__bot_id)

    def __repr__(self):
        return str(self.__bot_id)


class BotManager:
    def __init__(self):
        self.__bots = []
        self.__paths = []

    def activate(self, rounds=None, turns=None):
        for _ in range(rounds):
            for bot in self.__bots:
                bot.engine(turns=turns)

    # def add_bots(self, node=None, id=None):
    #     bot = Bot()
    #     bot.configure(node=node, id=id)
    #     self.__bots.append(bot)

        # self.__bots[-1].set_position(node)
        # self.__bots[-1].set_id(value=id)

    def __add_bots(self, node=None, id=None):
        bot = Bot()
        bot.configure(node=node, id=id)
        self.__bots.append(bot)

    def mass_add_bots(self, number_of_bots=None, nodes=None):
        if number_of_bots and nodes:
            for i in range(number_of_bots):
                self.__add_bots(node=nodes[i], id=i)

        elif number_of_bots and nodes is None:
            pass
        elif number_of_bots is None and nodes:
            pass
        else:
            pass


    def get_bots(self):
        return self.__bots

    def get_positions(self):
        return [bot.get_position() for bot in self.__bots]

    def get_paths(self):
        for bot in self.__bots:
            self.__paths.append(bot.get_path())
        return self.__paths




if __name__ == '__main__':
    def test_path_collect():
        import amoebots.node_construction as nc
        node = nc.Node()
        node.set_position((0, 0))
        bot = Bot()
        bot.set_position(node)
        bot.toggle_debug()
        bot.orientate()
        for _ in range(4):
            bot.create_on_the_move()
        path = bot.get_path()
        print(f"{path}")

    def test_scan_order():
        """
        tests orientation function
        """
        bot = Bot()
        bot.engine()
        bot.toogle_debug()
        print(f" This is the scan order {bot.get_scan_order()}")

    test_path_collect()
