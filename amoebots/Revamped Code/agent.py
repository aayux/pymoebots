from dataclasses import dataclass, field
from package import Token
from numpy import uint8

import link as lk
import package as pk
import numpy as np


@dataclass
class Agent:
    """
    This class is responsible for an
    agent's attributes and functions.
    Since most vars are established in or for certain phases,
    they may be denoted with an abbreviation of where
    they are created or primarily used.

    BS: Boundary Setup
    SS: Segment Setup
    IS: Identifier Setup
    IC: Identifier Comparison
    SV: Solitude Verification
    BI: Boundary Identification

    :param initialized: Has this agent called self.initialize()? Defaults to 0
    :type initialized: uint8 0|1

    :param predecessor: Agent which precedes this one in the DAG. Defaults to None
    :type predecessor: agent.Agent

    :param successor: Agent which succeeds this one in the DAG. Defaults to None
    :type successor: agent.Agent

    :param current_node: Node which this agent's host bot is on.
    :type current_node: node_skeleton.Node

    :param bot: Host bot of this agent.
    :type bot: bot_skeleton.Bot

    :param agent_id: This agent's ID number. Defaults to None.
    :type agent_id: uint

    :param successor_node: Reference to the succeeding Agent's node.
    :type successor_node: node_skeleton.Node

    :param predecessor_node: Reference to the preceding Agent's node.
    :type predecessor_node: node_skeleton.Node

    :param successor_bot: Reference to the succeeding Agent's host bot.
    :type successor_bot: bot_skeleton.Bot

    :param predecessor_bot: Reference to the preceding Agent's bot.
    :type predecessor_bot: bot_skeleton.Bot

    :param link: BS. Shared memory space between two neighbors. Defaults to None.
    :type link: link.Link

    :param link_published: BS. Once this agent's Link has been initialized, this becomes 1. Defaults to 0.
    :type link_published: uint8 0|1

    :param links_tested: BS. The agents has tested its connection to the Link. Defaults to 0.
    :type links_tested: uint8 0|1

    :param links_established: BS. The agent has established connection with its neighbor at the end of the link. Default to 0.
    :type links_established: uint8 0|1

    :param successor_link: BS. Reference to the link of the successor agent in the DAG. Defaults to None.
    :type successor_link: link.Link

    :param candidate_coin_flipped: SS. Has this agent flipped a coin yet to determine candidacy? Defaults to 0.
    :type candidate_coin_flipped: uint8 1|0

    :param candidate_coin_flip_result: SS. Is this agent a candidate as a result of the coin flip? Defaults to 0.
    :type candidate_coin_flip_result: uint8 1|0

    :param identifier: IS. The digit of the reverse identifier in the sequence. Separate from the original coin flip.
    :type identifier: uint8 1|0
    """
    initialized: np.uint8 = field(default=np.uint8(0))
    predecessor: str = field(default=None)
    successor: str = field(default=None)
    current_node: object = field(default=None)
    bot: object = field(default=None)
    agent_id: np.uint8 = field(default=None)
    successor_node: object = field(default=None)
    predecessor_node: object = field(default=None)
    successor_bot: object = field(default=None)
    predecessor_bot: object = field(default=None)

    # boundary_setup
    link: object = field(default=None)
    link_published: np.uint8 = field(default=np.uint8(0))
    links_tested: np.uint8 = field(default=np.uint8(0))
    links_established: np.uint8 = field(default=np.uint8(0))
    successor_link: object = field(default=None)

    # segment_setup
    segment_setup_status: np.uint8 = field(default=np.uint8(0))
    candidate: np.uint8 = field(default=np.uint8(0))

    # identifier_setup
    identifier_token: object = field(default=None)
    delimiter: object = field(default=None)
    delimiter_passed: object = field(default=None)
    identifier_setup_status: np.uint8 = field(default=np.uint8(0))
    wait_time: np.uint8 = field(default=None)
    wait: np.uint8 = field(default=None)

    def boundary_setup(self):
        """
        Phase of the Leader Election Algorithm.

        Establishes Link objects with neighbors if
        they are a predecessor or successor.
        One Link object is shared between two instances
        of an agent.

        :return: None
        """
        if not self.link_published:
            self.link = lk.Link(link_id=self.bot.get_id())
            package = pk.Package()
            package.store_link(access=self.predecessor_bot, link=self.link)
            self.bot.publish(agent_id=self.agent_id, item=package)
            self.link_published = np.uint8(1)
        elif self.successor_link is None:
            published = self.successor_bot.get_published()
            for i in range(3):
                if published[i] is not None and published[i].authorize(bot=self.bot):
                    self.successor_link = published[i].get_link()
        elif not self.links_established:
            if not self.links_tested:
                self.link.test_signal()
                self.successor_link.test_signal()
                self.links_tested = np.uint8(1)
                self.link.successor_agent = self
                self.successor_link.predecessor_agent = self
            elif self.link.get_test() == 2 and self.successor_link.get_test() == 2:
                self.links_established = np.uint8(1)
                self.clean_publishing_slot(slot=self.agent_id)

    def clean_publishing_slot(self, slot=None):
        """
        Calls up to the Bot hosting this
        Agent to remove any published data
        to the specified port keyword.

        :param slot: Direction keyword to clean, defaults to None
        :type slot: str

        :return: None
        """
        self.bot.clean_publishing_slot(slot=slot)

    def get_published(self):
        """
        Returns the Package object that
        the host bot has in its shared memory slot.

        TODO: I don't see this returnval defined anywhere,
        has it been renamed?

        :return: package.Package
        """
        return self.publish

    def identifier_setup(self):
        """
        Phase of the leader election algorithm.

        A token is passed starting from a candidate down the
        row to the end of the candidate's segment, giving each agent
        a random digit token 0 or 1 and then being passed on.

        TODO: we need to rework this to accept an incoming Package,
        let the package assign a 0 or 1 and then pass that package on.
        Before receiving this package, wait. After, move on to next phase.
        As well, the Package here has to check the next agent's candidate
        status, and not get passed if it is a candidate because it's reached
        the end of its current segment.

        :return: None
        """
        next_status = self.successor_link.successor_agent.segment_setup_status
        next_is_candidate = self.successor_link.successor_agent.candidate

        if next_status and not next_is_candidate:
            if self.candidate:
                if self.delimiter_passed is None:
                    self.identifier_token = Token(token_id=np.random.bytes(2),
                                                  identifer=np.random.choice(np.array([0, 1], dtype='uint8')))
                    self.delimiter = Token(delimiter=uint8(1))
                    self.successor_link.load_delimiter(delimiter=self.delimiter)
                    self.delimiter_passed = uint8(1)
                    self.identifier_setup_status = uint8(1)
            else:
                if self.link.get_delimiter() is not None:
                    self.identifier_token = Token(token_id=np.random.bytes(2),
                                                  identifer=np.random.choice(np.array([0, 1], dtype='uint8')))
                    self.successor_link.load_delimiter(delimiter=self.link.get_delimiter())
                    self.link.remove_delimiter()
                    self.identifier_setup_status = uint8(1)
        elif next_status and next_is_candidate:
            if self.candidate:
                self.identifier_token = Token(token_id=np.random.bytes(2),
                                              identifer=np.random.choice(np.array([0, 1], dtype='uint8')))
                self.delimiter = Token(delimiter=uint8(1))
                self.identifier_setup_status = uint8(1)
            else:
                self.identifier_token = Token(token_id=np.random.bytes(2),
                                              identifer=np.random.choice(np.array([0, 1], dtype='uint8')))
                self.identifier_setup_status = uint8(1)
        self.wait += 1
        if self.wait_time == self.wait:
            self.segment_setup_status = uint8(0)

    def initialize(self, predecessor=None, successor=None, current_node=None, bot=None, agent=None):
        """
        Initialize this agent. Sets self.initialized to 1.
        Note successor and predecessor can come from the same
        directional keyword port, but will almost always be two
        different agents.

        :param predecessor: Agent which precedes this one in the DAG. Defaults to None
        :type predecessor: agent.Agent

        :param successor: Agent which succeeds this one in the DAG. Defaults to None
        :type successor: agent.Agent

        :param current_node: Node which this agent's host bot is on.
        :type current_node: node_skeleton.Node

        :param bot: Host bot of this agent.
        :type bot: bot_skeleton.Bot

        :param agent: This agent's ID number(?) Defaults to None.
        :type agent: int(?)

        :return: None
        """
        self.predecessor = predecessor
        self.successor = successor
        self.current_node = current_node
        self.predecessor_node = self.current_node.check_neighbor(port=predecessor)
        self.successor_node = self.current_node.check_neighbor(port=successor)
        self.predecessor_bot = self.predecessor_node.get_bot()
        self.successor_bot = self.successor_node.get_bot()
        self.bot = bot
        self.agent_id = agent
        self.initialized = np.uint8(1)

    def is_initialized(self):
        """
        Whether this agent has called self.initialize().

        :return: int 0|1
        """
        return self.initialized

    def leader_election(self):
        """
        Controller for different phases of Leader Election.

        :return: 0 if not finished, 1 if finished.
        """
        if not self.links_established:
            self.boundary_setup()
            return np.uint8(0)
        elif not self.segment_setup_status:
            self.segment_setup()
            return np.uint8(0)
        elif not self.identifier_setup_status:
            self.identifier_setup()
            return np.uint8(0)
        return np.uint8(1)

    def segment_setup(self):
        """
        This method determines if the agent is a candidate by randomly
        selecting zero or one.
        One makes the agent a candidate,
        zero makes the agent a non-candidate.

        :return: None
        """
        self.candidate = np.random.choice(np.array([0, 1], dtype='uint8'))
        self.segment_setup_status = np.uint8(1)
        self.wait_time = uint8(50)
        self.wait = uint8(0)
