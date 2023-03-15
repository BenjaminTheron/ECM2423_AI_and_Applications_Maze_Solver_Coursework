"""Solves a maze using the A* search algorithm"""
import time
import math
from priorityQueue import MazePriorityQueue
from iterativeDepthFirstSearch import performanceStatistics, mazeOutputToFile


def mazeSolver(fileName):
    """ Uses the A* search algorithm to solve a maze and prints out
    statistics about the algorithm's performance when solving the maze,
    including the number of nodes explored, the execution time and the
    number of steps in the path. ADD MORE METRICS.
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

    # Stores both the path taken and the number of nodes explored by the
    # algorithm
    startTime = time.time()
    (mazePathAStar, nodesExpanded) = aStarSearch(mazeDictionary,
                                                 startPoint, goalPoint)
    endTime = time.time()
    mazePathString = ''

    # Converts the path list into a string with arrows between each point
    # Allows the path to be printed in a more readable format
    for item in mazePathAStar:
        if item == goalPoint:
            mazePathString += str(goalPoint)
        else:
            mazePathString += str(item) + " -> "

    # Prints out all the algorithm's performance statistics
    # Finds the difference between the time at the start and end of the search
    # and rounds it to five decimal places
    performanceStatistics(len(mazePathAStar),
                          nodesExpanded,
                          round(endTime - startTime, 5),
                          mazePathString
                          )
    
    mazeOutputToFile(mazeDictionary, fileName, mazePathAStar)


def aStarSearch(mazeDictionary, startPoint, goalPoint):
    """ Executes an A* search on the provided maze and returns the path taken
    by the algorithm from the start to the goal node, along with the number of
    nodes that have been expanded by the algorithm.
    """
    nodesExpanded = 0
    # Initialises a new priority queue for the maze and places the starting
    # node in it
    frontier = MazePriorityQueue()
    frontier.insert((startPoint,
                     heuristicCalculator(startPoint, goalPoint)))
    # Using a set to store the visited nodes reduces the time complexity by
    # O(n) when compared to a list
    visitedNodes = set()
    # Tracks the path taken by the algorithm as a list
    pathTaken = []
    # Stores the parent of each node in a dictionary
    parentDict = {}

    nodeCost = {}
    nodeFunctionCost = {}
    for item in mazeDictionary:
        if mazeDictionary[item] == '-':
            nodeCost[item] = math.inf
            nodeFunctionCost[item] = math.inf
    
    nodeCost[startPoint] = 0
    nodeFunctionCost[startPoint] = heuristicCalculator(startPoint, goalPoint)

    # While there are still paths to explore, move through the maze
    while frontier.isEmpty() is False:
        # Breaks the current node into a coordinate and cost function
        ((currentRow, currentColumn),
         currentCostFunction) = frontier.queuePop()
        nodesExpanded += 1

        # If the goal node has been reached, add it to the path taken
        if (currentRow, currentColumn) == goalPoint:
            pathTaken.append(goalPoint)
            # Backtracks to the start to get the path taken
            while (currentRow, currentColumn) != startPoint:
                pathTaken.append(parentDict[(currentRow, currentColumn)])
                (currentRow, currentColumn) = parentDict[(currentRow,
                                                          currentColumn)]

            # Returns the path taken (Reversed as moving from goal to start)
            return (list(reversed(pathTaken)), nodesExpanded)

        # Adds the current node to the set of visited nodes
        visitedNodes.add((currentRow, currentColumn))

        # Calculates each potential neighbouring node
        nextNodes = [
            (currentRow - 1, currentColumn), # Up
            (currentRow, currentColumn + 1), # Right
            (currentRow + 1, currentColumn), # Down
            (currentRow, currentColumn - 1)  # Left
        ]

        for (row, column) in nextNodes:
            # Only explores the next node if it is a valid path
            interimNodeCost = nodeCost[(currentRow, currentColumn)] + 1
            if row >= 0 and column >= 0 and mazeDictionary[(row,
                                                            column)] == '-':
                # The neighbouring node is only visited if it isn't in the
                # frontier and hasn't been visited
                if (row, column) not in visitedNodes and frontier.inQueue(
                        (row, column)) is False:
                    # Adds the neighbouring node along with its cost function
                    # to the frontier
                    frontier.insert(((row, column),
                                    heuristicCalculator((row, column),
                                                        goalPoint) + interimNodeCost))
                    # Stores the parent of the neighbouring node as the
                    # current node
                    nodeFunctionCost[(row, column)] = heuristicCalculator((row, column),goalPoint) + interimNodeCost
                    nodeCost[(row, column)] = interimNodeCost
                    parentDict[(row, column)] = (currentRow, currentColumn)
            
                # If the neighbnouring node is already in the frontier (and
                # hasn't been visited) change the value of the cost function
                # if it is lower than what is already stored in the frontier
                elif (row, column) not in visitedNodes and frontier.inQueue(
                        (row, column)) is True:
                    # if nodeFunctionCost[]
                    nodeFunctionCost[(row, column)] = heuristicCalculator((row, column), goalPoint) + interimNodeCost
                    nodeCost[(row, column)] = interimNodeCost
                    frontier.changeNodeCost(((row, column),
                                            heuristicCalculator((row, column),
                                                                goalPoint)
                                            + interimNodeCost))
                    parentDict[(row, column)] = (currentRow, currentColumn)

    # If the whole maze is explored and the goal node isn't found
    # return an empty path
    return (None, nodesExpanded)


def heuristicCalculator(currentPosition, goalPoint):
    """ Calculates a heuristic value for the node provided, this is the
    Manhattan distance between the current position and the goal node.
    Other heuristics (Euclidean and diagonal) are calculated for further
    experimentation.
    """
    # Breaks the goal node and the current node into a (row,column) tuple
    (currentRow, currentColumn) = currentPosition
    (goalRow, goalColumn) = goalPoint

    # Finds the Manhattan distance between the current node and the goal node
    dx = abs(currentColumn - goalColumn)
    dy = abs(currentRow - goalRow)

    # Returns the sum multiplied by an arbitrary weight (1) - Manhattan
    return (1.2 * (dx + dy))

    # Finds the Euclidean distance between the current node and the goal node
    # dx = abs(currentColumn - goalColumn)
    # dy = abs(currentRow - goalRow)

    # # Returns the square root of the sum of the squares multiplied by some arbitrary weight (1) - Euclidean
    # return (2 * math.sqrt(dx * dx + dy * dy))

    # Finds the diagonal distance between the current node and the goal node
    # dx = abs(goalColumn - currentColumn)
    # dy = abs(goalRow - currentRow)

    # # Returns the weight times the sum plus the minimum cost of moving diagonally
    # return 1.2 * (dx + dy) + (1.2 - 2 * 1.2) * min(dx, dy)



if __name__ == '__main__':
    mazeFileName = str(input(
                    "Enter the filename of the maze you would like solved: "))
    mazeSolver("../docs/mazes/" + mazeFileName)
