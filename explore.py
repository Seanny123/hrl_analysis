import sys
import ipdb
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose',
     color_scheme='Linux', call_pdb=1)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

import utils

file_list = []
filename_list = []
name_list = []
node_types = 2
run_nums = 2
node_name_list = ["noiseless", "with noise"]

for node_type in range(node_types):
	for run_num in range(run_nums):
		file_list.append(
			open("data_%s_easygrid.txt_0.0_%s.txt" %(run_num, node_type),"r").read().split("\n")
		)
		filename_list.append("data_%s_easygrid.txt_0.0_%s.txt" %(run_num, node_type))
		name_list.append("%s trial %s" %(node_name_list[node_type], run_num))


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
		utils.coverage_collect(t, fi, disc_list, disc_times, disc_count, freq_list)

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
	xtick_loc = np.concatenate((xtick_loc,tmp)
	)


plt.legend(plt_list, node_name_list, loc=3)
plt.xticks(xtick_loc, name_list, rotation="vertical")
fig.savefig("total_explored.png")

"""
# Alternatively, if you do get paranoid and run more tests, here's the code for summarizing the data too
plt.figure()
inc = 1
for node in range(node_types):
	node_std = np.std(disc_count[node*run_nums:(node+1)*run_nums])
	node_mean = np.mean(disc_count[node*run_nums:(node+1)*run_nums])
	plt.bar(node*inc, node_mean, yerr=node_std)
plt.xticks(np.arange(0, node_types, inc), node_name_list)
#plt.show()
"""

# Plot the rates of discovery
plt.figure()
for i, times in enumerate(disc_times):
	#ipdb.set_trace()
	plt.plot(times, np.arange(1, len(disc_times[i])+1), label=name_list[i])
plt.legend(loc=4)
fig.savefig("exploration_rate.png")


for node in range(4):
	fig = plt.figure()
	bounds=[0, 0.1, 10000]
	# Associate it to a colour
	cmap = mpl.colors.ListedColormap(['white', 'red'])
	norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
	img = plt.imshow(disc_list[node][4:15,5:17], interpolation='nearest', cmap=cmap, norm=norm, origin='lower')
	#plt.xticks(np.arange(grid_width))
	#plt.yticks(np.arange(grid_height))
	plt.grid(True,color='green')
	fig.savefig("explored%s.png" %node)

# Plot the distribution of discovery
for test in range(node_types+run_nums):
	fig = plt.figure()
	disc_avg = disc_list[test]
	# Associate it to a colour
	cmap = mpl.colors.LinearSegmentedColormap.from_list('my_colormap', ['white', 'blue','red'], 256)
	img = plt.imshow(disc_avg[4:15,5:17], interpolation='nearest', cmap=cmap, origin='lower')
	#plt.xticks(np.arange(grid_width))
	#plt.yticks(np.arange(grid_height))
	plt.colorbar(img, cmap=cmap)
	fig.savefig("disc%s.png" %test)

# plot frequency of discovery
for test in range(node_types+run_nums):
		fig = plt.figure()
		# Associate it to a colour
		cmap = mpl.colors.LinearSegmentedColormap.from_list('my_colormap', ['white','blue','red'], 256)
		img = plt.imshow(freq_list[test][4:15,5:17], interpolation='nearest', cmap=cmap, origin='lower')
		#plt.xticks(np.arange(grid_width))
		#plt.yticks(np.arange(grid_height))
		plt.colorbar(img, cmap=cmap)
		fig.savefig("freq%s.png" %test)