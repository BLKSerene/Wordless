# ----------------------------------------------------------------------
# Wordless: Tagsets - Mecab
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
#     MeCab: https://docs.google.com/spreadsheets/u/0/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY/edit?usp=sharing
#     spaCy: https://github.com/explosion/spaCy/blob/2ce9a220dbd30d3a79c2a232230204a102fb3f1d/spacy/lang/ko/tag_map.py
tagset_mapping = [
    ['NNG', 'NOUN', '일반 명사', ''],
    ['NNP', 'PROPN', '고유 명사', ''],
    ['NNB', 'NOUN', '의존 명사', ''],
    ['NNBC', 'NOUN', '단위를 나타내는 명사', ''],
    ['NR', 'NUM', '수사', ''],
    ['NP', 'PRON', '대명사', ''],

    ['VV', 'VERB', '동사', ''],
    ['VA', 'ADJ', '형용사', ''],
    ['VX', 'AUX', '보조 용언', ''],
    ['VCP', 'ADP', '긍정 지정사', ''],
    ['VCN', 'ADJ', '부정 지정사', ''],

    ['MM', 'DET', '관형사', ''],
    ['MAG', 'ADV', '일반 부사', ''],
    ['MAJ', 'CONJ', '접속 부사', ''],

    ['IC', 'INTJ', '감탄사', ''],

    ['JKS', 'ADP', '주격 조사', ''],
    ['JKC', 'ADP', '보격 조사', ''],
    ['JKG', 'ADP', '관형격 조사', ''],
    ['JKO', 'ADP', '목적격 조사', ''],
    ['JKB', 'ADP', '부사격 조사', ''],
    ['JKV', 'ADP', '호격 조사', ''],
    ['JKQ', 'ADP', '인용격 조사', ''],
    ['JX', 'ADP', '보조사', ''],
    ['JC', 'CONJ', '접속 조사', ''],

    ['EP', 'X', '선어말 어미', ''],
    ['EF', 'X', '종결 어미', ''],
    ['EC', 'X', '연결 어미', ''],
    ['ETN', 'X', '명사형 전성 어미', ''],
    ['ETM', 'X', '관형형 전성 어미', ''],

    ['XPN', 'PART', '체언 접두사', ''],

    ['XSN', 'X', '명사 파생 접미사  ', ''],
    ['XSV', 'X', '동사 파생 접미사', ''],
    ['XSA', 'X', '형용사 파생 접미사', ''],

    ['XR', 'X', '어근', ''],

    ['SF', 'PUNCT', '마침표, 물음표, 느낌표', ''],
    ['SE', 'PUNCT', '줄임표', '…'],
    ['SSO', 'PUNCT', '여는 괄호', '( ['],
    ['SSC', 'PUNCT', '닫는 괄호', ') ]'],
    ['SC', 'PUNCT', '구분자', ', · / :'],
    ['SY', 'SYM', '', ''],

    ['SL', 'X', '외국어', ''],
    ['SH', 'X', '한자', ''],
    ['SN', 'NUM', '숫자', '']
]
