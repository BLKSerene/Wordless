#
# Wordless: Tagsets - UniDic Tagset
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

# UniDic Tagset: https://gist.github.com/masayu-a/e3eee0637c07d4019ec9
# Universal POS Tags: http://universaldependencies.org/u/pos/all.html
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

    ['連体詞', 'PART', 'Adnominal', ''],
    ['未知語', 'X', 'Unknown words', ''],
    ['カタカナ文', 'X', 'Katakana', ''],
    ['漢文', 'X', 'Chinese writing', ''],
    ['言いよどみ', 'X', 'Hesitation', ''],
    ['web誤脱', 'X', 'Errors and omissions', ''],
    ['方言', 'X', 'Dialect', ''],
    ['ローマ字文', 'X', 'Latin alphabet', ''],
    ['新規未知語', 'X', 'New unknown word', '']
]
