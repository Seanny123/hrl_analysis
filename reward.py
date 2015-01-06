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
run_nums = 3
directed_node_name_list = ["error", "state"]
time_node_name_list = ["normal", "exponentional", "linear"]

for node_type in range(node_types):

# Get the total accumulated reward for each
# Average it over the types of runs
# Also get the exploration coverage of both
# No need to grab the frequency, because that's obviously going to depend on the reward