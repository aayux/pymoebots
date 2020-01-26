import numpy as np


class Node (object):
	def __init__(self, x=None, y=None, left=None, right=None, index=None, bots=np.array([], 'object'),is_exit=False):
		self.__x = x
		self.__y = y
		self.__left = left
		self.__right = right
		self.__index = index
		self.__bots = bots
		self.__is_exit = is_exit

	def set_right(self, node=None):
		self.__right = node

	def get_right(self):
		return self.__right
	
	def get_index(self):
		return self.__index
		
	def get_is_exit(self):
		return self.__is_exit
		
	def arrival(self, bot):
		self.__bots = np.append(self.__bots, bot)

	def departure(self, bot):
		self.__bots = np.delete(self.__bots, np.where(self.__bots==bot))
		
	def get_bots(self):
		return self.__bots

	def get_left(self):
		return self.__left

	def get_position(self):
		return self.__x, self.__y


class NodeManager (object):
	def __init__(self):
		self.__head = Node()
		self.__tail = self.__head
		self.__array = np.array([], dtype='object')
		
	def add_node(self, x=0, y=0, is_exit=False):
		self.__tail.set_right(Node(x=x, y=y, left=self.__tail, index=self.__array.size, is_exit=is_exit))
		self.__tail = self.__tail.get_right()
		self.__array = np.insert(self.__array, self.__array.size, self.__tail)

	def center(self):
		return self.__array[self.__array.size//2]

	def convert_path_to_nodes(self, path=None):
		converted_x = np.empty(path.shape)
		converted_y = np.empty(path.shape)
		for i in range(path.shape[0]):
			for j in range(path.shape[1]):
				converted_x[i][j] = self.__array[int(path[i][j])].get_position()[0]
				converted_y[i][j] = self.__array[int(path[i][j])].get_position()[1]
		return converted_x, converted_y
