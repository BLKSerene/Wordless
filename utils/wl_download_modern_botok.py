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

import botok
import pip
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

    SPACY_MODEL_NAME = 'xx_bo_tagger'
    SPACY_MODEL_GZIP = f'{SPACY_MODEL_NAME}.tar.gz'
    SPACY_MODEL_VER = '1.2.1'

    # Remove old versions
    pip.main(['uninstall', '-y', SPACY_MODEL_NAME])

    r = requests.get(
        f'https://github.com/Divergent-Discourses/Tibetan_SpaCy-Model/raw/refs/heads/main/packages/{SPACY_MODEL_NAME}-{SPACY_MODEL_VER}/dist/{SPACY_MODEL_NAME}-{SPACY_MODEL_VER}.tar.gz',
        timeout = 10
    )

    with open(SPACY_MODEL_GZIP, 'wb') as f:
        f.write(r.content)

    pip.main(['install', '--no-deps', SPACY_MODEL_GZIP])

    # Clean cache
    os.remove(SPACY_MODEL_GZIP)

if __name__ == '__main__':
    download_modern_botok()
