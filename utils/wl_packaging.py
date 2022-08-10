# ----------------------------------------------------------------------
# Utilities: Packaging - Packaging Script
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

import datetime
import os
import platform
import subprocess
import time

def print_with_elapsed_time(message):
    print(f'[{datetime.timedelta(seconds = round(time.time() - time_start))}] {message}')

# Version number
with open('src/VERSION', 'r', encoding = 'utf_8') as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            wl_ver = line.strip()

time_start = time.time()

# Package
print_with_elapsed_time('Start packaging...')

if platform.system() == 'Windows':
    return_val_packaging = subprocess.call('pyinstaller --noconfirm --clean wl_packaging.spec', shell = True)
elif platform.system() == 'Darwin':
    return_val_packaging = subprocess.call('python3 -m PyInstaller --noconfirm --clean wl_packaging.spec', shell = True)
elif platform.system() == 'Linux':
    return_val_packaging = subprocess.call('python3.8 -m PyInstaller --noconfirm --clean wl_packaging.spec', shell = True)

if return_val_packaging == 0:
    print_with_elapsed_time('Packaging done!')

    # Create folders
    if platform.system() in ['Windows', 'Linux']:
        os.makedirs('dist/Wordless/imports')
        os.makedirs('dist/Wordless/exports')
    elif platform.system() == 'Darwin':
        os.makedirs('dist/Wordless.app/Contents/Macos/imports')
        os.makedirs('dist/Wordless.app/Contents/Macos/exports')

    # Compress files
    print_with_elapsed_time('Compressing files... ')

    os.chdir('dist')

    if platform.system() == 'Windows':
        # "7z.exe" and "7z.dll" should be put under "C:\Windows\System32" first
        subprocess.call(f'7z a -tzip -mx9 wordless_{wl_ver}_windows.zip Wordless/', shell = True)
    elif platform.system() == 'Darwin':
        subprocess.call(f'ditto -c -k --sequesterRsrc --keepParent Wordless.app/ wordless_{wl_ver}_macos.zip', shell = True)
    elif platform.system() == 'Linux':
        subprocess.call(f'tar -czvf wordless_{wl_ver}_linux.tar.gz Wordless/', shell = True)

    print_with_elapsed_time('Compressing done!')

    # Test Wordless
    print_with_elapsed_time('Testing Wordless... ')

    if platform.system() == 'Windows':
        os.chdir('Wordless')
        return_val_test = subprocess.call(os.path.join(os.getcwd(), 'Wordless.exe'), shell = True)
    elif platform.system() == 'Darwin':
        return_val_test = subprocess.call(os.path.join(os.getcwd(), 'Wordless.app/Contents/Macos/Wordless'), shell = True)
    elif platform.system() == 'Linux':
        os.chdir('Wordless')
        return_val_test = subprocess.call('./Wordless', shell = True)

    # Remove custom settings file
    if platform.system() in ['Windows', 'Linux']:
        if os.path.exists('wl_settings.pickle'):
            os.remove('wl_settings.pickle')

        if os.path.exists('wl_settings_display_lang.pickle'):
            os.remove('wl_settings_display_lang.pickle')
    elif platform.system() == 'Darwin':
        if os.path.exists('Wordless.app/Contents/Macos/wl_settings.pickle'):
            os.remove('Wordless.app/Contents/Macos/wl_settings.pickle')

        if os.path.exists('Wordless.app/Contents/Macos/wl_settings_display_lang.pickle'):
            os.remove('Wordless.app/Contents/Macos/wl_settings_display_lang.pickle')

    if return_val_test == 0:
        print_with_elapsed_time('Testing passed!')
    else:
        print_with_elapsed_time('Testing failed!')
else:
    print_with_elapsed_time('Packaging failed!')
