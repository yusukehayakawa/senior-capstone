# from time import sleep
# import numpy as np
import agent
import time
import random
import sys
import math

class StandingOvationSimple:
  def __init__(self, N_Column, N_Row, tmax):

    self.NOfColumn = N_Column
    self.NOfRow = N_Row
    self.TMAX = tmax
    # agentField[0~2][row][col]作成
    self.agentField = [[[0+row for row in range(N_Row)] for col in range(N_Column) ] for k in range(2)]
    self.fRandomOrder = []
    self.fRandom = int(time.time() * 1000)

    count = 0
    row = 0
    while row < N_Row:
      col = 0
      while col < N_Column:
        self.fRandomOrder.append(count)
        self.agentField[0][row][col] = agent.Agent(0, 0.0)
        self.agentField[1][row][col] = agent.Agent(0, 0.0)
        count += 1
        col += 1
      row += 1
    self.setNewTrial()

  def setNewTrial(self):
    sizeHalf = len(self.fRandomOrder) / 2

    counter = 0
    random.shuffle(self.fRandomOrder)
    for i in self.fRandomOrder:
      row = int(i / self.NOfColumn) #整数に変換 切り捨て
      col = i % self.NOfColumn
      if counter < sizeHalf:
        behavior = 1
      else:
        behavior = 0
      self.agentField[0][row][col].behavior = behavior
      self.agentField[0][row][col].fRatio = 0.5
      self.agentField[1][row][col].behavior = behavior
      self.agentField[1][row][col].fRatio = 0.5

      counter += 1

  def run(self):
    t = 1
    while t < self.TMAX:
      self.nextStep(t)
      t += 1
      if t % 1 == 0:
        self.printBehavior(t)

  def printBehavior(self, time):
    row = 0
    while row < self.NOfRow:
      col = 0
      while col < self.NOfColumn:
        if self.agentField[time % 2][row][col].behavior == 0:
          print("_,", end="")
        else:
          print("0,", end="")
        col += 1
      sys.stdout.write('\n')
      row += 1
    sys.stdout.write('\n')

  def nextStep(self, t):
    self.nextStepStandingOvationSync(t)

  def getNeiborSetStandingOvation(self, row, col, agent, agentField):
    numberOfStanding = 0
    if row != 0:
      if col == 0:
        numberOfStanding += agentField[row - 1][col].behavior
        numberOfStanding += agentField[row][col + 1].behavior
        numberOfStanding += agentField[row - 1][col + 1].behavior
        agent.makeDecision(3, numberOfStanding)
        return True
      elif col == self.NOfColumn - 1:
        numberOfStanding += agentField[row - 1][col].behavior
        numberOfStanding += agentField[row][col - 1].behavior
        numberOfStanding += agentField[row - 1][col - 1].behavior
        agent.makeDecision(3, numberOfStanding)
        return True
      else:
        numberOfStanding += agentField[row - 1][col - 1].behavior
        numberOfStanding += agentField[row - 1][col].behavior
        numberOfStanding += agentField[row - 1][col + 1].behavior
        numberOfStanding += agentField[row][col - 1].behavior
        numberOfStanding += agentField[row][col + 1].behavior
        agent.makeDecision(5, numberOfStanding)
        return True
    else:
      if col == 0:
        numberOfStanding += agentField[row][col + 1].behavior
        agent.makeDecision(1, numberOfStanding)
        return True
      elif col == self.NOfColumn - 1:
        numberOfStanding += agentField[row][col - 1].behavior
        agent.makeDecision(1, numberOfStanding)
        return True
      else:
        numberOfStanding += agentField[row][col - 1].behavior
        numberOfStanding += agentField[row][col + 1].behavior
        agent.makeDecision(2, numberOfStanding)
        return True

  def nextStepStandingOvationSync(self, t):
    row = 0
    while row < self.NOfRow:
      col = 0
      while col < self.NOfColumn:
        self.getNeiborSetStandingOvation(row, col, self.agentField[t % 2][row][col], self.agentField[(t - 1) % 2])
        col += 1
      row += 1

  def getAgentField(self, t):
    return self.agentField[t % 2]

isSyncronize = True
so = StandingOvationSimple(30, 30, 4)
start = time.time() * 1000
so.run()
end = time.time() * 1000
runTime = (end - start) / 1000.0
print(runTime)
