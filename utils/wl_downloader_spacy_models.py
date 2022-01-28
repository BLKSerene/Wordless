# ----------------------------------------------------------------------
# Wordless: Downloaders - spaCy Models
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

import importlib
import platform
import subprocess

langs = [
    ['Catalan'         , 'cat', 'ca'],
    ['Chinese'         , 'zho', 'zh'],
    ['Danish'          , 'dan', 'da'],
    ['Dutch'           , 'nld', 'nl'],
    ['English'         , 'eng', 'en'],
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
    ['Spanish'         , 'spa', 'es']
]

model_name_cat = 'core_news_sm'
model_name_zho = 'core_web_sm'
model_name_dan = 'core_news_sm'
model_name_nld = 'core_news_sm'
model_name_eng = 'core_web_sm'
model_name_fra = 'core_news_sm'
model_name_deu = 'core_news_sm'
model_name_ell = 'core_news_sm'
model_name_ita = 'core_news_sm'
model_name_jpn = 'core_news_sm'
model_name_lit = 'core_news_sm'
model_name_mkd = 'core_news_sm'
model_name_nob = 'core_news_sm'
model_name_pol = 'core_news_sm'
model_name_por = 'core_news_sm'
model_name_ron = 'core_news_sm'
model_name_rus = 'core_news_sm'
model_name_spa = 'core_news_sm'

model_ver_cat = '3.2.0'
model_ver_zho = '3.2.0'
model_ver_dan = '3.2.0'
model_ver_nld = '3.2.0'
model_ver_eng = '3.2.0'
model_ver_fra = '3.2.0'
model_ver_deu = '3.2.0'
model_ver_ell = '3.2.0'
model_ver_ita = '3.2.0'
model_ver_jpn = '3.2.0'
model_ver_lit = '3.2.0'
model_ver_mkd = '3.2.0'
model_ver_nob = '3.2.0'
model_ver_pol = '3.2.0'
model_ver_por = '3.2.0'
model_ver_ron = '3.2.0'
model_ver_rus = '3.2.0'
model_ver_spa = '3.2.0'

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

    if globals()[f'updates_available_{lang_code_639_3}']:
        if platform.system() == 'Windows':
            subprocess.call(f'pip install https://github.com/explosion/spacy-models/releases/download/{lang_code_639_1}_{model_name}-{model_ver}/{lang_code_639_1}_{model_name}-{model_ver}-py3-none-any.whl', shell = True)
        elif platform.system() == 'Darwin':
            subprocess.call(f'sudo pip3 install https://github.com/explosion/spacy-models/releases/download/{lang_code_639_1}_{model_name}-{model_ver}/{lang_code_639_1}_{model_name}-{model_ver}-py3-none-any.whl', shell = True)
        elif platform.system() == 'Linux':
            subprocess.call(f'sudo pip3.8 install https://github.com/explosion/spacy-models/releases/download/{lang_code_639_1}_{model_name}-{model_ver}/{lang_code_639_1}_{model_name}-{model_ver}-py3-none-any.whl', shell = True)
    else:
        print(f"The latest version of spaCy's {lang_text} model ({model_ver}) has already been installed!")
