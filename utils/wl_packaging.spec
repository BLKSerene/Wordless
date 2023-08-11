# ----------------------------------------------------------------------
# Utilities: Packaging - spec file
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

import botok
import PyInstaller
import pymorphy3
import pythainlp
import spacy_pkuseg
import transformers
import underthesea.file_utils

import wl_utils

block_cipher = None

datas = []
is_windows, is_macos, is_linux = wl_utils.check_os()

# botok
datas.extend(PyInstaller.utils.hooks.collect_data_files('botok'))
# Dostoevsky
datas.extend(PyInstaller.utils.hooks.collect_data_files('dostoevsky'))
# jieba
datas.extend(PyInstaller.utils.hooks.collect_data_files('jieba'))
# khmer-nltk
datas.extend(PyInstaller.utils.hooks.collect_data_files('khmernltk'))
# Lingua
datas.extend(PyInstaller.utils.hooks.collect_data_files('lingua'))
# opencc-python
datas.extend(PyInstaller.utils.hooks.collect_data_files('opencc'))
# python-crfsuite
datas.extend(PyInstaller.utils.hooks.collect_data_files('pycrfsuite', include_py_files = True))
# python-mecab-ko
datas.extend(PyInstaller.utils.hooks.collect_data_files('mecab'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('mecab_ko_dic'))
# pymorphy3
datas.extend(PyInstaller.utils.hooks.copy_metadata('pymorphy3_dicts_ru'))
datas.extend(PyInstaller.utils.hooks.copy_metadata('pymorphy3_dicts_uk'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('pymorphy3_dicts_ru'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('pymorphy3_dicts_uk'))
# PyThaiNLP
datas.extend(PyInstaller.utils.hooks.collect_data_files('pythainlp'))
# simplemma
datas.extend(PyInstaller.utils.hooks.collect_data_files('simplemma'))
# spaCy
datas.extend(PyInstaller.utils.hooks.collect_data_files('spacy.lang', include_py_files = True))
datas.extend(PyInstaller.utils.hooks.copy_metadata('spacy_lookups_data'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('spacy_lookups_data', include_py_files = True))
datas.extend(PyInstaller.utils.hooks.collect_data_files('spacy_pkuseg'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('en_core_web_trf'))
datas.extend(PyInstaller.utils.hooks.copy_metadata('spacy_transformers'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('pip', include_py_files = True))

# Metadata required by Transformers
for package in transformers.dependency_versions_check.pkgs_to_check_at_runtime + ['torch']:
    if package != 'python':
        datas.extend(PyInstaller.utils.hooks.copy_metadata(package))

# SudachiPy
datas.extend(PyInstaller.utils.hooks.collect_data_files('sudachipy', include_py_files = True))
datas.extend(PyInstaller.utils.hooks.collect_data_files('sudachidict_core'))
# Underthesea
datas.extend(PyInstaller.utils.hooks.collect_data_files('underthesea'))
# wordcloud
datas.extend(PyInstaller.utils.hooks.collect_data_files('wordcloud'))

# Custom data files
datas.extend([
    # botok
    (botok.config.DEFAULT_BASE_PATH, 'pybo/dialect_packs'),
    # PyThaiNLP
    (pythainlp.tools.get_pythainlp_data_path(), 'pythainlp-data'),
    # spaCy-pkuseg
    (spacy_pkuseg.config.pkuseg_home, '.pkuseg'),
    # Underthesea
    (underthesea.file_utils.UNDERTHESEA_FOLDER, '.underthesea'),

    # Data
    ('../data', 'data'),
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
    ('../VERSION', '.')
])

# Hidden imports
hiddenimports = [
    # khmer-nltk
    'sklearn_crfsuite',

    # pymorphy3
    'pymorphy3_dicts_ru',
    'pymorphy3_dicts_uk',

    # spaCy
    'en_core_web_trf',
    'spacy_alignments',

    # SudachiPy
    'sudachidict_core',

    # Underthesea
    'sklearn.pipeline'
]

# When using uk_core_news_trf the first time after downloading the model using pip, pymorphy3's logging function would be overwritten by pip's and assertion would be raised during logging, so disable logging temporarily and restore logging after packaging completes
with open(pymorphy3.opencorpora_dict.wrapper.__file__, 'r+', encoding = 'utf_8') as f:
    pymorphy3_opencorpora_dict_wrapper = f.read()
    pymorphy3_opencorpora_dict_wrapper = pymorphy3_opencorpora_dict_wrapper.replace(
        'logger.info("format: %(format_version)s, revision: %(source_revision)s, updated: %(compiled_at)s", self._data.meta)',
        '# logger.info("format: %(format_version)s, revision: %(source_revision)s, updated: %(compiled_at)s", self._data.meta)'
    )

    f.seek(0)
    f.write(pymorphy3_opencorpora_dict_wrapper)

# Exclusions
excludes = []

# Icons
if is_windows or is_linux:
    icon = '../imgs/wl_icon.ico'
elif is_macos:
    icon = '../imgs/wl_icon.icns'

a = Analysis(
    ['../wordless/wl_main.py'],
    pathex = [],
    binaries = [],
    datas = datas,
    hiddenimports = hiddenimports,
    hookspath = [],
    hooksconfig = {},
    runtime_hooks = [],
    excludes = excludes,
    win_no_prefer_redirects = False,
    win_private_assemblies = False,
    cipher = block_cipher,
    noarchive = False
)

# Fix Fontconfig error when the frozen application is running on Ubuntu
# See: https://github.com/pyinstaller/pyinstaller/issues/3438#issuecomment-883161995
if is_linux:
    a.binaries = [x for x in a.binaries if not os.path.basename(x[1]).startswith(("libfontconfig", "libuuid"))]

pyz = PYZ(a.pure, a.zipped_data, cipher = block_cipher)

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
    argv_emulation = False,
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
# Reference: https://pyinstaller.org/en/stable/spec-files.html#spec-file-options-for-a-macos-bundle
if is_macos:
    wl_ver = wl_utils.get_wl_ver()

    app = BUNDLE(
        coll,
        name = 'Wordless.app',
        icon = icon,
        bundle_identifier = None,
        # References:
        #     https://developer.apple.com/library/archive/documentation/CoreFoundation/Conceptual/CFBundles/BundleTypes/BundleTypes.html
        #     https://developer.apple.com/documentation/bundleresources/information_property_list
        info_plist = {
            'CFBundleName': 'Wordless',
            'CFBundleDisplayName': 'Wordless',
            'CFBundleExecutable': 'Wordless',
            'CFBundlePackageType': 'APPL',
            'CFBundleVersion': wl_ver,
            'CFBundleShortVersionString': wl_ver,
            'CFBundleInfoDictionaryVersion': wl_ver,
            # Required by Retina displays on macOS
            # References:
            #     https://developer.apple.com/documentation/bundleresources/information_property_list/nshighresolutioncapable
            #     https://pyinstaller.org/en/stable/spec-files.html#spec-file-options-for-a-macos-bundle
            #     https://doc.qt.io/qt-5/highdpi.html#macos-and-ios
            'NSHighResolutionCapable': True,
            'NSPrincipalClass': 'NSApplication'
        }
    )

# Restore logging in pymorphy3
with open(pymorphy3.opencorpora_dict.wrapper.__file__, 'r+', encoding = 'utf_8') as f:
    pymorphy3_opencorpora_dict_wrapper = f.read()
    pymorphy3_opencorpora_dict_wrapper = pymorphy3_opencorpora_dict_wrapper.replace(
        '# logger.info("format: %(format_version)s, revision: %(source_revision)s, updated: %(compiled_at)s", self._data.meta)',
        'logger.info("format: %(format_version)s, revision: %(source_revision)s, updated: %(compiled_at)s", self._data.meta)'
    )

    f.seek(0)
    f.write(pymorphy3_opencorpora_dict_wrapper)
