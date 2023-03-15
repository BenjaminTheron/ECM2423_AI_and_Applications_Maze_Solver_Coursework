"""Solves a maze using the A* search algorithm"""
import time
import math
from priority_queue import MazePriorityQueue
from iterative_depth_first_search import performance_statistics
from iterative_depth_first_search import maze_output_to_file


def maze_solver(file_name: str) -> None:
    """ Uses the A* search algorithm to solve a maze and prints out
    statistics about the algorithm's performance when solving the maze,
    including the number of nodes explored, the execution time and the
    number of steps in the path.

    Args:
        file_name (str): The file name of the maze to be solved, provided as a
            string so that it can be used to open the maze file directly, with
            no error checking required.
    """
    # Track the column and row number of a given position
    row = 0
    column = 0
    # Stores the maze and maps each position to a wall/path value.
    maze_dictionary = {}

    # Opens the desired maze file and stores its contents in a string
    with open(file_name, "r", encoding="utf-8") as file_pointer:
        maze_string = file_pointer.readlines()

    # Getting the coordinates of the starting node
    start_point = (0, int(maze_string[0].index('-')/2))

    # Iterates through each character on each line in the provided text file
    for line in maze_string:
        num_dashes = line.count('-')
        # The goal node is the only node in the final row whose value is '-'
        if num_dashes == 1 and row > 0:
            # Removes the spaces from the line (is always a multiple of two)
            # And gets the index of the end node
            goal_point = (row, int(line.index('-')/2))

        for position in line:
            # Only storing values if they are a path or a wall
            if position in '#' or position in '-':
                maze_dictionary[(row, column)] = position
                column += 1

        # Moves down to the start of the next row
        column = 0
        row += 1

    # Stores both the path taken and the number of nodes explored by the
    # algorithm
    start_time = time.time()
    (maze_path_a_star,
     nodes_expanded) = a_star_search(maze_dictionary, start_point, goal_point)
    end_time = time.time()
    maze_path_string = ''

    # Converts the path list into a string with arrows between each point
    # Allows the path to be printed in a more readable format
    for item in maze_path_a_star:
        if item == goal_point:
            maze_path_string += str(goal_point)
        else:
            maze_path_string += str(item) + " -> "

    # Prints out all the algorithm's performance statistics
    # Finds the difference between the time at the start and end of the search
    # and rounds it to five decimal places
    performance_statistics(len(maze_path_a_star),
                           nodes_expanded,
                           round(end_time - start_time, 5),
                           maze_path_string
                           )

    # Outputs the algorithms path through the maze to the file mazePath.txt
    maze_output_to_file(maze_dictionary, file_name, maze_path_a_star)


def a_star_search(maze_dictionary: dict, start_point: tuple[int, int],
                  goal_point: tuple[int, int]) -> tuple[list[(int, int)], int]:
    """ Executes an A* search on the provided maze and returns the path taken
    by the algorithm from the start to the goal node, along with the number of
    nodes that have been expanded by the algorithm.

    Args:
        maze_dictionary (dict of (int, int): str): A mapping of each coordinate
            in the maze to a string representation of a wall or path. This
            simplifies the representation and makes accessing parts of the
            maze more efficient.
        start_point (tuple[int, int]): A coordinate (int, int) tuple indicating
            when the algorithm starts when solving the maze.
        goal_point (tuple[int, int]): A coordinate (int, int) tuple indicating
            when the algorithm ends when solving the maze.

    Returns:
        tuple[list[(int, int)], int]: (path_taken, nodes_expanded). A packaged
            tuple containing the number of nodes visited by the algorithm
            along with the path it took through the maze, as represented by
            a list of coordinates ((int, int) tuples). Doing this allows for
            multiple values to be returned in one go and simplifies the data
            collection process.
    """
    nodes_expanded = 0
    # Initialises a new priority queue for the maze and places the starting
    # node in it
    frontier = MazePriorityQueue()
    frontier.insert((start_point, heuristic_calculator(start_point,
                                                       goal_point)))
    visited_nodes = set()
    path_taken = []
    # Stores the parent of each node in a dictionary
    parent_dict = {}

    # Dictionaries to store the g(x) of a node (cost from the start to the
    # node) and the f(x) of a node (g(x) + h(x) (heuristic) of a node)
    node_cost = {}
    node_function_cost = {}
    # Initialises each cost and function cost to infinity
    for item in maze_dictionary:
        if maze_dictionary[item] == '-':
            node_cost[item] = math.inf
            node_function_cost[item] = math.inf

    # Adds the starting node along with it's cost and function cost to the
    # respective dictionaries
    node_cost[start_point] = 0
    node_function_cost[start_point] = heuristic_calculator(start_point,
                                                           goal_point)

    # While there are still paths to explore, move through the maze
    while frontier.is_empty() is False:
        # Breaks the current node into a coordinate and cost function
        ((current_row, current_column),
         current_cost_function) = frontier.queue_pop()
        nodes_expanded += 1

        # If the goal node has been reached, add it to the path taken
        if (current_row, current_column) == goal_point:
            path_taken.append(goal_point)
            # Backtracks to the start to get the path taken
            while (current_row, current_column) != start_point:
                path_taken.append(parent_dict[(current_row, current_column)])
                (current_row, current_column) = parent_dict[(current_row,
                                                             current_column)]

            # Returns the path taken (Reversed as moving from goal to start)
            return (list(reversed(path_taken)), nodes_expanded)

        visited_nodes.add((current_row, current_column))

        # Calculates each potential neighbouring node
        next_nodes = [
            (current_row - 1, current_column),  # Up
            (current_row, current_column + 1),  # Right
            (current_row + 1, current_column),  # Down
            (current_row, current_column - 1)   # Left
        ]

        for (row, column) in next_nodes:
            # Only explores the next node if it is a valid path
            # Finds the "pseudo" cost of the current node from the start node
            interimnode_cost = node_cost[(current_row, current_column)] + 1
            if row >= 0 and column >= 0 and maze_dictionary[(row,
                                                            column)] == '-':
                # The neighbouring node is only visited if it isn't in the
                # frontier and hasn't been visited
                if (row, column) not in visited_nodes and frontier.in_queue(
                        (row, column)) is False:
                    # Adds the neighbouring node along with its cost function
                    # to the frontier
                    frontier.insert(((row, column),
                                     heuristic_calculator((row, column),
                                                          goal_point)
                                    + interimnode_cost))
                    # Adds the f(x) and g(x) of the current node to the
                    # respective dictionaries
                    node_function_cost[(row, column)] = (heuristic_calculator(
                                                         (row, column),
                                                         goal_point)
                                                         + interimnode_cost)
                    node_cost[(row, column)] = interimnode_cost
                    # Stores the parent of the neighbouring node as the
                    # current node
                    parent_dict[(row, column)] = (current_row, current_column)

                # If the neighbnouring node is alread_y in the frontier (and
                # hasn't been visited) change the value of the cost function
                # if it is lower than what is alread_y stored in the frontier
                elif (row, column) not in visited_nodes and frontier.in_queue(
                        (row, column)) is True:
                    # Adds the f(x) and g(x) of the current node to the
                    # respective dictionaries
                    node_function_cost[(row, column)] = (heuristic_calculator(
                                                       (row, column),
                                                       goal_point)
                                                       + interimnode_cost)
                    node_cost[(row, column)] = interimnode_cost
                    frontier.change_node_cost(((row, column),
                                              heuristic_calculator((row,
                                                                    column),
                                                                   goal_point)
                                              + interimnode_cost))
                    # Stores the parent of the neighbouring node as the
                    # current node
                    parent_dict[(row, column)] = (current_row, current_column)

    # If the whole maze is explored and the goal node isn't found
    # return an empty path
    return (None, nodes_expanded)


def heuristic_calculator(current_position: tuple[int, int],
                         goal_point: tuple[int, int]) -> float:
    """ Calculates a heuristic value for the node provided, this is the
    Manhattan distance between the current position and the goal node.
    Other heuristics (Euclidean and diagonal) are calculated for further
    experimentation.

    Args:
        current_position (tuple[int, int]): A coordinate (int, int) tuple
            indicating the current position of the algorithm in the maze.
        goal_point (tuple[int, int]): A coordinate (int, int) tuple indicating
            when the algorithm ends when solving the maze.

    Returns:
        float: (1.2 * (d_x + d_y)). A float value representing the current
            position's distance from the goal node. This can be any one of
            three heuristic values (Manhattan, Euclidean, Diagonal), which
            also use an arbitrary weight to make them more efficient.
    """
    # Breaks the goal node and the current node into a (row,column) tuple
    (current_row, current_column) = current_position
    (goal_row, goal_column) = goal_point

    # Finds the Manhattan distance between the current node and the goal node
    d_x = abs(current_column - goal_column)
    d_y = abs(current_row - goal_row)

    # Returns the sum multiplied by an arbitrary weight (1) - Manhattan
    return 1.2 * (d_x + d_y)

    # Finds the Euclidean distance between the current node and the goal node
    # d_x = abs(current_column - goal_column)
    # d_y = abs(current_row - goal_row)

    # # Returns the square root of the sum of the squares multiplied by some
    # arbitrary weight (1) - Euclidean
    # return (2 * math.sqrt(d_x * d_x + d_y * d_y))

    # Finds the diagonal distance between the current node and the goal node
    # d_x = abs(goal_column - current_column)
    # d_y = abs(goal_row - current_row)

    # # Returns the weight times the sum plus the minimum cost of moving
    # diagonally
    # return 1.2 * (d_x + d_y) + (1.2 - 2 * 1.2) * min(d_x, d_y)


if __name__ == '__main__':
    MAZE_FILE_NAME = str(input(
                    "Enter the file_name of the maze you would like solved: "))
    maze_solver("../docs/mazes/" + MAZE_FILE_NAME)
