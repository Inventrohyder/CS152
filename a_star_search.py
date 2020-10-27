from puzzle_node import PuzzleNode
from heuristics import h1, h2, h3, heuristics
### Original was
# A* Tree Search Example for Robot Navigation
# By R. Shekhar
# On August 10, 2017

def solvePuzzle(state, heuristic):
    """This function should solve the n**2-1 puzzle for any n > 2 (although it may take too long for n > 4)).
    Inputs:
        -state: The initial state of the puzzle as a list of lists
        -heuristic: a handle to a heuristic function.  Will be one of those defined in Question 2.
    Outputs:
        -steps: The number of steps to optimally solve the puzzle (excluding the initial state)
        -exp: The number of nodes expanded to reach the solution
        -max_frontier: The maximum size of the frontier over the whole search
        -opt_path: The optimal path as a list of list of lists.  That is, opt_path[:,:,i] should give a list of lists
                    that represents the state of the board at the ith step of the solution.
        -err: An error code.  If state is not of the appropriate size and dimension, return -1.  For the extention task,
          if the state is not solvable, then return -2
    """
    # Define the start
    start = PuzzleNode(state)

    optimal_path_length = 0
    exp = 0
    max_frontier = 0
    optimal_path = None
    err = 0

    if not start.is_valid_puzzle():
        err = -1
        return optimal_path_length, exp, max_frontier, optimal_path, err

    # Define the heuristic functions here
    def f(node, heuristic=heuristic):
   	    return heuristic(node.state) 

    cur_heuristic = f


    # Start node
    start_node = start
    start_node.f_val = cur_heuristic(start)
    start_node.g_val = 0

    # Dictionary with current cost to reach all visited nodes
    costs_db = {str(start):start_node}

    # Frontier, stored as a Priority Queue to maintain ordering
    from queue import PriorityQueue

    frontier = PriorityQueue()
    frontier.put(start_node)
    max_frontier += 1

    # Begin A* Tree Search
    while not frontier.empty():
        # Take the next available node from the priority queue
        cur_node: PuzzleNode = frontier.get()
        max_frontier -= 1

        if cur_node.pruned:
            continue # Skip if this node has been marked for removal

        # Check if we are at the goal
        if cur_node.is_goal() : break

        # Get the next positions
        moves = cur_node.movable_tiles()
        for move in moves:
            next_node = cur_node.get_next_node(move)

            exp += 1 # Each valid child node generated is another step
            g_val = cur_node.g_val + 1 # Tentative cost value for child

            # If the child node is already in the cost database (i.e. explored) then see if we need to update the path.
            # In a graph search, we wouldn't even bother exploring it again.
            if str(next_node) in costs_db:
                if costs_db[str(next_node)].g_val > g_val:
                    costs_db[str(next_node)].pruned = True # Mark existing value for deletion from frontier
                else:
                    continue # ignore this child, since a better path has already been found previously.

            h_val = cur_heuristic(next_node)  # Heuristic cost from next node to goal
            next_node.f_val = g_val + h_val
            next_node.g_val = g_val
            next_node.parent = cur_node  # Create new node for child
            frontier.put(next_node)
            max_frontier += 1
            costs_db[str(next_node)] = next_node  # Mark the node as explored

    # Reconstruct the optimal path
    optimal_path = [cur_node.state]
    while cur_node.parent:
        optimal_path.append((cur_node.parent).state)
        cur_node = cur_node.parent
    optimal_path = optimal_path[::-1]
    print(f"A* search completed in {exp} steps\n")
    print(f"A* path length: {len(optimal_path)-1} steps\n")
    print(f"A* path to goal:\n")
    print(optimal_path)
    optimal_path_length = len(optimal_path)-1
    return optimal_path_length, exp, max_frontier, optimal_path, err