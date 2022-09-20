# ----------------------------------------------------------------------
# Utilities: Lower MACOS_DEPLOYMENT_TARGET of PyInstaller
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

import PyInstaller.building.api
import PyInstaller.building.utils
import requests

PYINSTALLER_VER = '5.4.1'
PROXIES = {'http': '', 'https': ''}

# Fetch codes
print(f'Downloading PyInstaller {PYINSTALLER_VER}... ', end = '')

r = requests.get(f'https://github.com/pyinstaller/pyinstaller/archive/refs/tags/v{PYINSTALLER_VER}.zip', proxies = PROXIES)

with open(f'pyinstaller-{PYINSTALLER_VER}.zip', 'wb') as f:
    f.write(r.content)

print('done!')

with zipfile.ZipFile(f'pyinstaller-{PYINSTALLER_VER}.zip', 'r') as zip_file:
    for file_name in zip_file.namelist():
        zip_file.extract(file_name, '.')

# Modify MACOSX_DEPLOYMENT_TARGET
# Reference: https://github.com/pyinstaller/pyinstaller/commit/80936c6399da561f00173b30b42c4133eeac019c#diff-449dff4a40028675f338ef14a95fad67edea219ff61fdb70940b7e62f31ac329
os.environ['MACOSX_DEPLOYMENT_TARGET'] = '10.9'

# Recompile the macOS bootloader
os.chdir(f'pyinstaller-{PYINSTALLER_VER}/bootloader')
subprocess.run(['python3', 'waf', 'all'], check = True)

# Compress files back into package
os.chdir('../..')
with zipfile.ZipFile(f'pyinstaller-{PYINSTALLER_VER}_modified.zip', 'w') as zip_file:
    for root, dirs, files in os.walk(f'pyinstaller-{PYINSTALLER_VER}'):
        for file in files:
            zip_file.write(os.path.join(root, file))

# Install PyInstaller
subprocess.run(['pip3', 'install', f'pyinstaller-{PYINSTALLER_VER}_modified.zip'], check = True)

# Clean files
shutil.rmtree(f'pyinstaller-{PYINSTALLER_VER}')
os.remove(f'pyinstaller-{PYINSTALLER_VER}_modified.zip')

# Modify signature-related codes in PyInstaller's source files as they are not supported on OS X 10.9
with open(PyInstaller.building.api.__file__, 'r', encoding = 'utf_8') as f:
    pyinstaller_building_api = f.read()

with open(PyInstaller.building.api.__file__, 'w', encoding = 'utf_8') as f:
    f.write(pyinstaller_building_api.replace('osxutils.remove_signature_from_binary(build_name)', '# osxutils.remove_signature_from_binary(build_name)'))

with open(PyInstaller.building.utils.__file__, 'r', encoding = 'utf_8') as f:
    pyinstaller_building_utils = f.read()

with open(PyInstaller.building.utils.__file__, 'w', encoding = 'utf_8') as f:
    f.write(pyinstaller_building_utils.replace('osxutils.sign_binary(cachedfile, codesign_identity, entitlements_file)', '# osxutils.sign_binary(cachedfile, codesign_identity, entitlements_file)'))
