from dataclasses import dataclass, field
from numpy import all, append, array, empty, ndarray, random, uint8, where, zeros
from concurrent.futures import ThreadPoolExecutor
from agent import Agent


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

    # id of bot, used for debugging purposes only
    bot_id: int = field(default=None)

    # Keeps unique ordering of ports, associated with orientation
    port_structure: ndarray = field(default=None)

    # Head of the bot
    head: object = field(default=None)

    # Tail of the bot
    tail: object = field(default=None)

    # number of agents that the bot is currently using
    number_of_agents: uint8 = field(default=None)

    # Refers to a specific space (used in scan_for_spaces)
    space: ndarray = field(default=None)

    # Array of spaces, agents take care of corresponding spaces
    spaces: ndarray = field(default=None)

    # Temporary variable used to store the end of a space that continues through the origin of orientation
    temp_space: str = field(default=None)

    # Keeps number of ports scanned during space scanning
    port_count: uint8 = field(default=None)

    # Used to signal if current scan is in a space (used in scan_for_spaces)
    scan_flag: uint8 = field(default=None)

    # Keeps array of working agents
    agents: ndarray = field(default=None)

    # Keeps the status of the leader election algorithm. 0 means unfinished, 1 means finished.
    leader_election_status: ndarray = field(default=None)

    # Used to establish links
    publishing: ndarray = field(default=None)

    # 0 means this bot is not the leader, 1 means this bot is the leader (should be assigned after leader election
    leader: uint8 = field(default=None)

    # 0 means that this bot is inactive, 1 means this bot is active
    active: uint8 = field(default=None)

    # 0 means the orientation phase is unfinished, 1 means that it is.
    orientate_status: uint8 = field(default=None)

    # 0 means that the scan_for_spaces algorithm is unfinished, 1 means that it it.
    scan_for_spaces_status: uint8 = field(default=None)

    def clean_publishing_slot(self, slot=None):
        self.publishing[slot] = None

    def engine(self):

        # Moves class variables to local variables
        active = self.active
        agents = self.number_of_agents

        leader_election = self.thread_leader_election
        leader_election_status = self.leader_election_status

        orientate = self.orientate
        orientate_status = self.orientate_status

        spaces_status = self.scan_for_spaces_status

        thread_spaces_and_leader = self.multi_task_scan_for_spaces_and_run_leader_election


        # Checks if the bot is active
        if active:

            # Checks if the bot has been orientated
            if not orientate_status:

                # Runs class function orientate and stores result
                orientate_status = orientate()

                # Moves local variable back to class variable
                self.orientate_status = orientate_status

                return uint8(0)

            # Checks if bot has finished scanning for spaces
            elif not spaces_status:

                # Runs multi thread function to complete port scan and start leader election when spaces are found
                thread_spaces_and_leader()

                return uint8(0)

            # Checks if the bot ended up with no agents
            elif agents == 0:

                # Deactivates bot. Most likely will be changed.
                active = uint8(0)

                # Moves local variable back to class variable
                self.active = active

                return uint8(0)

            # Checks if the leader election is done.
            elif not all(leader_election_status):

                # Runs leader election
                leader_election()

                return uint8(0)

            # Algorithm is done for now
            else:

                return uint8(1)

        # Bot is deactivated
        else:

            return uint8(1)

    def get_head(self):
        return self.head

    def get_id(self):
        return self.bot_id

    def get_published(self):
        return self.publishing

    def initialize(self):
        self.active = uint8(1)
        self.agents = array([Agent(), Agent(), Agent()])
        self.head.arrival(bot=self)
        self.leader = uint8(0)
        self.leader_election_status = zeros(3, dtype='uint8')
        self.number_of_agents = uint8(0)
        self.orientate_status = uint8(0)
        self.port_count = uint8(0)
        self.port_structure = empty(0, dtype="<U12")
        self.publishing = empty(3, dtype='object')
        self.scan_flag = uint8(0)
        self.scan_for_spaces_status = uint8(0)
        self.space = empty([2], "<U12")
        self.spaces = empty([3, 2], dtype="<U12")
        self.tail = self.head

        return



    def multi_task_scan_for_spaces_and_run_leader_election(self):

        # Moves class variables to local variables
        scan = self.scan_for_spaces
        agents = self.number_of_agents
        spaces = self.spaces
        head = self.head
        run_agent = self.run_agent

        # Uses thread pool function in futures to run up to four threads at once
        with ThreadPoolExecutor(max_workers=4) as ex:

            # Uses one thread to scan for spaces and store thread result in local variable
            result_0 = ex.submit(scan)

            # Loops through the number of agents
            for agent in range(agents):

                # Starts thread for associated agent. Run agent is the function being called by the thread. Spaces with
                # the associated agent number and 0 (for predecessor) or 1 (for successor) is also passes. The current
                # node is also passed as head.
                ex.submit(run_agent, agent, spaces[agent][0], spaces[agent][1], head)

            # Waits for all threads to finish.
            ex.shutdown(wait=True)

        # Stores result of scan for spaces done by thread
        result = result_0.result()

        # Moves result from local variable to class variable.
        self.scan_for_spaces_status = result

        return

    def orientate(self):
        """
        Creates internal list self.port_structure.
        Orientates bot on grid.
        Currently, randomly gives bot random orientation.

        :return: None
        """

        # Moves class variables to local variables
        choices = self.head.get_ports()
        structure = self.port_structure

        # Assigns length of choices array to local variable
        size_of_choices = uint8(len(choices))

        # Uses numpy random choice to chose a single choice from choices array
        choice = random.choice(choices)

        # Finds in the choices array where the random choice is and assigns the index to a local variable
        choice_index = uint8(where(choices == choice))

        # Loops through the size of the array
        for _ in range(size_of_choices):

            # appends to structure the string in choices associated with the index at choice index mod 6
            structure = append(structure, choices[choice_index % uint8(6)])

            # Increments index by one.
            choice_index += uint8(1)

        # assigns result of algorithm to class variable. Result: random clockwise order of node ports.
        self.port_structure = structure

        return uint8(1)

    def publish(self, agent_id=None, item=None):
        """
        This method writes information (ex tokens)to the selected agent
        """
        self.publishing[agent_id] = item

        return

    def scan_for_spaces(self):

        # Moves class variables to local variables
        check_neighbor = self.head.check_neighbor
        port_structure = self.port_structure
        port_count = self.port_count
        scan_flag = self.scan_flag
        space = self.space
        temp_space = self.temp_space
        spaces = self.spaces
        number_of_agents = self.number_of_agents

        # Checks the neighbor node associated with port_count mod 6 to see if it is occupied.
        occupied_status = check_neighbor(port=port_structure[port_count % 6]).get_occupied()

        # Checks occupied status results
        if not occupied_status:

            # If the space is not occupied it means we are within a space and the flag should be set.
            scan_flag = uint8(1)

        # if the space is occupied and the flag is set, it means we are coming out of a space.
        elif occupied_status and scan_flag:

            # Checks if a predecessor has been assigned to current space
            if not space[0]:

                # Assign node to predecessor position in space
                space[0] = port_structure[port_count % 6]

                # Sets node to temp space because we were in a space but didn't have predecessor. This means that
                # the current node is a successor to space we were in.
                temp_space = port_structure[port_count % 6]

            # Predecessor has been selected for this space
            else:

                # Assigns current port as successor for the current space
                space[1] = port_structure[port_count % 6]

            # Closes space
            scan_flag = uint8(0)

        # Checks if the node is occupied and we aren't current evaluating a space
        elif occupied_status and not scan_flag:

            # Add current node as a predecessor
            space[0] = port_structure[port_count % 6]

        # Checks if predecessor and successor roles have been met
        if space[0] and space[1]:

            # Checks if the space results are already apart of our spaces array
            if space not in spaces:

                # adds the space to the position associated with an agent
                spaces[number_of_agents] = space

                # resets space
                space = empty(2, "<U12")

                # Adds increment the number of bots by one
                number_of_agents += uint8(1)

                # Adds current node to predecessor position for next space evaluation
                space[0] = port_structure[port_count % 6]

        # Moves local variables to class variable
        self.port_structure = port_structure
        self.port_count = port_count
        self.scan_flag = scan_flag
        self.space = space
        self.temp_space = temp_space
        self.spaces = spaces
        self.number_of_agents = number_of_agents

        # Checks if port count is over 5
        if port_count > 5:

            # Checks if temporary space was used.
            if self.temp_space:

                # Assigns temporary space as successor ove the current space
                self.space[1] = self.temp_space

                # adds the space to the position associated with an agent
                self.spaces[self.number_of_agents] = self.space

                # Increases number of agents by one
                self.number_of_agents += uint8(1)

            return uint8(1)

        # Increases port count by one
        self.port_count += uint8(1)

        return uint8(0)

    def run_agent(self, agent=None, predecessor=None, successor=None, current_node=None):

        # Moves class variables to local variables
        initialized = self.agents[agent].is_initialized()
        status = self.leader_election_status[agent]
        leader_election = self.agents[agent].leader_election

        # Checks if agent has been initialized
        if not initialized:

            # Moves class variables to local variables
            initialize = self.agents[agent].initialize

            # Runs initialize method for agent
            initialize(predecessor=predecessor, successor=successor, current_node=current_node, bot=self, agent=agent)

        # Checks leader election status associated with agent
        if not status:

            # Runs leader election and stores result in status
            status = leader_election()

            # Moves status back to class variable in the position associated with the agent
            self.leader_election_status[agent] = status

        return

    def thread_leader_election(self):

        # Moves class variables to local variables
        agents = self.number_of_agents
        leader_election_status = self.leader_election_status
        run_agent = self.run_agent
        spaces = self.spaces
        head = self.head

        # Checks if the number of agents is one
        if agents == 1:

            # Assigns leader election status index one and two to one
            leader_election_status[1] = uint8(1)
            leader_election_status[2] = uint8(1)

        # Checks if the number of agents is two
        elif agents == 2:

            # Assigns leader election status index one and two to one
            leader_election_status[2] = uint8(1)

        # Uses thread pool function in futures to run up to four threads at once
        with ThreadPoolExecutor(max_workers=3) as ex:

            # Loops through the number of agents
            for agent in range(agents):

                # Starts thread for associated agent. Run agent is the function being called by the thread. Spaces with
                # the associated agent number and 0 (for predecessor) or 1 (for successor) is also passes. The current
                # node is also passed as head.
                ex.submit(run_agent, agent, spaces[agent][0], spaces[agent][1], head)

            # Waits for all threads to finish.
            ex.shutdown(wait=True)

        # Moves result from local variable to class variable.
        self.leader_election_status = leader_election_status

        return
