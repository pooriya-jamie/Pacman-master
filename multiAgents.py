from game import Directions
import random
import util
from pacman import GameState
from searchAgents import evaluationFunction
import numpy as np
from searchAgents import scoreEvaluationFunction
from game import Agent

def minDistanceBfs(currentGameState: GameState):
    walls = currentGameState.getWalls()
    height = 0
    for _ in walls:
        height += 1
    width = 0
    for _ in walls[0]:
        width += 1

    start_position = currentGameState.getPacmanPosition()
    visited = set()
    queue = util.Queue()
    queue.push([start_position, 0])
    while not queue.isEmpty():
        sposition = queue.pop()
        x, y = sposition[0]
        if currentGameState.hasFood(x, y):
            return sposition[1]
        if sposition[0] in visited:
            continue
        visited.add(sposition[0])
        for i in range(0, 4):
            x, y = sposition[0]
            # up
            if not walls[x - 1][y] and x > 0:
                queue.push([(x - 1, y), sposition[1] + 1])
            if not walls[x + 1][y] and x < height:
                queue.push([(x + 1, y), sposition[1] + 1])
            if not walls[x][y - 1] and y > 0:
                queue.push([(x, y - 1), sposition[1] + 1])
            if not walls[x][y + 1] and y < width:
                queue.push([(x, y + 1), sposition[1] + 1])
        # print("Exploring position:", sposition[0], "with distance:", sposition[1])  
    return float('inf')  # If no food found

def betterEvaluationFunction(gameState):
    # Extract useful information from the game state
    pacmanPosition = gameState.getPacmanPosition()
    foodGrid = gameState.getFood()
    remainingFood = foodGrid.asList()
    ghostStates = gameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    score = gameState.getScore()
    capsules = gameState.getCapsules()

    # Calculate the evaluation score
    evaluationScore = 0
    evaluationScore += score / 4  # Add the current score
    evaluationScore += 10 / minDistanceBfs(gameState)  # Subtract the distance to the nearest food
    evaluationScore -= 10 * len(remainingFood)  # Subtract a penalty based on the number of remaining food pellets

    # Add a bonus for power pellets
    powerPelletBonus = 60 * len(capsules)
    evaluationScore -= powerPelletBonus

    # Add a bonus for eating scared ghosts
    for ghostState, scaredTime in zip(ghostStates, scaredTimes):
        if scaredTime > 0 and pacmanPosition == ghostState.getPosition():
            evaluationScore -= 300

    return evaluationScore


class MinimaxAgent(Agent):

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = betterEvaluationFunction
        self.depth = int(depth)

    def minimax(self, gameState: GameState, depth, agentIndex):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maxValue(gameState, depth)
        else:
            return self.minValue(gameState, depth, agentIndex)

    def maxValue(self, gameState: GameState, depth):
        v = float('-inf')
        actions = gameState.getLegalActions(0)  # Pacman's actions
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            v = max(v, self.minimax(successor, depth, 1))  # Call minimax for the first ghost agent
        return v

    def minValue(self, gameState: GameState, depth, agentIndex):
        v = float('inf')
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == gameState.getNumAgents() - 1:
                v = min(v, self.minimax(successor, depth - 1, 0))  # Call minimax for the next depth and Pacman
            else:
                v = min(v, self.minimax(successor, depth, agentIndex + 1))  # Call minimax for the next agent
        return v

    def getAction(self, gameState: GameState):
        actions = gameState.getLegalActions(0)  # Pacman's actions
        bestAction = None
        bestValue = float('-inf')
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            value = self.minimax(successor, self.depth, 1)  # Call minimax for the first ghost agent
            if value > bestValue:
                bestValue = value
                bestAction = action
        return bestAction