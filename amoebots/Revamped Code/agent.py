from dataclasses import dataclass, field

import link as lk
import package as pk
import numpy as np


@dataclass
class Agent:
    """This class is responsible for an agent's attributes and functions"""
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
    candidate_coin_flipped: np.uint8 = field(default=np.uint8(0))
    candidate_coin_flip_result: np.uint8 = field(default=np.uint8(0))

    # identifier_setup
    identifier: np.uint8 = field(default=None)

    def boundary_setup(self):
        if not self.link_published:
            self.link = lk.Link(link_id=self.bot.get_id())
            package = pk.Package()
            package.store_link(access=self.predecessor_bot,link=self.link)
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
            elif self.link.get_test() == 2 and self.successor_link.get_test() == 2:
                self.links_established = np.uint8(1)
                self.clean_publishing_slot(slot=self.agent_id)

    def clean_publishing_slot(self, slot=None):
        self.bot.clean_publishing_slot(slot=slot)

    def get_published(self):
        return self.publish

    def identifier_setup(self):
        if self.candidate_coin_flip_result:
            if self.identifier is not None:
                self.identifier = np.random.choice(np.array([0, 1], dtype='uint8'))
            else:
                pass

    def initialize(self, predecessor=None, successor=None, current_node=None, bot=None, agent=None):
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
        return self.initialized

    def leader_election(self):
        if not self.links_established:
            self.boundary_setup()
            return np.uint8(0)
        # elif not self.candidate_coin_flipped:
        #     self.segment_setup()
        #     return np.uint8(0)
        return np.uint8(1)

    def segment_setup(self):
        """This method determines if the agent is a candidate by randomly selecting zero or one. One makes the agent a candidate, zero makes the agent a non-candidate."""
        self.candidate_coin_flip_result = np.random.choice(np.array([0, 1], dtype='uint8'))
        self.candidate_coin_flipped = np.uint8(1)
