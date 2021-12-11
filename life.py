"""This module contains the GUI for Life."""

import sys

# PySimpleGUI GitHub: https://github.com/PySimpleGUI/PySimpleGUI
# PySimpleGUI Documentation: https://pysimplegui.readthedocs.io/en/latest/
# PySimpleGUI call reference doc: https://pysimplegui.readthedocs.io/en/latest/call%20reference/
import PySimpleGUI as gui

from life_components.life_grid import LifeBoard
from life_utils.pop_ups import grid_size_warning

starting_head = [
    gui.Text("Welcome to the Game of Life!", auto_size_text=True),
    gui.Input("Grid Size: Must be > 2", key="grid_size"),
    gui.Button("Submit", target="grid_size")
]


def make_foot():
    return [gui.Button("Quit")]


layout = [starting_head, make_foot()]

starting_window = gui.Window("Hello World! GUI",
                             layout,
                             resizable=True,
                             size=(500, 500))

# Event Loop
# I'm not sure why, but it appears I can't combine
# the next two conditionals into one line.
# This is likely due to some weirdness with the library.

print()

while True:
    event, values = starting_window.read()

    if event == gui.WINDOW_CLOSED or event == "Quit":
        break

    # Generating life board, and running new window.
    if event == "Submit" and values.get("grid_size"):
        print("Detected grid submit")
        size = values["grid_size"]
        grid_input_valid = grid_size_warning(size)

        if grid_input_valid:
            starting_window.close()

            size = int(values["grid_size"])
            lifeboard = LifeBoard([size, size])

            life_window = gui.Window(
                "Game of Life",
                layout=[lifeboard.generate_grid(),
                        make_foot()],
                size=(500, 500))

        while grid_input_valid:
            life_event, life_values = life_window.read()

            if life_event == gui.WINDOW_CLOSED or life_event == "Quit":
                break

            # Processing LifeBoard
            # If a LifeNode button was pressed...
            if life_event.startswith("LN Position: "):
                # Extract the coordinates of the node.
                life_node_position = [int(life_event[14]), int(life_event[17])]
                life_node_row = life_node_position[0]
                life_node_column = life_node_position[1]

                life_node = lifeboard.update_node(life_node_position)
                life_window[f"LN Position: {life_node_position}"].update(
                    button_color=life_node.color)

        # It's possible to hit this point before life_window is initiatlized.
        try:
            life_window.close()
        except NameError:
            pass

    print(event, values)

starting_window.close()