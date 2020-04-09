from dataclasses import dataclass, field
from numpy import uint8, uint16, uint32, uint64, ndarray
from .skeleton import Node
from ..utils.baseutils import increment_index

@dataclass
class NodeManager(object):
    # dictionary of `Node` objects
    node_dict: dict = field(default=None)

    # numpy array of plotted points
    plotted_points: ndarray = field(default=None)

    # next available index in the lookup
    next_index: uint8 = uint8(0)

    def add_node(self, position:ndarray):
        r"""
        adds individual nodes to node lookup
        """
        # creates node and assigns it a place in the node dictionary
        self.node_dict[self.next_index] = Node(position=position, 
                                               node_ix=self.next_index)

        # increment the index by one
        self.next_index = increment_index(self.next_index)

    def grid_builder(self):
        r""" 
        create nodes at grid positions and link the nodes into a full grid
        """
        # rows and cols in the plotted points on the grid
        nrows, ncols, _ = self.plotted_points.shape

        # place nodes on the grid
        for ix in range(nrows):
            for jx in range(ncols):
                # add node to node manager
                self.add_node(position=self.plotted_points[ix][jx])

        # calls function to link all the created nodes together
        self.link(nrows)

    def link(self, nrows:int):
        r"""
        """

        # assigns class variables to method variable
        node_dict = self.node_dict
        index_range = len(self.node_dict)

        # Initializes method specific variables. Prev_row keeps a dictionary of nodes that belong to the previous row.
        # Row flag keeps track of even or odd rows, True means odd, False otherwise
        prev_row = {}
        row_flag = True

        # Loops through all points associated with the current grid
        for index in range(index_range):

            # Pulls node from current index in our node dictionary
            node = self.node_dict[index]

            # Checks of there is an entry for the next index position in our node dictionary and makes sure that it is
            # not a new row.
            if index + 1 in self.node_dict and (index + 1) % nrows:

                # Pulls next node from dictionary
                next_node = self.node_dict[index + 1]

                # Sets current nodes right neighbor to next node
                node.set_neighbor(port='right', node=next_node)

                # Sets next nodes left neighbor to current node
                next_node.set_neighbor(port='left', node=node)

            # Checks if the current index modded by row is 0
            if not index % nrows:

                # If it is, then switch row flag
                row_flag = not row_flag

            # If row flag is True it means we are on an odd row
            if row_flag:

                # Checks if the result of the current index modded by the row is in the previous row dictionary.
                if index % nrows in prev_row:

                    # If it is, then pull next node to work with from previous node dictionary
                    next_node = prev_row[index % nrows]

                    # Sets current nodes bottom left neighbor as the next node
                    node.set_neighbor(port='bottom left', node=next_node)

                    # Sets the next nodes top right neighbor as the cuurent node
                    next_node.set_neighbor(port='top right', node=node)

                # Checks if the result of the current index modded by the row plus 1 is in the previous row dictionary.
                if (index % nrows) + 1 in prev_row:
                    next_node = prev_row[(index % nrows) + 1]

                    # Sets current nodes bottom right neighbor as the next node
                    node.set_neighbor(port='bottom right', node=next_node)

                    # Sets the next nodes top left neighbor as the cuurent node
                    next_node.set_neighbor(port='top left', node=node)

            # Current row is even
            else:

                # Checks if the result of the current index modded by the row is in the previous row dictionary.
                if index % nrows in prev_row:

                    # If it is, then pull next node to work with from previous node dictionary
                    next_node = prev_row[index % nrows]

                    # Sets current nodes bottom right neighbor as the next node
                    node.set_neighbor(port='bottom right', node=next_node)

                    # Sets the next nodes top left neighbor as the cuurent node
                    next_node.set_neighbor(port='top left', node=node)

                    # Sets next node variable to whatever node that is to the left of the current next node
                    next_node = next_node.get_neighbor(port='left')

                    # Checks if there is a next node
                    if next_node:

                        # Sets current nodes bottom left neighbor as the next node
                        node.set_neighbor(port='bottom left', node=next_node)

                        # Sets the next nodes top right neighbor as the cuurent node
                        next_node.set_neighbor(port='top right', node=node)

            # Puts current node into the previous row dictionary at the index mode row
            prev_row[index % nrows] = node

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

    def set_plotted_points(self, plotted_points):

        # set plotted points to  class variable
        self.plotted_points = plotted_points

