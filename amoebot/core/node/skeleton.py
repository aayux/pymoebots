from dataclasses import dataclass, field
from numpy import uint8, ndarray, array

@dataclass
class Node(object):
    # position of node in relation to the grid
    position: ndarray = field(default=None)

    # node index in the lookup
    node_ix: uint8 = field(default=None)

    # ports labellings of the node
    ports: ndarray = field(default=None)

    # dictionary identifying ports with neighbours
    neighbors: dict = field(default=None)

    # 1 if a bot is on the node, 0 otherwise
    occupied: uint8 = field(default=None)

    # the bot currently occupying this node
    bot: object = field(default=None)

    def _post_init_(self):
        self.ports = array(['n', 'nw', 'sw', 's', 'se', 'ne'])
        self.neighbors = dict(n=None, nw=None, sw=None, 
                              s=None, se=None, ne=None)

    def scan_port(self, port:str) -> object:
        r"""
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

    def _get_neighbor(self, port:str) -> object: return self.neighbors[port]

    def _set_neighbor(self, port: str, node: object):
        # assign a neighbouring node to port
        self.neighbors[port] = node
