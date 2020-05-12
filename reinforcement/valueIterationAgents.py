# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #100 iterations
        #sets up v


        for i in range(self.iterations):
            #sets up v'
            values2 = util.Counter()

            #updates all states
            for state in self.mdp.getStates():
                actions = self.mdp.getPossibleActions(state)
                maxval = -float("inf")
                for act in actions:
                    qval = self.computeQValueFromValues(state,act)
                    if qval > maxval:
                        maxval = qval
                        #chooses max action for each update
                        values2[state] = maxval
            # v = v'
            self.values = values2






    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        #returns state value
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        #gathers the actions and probabilities
        #computes the expected value for taking each action
        next = self.mdp.getTransitionStatesAndProbs(state,action)
        value = 0
        for i in next:
            nextstate = i[0]
            prob = i[1]
            rewards = self.mdp.getReward(state,action,nextstate)
            value += prob*(rewards+self.discount*self.values[nextstate])

        return value


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        next = self.mdp.getPossibleActions(state)

        #no possible actions, returns none
        if len(next) == 0:
            return None

        #default best action value, and action
        best = -float('inf')
        action = None

        #chooses action with highest value
        for i in next:
            qval = self.computeQValueFromValues(state,i)
            if qval > best:
                action = i
                best = qval
        return action


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
