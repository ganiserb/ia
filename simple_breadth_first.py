#!/usr/bin/env python3

class Node(object):
    """
    Represents a Node of the state space graph.
    Each node contains:
        a state representation.
        a link to its parent node (except for the initial, which is None).
        the action that was used to reach its state (exceptp for the initial
        which is None.
    """
    parent = None
    state = None
    action = None
    
    def __init__(self, state, parent=None, action=None):
        self.parent = parent
        self.state = state
        self.action = action
        
    def __repr__(self):
        """
        This method is used to draw a nice representation of the current
        Node and all its parents. It is invoked by python whenever you
        cast a Node instance to string.
        """
        # Build a list with the path to the solution
        nodes = []
        node = self
        while node:
            nodes.append(node)
            node = node.parent
            
        # Make a nice printable string out of that list
        representation = ""
        for node in reversed(nodes):
            if node:
                action = node.action if node and node.action and node.parent else " "
                representation = "{}\n | \n | ({}) \n v \n{}".format(representation, action, str(node.state))
        return representation


class BreadthFirstTreeSearch(object):
    """
    Implementation of the Breadth First algorithm as tree search.

    To use it, create an instance passing a problem instance as
    a paramenter.
    Call run() to find a solution or explode.
    """
    problem = None
    
    def __init__(self, problem):
        self.problem = problem
    
    def run(self):
        node = Node(self.problem.initial)
        if self.problem.is_goal(node.state):
            return node
        frontier = [node]

        while True:
            if not frontier:
                raise Exception("Empty frontier. Solution not found")

            node = frontier.pop(0)
            for action in self.problem.actions(node.state):
                child_state = self.problem.result(node.state, action)
                child = Node(child_state, node, action)
                if child.state not in [n.state for n in frontier]:
                    if self.problem.is_goal(child.state):
                        return child
                    frontier.append(child)


class BreadthFirstGraphSearch(object):
    """
    Implementation of the Breadth First algorithm as graph search.
    This is just TreeSearch, but with an "explored" set of states and
    checks in place to make sure no state is repeated.

    To use it, create an instance passing a problem instance as
    a paramenter.
    Call run() to find a solution or explode.
    """
    problem = None
    
    def __init__(self, problem):
        self.problem = problem
    
    def run(self):
        node = Node(self.problem.initial)
        if self.problem.is_goal(node.state):
            return node
        frontier = [node]
        explored = set()

        while True:
            if not frontier:
                raise Exception("Empty frontier. Solution not found")

            node = frontier.pop(0)
            explored.add(node.state)
            for action in self.problem.actions(node.state):
                child_state = self.problem.result(node.state, action)
                child = Node(child_state, node, action)
                if child.state not in explored or child.state not in [n.state for n in frontier]:
                    if self.problem.is_goal(child.state):
                        return child
                    frontier.append(child)


class OchoProblem(object):
    """
    Definition of the 8 puzzle problem.
    In this case the state is represented as a string in which
    each newline (\n) divides the different rows. Number 0 represents
    the blank sqare.

    The action is a string with the number that has to be swapped
    by the 0.
    """
    #initial = "312\n045\n678"
    initial = "312\n065\n748"
    
    def find_number(self, state, number):
        # Returns a tuple containing the row and column number of 0
        rows = state.split("\n")
        for row_number, row in enumerate(rows):
            for column_number, column in enumerate(row):
                if column == number:
                    return (row_number, column_number)
    
    def get_number(self, row, column, state):
        # Returns the number in the state at the given row and column
        lines = state.split("\n")
        return lines[row][column]
    
    def actions(self, state):
        # The action is the numnber that has to be interchanged for 0
        actions = []
        row, column = self.find_number(state, "0")
        if row < 2:
            # down
            actions.append(self.get_number(row + 1, column, state))
        if row > 0:
            # up
            actions.append(self.get_number(row - 1, column, state))
        if column < 2:
            # right
            actions.append(self.get_number(row, column + 1, state))
        if column > 0:
            # left
            actions.append(self.get_number(row, column - 1, state))
        
        return actions
        
    def is_goal(self, state):
        return state == "012\n345\n678"
        
    def result(self, state, action):
        a = state.replace("0", "x")
        b = a.replace(action, "0")
        c = b.replace("x", action)
        return c


if __name__ == '__main__':
    # Instantiate the problem definition
    problem = OchoProblem()

    # Print the initial state just to see it
    print("Initial:")
    print(problem.initial)

    # Instantiate the search algorithm
    search = BreadthFirstGraphSearch(problem)
    # Make it run to search for a solution
    solution = search.run()

    # Print the solution
    print("Solution:")
    print(solution)
    
