import random as rd
import concurrent.futures as cf
import time


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
        # Replace above with more descriptive structure below
        # generated from self.__scan_for_open_ports()
        self.__port_structure = {}

        # This section deals with the bots traveling
        self.__head_path_x = []
        self.__head_path_y = []
        self.__tail_path_x = []
        self.__tail_path_y = []

        self.__debug = False

    def engine(self, turns=1):
        """
        This method is intended to run the bot's algorithm
        :param turns: Number of turns a bot may take before shutting down, defaults to 1.
        :type turns: int
        :return: None
        """
        if not self.__head_path_x:
            self.__orientate()
        else:
            for _ in range(turns):
                self.__move()

    def configure(self, node=None, id=None):
        """
        The method configures the bots position and id.

        :param node: Node object as head/tail for start position.
        :type node: node_construction.Node
        :param id: Bot unique private ID
        :type id: int
        :return: None
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

        :param value: New position.
        :type value: node_construction.Node
        :return: None
        """
        self.__head = value
        self.__tail = self.__head

    def __collect_path(self):
        """
        Records the current position of the head and tail to the bot's
        inner head path and tail path x and y arrays.

        :return: None
        """
        self.__head_path_x.append(self.__head.get_position()[0])
        self.__head_path_y.append(self.__head.get_position()[1])
        self.__tail_path_x.append(self.__tail.get_position()[0])
        self.__tail_path_y.append(self.__tail.get_position()[1])

    def __move(self, value=None):
        """
        Moves bot.

        If value None is given, the bot will move randomly.

        :param value: Direction keyword, defaults to None.
        :type value: str
        :return: None.
        """
        # Bot is extended, must move tail in.
        if self.__head is not self.__tail:
            temp = self.__tail
            self.__tail = self.__head
            temp.departure()

        # Pick a random direction keyword from the list of
        # current open ports in its scan order.
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
        """
        Create a map of open ports around bot.

        :return: Array of open port keywords for bot to move to.
        """
        available_choice = []
        for port in self.__scan_order:
            node = self.__head.get_node(port)
            if node is not None and not node.get_occupied():
                available_choice.append(port)
        return available_choice

    def __orientate(self):
        """
        Creates internal list self.__scan_order.
        Orientates bot on grid.
        Currently, randomly gives bot random orientation.

        :return: None
        """
        # Set node under this bot to be occupied by this bot.
        self.__head.arrival(bot=self)
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

    def scan_for_spaces(self):
        """
        Non-moving, pre-algorithm method.
        The intent is to scan for predecessors and successors to identify the
        directed acyclic graph of leader election, and system boundaries overall.

        Create internal dict self.__port_structure.
        Scan for spaces and spawn threads (agents) when found.
        Checks all port around it in a clockwise and counterclockwise way.
        Clockwise pass identifies successors in DAG,
        CCW pass id's predecessors.
        List of predecessors and successors is 1:1.

        :return: None
        """
        # Check round all ports twice.
        # First pass clockwise to id successors
        region_origin = ""
        region_end = ""
        # How many empty nodes between occupied ones?
        empty_region = 0
        port_structure = {
            "successors": [],
            "predecessors": [],
            "right":    {
                "region_origin":"",
                "empty_region":0,
                "occupied":0,
                "region_end":""
            },
            "bottom right":{
                "region_origin":"",
                "empty_region":0,
                "occupied":0,
                "region_end":""
            },
            "bottom left": {
                "region_origin":"",
                "empty_region":0,
                "occupied":0,
                "region_end":""
            },
            "left":     {
                "region_origin":"",
                "empty_region":0,
                "occupied":0,
                "region_end":""
            },
            "top left":  {
                "region_origin":"",
                "empty_region":0,
                "occupied":0,
                "region_end":""
            },
            "top right": {
                "region_origin":"",
                "empty_region":0,
                "occupied":0,
                "region_end":""
            }
        }

        for j in range(len(self.__scan_order) + 1):
            i = j % len(self.__scan_order)
            if self.__head.get_node(self.__scan_order[i]).get_occupied():

                port_structure[self.__scan_order[i]]["occupied"] = 1

                port_structure[self.__scan_order[i]]["region_origin"] = self.__scan_order[i]
                region_origin = self.__scan_order[i]

                port_structure[self.__scan_order[i]]["empty_region"] = 0

                if empty_region > 0:
                    port_structure["successors"].append(self.__scan_order[i])
                    # Can spawn thread here.
                    empty_region = 0

            else:
                port_structure[self.__scan_order[i]]["occupied"] = 0

                port_structure[self.__scan_order[i]]["region_origin"] = region_origin

                empty_region += 1
                port_structure[self.__scan_order[i]]["empty_region"] = empty_region

        empty_region = 0
        region_origin=""

        # Second pass counterclockwise to ID predecessors
        clockWiseTmp = [i for i in reversed(self.__scan_order)]
        for j in range(len(self.__scan_order) + 1):
            i = j % len(clockWiseTmp)
            if self.__head.get_node(clockWiseTmp[i]).get_occupied():
                port_structure[clockWiseTmp[i]]["occupied"] = 1

                region_origin = clockWiseTmp[i]
                port_structure[clockWiseTmp[i]]["region_origin"] = clockWiseTmp[i]

                port_structure[clockWiseTmp[i]]["empty_region"] = 0

                if empty_region > 0:
                    port_structure["predecessors"].append(clockWiseTmp[i])
                    empty_region = 0

            else:
                port_structure[clockWiseTmp[i]]["occupied"] = 0

                port_structure[clockWiseTmp[i]]["region_origin"] = region_origin

                empty_region += 1
                port_structure[clockWiseTmp[i]]["empty_region"] = empty_region

        port_structure["predecessors"] = [i for i in reversed(port_structure["predecessors"])]

        self.__port_structure = port_structure


        # flag = 0
        # port = 0
        # agents = 0
        # spaces = []
        #
        # while True:
        #     # Get current node in scan order, in relation to head
        #     if not self.__head.get_node(self.__scan_order[port%6]).get_occupied():
        #         # Not "flag" but space is occupied.
        #         if not flag and self.__head.get_node(self.__scan_order[port-1%6]).get_occupied():
        #             space = [self.__scan_order[(port-1)%6]]
        #             flag = 1
        #         port += 1
        #     elif self.__head.get_node(self.__scan_order[port%6]).get_occupied():
        #         if flag:
        #             space.append(self.__scan_order[port%6])
        #             flag = 0
        #             agents += 1
        #             spaces.append(space)
        #         port += 1
        #     if port > 5 and not flag:
        #         break
        # if self.__debug:
        #     return [agents, spaces]


    def get_path(self):
        """
        Retrieve 4 lists movement history of bots.

        :return: List of lists [head_path_x, head_path_y, tail_path_x, tail_path_y]
        """
        return [self.__head_path_x, self.__head_path_y, self.__tail_path_x, self.__tail_path_y]

    def __set_id(self, value):
        """
        Set a unique private ID if there is not one assigned.

        :param value: Bot ID
        :type value: int
        :return: None
        """
        if not self.__bot_id:
            self.__bot_id = value

    def toggle_debug(self):
        """
        Toogles debug mode for bots.
        This will most likely be offloaded to a class
        on it's own so that it can be added
        only when it is necessary.

        :return: None
        """
        self.__debug = not self.__debug
        print("This bot is now in debug mode")

    def get_scan_order(self):
        """
        Debug only.
        Gets current bots scan order.

        :return: List self.__scan_order
        """
        if self.__debug:
            return self.__scan_order
        else:
            print("Unable to return scan order. This bot is not in debug mode")

    def set_head_node(self, value):
        """
        Debug option to set head manually.

        :param value: Set head node and position manually.
        :type value: node_construction.Node
        :return: None
        """
        if self.__debug:
            self.__head = value
        else:
            print("Cannot run set_head_node method. Bot is not in debug mode")

    def get_head(self):
        """
        Get Node reference to this bot's head.

        :return: node_construction.Node
        """
        return self.__head

    def get_position(self):
        """
        Get position of this bot's head and tail.

        :return: Nested tuple of ((head_x, head_y), (tail_x, tail_y))
        """
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

    def port_status(self, *args):
        """
        Returns data about a specific port,
        or list of predecessors or successors.

        :param *args: Any port keyword string | "predecessors" | "successors"
        :type *args: str
        :return: Either full port structure or pieces.
        """

        if self.__debug:
            if len(args) > 0:
                packet = {}
                for elem in args:
                    if self.__port_structure[elem]:
                        packet[elem] = self.__port_structure[elem]
                return packet
            else:
                return self.__port_structure
        else:
            print("Cannot use method port_status. Bot not in debug mode.")

    def __str__(self):
        return str(self.__bot_id)

    def __repr__(self):
        return str(self.__bot_id)


class BotManager:
    """
    Manages:
        bot creation,
        activation time,
        Agents,
        Links.
        (Tokens?)
    Has access to the particle system as a whole,
    but only used for user functionality as it
    does not interfere with the algorithms themselves.

    """
    def __init__(self):
        self.__bots = []
        self.__paths = []

    def activate(self, rounds=1, turns=1):
        """
        Main engine for Bot Manager.
        Lets each bot have their share of the activation time,
        for as many rounds as necessary to complete the algorithm.
        TODO: Infinite/Until Termination should be 0.
        Is turns necessary? What is it used for?

        :param rounds: Number of full passes to make.
        :type rounds: int
        :param turns: Not sure.
        :type turns: int
        :return: None
        """
        for _ in range(rounds):
            for bot in self.__bots:
                bot.engine(turns=turns)

    def bot_threads(self, rounds=1, turns=1):
        """
        Allocates a ThreadPoolExecutor each round
        which activates bots.

        :param rounds: Number of passes on each bot, defaults to 1.
        :type rounds: int
        :param turns: defaults to 1
        :type turns: int
        :return: None
        """
        # pool = cf.ThreadPoolExecutor(1)
        for i in range(rounds):
            with cf.ThreadPoolExecutor() as executor:
                executor.map(self.__activate_bot, self.__bots)
                # futures = [executor.map(self.__activate_bot, self.__bots)]



        # for bot in self.__bots:
        #     with cf.ThreadPoolExecutor(max_workers=1) as executor:
        #         future = executor.submit(self.__activate_bot, bot, rounds)

    def __activate_bot(self, bot, turns=1):
        """
        Function to activate bot and give it its time
        in the algorithm. Called by bot_threads().

        :param bot: Reference to which bot to be activated.
        :type bot: Bot
        :return: None
        """
        bot.engine(turns=turns)

    # def add_bots(self, node=None, id=None):
    #     bot = Bot()
    #     bot.configure(node=node, id=id)
    #     self.__bots.append(bot)

        # self.__bots[-1].set_position(node)
        # self.__bots[-1].set_id(value=id)

    def __add_bots(self, node=None, id=None):
        """
        TODO: change name to add_bot?
        Adds a new bot to the grid, given a head node and private ID.
        Adds reference to bot to self.__bots

        :param node: Reference to Bot's head node.
        :type node: node_construction.Node
        :param id: Private bot ID.
        :type id: int
        :return: None
        """
        bot = Bot()
        bot.configure(node=node, id=id)
        self.__bots.append(bot)

    def mass_add_bots(self, number_of_bots=None, nodes=None):
        """
        Add multiple bots to the grid, one for each node provided.

        :param number_of_bots: How many Bots to add, defaults to value None.
        :type number_of_bots: int
        :param nodes: List of node references for each new Bot's head to go, defaults to None.
        :type nodes: List of node_construction.Node
        """
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
        """
        Returns a list of bots managed by this class.

        :return: List of bot_construction.Bot
        """
        return self.__bots

    def get_positions(self):
        """
        Returns list of lists of x and y points
        for head and tail of a bot.

        :return: Nested lists of x,y head and tail positions.
        """

        return [bot.get_position() for bot in self.__bots]

    def get_paths(self):
        """
        Returns a nested list of paths for every bot.

        :return: nested List of paths for each bot.
        """
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

    def test_port_structure():
        import node_construction as nc

        nodeman = nc.NodeManager()
        nodeman.create_cluster(x=8, y=4)

        occupied = [
            [3, 1], #center
            [2, 2], #top left
            [1, 1], #left
            [2, 0], #bottom left
            [4, 2], #top right
            [5, 1], #right
            [4, 0]  #bottom right
        ]
        botList = [Bot() for _ in range(len(occupied))]
        for i in range(len(botList)):
            botList[i].toggle_debug()
            botList[i].set_head_node(list(filter(lambda node: node.get_position() == occupied[i], nodeman.get_node_array()))[0])
            #botList[i].set_head_node(nodeList[i*2])
            botList[i].orientate()

        botList[0].scan_for_spaces()
        print(botList[0].port_status("predecessors", "successors"))


    #test_path_collect()
    test_port_structure()
