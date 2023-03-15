"""A custom implementation of a priority queue"""
import math

class MazePriorityQueue():
    """
    """
    def __init__(self):
        self.priorityQ = {}


    def changeNodeCost(self, data):
        "Finds and returns the index of a (row,column) coordinate in the priority queue"
        ((currentRow, currentColumn), newCostFunction) = data
        if self.priorityQ[(currentRow, currentColumn)] < newCostFunction:
            self.priorityQ[(currentRow, currentColumn)] = newCostFunction


    def insert(self, data):
        ((row, column), cost) = data
        self.priorityQ[row,column] = cost


    def inQueue(self, data):
        (row, column) = data
        
        if (row, column) in self.priorityQ:
            return True
        else:
            return False


    def isEmpty(self):
        if len(self.priorityQ) == 0:
            return True
        else:
            return False


    def queuePop(self):
        lowestItem = next(iter(self.priorityQ))
        lowestCost = self.priorityQ[lowestItem]

        for item in self.priorityQ:
            if self.priorityQ[item] <= lowestCost:
                lowestItem = item
                lowestCost = self.priorityQ[item]

        nextNode = (lowestItem, self.priorityQ[lowestItem])
        del self.priorityQ[lowestItem]
        return nextNode
