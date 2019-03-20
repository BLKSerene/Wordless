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
import shutil
import subprocess
import time

time_start_packaging = time.time()

# Package
print('Packaging Wordless ...')

if platform.system() == 'Windows':
    os.system('python -m PyInstaller -y wordless_packaging.spec')
elif platform.system() == 'Darwin':
    subprocess.call([
        'python3',
        '-m',
        'PyInstaller',
        '-y',
        'wordless_packaging.spec'
    ])
elif platform.system() == 'Linux':
    os.system('python3.7 -m PyInstaller -y wordless_packaging.spec')

time_elapsed_packaging = time.time() - time_start_packaging
print(f'Packaging done! (In {int(time_elapsed_packaging // 60)} minutes {int(time_elapsed_packaging % 60)} seconds)')

os.chdir('dist/Wordless')

# Create folders
if not os.path.exists('Import') or not os.path.exists('Export'):
    print('Creating folders ...')

    if not os.path.exists('Import'):
        os.mkdir('Import')
    if not os.path.exists('Export'):
        os.mkdir('Export')

# Copy files
if platform.system() == 'Darwin':
    time_start_copy_files = time.time()

    for dir_src, dirs, files in os.walk('.'):
        dir_src = os.path.realpath(dir_src)
        dir_app = dir_src.replace('dist/Wordless', 'dist/Wordless.app/Contents/MacOS')

        print(f'Copying folder {dir_app} ...')

        if not os.path.exists(dir_app):
            os.mkdir(dir_app)

        for file in files:
            path_src = os.path.join(dir_src, file)
            path_app = os.path.join(dir_app, file)

            if not os.path.exists(path_app):
                shutil.copy(path_src, path_app)

    time_elapsed_copy_files = time.time() - time_start_copy_files
    print(f'Finished copying all files! (In {int(time_elapsed_copy_files // 60)} minutes {int(time_elapsed_copy_files % 60)} seconds)')

# Testing
print('Running Wordless ...')

if platform.system() == 'Windows':
    os.system('start Wordless.exe')
elif platform.system() == 'Darwin':
    os.chdir('..')

    subprocess.call(['open', './Wordless.app'])
elif platform.system() == 'Linux':
    os.system('./Wordless')
