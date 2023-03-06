"""Implements the depth first search algorithm to solve a maze"""

def dfsMazeSolver(fileName):
    """ Uses the depth first search algorithm to solve a maze and prints out
    statistics about the algorithms performance solving the maze, incl the
    number of nodes explored, the execution time and the number of steps in
    the path. ADD MORE METRICS.
    """
    # Track the column and row number of a given position
    row = 0
    column = 0
    # Stores the maze and maps each position to a wall/path value.
    mazeDictionary = {}

    
    filePointer = open(fileName, "r")
    mazeString = filePointer.readlines()

    # Iterates through each character on each line in the provided text file
    for line in mazeString:
        for position in line:
            # Only storing values if they are a path or a wall
            if position == '#' or position == '-':
                mazeDictionary[(row,column)] = position
                row += 1

        row = 0
        column += 1
    
    filePointer.close()


if __name__ == '__main__':
    mazeFileName = str(input("Enter the filename of the maze you would like solved: "))
    dfsMazeSolver("../docs/mazes/" + mazeFileName)