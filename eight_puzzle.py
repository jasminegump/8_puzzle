# Outside citations
# https://www.ics.uci.edu/~welling/teaching/271fall09/InfSearch271f09.ppt
# https://stackoverflow.com/questions/43838601/how-can-i-get-the-index-of-a-nested-list-item
# deepcopy python
# heapq python


# TO DO
# How to create a graph/tree structure
# Then implement manhattan and misplaced tiles which is just different h(n) heuristics

from copy import deepcopy
import heapq

#puzzle = [[1,2,3],[5,4,0],[7,8,6]]
#puzzle = [[2,8,1],[0,4,3],[7,6,5]]
puzzle = [[1,8,2],[0,4,3],[7,6,5]]
goal_state = [[1,2,3],[4,5,6],[7,8,0]]

# My node class
class Node:
	def __init__(self, puzzle, g, h1, h2):

		# Contains the actual puzzle
		self.puzzle = puzzle

		# g(n) cost so far
		self.g = g

		# Heuristics where h1 = misplaced tiles, h2 = manhattan
		self.h1 = h1
		self.h2	= h2

	# This is necessary in order for heapqueue to work since certain heuristics will have the same priority
	# Therefore, arbitrarily compare nodes because priority really doesn't matter when they have the same f(n)
	# Got information on how to do this from:
	# https://stackoverflow.com/questions/39423979/order-of-comparison-for-heap-elements-in-python
	def __lt__(self, next):
		return self.h1 < next.h1

# Prints the puzzle nicely
def print_puzzle(puzzle):
	for i in puzzle:
		print (i)
	print("\n")

# Swaps the number with the blank spot 0
def swap_pieces(expand_puzzle, puzzle, seen_puzzle, num_row, num_col, b_row, b_col):

	# Must deepcopy the puzzle because each swap needs to be a new list and not a modification of old list
	# Each puzzle is a unique copy
	temp_puzzle = deepcopy(puzzle)

	# Swap blank and number
	temp_puzzle[num_row][num_col] = 0
	temp_puzzle[b_row][b_col] = puzzle[num_row][num_col]

	# Check if puzzle state seen before and add to seen puzzles
	if temp_puzzle not in seen_puzzle:
		expand_puzzle.append(temp_puzzle)
	return expand_puzzle

# Outputs a nested list of valid puzzles
def expand_node(puzzle, seen_puzzle):
	moves = []
	expand_puzzle = []

	# Returns blank's location as a tuple
	# Looking for 0
	# Consulted Stack Overflow for list comprehension: 
	# https://stackoverflow.com/questions/43838601/how-can-i-get-the-index-of-a-nested-list-item
	blank = 0
	blank_loc = [(i, j.index(blank)) for i, j in enumerate(puzzle) if blank in j]
	blank_row, blank_col = blank_loc[0][0], blank_loc[0][1]
	
	# Finds all valid moves

	# Move blank LEFT
	if blank_col - 1 >= 0:
		num_row = blank_row
		num_col = blank_col - 1
		expand_puzzle = swap_pieces(expand_puzzle, puzzle, seen_puzzle, num_row, num_col, blank_row, blank_col)

	# Move blank UP
	if blank_row - 1 >= 0:
		num_row = blank_row - 1
		num_col = blank_col
		expand_puzzle = swap_pieces(expand_puzzle, puzzle, seen_puzzle, num_row, num_col, blank_row, blank_col)

	# Move blank RIGHT
	if blank_col + 1 <= len(puzzle)-1:
		num_row = blank_row
		num_col = blank_col + 1
		expand_puzzle = swap_pieces(expand_puzzle, puzzle, seen_puzzle, num_row, num_col, blank_row, blank_col)

	# Move blank DOWN
	if blank_row + 1 <= len(puzzle)-1:
		num_row = blank_row + 1
		num_col = blank_col
		expand_puzzle = swap_pieces(expand_puzzle, puzzle, seen_puzzle, num_row, num_col, blank_row, blank_col)

	return expand_puzzle

###############################################################

# Uniform cost search search algorithm
def uniform_cost_search(puzzle):
	global num_nodes, max_queue
	seen_puzzle = []

	print("Expanding State: ", puzzle)

	# Make queue with initial state
	queue = make_fifo_queue(puzzle)

	# Loop until queue is empty
	while (len(queue) > 0):

		# Remove front
		node = queue.pop(0)

		# Add puzzle to seen puzzles
		seen_puzzle.append(node.puzzle)

		# 
		if node.puzzle == goal_state:
			print("Goal!")
			print("Expanded Nodes: ", num_nodes)
			print("Max Queue: ", max_queue)
			print("Depth: ", node.g)
			return True

		print("Expanding state")
		print_puzzle(node.puzzle)
		queue = fifo_queue_func(queue, node, seen_puzzle)

	# Exhausted every state and did not find solution
	return False

# Uniform Cost Search FIFO Queue
def make_fifo_queue(puzzle):
	global num_nodes, max_queue
	queue = []
	node = Node(puzzle, 0, 0, 0) # g = 0
	queue.append(node)
	num_nodes += 1
	if len(queue) > max_queue:
		max_queue = len(queue)
	return queue

# Uniform cost search queueing function
def fifo_queue_func(queue, node, seen_puzzle):
	global num_nodes, max_queue

	# This expands next moves
	expand_nodes = expand_node(node.puzzle, seen_puzzle)
	
	# Loads up queue with all expanded nodes
	for puzzle in expand_nodes:
		g = node.g + 1
		new_node = Node(puzzle, g, 0, 0)
		queue.append(new_node)
		num_nodes += 1
		if len(queue) > max_queue:
			max_queue = len(queue)
	for p in queue: 
		print ( p.puzzle)
	print("___________________")
	return queue

###############################################################
# A* Misplaced tile search algorithm

def misplaced_tile_search(puzzle):

	global num_nodes, max_queue

	seen_puzzle = []
	print("Expanding: ", puzzle)

	# Make queue with initial state
	heapq, queue = make_heap_queue(puzzle)

	# Loop until queue is empty
	while(len(queue) > 0):

		# Node is a tuple where the first item of tuple is the priorty of the heap queue and second item is the 
		# actual node containing the puzzle
		node = heapq.heappop(queue)
		node = node[1]

		seen_puzzle.append(node)

		if node.puzzle == goal_state:
			print("Goal!")
			print("Expanded Nodes: ", num_nodes)
			print("Max Queue: ", max_queue)
			print("Depth: ", node.g)
			return True
		print("Expanding state")
		print_puzzle(node.puzzle)
		heapq, queue = misplaced_queue_f(heapq, queue, node,seen_puzzle)

	return False

# A* Misplaced tile heap queue
# Read up on how to use heap queue library at the following:
# https://www.geeksforgeeks.org/heap-queue-or-heapq-in-python/
def make_heap_queue(puzzle):

	global num_nodes, max_queue

	queue = []
	heapq.heapify(queue)
	node = Node(puzzle, 0, 0, 0)

	# Save off into heap queue as a tuple: (priority, node)
	# Got information on this at the following:
	# https://docs.python.org/2/library/heapq.html#basic-examples
	heapq.heappush(queue,(0,node)) 

	num_nodes += 1
	if len(queue) > max_queue:
		max_queue = len(queue)

	return heapq, queue

# Calculates h1 which is the misplaced tile heuristic
def calc_h1(puzzle):
	h1 = 0
	for i in range(len(puzzle)):
		for j in range(len(puzzle)):
			# Count number of misplaced tiles (don't count blank or 0)
			if ((puzzle[i][j] != goal_state[i][j]) & (puzzle[i][j] != 0)):
					h1 += 1
	return h1

# A* Misplaced tile heap queuing function
def misplaced_queue_f(heapq, queue, node, seen_puzzle):
	global num_nodes, max_queue

	print(node.puzzle)

	# This expands next moves
	expand_nodes = expand_node(node.puzzle, seen_puzzle)
	
	# Go through each puzzle in the expanded moves and calculate f(n)
	# Put into heap queue in order of f(n) priority
	for puzzle in expand_nodes:
		h1 = calc_h1(puzzle)
		new_node = Node(puzzle, node.g + 1, h1 , 0)
		f = int(new_node.h1 + new_node.g)
		heapq.heappush(queue,(f,new_node))

		num_nodes += 1

		if len(queue) > max_queue:
			max_queue = len(queue)
	'''
	for p in queue: 
		print (p[0],p[1].value)
	print("___________________")
	'''
	return heapq, queue


###############################################################

def a_star_manhat_queue_f(heapq, queue, node, n, puzzle,seen_puzzle):
	global num_nodes, max_queue
	

	next_moves = expand_node(node, seen_puzzle)
	
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
	global num_nodes, max_queue
	seen_puzzle = []
	print("Start: ", puzzle)
	heapq, queue = make_heap_queue(puzzle)
	count = 0

	while(len(queue) > 0):
		node = heapq.heappop(queue)
		#print(node[1].value) # node[1] contains the actual node
		n = node[1]
		node = node[1].value
		seen_puzzle.append(node)

		if node == goal_state:
			print("Goal!")
			print("Expanded Nodes: ", num_nodes )
			print("Max Queue: ", max_queue)
			print("depth: ", n.g)
			return True
		print("Expanding state")
		print_puzzle(node)
		heapq, queue = a_star_manhat_queue_f(heapq, queue, node, n, puzzle,seen_puzzle)

	return False
###############################################################

def main(puzzle):
	global num_nodes, max_queue
	num_nodes,max_queue = 0,0
	#uniform_cost_search(puzzle)
	misplaced_tile_search(puzzle)
	#a_star_manhattan(puzzle)
	return

main(puzzle)