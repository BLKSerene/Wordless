# ----------------------------------------------------------------------
# Wordless: Tagsets - Asian Language Treebank
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

# Reference: https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/Khmer-annotation-guideline.pdf
tagset_mapping = [
    ['n', 'NOUN', 'General nouns, can be subjects or objects of tokens tagged by v', ''],
    ['v', 'VERB', 'General verbs, can take tokens tagged by n as arguments', ''],
    ['a', 'ADJ', 'General adjectives, can directly describe or modify tokens tagged by n', ''],
    ['o', 'PART', 'Other modifications or complements for tokens or larger syntactic parts', ''],

    ['1', 'NUM', 'General numbers', ''],
    ['.', 'PUNCT', 'General punctuation marks', ''],
    ['+', 'X', 'A catch-all category, for tokens with weak syntactic roles', '']
]
