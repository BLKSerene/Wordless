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
# Penn Treebank Tagset (OntoNotes 5): https://spacy.io/api/annotation
#
# Universal POS Tags: http://universaldependencies.org/u/pos/all.html
#

mappings = [
    ['ADD', 'X', 'Email', ''],
    ['AFX', 'X', 'Affix', ''],
    ['BES', 'AUX', 'Auxiliary "be"', 'be'],
    ['CC', 'CCONJ', 'Conjunction, coordinating', ''],
    ['CD', 'NUM', 'Cardinal number', ''],
    ['DT', 'DET', 'Determiner', ''],
    ['EX', 'PRON', 'Existential "there"', 'there'],
    ['FW', 'X', 'Foreign word', ''],
    ['GW', 'X', 'Additional word in multi-word expression', ''],
    ['HVS', 'VERB', 'Forms of "have"', 'have'],
    ['HYPH', 'PUNCT', 'Punctuation mark, hythen', ''],
    ['IN', 'ADP/SCONJ', 'Conjunction, subordinating or preposition', ''],

    ['JJ', 'ADJ', 'Adjective', ''],
    ['JJR', 'ADJ', 'Adjective, comparative', ''],
    ['JJS', 'ADJ', 'Adjective, superlative', ''],

    ['LS', 'SYM', 'List item marker', ''],
    ['MD', 'AUX', 'Verb, modal auxiliary', ''],
    ['NFP', 'PUNCT', 'Superfluous punctuation', ''],
    ['NIL', 'X', 'Missing tag', ''],

    ['NN', 'NOUN', 'Noun, singular or mass', ''],
    ['NNS', 'NOUN', 'Noun, plural', ''],
    ['NNP', 'PROPN', 'Noun, proper singular', ''],
    ['NNPS', 'PROPN', 'Noun, proper plural', ''],

    ['PDT', 'DET', 'Predeterminer', ''],
    ['POS', 'PART', 'Possessive ending', ''],

    ['PRP', 'PRON', 'Pronoun, personal', ''],
    ['PRP$', 'PRON', 'Pronoun, possessive', ''],

    ['RB', 'ADV', 'Adverb', ''],
    ['RBR', 'ADV', 'Adverb, comparative', ''],
    ['RBS', 'ADV', 'Adverb, superlative', ''],

    ['RP', 'ADP', 'Adverb, particle', ''],
    ['SYM', 'SYM', 'Symbol', ''],
    ['TO', 'PART', 'Infinitival "to"', 'to'],
    ['UH', 'INTJ', 'Interjection', ''],

    ['VB', 'VERB', 'Verb, base form', ''],
    ['VBD', 'VERB', 'Verb, past tense', ''],
    ['VBG', 'VERB', 'Verb, gerund or present participle', ''],
    ['VBN', 'VERB', 'Verb, past participle', ''],
    ['VBP', 'VERB', 'Verb, non-3rd person singular present', ''],
    ['VBZ', 'VERB', 'Verb, 3rd person singular present', ''],

    ['WDT', 'DET', 'Wh-determiner', ''],
    ['WP', 'PRON', 'Wh-pronoun, personal', ''],
    ['WP$', 'PRON', 'Wh-pronoun, possessive', ''],
    ['WRB', 'ADV', 'Wh-adverb', ''],

    ['-LRB-', 'PUNCT', 'Left bracket', '( [ {'],
    ['-RRB-', 'PUNCT', 'Right bracket', ') ] }'],
    [',', 'PUNCT', 'Punctuation mark, comma', ','],
    [':', 'PUNCT', 'Punctuation mark, colon, semicolon, hyphen or en dash', ': ; - –'],
    ['.', 'PUNCT', 'Punctuation mark, sentence closer or dollar sign', '. ? ! $'],
    ['\'\'', 'PUNCT', 'Punctuation mark, quotation mark, guillemet or single backtick', '\' " « » `'],
    ['``', 'PUNCT', 'Punctuation mark, double backtick', '``'],
    ['', 'PUNCT', 'Punctuation mark, em dash', '—'],

    ['_SP', 'X', 'Space', ' '],
    ['XX', 'X', 'Unknown', '']
]
