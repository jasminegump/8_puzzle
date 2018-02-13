from copy import deepcopy

puzzle = [[1,2,3],[4,0,5],[7,8,6]]
goal_state = [[1,2,3],[4,5,6],[7,8,0]]

class Node:
	def __init__(self, value, level):
		self.parent = None
		self.value = value
		self.level = level
# This contains my puzzle helper functions
class Puzzles:

	def print_puzzle(self,puzzle):
		for i in puzzle:
			print (i)
		print("\n")

	def valid_append(self, valid_puzzles, puzzle, repeated_state, row_1, col_1, row_2, col_2):
		temp_puzzle = deepcopy(puzzle)
		temp_puzzle[row_1][col_1] = 0
		temp_puzzle[row_2][col_2] = puzzle[row_1][col_1]
		if temp_puzzle not in repeated_state:
			valid_puzzles.append(temp_puzzle)
		return valid_puzzles

	# Outputs a nested list of valid puzzles
	def valid_moves(self,puzzle, repeated_state):
		moves = []
		valid_puzzles = []

		# Returns blank's location as a tuple
		# Consulted Stack Overflow for list comprehension trick: 
		# https://stackoverflow.com/questions/43838601/how-can-i-get-the-index-of-a-nested-list-item
		blank_loc = [(i, j.index(0)) for i, j in enumerate(puzzle) if 0 in j]
		blank_row, blank_col = blank_loc[0][0], blank_loc[0][1]
		
		# Finds all valid moves
		# Must use deep copy because each puzzle is a unique copy
		# LEFT
		if blank_col - 1 >= 0:
			valid_puzzles = self.valid_append(valid_puzzles, puzzle, repeated_state, blank_row, blank_col - 1, blank_row, blank_col)

		# UP
		if blank_row - 1 >= 0:
			valid_puzzles = self.valid_append(valid_puzzles, puzzle, repeated_state, blank_row - 1, blank_col, blank_row, blank_col)

		# RIGHT
		if blank_col + 1 <= len(puzzle)-1:
			valid_puzzles = self.valid_append(valid_puzzles, puzzle, repeated_state, blank_row, blank_col + 1, blank_row, blank_col)

		# DOWN
		if blank_row + 1 <= len(puzzle)-1:
			valid_puzzles = self.valid_append(valid_puzzles, puzzle, repeated_state, blank_row + 1, blank_col, blank_row, blank_col)

		return valid_puzzles


# This contains my searching algorithms
class SearchAlgorithm: 
	def uniform_cost_search(self,puzzle):
		level = 0
		global num_nodes, max_queue, depth
		repeated_state = []
		print("Start: ", puzzle)
		obj = Puzzles()
		queue = self.make_queue(puzzle)

		while (len(queue) > 0):
			#print("num_nodes",num_nodes)
			n = queue.pop(0)
			node = n.value
			
			repeated_state.append(node)

			if node == goal_state:
				print("Goal!")
				print("Expanded Nodes: ", num_nodes - 1)
				print("Max Queue: ", max_queue)
				print("depth: ", n.level)

				return True
			print("Expanding state")
			obj.print_puzzle(node)
			queue = self.queueing_function(queue, node, n, puzzle,repeated_state)

		return False
		#print("queue", queue, queue[0].value)

	def queueing_function(self, queue, node, n, puzzle, repeated_state):
		global num_nodes, max_queue, depth
		obj = Puzzles()
		next_moves = obj.valid_moves(node, repeated_state)
		
		for item in next_moves:
			node = Node(item, n.level + 1)
			queue.append(node)
			num_nodes += 1
			if len(queue) > max_queue:
				max_queue = len(queue)
		'''
		print("max", max_queue)

		for p in queue: 
			print ( p.value)
		print("___________________")
		'''
		return queue

	def make_queue(self,puzzle):
		global num_nodes, max_queue
		queue = []
		node = Node(puzzle, 0) # level 0
		queue.append(node)
		num_nodes += 1
		if len(queue) > max_queue:
			max_queue = len(queue)
		return queue

def main(puzzle):
	global num_nodes, max_queue, depth
	num_nodes,max_queue, depth = 0,0,0
	obj = SearchAlgorithm()
	obj.uniform_cost_search(puzzle)
	return

main(puzzle)