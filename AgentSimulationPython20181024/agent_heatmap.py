import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import neighbor_set
import time
import traceback
import pyautogui

# heatmap
# 0--blue
# 1--green
class AgentHeatmap(neighbor_set.NeighborSet):
  def __init__(self, n_column, n_row, tmax, neighbor_type, width):
    super().__init__(n_column, n_row, tmax, neighbor_type, width)
    self.f_neighbor_set = self.agent_field
    self.heatmap_data = np.zeros((n_column, n_row), dtype=int)

  def run(self):
    time_max = self.tmax
    for t in range(1, time_max):
      self.next_step(t)
      self.f_agent_field = self.get_agent_field(t)
      self.set_heatmap_data(self.f_agent_field)
      sns.heatmap(self.heatmap_data, cmap='winter', cbar=False, linewidths=.001, square=True)
    plt.show()
      #plt.pause(.0001)
      #print(t)
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

  if __name__ == '__main__':
    start = int(time.time() * 1000)
    agpanel = AgentHeatmap(300, 300, 5, 2, 0.3)
    agpanel.set_new_trial(2, 0.3, 0.5)
    agpanel.run()
    end = int(time.time() * 1000)
    run_time = (end - start) / 1000.0
    print(str(run_time))

# 引数
# set_new_trial(self, neighbor_type, width, rate_of_stand)
# STANDNIG_OVATION = 0
# ALL = 1
# MOOR = 2

