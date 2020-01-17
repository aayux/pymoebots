import math
import numpy as np
import node_construction as nc

class LineArea (object):
	def __init__(self, exit_node=None, number_of_bots=None):
		self.__exit_node_value = exit_node
		self.__number_of_bots = number_of_bots
		self.__n = math.ceil(self.__exit_node_value * 1.25)
		self.__n = self.__n if self.__n%2 else self.__n + 1
		self.__x = np.linspace(-10, 10, num=self.__n*2+1, endpoint=True)
		self.__y = np.zeros(self.__x.shape)
		self.__nodes = nc.NodeManager()
	
	def create_nodes(self):
		x_node = np.arange(-self.__n, self.__n+1)
		for i in x_node:
			if i == self.__exit_node_value:
				self.__nodes.add_node(x=i, is_exit=True)
			self.__nodes.add_node(x=i)

