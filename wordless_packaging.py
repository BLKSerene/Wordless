#
# Wordless: Packaging - Packaging Script
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

def print_with_elapsed_time(message):
    print(f'[{datetime.timedelta(seconds = round(time.time() - time_start))}] {message}')

time_start = time.time()

# Package
print_with_elapsed_time('Start packaging ...')

if platform.system() == 'Windows':
    return_val_packaging = subprocess.call('pyinstaller --noconfirm wordless_packaging.spec', shell = True)
elif platform.system() == 'Darwin':
    return_val_packaging = subprocess.call('python3 -m PyInstaller --noconfirm wordless_packaging.spec', shell = True)
elif platform.system() == 'Linux':
    subprocess.call('python3.7 -m PyInstaller --noconfirm wordless_packaging.spec', shell = True)

if return_val_packaging == 0:
    print_with_elapsed_time('Packaging done!')

    # Create folders
    print_with_elapsed_time('Creating folders ...')

    if not os.path.exists('dist/Wordless/Import'):
        os.mkdir('dist/Wordless/Import')
    if not os.path.exists('dist/Wordless/Export'):
        os.mkdir('dist/Wordless/Export')

    # Copy files
    if platform.system() == 'Darwin':
        for dir_src, dirs, files in os.walk('dist/Wordless/'):
            dir_src = os.path.realpath(dir_src)
            dir_app = dir_src.replace('dist/Wordless', 'dist/Wordless.app/Contents/MacOS')

            print_with_elapsed_time(f'Copying folder {dir_app} ...')

            if not os.path.exists(dir_app):
                os.mkdir(dir_app)

            for file in files:
                path_src = os.path.join(dir_src, file)
                path_app = os.path.join(dir_app, file)

                if not os.path.exists(path_app):
                    shutil.copy(path_src, path_app)

        print_with_elapsed_time(f'Finished copying all files!')

    # Test
    print_with_elapsed_time(f'Testing ...')

    if platform.system() == 'Windows':
        os.chdir('dist/Wordless')

        return_val_test = subprocess.call(os.path.join(os.getcwd(), 'Wordless.exe'), shell = True)
    elif platform.system() == 'Darwin':
        return_val_test = subprocess.call(os.path.join(os.getcwd(), 'Wordless.app/Contents/Macos/Wordless'), shell = True)
    elif platform.system() == 'Linux':
        os.chdir('dist/Wordless')

        return_val_test = subprocess.call('./Wordless', shell = True)

    if return_val_test == 0:
        print_with_elapsed_time(f'Pass!')
    else:
        print_with_elapsed_time(f'Fail!')
else:
    print_with_elapsed_time(f'Packaging failed!')
