# ECM2423_AI_and_Applications_Maze_Solver_Coursework

## Introduction
This project is intended to illustrate and show the performance of the depth first search algorithm along with
one other algorithm (A*) through a series of mazes.

## Prerequisites and Installation
Only built in modules and libraries were used in this project, so there are no prerequisites or installations
required to use the system.

## Project Tutorial
Four mazes were provided with the project, 'maze-Easy.txt', 'maze-Medium.txt', 'maze-Large.txt' and 'maze-VLarge.txt'.
Installing the project, moving to the src folder (cd to ECM2423_AI_Coursework/src or whatever the project folder is called/src)
of the project you can do the following:

  - Execute the A* search algorithm on a maze: Execute the command 'python3 a_star_search.py', then enter the exact
    filename of one of the four aforementioned mazes and press enter.

  - Execute the iterative DFS algorithm on a maze: Execute the command'python3 iterative_depth_first_search.py', then enter
    the exact filename of one of the four aforementioned mazes and press enter.

After execution, each algorithm will output the path taken, some performance metrics about the algorithm. Additionally,
by inspecting the file, maze\textunderscore path.txt, you can see a graphical representation of the path the algorithm
took through the maze (pressing ctrl-f or command-f and filtering by X will highlight the path and make it easier to see).

To add new mazes place to execute the algorithm on, place them into the docs folder in the project directory and follow the exact
steps provided above for the respective algorithm.

## Testing
No testing was required in the spec, and as I ran out of time, no testing was implemented.

### Notes
All functionality that was required by the specification was provided; however, there are a number of ways
in which the algorithms can be extended:

  - Add metrics to track the amount of memory consumed by the algorithm to track its space complexity.
  - Further optimise the algorithms and their operations to further reduce execution time.
  - Testing for the algorithms.

## Details

#### Authors
Benjamin Theron

#### License
MIT License
