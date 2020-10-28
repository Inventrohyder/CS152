import numpy as np
from puzzle_node import PuzzleNode
# Add any additional code here (e.g. for the memoization extension)

# YOUR CODE HERE (OPTIONAL)

# Misplaced tiles heuristic
def h1(state):
    """
    This function returns the number of misplaced tiles, given the board state
    Input:
        -state: the board state as a list of lists
    Output:
        -h: the number of misplaced tiles
    """
    state = PuzzleNode(state)
    return sum(
        [1 for i, x in enumerate(state.puzzle.flatten()) if i != x and x != 0]
    )

# Manhattan distance heuristic
def h2(state):
    """
    This function returns the Manhattan distance from the solved state, given the board state
    Input:
        -state: the board state as a list of lists
    Output:
        -h: the Manhattan distance from the solved configuration
    """
    node = PuzzleNode(state)
    total = 0
    for x in range(node.n):
        for y in range(node.n):
            if  node.goal[x][y] != 0:
                position = np.where(node.puzzle == node.goal[x][y])
                total += abs(position[0] - x) + abs(position[1] - y)
    return int(total)
    
# Extra heuristic for the extension.  If implemented, modify the function below
def h3(state):
    """
    This function returns a heuristic that dominates the Manhattan distance, given the board state
    Input:
        -state: the board state as a list of lists
    Output:
        -h: the Heuristic distance of the state from its solved configuration
    """
    return 0

# If you implement more than 3 heuristics, then add any extra heuristic functions onto the end of this list.
heuristics = [h1, h2, h3]