class Node(object):
    parent = None
    state = None
    
    def __init__(self, state, parent=None):
        self.parent = parent
        self.state = state
        
    def __repr__(self):
        rep = ""
        node = self
        while node:
            rep = rep + "\n | \n" + str(node.state)
            node = node.parent
        return rep
                

class OchoProblem(object):
    initial = "312\n045\n678"
    
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
        

class BreadthFirstSearch(object):
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
                child = Node(child_state, node)
                if child.state not in explored or child.state not in [n.state for n in frontier]:
                    if self.problem.is_goal(child.state):
                        return child
                    frontier.append(child)


if __name__ == '__main__':
    problem = OchoProblem()
    # ~ s = problem.initial
    # ~ print(problem.actions(s))
    # ~ print(problem.result(s, "3"))

    print("Initial:")
    print(problem.initial)
    
    search = BreadthFirstSearch(problem)
    solution = search.run()

    print("Solution:")
    print(solution)
    
