from copy import deepcopy

puzzle = [[1,2,3],[4,0,5],[7,8,6]]
goal_state = [[1,2,3],[4,5,6],[7,8,0]]

class Node:
	def __init__(self, value):
		self.parent = None
		self.value = value

# This contains my puzzle helper functions
class Puzzles:

	def print_puzzle(self,puzzle):
		for i in puzzle:
			print (i)
		print("\n")

	# Outputs a nested list of valid puzzles
	def valid_moves(self,puzzle, repeated_state):
		moves = []
		valid_puzzles = []
		#print("valid moves:", puzzle)

		# Returns blank's location as a tuple
		# Consulted Stack Overflow for list comprehension trick: 
		# https://stackoverflow.com/questions/43838601/how-can-i-get-the-index-of-a-nested-list-item
		blank_loc = [(i, j.index(0)) for i, j in enumerate(puzzle) if 0 in j]
		#print("blank loc:",blank_loc)
		blank_row, blank_col = blank_loc[0][0], blank_loc[0][1]
		
		#print("repeated_state",repeated_state)

		# Finds all valid moves
		# Must use deep copy because each puzzle is a unique copy
		# LEFT
		if blank_col - 1 >= 0:
			temp_puzzle = deepcopy(puzzle)
			temp_puzzle[blank_row][blank_col - 1] = 0
			temp_puzzle[blank_row][blank_col] = puzzle[blank_row][blank_col-1]
			if temp_puzzle not in repeated_state:
				valid_puzzles.append(temp_puzzle)
		# UP
		if blank_row - 1 >= 0:
			temp_puzzle = deepcopy(puzzle)
			temp_puzzle[blank_row - 1][blank_col] = 0
			temp_puzzle[blank_row][blank_col] = puzzle[blank_row-1][blank_col]
			if temp_puzzle not in repeated_state:
				valid_puzzles.append(temp_puzzle)
		# RIGHT
		if blank_col + 1 <= len(puzzle)-1:
			temp_puzzle = deepcopy(puzzle)
			temp_puzzle[blank_row][blank_col + 1] = 0
			temp_puzzle[blank_row][blank_col] = puzzle[blank_row][blank_col+1]
			if temp_puzzle not in repeated_state:
				valid_puzzles.append(temp_puzzle)
		# DOWN
		if blank_row + 1 <= len(puzzle)-1:
			temp_puzzle = deepcopy(puzzle)
			temp_puzzle[blank_row + 1][blank_col] = 0
			temp_puzzle[blank_row][blank_col] = puzzle[blank_row+1][blank_col]
			if temp_puzzle not in repeated_state:
				valid_puzzles.append(temp_puzzle)

		return valid_puzzles


# This contains my searching algorithms
class SearchAlgorithm: 
	def uniform_cost_search(self,puzzle):
		global num_nodes, max_queue, depth
		repeated_state = []
		print("Start: ", puzzle)
		obj = Puzzles()
		queue = self.make_queue(puzzle)
		#print("Expanding state")
		#obj.print_puzzle(puzzle)
		while (len(queue) > 0):

			node = queue.pop(0).value
			#print("Current HEAD")
			
			repeated_state.append(node)

			#obj.print_puzzle(node)
			if node == goal_state:
				print("Goal!")
				print("Expanded Nodes: ", num_nodes)
				print("Max Queue: ", max_queue)
				print("depth: ", depth)
				return True
			print("Expanding state")
			obj.print_puzzle(node)	
			queue = self.queueing_function(queue, node, puzzle,repeated_state)

		return False
		#print("queue", queue, queue[0].value)

	def queueing_function(self, queue, node, puzzle, repeated_state):
		global num_nodes, max_queue, depth
		obj = Puzzles()
		#print("Entering Queueing function")
		next_moves = obj.valid_moves(node, repeated_state)

		#print("Next Legal Moves Moves")
		#obj.print_puzzle(next_moves)
		
		
		for item in next_moves:
			node = Node(item)
			queue.append(node)
			num_nodes += 1
			if len(queue) > max_queue:
				max_queue = len(queue)
		#print("Queue items")
		#for p in queue: 
			#print ( p.value)
		#print("___________________")
		return queue

	def make_queue(self,puzzle):
		global num_nodes, max_queue
		queue = []
		node = Node(puzzle)
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