
import itertools


class Node:
	"""
	This the class Node, each Node must have a value(data), and may have
	two pointers (positive_child, negative_child)
	"""
	def __init__(self, data, positive_child=None, negative_child=None):
		self.data = data
		self.positive_child = positive_child
		self.negative_child = negative_child


class Record:
	"""
	This is the class of records where each record has a list of symptoms and
	illness.
	"""
	def __init__(self, illness, symptoms):
		self.illness = illness
		self.symptoms = symptoms


def identical(yes_side, no_side):
	"""
	This function takes two sides of trees, and checks if all sub-trees for
	each are the same.
	:param yes_side: one subtree (in this exercise the right side)
	:param no_side: the other subtree (in this exercise the left side)
	:return: True if they were the same. False, otherwise.
	"""
	if yes_side is None and no_side is None:
		return True

	if yes_side is not None and no_side is not None:
		return ((yes_side.data == no_side.data) and identical(
			yes_side.positive_child, no_side.positive_child) and identical(
			yes_side.negative_child, no_side.negative_child))
	return False


def parse_data(filepath):
	"""
	This function opens a file and read it,and returns a list of records
	from type Record.
	:param filepath: The file name
	:return: a list of records from type Record.
	"""
	with open(filepath) as data_file:
		records = []
		for line in data_file:
			words = line.strip().split()
			records.append(Record(words[0], words[1:]))
		return records


class Diagnoser:
	"""
	This is the class of diagnoser, it has methods that work on tree,
	where illnesses are the leaves, and symptoms are all other nodes
	including the root.
	"""
	def __init__(self, root):
		self.root = root
		self.current = root

	def diagnose(self, symptoms):
		"""
		This method gets a list of symptoms and searches in the tree for
		the route the the symptoms lead to, and finally returns the illness
		that matches the symptoms.
		:param symptoms: a list of strings.
		:return: the illness that matches the symptoms.
		"""
		ans = self.helper_diagnose(symptoms)
		self.current = self.root
		return ans

	def helper_diagnose(self, symptoms):
		"""
		This is a helper method for the function diagnose. it does
		recursion in order to traverse in the tree.
		:param symptoms: a list of strings.
		:return: the illness that matches the symptoms.
		"""
		if self.current.negative_child is None and \
				self.current.positive_child is None:
			return self.current.data

		elif self.current.data in symptoms and self.current.positive_child:
			self.current = self.current.positive_child
			self.helper_diagnose(symptoms)

		elif self.current.data not in symptoms and self.current.negative_child:
			self.current = self.current.negative_child
			self.helper_diagnose(symptoms)

		return self.current.data

	def calculate_success_rate(self, records):
		"""
		This method calculate the success rate for each illness depending
		on the data from records.
		:param records: a list of objects from type / class Record.
		:return: the success rate
		"""
		correct = 0
		if len(records) == 0:
			raise ValueError("the list is empty")
		for one_record in records:
			record_symptom = one_record.symptoms
			record_illness = one_record.illness
			d_illness = self.diagnose(record_symptom)
			if d_illness == record_illness:
				correct += 1
		return correct / len(records)

	def all_illnesses(self):
		"""
		This method returns a list of all illness in the tree.(it removes
		None from illnesses) where each illness appears only one time,
		and the list is sorted descending according to the number it
		appears in the list.
		:return: a sorted list of illnesses(descending).
		"""
		lst = []
		dic = self.helper_illnesses(self.current, {})
		if None in dic.keys():
			dic.pop(None)
		if dic == {}:
			return lst
		for item in sorted(dic.items(), key=lambda x: x[1])[::-1]:
			lst.append(item[0])
		return lst

	def helper_illnesses(self, current, dic):
		"""
		This is a helper method for the method illness. it traverse in
		the tree, and get the illnesses and the how many times they were
		repeated.(including None)
		:param current: the current node
		:param dic: an empty dictionary (changes each time (recursion))
		:return: a dictionary of all illnesses and how many times they were
		repeated
		"""
		if current.positive_child is None and current.negative_child is None:
			if current.data in dic.keys() and current.data is not None:
				dic[current.data] += 1
			else:
				dic[current.data] = 1
		else:
			self.helper_illnesses(current.positive_child, dic)
			self.helper_illnesses(current.negative_child, dic)
		return dic
		
	def paths_to_illness(self, illness):
		"""
		This method returns all the possible paths to an illness.
		:param illness: the illness we are searching it in a tree.
		:return: a list of all possible paths. (list of lists)
		"""
		if illness not in self.all_illnesses() and illness is not None:
			return []
		return self.helper_path(illness, self.root, [], [])

	def helper_path(self, illness, current, lst, res):
		"""
		This is a helper method for paths to illness
		:param illness: the illness we are searching it in a tree.
		:param current: the current node.
		:param lst: the list of one path.
		:param res: a list of lists
		:return: a list of all possible paths. (list of lists)
		"""
		if current.positive_child is None and current.negative_child is None:
			if illness == current.data:
				res.append(lst)
				return res

		if current.positive_child and current.negative_child:
			self.helper_path(illness, current.positive_child, lst + [True], res)
			self.helper_path(illness, current.negative_child, lst + [False], res)
		return res

	def minimize_false(self):
		"""
		This method minimize the tree that there is no duplication in the
		subtrees
		:return: None
		"""
		current = self.root
		list_of_extras = self.helper_minimize(current, [])
		while self.root in list_of_extras:
			self.root = self.root.positive_child
		self.helper2_minimize(current, list_of_extras)

	def minimize(self, remove_empty=False):
		"""
		This method minimize the tree that there is no duplication in the
		subtrees also there are no (None) illness in the tree. and removing
		extra questions that does not affect the result(illness)
		:param remove_empty: default False,leads to only remove duplications
		if True, also removes None and extra questions.
		:return: None
		"""
		self.minimize_false()
		if remove_empty is True and self.root.data:
			if self.root.positive_child is None and self.root.negative_child:
				self.root = self.root.negative_child
			if self.root.negative_child is None and self.root.positive_child:
				self.root = self.root.positive_child
			if self.root.positive_child:
				while self.root.positive_child.data is None:
					self.root = self.root.negative_child
					if self.root.positive_child is None:
						break

			if self.root.negative_child is not None:
				while self.root.negative_child.data is None:
					self.root = self.root.positive_child
					if self.root.negative_child is None:
						break

			current = self.root
			self.helper3_minimize(current)
			self.minimize_false()
			while None in self.helper_illnesses(self.root, {}).keys():
				self.minimize(True)

	def helper3_minimize(self, current):
		"""
		This is a helper method for minimize, it removes the None from the
		tree and removes extra questions.
		:param current: the Node where we exist. starting from root.
		:return: None if we reached the end of the tree.
		"""
		if current.positive_child is None and current.negative_child is None:
			return
		if current.positive_child.positive_child:
			if current.positive_child.positive_child.data is None:
				current.positive_child = current.positive_child.negative_child

		if current.positive_child.negative_child:
			if current.positive_child.negative_child.data is None:
				current.positive_child = current.positive_child.positive_child

		if current.negative_child.positive_child:
			if current.negative_child.positive_child.data is None:
				current.negative_child = current.negative_child.negative_child

		if current.negative_child.negative_child:
			if current.negative_child.negative_child.data is None:
				current.negative_child = current.negative_child.positive_child

		self.helper3_minimize(current.positive_child)
		self.helper3_minimize(current.negative_child)

	def helper2_minimize(self, current, list_of_extras):
		"""
		This method receives a list of all extra subtrees (questions) and
		removes duplication from the tree.
		:param current: the Node where we exist. starting from root.
		:param list_of_extras: a list of all questions(Nodes) that are duplicated
		:return: None if we reached the end of the tree.
		"""
		while current.positive_child in list_of_extras:
			current.positive_child = current.positive_child.positive_child

		while current.negative_child in list_of_extras:
			current.negative_child = current.negative_child.positive_child

		if current.positive_child is None and current.negative_child is None:
			return
		self.helper2_minimize(current.positive_child, list_of_extras)
		self.helper2_minimize(current.negative_child, list_of_extras)

	def helper_minimize(self, current, res):
		"""
		This method returns a list of all questions that are duplicated,
		and we can remove one of the subtrees.
		:param current: the Node where we exist. starting from root.
		:param res: an empty list.
		:return: a list of all questions(Nodes) that are duplicated
		"""
		if identical(current.positive_child, current.negative_child)\
				and current.positive_child and current.negative_child:
			res.append(current)

		if current.positive_child and current.negative_child:
			self.helper_minimize(current.positive_child, res)
			self.helper_minimize(current.negative_child, res)
		return res


def build_tree(records, symptoms):
	"""
	This function builds a tree that the leaves are the illnesses and all
	other nodes are questions(symptoms)
	:param records: a list of objects from type / class Record.
	:param symptoms: a list of strings.
	:return: an object from class diagnoser
	"""
	if symptoms == [] and records == []:
		return Diagnoser(Node(None))
	if symptoms == []:
		dic = {}
		for record in records:
			if record.illness in dic:
				dic[record.illness] += 1
			else:
				dic[record.illness] = 1
		illness = dic_to_one_lst(dic)
		diagnoser = Diagnoser(Node(illness))
		return diagnoser
	root = helper_build_tree(symptoms, 0)
	diagnoser = Diagnoser(root)
	for record in records:
		if type(record) is not Record:
			raise TypeError("record type must Record")
		current = root
		for my_symp in symptoms:
			if type(my_symp) is not str:
				raise TypeError("symptom type must be string")
			if my_symp in record.symptoms:
				current = current.positive_child
				if type(current.data) is dict:
					if record.illness not in current.data.keys():
						current.data[record.illness] = 1
					else: current.data[record.illness] += 1
			else:
				current = current.negative_child
				if type(current.data) is dict:
					if record.illness not in current.data.keys():
						current.data[record.illness] = 1
					else: current.data[record.illness] += 1
	helper_2_build_tree(root)
	return diagnoser


def dic_to_one_lst(dic):
	"""
	This function receives a dictionary and returns a list ordered descending
	according to the number of illness in the dictionary.
	:param dic: a dictionary where illnesses are keys, and the number they
	appear are the values.
	:return: empty list if the dictionry was empty or include only None.
	otherwise,the name of the illness that appears the most.
	"""
	lst = []
	if None in dic.keys():
		dic.pop(None)
	if dic == {}:
		return lst
	for item in sorted(dic.items(), key=lambda x: x[1]):
		lst = item[0]
	return lst


def helper_2_build_tree(current):
	"""
	This function traverse in the tree, until it reaches the leaves, it puts
	the illness that has the highest success rate in the data of the leaf.
	if there was no illness it makes the data of the leaf = None
	:param current: the Node where we exist. starting from root.
	:return: the data of the current for recursion.
	"""
	if type(current.data) is dict:
		current.data = dic_to_one_lst(current.data)
		if current.data == []:
			current.data = None
		return current.data
	else:
		helper_2_build_tree(current.positive_child)
		helper_2_build_tree(current.negative_child)


def helper_build_tree(symptoms, index):
	"""
	This is a helper function for the function build tree, it builds a node
	for each symptoms and the pointers between nodes.
	:param symptoms: a list of strings.
	:param index: the index of symptoms
	:return: the root that needs to to be used in recursion.
	"""
	if index == len(symptoms) - 1:
		root = Node(symptoms[index], Node({}), Node({}))
		return root
	root = Node(symptoms[index], helper_build_tree(symptoms, index+1),
			 helper_build_tree(symptoms, index+1))
	return root


def optimal_tree(records, symptoms, depth):
	"""
	This function returns an object from type diagnoser that have the
	highest success rate according to a number (= depth) of symptoms.
	:param records:  a list of objects from type / class Record.
	:param symptoms: a list of strings.
	:param depth: number between 0 and length the symptoms.
	:return: an object from type diagnoser that have the highest success rate.
	"""
	if depth < 0 or depth > len(symptoms) or depth != int(depth):
		raise ValueError("cannot be the depth!")
	if len(symptoms) != len(set(symptoms)):
		raise ValueError("symptom is repeated more than one time!")
	for record in records:
		if type(record) is not Record:
			raise TypeError("record type must Record")
	for symptom in symptoms:
		if type(symptom) is not str:
			raise TypeError("symptom type must string")

	symptoms_list = list(itertools.combinations(symptoms, depth))
	my_dic = {}
	for group_symptoms in symptoms_list:
		symptoms = list(group_symptoms)
		diagnoser = build_tree(records, symptoms)
		ans = diagnoser.calculate_success_rate(records)
		my_dic[diagnoser] = ans
	return dic_to_one_lst(my_dic)
