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

    def __init__(self,
                puzzle: List[List[int]],
                f_val: int = 0, g_val: int = 0,
                parent = None):
        self.puzzle = np.array(puzzle)
        self.state = self.puzzle.tolist()
        self.n = len(puzzle[0])
        self.goal = np.arange(
            len(self.puzzle.flatten())
        ).reshape(
            self.n,
            self.n
        )
        self.pruned = False
        self.f_val = f_val
        self.g_val = g_val
        self.parent = parent

    def is_valid_puzzle(self) -> bool:
        unique_numbers = set(self.puzzle.flatten())
        if len(unique_numbers) != self.n ** 2:
            return False
        return True

    def empty_slot(self) -> np.array:
        return np.where(self.puzzle == 0)

    def is_valid_position(self, position: tuple) -> bool:
        empty = self.empty_slot()
        if position[0] == empty[0] and position[1] == empty[1]:
            return False
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

    def get_next_node(self, position: tuple):
        if self.is_valid_position(position):
            empty = self.empty_slot()
            puzzle = self.puzzle.copy()
            puzzle[empty], puzzle[position] = puzzle[position], puzzle[empty]
            return PuzzleNode(puzzle=puzzle)
        raise ValueError("Invalid position")


    def is_goal(self):
        return np.all(self.puzzle == self.goal)

    def __lt__(self, other):
        return self.f_val < other.f_val

    def __str__(self):
        return self.puzzle.__str__()
