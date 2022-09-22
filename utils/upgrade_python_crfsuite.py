# ----------------------------------------------------------------------
# Utilities: Upgrade python-crfsuite
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
    'https://github.com/scrapinghub/python-crfsuite/archive/refs/heads/master.zip',
    'https://github.com/chokkan/crfsuite/archive/refs/heads/master.zip',
    'https://github.com/chokkan/liblbfgs/archive/refs/heads/master.zip'
]
FILE_NAMES = [
    'python_crfsuite.zip',
    'crfsuite.zip',
    'liblbfgs.zip'
]
TEMP_FOLDER = 'python_crfsuite_temp'

# Fetch latest codes
if not os.path.exists(TEMP_FOLDER):
    os.mkdir(TEMP_FOLDER)

for url, file_name in zip(URLS, FILE_NAMES):
    print(f'Downloading from "{url}"... ', end = '')

    r = requests.get(url)

    with open(f'{TEMP_FOLDER}/{file_name}', 'wb') as f:
        f.write(r.content)

    with zipfile.ZipFile(f'{TEMP_FOLDER}/{file_name}') as zip_file:
        zip_file.extractall(TEMP_FOLDER)

    print('done!')

# Modify files
print('Modifying files... ', end = '')

for module in ['crfsuite', 'liblbfgs']:
    shutil.copytree(
        f'{TEMP_FOLDER}/{module}-master',
        f'{TEMP_FOLDER}/python-crfsuite-master/{module}',
        dirs_exist_ok = True
    )

with open(f'{TEMP_FOLDER}/python-crfsuite-master/pycrfsuite/_pycrfsuite.pyx', 'r+', encoding = 'utf_8') as f:
    text = f.read()
    text = text.replace('# cython: c_string_encoding=ascii', '# cython: c_string_encoding=utf-8')

    f.seek(0)
    f.write(text)

with open(f'{TEMP_FOLDER}/python-crfsuite-master/pycrfsuite/_pycrfsuite.cpp', 'r+', encoding = 'utf_8') as f:
    text = f.read()
    text = text.replace('#define __PYX_DEFAULT_STRING_ENCODING_IS_ASCII 1', '#define __PYX_DEFAULT_STRING_ENCODING_IS_ASCII 0')
    text = text.replace('#define __PYX_DEFAULT_STRING_ENCODING_IS_UTF8 0', '#define __PYX_DEFAULT_STRING_ENCODING_IS_UTF8 1')
    text = text.replace('#define __PYX_DEFAULT_STRING_ENCODING "ascii"', '#define __PYX_DEFAULT_STRING_ENCODING "utf8"')
    text = text.replace('# cython: c_string_encoding=ascii', '# cython: c_string_encoding=utf-8')

    f.seek(0)
    f.write(text)

print('done!')

# Upgrade python-crfsuite
print('Upgrading python-crfsuite...')

shutil.make_archive('python_crfsuite_latest', 'zip', f'{TEMP_FOLDER}/python-crfsuite-master')

if platform.system() == 'Windows':
    subprocess.run(['pip', 'install', 'python_crfsuite_latest.zip'], check = True)
elif platform.system() == 'Darwin':
    subprocess.run(['pip3', 'install', 'python_crfsuite_latest.zip'], check = True)
elif platform.system() == 'Linux':
    subprocess.run(['pip3.8', 'install', 'python_crfsuite_latest.zip'], check = True)

# Clean files
print('Cleaning files... ', end = '')

shutil.rmtree(TEMP_FOLDER)
os.remove('python_crfsuite_latest.zip')

print('done!')
