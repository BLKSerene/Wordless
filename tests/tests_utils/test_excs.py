# ----------------------------------------------------------------------
# Tests: Utilities - Exceptions
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

import pytest

from wordless.wl_utils import wl_excs

def test_wl_exc():
    with pytest.raises(wl_excs.Wl_Exc):
        raise wl_excs.Wl_Exc()

def test_wl_exc_word_cloud():
    with pytest.raises(wl_excs.Wl_Exc_Word_Cloud):
        raise wl_excs.Wl_Exc_Word_Cloud()

def test_wl_exc_word_cloud_font():
    with pytest.raises(wl_excs.Wl_Exc_Word_Cloud_Font):
        raise wl_excs.Wl_Exc_Word_Cloud_Font()

def test_wl_exc_word_cloud_font_nonexistent():
    with pytest.raises(wl_excs.Wl_Exc_Word_Cloud_Font_Nonexistent):
        raise wl_excs.Wl_Exc_Word_Cloud_Font_Nonexistent()

def test_wl_exc_word_cloud_font_is_dir():
    with pytest.raises(wl_excs.Wl_Exc_Word_Cloud_Font_Is_Dir):
        raise wl_excs.Wl_Exc_Word_Cloud_Font_Is_Dir()

def test_wl_exc_word_cloud_font_unsupported():
    with pytest.raises(wl_excs.Wl_Exc_Word_Cloud_Font_Unsupported):
        raise wl_excs.Wl_Exc_Word_Cloud_Font_Unsupported()

def test_wl_exc_word_cloud_mask():
    with pytest.raises(wl_excs.Wl_Exc_Word_Cloud_Mask):
        raise wl_excs.Wl_Exc_Word_Cloud_Mask()

def test_wl_exc_word_cloud_mask_nonexistent():
    with pytest.raises(wl_excs.Wl_Exc_Word_Cloud_Mask_Nonexistent):
        raise wl_excs.Wl_Exc_Word_Cloud_Mask_Nonexistent()

def test_wl_exc_word_cloud_mask_is_dir():
    with pytest.raises(wl_excs.Wl_Exc_Word_Cloud_Mask_Is_Dir):
        raise wl_excs.Wl_Exc_Word_Cloud_Mask_Is_Dir()

def test_wl_exc_word_cloud_mask_unsupported():
    with pytest.raises(wl_excs.Wl_Exc_Word_Cloud_Mask_Unsupported):
        raise wl_excs.Wl_Exc_Word_Cloud_Mask_Unsupported()

if __name__ == '__main__':
    test_wl_exc()

    test_wl_exc_word_cloud()
    test_wl_exc_word_cloud_font()
    test_wl_exc_word_cloud_font_nonexistent()
    test_wl_exc_word_cloud_font_is_dir()
    test_wl_exc_word_cloud_font_unsupported()
    test_wl_exc_word_cloud_mask()
    test_wl_exc_word_cloud_mask_nonexistent()
    test_wl_exc_word_cloud_mask_is_dir()
    test_wl_exc_word_cloud_mask_unsupported()
