import numpy as np

class Node (object):
	def __init__(self, x=None, y=None, left=None, right=None, index=None, bots=np.array([]),is_exit=False):
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

class NodeManager (object):
	def __init__(self):
		self.__head = Node()
		self.__tail = self.__head
		self.__array = np.array([], dtype=object)
		
	def add_node(self, x=0, y=0, is_exit=False):
		self.__tail.set_right(Node(x=x, y=y, left=self.__tail, index=self.__array.size, is_exit=is_exit))
		self.__tail = self.__tail.get_right()
		self.__array = np.insert(self.__array, self.__array.size, self.__tail)
		
