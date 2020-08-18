from numpy import int8, ndarray, array

from ..core import Core

class Node(Core):
    def __init__(self, position:ndarray, wall:bool=False):
        r"""
        `position`  ::

        `neighbors` :: 

        `occupied`  ::  occupancy status of the current node

                        0   : node is unoccupied, 
                        1   : occupied by a contracted bot, 
                        2   : occupied by tail, 
                        3   : occupied by head, 
                        4   : trace particle on node, 
                        5   : node is a wall
        """

        # position of node in relation to the grid
        self.position:ndarray = position

        # ports labellings of the node
        self.ports:ndarray = array(['n', 'ne', 'se', 
                                    's', 'sw', 'nw'
                                ], dtype='<U2')

        # dictionary identifying neighbouring port locations
        self.neighbors:dict = dict(n=None, ne=None, se=None, 
                                   s=None, sw=None, nw=None)

        # occupancy status of the current node
        self.occupied:int8 = int8(5) if wall else int8(0)

    def place_particle(self, particle:str):
        r""" mark the node occupancy status during initialisation
        """
        particle_map = dict([
                            ('amoebot', int8(1)), 
                            ('amoebot tail', int8(2)), 
                            ('amoebot head', int8(3))
                        ])

        assert particle in particle_map, \
            LookupError(
                f'invalid particle {particle}'
            )

        self.occupied = particle_map[particle]

    def update_node_status(self, action:str):
        r""" mark the node occupancy status during amoebot activity
        """
        action_map = dict([
                            ('expand from', int8(2)), 
                            ('expand to', int8(3)), 
                            ('contract to', int8(1)), 
                            ('contract from', int8(0)), 
                            ('drop trace', int8(4))
                        ])

        assert action in action_map, \
            LookupError(
                f'invalid action {action}'
            )
        
        self.occupied = action_map[action]

    def set_neighbor(self, port:str, node_position:ndarray):
        # assign a neighbouring node to port
        self.neighbors[port] = node_position

    def get_neighbor(self, port:str) -> ndarray: return self.neighbors[port]

    @property
    def get_occupancy_status(self) -> int8: return self.occupied
    
    @property
    def get_all_ports(self) -> ndarray: return self.ports

    @property
    def is_occupied(self) -> bool:
        return int8(1) if self.occupied is not 0 else int8(0)

    @property
    def is_trace(self) -> bool:
        return int8(1) if self.occupied is 3 else int8(0)

    @property
    def is_wall(self) -> bool:
        return int8(1) if self.occupied is 4 else int8(0)

