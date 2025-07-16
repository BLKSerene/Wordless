# ----------------------------------------------------------------------
# Utilities: Download - pkuseg's default_v2 model
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

import os
import shutil
import zipfile

import spacy_pkuseg
import requests

def download_pkuseg():
    # Rename to the default model name
    path_dict_mixed = os.path.join(spacy_pkuseg.config.pkuseg_home, 'mixed')
    path_dict_mixed_zip = os.path.join(spacy_pkuseg.config.pkuseg_home, 'mixed.zip')

    # Remove old versions
    shutil.rmtree(spacy_pkuseg.config.pkuseg_home, ignore_errors = True)

    # Create folders
    os.makedirs(path_dict_mixed, exist_ok = True)

    # Download the default_v2 model
    print("Downloading pkuseg's default_v2 model...")

    r = requests.get(
        'https://github.com/lancopku/pkuseg-python/releases/download/v0.0.25/default_v2.zip',
        timeout = 10
    )

    with open(path_dict_mixed_zip, 'wb') as f:
        f.write(r.content)

    with zipfile.ZipFile(path_dict_mixed_zip) as f:
        f.extractall(path_dict_mixed)

    # Create an empty zip file to prevent redownloading
    os.remove(path_dict_mixed_zip)

    with open(path_dict_mixed_zip, 'wb') as f:
        pass

if __name__ == '__main__':
    download_pkuseg()
