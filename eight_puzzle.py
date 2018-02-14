# Outside citations
# https://www.ics.uci.edu/~welling/teaching/271fall09/InfSearch271f09.ppt
# https://stackoverflow.com/questions/43838601/how-can-i-get-the-index-of-a-nested-list-item
# deepcopy python

# TO DO
# How to create a graph/tree structure
# Then implement manhattan and misplaced tiles which is just different h(n) heuristics

from copy import deepcopy
import heapq

#puzzle = [[1,2,3],[5,4,0],[7,8,6]]
#puzzle = [[2,8,1],[0,4,3],[7,6,5]]
puzzle = [[1,8,2],[0,4,3],[7,6,5]]
goal_state = [[1,2,3],[4,5,6],[7,8,0]]

class Node:
	def __init__(self, value, g, h1, h2):

		self.parent = None
		self.value = value

		# g(n) cost so far
		self.g = g

		# Heuristics where h1 = misplaced tiles, h2 = manhattan
		self.h1 = h1
		self.h2	= h2

	 # do not compare nodes
	 # https://stackoverflow.com/questions/39423979/order-of-comparison-for-heap-elements-in-python
	def __lt__(self, other):
		return self.h1 < other.h1

# This contains my puzzle helper functions

def print_puzzle(puzzle):
	for i in puzzle:
		print (i)
	print("\n")

def valid_append(valid_puzzles, puzzle, repeated_state, row_1, col_1, row_2, col_2):
	temp_puzzle = deepcopy(puzzle)
	temp_puzzle[row_1][col_1] = 0
	temp_puzzle[row_2][col_2] = puzzle[row_1][col_1]
	if temp_puzzle not in repeated_state:
		valid_puzzles.append(temp_puzzle)
	return valid_puzzles

# Outputs a nested list of valid puzzles
def valid_moves(puzzle, repeated_state):
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
		valid_puzzles = valid_append(valid_puzzles, puzzle, repeated_state, blank_row, blank_col - 1, blank_row, blank_col)

	# UP
	if blank_row - 1 >= 0:
		valid_puzzles = valid_append(valid_puzzles, puzzle, repeated_state, blank_row - 1, blank_col, blank_row, blank_col)

	# RIGHT
	if blank_col + 1 <= len(puzzle)-1:
		valid_puzzles = valid_append(valid_puzzles, puzzle, repeated_state, blank_row, blank_col + 1, blank_row, blank_col)

	# DOWN
	if blank_row + 1 <= len(puzzle)-1:
		valid_puzzles = valid_append(valid_puzzles, puzzle, repeated_state, blank_row + 1, blank_col, blank_row, blank_col)

	return valid_puzzles


# This contains my searching algorithms

def uniform_cost_search(puzzle):
	g = 0
	global num_nodes, max_queue
	repeated_state = []
	print("Start: ", puzzle)
	queue = make_queue(puzzle)

	while (len(queue) > 0):
		#print("num_nodes",num_nodes)
		n = queue.pop(0)
		node = n.value
		
		repeated_state.append(node)

		if node == goal_state:
			print("Goal!")
			print("Expanded Nodes: ", num_nodes)
			print("Max Queue: ", max_queue)
			print("depth: ", n.g)

			return True
		print("Expanding state")
		print_puzzle(node)
		queue = queueing_function(queue, node, n, puzzle,repeated_state)

	return False
	#print("queue", queue, queue[0].value)

# Uniform cost search
def queueing_function(queue, node, n, puzzle, repeated_state):
	global num_nodes, max_queue

	next_moves = valid_moves(node, repeated_state)
	
	for item in next_moves:
		node = Node(item, n.g + 1,0,0)
		queue.append(node)
		num_nodes += 1
		if len(queue) > max_queue:
			max_queue = len(queue)
	for p in queue: 
		print ( p.value)
	print("___________________")
	return queue

# FIFO Queue for Uniform Cost Search
def make_queue(puzzle):
	global num_nodes, max_queue
	queue = []
	node = Node(puzzle, 0, 0, 0) # g = 0
	queue.append(node)
	num_nodes += 1
	if len(queue) > max_queue:
		max_queue = len(queue)
	return queue

# https://www.geeksforgeeks.org/heap-queue-or-heapq-in-python/
def make_heap_queue(puzzle):
	global num_nodes, max_queue
	queue = []
	heapq.heapify(queue)
	node = Node(puzzle, 0, 0, 0) # g = 0

	#https://docs.python.org/2/library/heapq.html#basic-examples
	heapq.heappush(queue,(0,node)) # Save off into heap queue as a tuple: (priority, node)
	num_nodes += 1
	if len(queue) > max_queue:
		max_queue = len(queue)
	return heapq, queue

def a_star_queue_f(heapq, queue, node, n, puzzle,repeated_state):
	global num_nodes, max_queue

	next_moves = valid_moves(node, repeated_state)
	
	for item in next_moves:
		h1 = 0
		# First calculate the f(n)
		for i in range(len(item)):
			#print(i)
			for j in range(len(item)):
				#print(item[i][j], goal_state[i][j])
				if item[i][j] != goal_state[i][j]:
					if item[i][j] != 0: # don't count 0
						h1 += 1

		#print(item, h1)
		node = Node(item, n.g + 1, h1 , 0)
		num_nodes += 1
		f = int(node.h1 + node.g)
		heapq.heappush(queue,(f,node))
		if len(queue) > max_queue:
			max_queue = len(queue)
	'''
	for p in queue: 
		print (p[0],p[1].value)
	print("___________________")
	'''
		
	return heapq, queue

def a_star_tile(puzzle):
	g = 0
	global num_nodes, max_queue
	repeated_state = []
	print("Start: ", puzzle)
	heapq, queue = make_heap_queue(puzzle)
	count = 0

	while(len(queue) > 0):
		node = heapq.heappop(queue)
		#print(node[1].value) # node[1] contains the actual node
		n = node[1]
		node = node[1].value
		repeated_state.append(node)

		if node == goal_state:
			print("Goal!")
			print("Expanded Nodes: ", num_nodes )
			print("Max Queue: ", max_queue)
			print("depth: ", n.g)
			return True
		print("Expanding state")
		print_puzzle(node)
		heapq, queue = a_star_queue_f(heapq, queue, node, n, puzzle,repeated_state)

	return False


def a_star_manhat_queue_f(heapq, queue, node, n, puzzle,repeated_state):
	global num_nodes, max_queue
	

	next_moves = valid_moves(node, repeated_state)
	
	for item in next_moves:
		mismatch = []
		# First calculate the f(n)
		for i in range(len(item)):
			#print(i)
			for j in range(len(item)):
				#print(item[i][j], goal_state[i][j])
				if item[i][j] != goal_state[i][j]:
					if item[i][j] != 0: # don't count 0
						if [i,j] not in mismatch:
							mismatch.append([i,j])

		# now go through the mismatch list and calculate h2
		h2 = 0
		for k in mismatch:

			# Returns goal's location as a tuple
			# Consulted Stack Overflow for list comprehension trick: 
			# https://stackoverflow.com/questions/43838601/how-can-i-get-the-index-of-a-nested-list-item
			goal_loc = [(i, j.index(item[k[0]][k[1]])) for i, j in enumerate(goal_state) if item[k[0]][k[1]] in j]
			goal_row, goal_col = goal_loc[0][0], goal_loc[0][1]
			h2 = h2 + abs(goal_row-k[0]) + abs(goal_col-k[1])

		node = Node(item, n.g + 1, 0 , h2)
		num_nodes += 1
		f = int(node.h2 + node.g)
		heapq.heappush(queue,(f,node))
		if len(queue) > max_queue:
			max_queue = len(queue)
	'''
	for p in queue: 
		print (p[0],p[1].value)
	print("___________________")
	'''
	return heapq, queue

def a_star_manhattan(puzzle):
	g = 0
	global num_nodes, max_queue
	repeated_state = []
	print("Start: ", puzzle)
	heapq, queue = make_heap_queue(puzzle)
	count = 0

	while(len(queue) > 0):
		node = heapq.heappop(queue)
		#print(node[1].value) # node[1] contains the actual node
		n = node[1]
		node = node[1].value
		repeated_state.append(node)

		if node == goal_state:
			print("Goal!")
			print("Expanded Nodes: ", num_nodes )
			print("Max Queue: ", max_queue)
			print("depth: ", n.g)
			return True
		print("Expanding state")
		print_puzzle(node)
		heapq, queue = a_star_manhat_queue_f(heapq, queue, node, n, puzzle,repeated_state)

	return False

def main(puzzle):
	global num_nodes, max_queue
	num_nodes,max_queue = 0,0
	uniform_cost_search(puzzle)
	#a_star_tile(puzzle)
	#a_star_manhattan(puzzle)
	return

main(puzzle)