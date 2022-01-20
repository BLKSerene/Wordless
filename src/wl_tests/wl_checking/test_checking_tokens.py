# ----------------------------------------------------------------------
# Wordless: Tests - Checking - Miscellaneous
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

from wl_checking import wl_checking_tokens

def test_is_word_alphabetic():
    assert wl_checking_tokens.is_word_alphabetic('A1')
    assert not wl_checking_tokens.is_word_alphabetic('1')

def test_is_word_alphanumeric():
    assert wl_checking_tokens.is_word_alphanumeric('_a')
    assert wl_checking_tokens.is_word_alphanumeric('_1')
    assert wl_checking_tokens.is_word_alphanumeric('_测')
    assert not wl_checking_tokens.is_word_alphanumeric('_')

def test_is_word_lowercase():
    assert wl_checking_tokens.is_word_lowercase('aa')
    assert not wl_checking_tokens.is_word_lowercase('Aa')
    assert not wl_checking_tokens.is_word_lowercase('测试')

def test_is_word_uppercase():
    assert wl_checking_tokens.is_word_uppercase('AA')
    assert not wl_checking_tokens.is_word_uppercase('Aa')
    assert not wl_checking_tokens.is_word_uppercase('测试')

def test_is_word_title_case():
    assert wl_checking_tokens.is_word_title_case('Aa')
    assert not wl_checking_tokens.is_word_title_case('AA')
    assert not wl_checking_tokens.is_word_title_case('测试')

def test_is_num():
    assert wl_checking_tokens.is_num('a1')
    assert not wl_checking_tokens.is_num('a_')

def test_is_punc():
    assert wl_checking_tokens.is_punc('.')
    assert not wl_checking_tokens.is_punc('a.')

if __name__ == '__main__':
    test_is_word_alphabetic()
    test_is_word_alphanumeric()
    test_is_word_lowercase()
    test_is_word_uppercase()
    test_is_word_title_case()
    test_is_num()
    test_is_punc()
