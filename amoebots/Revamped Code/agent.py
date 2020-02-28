from dataclasses import dataclass, field

import link as lk
import package as pk
import numpy as np


@dataclass
class Agent:
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

    link: object = field(default=lk.Link())
    link_published: np.uint8 = field(default=np.uint8(0))
    links_tested: np.uint8 = field(default=np.uint8(0))
    links_established: np.uint8 = field(default=np.uint8(0))
    predecessor_link: object  = field(default=None)
    publish: object = field(default=None)

    def boundary_setup(self):
        if not self.link_published:
            package = pk.Package()
            package.store_link(access=self.predecessor_bot,link=self.link)
            self.bot.publish(agent_id=self.agent_id, item=package)
            self.link_published = np.uint8(1)
        elif self.predecessor_link is None:
            published = self.predecessor_bot.get_published()
            for i in range(3):
                if published[i].authorize(bot=self.bot):
                    self.predecessor_link = published[i].get_link()
        elif not self.links_established:
            if not self.links_tested:
                self.link.test_signal()
                self.predecessor_link.test_signal()
                self.links_tested = np.uint8(1)
            elif self.link.get_test() == 2 and self.predecessor_link == 2:
                self.links_established = np.uint8(1)

    def get_published(self):
        return self.publish

    def initialize(self, predecessor=None, successor=None, current_node=None, bot=None, agent=None):
        self.predecessor = predecessor
        self.successor = successor
        self.current_node = current_node
        self.predecessor_node = self.current_node.get_bot()
        self.successor_node = self.current_node.get_bot()
        self.predecessor_bot = self.current_node.get_bot()
        self.successor_bot = self.current_node.get_bot()
        self.bot = bot
        self.agent_id = agent
        self.initialized = np.uint8(1)

    def is_initialized(self):
        return self.initialized

    def leader_election(self):
        if not self.links_established:
            self.boundary_setup()
            return np.uint8(0)
        return np.uint8(1)
