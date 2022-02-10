from util import manhattanDistance
from game import Directions
import random, util, sys

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

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()

        minDist = 999999
        for point in newFood:
            minDist = min(minDist, manhattanDistance(newPos, point))

        ghostDanger = 0
        for ghost in successorGameState.getGhostPositions():
            dist = max(4 - manhattanDistance(newPos, ghost), 0)
        ghostDanger += dist*dist

        return successorGameState.getScore() + 10.0/minDist - ghostDanger
		
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

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
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        agentCount = gameState.getNumAgents()

        def multiminimax(state, depth, agentIndex):
          legalActions = state.getLegalActions(agentIndex)
          if depth == 0 or len(legalActions) == 0:
            return (None, self.evaluationFunction(state))

          succAgentIndex = (agentIndex + 1) % agentCount
          succDepth = depth
          if succAgentIndex == 0: succDepth -= 1

          resultAction = None
          if agentIndex == 0:
            resultValue = float("-inf")
            for action in legalActions:
              succState = state.generateSuccessor(agentIndex, action)
              (_, succValue) = multiminimax(succState, succDepth, succAgentIndex) 
              if succValue > resultValue:
                (resultAction, resultValue) = (action, succValue)
          else:
            resultValue = float("inf")
            for action in legalActions:
              succState = state.generateSuccessor(agentIndex, action)
              (_, succValue) = multiminimax(succState, succDepth, succAgentIndex) 
              if succValue < resultValue:
                (resultAction, resultValue) = (action, succValue)

          return (resultAction, resultValue)

        result = multiminimax(gameState, self.depth, 0)
        return result[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        agentCount = gameState.getNumAgents()

        def multiminimax(state, depth, agentIndex, alpha, beta):
          legalActions = state.getLegalActions(agentIndex)
          if depth == 0 or len(legalActions) == 0:
            return (None, self.evaluationFunction(state))

          succAgentIndex = (agentIndex + 1) % agentCount
          succDepth = depth
          if succAgentIndex == 0: succDepth -= 1

          resultAction = None
          if agentIndex == 0:
            resultValue = float("-inf")
            for action in legalActions:
              succState = state.generateSuccessor(agentIndex, action)
              (_, succValue) = multiminimax(succState, succDepth, succAgentIndex, alpha, beta) 
              if succValue > resultValue:
                (resultAction, resultValue) = (action, succValue)
              if resultValue > beta: break
              alpha = max(alpha, resultValue)
          else:
            resultValue = float("inf")
            for action in legalActions:
              succState = state.generateSuccessor(agentIndex, action)
              (_, succValue) = multiminimax(succState, succDepth, succAgentIndex, alpha, beta) 
              if succValue < resultValue:
                (resultAction, resultValue) = (action, succValue)
              if resultValue < alpha: break
              beta = min(beta, resultValue)

          return (resultAction, resultValue)

        result = multiminimax(gameState, self.depth, 0, float("-inf"), float("inf"))
        return result[0]

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
        agentCount = gameState.getNumAgents()
        def multiminimax(state, depth, agentIndex):
          legalActions = state.getLegalActions(agentIndex)
          if depth == 0 or len(legalActions) == 0:
            return (None, self.evaluationFunction(state))

          succAgentIndex = (agentIndex + 1) % agentCount
          succDepth = depth
          if succAgentIndex == 0: succDepth -= 1

          resultAction = None
          if agentIndex == 0:
            resultValue = float("-inf")
            for action in legalActions:
              succState = state.generateSuccessor(agentIndex, action)
              (_, succValue) = multiminimax(succState, succDepth, succAgentIndex) 
              if succValue > resultValue:
                (resultAction, resultValue) = (action, succValue)
          else:
            resultValue = 0
            for action in legalActions:
              succState = state.generateSuccessor(agentIndex, action)
              (_, succValue) = multiminimax(succState, succDepth, succAgentIndex) 
              resultValue += succValue
            resultValue /= float(len(legalActions))

          return (resultAction, resultValue)

        result = multiminimax(gameState, self.depth, 0)
        return result[0]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Our heuristic works as follows, maximize score by running 
      away from ghosts and getting as close as possible to the minimum food 
      pellot at each state. To solve the pickle of being stuck between two food pellots
      (0   *Pacman*     0) we add an incrementing counter to the manhattanDistance
      between our agent's position and the distance to the food. We also add
      incentive for eating capsules if the capsule is closer than the ghost.
      Our heuristic averages ~1100 points.
    """
    # Useful information you can extract from a GameState (pacman.py)
    currPos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    score = currentGameState.getScore()
    
    if currentGameState.isWin(): return sys.maxsize
    if currentGameState.isLose(): return -sys.maxsize

    # Ghost distances
    minGhostDist = float("inf")
    ghostDists = []
    min
    for ghost in ghostStates:
        ghostDists.append(util.manhattanDistance(ghost.getPosition(), currPos))
    if len(ghostDists) > 0:
        minGhostDist = min(ghostDists)

    # Food score
    minFoodDist = float("inf")
    foodDists = []
    i = 0
    for food in foodList:
        foodDists.append(util.manhattanDistance(currPos, food) + i)
        i += 1
    if len(foodDists) > 0:
        minFoodDist = min(foodDists)
        
    # Capsules
    capsules = currentGameState.getCapsules()
    capDists = []
    minCapDist = 0
    for cap in capsules:
        capDists.append(util.manhattanDistance(currPos, cap))
    if len(capDists) > 0:
        minCapDist = min(capDists)
        
    scared = 0
    for scare in scaredTimes:
        scared += scare
        
    if minGhostDist < 3 and minGhostDist > minCapDist and minCapDist != 0:
        return score + 1/(5*float(minCapDist)) - minFoodDist
    elif minGhostDist < 3:
        return score + 5*minGhostDist - minFoodDist
    else:
        return score - minFoodDist

# Abbreviation
better = betterEvaluationFunction
