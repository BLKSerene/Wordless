# ----------------------------------------------------------------------
# Utilities: macOS - Recompile PyInstaller's bootloader
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
import shutil
import subprocess
import zipfile

import requests

PYINSTALLER_VER = '5.4.1'

# Fetch codes
print(f'Downloading PyInstaller {PYINSTALLER_VER}... ', end = '')

r = requests.get(f'https://github.com/pyinstaller/pyinstaller/archive/refs/tags/v{PYINSTALLER_VER}.zip')

with open(f'pyinstaller-{PYINSTALLER_VER}.zip', 'wb') as f:
    f.write(r.content)

print('done!')

with zipfile.ZipFile(f'pyinstaller-{PYINSTALLER_VER}.zip', 'r') as zip_file:
    for file_name in zip_file.namelist():
        zip_file.extract(file_name, '.')

# Lower MACOSX_DEPLOYMENT_TARGET and recompile the bootloader
# Reference: https://pyinstaller.org/en/stable/bootloader-building.html?highlight=waf#building-for-macos
os.environ['MACOSX_DEPLOYMENT_TARGET'] = '10.9'
os.chdir(f'pyinstaller-{PYINSTALLER_VER}/bootloader')

subprocess.run(['python3', 'waf', 'all'], check = True)

# Comment out signature-related codes in source files which do not work on OS X 10.9
os.chdir('..')

with open('PyInstaller/building/api.py', 'r+', encoding = 'utf_8') as f:
    pyinstaller_building_api = f.read()
    pyinstaller_building_api = pyinstaller_building_api.replace('osxutils.remove_signature_from_binary(build_name)', '# osxutils.remove_signature_from_binary(build_name)')

    f.seek(0)
    f.write(pyinstaller_building_api)

with open('PyInstaller/building/utils.py', 'r+', encoding = 'utf_8') as f:
    pyinstaller_building_utils = f.read()
    pyinstaller_building_utils = pyinstaller_building_utils.replace('osxutils.sign_binary(cachedfile, codesign_identity, entitlements_file)', '# osxutils.sign_binary(cachedfile, codesign_identity, entitlements_file)')

    f.seek(0)
    f.write(pyinstaller_building_utils)

# Install recompiled version of PyInstaller
os.chdir('..')

with zipfile.ZipFile(f'pyinstaller-{PYINSTALLER_VER}_modified.zip', 'w') as zip_file:
    for root, dirs, files in os.walk(f'pyinstaller-{PYINSTALLER_VER}'):
        for file in files:
            zip_file.write(os.path.join(root, file))

subprocess.run(['pip3', 'install', f'pyinstaller-{PYINSTALLER_VER}_modified.zip'], check = True)

# Clean files
shutil.rmtree(f'pyinstaller-{PYINSTALLER_VER}')
os.remove(f'pyinstaller-{PYINSTALLER_VER}.zip')
os.remove(f'pyinstaller-{PYINSTALLER_VER}_modified.zip')
