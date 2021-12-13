"""
This module contains the logic for the life grid.
"""
from typing import Counter

import PySimpleGUI as gui
from PySimpleGUI.PySimpleGUI import Window

from life_utils.layout_functions import make_foot


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
        self.next_status = None

        if self.alive:
            self.color = "white"

        else:
            self.color = "black"

        # The key must be str.
        # key will be passed to the event loop. This is how we'll know what to update.
        self.button = gui.Button(f"",
                                 button_color=self.color,
                                 expand_x=True,
                                 expand_y=True,
                                 mouseover_colors="light blue",
                                 pad=1,
                                 metadata=self.position,
                                 key=f"LN Position: {self.position}")

    def giveth_life(self):
        self.alive = True
        self.color = "white"

    def taketh_life(self):
        self.alive = False
        self.color = "black"

    def iterate(self):
        """
        Nodes are acted on in 2 steps. Pre-processing
        and iterating. Nodes need to be evaluated and
        acted on in 2 steps to prevent a race condition
        where a node being modified to alive will afect
        another node that hasn't been evaluated yet.

        When preprocessing the ndoe's next_status is set.
        When iterating, this method evaluates next status,
        and sets the other values of this node appropriately.

        This method will always reset self.next_status back to None.
        """

        if self.alive and self.next_status == "dead":
            self.taketh_life()
            self.next_status = None

        if not self.alive and self.next_status == "alive":
            self.giveth_life()
            self.next_status = None

        self.next_status = None

    def __repr__(self) -> str:
        if self.alive:
            return f"LN position: {self.position}. Status: alive"

        else:
            return f"LN position: {self.position}. Status: dead"


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

        self.life_grid_buttons = []
        self.life_grid = []
        for row in range(self.x_axis_length):

            row_list = []
            button_row_list = []

            for column in range(self.y_axis_length):

                life_node = LifeNode([row, column])
                row_list.append(life_node)
                button_row_list.append(life_node.button)

            self.life_grid.append(row_list)
            self.life_grid_buttons.append(button_row_list)

            self.number_of_rows = len(self.life_grid)
            # Since we're working with a square, we can assume the first
            # element of the life grid will contain the total number of columns.
            self.number_of_columns = len(self.life_grid[0])

        return self.life_grid_buttons

    # Not sure if this should just be in a seperate module, or if it's okay to keep it here.
    def life_window(self, production_flag=True):
        """
        A self contained instance of a PySimpleGui window.
        This method exists to help clean up the main life.py module.
        """

        next_step = gui.Button("Next Step")
        start_stop = gui.Button("Start/Stop")
        clear_board = gui.Button("Clear Board")

        layout = [[next_step, start_stop, clear_board],
                  self.generate_grid(),
                  make_foot()]

        self.window = gui.Window("Game of Life",
                                 layout=layout,
                                 size=(1000, 1000))

        while True:

            if production_flag:
                life_event, life_values = self.window.read()
                # print(life_event, life_values)

            # In a test enviornment, do not wait and allow the program to continue.
            else:
                life_event, life_values = None, {}
                self.window.read(timeout=1)
                self.window.close()

            if life_event == gui.WINDOW_CLOSED or life_event == "Quit":
                break

            if life_event == "Clear Board":
                self.clear_board()

            if life_event == "Start/Stop":
                while True:
                    life_event, life_values = self.window.read(timeout=1)
                    print(life_event, life_values)

                    self.pre_process_life_nodes()
                    self.process_iteration()

                    if life_event == gui.WINDOW_CLOSED or life_event == "Quit":
                        break

                    if life_event == "Start/Stop":
                        break

            if life_event == "Next Step":
                self.pre_process_life_nodes()
                self.process_iteration()

            # Processing LifeBoard
            # If a LifeNode button was pressed...
            if life_event.startswith("LN Position: "):

                # Extract the coordinates of the node.
                life_node_position = self.calculate_ln_position(life_event)

                # Update button color to match node status.
                life_node = self.node_button_press(life_node_position)
                self.update_node_button(life_node)

        # It's possible to hit this point before self.window is initiatlized.
        try:
            self.window.close()
        except NameError:
            pass

    def update_node_button(self, life_node):
        """
        Updates the button color.
        Must be run after self.window().
        """
        self.window[f"LN Position: {life_node.position}"].update(
            button_color=life_node.color)

    def clear_board(self):
        """
        Kills all life nodes on the grid.
        Must be run after self.generate_grid()
        """

        for row in self.life_grid:
            for node in row:
                node.taketh_life()
                self.update_node_button(node)

    def calculate_ln_position(self, window_event):
        """
        Since PySimpleGui can only pass strings as event information,
        we need to parse it. This function calculates the life node
        position based on the event emitted by pressing the button.
        """

        # Button events are emitted as: "LN Position: [5, 19]"
        #                                pos 14 and 17 ^  ^

        # Finding the opening braket, and going up to the comma.
        x = int(window_event[window_event.find("[") +
                             1:window_event.find(",")])

        # Finding the ", " and going up to the closing bracket.
        y = int(window_event[window_event.find(", ") +
                             1:window_event.find("]")])

        return [x, y]

    def pre_process_life_nodes(self):
        """
        This method will gather the status of all nodes
        on the board, and determine their life status on
        the next iteration. Returns a 2-D list of LifeNodes
        to be processed in the next iteration.
        """

        for row in self.life_grid:
            for node in row:
                neighbors = self.get_neighbors(node)
                neighbors = [
                    self.get_life_node(node).alive for node in neighbors
                    if node != None
                ]
                count_of_status = Counter(neighbors)
                alive_neighbors = count_of_status.get(True)
                if not alive_neighbors:
                    alive_neighbors = 0

                # Rules of the game of life.
                if node.alive and alive_neighbors < 2:
                    node.next_status = "dead"

                if node.alive and alive_neighbors == 2 or alive_neighbors == 3:
                    node.next_status = "alive"

                if node.alive and alive_neighbors > 3:
                    node.next_status = "dead"

                if not node.alive and alive_neighbors == 3:
                    node.next_status = "alive"

    def process_iteration(self):
        """
        Processes changes made in pre_process_life_nodes.
        This method should probably only be called inside of
        self.life_window()
        """
        for row in self.life_grid:
            for node in row:
                node.iterate()
                self.window[f"LN Position: {node.position}"].update(
                    button_color=node.color)

    def get_life_node(self, node_position):
        """
        Returns the life node at the given postion.
        node_position: list[row, column]
        """

        row = node_position[0]
        column = node_position[1]
        return self.life_grid[row][column]

    def node_button_press(self, node_position):
        """
        Switches a node between dead or alive.
        Can only be called after generate_grid().
        node_position: list [x,y]
        """

        life_node = self.get_life_node(node_position)

        if life_node.alive:
            life_node.taketh_life()
            return life_node

        else:
            life_node.giveth_life()
            return life_node

    def get_neighbors(self, life_node):
        """
        Returns a list of neighbor coordinates on the grid.
        If a node is on an edge, non-real neighbors will be
        returned as None.
        Can only be called after generate_grid().
        """

        row = life_node.position[0]
        column = life_node.position[1]

        def get_north_neighbor():
            if row - 1 >= 0:
                return [row - 1, column]

        # columns - 1 because we're working with indicies.
        def get_east_neighbor():
            if column + 1 <= self.number_of_columns - 1:
                return [row, column + 1]

        # rows - 1 because we're working with indicies.
        def get_south_neighbor():
            if row + 1 <= self.number_of_rows - 1:
                return [row + 1, column]

        def get_west_neighbor():
            if column - 1 >= 0:
                return [row, column - 1]

        def get_northeast_neighbor():
            if get_north_neighbor() and get_east_neighbor():
                return [row - 1, column + 1]

        def get_southeast_neighbor():
            if get_east_neighbor() and get_south_neighbor():
                return [row + 1, column + 1]

        def get_southwest_neighbor():
            if get_south_neighbor() and get_west_neighbor():
                return [row + 1, column - 1]

        def get_northwest_neighbor():
            if get_west_neighbor() and get_north_neighbor():
                return [row - 1, column - 1]

        return [
            get_north_neighbor(),
            get_northeast_neighbor(),
            get_east_neighbor(),
            get_southeast_neighbor(),
            get_south_neighbor(),
            get_southwest_neighbor(),
            get_west_neighbor(),
            get_northwest_neighbor()
        ]
