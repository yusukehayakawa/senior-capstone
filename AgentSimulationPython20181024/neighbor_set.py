import agent
import time
import random
import sys
import math

class NeighborSet(object):
  def __init__(self, n_column, n_row, tmax, neighbor_type, width):

    # Define field (environment)
    self.n_of_column = n_column
    self.n_of_row = n_row
    self.tmax = tmax
    self.F_FIELD_BUFFER_SIZE = 2

    # Define Agent properties
    self.f_width = 0

    # record data
    # agent_field[0~1][row][col]作成
    self.agent_field = [[[0+row for row in range(n_row)] for col in range(n_column) ] for k in range(self.F_FIELD_BUFFER_SIZE)]
    self.f_random_order = []
    # self.f_random = int(time.time() * 1000)
    self.f_number_of_changed_agents = []
    self.f_number_of_standing_agents = []
    self.f_number_of_changed_agents.append(self.n_of_column * self.n_of_row)
    self.f_min_number_of_changed_agents = self.n_of_column * self.n_of_row
    self.f_period_counter = 0
    self.f_final_time = 0
    self.f_final_number_of_changed_agents = 0
    self.f_final_period = 0

    self.STANDNIG_OVATION = 0
    self.ALL = 1
    self.MOOR = 2
    self.f_neighbor_type = neighbor_type
    behavior = 0
    count = 0
    rate = 0
    for row in range(0, n_row):
      for col in range(0, n_column):
        self.f_random_order.append(count)
        name = str(row) + "" + str(col)
        for k in range(0, self.F_FIELD_BUFFER_SIZE):
          self.agent_field[k][row][col] = agent.Agent(behavior, name, rate)
        count += 1
    self.set_new_trial(neighbor_type, width, 0.5)

  def initial_setting(self, neighbor_type, width):
    if width < 0.0 or width > 1.0:
      print("width is out of range [0,1]")
      return False
    else:
      self.f_width = width

    self.f_neighbor_type = neighbor_type
    self.f_period_counter = 0
    self.f_final_time = -1
    self.f_final_number_of_changed_agents = -1
    self.f_final_period = -1
    self.f_number_of_changed_agents = []
    self.f_number_of_changed_agents.append(self.n_of_column * self.n_of_row)
    return True

  def set_new_trial(self, neighbor_type, width, rate_of_stand):
    self.initial_setting(neighbor_type, width)
    size = len(self.f_random_order)
    number_of_stand = rate_of_stand * size
    counter_of_stand = number_of_stand
    counter = 0
    random.shuffle(self.f_random_order)
    rate = 0
    for i in self.f_random_order:
      row = int(i / self.n_of_column) #整数に変換 切り捨て
      col = i % self.n_of_column
      rate = self.f_width * (random.random() - 0.5) + 0.5
      if counter < counter_of_stand:
        behavior = 1
      else:
        behavior = 0

      for k in range(0, self.F_FIELD_BUFFER_SIZE): #2
        self.agent_field[k][row][col].behavior = behavior
        self.agent_field[k][row][col].f_ratio = rate
      counter += 1

    self.f_number_of_standing_agents = []
    self.f_number_of_standing_agents.append(counter_of_stand)
    self.f_min_number_of_changed_agents = self.n_of_column * self.n_of_row

  def get_neighbor_set_standing_ovation(self, row, col, agent, agent_field):
    number_of_standing = 0
    if row != 0:
      if col == 0: # agentが左端の列にいるとき
        number_of_standing += agent_field[row - 1][col].behavior
        number_of_standing += agent_field[row][col + 1].behavior
        number_of_standing += agent_field[row - 1][col + 1].behavior
        agent.make_decision(3, number_of_standing)
        return True
      elif col == self.n_of_column - 1: # agentが右端の列にいるとき
        number_of_standing += agent_field[row - 1][col].behavior
        number_of_standing += agent_field[row][col - 1].behavior
        number_of_standing += agent_field[row - 1][col - 1].behavior
        agent.make_decision(3, number_of_standing)
        return True
      else: # 左右、前に他のagentがいるとき
        number_of_standing += agent_field[row - 1][col - 1].behavior
        number_of_standing += agent_field[row - 1][col].behavior
        number_of_standing += agent_field[row - 1][col + 1].behavior
        number_of_standing += agent_field[row][col - 1].behavior
        number_of_standing += agent_field[row][col + 1].behavior
        agent.make_decision(5, number_of_standing)
        return True
    else:
      if col == 0: # agentが左角にいるとき(row,col)=(0,0)
        number_of_standing += agent_field[row][col + 1].behavior
        agent.make_decision(1, number_of_standing)
        return True
      elif col == self.n_of_column - 1: # agentが右角にいるとき
        number_of_standing += agent_field[row][col - 1].behavior
        agent.make_decision(1, number_of_standing)
        return True
      else: # agentが両端以外の最前列にいるとき
        number_of_standing += agent_field[row][col - 1].behavior
        number_of_standing += agent_field[row][col + 1].behavior
        agent.make_decision(2, number_of_standing)
        return True

  def get_neighbor_set_moor(self, row, col, agent, agent_field):
    number_of_standing = 0
    number_of_standing += agent_field[(row + 1) % self.n_of_row][(col + 1) % self.n_of_column].behavior
    number_of_standing += agent_field[(row + 1) % self.n_of_row][(col - 1 + self.n_of_column) % self.n_of_column].behavior
    number_of_standing += agent_field[row][(col + 1) % self.n_of_column].behavior
    number_of_standing += agent_field[row][(col - 1 + self.n_of_column) % self.n_of_column].behavior
    number_of_standing += agent_field[(row + 1) % self.n_of_row][col].behavior
    number_of_standing += agent_field[(row - 1 + self.n_of_row) % self.n_of_row][col].behavior
    number_of_standing += agent_field[(row - 1 + self.n_of_row) % self.n_of_row][(col + 1) % self.n_of_column].behavior
    number_of_standing += agent_field[(row - 1 + self.n_of_row) % self.n_of_row][(col - 1 + self.n_of_column) % self.n_of_column].behavior
    agent.make_decision(8, number_of_standing)

  def run(self):
    for i in range(1, self.tmax):
      if self.next_step(i):
        return True

  def run_non_stop(self):
    for i in range(1, self.tmax):
      self.next_step(i)
    return False

  def next_step(self, t):
    is_stable = False
    if self.f_neighbor_type == self.STANDNIG_OVATION:
      self.next_step_standing_ovation_sync(t)
    elif self.f_neighbor_type == self.MOOR:
      self.next_step_sync_moor(t)
    elif self.f_neighbor_type == self.ALL:
      self.next_step_all_sync(t)
    self.count_changed_and_stand_agent(t)
    num = self.f_number_of_changed_agents[t]
    if t > self.F_FIELD_BUFFER_SIZE:
      if num == 0:
        is_stable = True
        if self.f_final_number_of_changed_agents != 0:
          self.f_final_number_of_changed_agents = num
          self.f_final_period = 0
          self.f_final_time = t
      elif num < self.n_of_column * self.n_of_row / 50:
        if self.is_saturate(t):
          is_stable = True
    return is_stable

  def is_saturate(self, t):
    saturate = False
    max = 0
    if self.f_min_number_of_changed_agents > self.f_number_of_changed_agents[t]:
      self.f_min_number_of_changed_agents = self.f_number_of_changed_agents[t]
      self.f_final_number_of_changed_agents = self.f_min_number_of_changed_agents
      self.f_final_period = -1
      self.f_final_time = t
    if (t - self.f_final_time) > 50:
      for past in range(0, 50):
        if max < self.f_number_of_changed_agents[t - past]:
          max = self.f_number_of_changed_agents[t - past]
      if (max - self.f_min_number_of_changed_agents < 3):
        saturate = True
    return saturate

  def count_changed_and_stand_agent(self, t):
    counter_of_changed_agent = 0
    counter_of_stand = 0
    total_row = self.n_of_row
    total_col = self.n_of_column
    for i in range(0, total_row):
      for j in range(0, total_col):
        if (self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior != self.agent_field[(t - 1) % self.F_FIELD_BUFFER_SIZE][i][j].behavior):
          counter_of_changed_agent += 1
        if (self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior == 1):
          counter_of_stand += 1
    self.f_number_of_changed_agents.append(counter_of_changed_agent)
    self.f_number_of_standing_agents.append(counter_of_stand)

  def next_step_standing_ovation_sync(self, t):
    total_row = self.n_of_row
    total_col = self.n_of_column
    for row in range(0, total_row):
      for col in range(0, total_col):
        self.get_neighbor_set_standing_ovation(row, col, self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col], self.agent_field[(t - 1) % self.F_FIELD_BUFFER_SIZE])

  def next_step_sync_moor(self, t):
    total_row = self.n_of_row
    total_col = self.n_of_column
    for row in range(0, total_row):
      for col in range(0, total_col):
        self.get_neighbor_set_moor(row, col, self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col], self.agent_field[(t - 1) % self.F_FIELD_BUFFER_SIZE])

  def next_step_all_sync(self, t):
    total = self.n_of_column * self.n_of_row
    old_num_of_stand = self.f_number_of_standing_agents[t - 1]
    total_row = self.n_of_row
    total_col = self.n_of_column
    for i in range(0, total_row):
      for j in range(0, total_col):
        observed_num_of_stand = old_num_of_stand - self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior
        current_ratio = observed_num_of_stand / total
        # print(current_ratio)
        if current_ratio >= self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].f_ratio:
          self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior = 1
        else:
          self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior = 0

  def to_string_befavior(self, t):
    output = ""
    total_row = self.n_of_row
    total_col = self.n_of_column
    for row in range(0, total_row):
      for col in range(0, total_col):
        output += self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col].behavior + ","
      output += "\n"
    return output

  def to_string_threshold(self):
    output = ""
    total_row = self.n_of_row
    total_col = self.n_of_column
    for row in range(0, total_row):
      for col in range(0, total_col):
        output += self.agent_field[0][row][col].f_ratio + ","
      output += "\n"
    return output

  def to_string_number_of_changed_agent(self):
    output = ""
    total_standing_agents = len(self.f_number_of_standing_agents)
    for t in range(0, total_standing_agents):
      output += self.f_number_of_changed_agents[t] + "\n"
    return output

  def to_string_number_of_stand(self):
    output = ""
    total_changed_agents = len(self.f_number_of_changed_agents)
    for t in range(0, total_changed_agents):
      output += self.f_number_of_changed_agents[t] + "\n"
    return output

  def to_string_time_series(self):
    output = ""
    total_changed_agents = len(self.f_number_of_changed_agents)
    for t in range(0, total_changed_agents):
      output += t + "," + self.f_number_of_changed_agents[t] + "," + self.f_number_of_standing_agents[t] + "\n"
    return output

  def get_agent_field(self, t):
    return self.agent_field[t % self.F_FIELD_BUFFER_SIZE]

  # This method is unusable because period is much bigger than what I expected.
  # So please use "is_saturate" method to decide the system is in periodic phase.
  def is_periodic(self, t):
    periodic = False
    is_same_number = False
    c_num_of_c_agent = self.f_number_of_changed_agents[t]
    period = 0
    time = t - 1
    for time in range(time, t - self.F_FIELD_BUFFER_SIZE, -1):
      if c_num_of_c_agent == self.f_number_of_changed_agents[time]:
        is_same_number = True
        break

    if is_same_number:
      past = 1
      total_row = self.n_of_row
      total_col = self.n_of_column
      for past in range(past, self.F_FIELD_BUFFER_SIZE, 1):
        is_all_same = True
        try:
          for i in range(0, total_row):
            for j in range(0, total_col):
              if self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior != self.agent_field[(t - past) % self.F_FIELD_BUFFER_SIZE][i][j].behavior:
                is_all_same = False
                break
        except Exception as e:
          raise e
        if is_all_same:
          periodic = True
          if period == 0:
            period = past
    if periodic:
      if self.f_final_period == period:
        if self.f_period_counter == 0:
          self.f_final_time = t - period
          self.f_final_number_of_changed_agents = c_num_of_c_agent
        self.f_period_counter += 1
      else:
        self.f_final_period = period
        self.f_period_counter = 0
    if self.f_period_counter > 2:
      return True
    else:
      return False

# 実行
# 引数
# NeighborSet(n_column, n_row, tmax, neighbor_type, width)
# STANDNIG_OVATION = 0
# ALL = 1
# MOOR = 2

# str_s = ""
# str_t = ""
# so = NeighborSet(100, 100, 5, 2, 0.0)
# for width in range(0, 101, 20):
#   for neighbor_type in range(0, 3, 1):
#     if neighbor_type == 0:
#       str_t = "STANDNIG_OVATION"
#     elif neighbor_type == 1:
#       str_t = "All"
#     elif neighbor_type == 2:
#       str_t = "MOOR"
#     d_width = width / 100.0
#     so.set_new_trial(neighbor_type, d_width, 0.5)
#     start = int(time.time() * 1000)
#     so.run_non_stop()
#     end = int(time.time() * 1000)
#     run_time = (end - start) / 1000.0
#     print(str_t + "\t" + str(width) + "\t" + str(run_time))
