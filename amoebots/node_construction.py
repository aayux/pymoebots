class Node(object):
    """
    Node class that acts as node objects for bot landing.
    """

    def __init__(self):
        self.__right = None
        self.__bottom_right = None
        self.__bottom_left = None
        self.__left = None
        self.__top_left = None
        self.__top_right = None
        self.__position = None
        self.__occupied = False
        self.__bot = None

        self.__debug = False

    def get_node(self, value):
        """
        Gets node based on it's relative position:

        :param value: a direction keyword that acts as the trigger to a condition to return the right node.
        :type value: str
        :return: node_construction.Node
        """
        if value == 'right':
            return self.__right
        elif value == 'bottom right':
            return self.__bottom_right
        elif value == 'bottom left':
            return self.__bottom_left
        elif value == 'left':
            return self.__left
        elif value == 'top left':
            return self.__top_left
        elif value == 'top right':
            return self.__top_right

    def set_position(self, value):
        """
        sets the position of the node
        TODO: change this to {x:int, y:int} structure
        :param value: (x, y)
        :type value: list or tuple
        :return: None
        """
        self.__position = value

    def set_node(self, value, node):
        """
        sets the node associated with value relative to this node.

        :param value: Direction keyword
        :type value: str
        :param node: Node reference to set as relative to this node.
        :type node: node_construction.Node
        :return: None
        """

        if value == 'right':
            self.__right = node
        elif value == 'bottom right':
            self.__bottom_right = node
        elif value == 'bottom left':
            self.__bottom_left = node
        elif value == 'left':
            self.__left = node
        elif value == 'top left':
            self.__top_left = node
        elif value == 'top right':
            self.__top_right = node

    def get_position(self):
        """
        gets position of node.
        TODO: change this to {x:int, y:int} structure

        :return: (x, y) tuple
        """

        return self.__position

    def arrival(self, bot):
        """
        Add the bot that arrives on this node

        :param bot: reference to bot on this space
        :type bot: bot_construction.Bot
        :return: None
        """
        self.__occupied = True
        self.__bot = bot

    def departure(self):
        """
        Removes bot and unoccupies node after bot leaves.

        :return: Node
        """
        self.__occupied = False
        self.__bot = None

    def get_occupied(self):
        """
        Is node occupied?
        :return: bool
        """
        return self.__occupied

    def toggle_debug(self):
        """
        Toggle debug mode on this node.

        :return: None
        """
        self.__debug = not self.__debug
        print("This Node is in debug mode")

    def toggle_occupied(self):
        if self.__debug:
            self.__occupied = not self.__occupied
        else:
            print("Unable to toggle occupied settings. Bot not in debug mode")

    def create_node(self, node=None, choice=None):
        new_node = Node()
        if choice == 'right':

            position = (node.get_position()[0], node.get_position()[1]+2)
            new_node.set_position(position)
            self.link_nodes(choice=choice, node_1=node, node_2=new_node)
        elif choice == 'bottom right':
            position = (node.get_position()[0]-1, node.get_position()[1] + 1)
            new_node.set_position(position)
            self.link_nodes(choice=choice, node_1=node, node_2=new_node)
        elif choice == 'bottom left':
            position = (node.get_position()[0]-1, node.get_position()[1] - 1)
            new_node.set_position(position)
            self.link_nodes(choice=choice, node_1=node, node_2=new_node)
        elif choice == 'left':
            position = (node.get_position()[0], node.get_position()[1] - 2)
            new_node.set_position(position)
            self.link_nodes(choice=choice, node_1=node, node_2=new_node)
        elif choice == 'top left':
            position = (node.get_position()[0]+1, node.get_position()[1] - 1)
            new_node.set_position(position)
            self.link_nodes(choice=choice, node_1=node, node_2=new_node)
        elif choice == 'top right':
            position = (node.get_position()[0]+1, node.get_position()[1] + 1)
            new_node.set_position(position)
            self.link_nodes(choice=choice, node_1=node, node_2=new_node)

    def link_nodes(self, choice=None, node_1=None, node_2=None):
        if choice == 'right':
            node_1.set_node(value=choice, node=node_2)
            node_2.set_node(value="left", node=node_1)
        elif choice == 'bottom right':
            node_1.set_node(value=choice, node=node_2)
            node_2.set_node(value="top left", node=node_1)
        elif choice == 'bottom left':
            node_1.set_node(value=choice, node=node_2)
            node_2.set_node(value="top right", node=node_1)
        elif choice == 'left':
            node_1.set_node(value=choice, node=node_2)
            node_2.set_node(value="right", node=node_1)
        elif choice == 'top left':
            node_1.set_node(value=choice, node=node_2)
            node_2.set_node(value="bottom right", node=node_1)
        elif choice == 'top right':
            node_1.set_node(value=choice, node=node_2)
            node_2.set_node(value="bottom leftt", node=node_1)





class NodeManager(object):
    """
    Class used to manage a cluster of nodes

    :var node self.__head:
    """

    def __init__(self):
        self.__head = None
        self.__tail = self.__head
        self.__node_array = []
        self.__point_array = []
        self.__number_of_nodes = 0
        self.__cluster_info = None

    def create_cluster(self, x=None, y=None, origin=None):
        """
        creates a x by y sized cluster of nodes

        :param int x:
        :param y:
        :param origin:
        :return:
        """

        # set origin if origin is not specified
        if origin is None:
            origin = [0, 0]

        # set y value if y is not specified
        if y is None:
            y = x

        self.__cluster_info = [x, y, origin]

        for i in range(y):
            for j in range(x):
                # checks if the algorithm has started
                if self.__head is None:

                    # creates new node at head and assigns tail to it
                    self.__head = Node()
                    self.__tail = self.__head

                    # assigns new node the origin
                    self.__head.set_position(origin)

                elif i % 2 == 0:
                    # checks if current node is on the proper node before starting
                    if self.__tail.get_position()[1] != i:

                        # creates new node at top left and links the new node to the old one
                        self.__tail.set_node('top left', Node())
                        self.__tail.get_node('top left').set_node('bottom right', self.__tail)

                        # collects current position and moves tail to top left node
                        current_position = self.__tail.get_position()[:]
                        self.__tail = self.__tail.get_node('top left')

                        # assigns current node it's position
                        current_position[0] -= 1
                        current_position[1] += 1
                        self.__tail.set_position(current_position)

                    elif i != 0:
                        # creates left node
                        self.__tail.set_node('right', Node())

                        # This portion links the left nodes right value to the current node
                        self.__tail.get_node('right').set_node('left', self.__tail)

                        # This portion completes the triangle linking the bottom left node to the left node and vice
                        # versa
                        self.__tail.get_node('right').set_node('bottom left', self.__tail.get_node('bottom right'))
                        self.__tail.get_node('bottom right').set_node('top right', self.__tail.get_node('right'))

                        # completes the triangle between the left, left's bottom left and left's bottom right
                        temp = self.__tail.get_node('bottom right').get_node('right')
                        temp.set_node('top left', self.__tail.get_node('right'))
                        self.__tail.get_node('right').set_node('bottom right', temp)

                        # collects current position and moves tail to the left
                        current_position = self.__tail.get_position()[:]
                        self.__tail = self.__tail.get_node('right')

                        # assigns node its position
                        current_position[0] += 2
                        self.__tail.set_position(current_position)

                    else:
                        # creates new node at top left and links the new node to the old one
                        self.__tail.set_node('right', Node())
                        self.__tail.get_node('right').set_node('left', self.__tail)

                        # collects current position and moves tail to the left
                        current_position = self.__tail.get_position()[:]
                        self.__tail = self.__tail.get_node('right')

                        # assigns node its position
                        current_position[0] += 2
                        self.__tail.set_position(current_position)

                elif i % 2 == 1:
                    # checks if current node is on the proper node before starting
                    if self.__tail.get_position()[1] != i:

                        # creates new node at top left and links the new node to the old one
                        self.__tail.set_node('top right', Node())
                        self.__tail.get_node('top right').set_node('bottom left', self.__tail)

                        # collects current position and moves tail to top left node
                        current_position = self.__tail.get_position()[:]
                        self.__tail = self.__tail.get_node('top right')

                        # assigns current node it's position
                        current_position[0] += 1
                        current_position[1] += 1
                        self.__tail.set_position(current_position)

                    else:
                        # creates left node
                        self.__tail.set_node('left', Node())

                        # This portion links the left nodes right value to the current node
                        self.__tail.get_node('left').set_node('right', self.__tail)

                        # This portion completes the triangle linking the bottom left node to the left node and vice
                        # versa
                        self.__tail.get_node('left').set_node('bottom right', self.__tail.get_node('bottom left'))
                        self.__tail.get_node('bottom left').set_node('top left', self.__tail.get_node('left'))

                        # completes the triangle between the left, left's bottom left and left's bottom right
                        temp = self.__tail.get_node('bottom left').get_node('left')
                        temp.set_node('top right', self.__tail.get_node('left'))
                        self.__tail.get_node('left').set_node('bottom left', temp)

                        # collects current position and moves tail to the left
                        current_position = self.__tail.get_position()[:]
                        self.__tail = self.__tail.get_node('left')

                        # assigns node it's position
                        current_position[0] -= 2
                        self.__tail.set_position(current_position)
                self.__point_array.append(self.__tail.get_position())
                self.__node_array.append(self.__tail)
                self.__number_of_nodes += 1

    def plot(self):
        """
        creates the plot data for visual construction.

        :return: For lists of x and y points. [0] and [1] pertain to the straigt lines in the plot, while [2] and [3]
            pertain to the zig-zag portion
        """

        # parses cluster info into xy components for straight line and zig-zag computation.
        plot_x = [self.__cluster_info[2][0]]
        plot_y = [self.__cluster_info[2][1]]
        plot_x2 = [self.__cluster_info[2][0]]
        plot_y2 = [self.__cluster_info[2][1]]

        # creates all the straight lines needed for the plot. Starts from the bottom and works its way to the top.
        for i in range(self.__cluster_info[1]):
            for j in range(self.__cluster_info[0]):

                # skips origin
                if j == 0 and len(plot_x) == 1:
                    pass

                # if we are constructing the line on an even y value, multiply j by two to get our x-value and append
                # the result and i to there respective lists.
                elif i % 2 == 0:
                    plot_x.append(j * 2)
                    plot_y.append(i)

                # if we are constructing the line on an odd y value, subtract the current j value from the max x value
                # and then multiply result by two and add one to get our x-value. Append the result and i to there
                # respective lists.
                elif i % 2 == 1:
                    plot_x.append((self.__cluster_info[0] - j) * 2 - 1)
                    plot_y.append(i)

        # creates all the zig-zag lines needed for the plot. Starts from the bottom and works its way to the top.
        for i in range(self.__cluster_info[1] - 1):

            # checks if the current y value is even.
            if i % 2 == 0:
                # goes through two times the stored x value to cover all points on the y value and above the it.
                for j in range(1, self.__cluster_info[0] * 2):

                    # if the x value is odd then append the current j value but add one to the i value, else just append
                    # the values as is.
                    if j % 2:
                        plot_x2.append(j)
                        plot_y2.append(i + 1)
                    elif j % 2 == 0:
                        plot_x2.append(j)
                        plot_y2.append(i)

            # checks if the current y value is odd.
            elif i % 2:

                # goes through two times the stored x value with a displacement of negative two and traversing the list
                # backwards to cover all points on the y value and above the it.
                for j in range(self.__cluster_info[0] * 2 - 2, -1, -1):
                    # if the x value is even then append the current j value but add one to the i value, else just
                    # append the values as is.
                    if j % 2:
                        plot_x2.append(j)
                        plot_y2.append(i)
                    elif j % 2 == 0:
                        plot_x2.append(j)
                        plot_y2.append(i + 1)

        return [plot_x, plot_y, plot_x2, plot_y2]

    def get_node_array(self):
        return self.__node_array

    def get_points(self):
        return self.__point_array

    def get_number_of_nodes(self):
        """
        Quick function to get the total number of nodes created.

        :return: int value
        """
        return self.__number_of_nodes
