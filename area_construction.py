import math
import numpy as np
import node_construction as nc
import bot_construction as bc
import visuals_construction as vc


class LineArea (object):
	def __init__(self):
		self.__exit_node_value = None
		self.__number_of_bots = None
		self.__n = None
		self.__n = None
		self.__x = None
		self.__y = None
		self.__nodes = nc.NodeManager()
		self.__bots = bc.BotManager()
		self.__algorithm_selection = np.empty([3], dtype='int64')
		self.__byzantine = False
	
	def __create_nodes(self):
		x_node = np.arange(-self.__n, self.__n, dtype='int64')
		for i in x_node:
			if i == self.__exit_node_value:
				self.__nodes.add_node(x=i, is_exit=True)
			self.__nodes.add_node(x=i)

	def __nodes_center(self):
		return self.__nodes.center()

	def line_center(self):
		return self.__x[self.__x.size//2]
	
	def __create_bots_at_line_center(self):
		node = self.__nodes_center()
		self.__bots.add_bots(number_of_bots=self.__number_of_bots)
		self.__bots.configure_all_bots(node=node, algorithm=self.__algorithm_selection)
		
	def __configure(self, exit_node, number_of_bots, algorithm=None, byzantine=False):
		self.__exit_node_value = exit_node
		self.__number_of_bots = number_of_bots
		self.__byzantine = byzantine
		self.__n = math.ceil(self.__exit_node_value * 1.25)
		self.__n = self.__n if self.__n%2 else self.__n + 1
		self.__x = np.linspace(-10, 10, num=(self.__n*2)+1, endpoint=True)
		self.__y = np.zeros(self.__x.shape)
		if algorithm == None:
			self.__select_algorithm()
		else:
			self.__algorithm_selection = algorithm

	def run_simulation(self, exit_node, number_of_bots, algorithm=None, byzantine=False):
		self.__configure(exit_node, number_of_bots, algorithm=algorithm)
		self.__create_nodes()
		self.__create_bots_at_line_center()
		true_exit = False
		while not true_exit:
			true_exit = self.__bots.activate()
		true_paths = self.__nodes.convert_path_to_nodes(self.__bots.get_path())
		vc.create_environment(self.__x,true_paths[0],self.__y,true_paths[1])

	
	def __select_algorithm(self):
		self.__algorithm_selection[0] = 0
		if self.__number_of_bots < 3:
			self.__algorithm_selection[1] = self.__number_of_bots
			self.__algorithm_selection[2] = 1
		elif self.__number_of_bots > 2 and self.__byzantine:
			self.__algorithm_selection[1] = 3
			self.__algorithm_selection[2] = 1
		elif self.__number_of_bots > 2 and not self.__byzantine:
			self.__algorithm_selection[1] = 3
			self.__algorithm_selection[2] = 2
