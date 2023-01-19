# ----------------------------------------------------------------------
# Utilities: Downloaders - spaCy Models
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

import importlib
import platform
import subprocess

langs = [
    ['Catalan'         , 'cat', 'ca'],
    ['Chinese'         , 'zho', 'zh'],
    ['Croatian'        , 'hrv', 'hr'],
    ['Danish'          , 'dan', 'da'],
    ['Dutch'           , 'nld', 'nl'],
    ['English'         , 'eng', 'en'],
    ['Finnish'         , 'fin', 'fi'],
    ['French'          , 'fra', 'fr'],
    ['German'          , 'deu', 'de'],
    ['Greek'           , 'ell', 'el'],
    ['Italian'         , 'ita', 'it'],
    ['Japanese'        , 'jpn', 'ja'],
    ['Lithuanian'      , 'lit', 'lt'],
    ['Macedonian'      , 'mkd', 'mk'],
    ['Norwegian Bokmål', 'nob', 'nb'],
    ['Polish'          , 'pol', 'pl'],
    ['Portuguese'      , 'por', 'pt'],
    ['Romanian'        , 'ron', 'ro'],
    ['Russian'         , 'rus', 'ru'],
    ['Spanish'         , 'spa', 'es'],
    ['Swedish'         , 'swe', 'sv'],
    ['Ukrainian'       , 'ukr', 'uk']
]

model_name_zho = model_name_eng = 'core_web_sm'
model_name_cat = model_name_hrv = model_name_dan = model_name_nld = model_name_fin = \
model_name_fra = model_name_deu = model_name_ell = model_name_ita = model_name_jpn = \
model_name_lit = model_name_mkd = model_name_nob = model_name_pol = model_name_por = \
model_name_ron = model_name_rus = model_name_spa = model_name_swe = model_name_ukr = \
'core_news_sm'

model_ver_cat = model_ver_zho = model_ver_hrv = model_ver_dan = model_ver_nld = \
model_ver_eng = model_ver_fin = model_ver_fra = model_ver_deu = model_ver_ell = \
model_ver_ita = model_ver_jpn = model_ver_lit = model_ver_mkd = model_ver_nob = \
model_ver_pol = model_ver_por = model_ver_ron = model_ver_rus = model_ver_spa = \
model_ver_swe = model_ver_ukr = '3.4.0'

# Check updates
for lang_text, lang_code_639_3, lang_code_639_1 in langs:
    globals()[f'updates_available_{lang_code_639_3}'] = False

    try:
        model_name = globals()[f'model_name_{lang_code_639_3}']
        model = importlib.import_module(f'{lang_code_639_1}_{model_name}')

        if model.__version__ != globals()[f'model_ver_{lang_code_639_3}']:
            globals()[f'updates_available_{lang_code_639_3}'] = True
    except ModuleNotFoundError:
        globals()[f'updates_available_{lang_code_639_3}'] = True

# Download models
for lang_text, lang_code_639_3, lang_code_639_1 in langs:
    model_name = globals()[f'model_name_{lang_code_639_3}']
    model_ver = globals()[f'model_ver_{lang_code_639_3}']
    model_url = f'https://github.com/explosion/spacy-models/releases/download/{lang_code_639_1}_{model_name}-{model_ver}/{lang_code_639_1}_{model_name}-{model_ver}-py3-none-any.whl'

    if globals()[f'updates_available_{lang_code_639_3}']:
        if platform.system() == 'Windows':
            subprocess.run(['pip', 'install', model_url], check = True)
        elif platform.system() == 'Darwin':
            subprocess.run(['pip3', 'install', model_url], check = True)
        elif platform.system() == 'Linux':
            subprocess.run(['pip3.8', 'install', model_url], check = True)
    else:
        print(f"The latest version of spaCy's {lang_text} model ({model_ver}) has already been installed!")
