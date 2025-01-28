# ----------------------------------------------------------------------
# Wordless: Checks - Tokens
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

# References:
#     https://www.unicode.org/charts/nameslist/
#     https://en.wikipedia.org/wiki/Unicode_block
#     https://www.unicode.org/charts/index.html
UNICODE_HAN = [
    # CJK Radicals Supplement
    (0x2E80, 0x2E99), (0x2E9B, 0x2EF3),
    # Kangxi Radicals
    (0x2F00, 0X2FD5),
    # Ideographic Description Characters
    (0x2FF0, 0x2FFF),
    # CJK Symbols and Punctuation
    (0x3000, 0x3003), (0x3005, 0x302D), (0x3030, 0x3030), (0x3036, 0x303F),
    # Bopomofo
    (0x3105, 0x312F),
    # Kanbun
    (0x3190, 0x319F),
    # Bopomofo Extended
    (0x31A0, 0x31BF),
    # CJK Strokes
    (0x31C0, 0x31E3), (0x31EF, 0x31EF),
    # Enclosed CJK Letters and Months
    (0x3220, 0x325F), (0x3280, 0x32CF), (0x32FF, 0x32FF),
    # CJK Compatibility
    (0x3358, 0x33FF),
    # CJK Unified Ideographs Extension A
    (0x3400, 0x4DBF),
    # Yijing Hexagram Symbols
    (0x4DC0, 0x4DFF),
    # CJK Unified Ideographs
    (0x4E00, 0x9FFF),
    # Yi Syllables
    (0xA000, 0xA48C),
    # Yi Radicals
    (0xA490, 0xA4C6),
    # Phags-pa
    (0xA840, 0xA877),
    # CJK Compatibility Ideographs
    (0xF900, 0xFA6D), (0xFA70, 0xFAD9),
    # CJK Compatibility Forms
    (0xFE30, 0xFE4F),
    # Halfwidth and Fullwidth Forms
    (0xFF01, 0xFF0F), (0xFF1A, 0xFF1F), (0xFF3B, 0xFF40), (0xFF5B, 0xFF64),

    # Ideographic Symbols and Punctuation
    (0x16FE0, 0x16FE4), (0x16FF0, 0x16FF1),
    # Tangut
    (0x17000, 0x187F7),
    # Tangut Components
    (0x18800, 0x18AFF),
    # Khitan Small Script
    (0x18B00, 0x18CD5),
    # Tangut Supplement
    (0x18D00, 0x18D08),
    # Nushu
    (0x1B170, 0x1B2FB),
    # Enclosed Ideographic Supplement
    (0x1F210, 0x1F23B), (0x1F240, 0x1F248), (0x1F250, 0x1F251), (0x1F260, 0x1F265),

    # CJK Unified Ideographs Extension B
    (0x20000, 0x2A6DF),
    # CJK Unified Ideographs Extension C
    (0x2A700, 0x2B739),
    # CJK Unified Ideographs Extension D
    (0x2B740, 0x2B81D),
    # CJK Unified Ideographs Extension E
    (0x2B820, 0x2CEA1),
    # CJK Unified Ideographs Extension F
    (0x2CEB0, 0x2EBE0),
    # CJK Unified Ideographs Extension I
    (0x2EBF0, 0x2EE5D),
    # CJK Compatibility Ideographs Supplement
    (0x2F800, 0x2FA1D),

    # CJK Unified Ideographs Extension G
    (0x30000, 0x3134A),
    # CJK Unified Ideographs Extension H
    (0x31350, 0x323AF)
]

UNICODE_KANA = [
    # CJK Symbols and Punctuation
    (0x3031, 0x3035),
    # Hiragana
    (0x3041, 0x3096), (0x3099, 0x309F),
    # Katakana
    (0x30A0, 0x30FF),
    # Katakana Phonetic Extensions
    (0x31F0, 0x31FF),
    # Enclosed CJK Letters and Months
    (0x32D0, 0x32FE),
    # CJK Compatibility
    (0x3300, 0x3357),
    # Halfwidth and Fullwidth Forms
    (0xFF65, 0xFF9F),

    # Kana Extended-B
    (0x1AFF0, 0x1AFF3), (0x1AFF5, 0x1AFFB), (0x1AFFD, 0x1AFFE),
    # Kana Supplement
    (0x1B000, 0x1B0FF),
    # Kana Extended-A
    (0x1B100, 0x1B122),
    # Small Kana Extension
    (0x1B132, 0x1B132), (0x1B150, 0x1B152), (0x1B155, 0x1B155), (0x1B164, 0x1B167),
    # Enclosed Ideographic Supplement
    (0x1F200, 0x1F202)
]

# At least one letter or numeral
def is_word_alphanumeric(token):
    return any((char.isalnum() for char in token))

# At least one letter
def is_word_alphabetic(token):
    return any((char.isalpha() for char in token))

# At least one numeral
def is_num(token):
    return any((char.isnumeric() for char in token))

# All punctuation marks
def is_punc(token):
    return token and not any((char.isalnum() for char in token))

def is_han(char):
    char_ord = ord(char)

    return any((
        unicode_start <= char_ord <= unicode_end
        for unicode_start, unicode_end in UNICODE_HAN
    ))

def is_kana(char):
    char_ord = ord(char)

    return any((
        unicode_start <= char_ord <= unicode_end
        for unicode_start, unicode_end in UNICODE_KANA
    ))

def is_tibetan(char):
    # Tibetan
    return 0x0F00 <= ord(char) <= 0x0FFF

def has_han(token):
    return any((is_han(char) for char in token))

def has_kana(token):
    return any((is_kana(char) for char in token))

def has_tibetan(token):
    return any((is_tibetan(char) for char in token))
