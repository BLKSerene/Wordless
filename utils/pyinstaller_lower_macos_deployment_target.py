# ----------------------------------------------------------------------
# Wordless: Utilities - Lower MACOS_DEPLOYMENT_TARGET of PyInstaller
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

PYINSTALLER_PACKAGE_NAME = 'pyinstaller-4.5.1'

# Unzip the package
with zipfile.ZipFile(f'{PYINSTALLER_PACKAGE_NAME}.zip', 'r') as zip_file:
    for file_name in zip_file.namelist():
        zip_file.extract(file_name, '.')

# Reference: https://github.com/pyinstaller/pyinstaller/commit/80936c6399da561f00173b30b42c4133eeac019c#diff-449dff4a40028675f338ef14a95fad67edea219ff61fdb70940b7e62f31ac329
os.environ['MACOSX_DEPLOYMENT_TARGET'] = '10.11'

# Recompile the macOS bootloader
os.chdir(f'{PYINSTALLER_PACKAGE_NAME}/bootloader')
subprocess.call('python3 waf all', shell = True)

# Compress files back into package
os.chdir('..')
os.chdir('..')
with zipfile.ZipFile(f'{PYINSTALLER_PACKAGE_NAME}_modified.zip', 'w') as zip_file:
    for root, dirs, files in os.walk(PYINSTALLER_PACKAGE_NAME):
        for file in files:
            zip_file.write(os.path.join(root, file))

# Remove unzipped files
shutil.rmtree(PYINSTALLER_PACKAGE_NAME)

# Install PyInstaller
subprocess.call(f'pip3 install {PYINSTALLER_PACKAGE_NAME}_modified.zip', shell = True)

# Remove the modified package
os.remove(f'{PYINSTALLER_PACKAGE_NAME}_modified.zip')

# Modify signature-related commands in PyInstaller source files as they are not supported on OS X 10.11
import PyInstaller.building.api
import PyInstaller.building.utils

with open(PyInstaller.building.api.__file__, 'r', encoding = 'utf_8') as f:
    pyinstaller_building_api = f.read()

with open(PyInstaller.building.api.__file__, 'w', encoding = 'utf_8') as f:
    f.write(pyinstaller_building_api.replace('osxutils.remove_signature_from_binary(self.name)', '# osxutils.remove_signature_from_binary(self.name)'))

with open(PyInstaller.building.utils.__file__, 'r', encoding = 'utf_8') as f:
    pyinstaller_building_utils = f.read()

with open(PyInstaller.building.utils.__file__, 'w', encoding = 'utf_8') as f:
    f.write(pyinstaller_building_utils.replace('osxutils.remove_signature_from_binary(cachedfile)', '# osxutils.remove_signature_from_binary(cachedfile)').replace('osxutils.sign_binary(cachedfile, codesign_identity, entitlements_file)', '# osxutils.sign_binary(cachedfile, codesign_identity, entitlements_file)'))
