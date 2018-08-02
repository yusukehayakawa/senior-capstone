# from time import sleep
# import numpy as np
import agent
import time
import random
import sys

class StandingOvationSimple:
  def __init__(self, N_Column, N_Row, tmax):

    self.NOfColumn = N_Column
    self.NOfRow = N_Row
    self.TMAX = tmax

    self.agentField = [[[0+row for row in range(300)] for col in range(300) ] for k in range(3)]
    self.fRandomOrder = []
    self.fRandom = int(time.time() * 1000)

    count = 0
    row = 0
    col = 0

    while row < N_Row:
      while col < N_Column:
        self.fRandomOrder.append(count)
        # fRandom.NextDouble()
        self.agentField[0][row][col] = agent.Agent(0, 0.0)
        self.agentField[1][row][col] = agent.Agent(0, 0.0)
        count += 1
        col += 1
      row += 1
      col = 0
    self.setNewTrial()

  def setNewTrial(self):
    sizeHalf = len(self.fRandomOrder) / 2

    counter = 0
    random.shuffle(self.fRandomOrder)
    for i in self.fRandomOrder:
      row = round(i / self.NOfColumn) #整数に変換
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
    col = 0
    while row < self.NOfRow:
      while col < self.NOfColumn:
        self.getNeiborSetStandingOvation(row, col, self.agentField[t % 2][row][col], self.agentField[(t - 1) % 2])
        col += 1
      row += 1
      col = 0

  def getAgentField(self, t):
    return self.agentField[t % 2]

  # def main(self):
  #   isSyncronize = True
  #   so = StandingOvationSimple(300, 300, 800)
  #   start = time.time() * 1000
  #   so.run()
  #   end = time.time() * 1000
  #   runTime = (end - start) / 1000.0
  #   print(runTime)

  # if __name__ == "__main__":
  #   main()

isSyncronize = True
so = StandingOvationSimple(300, 300, 800)
start = time.time() * 1000
so.run()
end = time.time() * 1000
runTime = (end - start) / 1000.0
print(runTime)
