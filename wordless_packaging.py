#
# Wordless: Packaging
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import os
import platform
import time

time_start_packaging = time.time()

# Packaging
print('Packaging Wordless ...')

if platform.system() == 'Windows':
	os.system('pyinstaller -y wordless_packaging_windows.spec')
elif platform.system() == 'Darwin':
	os.system('pyinstaller -y wordless_packaging_macos.spec')

time_elapsed_packaging = time.time() - time_start_packaging
print(f'Packaging done! (In {int(time_elapsed_packaging // 60)} minutes {int(time_elapsed_packaging % 60)} seconds)')

os.chdir('dist/Wordless')

# Creating folders
print('Creating folders ...')

if not os.path.exists('Import'):
    os.mkdir('Import')
if not os.path.exists('Export'):
    os.mkdir('Export')

# Testing
print('Running Wordless ...')

os.system('Wordless.exe')
