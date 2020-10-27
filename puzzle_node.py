# Import any packages you need here
# Also define any variables as needed
import numpy as np
from typing import List

# YOUR CODE HERE (OPTIONAL)

# Now, define the class PuzzleNode:


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

    def empty_slot(self):
        return np.where(self.puzzle == 0)

    def is_valid_position(self, position: tuple) -> bool:
        if position[0] < self.n and position[0] >= 0:
            if position[1] < self.n and position[1] >= 0:
                return True
        return False

    def movable_tiles(self) -> List[tuple]:
        empty = self.empty_slot()
        valid = []
        next_positions = list()
        next_positions.append(
            (empty[0], empty[1] + 1)  # right
        )
        next_positions.append(
            (empty[0], empty[1] - 1)  # left
        )
        next_positions.append(
            (empty[0] - 1, empty[1])  # up
        )
        next_positions.append(
            (empty[0] + 1, empty[1])  # down
        )
        for position in next_positions:
            if self.is_valid_position(position):
                valid.append(position)
        return valid

    def is_goal(self):
        return np.all(self.puzzle == self.goal)

    def __str__(self):
        return self.puzzle.__str__()
