# ----------------------------------------------------------------------
# Utilities: Packaging - Packaging script
# Copyright (C) 2018-2025  Ye Lei (叶磊)
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import datetime
import os
import shutil
import subprocess
import time

from wordless.wl_utils import wl_misc

def print_with_elapsed_time(message):
    print(f'[{datetime.timedelta(seconds = round(time.time() - time_start))}] {message}')

is_windows, is_macos, is_linux = wl_misc.check_os()
wl_ver = wl_misc.get_wl_ver()
time_start = time.time()

# Package
print_with_elapsed_time('Start packaging...')

if is_windows:
    subprocess.run(['python', '-m', 'PyInstaller', '-y', '--clean', 'utils/wl_packaging.spec'], check = True)
elif is_macos:
    subprocess.run(['python3', '-m', 'PyInstaller', '-y', '--clean', 'utils/wl_packaging.spec'], check = True)
elif is_linux:
    subprocess.run(['python3.11', '-m', 'PyInstaller', '-y', '--clean', 'utils/wl_packaging.spec'], check = True)

# Create folders
if is_windows or is_linux:
    os.makedirs('dist/Wordless/imports')
    os.makedirs('dist/Wordless/exports')
elif is_macos:
    os.makedirs('dist/Wordless.app/Contents/MacOS/imports')
    os.makedirs('dist/Wordless.app/Contents/MacOS/exports')

if is_linux:
    # Fix GLib-GIO-ERROR, Gtk-WARNING, and many other errors/warnings on Linux
    # See: https://github.com/pyinstaller/pyinstaller/issues/7506
    os.remove('dist/Wordless/libs/libgtk-3.so.0')
    os.remove('dist/Wordless/libs/libstdc++.so.6')

    # Generate .desktop file
    subprocess.run(['python3.11', '-m', 'PyInstaller', '-y', '--clean', 'utils/linux_create_shortcut.py', '--contents-directory', 'libs'], check = True)
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
    subprocess.run([os.path.join(os.getcwd(), 'Wordless.app/Contents/MacOS/Wordless')], check = True)
elif is_linux:
    subprocess.run(['./Wordless'], check = True)

# Remove custom settings file
if is_windows or is_linux:
    files_settings = [
        'wl_settings.pickle',
        'wl_settings_display_lang.pickle'
    ]
elif is_macos:
    files_settings = [
        'Wordless.app/Contents/MacOS/wl_settings.pickle',
        'Wordless.app/Contents/MacOS/wl_settings_display_lang.pickle'
    ]

for file_settings in files_settings:
    if os.path.exists(file_settings):
        os.remove(file_settings)

print_with_elapsed_time('Tests passed!')

# Compress files
print_with_elapsed_time('Compressing files... ')

if is_windows or is_linux:
    os.chdir('..')

if is_windows:
    zip_file_name = f'wordless_{wl_ver}_windows.zip'
elif is_macos:
    zip_file_name = f'wordless_{wl_ver}_macos.zip'
elif is_linux:
    zip_file_name = f'wordless_{wl_ver}_linux.tar.gz'

# Clear cache
if os.path.exists(zip_file_name):
    os.remove(zip_file_name)

if is_windows:
    # Requires 7-Zip
    subprocess.run(['7z', 'a', '-tzip', '-mx9', zip_file_name, 'Wordless'], check = True)
elif is_macos:
    subprocess.run(['ditto', '-c', '-k', '--sequesterRsrc', '--keepParent', 'Wordless.app/', zip_file_name], check = True)
elif is_linux:
    subprocess.run(['tar', '-czvf', zip_file_name, 'Wordless/'], check = True)

print_with_elapsed_time('Compressing done!')
