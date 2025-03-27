# ----------------------------------------------------------------------
# Utilities: Download - modern-botok's dialect pack for Tibetan (Modern)
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

import botok
import requests

def download_modern_botok():
    path_dict_default = os.path.join(botok.config.DEFAULT_BASE_PATH, botok.config.DEFAULT_DIALECT_PACK)
    path_dict_custom = os.path.join(botok.config.DEFAULT_BASE_PATH, 'custom')

    # Remove old versions
    shutil.rmtree(path_dict_custom, ignore_errors = True)

    # Custom dictionary
    print("Downloading modern-botok's custom dictionary...")

    # Download default dictionary
    botok.WordTokenizer()

    shutil.copytree(path_dict_default, path_dict_custom)

    r = requests.get(
        'https://raw.githubusercontent.com/Divergent-Discourses/modern-botok/refs/heads/main/dictionary/tsikchen.tsv',
        timeout = 10
    )

    with open(os.path.join(path_dict_custom, 'dictionary', 'words', 'tsikchen.tsv'), 'wb') as f:
        f.write(r.content)

    # spaCy model
    print("Downloading modern-botok's spaCy model...")

    path_site_packages = os.path.dirname(botok.__path__[0])
    path_zh_bo_tagger = os.path.join(path_site_packages, 'zh_bo_tagger')
    path_zh_bo_tagger_egg_info = os.path.join(path_site_packages, 'zh_bo_tagger.egg-info')
    path_zh_bo_tagger_zip = os.path.join('Tibetan_SpaCy-Model-main', 'packages', 'zh_bo_tagger-1.1.3')
    path_site_packages_zip = os.path.join(path_site_packages, path_zh_bo_tagger_zip)

    # Remove old versions
    shutil.rmtree(path_zh_bo_tagger, ignore_errors = True)
    shutil.rmtree(path_zh_bo_tagger_egg_info, ignore_errors = True)

    r = requests.get(
        'https://github.com/Divergent-Discourses/Tibetan_SpaCy-Model/archive/refs/heads/main.zip',
        timeout = 10
    )

    with open(f'{path_zh_bo_tagger}.zip', 'wb') as f:
        f.write(r.content)

    with zipfile.ZipFile(f'{path_zh_bo_tagger}.zip', 'r') as f:
        for file in f.namelist():
            if os.path.normpath(file).startswith(os.path.join(path_zh_bo_tagger_zip, 'zh_bo_tagger')):
                f.extract(file, path_site_packages)

    shutil.copytree(os.path.join(path_site_packages_zip, 'zh_bo_tagger'), path_zh_bo_tagger)
    shutil.copytree(os.path.join(path_site_packages_zip, 'zh_bo_tagger.egg-info'), path_zh_bo_tagger_egg_info)

    # Clean cache
    shutil.rmtree(os.path.join(path_site_packages, 'Tibetan_SpaCy-Model-main'), ignore_errors = True)
    os.remove(os.path.join(path_site_packages, 'zh_bo_tagger.zip'))

if __name__ == '__main__':
    download_modern_botok()
