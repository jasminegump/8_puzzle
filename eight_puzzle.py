from copy import deepcopy

puzzle = [[1,2,3],[4,8,0],[7,6,5]]
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
		up, down, right, left = 1,-1,1,-1
		moves = []
		valid_puzzles = []
		#print("valid moves:", puzzle)

		# Returns blank's location as a tuple
		# Consulted Stack Overflow for list comprehension trick: 
		# https://stackoverflow.com/questions/43838601/how-can-i-get-the-index-of-a-nested-list-item
		blank_loc = [(i, j.index(0)) for i, j in enumerate(puzzle) if 0 in j]
		#print("blank loc:",blank_loc)
		blank_row, blank_col = blank_loc[0][0], blank_loc[0][1]
		
		print("repeated_state",repeated_state)

		# Finds all valid moves
		# Must use deep copy because each puzzle is a unique copy
		if blank_col - 1 >= 0:
			moves.append('left')
			temp_puzzle = deepcopy(puzzle)
			temp_puzzle[blank_row][blank_col - 1] = 0
			temp_puzzle[blank_row][blank_col] = puzzle[blank_row][blank_col-1]
			if temp_puzzle not in repeated_state:
				valid_puzzles.append(temp_puzzle)
		if blank_row - 1 >= 0:

			temp_puzzle = deepcopy(puzzle)
			temp_puzzle[blank_row - 1][blank_col] = 0
			temp_puzzle[blank_row][blank_col] = puzzle[blank_row-1][blank_col]
			if temp_puzzle not in repeated_state:
				valid_puzzles.append(temp_puzzle)
			moves.append('up')
		if blank_col + 1 <= len(puzzle)-1:
			temp_puzzle = deepcopy(puzzle)
			temp_puzzle[blank_row][blank_col + 1] = 0
			temp_puzzle[blank_row][blank_col] = puzzle[blank_row][blank_col+1]
			if temp_puzzle not in repeated_state:
				valid_puzzles.append(temp_puzzle)
			moves.append('right')
		if blank_row + 1 <= len(puzzle)-1:
			temp_puzzle = deepcopy(puzzle)
			temp_puzzle[blank_row + 1][blank_col] = 0
			temp_puzzle[blank_row][blank_col] = puzzle[blank_row+1][blank_col]
			if temp_puzzle not in repeated_state:
				valid_puzzles.append(temp_puzzle)
			moves.append('down')
		return valid_puzzles


# This contains my searching algorithms
class SearchAlgorithm: 
	def uniform_cost_search(self,puzzle):
		repeated_state = []
		print("Start: ", puzzle)
		obj = Puzzles()
		queue = self.make_queue(puzzle)

		count = 0
		while (len(queue) > 0):
		#print(queue.pop().value)
			node = queue.pop(0).value
			print("Current HEAD")
			obj.print_puzzle(node)
			repeated_state.append(node)

			#obj.print_puzzle(node)
			if node == goal_state:
				print("W00T!")
				return True
			queue = self.queueing_function(queue, node, puzzle,repeated_state)
			count +=1

		return False
		#print("queue", queue, queue[0].value)

	def queueing_function(self, queue, node, puzzle, repeated_state):
		obj = Puzzles()
		print("Entering Queueing function")
		next_moves = obj.valid_moves(node, repeated_state)
		#print("Head of Node:")
		#obj.print_puzzle(node)
		print("Next Legal Moves Moves")
		obj.print_puzzle(next_moves)
		for item in next_moves:
			duplicate = False
			node = Node(item)
			if len(queue) > 0:
				
				if node.value in queue:
					print ("already exists")
				else:
					queue.append(node)
			else:
				queue.append(node)
		print("Queue items")
		for p in queue: 
			print ( p.value)
		print("___________________")
		return queue

	def make_queue(self,puzzle):
		#queue = []
		queue = []
		node = Node(puzzle)
		#print(node.value)
		queue.append(node)
		#print(queue)
		return queue

def main(puzzle):
	obj = SearchAlgorithm()
	obj.uniform_cost_search(puzzle)
	return

main(puzzle)