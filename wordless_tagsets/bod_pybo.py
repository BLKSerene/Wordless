#
# Wordless: Mapping Table (pybo Tagset -> Universal POS Tags)
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

#
# Universal POS Tags: http://universaldependencies.org/u/pos/all.html
#

mappings = [
    ['ADJ', 'ADJ', 'Adjectives', ''],
    ['ADP', 'ADP', 'Adposition', ''],
    ['ADV', 'ADV', 'Adverb', ''],
    ['AUX', 'AUX', 'Auxiliary', ''],
    ['CONJ', 'CONJ', 'Conjunction', ''],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', ''],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', ''],
    ['DET', 'DET', 'Determiner', ''],
    ['INTJ', 'INTJ', 'Interjection', ''],
    ['NOUN', 'NOUN', 'Noun', ''],
    ['PROPN', 'PROPN', 'Proper noun', ''],
    ['NUM', 'NUM', 'Numeral', ''],
    ['PART', 'PART', 'Particle', ''],
    ['PRON', 'PRON', 'Pronoun', ''],
    ['VERB', 'VERB', 'Verb', ''],

    ['punct', 'PUNCT', 'Punctuation', ''],
    ['SYM', 'SYM', 'Symbol', ''],
    ['X', 'X', 'Other', ''],

    ['OTHER', 'X', '', ''],
    ['OOV', 'X', '', ''],
    ['non-word', 'X', '', ''],
    ['non-bo', 'X', '', '']
]
