# ----------------------------------------------------------------------
# Utilities: Packaging - spec File
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

import platform

import PyInstaller
import pythainlp
import spacy_pkuseg
import underthesea.file_utils

block_cipher = None
datas = []

# botok
datas.extend(PyInstaller.utils.hooks.collect_data_files('botok'))
# jieba
datas.extend(PyInstaller.utils.hooks.collect_data_files('jieba'))
# Lingua
datas.extend(PyInstaller.utils.hooks.collect_data_files('lingua'))
# OpenCC
datas.extend(PyInstaller.utils.hooks.collect_data_files('opencc'))
# Python-crfsuite
datas.extend(PyInstaller.utils.hooks.collect_data_files('pycrfsuite', include_py_files = True))
# pymorphy2
datas.extend(PyInstaller.utils.hooks.copy_metadata('pymorphy2_dicts_ru'))
datas.extend(PyInstaller.utils.hooks.copy_metadata('pymorphy2_dicts_uk'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('pymorphy2_dicts_ru'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('pymorphy2_dicts_uk'))
# Pyphen
datas.extend(PyInstaller.utils.hooks.collect_data_files('pyphen'))
# PyThaiNLP
datas.extend(PyInstaller.utils.hooks.collect_data_files('pythainlp'))
# Sacremoses
datas.extend(PyInstaller.utils.hooks.collect_data_files('sacremoses'))
# spaCy
datas.extend(PyInstaller.utils.hooks.collect_data_files('spacy.lang', include_py_files = True))
datas.extend(PyInstaller.utils.hooks.copy_metadata('spacy_lookups_data'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('spacy_lookups_data', include_py_files = True))
datas.extend(PyInstaller.utils.hooks.collect_data_files('spacy_pkuseg'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('ca_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('zh_core_web_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('hr_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('da_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('de_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('el_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('en_core_web_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('fi_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('fr_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('it_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('ja_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('lt_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('mk_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('nb_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('nl_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('pl_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('pt_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('ro_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('ru_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('es_core_news_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('sv_core_news_sm'))
# SudachiPy
datas.extend(PyInstaller.utils.hooks.collect_data_files('sudachipy'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('sudachidict_core'))
# TextBlob
datas.extend(PyInstaller.utils.hooks.collect_data_files('textblob'))
# Underthesea
datas.extend(PyInstaller.utils.hooks.collect_data_files('underthesea'))
# wordcloud
datas.extend(PyInstaller.utils.hooks.collect_data_files('wordcloud'))

# Custom data files
datas.extend([
    # PyThaiNLP
    (pythainlp.tools.get_pythainlp_data_path(), 'pythainlp-data'),
    # spaCy-pkuseg
    (spacy_pkuseg.config.pkuseg_home, '.pkuseg'),
    # Underthesea
    (underthesea.file_utils.UNDERTHESEA_FOLDER, '.underthesea'),

    # Data
    ('../data', 'data'),
    # Fonts
    ('../fonts', 'fonts'),
    # Images
    ('../imgs', 'imgs'),
    # Translation
    ('../trs', 'trs'),
    # Misc
    ('../ACKNOWLEDGMENTS.md', '.'),
    ('../ACKNOWLEDGMENTS_zho_cn.md', '.'),
    ('../ACKNOWLEDGMENTS_zho_tw.md', '.'),
    ('../CHANGELOG.md', '.'),
    ('../LICENSE.txt', '.'),
    ('../LICENSE_zho_cn.txt', '.'),
    ('../LICENSE_zho_tw.txt', '.'),
    ('../VERSION', '.')
])

# Hidden imports
hiddenimports = [
    # pymorphy2
    'pymorphy2_dicts_ru',
    'pymorphy2_dicts_uk',

    # scikit-learn
    'sklearn.pipeline',

    # spaCy models
    'ca_core_news_sm',
    'zh_core_web_sm',
    'hr_core_news_sm',
    'da_core_news_sm',
    'de_core_news_sm',
    'el_core_news_sm',
    'en_core_web_sm',
    'fi_core_news_sm',
    'fr_core_news_sm',
    'it_core_news_sm',
    'ja_core_news_sm',
    'lt_core_news_sm',
    'mk_core_news_sm',
    'nb_core_news_sm',
    'nl_core_news_sm',
    'pl_core_news_sm',
    'pt_core_news_sm',
    'ro_core_news_sm',
    'ru_core_news_sm',
    'es_core_news_sm',
    'sv_core_news_sm',

    # SudachiPy
    'sudachidict_core'
]

# Exclusions
excludes = []

# Icons
if platform.system() in ['Windows', 'Linux']:
    icon = '../imgs/wl_icon.ico'
elif platform.system() == 'Darwin':
    icon = '../imgs/wl_icon.icns'

a = Analysis(
    ['../wordless/wl_main.py'],
    pathex = [],
    binaries = [],
    datas = datas,
    hiddenimports = hiddenimports,
    hookspath = [],
    runtime_hooks = [],
    excludes = excludes,
    win_no_prefer_redirects = False,
    win_private_assemblies = False,
    cipher = block_cipher,
    noarchive = False
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher = block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries = True,
    name = 'Wordless',
    debug = False,
    bootloader_ignore_signals = False,
    strip = False,
    upx = True,
    console = False,
    disable_windowed_traceback = False,
    target_arch = None,
    codesign_identity = None,
    entitlements_file = None,
    icon = icon
)

# Collect data files
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip = False,
    upx = True,
    upx_exclude = [],
    name = 'Wordless'
)

# Bundle application on macOS
if platform.system() == 'Darwin':
    app = BUNDLE(
        coll,
        name = 'Wordless.app',
        icon = icon,
        bundle_identifier = None,
        info_plist = {
            'NSHighResolutionCapable': 'True'
        }
    )
