# Conway's Game of Life
I saw this game in a Veritasium video and I thought this would be a fun project that would be easy to get off the ground, and lends its self to continual updates. See this [article](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) for an explination of what it is. 

## How to install:
- Clone/download this code to your computer.
- Install [Python](https://www.python.org/downloads/)
- Navigate to the directory where this code lives, open a terminal window, and run: `pip3 install -r requirements.txt`

## How to run:
- Open a terminal window, and navigate to this directory.
- Type: `python3 life.py` and press enter.

## How to use:
The first window to appear will be the window to collect information about how large you want the grid to be. Type in a number and press Submit.

The next window to appear will contain the grid with the individual life nodes. All nodes start out as dead. You can toggle them alive by clicking on them. Note: You can only toggle nodes while the simulation is stopped.

You can advance one step (or generation) at a time by clicking Next. Alternatively, you can have the game play its self by clicking on Start/Stop.

## TO DO:
At the time of writing, this is a bare minimum viable product. Ideally, I will never stop finding ways to improve this, but it's fairly rough around the edges at the moment.

This TODO list is not in any particular order.
- Write more tests! Code coverage is not as comprehensive as I'd like it to be.
- Game runs slower the larger the grid is. Looking at CPU usage, it's maxed out an entire core. 
    - Implement multi-core processing in Python.
- Add a generation counter.
- Add a "clear board" button to start from a clean slate.
    - Reset generation counter when this button is pressed.
- Find available monitors:
    - Select largest monitor.
    - Find screen size.
    - Take the shorter dimension, and use that as a square to display the grid.
- Make window resizable.
- Make window zoomable.
- Save simulation runs.
    - Should take the starting conditions from generation 0, and save them to disk.
- Build support for loading saved runs.
- Impliment a lexicon similar to [here](https://playgameoflife.com/)
    - User should be able to save their own patterns to it.
- Remove user input from business logic, and move into own module. (Collecting grid size.)


## Notes:
### Limitations of PySimpleGui
- Can't redraw the window once it's created. This is why two windows are needed when collecting information and then displaying the game.
- I suspect the game runs slowly because PySimpleGui consumes a lot of CPU usage to draw the buttons or something. It's either that or Python is just a slow language, and this is one of it's drawbacks.
    - Not sure if I can direct Python to utilzie the GPU for drawing the buttons, but this is worth looking into.

### Limitations of Python
Since Python is an interpreted language, it runs slowly.