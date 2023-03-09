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
    mazePath = recursiveDFS(mazeDictionary, startPoint, goalPoint, [])
    endTime = time.time()
    count = 0
    mazePathSet = set()
    pathString = ""
    while mazePath[count] != goalPoint:
        pathString += str(mazePath[count]) + " -> "
        mazePathSet.add(mazePath[count])
        
        if count%13 == 0 and count > 0:
            pathString += "\n"

        count += 1

    pathString += str(goalPoint)
    mazePathSet.add(goalPoint)
    print(goalPoint)

    # The number of steps in the resulting path is the length of the returned path
    print("The number of steps in the path taken:             ", count + 1)

    # The number of nodes explored is the same as the length of the returned path
    print("The number of nodes explored by the algorithm was: ", len(mazePathSet))

    # Outputs the time taken by the algorithm to solve the maze
    print("The time taken to solve the maze was:              ", round(endTime - startTime, 5), " seconds")

    # The total number of steps taken by the algorithm



    # The path taken by the algorithm
    print("The full path taken by the algorithm is: \n" + pathString)


def recursiveDFS(mazeDictionary, startPoint, goalPoint, pathTaken):
    """ Executes the depth first search algorithm on a provided maze and
    returns the path taken by the algorithm.
    """
    global totalSteps
    # Breaks the starting point down into a (x,y) coordinate
    (currentRow, currentColumn) = startPoint
    # If the node currently being looked at is the final one, return the path
    # taken through the maze
    if startPoint == goalPoint:
        pathTaken.append(startPoint)
        return pathTaken

    # Stores the list of possible next nodes in a list
    # At most four ways you can go from the current node (left, down, right or up)
    # ASSUMES each maze has a wall, so bounds checking only needs to be done when
    # looking at the first node
    nextNodes = [
        (currentRow, currentColumn - 1),
        (currentRow + 1, currentColumn),
        (currentRow, currentColumn + 1),
        (currentRow - 1, currentColumn)
    ]

    for (row, column) in nextNodes:
        # Only explore the next node if it is a path
        if row >= 0 and column >= 0 and mazeDictionary[(row,column)] == '-':
            # If the next node hasn't been visited yet, continue as normal,
            # Other wise move on to the next node
            if (row,column) not in pathTaken:
                pathTaken.append(startPoint)
                print((row,column))
                print(pathTaken)
                time.sleep(5)
                # Adds the node to the path of visited nodes
                recursiveDFS(mazeDictionary, (row,column), goalPoint, pathTaken)
            
    # If the current node is a dead end, back track up the maze until another 
    # node can be explored
    return pathTaken


if __name__ == '__main__':
    mazeFileName = str(input("Enter the filename of the maze you would like solved: "))
    mazeSolver("../docs/mazes/" + mazeFileName)