from dataclasses import dataclass, field
from numpy import uint8, uint16, uint32, uint64, ndarray
from node_skeleton import Node
from reuseables import uint_limits


@dataclass
class NodeManager:
    # Dictionary of nodes
    node_dict: dict = field(default=None)

    # Numpy array of plotted points
    plotted_points: ndarray = field(default=None)

    # Initialized variables
    next_index: uint8 = field(default=None)

    def add_node(self, position=None):
        """
        Adds individual nodes to node list
        """
        # Assigns Class variable to method variable
        index = self.next_index

        # creates node and assigns it a spot in the node dictionary
        self.node_dict[index] = Node(position=position, node_id=index)

        # Creating variables for upper limits for unsigned ints
        upper_8 = uint_limits[8][1]
        upper_16 = uint_limits[16][1]
        upper_32 = uint_limits[32][1]

        # Increments index by appropriate amount and type
        if index < upper_8:
            index += uint8(1)
        elif index < upper_16:
            index += uint16(1)
        elif index < upper_32:
            index += uint32(1)
        else:
            index += uint64(1)

        # Assigns method variables back to Class variables
        self.next_index = index

    def create_node_structure(self):
        points = self.plotted_points

        # Creates variable for the rows in points
        rows = len(points)

        # Creates variable for the columns in points
        columns = len(points[0])

        # Creates variable to hold Class function
        add_node = self.add_node

        # Creates variable to hold Class function
        link_nodes = self.link_nodes

        # loops through the number of rows to add nodes
        for row in range(rows):

            # loops through the number of columns to add nodes
            for column in range(columns):

                # Creates point based on data at points[row][column]
                point = points[row][column]

                # add node to node manager
                add_node(position=point)

        # Calls function to link all the created nodes together
        link_nodes(row=columns)


    def get_node(self, node_id=None):
        """
        gets specific node from node lise.
        """
        return self.node_dict[node_id]

    def get_node_list(self):
        """
        Returns all nodes from node list
        """
        return self.node_dict

    def get_number_nodes(self):
        """
        Returns total number of nodes in graph
        """
        return len(self.node_dict)

    def initialize(self):

        # initializes next index to zero
        self.next_index = uint8(0)

        # initializes node dictionary
        self.node_dict = {}

    def link_nodes(self, row=None):
        # parameter 'row' to mod against index to determine the end of a row.

        # assigns class variables to method variable
        node_dict = self.node_dict
        index_range = len(self.node_dict)
        prev_row = {}
        row_count = -1

        for index in range(index_range):
            node = node_dict[index]
            if index + 1 in node_dict and (index + 1) % row:
                new_node = node_dict[index + 1]
                node.set_neighbor(port='right', node=new_node)
                new_node.set_neighbor(port='left', node=node)
            if not index % row:
                row_count += 1
            if row_count % 2:
                if index % row in prev_row:
                    new_node = prev_row[index % row]
                    node.set_neighbor(port='bottom left', node=new_node)
                    new_node.set_neighbor(port='top right', node=node)
                if (index % row) + 1 in prev_row:
                    new_node = prev_row[(index % row) + 1]
                    node.set_neighbor(port='bottom right', node=new_node)
                    new_node.set_neighbor(port='top left', node=node)
            else:
                if index % row in prev_row:
                    new_node = prev_row[index % row]
                    node.set_neighbor(port='bottom right', node=new_node)
                    new_node.set_neighbor(port='top left', node=node)
                    new_node = new_node.get_neighbor(port='left')
                    if new_node:
                        node.set_neighbor(port='bottom left', node=new_node)
                        new_node.set_neighbor(port='top right', node=node)
            prev_row[index % row] = node

        self.node_dict = node_dict

    def set_plotted_points(self, plotted_points):

        # set plotted points to  class variable
        self.plotted_points = plotted_points

