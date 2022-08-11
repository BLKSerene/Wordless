# ----------------------------------------------------------------------
# Wordless: Checking - Tokens
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

# At least one letter
def is_word_alphabetic(token):
    return any((char for char in token if char.isalpha()))

# At least one letter or numeral
def is_word_alphanumeric(token):
    return any((char for char in token if char.isalnum()))

def is_word_lowercase(token):
    return token.islower()

def is_word_uppercase(token):
    return token.isupper()

def is_word_title_case(token):
    return token.istitle()

# At least one numeral
def is_num(token):
    return any(map(str.isnumeric, token))

# All punctuation marks
def is_punc(token):
    return token and not any(map(str.isalnum, token))
