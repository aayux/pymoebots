from dataclasses import dataclass, field

import node_skeleton as ns
import numpy as np


@dataclass
class NodeManager:
    node_list: dict = field(default=None)
    next_index: np.uint8 = field(default=np.uint8(0))
    plotted_points: np.ndarray = field(default=None)

    def add_node(self, position=None):
        """
        Adds individual nodes to node list
        """
        if not self.node_list:
            self.node_list = {}
        self.node_list[self.next_index] = ns.Node(position=position, node_id=self.next_index)
        if self.next_index < 255:
            self.next_index += np.uint8(1)
        elif self.next_index < 65534:
            self.next_index += np.uint16(1)
        elif self.next_index < 429496728:
            self.next_index += np.uint32(1)

    def get_node(self, node_id=None):
        """
        gets specific node from node list.
        """
        return self.node_list[node_id]

    def create_node_structure(self):
        for row in range(self.plotted_points.shape[0]):
            for point in range(self.plotted_points[row].shape[0]):
                self.add_node(position=self.plotted_points[row][point])
        self.link_nodes(row=self.plotted_points[0].shape[0])

    def link_nodes(self, row=None):
        index = len(self.node_list)
        prev_row = {}
        row_count = -1

        for i in range(index):
            node = self.node_list[i]
            if i + 1 in self.node_list and (i + 1) % row:
                new_node = self.node_list[i + 1]
                node.set_neighbor(port='right', node=new_node)
                new_node.set_neighbor(port='left', node=node)
            if not i % row:
                row_count += 1
            if row_count % 2:
                if i % row in prev_row:
                    new_node = prev_row[i % row]
                    node.set_neighbor(port='bottom left', node=new_node)
                    new_node.set_neighbor(port='top right', node=node)
                if (i % row) + 1 in prev_row:
                    new_node = prev_row[(i % row) + 1]
                    node.set_neighbor(port='bottom right', node=new_node)
                    new_node.set_neighbor(port='top left', node=node)
            else:
                if i % row in prev_row:
                    new_node = prev_row[i % row]
                    node.set_neighbor(port='bottom right', node=new_node)
                    new_node.set_neighbor(port='top left', node=node)
                    new_node = new_node.get_neighbor(port='left')
                    if new_node:
                        node.set_neighbor(port='bottom left', node=new_node)
                        new_node.set_neighbor(port='top right', node=node)
            prev_row[i % row] = node

    def get_number_nodes(self):
        """Returns total number of nodes in graph"""
        return len(self.node_list)

    def get_node_list(self):
        """Returns all nodes from node list"""
        return self.node_list


if __name__ == "__main__":
    pass
