import agent
import time
import random
import sys
import math

class StandingOvation(object):
  def __init__(self, n_column, n_row, tmax, neighbor_type, is_syncronize, width):

    # Define field (environment)
    self.n_of_column = n_column
    self.n_of_row = n_row
    self.tmax = tmax
    self.F_FIELD_BUFFER_SIZE = 2

    # Define Agent properties
    self.f_width = 0
    self.f_is_synchronize = 0

    # record data
    # agent_field[0~1][row][col]作成
    self.agent_field = [[[0+row for row in range(n_row)] for col in range(n_column) ] for k in range(self.F_FIELD_BUFFER_SIZE)]
    self.f_random_order = []
    self.f_random = int(time.time() * 1000)
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
    self.NEUMANN = 3
    self.CONES = 4
    self.f_neighbor_type = neighbor_type

    behavior = 0
    count = 0
    rate = 0
    row = 0
    while row < n_row:
      col = 0
      while col < n_column:
        self.f_random_order.append(count)
        name = str(row) + "" + str(col)
        k = 0
        while k < self.F_FIELD_BUFFER_SIZE: #2
          self.agent_field[k][row][col] = agent.Agent(behavior, name, rate)
          k += 1
        count += 1
        col += 1
      row += 1
    self.set_new_trial(neighbor_type, is_syncronize, width, 0.5)

  def initial_setting(self, neighbor_type, is_syncronize, width):
    if width < 0.0 or width > 1.0:
      print("width is out of range [0,1]")
      return False
    else:
      self.f_width = width

    self.f_neighbor_type = neighbor_type
    self.f_is_synchronize = is_syncronize
    self.f_period_counter = 0
    self.f_final_time = -1
    self.f_final_number_of_changed_agents = -1
    self.f_final_period = -1
    self.f_number_of_changed_agents = []
    self.f_number_of_changed_agents.append(self.n_of_column * self.n_of_row)
    return True

  def set_new_trial(self, neighbor_type, is_syncronize, width, rate_of_stand):
    self.initial_setting(neighbor_type, is_syncronize, width)
    size = len(self.f_random_order)
    number_of_stand = rate_of_stand * size
    counter_of_stand = number_of_stand
    counter = 0
    random.shuffle(self.f_random_order)
    rate = 0
    for i in self.f_random_order:
      row = int(i / self.n_of_column) #整数に変換 切り捨て
      col = i % self.n_of_column
      rate = self.f_width * (self.f_random - 0.5) + 0.5
      if counter < counter_of_stand:
        behavior = 1
      else:
        behavior = 0

      k = 0
      while k < self.F_FIELD_BUFFER_SIZE: #2
        self.agent_field[k][row][col].behavior = behavior
        self.agent_field[k][row][col].f_ratio = rate
        k += 1

      counter += 1
    self.f_number_of_standing_agents.clear()
    self.f_number_of_standing_agents.append(counter_of_stand)
    self.f_min_number_of_changed_agents = self.n_of_column * self.n_of_row

  def get_neighbor_set_standing_ovation(self, row, col, agent, agent_field):
    number_of_standing = 0
    if row != 0:
      if col == 0:
        number_of_standing += agent_field[row - 1][col].behavior
        number_of_standing += agent_field[row][col + 1].behavior
        number_of_standing += agent_field[row - 1][col + 1].behavior
        agent.make_decision(3, number_of_standing)
        return True
      elif col == self.n_of_column - 1:
        number_of_standing += agent_field[row - 1][col].behavior
        number_of_standing += agent_field[row][col - 1].behavior
        number_of_standing += agent_field[row - 1][col - 1].behavior
        agent.make_decision(3, number_of_standing)
        return True
      else:
        number_of_standing += agent_field[row - 1][col - 1].behavior
        number_of_standing += agent_field[row - 1][col].behavior
        number_of_standing += agent_field[row - 1][col + 1].behavior
        number_of_standing += agent_field[row][col - 1].behavior
        number_of_standing += agent_field[row][col + 1].behavior
        agent.make_decision(5, number_of_standing)
        return True
    else:
      if col == 0:
        number_of_standing += agent_field[row][col + 1].behavior
        agent.make_decision(1, number_of_standing)
        return True
      elif col == self.n_of_column - 1:
        number_of_standing += agent_field[row][col - 1].behavior
        agent.make_decision(1, number_of_standing)
        return True
      else:
        number_of_standing += agent_field[row][col - 1].behavior
        number_of_standing += agent_field[row][col + 1].behavior
        agent.make_decision(2, number_of_standing)
        return True

  def get_neighbor_set_cones(self, row, col, agent, agent_field):
    number_of_standing = 0
    counter = 0
    if col == 0:
      number_of_standing += agent_field[row][col + 1].behavior
      counter += 1
    elif col == self.n_of_column - 1:
      number_of_standing += agent_field[row][col - 2].behavior
      counter += 1
    else:
      number_of_standing += agent_field[row][col - 1].behavior
      number_of_standing += agent_field[row][col + 1].behavior
      counter += 2

    if row != 0:
      i = 1
      while i < row:
        j = col - i
        while j <= col + i:
          if j >= 0 and j < self.n_of_column:
            number_of_standing += agent_field[row - i][j].behavior
            counter += 1
          j += 1
        i += 1
    agent.make_decision(counter, number_of_standing)


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


  def get_neighbor_set_neumann(self, row, col, agent, agent_field):
    number_of_standing = 0
    number_of_standing += agent_field[row][(col + 1) % self.n_of_column].behavior
    number_of_standing += agent_field[row][(col - 1 + self.n_of_column) % self.n_of_column].behavior
    number_of_standing += agent_field[(row + 1) % self.n_of_row][col].behavior
    number_of_standing += agent_field[(row - 1 + self.n_of_row) % self.n_of_row][col].behavior
    agent.make_decision(4, number_of_standing)

  def run(self):
    t = 1
    while t < self.tmax:
      if self.next_step(t):
        return True
      t += 1

  def run_non_stop(self):
    t = 1
    while t < self.tmax:
      self.next_step(t)
      t += 1
    # print()
    return False


  # @param t

  def next_step(self, t):
    is_stable = False
    if self.f_is_synchronize:
      if self.f_neighbor_type == self.STANDNIG_OVATION:
        self.next_step_standing_ovation_sync(t)
      elif self.f_neighbor_type == self.CONES:
        self.next_step_sync_cone(t)
      elif self.f_neighbor_type == self.MOOR:
        self.next_step_sync_moor(t)
      elif self.f_neighbor_type == self.NEUMANN:
        self.next_step_sync_neumann(t)
      elif self.f_neighbor_type == self.ALL:
        self.next_step_all_sync(t)
    else:
      if self.f_neighbor_type == self.STANDNIG_OVATION:
        self.next_step_standing_ovation_async(t)
      elif self.f_neighbor_type == self.CONES:
        self.next_step_async_cone(t)
      elif self.f_neighbor_type == self.MOOR:
        self.next_step_async_moor(t)
      elif self.f_neighbor_type == self.NEUMANN:
        self.next_step_async_neumann(t)
      elif self.f_neighbor_type == self.ALL:
        self.next_step_all_async(t)

    self.count_changed_and_stand_agent(t)
    num = self.f_number_of_changed_agents[t]
    # チェック
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
    # チェック
    if self.f_min_number_of_changed_agents > self.f_number_of_changed_agents[t]:
      self.f_min_number_of_changed_agents = self.f_number_of_changed_agents[t]
      self.f_final_number_of_changed_agents = self.f_min_number_of_changed_agents
      self.f_final_period = -1
      self.f_final_time = t
    if (t - self.f_final_time) > 50:
      past = 0
      while past < 50:
        if max < self.f_number_of_changed_agents[t - past]:
          max = self.f_number_of_changed_agents[t - past]
        past += 1
      if (max - self.f_min_number_of_changed_agents < 3):
        saturate = True
    return saturate

  def count_changed_and_stand_agent(self, t):
    counter_of_changed_agent = 0
    counter_of_stand = 0
    i = 0
    while i < self.n_of_row:
      j = 0
      while j < self.n_of_column:
        if (self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior != self.agent_field[(t - 1) % self.F_FIELD_BUFFER_SIZE][i][j].behavior):
          counter_of_changed_agent += 1
        if (self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior == 1):
          counter_of_stand += 1
        j += 1
      i += 1
    self.f_number_of_changed_agents.append(counter_of_changed_agent)
    self.f_number_of_standing_agents.append(counter_of_stand)

  def next_step_standing_ovation_sync(self, t):
    row = 0
    while row < self.n_of_row:
      col = 0
      while col < self.n_of_column:
        self.get_neighbor_set_standing_ovation(row, col, self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col], self.agent_field[(t - 1) % self.F_FIELD_BUFFER_SIZE])
        col += 1
      row += 1

  def next_step_standing_ovation_async(self, t):
    i = 0
    while i < self.n_of_row:
      j = 0
      while j < self.n_of_column:
        self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior = self.agent_field[(t - 1) % self.F_FIELD_BUFFER_SIZE][i][j].behavior
        j += 1
      i += 1
    random.shuffle(self.f_random_order)
    for i in self.f_random_order:
      row = int(i / self.n_of_column) #整数に変換 切り捨て
      col = i % self.n_of_column
      self.get_neighbor_set_standing_ovation(row, col, self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col], self.agent_field[t % self.F_FIELD_BUFFER_SIZE])

  def next_step_sync_cone(self, t):
    row = 0
    while row < self.n_of_row:
      col = 0
      while col < self.n_of_column:
        self.get_neighbor_set_cones(row, col, self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col], self.agent_field[(t - 1) % self.F_FIELD_BUFFER_SIZE])
        col += 1
      row += 1

  def next_step_async_cone(self, t):
    i = 0
    while i < self.n_of_row:
      j = 0
      while j < self.n_of_column:
        self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior = self.agent_field[(t - 1) % self.F_FIELD_BUFFER_SIZE][i][j].behavior
        j += 1
      i += 1
    random.shuffle(self.f_random_order)
    for i in self.f_random_order:
      row = int(i / self.n_of_column) #整数に変換 切り捨て
      col = i % self.n_of_column
      self.get_neighbor_set_cones(row, col, self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col], self.agent_field[t % self.F_FIELD_BUFFER_SIZE])

  def next_step_sync_moor(self, t):
    row = 0
    while row < self.n_of_row:
      col = 0
      while col < self.n_of_column:
        self.get_neighbor_set_moor(row, col, self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col], self.agent_field[(t - 1) % self.F_FIELD_BUFFER_SIZE])
        col += 1
      row += 1

  def next_step_async_moor(self, t):
    i = 0
    while i < self.n_of_row:
      j = 0
      while j < self.n_of_column:
        self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior = self.agent_field[(t - 1) % self.F_FIELD_BUFFER_SIZE][i][j].behavior
        j += 1
      i += 1

    random.shuffle(self.f_random_order)
    for i in self.f_random_order:
      row = int(i / self.n_of_column) #整数に変換 切り捨て
      col = i % self.n_of_column
      self.get_neighbor_set_moor(row, col, self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col], self.agent_field[t % self.F_FIELD_BUFFER_SIZE])

  def next_step_sync_neumann(self, t):
    row = 0
    while row < self.n_of_row:
      col = 0
      while col < self.n_of_column:
        self.get_neighbor_set_neumann(row, col, self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col], self.agent_field[(t - 1) % self.F_FIELD_BUFFER_SIZE])
        col += 1
      row += 1

  def next_step_async_neumann(self, t):
    i = 0
    while i < self.n_of_row:
      j = 0
      while j < self.n_of_column:
        self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior = self.agent_field[(t - 1) % self.F_FIELD_BUFFER_SIZE][i][j].behavior
        j += 1
      i += 1

    random.shuffle(self.f_random_order)
    for i in self.f_random_order:
      row = int(i / self.n_of_column) #整数に変換 切り捨て
      col = i % self.n_of_column
      self.get_neighbor_set_neumann(row, col, self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col], self.agent_field[t % self.F_FIELD_BUFFER_SIZE])

  def next_step_all_sync(self, t):
    total = self.n_of_column * self.n_of_row
    old_num_of_stand = self.f_number_of_standing_agents[t - 1]
    i = 0
    while i < self.n_of_row:
      j = 0
      while j < self.n_of_column:
        observed_num_of_stand = old_num_of_stand - self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior
        current_ratio = observed_num_of_stand / total
        # print(current_ratio)
        if current_ratio >= self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].f_ratio:
          self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior = 1
        else:
          self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior = 0
        j += 1
      i += 1

  def next_step_all_async(self, t):
    total = self.n_of_column * self.n_of_row
    old_num_of_stand = self.f_number_of_standing_agents[t - 1]
    observed_num_of_stand = 0
    i = 0
    while i < self.n_of_row:
      j = 0
      while j < self.n_of_column:
        self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior = self.agent_field[(t - 1) % self.F_FIELD_BUFFER_SIZE][i][j].behavior
        j += 1
      i += 1

    for i in self.f_random_order:
      row = int(i / self.n_of_column) #整数に変換 切り捨て
      col = i % self.n_of_column
      observed_num_of_stand = old_num_of_stand - self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col].behavior
      current_ratio = observed_num_of_stand / total
      # print(current_ratio)
      if (observed_num_of_stand / total) >= self.agent_field[0][row][col].f_ratio:
        if self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col].behavior == 0:
          self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col].behavior = 1
          old_num_of_stand += 1
      else:
        if self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col].behavior == 1:
          self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col].behavior = 0
          old_num_of_stand -= 1

  def to_string_befavior(self, t):
    output = ""
    row = 0
    while row < self.n_of_row:
      col = 0
      while col < self.n_of_column:
        output += self.agent_field[t % self.F_FIELD_BUFFER_SIZE][row][col].behavior + ","
        col += 1
      output += "\n"
      row += 1
    return output

  def to_string_threshold(self):
    output = ""
    row = 0
    while row < self.n_of_row:
      col = 0
      while col < self.n_of_column:
        output += self.agent_field[0][row][col].f_ratio + ","
        col += 1
      output += "\n"
      row += 1
    return output

  def to_string_number_of_changed_agent(self):
    output = ""
    t = 0
    while t < len(self.f_number_of_standing_agents):
      output += self.f_number_of_changed_agents[t] + "\n"
      t += 1
    return output

  def to_string_number_of_stand(self):
    output = ""
    t = 0
    while t < len(self.f_number_of_changed_agents):
      output += self.f_number_of_changed_agents[t] + "\n"
      t += 1
    return output

  def to_string_time_series(self):
    output = ""
    t = 0
    while t < len(self.f_number_of_changed_agents):
      output += t + "," + self.f_number_of_changed_agents[t] + "," + self.f_number_of_standing_agents[t] + "\n"
      t += 1
    return output


  # @param t
  # @return

  def get_agent_field(self, t):
    return self.agent_field[t % self.F_FIELD_BUFFER_SIZE]

  def trial_result(self, t):
    number_of_stand = 0
    if self.f_final_time < 0:
      self.f_final_time = self.tmax - 1
      self.f_number_of_changed_agents = self.f_number_of_changed_agents[self.tmax - 1]
      number_of_stand = self.f_number_of_standing_agents[self.tmax -1]
      self.f_final_period = -1
    else:
      number_of_stand = self.f_number_of_standing_agents[self.f_final_time]
    result_str = ""
    if self.f_neighbor_type == self.STANDNIG_OVATION:
      result_str += "STANDNIG_OVATION,"
    elif self.f_neighbor_type == self.CONES:
      result_str += "CONES,"
    elif self.f_neighbor_type == self.MOOR:
      result_str += "MOOR,"
    elif self.f_neighbor_type == self.NEUMANN:
      result_str += "NEUMANN,"
    elif self.f_neighbor_type == self.ALL:
      result_str += "ALL,"

    if self.f_is_synchronize:
      result_str += "S"
    else:
      result_str += "A"

    result_str += "," + str(self.f_width) + "," + str(self.f_final_time) + "," + str(self.f_final_number_of_changed_agents) + "," + str(number_of_stand)
    return result_str

  # This method is unusable because period is much bigger than what I expected.
  # So please use "is_saturate" method to decide the system is in periodic phase.

  def is_periodic(self, t):
    periodic = False
    is_same_number = False
    c_num_of_c_agent = self.f_number_of_changed_agents[t]
    period = 0
    time = t - 1
    while time > t - self.F_FIELD_BUFFER_SIZE:
      if c_num_of_c_agent == self.f_number_of_changed_agents[time]:
        is_same_number = True
        break
      time -= 1

    if is_same_number:
      past = 1
      while past < self.F_FIELD_BUFFER_SIZE:
        is_all_same = True
        try:
          i = 0
          while i < self.n_of_row:
            j = 0
            while j < self.n_of_column:
              if self.agent_field[t % self.F_FIELD_BUFFER_SIZE][i][j].behavior != self.agent_field[(t - past) % self.F_FIELD_BUFFER_SIZE][i][j].behavior:
                is_all_same = False
                break
              j += 1
            i += 1
        except Exception as e:
          raise e
        if is_all_same:
          periodic = True
          if period == 0:
            period = past
        past += 1
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
is_syncronize = True
str_s = ""
str_t = ""
so = StandingOvation(30, 30, 4, 3, is_syncronize, 0.0)
# StandingOvation NEUMANN

trial = 100
while trial < 102:
  if trial % 2 == 1:
    is_syncronize = True
  else:
    is_syncronize = False
  width = 0
  while width <= 100:
    neighbor_type = 0
    while neighbor_type < 4:
      if is_syncronize == True:
        str_s = "S"
      else:
        str_s = "A"
      if neighbor_type == 0:
        str_t = "STANDNIG_OVATION"
      elif neighbor_type == 1:
        str_t = "All"
      elif neighbor_type == 2:
        str_t = "NEUMANN"
      elif neighbor_type == 3:
        str_t = "MOOR"
      elif neighbor_type == 4:
        str_t = "CONES"

      d_width = width / 100.0
      so.set_new_trial(neighbor_type, is_syncronize, d_width, 0.5)
      start = int(time.time() * 1000)
      so.run_non_stop()
      end = int(time.time() * 1000)
      runTime = (end - start) / 1000.0

      # print(str_s + "\t" + str_t + "\t" + str(width) + "\t" + runTime)
      neighbor_type += 1
    width += 20
  trial += 1
