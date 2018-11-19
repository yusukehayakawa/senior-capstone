import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import standing_ovation
import time
import traceback

class AgentHeatmap(standing_ovation.StandingOvation):
  def __init__(self, n_column, n_row, tmax, neighbor_type, is_syncronize, width):
    super().__init__(n_column, n_row, tmax, neighbor_type, is_syncronize, width)
    self.f_standing_ovation = self.agent_field
    self.g_data = np.zeros((n_column, n_row), dtype=int)

  def run(self):
    t = 1
    while t < self.tmax:
      self.next_step(t)
      self.f_agent_field = self.get_agent_field(t)
      self.set_heatmap_data(self.f_agent_field)
      sns.heatmap(self.g_data, cmap='winter', cbar=False, linewidths=.001, square=True)
      plt.pause(.0001)
      # try:
      #   time.sleep(delay)
      # except:
      #   print(traceback.format_exc())
      #   traceback.print_exc()
      t += 1

  def get_agent_field(self, t):
    return self.agent_field[t % 2]

  def set_heatmap_data(self, f_agent_field):
    row = 0
    while row < self.n_of_row:
      col = 0
      while col < self.n_of_column:
        self.g_data[row][col] = f_agent_field[row][col].behavior
        col += 1
      row += 1

start = int(time.time() * 1000)
agpanel = AgentHeatmap(30, 30, 10, 1, True, 0)
agpanel.set_new_trial(1, True, 0, 0.5)
agpanel.run()
end = int(time.time() * 1000)
run_time = (end - start) / 1000.0
print(str(run_time))
# try:
#   time.sleep(30)
# except:
#   print(traceback.format_exc())
#   traceback.print_exc()

# set_new_trial(neighbor_type, is_syncronize, width, 0.5)
# STANDNIG_OVATION = 0
# ALL = 1
# MOOR = 2
# NEUMANN = 3
# CONES = 4
