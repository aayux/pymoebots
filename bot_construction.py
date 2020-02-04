import numpy as np
import node_construction as nc


class Bot (object):
	def __init__(self):
		self.__current_node = nc.Node()
		self.__path = np.array([], dtype='int64')
		self.__bot_id = None
		self.__exit_found = 0
		self.__exit_found_by = np.empty([], 'int64')
		self.__steps_exit_found = 0
		self.__exit_loc = 0
		self.__true_exit = 0
		self.__steps = 0
		self.__distance_covered = np.zeros(2)
		self.__instructions = True
		self.__count = 0
		self.__next_count_limit = 1
		self.__algorithm_selection = np.empty([3], dtype='int64')
		self.__speed = 2
		self.__wireless = False
		self.__number_of_bots = 0
		self.__bots_found = False
		self.__move_together = 0

		self.__bots_in_area = None
		self.__algorithm = None
		self.__step_at_exit_found=None
		self.__sync_module = None
		self.__wireless_configured = False
		self.__searcher = False
		self.__claim = None
		self.__bot_in_environment = None
		self.__open_claim = None
		self.__sync = False
		self.__all_sync = False

	def configure(self, node, bot_id, algorithm, wireless=False):
		self.__current_node = node
		self.__current_node.arrival(bot=self)
		self.__bot_id = bot_id
		self.__algorithm_selection[:] = algorithm
		self.__distance_covered[:] = self.__current_node.get_index()
		self.__path = np.insert(self.__path, self.__path.size, self.__current_node.get_index())
		self.__wireless = wireless

	def engine(self):
		self.__algorithm_runner()
		return np.array([self.__true_exit])

		# if np.all(self.__algorithm_selection[:] == [0,1,1]):
		# 	self.algorithm_one_bot()
		# return np.array([self.__true_exit])

	def __is_exit(self):
		self.__exit_found = self.__current_node.get_is_exit()
		return self.__exit_found

	def __move_right(self):
		if self.__current_node.get_right():
			self.__current_node.departure(bot=self)
			self.__current_node = self.__current_node.get_right()
			self.__current_node.arrival(bot=self)
			self.__path = np.append(self.__path, self.__current_node.get_index())
			if self.__current_node.get_index() > self.__distance_covered[1]:
				self.__distance_covered[1] = self.__current_node.get_index()
		else:
			self.__wait()

	def __move_left(self):
		if self.__current_node.get_left().get_position()[0] != None:
			self.__current_node.departure(bot=self)
			self.__current_node = self.__current_node.get_left()
			self.__current_node.arrival(bot=self)
			self.__path = np.append(self.__path, self.__current_node.get_index())
			if self.__current_node.get_index() < self.__distance_covered[0]:
				self.__distance_covered[0] = self.__current_node.get_index()
		else:
			self.__wait()

	def __wait(self):
		self.__path = np.append(self.__path, self.__current_node.get_index())

	def __algorithm_runner(self):
		if not self.__steps:
			self.__initial_scan()
			self.__initial_update()
			if self.__bot_id == 0 and self.__wireless:
				self.__set_up_wireless()
		else:
			self.__scan()
			self.__query()
			if self.__algorithm == 0:
				self.__algorithm_0()
			elif self.__algorithm == 1:
				self.__algorithm_1()
			elif self.__algorithm == 2:
				self.__algorithm_2w()
			elif self.__algorithm == 2.1:
				self.__algorithm_2()
			elif self.__algorithm == 3:
				self.__algorithm_3w()
			self.__scan()
			self.__query()
			self.__update_bot()

	def __initial_update(self):
		self.__steps += 1
		if self.__number_of_bots == 1:
			self.__algorithm = 1
		elif self.__number_of_bots == 2 and self.__wireless:
			self.__algorithm = 2
		elif self.__number_of_bots == 2 and not self.__wireless:
			self.__algorithm = 2.1
		elif self.__number_of_bots > 2 and self.__wireless:
			self.__algorithm = 3

	def __update_bot(self):
		self.__steps += 1
		if self.__number_of_bots == 1:
			self.__count_instructions()

	def __count_instructions(self):
		self.__count += 1
		if self.__count == self.__next_count_limit:
			self.__next_count_limit += 2
			self.__count = 0
			self.__instructions = not self.__instructions

	def __set_up_wireless(self):
		self.__sync_module = SyncModule()
		self.__sync_module.set_bots(self.__bots_in_area)
		self.__wireless_configured = True
		for bot in self.__bots_in_area:
			bot.set_sync_module(self.__sync_module)

	def __initial_scan(self):
		self.__bots_in_area = self.__current_node.get_bots()
		self.__number_of_bots = self.__bots_in_area.size
		if not self.__wireless_configured:
			self.__bot_in_environment = self.__bots_in_area

	def __scan(self):
		"""
		scans local area for bot and exit point
		:return:
		"""
		self.__bots_in_area = self.__current_node.get_bots()
		self.__exit_found = self.__current_node.get_is_exit()
		if self.__exit_found:
			self.__exit_loc = self.__current_node
			self.__step_at_exit_found = self.__steps
			if self.__wireless_configured:
				self.__sync_module.set_claim(self.claim_info())
			else:
				self.__claim = self.claim_info()
			self.__algorithm = 0

	def __query(self):
		if self.__wireless_configured:
			if self.__sync_module.get_claim_status():
				self.__algorithm = 0

	def set_sync_module(self, value):
		self.__sync_module = value
		self.__wireless_configured = True

	def __algorithm_0(self):
		"""
		exit algorithm
		:return:
		"""
		if self.__number_of_bots == 1:
			self.__true_exit = self.__exit_found
		elif self.__number_of_bots == 2:
			if self.__wireless_configured:
				if self.__current_node == self.__sync_module.get_claim():
					if self.__bots_in_area.size == self.__sync_module.get_bots().size:
						self.__true_exit = self.__exit_found
					else:
						self.__wait()
				elif self.__current_node.get_position()[0] < self.__sync_module.get_claim().get_position()[0]:
					self.__move_right()
				else:
					self.__move_left()
			elif not self.__wireless_configured:
				if self.__all_sync:
					if self.__current_node != self.__claim[0]:
						if self.__current_node.get_position()[0] < self.__claim[0].get_position()[0]:
							self.__move_right()
						elif self.__current_node.get_position()[0] > self.__claim[0].get_position()[0]:
							self.__move_left()
					else:
						if self.__bots_in_area.size == self.__bot_in_environment.size:
							max_path = 0
							for bot in self.__bot_in_environment:
								if max_path < bot.get_path().size:
									max_path = bot.get_path().size
							if max_path == self.__path.size:
								self.__true_exit = self.__exit_found
							else:
								self.__wait()
						else:
							self.__wait()
				elif self.__current_node == self.__claim[0] and not self.__searcher:
					self.__searcher = True
				elif self.__searcher and (self.__bots_in_area.size != self.__bot_in_environment.size):
					if self.__bot_id%2:
						self.__move_right()
					else:
						self.__move_left()
				elif self.__searcher and self.__bots_in_area.size == self.__bot_in_environment.size and not self.__open_claim:
					self.__searcher = False
					for bot in self.__bots_in_area:
						if bot.get_bot_id() != self.__bot_id:
							bot.set_claim(self.__claim)
							bot.set_open_claim(True)
							bot.set_algorithm(0)
					self.__open_claim = True
					self.__sync = True
					self.__wait()
				elif self.__open_claim and not self.__all_sync:
					count = 0
					for bot in self.__bots_in_area:
						if bot.get_bot_id() != self.__bot_id:
							if bot.get_sync_status():
								count += 1
					if count == self.__bots_in_area.size-1:
						self.__all_sync = True
					self.__sync = True
					self.__wait()
		elif self.__number_of_bots > 2:
			if self.__wireless_configured:
				if self.__current_node == self.__sync_module.get_claim():
					if self.__bots_in_area.size == self.__sync_module.get_bots().size:
						max_path = 0
						for bot in self.__sync_module.get_bots():
							if max_path < bot.get_path().size:
								max_path = bot.get_path().size
						if max_path == self.__path.size:
							self.__true_exit = self.__exit_found
						else:
							self.__wait()
					else:
						self.__wait()
				elif self.__current_node.get_position()[0] < self.__sync_module.get_claim().get_position()[0]:
					self.__move_right()
				else:
					self.__move_left()








	def __algorithm_1(self):
		if self.__instructions:
			self.__move_left()
		else:
			self.__move_right()

	def __algorithm_2(self):
		if self.__steps%self.__speed == 0:
			if self.__bot_id%2:
				self.__move_left()
			else:
				self.__move_right()
		else:
			self.__wait()

	def __algorithm_2w(self):
		if self.__bot_id%2:
			self.__move_left()
		else:
			self.__move_right()

	def __algorithm_3w(self):
		if self.__bot_id%2:
			self.__move_left()
		else:
			self.__move_right()

	def __algorithm_3wb(self):
		pass

	def __algorithm_3(self):
		pass

	def __algorithm_3b(self):
		pass

	def get_exit_found(self):
		return self.__exit_found

	def get_bot_id(self):
		return self.__bot_id

	def claim_info(self):
		return self.__exit_loc, self.__step_at_exit_found

	def toggle_wireless(self):
		self.__wireless = not self.__wireless

	def algorithm_one_bot(self):
		if self.__current_node.get_is_exit():
			self.__exit_found = 1
		elif not self.__steps:
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

	# def algorithm_two_bot_nw(self):
	# 	if self.__current_node.get_is_exit():
	# 		self.__exit_found = 1
	# 		self.__exit_found_by = self.__bot_id
	# 		self.__exit_loc = self.__current_node.get_position()
	# 		self.__claim = 1
	# 	elif not self.__steps:
	# 		if self.__number_of_bots:
	# 			self.__steps += 1
	# 		elif not self.__number_of_bots:
	# 			bots = self.__current_node.get_bots()
	# 			for bot in bots:
	# 				bot.set_number_of_bots(bots.size)
	# 			self.__steps += 1
	# 	elif self.__instructions and not self.__exit_found:
	# 		self.__steps += 1
	# 		if self.__steps % self.__speed == 0:
	# 			if self.__bot_id%2:
	# 				self.__move_right()
	# 			else:
	# 				self.__move_left()
	# 	if self.__instructions and self.__exit_found and not self.__bots_found:
	# 		bots = self.__current_node.get_bots()
	# 		if bots.size == self.__number_of_bots:
	# 			self.__steps += 1
	# 			for bot in bots:
	# 				bot.set_instruction(False)
	# 				bot.set_bots_found(True)
	# 		else:
	# 			self.__steps += 1
	# 			if self.__bot_id%2:
	# 				self.__move_left()
	# 			else:
	# 				self.__move_right()
	# 	elif not self.__instructions:
	# 		bots = self.__current_node.get_bots()
	# 		if current
	# 	elif self.__exit_found and self.__bots_found and self.__exit_found_by == self.__bot_id:
	# 		bots = self.__current_node.get_bots()
	# 		if bots.size == self.__number_of_bots and 1:
	# 			if self.__bot_id%2:
	# 				self.__move_left()
	# 				self.__update_algorithm_two_bot_nw()
	# 			else:
	# 				self.__move_right()
	# 				self.__update_algorithm_two_bot_nw()
	# 	else:
	# 		pass

		# elif not self.__instructions and not self.__exit_found:
		# 	pass
		# if self.__exit_found:
		# 	pass


		pass

	def algorithm_two_bot_w(self):
		pass
		
	def __update_algorithm_one_bot(self):
		self.__count += 1
		if self.__count == self.__next_count_limit:
			self.__instructions = not self.__instructions
			self.__count = 0
			self.__next_count_limit += 2
		self.__steps += 1

	def __update_algorithm_two_bot_nw(self):
		self.__steps += 1
		pass

	def __is_true_exit(self):
		if self.__true_exit:
			return True
		bots = self.__current_node.get_bots()
		votes = np.array([], dtype='int64')
		number_to_verify = self.__number_of_bots//2 + 1
		if bots.size >= number_to_verify:
			for bot in bots:
				votes = np.append(votes, bot.is_exit())
		result = np.count_nonzero(votes)
		if result >= number_to_verify:
			for bot in bots:
				bot.set_true_exit(True)
	
	def set_number_of_bots(self, number_of_bots):
		self.__number_of_bots = number_of_bots
	
	def set_true_exit(self, value):
		self.__true_exit = value

	def get_path(self):
		return self.__path

	def set_bots_found(self, value):
		self.__bots_found = value

	def set_instruction(self, value):
		self.__instructions = value

	def set_speed(self, value):
		self.__speed = value

	def set_claim(self, value):
		self.__claim = value

	def set_open_claim(self, value):
		self.__open_claim = value

	def get_sync_status(self):
		return self.__sync

	def set_algorithm(self, value):
		self.__algorithm = 0


class ExitFindModule (object):
	"""
	All calls for check in this module need to have the bot on the same node as bot being checked.
	"""
	def __init__(self):
		self.__exit_found = None
		self.__open_claim = None
		self.__.claims = np.array([], dtype='object')

class SyncModule (object):
	def __init__(self):
		self.__bots_in_environment = None
		self.__open_claim = False
		self.__sync = 0
		self.__claims = np.array([], dtype='object')

	def get_bots(self):
		return self.__bots_in_environment

	def get_claim_status(self):
		return self.__open_claim

	def get_claim(self):
		return self.__claims[0]

	def set_bots(self, value):
		self.__bots_in_environment = value

	def set_claim(self, value):
		if value not in self.__claims:
			self.__claims = np.append(self.__claims, value)
		if self.__sync == 2:
			self.__open_claim = True
		self.__sync += 1


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
			
	def configure_all_bots(self, node=None, algorithm=None, wireless=False):
		for i in range(self.__bots.size):
			if self.__next_to_configure == self.__bots.size:
				break
			self.__bots[self.__next_to_configure].configure(node=node, bot_id=self.__next_to_configure, algorithm=algorithm, wireless=wireless)
			self.__next_to_configure += 1
			
	def activate(self):
		two_step_exit = np.empty([self.__bots.size, 1])
		for i in range(self.__bots.size):
			two_step_exit[i] = self.__bots[i].engine()
		valid_vote = self.__bots.size//2+1
		if np.count_nonzero(two_step_exit) >= valid_vote:
			return True
		return False

	def get_path(self):
		paths = np.empty([self.__bots.size, self.__bots[0].get_path().size])
		for i in range(self.__bots.size):
			if i == 0:
				paths[i] = self.__bots[i].get_path()
			else:
				a = self.__bots[i].get_path()
				paths[i] = self.__bots[i].get_path()
		return paths

	def toggle_wireless(self):
		for bot in self.__bots:
			bot.toggle_wireless()
	
