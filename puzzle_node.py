import numpy as np
from typing import List

class PuzzleNode:
    """
    Class PuzzleNode: Provides a structure for performing A* search for the n^2-1 puzzle
    """

    def __init__(self,
                 puzzle: List[List[int]],
                 f_val: int = 0, g_val: int = 0,
                 parent=None):
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

    def inversions(self) -> int:
        """
        Produces the number of inversions the puzzle has

        :returns the number of inversions in the puzzle
        """
        total_inversions = 0
        numbers = self.puzzle.flatten()
        for i, x in enumerate(numbers):
            for y in numbers[i:]:
                if x > y and y != 0:
                    total_inversions += 1
        return total_inversions

    def is_solvable(self) -> bool:
        """
        Checks if the current n * n puzzle is solvable

        The formula says:
            * If the grid width is odd, then the number of inversions in a solvable situation is even.
            * If the grid width is even, and the blank is on an even row counting from the bottom (second-last, fourth-last etc), then the number of inversions in a solvable situation is odd.
            * If the grid width is even, and the blank is on an odd row counting from the bottom (last, third-last, fifth-last etc) then the number of inversions in a solvable situation is even.
            * That gives us this formula for determining solvability:
        ( (grid width odd) && (#inversions even) )  ||  ( (grid width even) && ((blank on odd row from bottom) == (#inversions even)) )

        :returns True if it is solvable and False otherwise

        Note
        ----
        The original description of identifying solvability was by Mark Ryan
        from The University of Birmingham
        https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html

        """
        inversions = self.inversions()
        blank_row = self.empty_slot()[0]
        blank_row = self.n - blank_row  # blank row count from the bottom
        return (
            (self.n % 2 == 1 and inversions % 2 == 0) or
            (self.n % 2 == 0 and blank_row % 2 == 0 and inversions % 2 == 1) or
            (self.n % 2 == 0 and blank_row % 2 == 1 and inversions % 2 == 0)
        )

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
