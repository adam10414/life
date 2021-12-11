"""This module contains the GUI for Life."""

import sys

# PySimpleGUI GitHub: https://github.com/PySimpleGUI/PySimpleGUI
# PySimpleGUI Documentation: https://pysimplegui.readthedocs.io/en/latest/
# PySimpleGUI call reference doc: https://pysimplegui.readthedocs.io/en/latest/call%20reference/
import PySimpleGUI as gui

from life_components.life_grid import LifeBoard

lifeboard = LifeBoard([3, 3])

row1 = [gui.Text("Testing Buttons")]
grid = lifeboard.generate_grid()
row3 = [gui.Button("Quit")]

layout = [row1, grid, row3]

window = gui.Window("Hello World! GUI",
                    layout,
                    resizable=True,
                    size=(500, 500))

# Event Loop
# I'm not sure why, but it appears I can't combine
# the next two conditionals into one line.
# This is likely due to some weirdness with the library.

print()

while True:
    event, values = window.read()

    if event == gui.WINDOW_CLOSED or event == "Quit":
        break

    # Processing LifeBoard
    # If a LifeNode button was pressed...
    if event.startswith("LN Position: "):
        # Extract the coordinates of the node.
        life_node_position = [int(event[14]), int(event[17])]
        life_node_row = life_node_position[0]
        life_node_column = life_node_position[1]

        life_node = lifeboard.update_node(life_node_position)
        window[f"LN Position: {life_node_position}"].update(
            button_color=life_node.color)

        life_node_neighbors = lifeboard.get_neighbors(life_node)
        print(event)
        print("")
        print(life_node_neighbors)

print("Broke out of loop")

window.close()