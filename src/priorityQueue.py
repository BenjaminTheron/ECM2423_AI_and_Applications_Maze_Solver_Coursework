"""A custom implementation of a priority queue"""
import math

class MazePriorityQueue():
    """"""
    def __init__(self):
        self.priorityQ = []

    def changeNodeCost(self, data):
        "Finds and returns the index of a (row,column) coordinate in the priority queue"
        ((currentRow, currentColumn), newCost) = data
        for item in self.priorityQ:
            ((row,column),cost) = item

            if (row, column) == (currentRow, currentColumn) and newCost < cost:
                self.priorityQ[self.priorityQ.index((row,column),cost)] = ((row,column), newCost)
    
    def setIndex(self, index, data):
        self.priorityQ[index] = data

    def insert(self, data):
        self.priorityQ.append(data)

    def inQueue(self, data):
        if data in self.priorityQ:
            return True
        else:
            return False

    def isEmpty(self):
        if len(self.priorityQ) == 0:
            return True
        else:
            return False
    
    def queuePop(self):
        lowestValue = 0

        # Remove the item with the lowest heuristic (distance to goal node)
        for i in range(len(self.priorityQ)):
            ((row, column), currentHeuristic) = self.priorityQ[i]
            (coordinates, lowestHeuristic) = self.priorityQ[lowestValue]
            if currentHeuristic < lowestHeuristic:
                lowestValue = i
        
        nextNode = self.priorityQ[lowestValue]
        del self.priorityQ[lowestValue]
        return nextNode
