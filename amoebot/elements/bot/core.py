import numpy as np

from dataclasses import dataclass, field
from numpy import array, ndarray, uint8
from ..network.agent import Agent
from ..attributes import Attributes

@dataclass
class Amoebot(Attributes):
    r"""
    core amobeot functionalities, extended using functional modules
    """

    # bot should be anonymous, use this for debugging only
    # bot_id: int = field(default=None)

    # stores unique ordering of ports
    port_labels: ndarray = field(default=None)

    # head of the bot
    head: object = field(default=None)

    # tail of the bot
    tail: object = field(default=None)

    # number of parallel agents the bot is running
    n_agents: uint8 = field(default=None)

    # numpy array of working agents
    agents: ndarray = field(default=None)

    # count of ports scanned
    n_ports_scanned: uint8 = field(default=None)

    # 1 if port scan returns an empty space
    empty_flag: uint8 = field(default=None)

    # a message pipe for sharing packets between agents
    pipe: ndarray = field(default=None)

    # activation status, true means the bot is active
    active: uint8 = field(default=None)

    def __post_init__(self):
        self.active = True
        self.agents = array([Agent(), Agent(), Agent()])
        self.n_agents = uint8(0)

        self.head.arrival(bot=self)
        self.tail = self.head

        self.n_ports_scanned = uint8(0)
        self.port_labels = np.empty(0, dtype='<U2')
        self.pipe = np.empty(3, dtype='object')
        
        self.empty_flag = uint8(0)

    def execute(self) -> uint8:
        r"""
        Worker function for each amoebot. Manages parallelisation between agents
        and attaches functional modules to the amoebot as callbacks.

        returns: np.uint8:   execution status
        """
        # if the bot is active
        if self.active:
            # do stuff
            return uint8(0)
        else:
            return uint8(1)
    
    def orient(self) -> uint8:
        r""" 
        orients with a random clockwise ordering of ports around the bot
        """

        ports = self.head._get_ports()
        n_ports = uint8(len(ports))

        # choose a port at random
        choice = np.random.choice(ports)
        choice_ix = uint8(np.where(ports == choice))

        for _ in range(n_ports):
            self.port_labels = np.append(self.port_labels, 
                                        ports[choice_ix % uint8(6)])
            choice_ix += uint8(1)

        return uint8(1)
    
    def publish(self, slot:uint8, packet:object):
        r"""
        write (tokens) to the selected agent at slot
        """
        self.pipe[slot] = packet

    def scan_ports(self) -> uint8:
        r"""
        """
        # TODO: required? copy variables and methods to avoid contention
        scan_port = self.head.scan_port
        n_ports_scanned = self.n_ports_scanned
        empty_flag = self.empty_flag

        # scan the neighbouring ports for occupancy status
        occupied = scan_port(self.port_labels[n_ports_scanned % 6]).get_occupied()
        if not occupied: empty_flag = uint8(1)

        self.port_count += uint8(1)
        self.empty_flag = empty_flag

        return uint8(0)

    def _clear_publishing_slot(self, slot:uint8): 
        self.pipe[slot] = None

    def _get_published(self): return self.publishing

    def _get_id(self): raise NotImplementedError

    def _get_head(self): return self.head
