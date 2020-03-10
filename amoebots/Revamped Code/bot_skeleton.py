from dataclasses import dataclass, field

import agent as ag
import numpy as np
import concurrent.futures as cf


@dataclass
class Bot:
    """
    This class is responsible for a bot's
    general attributes and functions.
    Bot functionality will be extended by using other modules.

    :param bot_id: Bot's unique ID. Only used for debugging/non-algorithm operations.
    :type bot_id: uint

    :param port_structure: A record of a bot's neighbors, built from its self.orientate method.
    :type port_structure: Array of directional keyword strings.

    :param head:
    :type head:

    :param tail:
    :type tail:

    :param number_of_agents:
    :type number_of_agents:

    :param space:
    :type space:

    :param spaces:
    :type spaces:

    :param temp_space:
    :type temp_space:

    :param port_count:
    :type port_count:

    :param scan_flag:
    :type scan_flag:

    :param scan_flag_2:
    :type scan_flag_2:

    :param agents:
    :type agents:

    :param leader_election_status:
    :type leader_election_status:

    :param publishing:
    :type publishing:

    :param leader:
    :type leader:

    :param active:
    :type active:

    :param orientate_status:
    :type orientate_status:

    :param active:
    :type active:
    """
    # general information
    bot_id: int = field(default=None)
    port_structure: np.ndarray = field(default=None)

    # body
    head: object = field(default=None)
    tail: object = field(default=None)

    number_of_agents: np.uint8 = field(default=np.uint8(0))
    space: np.ndarray = field(default=None)
    spaces: np.ndarray = field(default=None)
    temp_space: str = field(default=None)
    port_count: np.uint8 = field(default=np.uint8(0))
    scan_flag: np.uint8 = field(default=np.uint8(0))
    scan_flag_2: np.uint8 = field(default=np.uint8(0))
    agents: np.ndarray = field(default=None)
    leader_election_status: np.ndarray = field(default=None)
    publishing: np.ndarray = field(default=None)
    leader: np.uint8 = field(default=np.uint8(0))
    active: np.uint8 = field(default=np.uint8(1))

    orientate_status: np.uint8 = field(default=np.uint8(0))
    scan_for_spaces_status: np.uint8 = field(default=np.uint8(0))

    def clean_publishing_slot(self, slot=None):
        self.publishing[slot] = None

    def engine(self):
        if self.active:
            if not self.orientate_status:
                self.orientate_status = self.orientate()
                return np.int8(0)
            elif not self.scan_for_spaces_status:
                with cf.ThreadPoolExecutor(max_workers=4) as ex:
                    result_0 = ex.submit(self.scan_for_spaces)
                    for i in range(self.number_of_agents):
                        ex.submit(self.run_agent, i + 1, self.spaces[i][0], self.spaces[i][1], self.head)
                    # if self.number_of_agents > 0 and not self.leader_election_status[0]:
                    #     ex.submit(self.run_agent, 1, self.spaces[0][0], self.spaces[0][1], self.head)
                    # if self.number_of_agents > 1 and not self.leader_election_status[1]:
                    #     ex.submit(self.run_agent, 2, self.spaces[1][0], self.spaces[1][1], self.head)
                    # if self.number_of_agents > 2 and not self.leader_election_status[2]:
                    #     ex.submit(self.run_agent, 3, self.spaces[2][0], self.spaces[2][1], self.head)
                    ex.shutdown(wait=True)
                self.scan_for_spaces_status = result_0.result()
                return np.int8(0)
            elif self.number_of_agents == 0:
                self.active = np.uint8(0)
                return np.int8(0)
            elif not np.all(self.leader_election_status):
                if self.number_of_agents == 1:
                    self.leader_election_status[1] = np.int8(1)
                    self.leader_election_status[2] = np.int8(1)
                elif self.number_of_agents == 2:
                    self.leader_election_status[2] = np.int8(1)
                with cf.ThreadPoolExecutor(max_workers=3) as ex:
                    for i in range(self.number_of_agents):
                        ex.submit(self.run_agent, i + 1, self.spaces[i][0], self.spaces[i][1], self.head)
                    # if self.number_of_agents > 0 and not self.leader_election_status[0]:
                    #     ex.submit(self.run_agent, 1, self.spaces[0][0], self.spaces[0][1], self.head)
                    # if self.number_of_agents > 1 and not self.leader_election_status[1]:
                    #     ex.submit(self.run_agent, 2, self.spaces[1][0], self.spaces[1][1], self.head)
                    # if self.number_of_agents > 2 and not self.leader_election_status[2]:
                    #     ex.submit(self.run_agent, 3, self.spaces[2][0], self.spaces[2][1], self.head)
                    ex.shutdown(wait=True)
                # print(f"i'm not resolved {self.bot_id}")
                return np.int8(0)
            else:
                return np.int8(1)
        else:
            return np.int8(1)

    def get_head(self):
        return self.head

    def get_id(self):
        return self.bot_id

    def get_published(self):
        return self.publishing

    def orientate(self):
        """
        Creates internal list self.port_structure.
        Orientates bot on grid.
        Currently, randomly gives bot random orientation.

        :return: None
        """
        self.tail = self.head
        self.head.arrival(bot=self)
        choices = self.head.get_ports()
        choice = np.random.choice(choices)
        choice_index = np.uint8(np.where(choices == choice))
        self.port_structure = np.empty(0, dtype="<U12")
        for _ in range(np.uint8(choices.size)):
            self.port_structure = np.append(self.port_structure, choices[choice_index[0] % np.uint8(6)])
            choice_index += np.uint8(1)
        self.agents = np.array([ag.Agent(), ag.Agent(), ag.Agent()])
        self.publishing = np.empty(3, dtype='object')
        self.leader_election_status = np.zeros(3, dtype='uint8')
        return np.uint8(1)

    def publish(self, agent_id=None, item=None):
        """This method writes information (ex tokens)to the selected agent"""
        self.publishing[agent_id] = item

    def scan_for_spaces(self):
        if self.space is None:
            self.space = np.empty([2], "<U12")

        if self.spaces is None:
            self.spaces = np.empty([3, 2], dtype="<U12")

        occupied_status = self.head.check_neighbor(port=self.port_structure[self.port_count % 6]).get_occupied()

        if not occupied_status:
            self.scan_flag = np.uint8(1)

        elif occupied_status and self.scan_flag:
            if not self.space[0]:
                if self.port_count % 6:
                    self.space[0] = self.port_structure[self.port_count % 6]
                    self.temp_space = self.port_structure[self.port_count % 6]
                else:
                    self.space[0] = self.port_structure[self.port_count % 6]
            else:
                self.space[1] = self.port_structure[self.port_count % 6]
            self.scan_flag = np.uint8(0)

        elif occupied_status and not self.scan_flag:
            self.space[0] = self.port_structure[self.port_count % 6]

        if self.space[0] and self.space[1]:
            if self.space not in self.spaces:
                self.spaces[self.number_of_agents] = self.space
                self.space = np.empty(2, "<U12")
                self.number_of_agents += np.uint8(1)
                self.space[0] = self.port_structure[self.port_count % 6]

        if self.port_count > 5:
            if self.temp_space:
                self.space[1] = self.temp_space
                self.spaces[self.number_of_agents] = self.space
                self.number_of_agents += np.uint8(1)
            return np.uint8(1)

        self.port_count += np.uint8(1)
        return np.uint8(0)

    def run_agent(self, agent=None, predecessor=None, successor=None, current_node=None):
        # print(f"I'm running {self.bot_id}")
        if agent == 1:
            if not self.agents[0].is_initialized():
                self.agents[0].initialize(predecessor=predecessor, successor=successor, current_node=current_node,
                                          bot=self, agent=0)
            if not self.leader_election_status[0]:
                self.leader_election_status[0] = self.agents[0].leader_election()
        elif agent == 2:
            if not self.agents[1].is_initialized():
                self.agents[1].initialize(predecessor=predecessor, successor=successor, current_node=current_node,
                                          bot=self, agent=1)
            if not self.leader_election_status[1]:
                self.leader_election_status[1] = self.agents[1].leader_election()
        elif agent == 3:
            if not self.agents[2].is_initialized():
                self.agents[2].initialize(predecessor=predecessor, successor=successor, current_node=current_node,
                                          bot=self, agent=2)
            if not self.leader_election_status[2]:
                self.leader_election_status[2] = self.agents[2].leader_election()


if __name__ == "__main__":
    def test_single_repr():
        a = np.empty(0, dtype='object')
        bot = Bot()
        a = np.append(a, bot)
        print(f"{a}")


    def test_multiple_repr():
        a = np.empty(0, dtype="object")
        for i in range(np.uint8(10)):
            bot = Bot(bot_id=np.uint8(i))
            a = np.append(a, bot)
        print(f"{a}")


    def test_node_assignment_to_head():
        import node_manager as nm
        node_manager = nm.NodeManager()
        node_manager.add_node((np.uint8(0), np.uint8(0)))
        node = node_manager.get_node(np.uint8(0))
        bot = Bot(head=node)
        print(bot.get_head())


    def test_orientate():
        import node_manager as nm
        node_manager = nm.NodeManager()
        node_manager.add_node((np.uint8(0), np.uint8(0)))
        node = node_manager.get_node(np.uint8(0))
        bot = Bot(head=node)
        bot.orientate()
        print(f"{bot.port_structure}")


    # test_single_repr()
    # test_multiple_repr()
    # test_node_assignment_to_head()
    # test_orientate()
    pass
