from dataclasses import dataclass, field
from numpy import uint8, ndarray, array


@dataclass
class Node:
    # Position of node in relation to the grid it is associated with
    position: ndarray = field(default=None)

    # Node id that corresponds to it's position the node dictionary
    node_id: uint8 = field(default=None)

    # List of ports associated with node
    ports: ndarray = field(default=None)

    # Neighbors: object = field(default=nopo.PortDict())
    neighbors: dict = field(default=None)

    # Keeps occupied status
    occupied: uint8 = field(default=None)

    # The bot that is current occupying this node
    bot: object = field(default=None)

    def arrival(self, bot):
        """
        bot arrival on this node sets occupied state to 1, meaning occupied
        """

        # Sets occupied status to one
        self.occupied = uint8(1)

        # Records which bot is currently occupy the node
        self.bot = bot

    def check_neighbor(self, port):
        # used for bot port scanning. Removes None spots for bots.

        # Set node to neighbor value located at specified port
        node = self.neighbors[port]

        # Checks if the neighbor at specified port is None
        if node is None:

            # If it is, create spare Node
            node = Node()

            # Initialize spare node
            node.initialize()

        return node

    def departure(self):
        """
        bot departure from this node sets occupied state to 0, meaning unoccupied
        """

        # Sets occupied status to one
        self.occupied = uint8(0)

        # Removes whatever bot that currently on the node.
        self.bot = None

    def get_bot(self):
        return self.bot

    def get_id(self):
        return self.node_id

    def get_ports(self):
        return self.ports

    def get_neighbor(self, port):

        # Assigns class variables and methods to method variables
        neighbors = self.neighbors
        initialize = self.initialize

        # Checks if neighbor is None, meaning it has not been initialized
        if neighbors is None:

            # Initializes node
            initialize()

            # Assigns updated class variable to method variable
            neighbors = self.neighbors

        return neighbors[port]

    def get_occupied(self):
        return self.occupied

    def initialize(self):

        # Assigns port list to ports variable
        self.ports = array(['right', 'bottom right', 'bottom left', 'left', 'top left', 'top right'])

        # Creates neighbors dictionary list
        self.neighbors = {
            'right': None,
            'bottom right': None,
            'bottom left': None,
            'left': None,
            'top left': None,
            'top right': None}

    def set_neighbor(self, port: str, node: object):

        # Assigns class variables and methods to method variables
        neighbors = self.neighbors
        initialize = self.initialize

        # Checks if neighbor is None, meaning it has not been initialized
        if neighbors is None:

            # Initializes node
            initialize()

            # Assigns updated class variable to method variable
            neighbors = self.neighbors

        # Assigns node to corresponding port location
        neighbors[port] = node

        # Returns method variable to class variable. (May be unnecessary)
        self.neighbors = neighbors
