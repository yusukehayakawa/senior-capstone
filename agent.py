class Agent:
  def __init__(self, s, ratio):
    self.behavior = s  # 1--GOOD,0--BAD
    self.fRatio = ratio #周りの何％が立っていたら自分がたつか

  def makeDecision(self, numberOfObservedAgent, numberOfStandOrGoodAgent):
    ratio = numberOfStandOrGoodAgent / numberOfObservedAgent
    if ratio - self.fRatio > 0.001:
      behavior = 1
    elif ratio - self.fRatio < -0.001:
      behavior = 0
