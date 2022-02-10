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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):

    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    graph = {}
    graphMini = {}
    currentNode = problem.getStartState()
    goal = currentNode

    def graphCreator(currentNode):
        hold = []
        if problem.getSuccessors(currentNode):
            graph[currentNode] = problem.getSuccessors(currentNode)
            for x in range(len(graph[currentNode])):
                hold.append(graph[currentNode][x][0])
            graphMini[currentNode] = hold
            for x in range(len(graph[currentNode])):
                if not graph[currentNode][x][0] in graph:
                    graphCreator(graph[currentNode][x][0])
        else:
            return

    graphCreator(problem.getStartState())

    for x in graphMini:
        if problem.isGoalState(x):
            goal = x
        hold = graphMini[x]
        for y in hold:
            if problem.isGoalState(y):
                goal = y

    print(graphMini)
    print(goal)
    print(problem.getStartState())

    if goal == problem.getStartState():
        return []

    listHold = []
    listAnswer = []
    listAnswer.append(goal)

    visited = set()

    def dfs(visited, graphMini, node):
        if node not in visited:
            listHold.append(node)
            visited.add(node)
            for neighbour in graphMini[node]:
                dfs(visited, graphMini, neighbour)

    dfs(visited, graphMini, goal)

    goalIndex = listHold.index(goal)
    while(True):
        hold = []
        hold = graphMini[listHold[goalIndex]]
        for x in range(1, goalIndex):
            if listHold[goalIndex-x] in hold:
                listAnswer.append(listHold[goalIndex-x])
                goalIndex = goalIndex-x
                break
        if(problem.getStartState() in hold):
            listAnswer.append(problem.getStartState())
            break
    listAnswer.reverse()
    print(listAnswer)

    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    directions = []
    for x in range(len(listAnswer)-1):
        if(listAnswer[x][0] - listAnswer[x+1][0] == 1):
            directions.append(w)
        if(listAnswer[x][0] - listAnswer[x+1][0] == -1):
            directions.append(e)
        if(listAnswer[x][1] - listAnswer[x+1][1] == 1):
            directions.append(s)
        if(listAnswer[x][1] - listAnswer[x+1][1] == -1):
            directions.append(n)

    return directions

    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visited = []
    hold = []
    queue = util.Queue()
    startNode = problem.getStartState()
    queue.push(startNode)
    visited.append(startNode)
    path = {}
    # problem.isGoalState(problem.getStartState()
    # problem.getSuccessors(problem.getStartState()

    def bfs(visited):
        while not queue.isEmpty():
            holdNode = queue.pop()
            if problem.isGoalState(holdNode):
                return holdNode
            hold = problem.getSuccessors(holdNode)
            path[holdNode] = hold
            for x in hold:
                if x[0] not in visited:
                    queue.push(x[0])
                    visited.append(x[0])

    hold = []
    goal = bfs(visited)

    def find(goal):
        holdRange = []
        for x in visited:
            if x in path:
                for holdList in path[x]:
                    if holdList[0] == goal:
                        holdRange.append(x)
                        goal = holdRange[0]
                        return (goal, holdList[1])

    while(goal != startNode):
        holdFind = find(goal)
        hold.append(holdFind[1])
        goal = holdFind[0]

    hold.reverse()
    return hold

    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    path = {}
    Queue = util.PriorityQueue()
    startNode = problem.getStartState()
    holdCost = {}
    holdCost[startNode] = []
    listCost = []
    Queue.push(startNode, 0)
    visited = []
    visited.append(startNode)

    # return []
    while(not Queue.isEmpty()):
        currentNode = Queue.pop()
        if problem.isGoalState(currentNode):
            break
        hold = problem.getSuccessors(currentNode)
        print(currentNode, " child for ", hold)
        if hold:
            for x in hold:
                if x[0] not in visited:
                    listCost = []
                    for i in holdCost[currentNode]:
                        listCost.append(i)
                    listCost.append(x[1])
                    if [] in listCost:
                        listCost.remove([])
                    holdCost[x[0]] = listCost
                    print("listCost", x[0], "=", listCost)
                    Queue.push(x[0], x[2]+problem.getCostOfActions(holdCost[x[0]]))
                    print("problem.getCostOfActions(holdCost[x[0]]) = ", problem.getCostOfActions(holdCost[x[0]]))
                    print("total cost = ",problem.getCostOfActions(holdCost[x[0]]))
                    path[currentNode] = x
                    visited.append(x[0])
        print()

    print(holdCost)
    return holdCost[currentNode]
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    Queue = util.PriorityQueue()
    startNode = problem.getStartState()
    cost = {}
    Queue.push(startNode,0)
    while not Queue.isEmpty():
        currentNode = Queue.pop()
        hold = problem.getSuccessors(currentNode)
        for x in hold :
            cost[x[0]]
    print(heuristic('S',problem))
    return[]
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
