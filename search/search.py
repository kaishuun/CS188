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

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 20
"""
#
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
<Your feedback goes here>
I had a bit of trouble implementing DFS/BFS since I wasn't sure how to keep track of the nodes,
but otherwise everything else was straight forwards
"""
#####################################################
#####################################################

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
    """
    Q1.1
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print ( problem.getStartState() ) GETS THE STARTING STATE
    You will get (5,5)

    print (problem.isGoalState(problem.getStartState()) )
    You will get True


    print ( problem.getSuccessors(problem.getStartState()) )
    You will get [((x1,y1),'South',1),((x2,y2),'West',1)]
    """
    "*** YOUR CODE HERE ***"

    #CURRENT STATUS:
    #ALGORITHM: WORKING
    #LENGTH: WORKING

    #sets up explored list
    explored = []

    #gets the starting and current state, puts onto explored, and pushes the initial direction
    current = problem.getStartState()
    explored.append(current);

    frontier = util.Stack()
    frontier.push((current,[]))

    while not frontier.isEmpty():

        #gets the new node and the directions to that node
        current,directions = frontier.pop();

        #returns the path if it is at the goal state
        if problem.isGoalState(current):
            return directions

        #adds to explored set
        if not current in explored:
            explored.append(current)

        #gets the node's successors and adds their path and location to the fringe
        successors = problem.getSuccessors(current)
        for i in successors:
            if not i[0] in explored:
                result = directions + [i[1]]
                frontier.push((i[0],result))

    #returns fail if nothing found
    return -1



def breadthFirstSearch(problem):
    """
    Q1.2
    Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #sets up explored list
    explored = []

    #gets the starting and current state, puts onto explored, and pushes the initial direction
    current = problem.getStartState()
    explored.append(current);

    frontier = util.Queue()
    frontier.push((current,[]))

    while not frontier.isEmpty():

        #gets the new node and the directions to that node
        current,directions = frontier.pop();

        #returns the path if it is at the goal state
        if problem.isGoalState(current):
            return directions

        #gets the node's successors and adds their path and location to the fringe
        successors = problem.getSuccessors(current)
        for i in successors:
            if not i[0] in explored:
                explored.append(i[0])
                result = directions + [i[1]]
                frontier.push((i[0],result))

    #returns fail if nothing found
    return -1



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Q1.3
    Search the node that has the lowest combined cost and heuristic first."""
    """Call heuristic(s,problem) to get h(s) value."""
    "*** YOUR CODE HERE ***"

    #sets up explored list
    explored = []

    #gets the starting and current state, finds its fn value and pushes to fringe
    current = problem.getStartState()

    frontier = util.PriorityQueue()
    fn = heuristic(current, problem)
    frontier.push((current,[]),fn)

    while not frontier.isEmpty():

        #gets the new node and the directions to that node
        current,directions = frontier.pop();

        #returns the path if it is at the goal state
        if problem.isGoalState(current):
            return directions

        #gets the node's successors and adds their path and location to the fringe
        if not current in explored:
            successors = problem.getSuccessors(current)

            for i in successors:
                if not i[0] in explored:
                    result = directions + [i[1]]
                    fn = problem.getCostOfActions(result) + heuristic(i[0],problem)
                    frontier.push((i[0],result),fn)
        #adds to explored set
        explored.append(current)

    #returns fail if nothing found
    return -1

def priorityQueueDepthFirstSearch(problem):
    """
    Q1.4a.
    Reimplement DFS using a priority queue.
    """
    "*** YOUR CODE HERE ***"
    #sets up explored list
    explored = []

    #gets the starting and current state, puts onto explored, and pushes the initial direction
    current = problem.getStartState()
    explored.append(current);

    frontier = util.PriorityQueue()
    frontier.push((current,[]),-problem.getCostOfActions([]))

    while not frontier.isEmpty():

        #gets the new node and the directions to that node
        current,directions = frontier.pop();

        #returns the path if it is at the goal state
        if problem.isGoalState(current):
            return directions

        #adds to explored set
        if not current in explored:
            explored.append(current)

        #gets the node's successors and adds their path and location to the fringe
        successors = reversed(problem.getSuccessors(current))
        for i in successors:
            if not i[0] in explored:
                result = directions + [i[1]]
                frontier.push((i[0],result),-problem.getCostOfActions(result))

    #returns fail if nothing found
    return -1


def priorityQueueBreadthFirstSearch(problem):
    """
    Q1.4b.
    Reimplement BFS using a priority queue.
    """
    "*** YOUR CODE HERE ***"
    #sets up explored list
    explored = []

    #gets the starting and current state, puts onto explored, and pushes the initial direction
    current = problem.getStartState()
    explored.append(current)
    frontier = util.PriorityQueue()
    frontier.push((current,[]),problem.getCostOfActions([]))

    while not frontier.isEmpty():

        #gets the new node and the directions to that node
        current,directions = frontier.pop();

        #returns the path if it is at the goal state
        if problem.isGoalState(current):
            return directions

        #gets the node's successors and adds their path and location to the fringe
        successors = problem.getSuccessors(current)
        for i in successors:
            if not i[0] in explored:
                explored.append(i[0])
                result = directions + [i[1]]
                frontier.push((i[0],result),problem.getCostOfActions(result))

    #returns fail if nothing found
    return -1

#####################################################
#####################################################
# Discuss the results of comparing the priority-queue
# based implementations of BFS and DFS with your original
# implementations.

"""
The results from using a priority queue, were around the same as using the stack/queue,
one difference could be that the priority queue takes o(logn) for push/pop while the stack/Queue
takes o(1) time
"""



#####################################################
#####################################################



# Abbreviations (please DO NOT change these.)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
bfs2 = priorityQueueBreadthFirstSearch
dfs2 = priorityQueueDepthFirstSearch
