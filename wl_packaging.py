#
# Wordless: Packaging - Packaging Script
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
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
print_with_elapsed_time('Start packaging...')

if platform.system() == 'Windows':
    return_val_packaging = subprocess.call('pyinstaller --noconfirm wl_packaging.spec', shell = True)
elif platform.system() == 'Darwin':
    return_val_packaging = subprocess.call('python3 -m PyInstaller --noconfirm wl_packaging.spec', shell = True)
elif platform.system() == 'Linux':
    return_val_packaging = subprocess.call('python3.8 -m PyInstaller --noconfirm wl_packaging.spec', shell = True)

if return_val_packaging == 0:
    print_with_elapsed_time('Packaging done!')

    # Create folders
    os.makedirs('dist/Wordless/Import', exist_ok = True)
    os.makedirs('dist/Wordless/Export', exist_ok = True)

    if platform.system() == 'Windows':
        # Compress files
        print_with_elapsed_time('Compressing files...')

        os.chdir('dist')
        if os.path.exists('Wordless_windows.zip'):
            os.remove('Wordless_windows.zip')
        # "7z.exe" and "7z.dll" should be put under "C:\Windows\System32" first
        subprocess.call('7z a -tzip -mx9 wordless_windows.zip Wordless/', shell = True)

        print_with_elapsed_time('Compressing done!')

        # Test
        print_with_elapsed_time(f'Start testing...')

        os.chdir('Wordless')
        return_val_test = subprocess.call(os.path.join(os.getcwd(), 'Wordless.exe'), shell = True)

        # Remove custom settings file
        if os.path.exists('wl_settings.pickle'):
            os.remove('wl_settings.pickle')
    elif platform.system() == 'Darwin':
        # Compress files
        print_with_elapsed_time('Compressing files...')

        os.chdir('dist')
        if os.path.exists('Wordless_macos.zip'):
            os.remove('Wordless_macos.zip')
        subprocess.call('ditto -c -k --sequesterRsrc --keepParent Wordless.app/ wordless_macos.zip', shell = True)

        print_with_elapsed_time('Compressing done!')

        # Test
        print_with_elapsed_time(f'Start testing...')

        return_val_test = subprocess.call(os.path.join(os.getcwd(), 'Wordless.app/Contents/Macos/Wordless'), shell = True)

        # Remove custom settings file
        if os.path.exists('Wordless.app/Contents/Macos/wl_settings.pickle'):
            os.remove('Wordless.app/Contents/Macos/wl_settings.pickle')
    elif platform.system() == 'Linux':
        # Compress files
        print_with_elapsed_time('Compressing files...')

        os.chdir('dist')
        subprocess.call('tar -czvf wordless_linux.tar.gz Wordless/', shell = True)

        print_with_elapsed_time('Compressing done!')

        # Test
        print_with_elapsed_time(f'Start testing...')

        os.chdir('Wordless')
        return_val_test = subprocess.call('./Wordless', shell = True)

        # Remove custom settings file
        if os.path.exists('wl_settings.pickle'):
            os.remove('wl_settings.pickle')

    if return_val_test == 0:
        print_with_elapsed_time(f'Testing passed!')
    else:
        print_with_elapsed_time(f'Testing failed!')
else:
    print_with_elapsed_time(f'Packaging failed!')
