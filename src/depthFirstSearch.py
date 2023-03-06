"""Solves a maze using the depth first search algorithm"""

def mazeSolver(fileName):
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

    # Opens the desired maze file and stores its contents in a string
    filePointer = open(fileName, "r")
    mazeString = filePointer.readlines()

    # Iterates through each character on each line in the provided text file
    for line in mazeString:
        numDashes = line.count('-')
        # The goal the node is the only node in the final row whose value is '-'
        if numDashes == 1:
            goalRow = row

        for position in line:
            # Only storing values if they are a path or a wall
            if position == '#' or position == '-':
                mazeDictionary[(row,column)] = position
                column += 1

        column = 0
        row += 1
    
    filePointer.close()

    # Stores the path through the maze
    mazePath = dfs(mazeDictionary, goalRow)

    print(mazeDictionary)


def dfs(mazeDictionary):
    """ Executets the depth first search algorithm on a provided maze and
    returns the path taken by the algorithm.
    """

    for point in mazeDictionary:
        # Finds the starting point
        if point == '-':
            # Explore each branch as far as possible from left to right
            print()


if __name__ == '__main__':
    mazeFileName = str(input("Enter the filename of the maze you would like solved: "))
    mazeSolver("../docs/mazes/" + mazeFileName)