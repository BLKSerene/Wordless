#
# Wordless: Packaging Hook - pymorphy2
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

# Reference: https://github.com/pyinstaller/pyinstaller/issues/3050

import pkg_resources

def iter_entry_points(group, name = None):
    for entry_point in entry_points:
    	if entry_point.find(group) > -1:
	        entry_point_parsed = pkg_resources.EntryPoint.parse(entry_point)
	        entry_point_parsed.dist = pkg_resources.Distribution()

	        yield entry_point_parsed

entry_points = [
    'uk = pymorphy2_dicts_uk',
    'ru = pymorphy2_dicts_ru'
]

pkg_resources.iter_entry_points = iter_entry_points
