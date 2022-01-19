# ----------------------------------------------------------------------
# Wordless: Tests - Checking - Unicode
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

import sys

sys.path.append('.')

from wl_checking import wl_checking_unicode

def test_is_han():
    assert wl_checking_unicode.is_han('测')
    assert not wl_checking_unicode.is_han('a')
    assert not wl_checking_unicode.is_han('_')

def test_is_eng():
    assert wl_checking_unicode.is_eng('a')
    assert wl_checking_unicode.is_eng('_')
    assert not wl_checking_unicode.is_eng('测')

def test_is_kana():
    assert wl_checking_unicode.is_kana('あ')
    assert not wl_checking_unicode.is_kana('a')
    assert not wl_checking_unicode.is_kana('_')

def test_is_thai():
    assert wl_checking_unicode.is_thai('ะ')
    assert not wl_checking_unicode.is_thai('a')
    assert not wl_checking_unicode.is_thai('_')

def test_is_tibetan():
    assert wl_checking_unicode.is_tibetan('ཨ')
    assert not wl_checking_unicode.is_tibetan('a')
    assert not wl_checking_unicode.is_tibetan('_')

def test_has_han():
    assert wl_checking_unicode.has_han('测a')
    assert not wl_checking_unicode.has_han('Aa')
    assert not wl_checking_unicode.has_han('a_')

def test_is_eng_token():
    assert wl_checking_unicode.is_eng_token('Aa')
    assert wl_checking_unicode.is_eng_token('a_')
    assert not wl_checking_unicode.is_eng_token('a测')

def test_has_kana():
    assert wl_checking_unicode.has_kana('あ_')
    assert not wl_checking_unicode.has_kana('a_')
    assert not wl_checking_unicode.has_kana('a测')

def test_has_thai():
    assert wl_checking_unicode.has_thai('ะ_')
    assert not wl_checking_unicode.has_thai('a_')
    assert not wl_checking_unicode.has_thai('a测')

def test_has_tibetan():
    assert wl_checking_unicode.has_tibetan('ཨ_')
    assert not wl_checking_unicode.has_tibetan('a_')
    assert not wl_checking_unicode.has_tibetan('a测')

if __name__ == '__main__':
    test_is_han()
    test_is_eng()
    test_is_kana()
    test_is_thai()
    test_is_tibetan()

    test_has_han()
    test_is_eng_token()
    test_has_kana()
    test_has_thai()
    test_has_tibetan()
