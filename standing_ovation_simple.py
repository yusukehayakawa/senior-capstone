import agent
import time
import random
import sys
import math

class StandingOvationSimple(object):
  def __init__(self, n_column, n_row, tmax):

    self.n_of_column = n_column
    self.n_of_row = n_row
    self.tmax = tmax
    # agent_field[0~1][row][col]作成
    self.agent_field = [[[0+row for row in range(n_row)] for col in range(n_column) ] for k in range(2)]
    self.f_random_order = []
    self.f_random = int(time.time() * 1000)

    count = 0
    row = 0
    while row < n_row:
      col = 0
      while col < n_column:
        self.f_random_order.append(count)
        self.agent_field[0][row][col] = agent.Agent(0, 0.0)
        self.agent_field[1][row][col] = agent.Agent(0, 0.0)
        count += 1
        col += 1
      row += 1
    self.set_new_trial()

  def set_new_trial(self):
    size_half = len(self.f_random_order) / 2

    counter = 0
    random.shuffle(self.f_random_order)
    for i in self.f_random_order:
      row = int(i / self.n_of_column) #整数に変換 切り捨て
      col = i % self.n_of_column
      if counter < size_half:
        behavior = 1
      else:
        behavior = 0
      self.agent_field[0][row][col].behavior = behavior
      self.agent_field[0][row][col].f_ratio = 0.5
      self.agent_field[1][row][col].behavior = behavior
      self.agent_field[1][row][col].f_ratio = 0.5

      counter += 1

  def run(self):
    t = 1
    while t < self.tmax:
      self.next_step(t)
      t += 1
      # if t % 1 == 0:
      #   self.print_behavior(t)

  def print_behavior(self, time):
    row = 0
    while row < self.n_of_row:
      col = 0
      while col < self.n_of_column:
        if self.agent_field[time % 2][row][col].behavior == 0:
          print("_,", end="")
        else:
          print("0,", end="")
        col += 1
      sys.stdout.write('\n')
      row += 1
    sys.stdout.write('\n')

  def next_step(self, t):
    self.next_step_standing_ovation_sync(t)

  def get_neibor_set_standing_ovation(self, row, col, agent, agent_field):
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

  def next_step_standing_ovation_sync(self, t):
    row = 0
    while row < self.n_of_row:
      col = 0
      while col < self.n_of_column:
        self.get_neibor_set_standing_ovation(row, col, self.agent_field[t % 2][row][col], self.agent_field[(t - 1) % 2])
        col += 1
      row += 1

  def get_agent_field(self, t):
    return self.agent_field[t % 2]

is_syncronize = True
so = StandingOvationSimple(30, 30, 3)
start = time.time() * 1000
so.run()
end = time.time() * 1000
run_time = (end - start) / 1000.0
print(run_time)
