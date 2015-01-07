import sys
import ipdb
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose',
     color_scheme='Linux', call_pdb=1)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

import utils

file_list = []
filename_list = []
name_list = []
file_info = {
	"directed": {
			"node_types": 2,
			"run_nums": 3,
			"data_list": {
				"6_6_cornergoals.txt": [],
				"easy_cornergoals.txt": []
			},
			"reward_list": {
				"6_6_cornergoals.txt": [],
				"easy_cornergoals.txt": []
			},
			"node_name_list": ["error", "state"]
		},
	"time": {
			"node_types": 3,
			"run_nums": 3,
			"data_list": {
				"6_6_cornergoals.txt": [],
				"easy_cornergoals.txt": []
			},
			"reward_list": {
				"6_6_cornergoals.txt": [],
				"easy_cornergoals.txt": []
			},
			"node_name_list": ["normal", "exponentional", "linear"]
		}
}

node_types = 2
run_nums = 3
grid_name_list = ["6_6_cornergoals.txt", "easy_cornergoals.txt"]
node_name_list = ["error", "state", "normal", "exponentional", "linear"]

for fi, info in file_info.iteritems():
	for node_type in range(info["node_types"]):
		for run_num in range(info["run_nums"]):
			for file_name, file_list in info["data_list"].iteritems():
				file_list.append(
					open(os.path.join("new",fi,"data_%s_%s_-0.05_%s.txt" %(run_num, file_name, node_type)), "r"
						).read().split("\n")
				)
			for file_name, file_list in info["reward_list"].iteritems():
				file_list.append(
					open(os.path.join("new",fi,"reward_%s_%s_-0.05_%s.txt" %(run_num, file_name, node_type)), "r"
						).read().split(";")
				)

# Get the total accumulated reward for each
acc_reward_list = {
	"6_6_cornergoals.txt": [],
	"easy_cornergoals.txt": []
}
avg_acc = {
	"6_6_cornergoals.txt": [],
	"easy_cornergoals.txt": []
}

name_list = []
fi = 0
last_length = 0

total_length = 0
for group, info in file_info.iteritems():
	total_length += info["node_types"]*info["run_nums"]
disc_times = [[] for i in range(len(file_list))]
# which cells were discovered
disc_list = []
disc_count = [0 for _ in range(len(file_list))]
grid_width = 20
grid_height = 20

for group, info in file_info.iteritems():
	curr_offset = fi*last_length
	name_list.appnd(info["node_name_list"])
	for grid, r_lists in info["reward_list"].iteritems():

		# get the reward accumulation
		for list_index, r_list in enumerate(r_lists):
			acc_reward_list[grid].append(
				np.zeros(len(r_list)+1),
				dtype=np.float64
			)
			# because otherwise accessing the correct index is painful
			acc_reward = acc_reward_list[grid][list_index+curr_offset]

			for line_index in range(len(r_list)):
				res = r_list[line_index].split(" ")
				# add to the current accumulated reward, the previous accumulated reward and the new reward
				acc_reward[line_index+1] = acc_reward[line_index] + res[1]

		# now get the average
		# assuming each file has a uniform number of runs
		for ai in np.arange(0, len(acc_reward_list[grid])-info["run_nums"], info["run_nums"]):
			avg_acc[grid].append(
				np.mean(
					acc_reward_list[ai+curr_offset:ai+info["run_nums"]+curr_offset],
					)
				)

		# now get the coverage
		for grid, d_lists in info["data_list"].iteritems():
			for di, d_list in enumerate(d_lists):
				disc_list.append(np.zeros((grid_width, grid_height), dtype=np.float64))
				for data in d_list:
					# No need to grab the frequency, because that's obviously going to depend on the reward
					utils.coverage_collect(data, di+curr_offset, disc_list, disc_times, disc_count)
	fi += 1
	last_length = info["node_types"]*info["run_nums"]


# plot the reward accumulation
period = 0.5
x_vals = np.arange(0.0, len(acc_reward_list["6_6_cornergoals.txt"][0]), 5)
for grid, r_lists in acc_reward_list.iteritems():
	fig = plt.figure()
	for ri, r_list in enumerate(r_lists):
		plt.plot(x_vals, r_list, label=name_list[ri])
	fig.savefig("reward_%s.png" %grid)

# plot the exploration
fig = plt.figure()
fi = 0
last_length = 0
for group, info in file_info.iteritems():
	run_nums = info["run_nums"]
	for node in range(info["node_types"]):
		node_std = np.std(disc_count[node*run_nums:(node+1)*run_nums])
		node_mean = np.mean(disc_count[node*run_nums:(node+1)*run_nums])
		plt.bar(node*inc, node_mean, yerr=node_std)
	fi += 1
	last_length = info["node_types"]*info["run_nums"]
plt.xticks(np.arange(0, node_types, inc), node_name_list)
fig.savefig("average_with_reward_explore.png")

# And if we're really ambitious, find a measure for the amount of clustering
# Which I guess is the amount of area enclosed?