# ----------------------------------------------------------------------
# Wordless: Tagsets - Yunshan Cup 2020
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

# Reference: https://github.com/FoVNull/SeqLabeling/blob/main/reference/Lao_POS.tsv
tagset_mapping = [
    ['N', 'NOUN', '名词', ''],
    ['TTL', 'NOUN', '称号名词', ''],
    ['PRN', 'PROPN', '专有名词', ''],

    ['NTR', 'PRON', '疑问代词', ''],
    ['DMN', 'PRON', '指示代词', ''],
    ['PRS', 'PRON', '人称代词', ''],
    ['REL', 'PRON', '关系代词', ''],

    ['V', 'VERB', '动词', ''],

    ['PRA', 'AUX', '前置助动词', ''],
    ['PVA', 'AUX', '后置助动词', ''],

    ['ADJ', 'ADJ', '形容词', ''],
    ['ADV', 'ADV', '副词', ''],

    ['DBQ', 'DET', '数词前限定词', ''],
    ['DAQ', 'DET', '数词后限定词', ''],
    ['IBQ', 'DET', '数词前不定限定词', ''],
    ['IAQ', 'DET', '数词后不定限定词', ''],
    ['DAN', 'DET', '名词后限定词', ''],
    ['IAC', 'DET', '名词后不定限定词', ''],

    ['CNM', 'NUM', '基数词', ''],
    ['ONM', 'ADJ', '序数词', ''],

    ['COJ', 'CONJ', '连词', ''],
    ['PRE', 'ADP', '介词', ''],

    ['CLF', 'PART', '量词', ''],
    ['FIX', 'PART', '前置词', ''],
    ['NEG', 'PART', '否定词', ''],

    ['INT', 'INTJ', '语气词', ''],
    ['PUNCT', 'PUNCT', '标点符号', '']
]
