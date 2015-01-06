import sys
import ipdb
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose',
     color_scheme='Linux', call_pdb=1)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

file_list = []
filename_list = []
name_list = []
node_types = 2
run_nums =2
node_name_list = ["noiseless", "with noise"]

for node_type in range(node_types):
	for run_num in range(run_nums):
		file_list.append(
			open("data_%s_easygrid.txt_0.0_%s.txt" %(run_num, node_type),"r").read().split("\n")
		)
		filename_list.append("data_%s_easygrid.txt_0.0_%s.txt" %(run_num, node_type))
		node_name = node_name_list[node_type]
		name_list.append("%s trial %s" %(node_name, run_num))
#ipdb.set_trace()


# Should I be using numpy here?

grid_width = 20
grid_height = 20
xoffset = grid_width/2
yoffset = grid_height/2
x_list = []
y_list = []
# when the cells were discovered
disc_times = [[] for i in range(len(file_list))]
# which cells were discovered
disc_list = []
# how often cells were visited
freq_list = []
disc_count = [0 for _ in range(len(file_list))]
# get the discovery time of all these mofos
for fi in range(len(file_list)):
	disc_list.append(np.zeros((grid_width, grid_height), dtype=np.float64))
	freq_list.append(np.zeros((grid_width, grid_height), dtype=np.float64))
	for t in file_list[fi]:
		if(t != "" and t != "r\n"):
			res = t.split(" ")

			x_coord = int(float(res[1]) + xoffset)
			y_coord = int(float(res[2]) + yoffset)

			freq_list[fi][x_coord][y_coord] += 1
			current_cell = disc_list[fi][x_coord][y_coord]

			# I think we're accidentally colouring previously discovered cells, but I'm having a hard time proving it
			# Unit test time!
			if(current_cell < 0.1):
				disc_count[fi] += 1
				# state which cell was discoverd
				# undo the offset
				x_list.append(x_coord)
				y_list.append(y_coord)
				disc_list[fi][x_coord][y_coord] = res[0]
				# append when this new cell was discovered
				disc_times[fi].append(res[0])
print("xmin: %s, xmax %s" %(min(x_list), max(x_list)))
print("ymin: %s, ymax %s" %(min(y_list), max(y_list)))


# Plot the total discovery as "trial 1, trial 2", since there's no reason to hide the data and showing the average would probably be a bit annoying
fig = plt.figure()
xtick_loc = np.array([])
bar_width = 0.35
inc = 0.5
colour_list = ['r', 'b']
plt_list = [0 for _ in range(node_types)]

for node in range(node_types):
	plt_list[node] = plt.bar(
		np.arange(
			node*(run_nums*bar_width+inc),
			(node+1)*run_nums*bar_width+inc*node,
			bar_width
		), 
		disc_count[node*run_nums:(node+1)*run_nums],
		bar_width,
		color=colour_list[node]
	)
	tmp = np.arange(
				bar_width/2.0+node*(run_nums*bar_width+inc),
				(node+1)*run_nums*bar_width+inc*node+bar_width/2.0,
				bar_width
			)
	xtick_loc = np.concatenate(
		(xtick_loc,
		tmp)
	)

plt.legend(plt_list, node_name_list, loc=3)
plt.xticks(xtick_loc, name_list, rotation="vertical")
plt.show()