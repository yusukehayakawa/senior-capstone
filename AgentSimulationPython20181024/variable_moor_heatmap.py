import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import variable_moor
import time
import traceback
import pyautogui

# heatmap
# 0--blue
# 1--green
class VariableMoorHeatmap(variable_moor.VariableMoor):
  def __init__(self, n_column, n_row, tmax, neighbor_type, width, number_of_observed_agent, number_of_case):
    super().__init__(n_column, n_row, tmax, neighbor_type, width)
    self.f_neighbor_set = self.agent_field
    self.heatmap_data = np.zeros((n_column, n_row), dtype=int)
    self.number_of_observed_agent = number_of_observed_agent
    self.number_of_case = number_of_case

  def run(self):
    time_max = self.tmax
    for t in range(1, time_max):
      self.next_step(t)
      self.f_agent_field = self.get_agent_field(t)
      self.set_heatmap_data(self.f_agent_field)
      sns.heatmap(self.heatmap_data, cmap='winter', cbar=False, linewidths=.001, square=True)
      plt.pause(.0001)
      # print(t)
      # スクリーンショット
      # sc = pyautogui.screenshot()
      # sc.save('screenshot' + str(t) + '.png')
      # if t == 1 or t % 50 == 0:
      #   sc = pyautogui.screenshot()
      #   sc.save('screenshot' + str(t) + '.png')

  def get_agent_field(self, t):
    return self.agent_field[t % 2]

  def set_heatmap_data(self, f_agent_field):
    total_row = self.n_of_row
    total_col = self.n_of_column
    for row in range(0, total_row):
      for col in range(0, total_col):
        self.heatmap_data[row][col] = f_agent_field[row][col].behavior

# start = int(time.time() * 1000)
# agpanel = VariableMoorHeatmap(50, 50, 50, 3, 0.0, 5, 4)
# agpanel.set_new_trial(3, 0.0, 0.5)
# agpanel.run()
# end = int(time.time() * 1000)
# run_time = (end - start) / 1000.0
# print(str(run_time))

# 引数
# set_new_trial(self, neighbor_type, width, rate_of_stand)
# STANDNIG_OVATION = 0
# ALL = 1
# MOOR = 2
# VARIABLE_MOOR = 3
  if __name__ == '__main__':
    f_sort_of_neighbor = [ 1, 2, 6, 10, 12, 10, 6, 2, 1 ]
    for a in range(8, 0, -1):
      for b in range(0, f_sort_of_neighbor[a], 1):
        agpanel = VariableMoorHeatmap(100, 100, 20, 3, 0.0, a, b)
        agpanel.set_new_trial(3, 0.0, 0.5)
        agpanel.run()
        print('近隣数' + str(a) + ':ケース' +str(b) + ' done!')



# def run(number_of_observed_agent, number_of_case, neighbor_type):
#   f_standing_ovation.set_new_trial()
#   for t in range(1, self.tmax, 1):
#     f_agent_field = f_standing_ovation.get_agent_field(t - 1)

#     repaint

#     f_standing_ovation.next_step(t, number_of_observed_agent, number_of_case, neighbor_type)

# def next_step(t, number_of_observed_agent, number_of_case, neighbor_type):
  
#   if neighbor_type == "uniform":
#     neighbor_set = NeighborSet.get_neighbor_set_variable_moor(number_of_observed_agent, number_of_case)
#   elif neighbor_type == "small_world":
#     neighbor_set = NeighborSet.get_neighbor(8, 0)
#   for row in range(0, n_of_row, 1):
#     for col in range(0, n_of_col, 1):
#       if neighbor_type == "random":
#         neighbor_set = NeighborSet.get_random_neighbor(number_of_observed_agent)

#       c_agent = agent_field

#       if neighbor_type == "small_world":
#         counter = set_random

