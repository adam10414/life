"""This module contains the GUI for Life."""

# PySimpleGUI GitHub: https://github.com/PySimpleGUI/PySimpleGUI
# PySimpleGUI Documentation: https://pysimplegui.readthedocs.io/en/latest/
# PySimpleGUI call reference doc: https://pysimplegui.readthedocs.io/en/latest/call%20reference/
import PySimpleGUI as gui
from PySimpleGUI.PySimpleGUI import WINDOW_CLOSED, Canvas

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
while True:
    event, values = window.read()

    if event == gui.WINDOW_CLOSED or event == "Quit":
        break

print("Broke out of loop")

window.close()