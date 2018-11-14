class Agent:
  def __init__(self, s, ratio, lname):
    self.behavior = s  # 1--GOOD,0--BAD
    self.f_ratio = ratio #周りの何％が立っていたら自分がたつか
    self.name = lname

  def make_decision(self, number_of_observed_agent, number_of_stand_or_good_agent):
    ratio = number_of_stand_or_good_agent / number_of_observed_agent
    if ratio - self.f_ratio > 0.001:
      self.behavior = 1
    elif ratio - self.f_ratio < -0.001:
      self.behavior = 0
