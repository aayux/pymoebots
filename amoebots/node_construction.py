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
        self.__bots = None

    def get_node(self, value):
        """
        Gets node based on it's relative position:

        :param str value: a value that actc as the trigger to a condition to return the right node.
        :return: node object
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

        :param value:
        :return:
        """
        self.__position = value

    def set_node(self, value, node):
        """
        sets the node associated with value relative to this node.

        :param value:
        :param node:
        :return:
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

        :return:
        """

        return self.__position

    def arrival(self, bot):
        """
        Add the bot that arrives on this n
        :param Bot bot:
        :return:
        """
        pass


class NodeManager(object):
    """
    Class used to manage a cluster of nodes

    :var node self.__head:
    """

    def __init__(self):
        self.__head = None
        self.__tail = self.__head
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

    def get_number_of_nodes(self):
        """
        Quick function to get the total number of nodes created.

        :return: int value
        """
        return self.__number_of_nodes
