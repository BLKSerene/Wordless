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

import datetime
import os
import platform
import shutil
import subprocess
import time

time_start = time.time()

# Package
print(f'[{datetime.timedelta(seconds = round(time.time() - time_start))}] Packaging Wordless ...')

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

print(f'[{datetime.timedelta(seconds = round(time.time() - time_start))}] Packaging completed successfully!')

os.chdir('dist/Wordless')

# Create folders
if not os.path.exists('Import') or not os.path.exists('Export'):
    print(f'[{datetime.timedelta(seconds = round(time.time() - time_start))}] Creating folders ...')

    if not os.path.exists('Import'):
        os.mkdir('Import')
    if not os.path.exists('Export'):
        os.mkdir('Export')

# Copy files
if platform.system() == 'Darwin':
    for dir_src, dirs, files in os.walk('.'):
        dir_src = os.path.realpath(dir_src)
        dir_app = dir_src.replace('dist/Wordless', 'dist/Wordless.app/Contents/MacOS')

        print(f'[{datetime.timedelta(seconds = round(time.time() - time_start))}] Copying folder {dir_app} ...')

        if not os.path.exists(dir_app):
            os.mkdir(dir_app)

        for file in files:
            path_src = os.path.join(dir_src, file)
            path_app = os.path.join(dir_app, file)

            if not os.path.exists(path_app):
                shutil.copy(path_src, path_app)

    print(f'[{datetime.timedelta(seconds = round(time.time() - time_start))}] Finished copying all files!')

# Testing
print(f'[{datetime.timedelta(seconds = round(time.time() - time_start))}] Running Wordless ...')

if platform.system() == 'Windows':
    os.system('start Wordless.exe')
elif platform.system() == 'Darwin':
    os.chdir('..')

    subprocess.call(['open', './Wordless.app'])
elif platform.system() == 'Linux':
    os.system('./Wordless')
