# ----------------------------------------------------------------------
# Tests: Checks - Tokens
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

from wordless.wl_checks import wl_checks_tokens

def test_is_word_alphanumeric():
    assert wl_checks_tokens.is_word_alphanumeric('_a')
    assert wl_checks_tokens.is_word_alphanumeric('_1')
    assert wl_checks_tokens.is_word_alphanumeric('_测')
    assert not wl_checks_tokens.is_word_alphanumeric('_')

def test_is_word_alphabetic():
    assert wl_checks_tokens.is_word_alphabetic('A1')
    assert not wl_checks_tokens.is_word_alphabetic('1')

def test_is_num():
    assert wl_checks_tokens.is_num('a1')
    assert not wl_checks_tokens.is_num('a_')

def test_is_punc():
    assert wl_checks_tokens.is_punc('.')
    assert not wl_checks_tokens.is_punc('a.')

def test_is_han():
    assert wl_checks_tokens.is_han('测')
    assert not wl_checks_tokens.is_han('a')
    assert not wl_checks_tokens.is_han('_')

def test_is_kana():
    assert wl_checks_tokens.is_kana('あ')
    assert not wl_checks_tokens.is_kana('a')
    assert not wl_checks_tokens.is_kana('_')

def test_is_tibetan():
    assert wl_checks_tokens.is_tibetan('ཨ')
    assert not wl_checks_tokens.is_tibetan('a')
    assert not wl_checks_tokens.is_tibetan('_')

def test_has_han():
    assert wl_checks_tokens.has_han('测a')
    assert not wl_checks_tokens.has_han('Aa')
    assert not wl_checks_tokens.has_han('a_')

def test_has_kana():
    assert wl_checks_tokens.has_kana('あ_')
    assert not wl_checks_tokens.has_kana('a_')
    assert not wl_checks_tokens.has_kana('a测')

def test_has_tibetan():
    assert wl_checks_tokens.has_tibetan('ཨ_')
    assert not wl_checks_tokens.has_tibetan('a_')
    assert not wl_checks_tokens.has_tibetan('a测')

if __name__ == '__main__':
    test_is_word_alphanumeric()
    test_is_word_alphabetic()
    test_is_num()
    test_is_punc()

    test_is_han()
    test_is_kana()
    test_is_tibetan()

    test_has_han()
    test_has_kana()
    test_has_tibetan()
