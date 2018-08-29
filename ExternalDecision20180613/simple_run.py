import standing_ovation
# import agent
from time import sleep
import time
import sys
import numpy as np

class SimpleRun:
  def __init__(self, f_standing_ovation):
    standing_ovation.StandingOvation(300, 300, 800, 1, True, 0.0)
    # StandingOvation ALL

    self.f_n_of_column = f_standing_ovation.n_of_column
    self.f_n_of_row = f_standing_ovation.n_of_row
    self.f_tmax = f_standing_ovation.tmax
    self.f_neibour_type = f_standing_ovation.f_neibour_type

  def run(self):
    t = 1
    while t < self.f_tmax:
      if self.next_step(t):
        print(self.f_standing_ovation.trial_result(t))
        return True
      t += 1
    print(self.f_standing_ovation.trial_result(self.f_tmax - 1))
    return False

  def run_non_stop(self, delay):
    t = 1
    while t < self.f_tmax:
      if not self.next_step(t):
        try:
          time.sleep(delay)
        except Exception as e:
          raise e
      else:
        print(self.f_standing_ovation.trial_result(self.f_tmax - 1))
        return False
      t += 1
    print(self.f_standing_ovation.trial_result(self.f_tmax - 1))
    return False

  def next_step(self, t):
    is_stable = self.f_standing_ovation.next_step(t)
    f_agent_field = self.f_standing_ovation.get_agent_field(t)
    return is_stable

# 実行
agpanel = SimpleRun()
trial = 0
while trial < 100:
  neibour_type = 0
  while neibour_type < 4:
    width = 0
    while width <= 100:
      d_width = width / 100.0
      agpanel.f_standing_ovation.set_new_trial(neibour_type, True, d_width, 0.5)
      agpanel.run_non_stop(0)
      time.sleep(3000)
      width += 20
    neibour_type += 1
  trial += 1
sys.exit()
