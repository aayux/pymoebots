from __future__ import annotations

from numpy import uint8, ndarray, array
from ..core import Core

class Node(Core):
    def __init__(self, position:ndarray, node_ix:uint8):
        # position of node in relation to the grid
        self.position: ndarray = position

        # node index in the lookup
        self.node_ix: uint8 = node_ix

        # ports labellings of the node
        self.ports: ndarray = array(['n', 'nw', 'sw', 's', 'se', 'ne'])

        # dictionary identifying ports with neighbours
        self.neighbors: dict = dict(n=None, nw=None, sw=None, 
                                    s=None, se=None, ne=None)

        # 1 if a bot is on the node, 0 otherwise
        self.occupied: uint8 = None

        # the bot currently occupying this node
        self.bot: object = None

    def scan_port(self, port:str) -> object:
        r"""
        scan neighbouring ports and create nodes for bots to move into
        """

        node = self.neighbors[port]
        
        if node is None:
            
            # create a spare `Node` object
            node = Node()
        
        return node

    def arrival(self, bot:object):
        r""" mark bot arrival on node
        """
        self.occupied = uint8(1)
        self.bot = bot

    def departure(self):
        r""" mark bot departure from node
        """
        self.occupied = uint8(0)
        self.bot = None

    def _get_bot(self) -> object: return self.bot

    def _get_ix(self) -> uint8: return self.node_ix

    def _get_ports(self) -> ndarray: return self.ports

    def _get_occupied(self) -> uint8: return self.occupied

    def _get_neighbor(self, port:str) -> Node: return self.neighbors[port]

    def set_neighbor(self, port:str, node:Node):
        # assign a neighbouring node to port
        self.neighbors[port] = node
