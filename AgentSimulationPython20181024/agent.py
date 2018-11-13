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





# self.f_sort_of_neighbor = [ 1, 2, 6, 10, 12, 10, 6, 2, 1 ]
# def simulation_uniform_neighbor():
#   for a in range(8, 0, -1):
#     for b in range(0, f_sort_of_neighbor[a], 1):
#       run(a, b, neighbor_type)

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
