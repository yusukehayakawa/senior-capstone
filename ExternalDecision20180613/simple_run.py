from standing_ovation import StandingOvation
import agent
from time import sleep
import time
import sys
import numpy as np

class SimpleRun:

  # f_standing_ovation = StandingOvation()
  # f_agent_field = Agent()
  # f_n_of_column = 0
  # f_n_of_row = 0
  # f_tmax = 0
  # f_neibour_type = 0
  # fSizeX = 0
  # fSizeY = 0

  def __init__(self, f_standing_ovation):
    super().__init__(300, 300, 800, standing_ovation.all, True, 0.0)

    self.f_n_of_column = f_standing_ovation.n_of_column
    self.f_n_of_row = f_standing_ovation.n_of_row
    self.f_tmax = f_standing_ovation.tmax
    self.f_neibour_type = f_standing_ovation.f_neibour_type

  def run(self):
    t = 1
    while t < f_tmax:
      if next_step(t):
        print(f_standing_ovation.trial_result(t))
        return True
      t += 1
    print(f_standing_ovation.trial_result(f_tmax - 1))
    return False

  def run_non_stop(self, delay):
    t = 1
    while t < f_tmax:
      if not next_step(t):
        try:
          time.sleep(delay)
        except Exception as e:
          raise e
      else:
        print(f_standing_ovation.trial_result(f_tmax - 1))
        return False
      t += 1
    print(f_standing_ovation.trial_result(f_tmax - 1))
    return False

  def next_step(t):
    is_stable = f_standing_ovation.next_step(t)
    f_agent_field = f_standing_ovation.get_agent_field(t)
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
