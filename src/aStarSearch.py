"""Solves a maze using the A* search algorithm"""
import time
from priorityQueue import MazePriorityQueue

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
                mazeDictionary[(row,column)] = position
                column += 1

        # Moves down to the start of the next row
        column = 0
        row += 1
    
    filePointer.close()

    startTime = time.time()
    # Stores the path taken through the maze via a recursive DFS algorithm
    # mazePathRecursiveDFS = recursiveDFS(mazeDictionary, startPoint, goalPoint, [])
    # endTime = time.time()
    # count = 0
    # mazePathSet = set()
    # pathString = ""
    # while mazePathRecursiveDFS[count] != goalPoint:
    #     mazePathSet.add(mazePathRecursiveDFS[count])
    #     pathString += str(mazePathRecursiveDFS[count]) + " -> "

    #     if count%10 == 0 and count > 0:
    #         pathString += "\n"

    #     count += 1

    # pathString += str(goalPoint)
    # mazePathSet.add(goalPoint)
    #performanceStatistics(count+1, len(mazePathSet), round(endTime - startTime, 5), pathString)

    # Stores the path taken through the maze via an iterative DFS algorithm
    startTime2 = time.time()
    (mazePathAStar, nodesExpanded) = aStarSearch(mazeDictionary, startPoint, goalPoint)
    endTime2 = time.time()
    # print(mazePathIterativeDFS)
    print(mazePathAStar)
    print("Time taken: ", round(endTime2 - startTime2, 5))


def aStarSearch(mazeDictionary, startPoint, goalPoint):
    """ Executes an A* search on the provided maze and returns the path taken
    by the algorithm from the start to the goal node, along with the number of
    nodes that have been expanded by the algorithm.
    """
    nodesExpanded = 0
    frontier = MazePriorityQueue()
    frontier.insert((startPoint, heuristicCalculator(startPoint, goalPoint) + 1))
    visitedNodes = set()
    visitedNodes.add(startPoint)
    pathTaken = []
    parentDict = {}

    while frontier.isEmpty() == False:
        ((currentRow, currentColumn), currentCostFunction) = frontier.queuePop()
        nodesExpanded += 1

        if (currentRow, currentColumn) == goalPoint:
            pathTaken.append(goalPoint)
            # Backtracks to the start to get the path taken
            while (currentRow, currentColumn) != startPoint:
                pathTaken.append(parentDict[(currentRow, currentColumn)])
                (currentRow, currentColumn) = parentDict[(currentRow, currentColumn)]
            
            # Returns the path taken (Reversed as moving from goal to start)
            return (list(reversed(pathTaken)), nodesExpanded)
        
        visitedNodes.add((currentRow,currentColumn))

        nextNodes = [
            (currentRow, currentColumn - 1),
            (currentRow + 1, currentColumn),
            (currentRow, currentColumn + 1),
            (currentRow - 1, currentColumn)
        ]

        for (row, column) in nextNodes:
            # Only explores the next node if it is a path
            if row >= 0 and column >= 0 and mazeDictionary[(row,column)] == '-':

                if (row,column) not in visitedNodes and frontier.inQueue((row, column)) == False:
                    frontier.insert(((row,column), heuristicCalculator((row,column), goalPoint) + 1))
                    parentDict[(row,column)] = (currentRow, currentColumn)

                elif (row,column) not in visitedNodes and frontier.inQueue((currentRow, currentColumn)) == True:
                    frontier.changeNodeCost(((row, column), heuristicCalculator((row,column), goalPoint) + 1))

    return (None, nodesExpanded)


def heuristicCalculator(currentPosition, goalPoint):
    """ Calculates a heuristic value for the node provided, this is the
    Manhattan distance between the current position and the goal node.
    Other heuristics (Euclidiean and diagonal) are calculated for further
    experimentation.
    """
    (currentRow, currentColumn) = currentPosition
    (goalRow, goalColumn) = goalPoint

    dx = abs(goalRow - currentRow)
    dy = abs(goalColumn - goalColumn)

    return (10 * (dx + dy))


def performanceStatistics(numSteps, numNodes, timeTaken, fullPath):
    """ Outputs the performance statistics for a given algorithm, including
    the number of steps the algorithm takes, the number of nodes it explores
    The time it takes to execute and the full path from start to finish.
    """
    print("The number of steps in the path taken:             ", numSteps)
    print("The number of nodes explored by the algorithm was: ", numNodes)
    print("The time taken to solve the maze was:              ", timeTaken, " seconds")
    print("The full path taken by the algorithm is:         \n" + fullPath)


if __name__ == '__main__':
    mazeFileName = str(input("Enter the filename of the maze you would like solved: "))
    mazeSolver("../docs/mazes/" + mazeFileName)