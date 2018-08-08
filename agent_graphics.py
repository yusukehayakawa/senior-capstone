import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import standing_ovation_simple
import time
import traceback
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class AgentGraphics(standing_ovation_simple.StandingOvationSimple):
  def __init__(self, n_column, n_row, tmax):
    super().__init__(n_column, n_row, tmax)
    # self.graohics = 
    # self.dimension = 
    self.f_standing_ovation = self.agent_field
    # self.f_agent_field = self.get_agent_field(t)
    # self.f_n_of_column = self.n_of_column
    # self.f_n_of_row = self.n_of_row
    # self.f_tmax = self.tmax
    self.g_data = np.zeros((n_column, n_row), dtype=int)
    self.f_size_x = 0 
    self.f_size_y = 0

  def paint_component(self):
    fig = plt.figure()
    animation.FuncAnimation(fig, self.update, interval=100, frames=self.tmax, repeat=False)
    # sns.heatmap(self.g_data, cmap='winter', cbar=False, linewidths=1, square=True)

  def update(self, i):
    plt.clf()
    self.next_step(i)
    self.f_agent_field = self.get_agent_field(i)
    self.plot_grid(self.f_agent_field)
    sns.heatmap(self.g_data, cmap='winter', cbar=False, linewidths=1, square=True)
    # t = time
    # fig = plt.figure()
    # while i < self.tmax:
    #   self.next_step(i)
    #   self.f_agent_field = self.get_agent_field(i)
    #   self.plot_grid(self.f_agent_field)
    #   # heatmap = sns.heatmap(self.g_data, cmap='winter', cbar=False, linewidths=1, square=True)
    #   # plt.show()
    #   sns.heatmap(self.g_data, cmap='winter', cbar=False, linewidths=1, square=True)

    #   # animation.FuncAnimation(fig, self.paint_component(), interval=100)
    #   # plt.show()
    #   # try:
    #   #   time.sleep(delay)
    #   # except:
    #   #   print(traceback.format_exc())
    #   #   traceback.print_exc()
    #   i += 1

  def get_agent_field(self, t):
    return self.agent_field[t % 2]

  def plot_grid(self, f_agent_field):
    row = 0
    while row < self.n_of_row:
      col = 0
      while col < self.n_of_column:
        self.g_data[row][col] = f_agent_field[row][col].behavior
        col += 1
      row += 1



agpanel = AgentGraphics(30, 30, 10)
agpanel.set_new_trial()
agpanel.paint_component()
# try:
#   time.sleep(30)
# except:
#   print(traceback.format_exc())
#   traceback.print_exc()

