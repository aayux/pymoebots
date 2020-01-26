import numpy as np
import node_construction as nc


class Bot (object):
	def __init__(self):
		self.__current_node = nc.Node()
		self.__path = np.array([], dtype='int64')
		self.__bot_id = None
		self.__exit_found = 0
		self.__steps_exit_found = 0
		self.__exit_loc = 0
		self.__true_exit = 0
		self.__steps = 0
		self.__distance_covered = np.zeros(2)
		self.__instructions = True
		self.__count = 0
		self.__next_count_limit = 1
		self.__algorithm_selection = np.empty([3], dtype='int64')
		self.__speed = 1
		self.__wireless = 0
		self.__number_of_bots = 0

	def configure(self, node, bot_id, algorithm):
		self.__current_node = node
		self.__current_node.arrival(bot=self)
		self.__bot_id = bot_id
		self.__algorithm_selection[:] = algorithm
		self.__distance_covered[:] = self.__current_node.get_index()
		self.__path = np.insert(self.__path, self.__path.size, self.__current_node.get_index())

	def engine(self):
		if np.all(self.__algorithm_selection[:] == [0,1,1]):
			self.algorithm_one_bot()
		return np.array([self.__true_exit])

	def is_exit(self):
		self.__exit_found = self.__current_node.get_is_exit()
		return self.__exit_found

	def __move_right(self):
		self.__current_node.departure(bot=self)
		self.__current_node = self.__current_node.get_right()
		self.__current_node.arrival(bot=self)
		self.__path = np.append(self.__path, self.__current_node.get_index())
		if self.__current_node.get_index() > self.__distance_covered[1]:
			self.__distance_covered[1] = self.__current_node.get_index()

	def __move_left(self):
		self.__current_node.departure(bot=self)
		self.__current_node = self.__current_node.get_left()
		self.__current_node.arrival(bot=self)
		self.__path = np.append(self.__path, self.__current_node.get_index())
		if self.__current_node.get_index() < self.__distance_covered[0]:
			self.__distance_covered[0] = self.__current_node.get_index()

	def algorithm_one_bot(self):
		if self.__current_node.get_is_exit():
			self.__exit_found = 1
		elif not self.__steps:
			if self.__number_of_bots:
				self.__steps += 1
			elif not self.__number_of_bots:
				bots = self.__current_node.get_bots()
				self.__number_of_bots=bots.size
				self.__steps += 1
		elif self.__instructions and not self.__exit_found:
			self.__move_left()
			self.__update_algorithm_one_bot()
		elif not self.__instructions and not self.__exit_found:
			self.__move_right()
			self.__update_algorithm_one_bot()
		if self.__exit_found:
			self.__is_true_exit()
		
	def __update_algorithm_one_bot(self):
		self.__count += 1
		if self.__count == self.__next_count_limit:
			self.__instructions = not self.__instructions
			self.__count = 0
			self.__next_count_limit += 2
		self.__steps += 1
		
	def __is_true_exit(self):
		if self.__true_exit:
			return True
		bots = self.__current_node.get_bots()
		votes = np.array([], dtype='int64')
		number_to_verify = self.__number_of_bots//2 + 1
		if bots.size >= number_to_verify:
			for bot in bots:
				votes = np.append(votes, bot.is_exit())
		test = np.count_nonzero(votes)
		if test >= number_to_verify:
			for bot in bots:
				bot.set_true_exit(True)
	
	def set_number_of_bots(self, number_of_bots):
		self.__number_of_bots = number_of_bots
	
	def set_true_exit(self, value):
		self.__true_exit = value

	def get_path(self):
		return self.__path


class BotManager (object):
	def __init__(self):
		self.__bots = np.array([], dtype='object')
		self.__next_to_configure = 0
		self.__exit_found = False
		self.__wireless = False
		self.__true_exit = False
	
	def add_bots(self, number_of_bots = 1):
		for i in range(number_of_bots):
			self.__bots = np.insert(self.__bots, self.__bots.size, Bot())
			
	def configure_all_bots(self, node, algorithm):
		for i in range(self.__bots.size):
			if self.__next_to_configure == self.__bots.size:
				break
			self.__bots[self.__next_to_configure].configure(node=node, bot_id=self.__next_to_configure, algorithm=algorithm)
			self.__next_to_configure += 1
			
	def activate(self):
		two_step_exit = np.empty([self.__bots.size, 1])
		for i in range(self.__bots.size):
			two_step_exit[i] = self.__bots[i].engine()
		valid_vote = (self.__bots.size//2)+1
		if np.count_nonzero(two_step_exit) >= valid_vote:
			return True
		return False

	def get_path(self):
		for i in range(self.__bots.size):
			if i == 0:
				paths = np.empty([self.__bots.size, self.__bots[i].get_path().size])
				paths[i] = self.__bots[i].get_path()
			else:
				paths[i] = self.__bots[i].get_path()
		return paths
	
