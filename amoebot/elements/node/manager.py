from dataclasses import dataclass, field
from numpy import uint8, uint16, uint32, uint64, ndarray
from .core import Node
from ..utils.baseutils import increment_index
from ..manager import Manager

@dataclass
class NodeManager(Manager):
    # dictionary of `Node` objects
    node_dict: dict = field(default_factory=dict)

    # numpy array of plotted points
    grid_points: ndarray = field(default=None)

    # next available index in the lookup
    next_node_ix: uint8 = uint8(0)

    def _post_init_(self, points:ndarray):
        self.grid_points = points

    def grid_builder(self):
        r""" 
        create nodes at grid positions and link the nodes into a full grid
        """
        # rows and cols in the plotted points on the grid
        nrows, ncols, _ = self.grid_points.shape

        # place nodes on the grid
        for ix in range(nrows):
            for jx in range(ncols):
                # add node to node manager
                self._add_node(position=self.grid_points[ix][jx])

        # calls function to link all the created nodes together
        self._linkup(nrows)

    def _add_node(self, position:ndarray):
        r"""
        add individual nodes to node lookup
        """
        # creates node and assigns it a place in the node dictionary
        self.node_dict[self.next_node_ix] = Node(position=position, 
                                                 node_ix=self.next_node_ix)

        # increment the index by one
        self.next_node_ix = increment_index(self.next_node_ix)

    def _linkup(self, ncols:int):
        r"""
        """
        # lookup for visited nodes
        # keys: column indexes, values: next node index to link
        visited = dict()

        # column parity holds True if odd
        col_parity = True

        # loops through all points associated with the current grid
        for ix in range(len(self.node_dict)):

            node = self.node_dict[ix]

            # verify next index position is available in current column
            if ix + 1 in self.node_dict and (ix + 1) % ncols:

                next_node = self.node_dict[ix + 1]

                # set node's northern neighbour
                node.set_neighbor(port='n', node=next_node)

                # set next node's southern neighbour
                next_node.set_neighbor(port='s', node=node)

            # flip column parity at every column
            if not ix % ncols: col_parity = ~col_parity

            if col_parity:

                # if in the same col
                if ix % ncols in visited.keys():

                    # get the next node from lookup
                    next_node = visited[ix % ncols]

                    # set node's southwestern neighbour as the next node
                    node.set_neighbor(port='sw', node=next_node)

                    # set next node's northeastern neighbour
                    next_node.set_neighbor(port='ne', node=node)

                # has the (current column + 1) been visited
                if (ix % ncols) + 1 in visited.keys():
                    next_node = visited[(ix % ncols) + 1]

                    # set node's southeastern neighbour as the next node
                    node.set_neighbor(port='se', node=next_node)

                    # set next node's northwestern neighbour
                    next_node.set_neighbor(port='nw', node=node)
            else:   # even row
                if ix % ncols in visited.keys():

                    next_node = visited[ix % ncols]

                    # set node's southeastern neighbour as the next node
                    node.set_neighbor(port='se', node=next_node)

                    # set next node's northwestern neighbour
                    next_node.set_neighbor(port='nw', node=node)

                    # set next node to node directly south of current next node
                    next_node = next_node.get_neighbor(port='s')

                    if next_node:

                        # set node's southeastern neighbour as the next node
                        node.set_neighbor(port='se', node=next_node)

                        # set next node's northwestern neighbour
                        next_node.set_neighbor(port='nw', node=node)

            # update current column's last visited node
            visited[ix % ncols] = node

    def _get_node(self, node_ix:uint8) -> Node: 
        return self.node_dict[node_ix]

    def _get_node_list(self) -> dict: return self.node_dict

    def _get_num_nodes(self) -> int: return len(self.node_dict)

