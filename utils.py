def coverage_collect(data, fi, disc_list, disc_times, disc_count, freq_list=None, xoffset=20, yoffset=20):
	if(data != "" and data != "r\n"):
		res = data.split(" ")

		x_coord = int(float(res[1]) + xoffset)
		y_coord = int(float(res[2]) + yoffset)

		if(freq_list != None):
			freq_list[fi][x_coord][y_coord] += 1
		current_cell = disc_list[fi][x_coord][y_coord]

		# I think we're accidentally colouring previously discovered cells, but I'm having a hard time proving it
		# Unit test time!
		if(current_cell < 0.1):
			disc_count[fi] += 1
			# state which cell was discoverd
			# undo the offset
			disc_list[fi][x_coord][y_coord] = res[0]
			# append when this new cell was discovered
			disc_times[fi].append(res[0])