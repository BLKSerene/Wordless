#
# Wordless: Tagsets - pybo Tagset
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

#
# pybo Tagset: https://github.com/Esukhia/pybo/blob/master/pybo/vars.py
#
# Universal POS Tags: http://universaldependencies.org/u/pos/all.html
#

mappings = [
    # pos
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
    ['OOV', 'X', '', 'Unknown'],
    ['NON-WORD', 'X', '', 'Non-word'],

    # chunk_type
    ['BO', 'X', '', 'Tibetan language'],
    ['LATIN', 'X', '', 'Latin languages'],
    ['CJK', 'X', '', 'CJK languages'],
    ['OTHER', 'X', '', 'Other languages'],

    ['NUM', 'NUM', '', 'Numeral'],
    ['NON_NUM', 'X', '', 'Non-numeral'],
    ['PUNCT', 'PUNCT', '', 'Punctuation'],
    ['NON_PUNCT', 'X', '', 'Non-punctuation'],
    ['SYM', 'SYM', '', 'Symbol'],
    ['NON_SYM', 'X', '', 'Non-symbol'],
    ['SPACE', 'X', '', 'Space'],
    ['NON_SPACE', 'X', '', 'Non-space']
]
