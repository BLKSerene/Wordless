#
# Wordless: Mapping Table (ORCHID Tagset -> Universal POS Tags)
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

#
# ORCHID Tagset: https://www.researchgate.net/publication/243783378_Thai_Part-of-speech_Tagged_Corpus_ORCHID
#
# Universal POS Tags: http://universaldependencies.org/u/pos/all.html
#

mappings = [
    ['NPRP', 'PROPN', 'Proper noun', ''],
    
    ['NCNM', 'NUM', 'Cardinal number', ''],
    ['NONM', 'ADJ', 'Ordinal number', ''],

    ['NLBL', 'NOUN', 'Label noun', ''],
    ['NCMN', 'NOUN', 'Common noun', ''],
    ['NTTL', 'NOUN', 'Title noun', ''],

    ['PPRS', 'PRON', 'Personal pronoun', ''],
    ['PDMN', 'PRON', 'Demonstrative pronoun', ''],
    ['PNTR', 'PRON', 'Interrogative pronoun', ''],
    ['PREL', 'PRON', 'Relative pronoun', ''],

    ['VACT', 'VERB', 'Active verb', ''],
    ['VSTA', 'VERB', 'Static verb', ''],
    ['VATT', 'VERB', 'Attributive verb', ''],

    ['XVBM', 'AUX', 'Pre-verb auxiliary, before negator “ไม่”', ''],
    ['XVAM', 'AUX', 'Pre-verb auxiliary, after negator "ไม่"', ''],
    ['XVMM', 'AUX', 'Pre-verb auxiliary, before or after negator "ไม่"', ''],
    ['XVBB', 'AUX', 'Pre-verb auxiliary, in imperative mood', ''],
    ['XVAE', 'AUX', 'Post-verb auxiliary', ''],

    ['DDAN', 'DET', 'Definite determiner,\nafter noun without classifier in between', ''],
    ['DDAC', 'DET', 'Definite determiner,\nallowing classifier in between', ''],
    ['DDBQ', 'DET', 'Definite determiner,\nbetween noun and classifier or preceding quantitative expression', ''],
    ['DDAQ', 'DET', 'Definite determiner,\nfollowing quantitative expression', ''],
    ['DIAC', 'DET', 'Indefinite determiner,\nfollowing noun; allowing classfifier in between', ''],
    ['DIBQ', 'DET', 'Indefinite determiner,\nbetween noun and classifier or preceding quantitative expression', ''],
    ['DIAQ', 'DET', 'Indefinite determiner,\nfollowing quantitative expression', ''],
    ['DCNM', 'DET', 'Determiner,\ncardinal number expression', ''],
    ['DONM', 'DET', 'Determiner,\nordinal number expression', ''],

    ['ADVN', 'ADV', 'Adverb with normal form', ''],
    ['ADVI', 'ADV', 'Adverb with iterative form', ''],
    ['ADVP', 'ADV', 'Adverb with prefixed form', ''],
    ['ADVS', 'ADV', 'Sentential adverb', ''],

    ['CNIT', 'PART', 'Unit classifier', ''],
    ['CLTV', 'PART', 'Collective classifier', ''],
    ['CMTR', 'PART', 'Measurement classifier', ''],
    ['CFQC', 'PART', 'Frequency classifier', ''],
    ['CVBL', 'PART', 'Verbal classifier', ''],

    ['JCRG', 'CCONJ', 'Coordinating conjunction', ''],
    ['JCMP', 'CCONJ', 'Comparative conjunction', ''],
    ['JSBR', 'SCONJ', 'Subordinating conjunctino', ''],

    ['RPRE', 'ADP', 'Preposition', ''],

    ['INT', 'INTJ', 'Interjection', ''],

    ['FIXN', 'PART', 'Nominal prefix', ''],
    ['FIXV', 'PART', 'Adverbial prefix', ''],

    ['EAFF', 'PART', 'Ending for affirmative sentence', ''],
    ['EITT', 'PART', 'Ending for interrogative sentence', ''],

    ['NEG', 'PART', 'Negator', ''],

    ['PUNC', 'PUNCT', 'Punctuation', '( ) “ , ;']
]
