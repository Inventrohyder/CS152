from puzzle_node import PuzzleNode
from queue import PriorityQueue
from typing import List
from heuristics import heuristics
import json


def get_error_code(node: PuzzleNode) -> int:
    """
    Checks if the puzzle has an error

    :param node: the puzzle to check
    :returns -1 if it is an invalid puzzle,
        -2 if it is not solvable
        0 if there is no error
    """
    if not node.is_valid_puzzle():
        return - 1
    if not node.is_solvable():
        return - 2
    return 0


# Original was
# A* Tree Search Example for Robot Navigation
# By R. Shekhar
# On August 10, 2017
def solvePuzzle(state, heuristic,
                check_solvability: bool = True,
                pattern_db_filename: str = "pattern_db.json"
                ):
    """This function should solve the n**2-1 puzzle for any n > 2 (although it may take too long for n > 4)).
    Inputs:
        -state: The initial state of the puzzle as a list of lists
        -heuristic: a handle to a heuristic function.  Will be one of those defined in Question 2.
        -check_solvability: should we check the solvability of the state
        -pattern_db_filename: the file name that stores known patterns
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
    err = get_error_code(start)

    if err != 0 and check_solvability:
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
    costs_db = {str(start): start_node}

    # Frontier, stored as a Priority Queue to maintain ordering
    frontier = PriorityQueue()
    frontier.put(start_node)
    max_frontier += 1

    # Begin A* Tree Search
    while not frontier.empty():
        # Take the next available node from the priority queue
        cur_node: PuzzleNode = frontier.get()
        max_frontier -= 1

        if cur_node.pruned:
            continue  # Skip if this node has been marked for removal

        # Check if we are at the goal
        if cur_node.is_goal():
            break

        # Get the next positions
        moves = cur_node.movable_tiles()
        for move in moves:
            next_node = cur_node.get_next_node(move)

            exp += 1  # Each valid child node generated is another step
            g_val = cur_node.g_val + 1  # Tentative cost value for child

            # If the child node is already in the cost database (i.e. explored) then see if we need to update the path.
            # In a graph search, we wouldn't even bother exploring it again.
            if str(next_node) in costs_db:
                if costs_db[str(next_node)].g_val > g_val:
                    # Mark existing value for deletion from frontier
                    costs_db[str(next_node)].pruned = True
                else:
                    # ignore this child, since a better path has already been found previously.
                    continue

            # Heuristic cost from next node to goal
            h_val = cur_heuristic(next_node)
            next_node.f_val = g_val + h_val
            next_node.g_val = g_val
            next_node.parent = cur_node  # Create new node for child
            frontier.put(next_node)
            max_frontier += 1
            costs_db[str(next_node)] = next_node  # Mark the node as explored

    # Get the existing patterns
    patterns = {}
    try:
        with open("pattern_db.json", "r") as patterns_file:
            patterns = json.load(patterns_file)
    except FileNotFoundError:
        pass

    # Reconstruct the optimal path
    # and save to the pattern database
    optimal_path = [cur_node.state]
    with open("pattern_db.json", "w") as patterns_file:
        counter = 0
        while cur_node.parent:
            patterns[str(cur_node.state)] = counter
            optimal_path.append((cur_node.parent).state)
            cur_node = cur_node.parent
            counter += 1
        json.dump(patterns, patterns_file, indent=4)
    optimal_path = optimal_path[::-1]
    optimal_path_length = len(optimal_path) - 1
    return optimal_path_length, exp, max_frontier, optimal_path, err
