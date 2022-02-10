import mdp, util
import sys

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() 
        self.runValueIteration()

    def runValueIteration(self):
        mdp = self.mdp
        discount = self.discount
        iterations = self.iterations

        

        for i in range(iterations):
          valuesK1 = self.values.copy()

          for state in mdp.getStates():
            Q_s = util.Counter()
            
            for action in mdp.getPossibleActions(state):
              Q_s[action] = self.computeQValueFromValues(state, action)
            
            valuesK1[state] = Q_s[Q_s.argMax()]

          self.values = valuesK1


    def getValue(self, state):
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        
        mdp = self.mdp
        values = self.values
        discount = self.discount
        T = mdp.getTransitionStatesAndProbs(state, action)
        T_R_gV = util.Counter() 

        for (nextState, prob) in T:
          R = mdp.getReward(state, action, nextState)
          T_R_gV[nextState] = prob * (R + discount * self.getValue(nextState))

        return T_R_gV.totalCount()


    def computeActionFromValues(self, state):
        mdp = self.mdp

        bestAction = None
        bestQ = float('-inf')

        for action in mdp.getPossibleActions(state):
          Q_s_a = self.computeQValueFromValues(state, action) 
          if Q_s_a > bestQ:
            bestQ = Q_s_a
            bestAction = action

        return bestAction



    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        iterCounter = 0

        while iterCounter < self.iterations:
          for state in self.mdp.getStates():
            Q_s = util.Counter()
            
            for action in self.mdp.getPossibleActions(state):
              Q_s[action] = self.computeQValueFromValues(state, action)
            
            self.values[state] = Q_s[Q_s.argMax()]
            
            iterCounter += 1
            if iterCounter >= self.iterations:
              return



class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):

        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):

        mdp = self.mdp
        values = self.values
        discount = self.discount
        iterations = self.iterations
        theta = self.theta
        states = mdp.getStates()


        predecessors = {} # dict
        for state in states:
          predecessors[state] = set()

        pq = util.PriorityQueue()

        for state in states:
          Q_s = util.Counter()

          for action in mdp.getPossibleActions(state):
            T = mdp.getTransitionStatesAndProbs(state, action)
            for (nextState, prob) in T:
              if prob != 0:
                predecessors[nextState].add(state)

            Q_s[action] = self.computeQValueFromValues(state, action)

          if not mdp.isTerminal(state):
            maxQ_s = Q_s[Q_s.argMax()]
            diff = abs(values[state] - maxQ_s)
            pq.update(state, -diff)


        for i in range(iterations):
          if pq.isEmpty():
            return

          state = pq.pop()

          if not mdp.isTerminal(state):
            Q_s = util.Counter()
            for action in mdp.getPossibleActions(state):
              Q_s[action] = self.computeQValueFromValues(state, action)

            values[state] = Q_s[Q_s.argMax()]

          for p in predecessors[state]:
            Q_p = util.Counter()
            for action in mdp.getPossibleActions(p):
              Q_p[action] = self.computeQValueFromValues(p, action)

            maxQ_p = Q_p[Q_p.argMax()]
            diff = abs(values[p] - maxQ_p)
              
            if diff > theta:
              pq.update(p, -diff)
