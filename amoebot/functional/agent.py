from dataclasses import dataclass, field
from link import Link
from package import Package, Token
from numpy import uint8, array, random

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

    # Part of initialize sequence #####################################################################################
    # Hold whether the agent has been initialized or not
    initialized: uint8 = field(default=None)

    # agents predecessor
    predecessor: str = field(default=None)

    # agent's successor
    successor: str = field(default=None)

    # The current node the agent is on
    current_node: object = field(default=None)

    # The bot this agent is assigned to
    bot: object = field(default=None)

    # The agents id: range from 0-2
    agent_id: uint8 = field(default=None)

    # The reference to the node of the successor
    successor_node: object = field(default=None)

    # The reference to the node of the predecessor
    predecessor_node: object = field(default=None)

    # The reference to the successor bot
    successor_bot: object = field(default=None)

    # The reference to the predecessor bot
    predecessor_bot: object = field(default=None)

    # Constants #######################################################################################################
    DONE: uint8 = field(default=None)
    NOT_DONE: uint8 = field(default= None)
    wait_time: uint8 = field(default=uint8(50))
    wait: uint8 = field(default=uint8(0))

    done: uint8 = field(default=uint8(1))
    unfinished: uint8 = field(default=uint8(0))

    # boundary_setup ##################################################################################################
    link: object = field(default=None)
    link_published: uint8 = field(default=None)
    links_tested: uint8 = field(default=None)
    links_established: uint8 = field(default=None)
    successor_link: object = field(default=None)
    boundary_setup_status: uint8 = field(default=None)

    # segment_setup ###################################################################################################
    segment_setup_status: uint8 = field(default=None)
    candidate: uint8 = field(default=None)

    # identifier_setup ################################################################################################
    identifier_token: object = field(default=None)
    delimiter: object = field(default=None)
    delimiter_passed: object = field(default=None)
    identifier_setup_status: np.uint8 = field(default=None)


    # identifier_setup_phase_2 ########################################################################################
    identifier_setup_phase_2_status: uint8 = field(default=None)
    reversed_identifier: uint8 = field(default=None)
    activated: uint8 = field(default=None)


    def binary_choice(self):
        return random.choice(np.array([0, 1], dtype='uint8'))

    def boundary_setup(self):
        """
        Phase of the Leader Election Algorithm.

        Establishes Link objects with neighbors if
        they are a predecessor or successor.
        One Link object is shared between two instances
        of an agent.

        :return: None
        """

        # Move class variable to method variables
        established = self.links_established
        link_published = self.link_published
        successor_link = self.successor_link

        # Move class functions to method functions
        establish_link = self.establish_link
        get_successor_link = self.get_successor_link
        publish_link = self.publish_link

        # Checks if link has been published by this agent
        if not link_published:

            # Publishes link
            publish_link()

        # Checks if successor link has been retrieved
        elif successor_link is None:

            # Retrieves successor's link
            get_successor_link()

        # Checks if link has been established
        elif not established:

            # Establishes link
            establish_link()

        else:

            # Marks boundary setup as finished.
            self.boundary_setup_status = uint8(1)

        return

    def clean_publishing_slot(self, slot=None):
        """
        Calls up to the Bot hosting this
        Agent to remove any published data
        to the specified port keyword.

        :param slot: Direction keyword to clean, defaults to None
        :type slot: str

        :return: None
        """

        # Moves class variables to local variables
        clean = self.bot.clean_publishing_slot

        # cleans associated agent slot within bot.
        clean(slot=slot)

        return

    def create_uid(self):
        return array([random.randint(256, dtype='uint8'), random.randint(256, dtype='uint8')])

    def establish_link(self):

        # Store test results
        tested = self.links_tested
        link_test = self.link.get_test()
        successor_link_test = self.successor_link.get_test()
        links_established = self.links_established

        # Moves class function to method variable
        test_link = self.test_link
        established = self.established

        # Checks if collected links have been tested
        if not tested:

            # Test links
            test_link()

        # Checks if links have been tested successfully
        elif link_test == 2 and successor_link_test == 2:

            # Confirms that links have been successfully tested and a connection has been established.
            established()

        elif links_established:

            self.boundary_setup_status = uint8(1)

        return

    def established(self):

        # Moves class variables and funtions to local variables
        clean_slot = self.clean_publishing_slot
        agent = self.agent_id

        # Confirms that agent has an established link
        self.links_established = uint8(1)

        # Cleans the agents published slot head in bot
        clean_slot(slot=agent)

        return

    def get_published(self):
        """
        Returns the Package object that
        the host bot has in its shared memory slot.

        TODO: I don't see this returnval defined anywhere,
        has it been renamed?

        :return: package.Package
        """
        return self.publish

    def get_successor_link(self):
        # Grabs published array from successor
        published = self.successor_bot.get_published()

        # Loops through possible number of agents
        for i in range(3):

            # Checks if the value at the index of the published array is not None and the current agent is authorized to
            # access the package
            if published[i] is not None and published[i].authorize(bot=self.bot):

                # Puts package link in local variable
                link = published[i].get_link()

        # Move local variable to class variable
        self.successor_link = link

        return

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
        DONE = self.DONE
        next_status = self.successor_link.successor_agent.segment_setup_status
        next_is_candidate = self.successor_link.successor_agent.candidate

        if next_status and not next_is_candidate:

            if self.candidate:

                if self.delimiter_passed is None:
                    token_id = self.create_uid()
                    identifier = self.binary_choice()
                    self.identifier_token = Token(token_id=token_id, identifer=identifier)

                    delimiter = Token(delimiter=uint8(1), identifer=identifier)
                    self.successor_link.load_delimiter(delimiter=delimiter)
                    self.delimiter_passed = uint8(1)
                    self.identifier_setup_status = DONE

            else:

                if self.link.get_delimiter() is not None:
                    token_id = self.create_uid()
                    identifier = self.binary_choice()
                    self.identifier_token = Token(token_id=token_id, identifer=identifier)

                    self.successor_link.load_delimiter(delimiter=self.link.get_delimiter())
                    self.link.remove_delimiter()
                    self.identifier_setup_status = DONE

        elif next_status and next_is_candidate:

            if self.candidate:
                token_id = self.create_uid()
                identifier = self.binary_choice()
                self.identifier_token = Token(token_id=token_id, identifer=identifier)

                self.delimiter = Token(delimiter=uint8(1), identifer=identifier)
                self.identifier_setup_status = DONE

            else:
                token_id = self.create_uid()
                identifier = self.binary_choice()
                self.identifier_token = Token(token_id=token_id, identifer=identifier)

                self.delimiter = self.link.get_delimiter()
                self.identifier_setup_status = DONE

        self.wait += uint8(1)

        if self.wait_time == self.wait:
            self.segment_setup_status = self.unfinished

    def identifier_setup_phase_2(self):
        predecessor_candidacy = self.link.get_predecessor_candidacy()
        if predecessor_candidacy:
            if self.candidate:
                self.reversed_identifier = self.delimiter
                self.identifier_setup_phase_2_status = self.done
            else:
                pass
        if self.delimiter:
            pass

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

        self.DONE = uint8(1)
        self.NOT_DONE = uint8(0)
        self.wait_time = uint8(50)
        self.wait = uint8(0)

        DONE = self.DONE
        NOT_DONE = self.NOT_DONE

        self.predecessor = predecessor
        self.successor = successor
        self.current_node = current_node
        self.predecessor_node = self.current_node.check_neighbor(port=predecessor)
        self.successor_node = self.current_node.check_neighbor(port=successor)
        self.predecessor_bot = self.predecessor_node.get_bot()
        self.successor_bot = self.successor_node.get_bot()
        self.bot = bot
        self.agent_id = agent

        self.link_published = NOT_DONE
        self.links_tested = NOT_DONE
        self.links_established = NOT_DONE

        self.segment_setup_status = NOT_DONE
        self.candidate = NOT_DONE

        self.identifier_setup_phase_2_status = NOT_DONE
        self.identifier_setup_status = NOT_DONE




        self.initialized = DONE

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

        # Move class variables to method variables
        boundary_setup_status = self.boundary_setup_status
        done = self.DONE
        not_done = self.NOT_DONE

        # Move class function to method function
        boundary_setup = self.boundary_setup

        # Check
        if not boundary_setup_status:
            boundary_setup()
            return not_done
        # elif not self.segment_setup_status:
        #     self.segment_setup()
        #     return self.unfinished
        # elif not self.identifier_setup_status:
        #     self.identifier_setup()
        #     return self.unfinished
        # elif not self.identifier_setup_phase_2_status:
        #     self.identifier_setup_phase_2()
        #     return np.uint8(0)
        return done

    def publish_link(self):
        # Moves class variables to local variables
        done = self.DONE
        predecessor = self.predecessor_bot

        # Move bot function to local variable
        publish = self.bot.publish

        # Creates link instance
        link = Link()

        # Initializes link instance
        link.initialize()

        # Creates package instance
        package = Package()

        # Place predecessor and link inside package
        package.store_link(access=predecessor, link=link)

        # Publishes package to bot
        publish(agent_id=self.agent_id, item=package)

        # Moves local variable back to class variable
        self.link = link
        self.link_published = done

        return

    def segment_setup(self):
        """
        This method determines if the agent is a candidate by randomly
        selecting zero or one.
        One makes the agent a candidate,
        zero makes the agent a non-candidate.

        :return: None
        """
        self.candidate = self.binary_choice()
        self.segment_setup_status = self.done
        self.wait = uint8(0)

    def test_link(self):

        # Moves class variables to local variables
        link = self.link
        successor_link = self.successor_link

        # Runs link built in test
        link.test_signal()
        successor_link.test_signal()

        # Confirms that the agent has test both links so that it will not test the links again
        self.links_tested = uint8(1)

        # sets agent to associated position within links
        link.set_successor_agent(agent=self)
        successor_link.set_predecessor_agent(agent=self)

        # Move local variable to class variable
        self.link = link
        self.successor_link = successor_link

        return


def binary_choice():
    return random.choice(np.array([0, 1], dtype='uint8'))


def create_uid():
    return array([random.randint(256, dtype='uint8'), random.randint(256, dtype='uint8')])