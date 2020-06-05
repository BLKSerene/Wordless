#
# Wordless: Tagsets - Penn Treebank Tagset
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

#
# Penn Treebank Tagset: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
#
# Universal POS Tags: http://universaldependencies.org/u/pos/all.html
#

mappings = [
    ['CC', 'CCONJ', 'Coordinating conjunction', ''],
    ['CD', 'NUM', 'Cardinal number', ''],
    ['DT', 'DET', 'Determiner', ''],
    ['EX', 'ADV', 'Existential "there"', 'there'],
    ['FW', 'X', 'Foreign word', ''],
    ['IN', 'ADP/SCONJ', 'Preposition or subordinating conjunction', ''],

    ['JJ', 'ADJ', 'Adjective', ''],
    ['JJR', 'ADJ', 'Adjective, comparative', ''],
    ['JJS', 'ADJ', 'Adjective, superlative', ''],

    ['LS', 'SYM', 'List item marker', ''],
    ['MD', 'AUX', 'Modal', ''],

    ['NN', 'NOUN', 'Noun, singular or mass', ''],
    ['NNS', 'NOUN', 'Noun, plural', ''],
    ['NNP', 'PROPN', 'Proper noun, singular', ''],
    ['NNPS', 'PROPN', 'Proper noun, plural', ''],

    ['PDT', 'PART', 'Predeterminer', ''],
    ['POS', 'PART', 'Possessive ending', ''],

    ['PRP', 'PRON', 'Personal pronoun', ''],
    ['PRP$', 'PRON', 'Possessive pronoun', ''],

    ['RB', 'ADV', 'Adverb', ''],
    ['RBR', 'ADV', 'Adverb, comparative', ''],
    ['RBS', 'ADV', 'Adverb, superlative', ''],

    ['RP', 'PART', 'Particle', ''],
    ['SYM', 'SYM', 'Symbol', ''],
    ['TO', 'PART', '"to"', 'to'],
    ['UH', 'INTJ', 'Interjection', ''],

    ['VB', 'VERB', 'Verb, base form', ''],
    ['VBD', 'VERB', 'Verb, past tense', ''],
    ['VBG', 'VERB', 'Verb, gerund or present participle', ''],
    ['VBN', 'VERB', 'Verb, past participle', ''],
    ['VBP', 'VERB', 'Verb, non-3rd person singular present', ''],
    ['VBZ', 'VERB', 'Verb, 3rd person singular present', ''],

    ['WDT', 'DET', 'Wh-determiner', ''],
    ['WP', 'PRON', 'Wh-pronoun', ''],
    ['WP$', 'PRON', 'Possessive wh-pronoun', ''],
    ['WRB', 'ADV', 'Wh-adverb', ''],

    ['\'\'', 'PUNCT', 'Single quotation mark', '\''],
    ['(', 'PUNCT', 'Left round and curly bracket', '( {'],
    [')', 'PUNCT', 'Right round and curly bracket', ') }'],
    [',', 'PUNCT', 'Comma', ','],
    ['.', 'PUNCT', 'Period, question mark and exclamation mark', '. ? !'],
    [':', 'PUNCT', 'Colon and semicolon', ': ;'],
    ['``', 'PUNCT', 'Double quotation mark and backtick', '" `'],

    ['#', 'SYM', 'Number sign', '#'],
    ['$', 'SYM', 'Dollar sign', '$']
]
