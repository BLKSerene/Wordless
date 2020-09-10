#
# Wordless: Downloaders - spaCy Models
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import importlib
import platform
import subprocess
import sys

langs = [
    ['Danish'          , 'dan', 'da'],
    ['Dutch'           , 'nld', 'nl'],
    ['English'         , 'eng', 'en'],
    ['French'          , 'fra', 'fr'],
    ['German'          , 'deu', 'de'],
    ['Greek'           , 'ell', 'el'],
    ['Italian'         , 'ita', 'it'],
    ['Lithuanian'      , 'lit', 'lt'],
    ['Norwegian Bokmål', 'nob', 'nb'],
    ['Polish'          , 'pol', 'pl'],
    ['Portuguese'      , 'por', 'pt'],
    ['Romanian'        , 'ron', 'ro'],
    ['Spanish'         , 'spa', 'es']
]

model_name_dan = 'core_news_sm'
model_name_nld = 'core_news_sm'
model_name_eng = 'core_web_sm'
model_name_fra = 'core_news_sm'
model_name_deu = 'core_news_sm'
model_name_ell = 'core_news_sm'
model_name_ita = 'core_news_sm'
model_name_lit = 'core_news_sm'
model_name_nob = 'core_news_sm'
model_name_pol = 'core_news_sm'
model_name_por = 'core_news_sm'
model_name_ron = 'core_news_sm'
model_name_spa = 'core_news_sm'

model_ver_dan = '2.3.0'
model_ver_nld = '2.3.0'
model_ver_eng = '2.3.1'
model_ver_fra = '2.3.0'
model_ver_deu = '2.3.0'
model_ver_ell = '2.3.0'
model_ver_ita = '2.3.0'
model_ver_lit = '2.3.0'
model_ver_nob = '2.3.0'
model_ver_pol = '2.3.0'
model_ver_por = '2.3.0'
model_ver_ron = '2.3.1'
model_ver_spa = '2.3.1'

# Download models
for lang_text, lang_code_639_3, lang_code_639_1 in langs:
    model_name = globals()[f'model_name_{lang_code_639_3}']
    model_ver = globals()[f'model_ver_{lang_code_639_3}']

    if globals()[f'updates_available_{lang_code_639_3}']:
        if platform.system() == 'Windows':
            subprocess.call(f'pip install https://github.com/explosion/spacy-models/releases/download/{lang_code_639_1}_{model_name}-{model_ver}/{lang_code_639_1}_{model_name}-{model_ver}.tar.gz', shell = True)
        elif platform.system() == 'Darwin':
            subprocess.call(f'sudo pip3 install https://github.com/explosion/spacy-models/releases/download/{lang_code_639_1}_{model_name}-{model_ver}/{lang_code_639_1}_{model_name}-{model_ver}.tar.gz', shell = True)
        elif platform.system() == 'Linux':
            subprocess.call(f'sudo pip3.7 install https://github.com/explosion/spacy-models/releases/download/{lang_code_639_1}_{model_name}-{model_ver}/{lang_code_639_1}_{model_name}-{model_ver}.tar.gz', shell = True)
    else:
        print(f"The latest version of spaCy's {lang_text} model has already been installed!")

print('All done!')
