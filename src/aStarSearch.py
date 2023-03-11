"""Solves a maze using the depth first search algorithm"""
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
    mazePathAStar = aStarSearch(mazeDictionary, startPoint, goalPoint)
    endTime2 = time.time()
    # print(mazePathIterativeDFS)
    print("Time taken: ", round(endTime2 - startTime2, 5))


def aStarSearch():
    """
    """


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