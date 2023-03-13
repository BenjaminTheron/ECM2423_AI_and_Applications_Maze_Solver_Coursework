""" Solves a maze using an iterative depth first search algorithm """
import time
from recursiveDepthFirstSearch import performanceStatistics


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

    # Getting the coordinates of the starting node
    startPoint = (0, int(mazeString[0].index('-')/2))

    # Iterates through each character on each line in the provided text file
    for line in mazeString:
        numDashes = line.count('-')
        # The goal node is the only node in the final row whose value is '-'
        if numDashes == 1 and row > 0:
            # Removes the spaces from the line (is always a multiple of two)
            # And gets the index of the end node
            goalPoint = (row, int(line.index('-')/2))

        for position in line:
            # Only storing values if they are a path or a wall
            if position == '#' or position == '-':
                mazeDictionary[(row, column)] = position
                column += 1

        # Moves down to the start of the next row
        column = 0
        row += 1

    filePointer.close()

    # Stores the path taken through the maze via an iterative DFS algorithm
    startTime = time.time()
    (mazePathIterativeDFS, nodesExpanded) = iterativeDFS(mazeDictionary,
                                                         startPoint,
                                                         goalPoint
                                                         )
    endTime = time.time()

    # Converts the path taken into a more readable string, with arrows between
    # the points
    mazePathString = ''
    for item in mazePathIterativeDFS:
        if item == goalPoint:
            mazePathString += str(goalPoint)
        else:
            mazePathString += str(item) + " -> "

    # Prints out all the algorithm's performance statistics
    # Finds the difference between the time at the start and end of the search
    # and rounds it to five decimal places
    performanceStatistics(len(mazePathIterativeDFS),
                          nodesExpanded,
                          round(endTime - startTime, 5),
                          mazePathString
                          )


def iterativeDFS(mazeDictionary, startPoint, goalPoint):
    """ Executes an iterative depth first search on the provided maze and
    returns the path taken by the algorithm from the start to the goal node.
    """
    nodesExpanded = 0
    # Tracks the path taken by the algorithm as a list
    pathTaken = []
    # Stores the nodes that have already been visited by the algorithm
    visitedNodes = set()
    # Stores the parent of each node as a dictionary
    parentDict = {}
    # Initialises the stack to be used by the algorithm
    dfsStack = [startPoint]

    # While there are still nodes to explore, search through the maze
    while (len(dfsStack) > 0):
        # Get the current node to look at (at the top of the stack)
        (currentRow, currentColumn) = dfsStack.pop()
        nodesExpanded += 1

        # If the goal node has been reached add it to the path taken
        if (currentRow, currentColumn) == goalPoint:
            pathTaken.append(goalPoint)

            # Backtracks to the start to get the path taken
            while (currentRow, currentColumn) != startPoint:
                pathTaken.append(parentDict[(currentRow, currentColumn)])
                (currentRow, currentColumn) = parentDict[(currentRow,
                                                          currentColumn)]

            # Returns the path taken (Reversed as moving from goal to start)
            return (list(reversed(pathTaken)), nodesExpanded)

        # Calculates each potential neighbouring node
        nextNodes = [
            (currentRow, currentColumn - 1),
            (currentRow + 1, currentColumn),
            (currentRow, currentColumn + 1),
            (currentRow - 1, currentColumn)
        ]

        for (row, column) in nextNodes:
            # Only explores the next node if it is a valid path
            if row >= 0 and column >= 0 and mazeDictionary[(row,
                                                            column)] == '-':
                if (row, column) not in visitedNodes:
                    visitedNodes.add((row, column))
                    dfsStack.append((row, column))
                    parentDict[(row, column)] = (currentRow, currentColumn)

    # If the current node being looked at is the goal node, return the stack
    return pathTaken


if __name__ == '__main__':
    mazeFileName = str(input(
        "Enter the filename of the maze you would like solved: "))
    mazeSolver("../docs/mazes/" + mazeFileName)
