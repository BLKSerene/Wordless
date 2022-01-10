# ----------------------------------------------------------------------
# Wordless: Tagsets - Penn Treebank Tagset
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

# Penn Treebank Tagset: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# Universal POS Tags: http://universaldependencies.org/u/pos/all.html
MAPPINGS = [
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
