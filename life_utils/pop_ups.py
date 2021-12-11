import PySimpleGUI as gui


def grid_size_warning(grid_size, test_flag=False):
    """
    Warns the user that their input is invalid.
    grid_size: input from starting_window.
    """
    try:
        grid_size = int(grid_size)
        if grid_size < 3:
            raise ValueError
        return True

    except ValueError:
        if test_flag:
            return None

        grid_size_warning = gui.Window(
            "Warning",
            finalize=True,
            layout=[[
                gui.Text(
                    "Grid size must be a whole number, and grater than 2.")
            ], [gui.Button("Close Warning")]])

        grid_size_warning.ding()

        while True:
            warning_events, warning_values = grid_size_warning.read()

            if warning_events == "Close Warning":
                break

        grid_size_warning.close()