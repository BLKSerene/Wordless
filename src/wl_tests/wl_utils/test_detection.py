#
# Wordless: Tests - Utilities - Detection
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import os
import re
import sys

sys.path.append('.')

import pytest

from wl_tests import wl_test_init
from wl_utils import wl_detection

main = wl_test_init.Wl_Test_Main()
main.settings_custom['auto_detection']['detection_settings']['number_lines_no_limit'] = True

# Encoding detection
@pytest.mark.parametrize('file_name', os.listdir(f'wl_tests/files/wl_utils/wl_detection/encoding/'))
def test_detection_encoding(file_name):
    file = {}

    file['path'] = f'wl_tests/files/wl_utils/wl_detection/encoding/{file_name}'
    file['name'] = os.path.basename(file['path'])
    file['encoding'] = 'utf_8'

    encoding_code, success = wl_detection.detect_encoding(main, file["path"])

    encoding_code_file = re.search(r'(?<=\()[^\(\)]+?(?=\)\.txt)', file_name).group()
    encoding_code_file = encoding_code_file.lower()
    encoding_code_file = encoding_code_file.replace('-', '_')

    assert encoding_code == encoding_code_file
    assert success

# Language detection
@pytest.mark.parametrize('file_name', os.listdir(f'wl_tests/files/wl_utils/wl_detection/lang/'))
def test_detection_lang(file_name):
    file = {}

    file['path'] = f'wl_tests/files/wl_utils/wl_detection/lang/{file_name}'
    file['name'] = os.path.basename(file['path'])
    file['encoding'] = 'utf_8'

    lang_code, success = wl_detection.detect_lang(main, file)

    assert lang_code == file_name.replace('.txt', '')
    assert success
