"""
This module contains the logic for the life grid.
"""

from PySimpleGUI import Button


class LifeNode():
    """
    A life node is a single square on the board.
    It has a position of where it's located on the LifeBoard.
    It knows whether it's alive or dead.
    """
    def __init__(self, position, alive=False):
        """
        position = [row, column]
        alive = bool
        """
        if type(position) is not list:
            raise TypeError(
                f"LifeNode's position should be a list. Type received is {type(position)}"
            )

        self.position = position
        self.alive = alive

        if self.alive:
            self.color = "white"

        else:
            self.color = "black"

    def giveth_life(self):
        self.alive = True

    def taketh_life(self):
        self.alive = False

    def button(self):
        """Returns a button representation of this node."""
        return Button("",
                      button_color=self.color,
                      expand_x=True,
                      expand_y=True,
                      mouseover_colors="light blue",
                      pad=1)

    def __repr__(self) -> str:
        return f"LN position: {self.position}"


class LifeBoard():
    """
    The life board contains all of the life nodes, and rules of the game.
    This board will always be a square.
    """
    def __init__(self, grid_size):
        "grid_size: [length, height]"

        if type(grid_size) is not list:
            raise TypeError(
                f"LifeBoard.grid_size should be a list. Type received is: {type(grid_size)}"
            )

        if grid_size[0] != grid_size[1]:
            raise ValueError(
                f"Grid should be a square, the sizes provided are: Length: {grid_size[0]}, Height: {grid_size[1]}"
            )

        self.x_axis_length = grid_size[0]
        self.y_axis_length = grid_size[1]

    def generate_grid(self):
        """
        Returns a list of LifeNodes with coordinates.
        Can be used to plug directly into PySimpleGUI.
        """

        self.life_grid = []
        for row in range(self.x_axis_length):
            row_list = []
            for column in range(self.y_axis_length):
                row_list.append(LifeNode([row, column]).button())

            self.life_grid.append(row_list)

        return self.life_grid


# test_board = LifeBoard([3, 3])

# test_grid = test_board.generate_grid()

# print(test_grid)