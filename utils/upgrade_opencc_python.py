# ----------------------------------------------------------------------
# Utilities: Upgrade opencc-python
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
import platform
import shutil
import subprocess
import zipfile

import requests

URLS = [
    'https://github.com/yichen0831/opencc-python/archive/refs/heads/master.zip',
    'https://github.com/BYVoid/OpenCC/archive/refs/heads/master.zip'
]
FILE_NAMES = [
    'opencc_python.zip',
    'opencc.zip'
]
TEMP_FOLDER = 'opencc_python_temp'

# Fetch latest codes
if not os.path.exists(TEMP_FOLDER):
    os.mkdir(TEMP_FOLDER)

for url, file_name in zip(URLS, FILE_NAMES):
    print(f'Downloading from "{url}"... ', end = '')

    r = requests.get(url)

    with open(os.path.join(TEMP_FOLDER, file_name), 'wb') as f:
        f.write(r.content)

    folder_name = file_name.split('.', maxsplit = 1)[0]

    with zipfile.ZipFile(os.path.join(TEMP_FOLDER, file_name)) as zip_file:
        zip_file.extractall(TEMP_FOLDER)

    print('done!')

# Upgrade dictionaries
print('Upgrading dictionaries... ', end = '')

shutil.copytree(
    f'{TEMP_FOLDER}/OpenCC-master/data/dictionary',
    f'{TEMP_FOLDER}/opencc-python-master/opencc/dictionary',
    dirs_exist_ok = True
)

print('done!')

# Upgrade opencc-python
print('Upgrading opencc-python...')

shutil.make_archive('opencc_python_latest', 'zip', f'{TEMP_FOLDER}/opencc-python-master')

if platform.system() == 'Windows':
    subprocess.run(['pip', 'install', 'opencc_python_latest.zip'], check = True)
elif platform.system() == 'Darwin':
    subprocess.run(['pip3', 'install', 'opencc_python_latest.zip'], check = True)
elif platform.system() == 'Linux':
    subprocess.run(['pip3.8', 'install', 'opencc_python_latest.zip'], check = True)

# Clean files
print('Cleaning files... ', end = '')

shutil.rmtree(TEMP_FOLDER)
os.remove('opencc_python_latest.zip')

print('done!')
