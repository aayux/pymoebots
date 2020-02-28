from dataclasses import dataclass, field

import numpy as np


@dataclass
class Node:
    position: tuple = field(default=None)
    node_id: np.uint8 = field(default=None)

    ports: np.ndarray = np.array(['right', 'bottom right', 'bottom left', 'left', 'top left', 'top right'])

    neighbors: dict = field(default=None)

    occupied: np.uint8 = field(default=None)
    bot: object = field(default=None)

    def arrival(self, bot):
        self.occupied = np.uint8(1)
        self.bot = bot
        
    def check_neighbor(self, port):
        if not self.neighbors[port]:
            node = Node()
            node.initialize()
            return node
        return self.neighbors[port]        

    def departure(self):
        self.occupied = np.uint8(0)
        self.bot = None

    def get_bot(self):
        return self.bot

    def get_id(self):
        return self.node_id

    def get_ports(self):
        return self.ports

    def get_neighbor(self, port):
        if not self.neighbors:
            self.neighbors = {
                'right': None,
                'bottom right': None,
                'bottom left': None,
                'left': None,
                'top left': None,
                'top right': None}
        return self.neighbors[port]

    def get_occupied(self):
        return self.occupied
        
    def initialize(self):
        self.neighbors = {
                'right': None,
                'bottom right': None,
                'bottom left': None,
                'left': None,
                'top left': None,
                'top right': None}
        

    def set_neighbor(self, port: str, node: object):
        if not self.neighbors:
            self.neighbors = {
                'right': None,
                'bottom right': None,
                'bottom left': None,
                'left': None,
                'top left': None,
                'top right': None}
        self.neighbors[port] = node
