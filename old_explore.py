not_equal = []
count = 0
for i,j in zip(file_list[0], file_list[1]):
	if(i != j ):
		not_equal.append(1)
		count += 1
	else:
		not_equal.append(0)