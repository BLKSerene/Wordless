#
# Wordless: Packaging - spec File
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import os
import platform
import sys

import PyInstaller

block_cipher = None
datas = []

# jieba
datas.extend(PyInstaller.utils.hooks.collect_data_files('jieba'))
# langdetect
datas.extend(PyInstaller.utils.hooks.collect_data_files('langdetect'))
# nagisa
datas.extend(PyInstaller.utils.hooks.collect_data_files('nagisa', include_py_files = True))
# pybo
datas.extend(PyInstaller.utils.hooks.collect_data_files('pybo'))
# pymorphy2
datas.extend(PyInstaller.utils.hooks.collect_data_files('pymorphy2_dicts_ru'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('pymorphy2_dicts_uk'))
# PyThaiNLP
datas.extend(PyInstaller.utils.hooks.collect_data_files('pythainlp'))
# SacreMoses
datas.extend(PyInstaller.utils.hooks.collect_data_files('sacremoses'))
# spaCy
datas.extend(PyInstaller.utils.hooks.collect_data_files('spacy.lang', include_py_files = True))
datas.extend(PyInstaller.utils.hooks.collect_data_files('de_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('el_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('en_core_web_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('es_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('fr_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('it_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('nl_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('pt_core_news_sm'))
# Underthesea
datas.extend(PyInstaller.utils.hooks.collect_data_files('underthesea'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('languageflow'))
# wordcloud
datas.extend(PyInstaller.utils.hooks.collect_data_files('wordcloud'))
# Custom Data
datas.extend([
    ('src/imgs', 'imgs'),
    ('src/lemmatization', 'lemmatization'),
    ('src/stop_words', 'stop_words')
])
# Miscellaneous
datas.extend([
    ('src/VERSION', '.'),
    ('LICENSE.txt', '.')
])

if platform.system() == 'Darwin':
    datas.extend(PyInstaller.utils.hooks.collect_data_files('PIL', include_py_files = True))

hiddenimports = [
    # pymorphy2
    'pymorphy2_dicts_ru',
    'pymorphy2_dicts_uk',

    # spaCy
    'spacy._align',
    'spacy.lexeme',
    'spacy.matcher._schemas',
    'spacy.morphology',
    'spacy.parts_of_speech',
    'spacy.tokens._retokenize',
    'spacy.tokens.underscore',
    'spacy.strings',
    'spacy.syntax._beam_utils',
    'spacy.syntax._parser_model',
    'spacy.syntax.arc_eager',
    'spacy.syntax.ner',
    'spacy.syntax.nn_parser',
    'spacy.syntax.stateclass',
    'spacy.syntax.transition_system',

    'blis',
    'blis.py',

    'cymem',
    'cymem.cymem',

    'murmurhash',

    'preshed.maps',

    'srsly.msgpack.util',

    'thinc.extra.search',
    'thinc.linalg',
    'thinc.neural._aligned_alloc'
]

runtime_hooks = [
    'wordless_hook_pymorphy2.py'
]

if platform.system() == 'Windows':
    excludes = []
elif platform.system() == 'Darwin':
    excludes = [
        'joblib',
        'PIL'
    ]

a = Analysis(['src/wordless_main.py'],
             pathex = [],
             binaries = [],
             datas = datas,
             hiddenimports = hiddenimports,
             hookspath = [],
             runtime_hooks = runtime_hooks,
             excludes = excludes,
             win_no_prefer_redirects = False,
             win_private_assemblies = False,
             cipher = block_cipher,
             noarchive = False)

pyz = PYZ(a.pure, a.zipped_data,
          cipher = block_cipher)

if platform.system() == 'Windows':
    icon = 'src/imgs/wordless_icon.ico'
elif platform.system() == 'Darwin':
    icon = 'src/imgs/wordless_icon.icns'

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries = True,
          name = 'Wordless',
          debug = False,
          bootloader_ignore_signals = False,
          strip = False,
          upx = True,
          console = False,
          icon = icon)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip = False,
               upx = True,
               name = 'Wordless')

if platform.system() == 'Darwin':
    app = BUNDLE(exe,
                 name = 'Wordless.app',
                 icon = icon,
                 bundle_identifier = None,
                 info_plist = {
                    'NSHighResolutionCapable': 'True'
                 })
