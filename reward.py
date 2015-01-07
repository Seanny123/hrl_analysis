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
d_filename_list = []
r_filename_list = []
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
name_list = []
colour_filler = ["r", "g", "b", "m", "c"]
colour_list = []

for fi, info in file_info.iteritems():
	for node_type in range(info["node_types"]):
		for run_num in range(info["run_nums"]):
			name_list.append("%s %s" %(info["node_name_list"][node_type], run_num))
			#colour_list.append(colour_filler[node_type])

			for file_name, file_list in info["data_list"].iteritems():
				file_list.append(
					open(os.path.join("new",fi,"data_%s_%s_-0.05_%s.txt" %(run_num, file_name, node_type)), "r"
						).read().split("\n")
				)
				d_filename_list.append("data_%s_%s_-0.05_%s.txt" %(run_num, file_name, node_type))

			for file_name, file_list in info["reward_list"].iteritems():
				file_list.append(
					open(os.path.join("new",fi,"reward_%s_%s_-0.05_%s.txt" %(run_num, file_name, node_type)), "r"
						).read().split(";")
				)
				r_filename_list.append("reward_%s_%s_-0.05_%s.txt" %(run_num, file_name, node_type))

# Get the total accumulated reward for each
acc_reward_list = {
	"6_6_cornergoals.txt": [],
	"easy_cornergoals.txt": []
}
avg_acc = {
	"6_6_cornergoals.txt": [],
	"easy_cornergoals.txt": []
}
std_acc = {
	"6_6_cornergoals.txt": [],
	"easy_cornergoals.txt": []
}

fi = 0
last_length = 0

total_length = 0
for group, info in file_info.iteritems():
	total_length += info["node_types"]*info["run_nums"]

disc_times = {
	"6_6_cornergoals.txt": [[] for i in range(total_length)],
	"easy_cornergoals.txt": [[] for i in range(total_length)]
}
# which cells were discovered
disc_list = {
	"6_6_cornergoals.txt": [],
	"easy_cornergoals.txt": []
}
disc_count = {
	"6_6_cornergoals.txt":  [0 for _ in range(total_length)],
	"easy_cornergoals.txt":  [0 for _ in range(total_length)]
}
grid_width = 20
grid_height = 20

for group, info in file_info.iteritems():
	curr_offset = fi*last_length
	for grid, r_lists in info["reward_list"].iteritems():

		# get the reward accumulation
		for list_index, r_list in enumerate(r_lists):
			acc_reward_list[grid].append(
				np.zeros(
						len(r_list) + 1,
						dtype=np.float64
					),
			)
			# because otherwise accessing the correct index is painful
			acc_reward = acc_reward_list[grid][list_index+curr_offset]

			for line_index in range(len(r_list)):
				res = r_list[line_index].split(" ")
				# add to the current accumulated reward, the previous accumulated reward and the new reward
				acc_reward[line_index+1] = acc_reward[line_index] + float(res[1])

			# If no reward was accumulated at all, then something terrible has happened
			if(acc_reward[-1] < 0.1):
				print("Oh no: %s %s %s" %(group, grid, list_index))

		# now get the average
		# assuming each file has a uniform number of runs
		# OH GOD, UNIT TEST THIS
		for ai in np.arange(0, len(acc_reward_list[grid])-info["run_nums"], info["run_nums"]):
			avg_acc[grid].append(
				np.mean(
					acc_reward_list[grid][ai+curr_offset:ai+info["run_nums"]+curr_offset],
						axis=0
					)
				)
			std_acc[grid].append(
				np.mean(
					acc_reward_list[grid][ai+curr_offset:ai+info["run_nums"]+curr_offset],
						axis=0
					)
				)
			ipdb.set_trace()

		# now get the coverage
		for grid, d_lists in info["data_list"].iteritems():
			for di, d_list in enumerate(d_lists):
				disc_list[grid].append(np.zeros((grid_width, grid_height), dtype=np.float64))
				for data in d_list:
					# No need to grab the frequency, because that's obviously going to depend on the reward
					utils.coverage_collect(data, di+curr_offset, disc_list[grid], disc_times[grid], disc_count[grid])
	fi += 1
	last_length = info["node_types"]*info["run_nums"]


# plot the reward accumulation
# except for the ones that accumulated zero reward
period = 0.5
x_vals = np.arange(0.0, 5*acc_reward_list["6_6_cornergoals.txt"][0].size, 5)
for grid, r_lists in acc_reward_list.iteritems():
	fig = plt.figure()
	for ri, r_list in enumerate(r_lists):
		if(r_list[-1] > 0.1):
			plt.plot(x_vals, r_list, label=name_list[ri], color=colour_filler[ri/3])
	plt.legend(loc=0)
	fig.savefig("reward_%s.png" %grid)

# plot the average reward
period = 0.5
x_vals = np.arange(0.0, 5*acc_reward_list["6_6_cornergoals.txt"][0].size, 5)
for grid, r_lists in avg_acc.iteritems():
	fig = plt.figure()
	for ri, r_list in enumerate(r_lists):
		if(r_list[-1] > 0.1):
			plt.plot(x_vals, r_list, label=name_list[ri], color=colour_filler[ri])
			plt.fill_between(x_vals, r_list+std_acc[grid][ri], r_list-std_acc[grid][ri], facecolor=color_filler[ri], alpha=0.5)
	plt.legend(loc=0)
	fig.savefig("reward_%s.png" %grid)

# plot the exploration
fig = plt.figure()
fi = 0
last_length = 0
inc = 1
# WTF: Why am I only seeing three bars?
# OH GOD WE NEED TO SEPERATE THE GRIDS
for group, info in file_info.iteritems():
	run_nums = info["run_nums"]
	for grid in grid_name_list:
	for node in range(info["node_types"]):
		node_std = np.std(disc_count[grid][node*run_nums+curr_offset:(node+1)*run_nums+curr_offset])
		node_mean = np.mean(disc_count[grid][node*run_nums+curr_offset:(node+1)*run_nums+curr_offset])
		plt.bar(node*inc, node_mean, yerr=node_std)
	fi += 1
	last_length = info["node_types"]*info["run_nums"]
	curr_offset = fi*last_length

plt.xticks(np.arange(0, node_types, inc), node_name_list)
fig.savefig("average_with_reward_explore.png")

# And if we're really ambitious, find a measure for the amount of clustering
# Which I guess is the amount of area enclosed?