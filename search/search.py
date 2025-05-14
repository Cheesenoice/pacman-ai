# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    from util import Stack
    stack = Stack()
    visited = set()
    stack.push((problem.getStartState(), []))
    
    while not stack.isEmpty():
        state, actions = stack.pop()
        if state in visited:
            continue
        if problem.isGoalState(state):
            return actions
        visited.add(state)
        for next_state, action, cost in problem.getSuccessors(state):
            if next_state not in visited:
                stack.push((next_state, actions + [action]))
    return []

def breadthFirstSearch(problem):
    from util import Queue
    queue = Queue()
    visited = set()
    queue.push((problem.getStartState(), []))
    
    while not queue.isEmpty():
        state, actions = queue.pop()
        if state in visited:
            continue
        if problem.isGoalState(state):
            return actions
        visited.add(state)
        for next_state, action, cost in problem.getSuccessors(state):
            if next_state not in visited:
                queue.push((next_state, actions + [action]))
    return []


def uniformCostSearch(problem):
    from util import PriorityQueue
    pq = PriorityQueue()
    visited = set()
    pq.push((problem.getStartState(), [], 0), 0)
    
    while not pq.isEmpty():
        state, actions, cost = pq.pop()
        if state in visited:
            continue
        if problem.isGoalState(state):
            return actions
        visited.add(state)
        for next_state, action, step_cost in problem.getSuccessors(state):
            if next_state not in visited:
                new_cost = cost + step_cost
                pq.push((next_state, actions + [action], new_cost), new_cost)
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


# In both pratical task and Assignment 1
def aStarSearch(problem, heuristic=nullHeuristic):
    from util import PriorityQueue
    pq = PriorityQueue()
    visited = set()
    start_state = problem.getStartState()
    pq.push((start_state, [], 0), heuristic(start_state, problem))
    
    while not pq.isEmpty():
        state, actions, cost = pq.pop()
        if state in visited:
            continue
        if problem.isGoalState(state):
            return actions
        visited.add(state)
        for next_state, action, step_cost in problem.getSuccessors(state):
            if next_state not in visited:
                new_cost = cost + step_cost
                priority = new_cost + heuristic(next_state, problem)
                pq.push((next_state, actions + [action], new_cost), priority)
    return []


# Extensions Assignment 1
def iterativeDeepeningSearch(problem):
    """Search the deepest node in an iterative manner."""

    class SearchNode:
        """
            Creates node: <state, action, depth, parent_node>
        """
        def __init__(self, state, action=None, depth = 0, parent=None):
            self.state = state
            self.action = action
            self.parent = parent
            if parent:
                self.depth = depth + parent.depth
            else:
                self.depth = depth

        def extract_solution(self):
            """ Gets complete path from initial state to goal state """
            action_path = []
            search_node = self
            while search_node:
                if search_node.action:
                    action_path.append(search_node.action)
                search_node = search_node.parent
            return list(reversed(action_path))

    # limit for IDS
    limit = 0

    # controlling infinite loop
    LOOP_COUNT = 0
    LOOP_LIMIT = 999999999

    # running iteratively
    # increasing limit until goal-state is found
    while True:

        # no solution hard limit check
        if LOOP_COUNT == LOOP_LIMIT:
            break

        node = SearchNode(problem.getStartState())

        # goal-test
        if problem.isGoalState(node.state):
            return node.extract_solution()

        frontier = util.Stack()     # LIFO stack
        explored = set()            # empty set
        frontier.push(node)

        # run until frontier is empty
        while not frontier.isEmpty():
            node = frontier.pop()  # choose the deepest node in frontier
            explored.add(node.state)

            # never expand branch farther than the limit
            if node.depth < limit:
                # expand node
                successors = problem.getSuccessors(node.state)

                for succ in successors:
                    # make-child-node
                    # path step cost is considered as depth
                    child_node = SearchNode(succ[0], succ[1], succ[2], node)
                    # child.STATE is not in explored
                    if child_node.state not in explored:
                        # GOAL-TEST done on generation
                        if problem.isGoalState(child_node.state):
                            return child_node.extract_solution()
                        frontier.push(child_node)

        # goal-state not found -> increase limit by 1
        limit += 1
        LOOP_COUNT += 1

    # no solution
    util.raiseNotDefined()


def enforcedHillClimbing(problem, heuristic=nullHeuristic):
    """
    Local search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call it.
    The heuristic function is "manhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second arguement (heuristic).
    """
    # class to represent SearchNode
    class SearchNode:
        """
            Creates node: <state, action, h(s), parent_node>
        """
        def __init__(self, state, action=None, h = None, parent=None):
            self.state = state
            self.action = action
            self.parent = parent
            self.h = h

        def extract_solution(self):
            """ Gets complete path from goal state to parent node """
            action_path = []
            search_node = self
            while search_node:
                if search_node.action:
                    action_path.append(search_node.action)
                search_node = search_node.parent
            return list(reversed(action_path))

    # make search node function
    def make_search_node(state, action = None, parent = None):
        h_value = heuristic(state, problem)
        return SearchNode(state, action, h_value, parent)

    # improve helper function
    def improve(node_to_improve):

        queue = util.Queue()  # FIFO queue
        queue.push(node_to_improve)
        closed = set()

        while not queue.isEmpty():
            node = queue.pop()  # pop-front
            if node.state not in closed:
                closed.add(node.state)

                if node.h < node_to_improve.h:
                    return node

                successors = problem.getSuccessors(node.state)
                for succ in successors:
                    new_node = make_search_node(succ[0], succ[1], node)
                    queue.push(new_node)
        # fail
        return None

    # main iterative loop
    node = make_search_node(problem.getStartState())
    while not problem.isGoalState(node.state):
        node = improve(node)

    if node:
        return node.extract_solution()
    else:
        # no solution
        util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
ehc = enforcedHillClimbing