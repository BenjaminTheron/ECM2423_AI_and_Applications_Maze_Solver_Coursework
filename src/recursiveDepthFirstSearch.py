""" Solves a maze using a recursive depth first search algorithm """
import time


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

    # Stores the path taken through the maze via a recursive DFS algorithm
    # In addition to the number of nodes explored by the algorithm
    startTime = time.time()
    mazePathRecursiveDFS = recursiveDFS(mazeDictionary,
                                        startPoint, goalPoint, [])
    endTime = time.time()

    nodesExpanded = len(mazePathRecursiveDFS)
    mazePathRecursiveDFS = list(dict.fromkeys(mazePathRecursiveDFS))

    # Converts the path taken into a more readable string, with arrows between
    # the points
    mazePathString = ''
    for item in mazePathRecursiveDFS:
        if item == goalPoint:
            mazePathString += str(goalPoint)
            break
        else:
            mazePathString += str(item) + " -> "

    # Prints out all the algorithm's performance statistics
    # Finds the difference between the time at the start and end of the search
    # and rounds it to five decimal places
    performanceStatistics(len(mazePathRecursiveDFS),
                          nodesExpanded,
                          round(endTime - startTime, 5),
                          mazePathString
                          )


def recursiveDFS(mazeDictionary, startPoint, goalPoint, pathTaken):
    """ Executes a recursive depth first search on the provided maze and
    returns the path taken by the algorithm from the start to the goal node.
    """
    # Breaks the starting point down into a (x,y) coordinate
    (currentRow, currentColumn) = startPoint
    # If the node currently being looked at is the final one, return the path
    # taken through the maze
    if startPoint == goalPoint:
        pathTaken.append(startPoint)
        return pathTaken

    # Stores the list of possible next nodes in a list
    # At most four ways you can go from the current node (left, down, right or
    # up). ASSUMES each maze has a wall, so bounds checking only needs to be
    # done when looking at the first node
    nextNodes = [
        (currentRow, currentColumn - 1),
        (currentRow + 1, currentColumn),
        (currentRow, currentColumn + 1),
        (currentRow - 1, currentColumn)
    ]

    for (row, column) in nextNodes:
        # Only explore the next node if it is a path
        if row >= 0 and column >= 0 and mazeDictionary[(row, column)] == '-':
            # If the next node hasn't been visited yet, continue as normal,
            # Otherwise move on to the next node
            if (row, column) not in pathTaken:
                pathTaken.append(startPoint)
                # Adds the node to the path of visited nodes
                recursiveDFS(mazeDictionary,
                             (row, column), goalPoint, pathTaken)

    # If the current node is a dead end, back track up the maze until another
    # node can be explored
    return pathTaken


def performanceStatistics(numSteps, numNodes, timeTaken, fullPath):
    """ Outputs the performance statistics for a given algorithm, including
    the number of steps the algorithm takes, the number of nodes it explores
    The time it takes to execute and the full path from start to finish.
    """
    print("The full path taken by the algorithm is:         \n" + fullPath)
    print("The number of steps in the path taken:             ", numSteps)
    print("The number of nodes explored by the algorithm was: ", numNodes)
    print("The time taken to solve the maze was:              ", timeTaken,
          " seconds")


if __name__ == '__main__':
    mazeFileName = str(input(
        "Enter the filename of the maze you would like solved: "))
    mazeSolver("../docs/mazes/" + mazeFileName)
