import ipdb
import sys
import os
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose',
     color_scheme='Linux', call_pdb=1)

file_list = []
name_list = []

for run_num in range(2):
	for node_type in range(2):
		file_list.append(
			open("data_%s_3_3_nogrid_goal.txt_0.0_%s.txt" %(run_num, node_type), "r").read().split("\n")
		)
		name_list.append("data_%s_3_3_nogrid_goal.txt_0.0_%s.txt" %(run_num, node_type))

grid_width = 3
grid_height = 3
complete = [[1 for _ in range(grid_width)] for _ in range(grid_height)]

total_count = [0 for _ in range(len(file_list))]
for fi in range(len(file_list)):
	state_list = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
	for t in file_list[fi]:
		total_count[fi] += 1
		res = t.split(" ")
		state_list[int(float(res[1]))][int(float(res[2]))] = 1
		if(state_list == complete):
			break

# copy the other code from elsewhere