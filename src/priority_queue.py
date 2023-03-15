"""A custom implementation of a priority queue"""


class MazePriorityQueue():
    """ A class that implements a custom priority queue (represented as a
    dictionary for efficiency - provides direct access to elements) along with
    a number of methods for performing operations on the queue, such as
    insert(), is_empty(), in_queue(), pop() and changing the cost value of a
    node.
    """
    def __init__(self):
        """ A basic constructor that initialises the priority queue as a
        dictionary
        """
        self.priority_queue = {}

    def change_node_cost(self, data: tuple[(int, int), float]) -> None:
        """ Finds the index of a (row, column) coordinate that is already in
        the queue, if the provided cost is lower than the cost that is already
        stored in the queue, it is changed to the new value.

        Args:
            data (tuple[(int, int), float]): A packaged tuple containing a
                coordinate along with an updated cost f(x) for it. Doing this
                makes transfering more data specific to a node much easier and
                makes it easier to compare the new f(x) with the old f(x).
        """
        # Breaks the provided data into a (point, cost) tuple
        ((current_row, current_column), new_cost_function) = data

        if self.priority_queue[(current_row,
                                current_column)] < new_cost_function:
            self.priority_queue[(current_row,
                                 current_column)] = new_cost_function

    def insert(self, data: tuple[(int, int), float]) -> None:
        """ Inserts the provided data into the priority queue.

        Args:
            data (tuple[(int, int), float]): A packaged tuple containing a
                coordinate along with it's f(x). This is done to make
                insertion much easier and more readable.
        """
        # Breaks the provided data into a (point, cost) tuple
        ((row, column), cost) = data
        # Adds a new key (point) value (cost) pair to the priority queue
        self.priority_queue[row, column] = cost

    def in_queue(self, data: tuple[int, int]) -> bool:
        """ Checks if the provided coordinate is in the priority queue

        Args:
            data (tuple[int, int]): A packaged tuple containing the row and
                column of the coordinate being checked. Allows for efficient
                validation.

        Returns:
            bool: (True, False). A simple boolean value to indicate the
                presence (or lack of) of a point in the queue.
        """
        # Breaks the provided data into a tuple of the coordinate
        (row, column) = data

        if (row, column) in self.priority_queue:
            return True

        return False

    def is_empty(self) -> bool:
        """ Checks if the priority queue is empty.

        Returns:
            bool: (True, False). A simple boolean value indicating whether the
                queue is empty of not.
        """
        if len(self.priority_queue) == 0:
            return True

        return False

    def queue_pop(self) -> tuple[(int, int), float]:
        """ Returns and removes the element in the priority queue with the
        highest priority (lowest f(x)).

        Returns:
            tuple[(int, int), float]: (next_node). A packaged tuple containing
                the f(x) and (row, column) coordinates of the next node to be
                explored by the algorithm.
        """
        # Initialises the lowest cost/ point as the first item in the priority
        # queue
        lowest_item = next(iter(self.priority_queue))
        lowest_cost = self.priority_queue[lowest_item]

        # Loops through the entire priority queue until it has found the
        # coordinate with the lowest cost
        for item in self.priority_queue:
            if self.priority_queue[item] <= lowest_cost:
                lowest_item = item
                lowest_cost = self.priority_queue[item]

        # Packages the coordinates and respective cost to be returned into a
        # tuple and removes it from the priority queue before returning it
        next_node = (lowest_item, self.priority_queue[lowest_item])
        del self.priority_queue[lowest_item]
        return next_node
