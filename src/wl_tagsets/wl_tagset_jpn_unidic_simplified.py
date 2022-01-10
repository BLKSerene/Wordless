# ----------------------------------------------------------------------
# Wordless: Tagsets - UniDic Tagset (Simplified)
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

# UniDic Tagset: https://gist.github.com/masayu-a/e3eee0637c07d4019ec9
# Universal POS Tags: http://universaldependencies.org/u/pos/all.html
MAPPINGS = [
    ['代名詞', 'PRON', 'Pronoun', ''],
    ['副詞', 'ADV', 'Adverb', ''],
    ['助動詞', 'AUX', 'Auxiliary verb', ''],
    ['助詞', 'PART', 'Particle', ''],
    ['動詞', 'VERB', 'Verb', ''],
    ['名詞', 'NOUN', 'Noun', ''],
    ['形容詞', 'ADJ', 'Adjective', ''],
    ['形状詞', 'NOUN', 'Adjectival noun', ''],
    ['感動詞', 'INTJ', 'Interjection', ''],
    ['接尾辞', 'PART', 'Suffix', ''],
    ['接続詞', 'CONJ', 'Conjunction', ''],
    ['接頭辞', 'PART', 'Prefix', ''],
    ['空白', 'X', 'Whitespace', ''],
    ['補助記号', 'PUNCT/SYM', 'Supplementary symbol', ''],
    ['記号', 'SYM', 'Symbol', ''],
    ['URL', 'SYM', 'URL', ''],
    ['連体詞', 'PART', 'Adnominal', ''],

    ['未知語', 'X', 'Unknown words', ''],
    ['カタカナ文', 'X', 'Katakana', ''],
    ['oov', 'X', 'Unknown words', ''],
    ['漢文', 'X', 'Chinese writing', ''],
    ['英単語', 'X', 'English Word', ''],
    ['言いよどみ', 'X', 'Hesitation', ''],
    ['web誤脱', 'X', 'Errors and omissions', ''],
    ['方言', 'X', 'Dialect', ''],
    ['ローマ字文', 'X', 'Latin alphabet', ''],
    ['新規未知語', 'X', 'New unknown word', '']
]
