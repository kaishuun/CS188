# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, depthGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the depth and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = depthGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        ""
        #distance away from dots (manhattan Distance)
        foodloc = depthGameState.getFood().asList() + depthGameState.getCapsules()
        fooddist = []


        if not action == "Stop":
        #Gathers closest food and ranks it the highest
            for i in foodloc:
                dist = util.manhattanDistance(newPos,i)
                if not dist == 0:
                    #inverse distance for food
                    fooddist.append(1.0/dist)
                else:
                    #eats the food if close
                    fooddist.append(float("inf"))

            #Pacman never touches a ghost
            ghostpos = successorGameState.getGhostPositions()
            for i in ghostpos:
                distapart = util.manhattanDistance(newPos,i)
                if distapart <= 3:
                    return -float("inf")

            return max(fooddist) + scoreEvaluationFunction(depthGameState)
        #returns -inf if not moving
        return -float("inf")


def scoreEvaluationFunction(depthGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return depthGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the depth gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
            [North, East, South West]

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
            possible actions: getScore() ect ect

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        #gathers the successors from the source and possible actions
        actions = gameState.getLegalActions(0)
        successors = []
        for i in actions:
            successors.append(gameState.generateSuccessor(0,i))
        #sets the best action as 0 and the max value as -infinity
        maxutil = -float("inf")
        best = 0

        #chooses and stoes the best action
        for i in range(len(successors)):
            val = self.value(successors[i],1,0)
            if val > maxutil:
                maxutil = val
                best = i

        return actions[best]


    def value(self,gameState,agent,depth):
        #returns value if at a leaf
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        #if at a player agent, goes to max
        elif agent == 0:
            return self.maxvalue(gameState,agent,depth)
        #if at a AI agent, goes to min
        elif agent > 0:
            return self.minvalue(gameState,agent,depth)

    def maxvalue(self,gameState,agent,depth):
        #sets the value to be -infinity
        v = -float("inf")

        #gathers the next state data
        actions = gameState.getLegalActions(agent)
        successors = []
        for i in actions:
            successors.append(gameState.generateSuccessor(agent,i))

        #finds the max value for each state
        for i in successors:
            v = max(v,self.value(i,1,depth))
        return v;

    def minvalue(self,gameState,agent,depth):
        #sets value to infinity
        v = float("inf")

        #gathers the successors
        actions = gameState.getLegalActions(agent)
        successors = []
        for i in actions:
            successors.append(gameState.generateSuccessor(agent,i))

        #gathers the value for each successor
        for i in successors:
            if agent+1 == gameState.getNumAgents():
                v = min(v,self.value(i,0,depth +1))
            elif not agent == 0:
                v = min(v,self.value(i,agent + 1,depth))
        return v



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #gathers all actions and successors of the first node
        actions = gameState.getLegalActions(0)
        successors = []
        for i in actions:
            successors.append(gameState.generateSuccessor(0,i))

        #sets variables
        maxutil = -float("inf")
        best = 0
        alpha = -float("inf")
        beta = float("inf")

        #finds the best choice by pruning
        for i in range(len(successors)):
            val = self.value(successors[i],1,0,alpha,beta)
            if val > maxutil:
                maxutil = val
                best = i
            alpha = max(alpha,maxutil)

        return actions[best]


    def value(self,gameState,agent,depth,alpha,beta):
        #evaluates util at nodes
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        #runs max if player turn
        elif agent == 0:
            return self.maxvalue(gameState,agent,depth,alpha,beta)
        #runs min if AI turn
        elif agent > 0:
            return self.minvalue(gameState,agent,depth,alpha,beta)

    def maxvalue(self,gameState,agent,depth,alpha,beta):
        #sets the value to be -infinity
        v = -float("inf")

        #gathers the next state data
        actions = gameState.getLegalActions(agent)

        #finds the max value for each state
        for i in actions:
            state = gameState.generateSuccessor(agent,i)
            v = max(v,self.value(state,1,depth,alpha,beta))

            if v > beta:
                return v
            alpha = max(alpha,v)
        return v

    def minvalue(self,gameState,agent,depth,alpha,beta):
        #sets value to infinity
        v = float("inf")

        #gathers the Actions
        actions = gameState.getLegalActions(agent)
        for i in actions:
            state = gameState.generateSuccessor(agent,i)

            if agent+1 == gameState.getNumAgents():
                v = min(v,self.value(state,0,depth +1,alpha,beta))
            elif not agent == 0:
                v = min(v,self.value(state,agent + 1,depth,alpha,beta))

            if v < alpha:
                return v
            beta = min(beta,v)
        return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        #gets all successors and actions from the first node
        actions = gameState.getLegalActions(0)
        successors = []
        for i in actions:
            successors.append(gameState.generateSuccessor(0,i))

        maxutil = -float("inf")
        best = 0
        #find the max value
        for i in range(len(successors)):
            val = self.value(successors[i],1,0)
            if val > maxutil:
                maxutil = val
                best = i

        return actions[best]


    def value(self,gameState,agent,depth):
        #returns the util for each leaf
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        #runs the max eval if player
        elif agent == 0:
            return self.maxvalue(gameState,agent,depth)
        #finds the expected value of the agents
        elif agent > 0:
            return self.expvalue(gameState,agent,depth)

    def maxvalue(self,gameState,agent,depth):
        #sets the value to be -infinity
        v = -float("inf")

        #gathers the next state data
        actions = gameState.getLegalActions(agent)

        #finds the max value for each state
        for i in actions:
            v = max(v,self.value(gameState.generateSuccessor(agent,i),1,depth))
        return v;

    def expvalue(self,gameState,agent,depth):
        #sets expected value to 0
        v = 0.0

        #gathers the successors and calculates the uniform probability
        actions = gameState.getLegalActions(agent)
        p = 1.0/len(actions)
        #calculates the expecation sum x*p(x)
        for i in actions:
            if agent+1 == gameState.getNumAgents():
                v = v + self.value(gameState.generateSuccessor(agent,i),0,depth +1)*p
            elif not agent == 0:
                v = v + self.value(gameState.generateSuccessor(agent,i),agent + 1,depth)*p
        return v

def betterEvaluationFunction(depthGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Returns the higher points for the closest food + game score
                    if it is near a ghost not on the timer, it will avoid
                    if it is near a ghost on the timer, it will eat it
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    newPos = depthGameState.getPacmanPosition()
    newFood = depthGameState.getFood()
    newGhostStates = depthGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]



    foodloc = depthGameState.getFood().asList()
    fooddist = [0.0]

    #Ranks food distance from nearest to farthest, pacman eats the food if it is near
    for i in foodloc:
        dist = util.manhattanDistance(newPos,i)
        if not dist < 1:
            fooddist.append(1.0/dist)
        else:
            fooddist.append(30)

    #Never move towards ghost if ghost is hunting
    #Eats ghost if ghost is edible
    ghostpos = depthGameState.getGhostPositions()
    for i in range(len(ghostpos)):
        if ghostpos[i] == newPos and newScaredTimes[i] == 0:
            return -float("inf")
        elif ghostpos[i] == newPos and newScaredTimes[i] > 0:
            return float("inf")
    #puts a heavier weight on food location
    return 10*max(fooddist)+5*depthGameState.getScore()

# Abbreviation
better = betterEvaluationFunction
