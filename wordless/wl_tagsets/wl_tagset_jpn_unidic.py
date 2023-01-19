# ----------------------------------------------------------------------
# Wordless: Tagsets - UniDic Tagset
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

# Reference: https://gist.github.com/masayu-a/e3eee0637c07d4019ec9
MAPPINGS = [
    ['代名詞', 'PRON', 'Pronoun', ''],
    ['副詞', 'ADV', 'Adverb', ''],
    ['助動詞', 'AUX', 'Auxiliary verb', ''],

    ['助詞-係助詞', 'PART', 'Binding particle', ''],
    ['助詞-副助詞', 'PART', 'Adverbial particle', ''],
    ['助詞-接続助詞', 'PART', 'Conjunctive particle', ''],
    ['助詞-格助詞', 'PART', 'Case particle', ''],
    ['助詞-準体助詞', 'PART', 'Nominal particle', ''],
    ['助詞-終助詞', 'PART', 'Phrase-final particle', ''],

    ['動詞-一般', 'VERB', 'General verb', ''],
    ['動詞-非自立可能', 'VERB', 'Bound verb', ''],

    ['名詞-助動詞語幹', 'NOUN', 'Auxiliary noun', ''],
    ['名詞-固有名詞-一般', 'NOUN', 'General proper noun', ''],
    ['名詞-固有名詞-人名-一般', 'NOUN', 'General name', ''],
    ['名詞-固有名詞-人名-名', 'NOUN', 'Firstname', ''],
    ['名詞-固有名詞-人名-姓', 'NOUN', 'Surname', ''],
    ['名詞-固有名詞-地名-一般', 'NOUN', 'General place name', ''],
    ['名詞-固有名詞-地名-国', 'NOUN', 'Country name', ''],
    ['名詞-数詞', 'NOUN', 'Numeral', ''],
    ['名詞-普通名詞-サ変可能', 'NOUN', 'Suru-verbal common noun', ''],
    ['名詞-普通名詞-サ変形状詞可能', 'NOUN', 'Adjectival verbal common noun', ''],
    ['名詞-普通名詞-一般', 'NOUN', 'General common noun', ''],
    ['名詞-普通名詞-副詞可能', 'NOUN', 'Adverbial common noun', ''],
    ['名詞-普通名詞-助数詞可能', 'NOUN', 'Counter words', ''],
    ['名詞-普通名詞-形状詞可能', 'NOUN', 'Adjectival common noun', ''],

    ['形容詞-一般', 'ADJ', 'General adjective', ''],
    ['形容詞-非自立可能', 'ADJ', 'Bound adjective', ''],

    ['形状詞-タリ', 'NOUN', 'Adjectival noun', ''],
    ['形状詞-一般', 'NOUN', 'General adjectival noun', ''],
    ['形状詞-助動詞語幹', 'NOUN', 'Auxiliary adjectival noun', ''],

    ['感動詞-フィラー', 'INTJ', 'Filler', ''],
    ['感動詞-一般', 'INTJ', 'General interjection', ''],

    ['接尾辞-動詞的', 'PART', 'Verbal suffix', ''],
    ['接尾辞-名詞的-サ変可能', 'PART', 'Suru-verbal nominal suffix', ''],
    ['接尾辞-名詞的-一般', 'PART', 'General nominal suffix', ''],
    ['接尾辞-名詞的-副詞可能', 'PART', 'Adverbial nominal suffix', ''],
    ['接尾辞-名詞的-助数詞', 'PART', 'Counter nominal suffix', ''],
    ['接尾辞-形容詞的', 'PART', 'Adjective suffix', ''],
    ['接尾辞-形状詞的', 'PART', 'Adjectival noun suffix', ''],

    ['接続詞', 'CONJ', 'Conjunction', ''],
    ['接頭辞', 'PART', 'Prefix', ''],

    ['空白', 'X', 'Whitespace', ''],

    ['補助記号-一般', 'SYM', 'General supplementary symbol', ''],
    ['補助記号-句点', 'PUNCT', 'Period', ''],
    ['補助記号-括弧閉', 'PUNCT', 'Close bracket', ''],
    ['補助記号-括弧開', 'PUNCT', 'Open bracket', ''],
    ['補助記号-読点', 'PUNCT', 'Comma', ''],
    ['補助記号-ＡＡ-一般', 'SYM', 'General ASCII art', ''],
    ['補助記号-ＡＡ-顔文字', 'SYM', 'Emoticon', ''],

    ['記号-一般', 'SYM', 'General symbol', ''],
    ['記号-文字', 'SYM', 'Character', ''],

    ['連体詞', 'PART', 'Adnominal', '']
]
