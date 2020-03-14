from dataclasses import dataclass, field
from numpy import all, append, array, ndarray, random, uint8, zeros
from reuseables import increase_index
from bot_skeleton import Bot
from concurrent import futures

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

    # Dictionary that holds all bots associated with manager
    bot_dict: dict = field(default=None)

    # Keeps index value for bot creation
    next_index: uint8 = field(default=None)

    # Array of 0 or 1's associated with each bot. 0 means unfinished, 1 means finished.
    bot_status: ndarray = field(default=None)

    def activate(self, index=None):
        """
        Represents a bot_skeleton.Bot running one timestep. Runs the bot's engine function.

        :param index: Bot ID.
        :type index: uint

        :return: None
        """

        # Assigns Class variable to method variable
        bot_status = self.bot_status
        bot_dict = self.bot_dict

        # Saves the number of botsin bot dictionary and associated status to local variable
        length_of_bot_status = len(bot_status)
        length_of_bot_dict = len(bot_dict)

        # Checks if the index is not none
        if index is not None:

            # Checks to see if the number of associated statuses are the same as the number of bots
            if length_of_bot_status != length_of_bot_dict:

                # Runs bots engine method and stores return status
                status = bot_dict[index].engine()

                # Appends returned status to to bot status
                bot_status = append(bot_status, status)
            else:

                # Runs bots engine method and stores return status in associated status position
                bot_status[index] = bot_dict[index].engine()

        # Returns local variable bot status to class variable.
        self.bot_status = bot_status

    def activate_mf(self):
        """
        Sets up threaded calls to all Bots activation methods.

        :return: None
        """
        # Assigns Class variable to method variable
        bot_dict = self.bot_dict
        activate = self.activate

        # Saves the number of bots in bot dictionary to local variable
        length_of_bot_dict = len(bot_dict)

        # Sets up thread pool as executor
        with futures.ThreadPoolExecutor() as executor:

            # maps range to active method
            executor.map(activate, range(length_of_bot_dict))

        # Assigns updated Class variable to method variable
        bot_status = self.bot_status

        # Checks if all bot statuses are True, meaning they are finished.
        if all(bot_status):
            return uint8(1)
        return uint8(0)

    def activate_si(self):
        """
        Sequential bot activations. Bot activations are arbitrary as long as
        each one gets equal time to run during each time step,
        so they just run in the order that they were created.

        Initializes self.bot_statuses.

        Once all bot_statuses are 1, this method returns 1.

        :return: uint 0|1
        """

        # Assigns Class variable to method variable
        bot_dict = self.bot_dict
        activate = self.activate

        # Saves the number of bots in bot dictionary to local variable
        length_of_bot_dict = len(bot_dict)

        # loops through for the number of bots number of times
        for index in range(length_of_bot_dict):

            # Runs activate class method for the specific
            activate(index=index)

        # Assigns updated Class variable to method variable
        bot_status = self.bot_status

        # Checks if all bot statuses are True, meaning they are finished.
        if all(bot_status):
            return uint8(1)
        return uint8(0)

    def add_bot(self, node=None):
        """
        Adds individual bot to bot list.

        :return: None
        """

        # Assigns Class variable to method variable
        index = self.next_index
        bot_dict = self.bot_dict

        # creates bot and assigns it a spot in the bot dictionary
        bot_dict[index] = Bot(head=node, bot_id=index)

        # Increase index by one
        index = increase_index(index)

        # Assigns method variables back to Class variables
        self.next_index = index
        self.bot_dict = bot_dict

    def initialize(self):

        # initializes next index to zero
        self.next_index = uint8(0)

        # initializes node dictionary
        self.bot_dict = {}

        # initializes bot statuses
        self.bot_status = zeros(0, dtype="uint8")

    def random_bot_placement(self, number_of_bots=None, node_list=None):
        """
        Places each bots on an instance of a node_skeleton.Node
        in the graph randomly.

        :return: None
        """

        # Assigns class method to local variable
        add_bot = self.add_bot

        # Coverts list of dictionary values to a workable list
        dictionary_values_to_list = list(node_list.values())

        # Converts list to a numpy ndarray list
        list_to_ndarray = array(dictionary_values_to_list)

        # Shuffles list of nodes
        random.shuffle(list_to_ndarray)

        # Loops through the number of bots
        for index in range(number_of_bots):

            # Adds bot to bot dictionary with the node
            add_bot(node=list_to_ndarray[index])


if __name__ == "__main__":
    pass
