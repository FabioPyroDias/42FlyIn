*This project has been created as part of the 42 curriculum by fda-cruz*

## Description

Fly-in consists of routing a set of drones, exploring a graph, and reaching a goal in the most efficient way possible, turn-by-turn.

The graph is made of hubs and connections between them. There is always a start hub and an end hub.

The map is generated from a map file, which defines the start hub as well as the end hub, all the other hubs as well as the connections.

The program ensures that:
- No duplicate hubs or connections
- The map is valid and solvable.

The project also includes visualization in the form of a graphical render.

## Requirements

Make sure `make` is installed on your system:

```bash
sudo apt install make
```

Python 3.10 or higher is required. Check your version with:

```bash
python3 --version
```

A virtual environment (flyin) will be created automatically during installation. This ensures project dependencies are isolated.

## Instructions

### Instalation
To install project dependencies, simply run `make install` in the terminal.
This will:
- Create a virtual environment flyin
- Install required Python packages (flake8, mypy, pygame, etc.)

### Execution
Run the program with `make run` followed by the path to the desired map.

## Technical Overview

### Map File
The program requires a map file to generate the graph.
Each field representing a `hub` is formatted by `KEY : VALUE` per line, followed by some optional `metadata` values enclosed in brackets, [].
In the case of the `connection`, the format is `KEY : HUB1 HUB2`, both separated by whitespace and can also be followed by optional `metadata`
Lines starting with `#` or empty are commented and ignored.

The first field must be `nb_drones`, followed by a positive **integer**

All the other mandatory fields are presented below:

| Field | Description |
|:-----|:------|
| start_hub | where all the drones exist in the first turn |
| end_hub | the goal of the map |
| hub | hubs spreaded throughout the map |
| connection | bridge between the hubs |

To ensure the correct configuration of the maps, several rules were implemented.
- `start_hub` and `end_hub` cannot have the same name nor the same coordinates.
    They have to be strictly different.
- All `hubs` must have different names as well as different coordinates
- Every `connection` is between two `hubs` and they need to be previously defined.

The optional `metadata` for `start_hub`, `end_hub` and `hub` are as follows:

| Metadata Field | Description |
|:-----|:------|
| zone | influences the turns the drones take to arrive at the hub, as well as preference in the pathfinding algorithm |
| color | affects the visual aspect of the node |
| max_drones | maximum drones that can occupy the `hub` simultaneously, the default being **1** |

The optional `metadata` for `connection` is `max_link_capacity` and this limits the amount of drones that can go through it in the same turn.
The default value is also **1**.

Some examples of the fields alongside their `metadata`:
- nb_drones: 42
- start_hub: start 0 0 [color=green]
- end_hub: goal 10 10 [color=red]
- hub: normal_hub 1 1
- hub: blocked_hub 2 -2 [color=black zone=blocked]
- hub: priority_hub 0 1 [zone=priority max_drones=4]
- hub: restricted_hub 4 4 [zone=restricted]
- connection: start-blocked
- connection: start-priority_hub [max_link_capacity=2]

Several map files are included in the repository, under the `maps` folder.

### Validate Map
As previously stated, the map must have at least one possible path between `start_hub` and `end_hub`.
To achieve this validation, a personal algorithm was developed.

Starting on the `start_hub`, all the connected `hubs` are verified and checked for a match between them and `end_hub`.
If there's a match, that path is added to a list holding all the possible, valid paths as well as the cost of the path.
If they're not, this new path found is added to a list to keep exploring it by getting the connected `hubs` of the last `hub` added.

There's one possible scenario where the `hub` is not the `end_hub` and yet the algorithm stops exploring it.
If the checked `hub` has the metadata `zone` type of **blocked**, then that path ends there.

By the end of the algorithm, all possible paths are explored and the valid ones are stored.
This cost of the path is simply the amount of turns it takes the `drones` to traverse the map from `start_hub` to `end_hub`.

The map is ordered by cost and the tie-breaker between paths with the same cost goes down to the number of `hubs` containing the `zone` type **priority**.

Initially, the solving-algorithm took into account all these possible paths and the `drones` would adapt the path chosen and explore several in a single simulation.
Unfortunately, after careful analytical consideration, the results presented when only the best, least expensive path was chosen as the solving path had much better results.


### Map Solving Algorithm
To solve the map yet another personal algorithm was developed, based on the constraints and limitations of the map and project.
It was planned and executed with a Turn-based movement flow.

The algorithm will run while there are `drones` that haven't reached the `end_hub`.
The current `drone` being simulated will take into all the previous `drones` already simulated in that turn.

First, the `connection` between the current `hub` and the target `hub` is analyzed.
If the number of current `drones` present in the `connection` is the same as the `max_link_capacity`, this `drone` skips this turn.
If not, the turn continues.

Secondly, the target `hub` is evaluated.
If the `hub` has the capacity to hold the current `drone`, the turn continues.
There is a special case in which the `hub` doesn't have the capacity for now, but a turn later it will. This is the case of the `hubs` with the `zone` type of **restricted**. If a `drone` is on the way to that `hub`, it arrives in the next turn. During the turn the `drone` will arrive, the following `drone` can start to move towards that `hub` and both `drones` won't find one another.
This is another benefit of just having one path to follow.
If any of these cases is detected, the `drone` skips the turn.

By the end of all these checks, the target `hub` is assigned to the `drone` and it simulates the move in that turn, updating all the `hubs` affected by the behaviour of this `drone`.

After cycling through all the `drones`, it is verified if they exist in the `end_hub`.
If they do, they're removed from the algorithm simulation.

Everytime a move is made by a `drone`, a message is stored. By the end of the turn, all the messages stored during that turn, are displayed in the terminal following a specific format detailed in the next section.
The movement itself is also stored for later graphical display. This also will be addressed later.

### Output Message Format
For each turn, a set of movements by the `drones` are made.
These are stored individually and, by the end of the turn, printed to the terminal.
Depending on the movement, there are two possible formats for these messages.

- The `drone` reached a `hub`: In this case the format is `drone_id-reached_hub`
- The drone is in the middle of a `connection`, in other words, it's target is a **restricted** `hub`: `drone_id-current_hub-target_hub`

Each event is separated by a whitespace, allowing for a cleaner analysis on each drone movement.

Short example:

- D1-waypoint2 D2-waypoint1

In this example, the `drone` identified with **D1** reached the `hub` **waypoint2** in the same turn as `drone` **D2** reached **waypoint1**

An example where a `drone` is in the middle of a `connection`:

- D9-conv_restricted8-conv_restricted9

`drone` **D9** is found between `hub` **conv_restricted8** and `hub` **conv_restricted9**


### Graphical Display
After the simulation is finished, a replay of the turns is displayed graphically for better visualization and understanding of the drone pathing.
For this to happen, the events stored previously in the simulation are now used.

The coordinates for both `hubs`, `connections` and `drones` are mapped to the graphical window space. Each `hub` will be presented with the `color` value specified in the map file.

For each turn, the `drones` that moved are updated and everything is redrawn each frame.
A simulation turn takes one second followed by a small pause of 0.1 seconds. This allows the viewer to digest the turn in question before the next one plays.

After all the events are done, the graphical render is finished and the window takes two seconds to close.

Each `hub` can have a specific symbol that marks them as a different `zone` than the **normal**. To help identify which zone is a specific `hub`, this icon is tinted with **green** for **priority** zones, **yellow** for **restricted** zones and, finally, **red** for **blocked zones**.
This information is displayed in a bottom panel.

There's also a panel in the top left corner displaying the current turn playing and the maximum amount of turns the simulation took.

### Project Structure

```text
.
├── assets
│   ├── Background.png
│   ├── Base.png
│   ├── Border.png
│   ├── Drone.png
│   ├── Highlight.png
│   ├── RainbowNode.png
│   ├── Shadow.png
│   └── Zone.png
├── main.py
├── Makefile
├── README.md
└── src
    ├── consts.py
    ├── __init__.py
    ├── manager.py
    ├── map
    │   ├── connection.py
    │   ├── drone.py
    │   ├── __init__.py
    │   ├── map_config.py
    │   ├── map.py
    │   ├── node.py
    │   └── zones.py
    ├── parser
    │   ├── __init__.py
    │   └── parser.py
    └── render
        └── renderer.py
```

The `maps` directory was removed from the tree above for the sake of clarity.
The tree for it:

```text
├── maps
│   ├── challenger
│   │   └── 01_the_impossible_dream.txt
│   ├── easy
│   │   ├── 01_linear_path.txt
│   │   ├── 02_simple_fork.txt
│   │   └── 03_basic_capacity.txt
│   ├── hard
│   │   ├── 01_maze_nightmare.txt
│   │   ├── 02_capacity_hell.txt
│   │   └── 03_ultimate_challenge.txt
│   ├── medium
│   │   ├── 01_dead_end_trap.txt
│   │   ├── 02_circular_loop.txt
│   │   └── 03_priority_puzzle.txt
│   └── README.md
```

## Resources

### Graph

- [*Graph Theory*](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)) - Explanation of what a graph is

### Algorithms

- [*Dijkstra Algorithm*](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) - Mentioned several times by my colleagues

### Graphical Rendering

- [*Pygame Documentation*](https://www.pygame.org/docs/) - Documents for the library used for graphical display

### Use of AI
No AI was used to develop and complete this project.