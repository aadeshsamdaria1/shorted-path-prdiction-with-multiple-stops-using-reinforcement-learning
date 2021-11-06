#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


environment_rows = 11
environment_columns = 11
# setting up the q_values of the map
actions = ['up', 'right', 'down', 'left'] # possible actions
rewards = np.full((environment_rows, environment_columns), -100.) # setting map element reward
aisles = {}
aisles[1] = [i for i in range(1, 9)]
aisles[2] = [1, 7, 9]
aisles[3] = [i for i in range(1, 8)]
aisles[3].append(9)
aisles[4] = [3, 7, 9]
aisles[5] = [i for i in range(11)]
aisles[6] = [2, 5, 8]
aisles[7] = [i for i in range(1, 10)]
aisles[8] = [3, 7, 10]
aisles[9] = [i for i in range(11)]
aisles[10] = [0, 4, 7, 10]

#set the rewards for all aisle locations (i.e., white squares)
for row_index in range(1, 10):
  for column_index in aisles[row_index]:
    rewards[row_index, column_index] = -1.

#display rewards matrix
mp = []
final_reward = rewards
for reward in rewards:
    mp.append(reward)

df = pd.DataFrame(mp)

sns.heatmap(df, linewidths=0.5)


def is_terminal_state(current_row_index, current_column_index):
  if rewards[current_row_index, current_column_index] == -1.:
    return False
  else:
    return True

def get_starting_location():
  current_row_index = np.random.randint(environment_rows)
  current_column_index = np.random.randint(environment_columns)
  while is_terminal_state(current_row_index, current_column_index):
    current_row_index = np.random.randint(environment_rows)
    current_column_index = np.random.randint(environment_columns)
  return current_row_index, current_column_index

def get_next_action(current_row_index, current_column_index, epsilon):
  if np.random.random() < epsilon:
    return np.argmax(q_values[current_row_index, current_column_index])
  else:
    return np.random.randint(4)

def get_next_location(current_row_index, current_column_index, action_index):
  new_row_index = current_row_index
  new_column_index = current_column_index
  if actions[action_index] == 'up' and current_row_index > 0:
    new_row_index -= 1
  elif actions[action_index] == 'right' and current_column_index < environment_columns - 1:
    new_column_index += 1
  elif actions[action_index] == 'down' and current_row_index < environment_rows - 1:
    new_row_index += 1
  elif actions[action_index] == 'left' and current_column_index > 0:
    new_column_index -= 1
  return new_row_index, new_column_index

def get_shortest_path(start_row_index, start_column_index):
  if is_terminal_state(start_row_index, start_column_index):
    return []
  else:
    current_row_index, current_column_index = start_row_index, start_column_index
    shortest_path = []
    shortest_path.append([current_row_index, current_column_index])
    while not is_terminal_state(current_row_index, current_column_index):
      action_index = get_next_action(current_row_index, current_column_index, 1.)
      current_row_index, current_column_index = get_next_location(current_row_index, current_column_index, action_index)
      shortest_path.append([current_row_index, current_column_index])
    return shortest_path


#define training parameters
def train():
    epsilon = 0.9
    discount_factor = 0.9
    learning_rate = 0.9
    for episode in range(1000):
      row_index, column_index = get_starting_location()
      while not is_terminal_state(row_index, column_index):
        action_index = get_next_action(row_index, column_index, epsilon)
        old_row_index, old_column_index = row_index, column_index
        row_index, column_index = get_next_location(row_index, column_index, action_index)
        reward = rewards[row_index, column_index]
        old_q_value = q_values[old_row_index, old_column_index, action_index]
        temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value
        new_q_value = old_q_value + (learning_rate * temporal_difference)
        q_values[old_row_index, old_column_index, action_index] = new_q_value

    print('Training complete!')


starting_point = [5,10]
stops = [[9,0], [2,9], [4,3]]
current_stop = starting_point
final_path_array = []

for k,v in stops:
    rewards[k, v] = 100.


for i in stops:
q_values = np.zeros((environment_rows, environment_columns, 4))
train()
shortest_path = get_shortest_path(current_stop[0], current_stop[1])
print(shortest_path)
final_path_array.append(shortest_path)
current_stop = shortest_path[-1]
rewards[current_stop[0], current_stop[1]] = -1

for i in final_path_array:
for k,v in i:
    final_reward[k,v] = 50
for k,v in stops:
 final_reward[k,v] = 100
final_reward[starting_point[0],starting_point[1]] = 10

print(final_reward)


mp = []
for reward in final_reward:
    mp.append(reward)

df = pd.DataFrame(mp)

sns.heatmap(df, linewidths=0.5)
