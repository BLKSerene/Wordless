# ----------------------------------------------------------------------
# Utilities: Data - Extract the 1000 most common syllables from all easy documents of the corpus of Vietnamese text readability dataset on literature domain
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

import collections
import glob

syls = []
freq_syls = []

# The corpus of Vietnamese text readability dataset on literature domain: https://github.com/anvinhluong/Vietnamese-text-readability/blob/master/Vietnamese%20Text%20Readability%20Corpus.zip
for file in glob.glob('Vietnamese Text Readability Corpus/easy_*.txt'):
    print(f'Processing file {file}...')

    with open(file, 'r', encoding = 'utf_8') as f:
        syls.extend(f.read().split())

# Get the 1000 most frequent syllables (excluding punctuation marks)
for syl, freq in sorted(collections.Counter(syls).items(), key = lambda item: item[1], reverse = True):
    if any((char for char in syl if char.isalnum())):
        freq_syls.append((syl, freq))

    if len(freq_syls) >= 1000:
        break

with open('data/luong_nguyen_dinh_freq_syls_easy_1000.txt', 'w', encoding = 'utf_8') as f:
    for syl, _ in freq_syls:
        f.write(syl + '\n')
