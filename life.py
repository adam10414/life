"""This module contains the GUI for Life."""

import sys

# PySimpleGUI GitHub: https://github.com/PySimpleGUI/PySimpleGUI
# PySimpleGUI Documentation: https://pysimplegui.readthedocs.io/en/latest/
# PySimpleGUI call reference doc: https://pysimplegui.readthedocs.io/en/latest/call%20reference/
import PySimpleGUI as gui

from life_components.life_grid import LifeBoard
from life_utils.pop_ups import grid_size_warning
from life_utils.layout_functions import make_foot

starting_head = [
    gui.Text("Welcome to the Game of Life!", auto_size_text=True),
    gui.Input("Grid Size: Must be > 2", key="grid_size"),
    gui.Button("Submit", target="grid_size")
]

layout = [starting_head, make_foot()]

starting_window = gui.Window("Hello World! GUI",
                             layout,
                             resizable=True,
                             size=(500, 500))

# Event Loop
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
            lifeboard.life_window()

    print(event, values)

starting_window.close()