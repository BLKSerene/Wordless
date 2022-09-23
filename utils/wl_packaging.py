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
import shutil
import subprocess
import time

import wl_utils

def print_with_elapsed_time(message):
    print(f'[{datetime.timedelta(seconds = round(time.time() - time_start))}] {message}')

is_windows, is_macos, is_linux = wl_utils.check_os()
wl_ver = wl_utils.check_os()
time_start = time.time()

# Package
print_with_elapsed_time('Start packaging...')

if is_windows:
    subprocess.run(['python', '-m', 'PyInstaller', '--clean', '--noconfirm', 'wl_packaging.spec'], check = True)
elif is_macos:
    subprocess.run(['python3', '-m', 'PyInstaller', '--clean', '--noconfirm', 'wl_packaging.spec'], check = True)
elif is_linux:
    subprocess.run(['python3.8', '-m', 'PyInstaller', '--clean', '--noconfirm', 'wl_packaging.spec'], check = True)

# Create folders
if is_windows or is_linux:
    os.makedirs('dist/Wordless/imports')
    os.makedirs('dist/Wordless/exports')
elif is_macos:
    os.makedirs('dist/Wordless.app/Contents/Macos/imports')
    os.makedirs('dist/Wordless.app/Contents/Macos/exports')

# Running on Linux requires sudo
if is_linux:
    with open('dist/Wordless/Wordless.sh', 'w', encoding = 'utf_8') as f:
        f.write('#!/bin/bash\n')
        # Fix libGL error on Linux
        f.write('sudo LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6 ./Wordless\n')

    # Allow excuting file as program
    subprocess.run(['chmod', '+x', 'dist/Wordless/Wordless.sh'], check = True)

    # Create .desktop file
    subprocess.run(['python3.8', '-m', 'PyInstaller', '--clean', '--noconfirm', 'linux_create_shortcut.py'], check = True)
    shutil.copyfile('dist/linux_create_shortcut/linux_create_shortcut', 'dist/Wordless/Wordless - Create Shortcut')
    subprocess.run(['chmod', '+x', 'dist/Wordless/Wordless - Create Shortcut'], check = True)

print_with_elapsed_time('Packaging done!')

# Test Wordless
print_with_elapsed_time('Testing Wordless... ')

if is_windows or is_linux:
    os.chdir('dist/Wordless')
elif is_macos:
    os.chdir('dist')

if is_windows:
    subprocess.run([os.path.join(os.getcwd(), 'Wordless.exe')], check = True)
elif is_macos:
    subprocess.run([os.path.join(os.getcwd(), 'Wordless.app/Contents/Macos/Wordless')], check = True)
elif is_linux:
    subprocess.run(['./Wordless'], check = True)

if is_windows or is_linux:
    os.chdir('..')

# Remove custom settings file
if is_windows or is_linux:
    if os.path.exists('wl_settings.pickle'):
        os.remove('wl_settings.pickle')

    if os.path.exists('wl_settings_display_lang.pickle'):
        os.remove('wl_settings_display_lang.pickle')
elif is_macos:
    if os.path.exists('Wordless.app/Contents/Macos/wl_settings.pickle'):
        os.remove('Wordless.app/Contents/Macos/wl_settings.pickle')

    if os.path.exists('Wordless.app/Contents/Macos/wl_settings_display_lang.pickle'):
        os.remove('Wordless.app/Contents/Macos/wl_settings_display_lang.pickle')

print_with_elapsed_time('Tests passed!')

# Compress files
print_with_elapsed_time('Compressing files... ')

if is_windows:
    # "7z.exe" and "7z.dll" should be put under "C:/Windows/System32" first
    subprocess.run(['7z', 'a', '-tzip', '-mx9', f'wordless_{wl_ver}_windows.zip', 'Wordless/'], check = True)
elif is_macos:
    subprocess.run(['ditto', '-c', '-k', '--sequesterRsrc', '--keepParent', 'Wordless.app/', f'wordless_{wl_ver}_macos.zip'], check = True)
elif is_linux:
    subprocess.run(['tar', '-czvf', f'wordless_{wl_ver}_linux.tar.gz', 'Wordless/'], check = True)

print_with_elapsed_time('Compressing done!')
