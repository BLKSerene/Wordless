# ----------------------------------------------------------------------
# Wordless: Utilities - Translation - Generate TS Files
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import os
import pathlib
import re
import subprocess

files = []

for file in pathlib.Path('../src').rglob('*.py'):
    if all([
        os.path.sep + folder + os.path.sep not in str(file)
        for folder in ['build', 'dist', 'wl_tests', 'lemmatization', 'stop_word_lists']
    ]):
        files.append(str(file))

    # Use "_tr" as a shortcut of QCoreApplication.translate
    subprocess.call(f"pylupdate5 -verbose -translate-function _tr {' '.join(files)} -ts ../src/trans/zho_cn.ts", shell = True)

# Fix HTML entities
with open(r'../src/trans/zho_cn.ts', 'r', encoding = 'utf_8') as f:
    contents = f.read()

# Replace "&amp;xxxx;" with "&xxxx;"
contents = re.sub(r'&amp;([a-z]{2,5});', r'&\1;', contents)
# Escape non-breaking spaces
contents = contents.replace(r'&nbsp', r'&amp;nbsp')

with open(r'../src/trans/zho_cn.ts', 'w', encoding = 'utf_8') as f:
    f.write(contents)
