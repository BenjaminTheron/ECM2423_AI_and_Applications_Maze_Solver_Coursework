""" Solves a maze using an iterative depth first search algorithm """
import time


def maze_solver(file_name: str) -> None:
    """ Uses the depth first search algorithm to solve a maze and prints out
    statistics about the algorithm's performance solving the maze, incl the
    number of nodes explored, the execution time and the number of steps in
    the path.

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

    # Stores the path taken through the maze, along with the number of nodes
    # Explored by the algorithm
    start_time = time.time()
    (maze_path_iterative_dfs, nodes_expanded) = iterative_dfs(maze_dictionary,
                                                              start_point,
                                                              goal_point
                                                              )
    end_time = time.time()

    # Converts the path taken into a more readable string, with arrows between
    # the points
    maze_path_string = ''
    for item in maze_path_iterative_dfs:
        if item == goal_point:
            maze_path_string += str(goal_point)
        else:
            maze_path_string += str(item) + " -> "

    # Prints out all the algorithm's performance statistics
    # Finds the difference between the time at the start and end of the search
    # and rounds it to five decimal places
    performance_statistics(len(maze_path_iterative_dfs),
                           nodes_expanded,
                           round(end_time - start_time, 5),
                           maze_path_string
                           )

    # Outputs the algorithms path through the maze to the file mazePath.txt
    maze_output_to_file(maze_dictionary, file_name, maze_path_iterative_dfs)


def iterative_dfs(maze_dictionary: dict,
                  start_point: tuple[int, int],
                  goal_point: tuple[int, int]
                  ) -> tuple[list[(int, int)], int]:
    """ Executes an iterative depth first search on the provided maze and
    returns the path taken by the algorithm from the start to the goal node.

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
    path_taken = []
    visited_nodes = set()
    # Stores the parent of each node as a dictionary
    parent_dict = {}
    # Initialises the stack to be used by the algorithm
    dfs_stack = [start_point]

    # While there are still nodes to explore, search through the maze
    while len(dfs_stack) > 0:
        # Get the current node to look at (at the top of the stack)
        (current_row, current_column) = dfs_stack.pop()
        nodes_expanded += 1

        # If the goal node has been reached add it to the path taken
        if (current_row, current_column) == goal_point:
            path_taken.append(goal_point)

            # Backtracks to the start to get the path taken
            while (current_row, current_column) != start_point:
                path_taken.append(parent_dict[(current_row, current_column)])
                (current_row, current_column) = parent_dict[(current_row,
                                                             current_column)]

            # Returns the path taken (Reversed as moving from goal to start)
            return (list(reversed(path_taken)), nodes_expanded)

        # Calculates each potential neighbouring node
        # As a stack is being used, the nodes need to be added in the reverse
        # order to which they are to be searched
        next_nodes = [
            (current_row - 1, current_column),  # Up
            (current_row, current_column + 1),  # Right
            (current_row + 1, current_column),  # Down
            (current_row, current_column - 1)   # Left
        ]

        for (row, column) in next_nodes:
            # Only explores the next node if it is a valid path
            if row >= 0 and column >= 0 and maze_dictionary[(row,
                                                            column)] == '-':
                if (row, column) not in visited_nodes:
                    visited_nodes.add((row, column))
                    dfs_stack.append((row, column))
                    parent_dict[(row, column)] = (current_row, current_column)

    # If the stack is empty, return the path so far
    return path_taken


def performance_statistics(num_steps: int, num_nodes: int, time_taken: float,
                           full_path: str) -> None:
    """ Outputs the performance statistics for a given algorithm, including
    the number of steps the algorithm takes, the number of nodes it explores,
    the time it takes to execute and the full path from start to finish.

    Args:
        num_steps (int): The total number of steps the algorithm takes to solve
            the maze, provided as an int for convenience.
        num_nodes (int): The total number of nodes the algorithm visited whilst
            solving the maze, provided as an int for convenience.
        time_taken (float): The time taken by the algorithm to solve the maze,
            provided as a float (most applicable) and rounded to five decimal
            places for readability.
        full_path (str): A string representation of path the algorithm took
            through the maze, done to improve readability and improve error
            checking.
    """
    print("The full path taken by the algorithm is:         \n" + full_path)
    print("The number of steps in the path taken:             ", num_steps)
    print("The number of nodes explored by the algorithm was: ", num_nodes)
    print("The time taken to solve the maze was:              ", time_taken,
          " seconds")


def maze_output_to_file(maze_dictionary: dict, file_name: str,
                        path_taken: list[(int, int)]) -> None:
    """ Outputs the path the algorithm took through the maze to a text file,
    named mazePath.txt, where the path is indicated with X's over the normal
    maze file.

    Args:
        maze_dictionary (dict of (int, int): str): A mapping of each coordinate
            in the maze to a string representation of a wall or path. This
            simplifies the representation and makes accessing parts of the
            maze more efficient.
        file_name (str): The file name of the maze that's been solved, provided
            as a string so that it can be used to open the maze file directly,
            with no error checking required.
        path_taken (list[(int, int)])): A list of the coordinates (tuple of int
            for convenience) that the algorithm passed through when solving
            the maze.
    """
    # Opens the file, reads its contents to a string and closes it
    with open(file_name, "r", encoding="utf-8") as maze_file:
        maze_string = maze_file.readlines()

    # Finds the total number of columns in the maze (excl spaces)
    num_columns = int(len(maze_string[0])/2) - 1
    maze_string_with_path = ""

    # Overwrite any coordinates that are in the dictionary and path taken and
    # set their value to X
    for (row, column) in path_taken:
        maze_dictionary[(row, column)] = "X"

    # Rewrites the maze as a string from the altered dictionary
    for (row, column) in maze_dictionary:
        maze_string_with_path += " " + maze_dictionary[(row, column)]

        if column == num_columns:
            maze_string_with_path += "\n"

    # Writes the string to the file mazePath.txt
    with open("maze_path.txt", "w", encoding="utf-8") as file_pointer:
        file_pointer.writelines(maze_string_with_path)


if __name__ == '__main__':
    MAZE_FILE_NAME = str(input(
        "Enter the file_name of the maze you would like solved: "))
    maze_solver("../docs/mazes/" + MAZE_FILE_NAME)
