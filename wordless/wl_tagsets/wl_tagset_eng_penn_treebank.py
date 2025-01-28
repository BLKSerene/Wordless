# ----------------------------------------------------------------------
# Wordless: Tagsets - Penn treebank
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
#     https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
#     https://github.com/nltk/nltk_data/blob/gh-pages/packages/taggers/universal_tagset.zip
tagset_mapping = [
    ['CC', 'CCONJ', 'Coordinating conjunction', ''],
    ['CD', 'NUM', 'Cardinal number', ''],
    ['CD|RB', 'X', '', ''],
    ['DT', 'DET', 'Determiner', ''],
    ['EX', 'DET', 'Existential "there"', 'there'],
    ['FW', 'X', 'Foreign word', ''],
    ['IN', 'ADP/SCONJ', 'Preposition or subordinating conjunction', ''],
    ['IN|RP', 'ADP/SCONJ', '', ''],

    ['JJ', 'ADJ', 'Adjective', ''],
    ['JJ|RB', 'ADJ', '', ''],
    ['JJ|VBG', 'ADJ', '', ''],
    ['JJR', 'ADJ', 'Adjective, comparative', ''],
    ['JJRJR', 'ADJ', '', ''],
    ['JJS', 'ADJ', 'Adjective, superlative', ''],

    ['LS', 'PUNCT', 'List item marker', ''],
    ['MD', 'VERB', 'Modal', ''],

    ['NN', 'NOUN', 'Noun, singular or mass', ''],
    ['NN|NNS', 'NOUN', '', ''],
    ['NN|SYM', 'NOUN', '', ''],
    ['NN|VBG', 'NOUN', '', ''],
    ['NNS', 'NOUN', 'Noun, plural', ''],
    ['NNP', 'PROPN', 'Proper noun, singular', ''],
    ['NNPS', 'PROPN', 'Proper noun, plural', ''],
    ['NP', 'NOUN', '', ''],

    ['PDT', 'DET', 'Predeterminer', ''],
    ['POS', 'PART', 'Possessive ending', ''],

    ['PRP', 'PRON', 'Personal pronoun', ''],
    ['PRP|VBP', 'PRON', '', ''],
    ['PRP$', 'PRON', 'Possessive pronoun', ''],
    ['PRT', 'PART', '', ''],

    ['RB', 'ADV', 'Adverb', ''],
    ['RB|RP', 'ADV', '', ''],
    ['RB|VBG', 'ADV', '', ''],
    ['RBR', 'ADV', 'Adverb, comparative', ''],
    ['RBS', 'ADV', 'Adverb, superlative', ''],

    ['RN', 'X', '', ''],
    ['RP', 'PART', 'Particle', ''],
    ['SYM', 'SYM', 'Symbol', ''],
    ['TO', 'PART', '"to"', 'to'],
    ['UH', 'INTJ', 'Interjection', ''],

    ['VB', 'VERB', 'Verb, base form', ''],
    ['VBD', 'VERB', 'Verb, past tense', ''],
    ['VBD|VBN', 'VERB', '', ''],
    ['VBG', 'VERB', 'Verb, gerund or present participle', ''],
    ['VBG|NN', 'VERB', '', ''],
    ['VBN', 'VERB', 'Verb, past participle', ''],
    ['VBP', 'VERB', 'Verb, non-3rd person singular present', ''],
    ['VBP|TO', 'VERB', '', ''],
    ['VBZ', 'VERB', 'Verb, 3rd person singular present', ''],
    ['VP', 'VERB', '', ''],

    ['WDT', 'DET', 'Wh-determiner', ''],
    ['WH', 'X', '', ''],
    ['WP', 'PRON', 'Wh-pronoun', ''],
    ['WP$', 'PRON', 'Possessive wh-pronoun', ''],
    ['WRB', 'ADV', 'Wh-adverb', ''],

    [',', 'PUNCT', 'Comma', ','],
    ['.', 'PUNCT', 'Period', '.'],
    ['?', 'PUNCT', 'Question mark', '?'],
    ['!', 'PUNCT', 'Exclamation mark', '!'],
    [':', 'PUNCT', 'Colon and semicolon', ': ;'],
    ["''", 'PUNCT', 'Single quotation mark', "'"],
    ['``', 'PUNCT', 'Double quotation mark and backtick', '" `'],
    ['(', 'PUNCT', 'Left round and curly bracket', '( {'],
    [')', 'PUNCT', 'Right round and curly bracket', ') }'],
    ['-LRB-', 'PUNCT', 'Left round bracket', '('],
    ['-RRB-', 'PUNCT', 'Left round bracket', ')'],

    ['#', 'SYM', 'Number sign', '#'],
    ['$', 'SYM', 'Dollar sign', '$']
]
