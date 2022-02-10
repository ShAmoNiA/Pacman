from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)
        self.values = util.Counter()
    def getQValue(self, state, action):
        qValue = self.values[(state, action)]
        if qValue == 0:
          return 0.0
        else:
          return self.values[(state, action)]



    def computeValueFromQValues(self, state):
        legalActions = self.getLegalActions(state)
        maxValue = float("-inf")
        if len(legalActions) == 0:
          return 0.0
        else:
          for action in legalActions:
            if self.getQValue(state, action) > maxValue:
              maxValue = self.getQValue(state, action)
        return maxValue

    def computeActionFromQValues(self, state):
        # print "computeActionFromQValues"
        bestAction = None
        legalActions = self.getLegalActions(state)
        maxValue = float("-inf")
        if len(legalActions) == 0:
          return bestAction
        else: 
          for action in legalActions:

            if self.getQValue(state, action) > maxValue:
              bestAction = action
              maxValue = self.getQValue(state, action)
            elif self.getQValue(state, action) == maxValue:
              bestAction = random.choice([bestAction, action])
        return bestAction

    def getAction(self, state):
        legalActions = self.getLegalActions(state)
        action = None
        if len(legalActions) == 0:
          return action
        else: 
          boolean = util.flipCoin(self.epsilon)
          if boolean:
            action = random.choice(legalActions)
          else:
            action = self.computeActionFromQValues(state)
        return action

    def update(self, state, action, nextState, reward):
        qCurr = self.getQValue(state, action)
        qUpdated = (1 - self.alpha) * qCurr + self.alpha * (reward + self.discount * self.computeValueFromQValues(nextState))       
        self.values[(state, action)] = qUpdated
        

    def getPolicy(self, state):
      return self.computeActionFromQValues(state)

    def getValue(self, state):
      return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        features = self.featExtractor.getFeatures(state, action)
        weights = self.weights

        totalQValue = 0

        for feature in features.sortedKeys():
          w_value = weights[feature]
          f_value = features[feature]
          totalQValue += w_value * f_value

        return totalQValue

    def update(self, state, action, nextState, reward):
        features = self.featExtractor.getFeatures(state, action)
        difference = (reward + self.discount * self.computeValueFromQValues(nextState)) - self.getQValue(state, action)
        for feature in features.sortedKeys():       
          self.weights[feature] = self.weights[feature] + self.alpha * difference * features[feature]

    def final(self, state):
        PacmanQAgent.final(self, state)
