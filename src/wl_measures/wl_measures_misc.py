#
# Wordless: Measures - Miscellaneous
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import numpy

def modes(inputs):
	inputs_modes = []

	unique, unique_counts = numpy.unique(inputs, return_counts = True)
	unique_counts_max = numpy.max(unique_counts)

	for val, freq in zip(unique, unique_counts):
		if freq == unique_counts_max:
			inputs_modes.append(val)

	return inputs_modes
