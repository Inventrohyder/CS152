# Import any packages you need here
# Also define any variables as needed
import numpy as np
from typing import List

# YOUR CODE HERE (OPTIONAL)

#Now, define the class PuzzleNode:
class PuzzleNode:
    """
    Class PuzzleNode: Provides a structure for performing A* search for the n^2-1 puzzle
    """
    def __init__(self, puzzle: List[List[int]]):
        self.puzzle = np.array(puzzle)
        self.n = len(puzzle[0])
        self.goal = np.arange(
            len(self.puzzle.flatten())
            ).reshape(
                self.n,
                self.n
                )
        # n = len(puzzle[0])
        # unique_numbers = set(puzzle.flatten())
        # if len(unique_numbers) != n ** 2:
        #     return - 1

    def is_goal(self):
        return np.all(self.puzzle == self.goal)
        
    def __str__(self):
        return self.puzzle.__str__()
