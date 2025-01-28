# ----------------------------------------------------------------------
# Wordless: Tagsets - Universal POS tags - Norwegian
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

# Universal POS Tags: https://universaldependencies.org/no/pos/
tagset_mapping = [
    ['ADJ', 'ADJ', 'Adjective', 'stor, gammel, grønn'],
    ['ADP', 'ADP', 'Adposition', 'i, på, utenfor'],
    ['ADV', 'ADV', 'Adverb', '(Han kom) nettopp, Derfor (kom han), nesten (ferdig)'],
    ['AUX', 'AUX', 'Auxiliary', 'Temporal: har (spist), er (kommet)\nPassive: blir (spist)\nModal: kan/skal/vil/må/bør (spise)\nCopula: er (god)'],
    ['CONJ', 'CONJ', 'Coordinating/subordinating conjunction', 'See CCONJ and SCONJ'],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', 'og, eller, men'],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', 'Complementizers: at, om\nAdverbial clause introducers: når, siden, fordi'],
    ['DET', 'DET', 'Determiner', 'Possessive: mitt (barn), våre (barn), (barnet) vårt\nDemonstrative: dette (barnet), det (barnet), den (bilen), (det) samme (barnet) , (det) andre (barnet), hvilken (bil), hvilket (hus)\nQuantifying: en (bil), et (barn), ei (jente), noen (biler), alle (biler), begge (bilene)'],
    ['INTJ', 'INTJ', 'Interjection', 'ja, nei, hei, hallo, heisan, å, ok, piip'],
    ['NOUN', 'NOUN', 'Noun', 'jente, katt, tre, luft, skjønnhet'],
    ['PROPN', 'PROPN', 'Proper noun', 'Kari, Ola\nOslo, Bergen'],
    ['NUM', 'NUM', 'Numeral', '0, 1, 2, 3, 4, 5, 2014, 1000000, 3.14159265359\ntre, femtito, fire-fem, tusen'],
    ['PART', 'PART', 'Particle', '(Han liker) ikke å (spise is)'],
    ['PRON', 'PRON', 'Pronoun', 'Personal: han, hun, det, ham, henne\nDemonstrative: dette\nReflexive: seg\nReciprocal: hverandre\nInterrogative: hvem, hva, hvilken\nTotality: alle\nIndefinite: noen\nRelative: som'],
    ['VERB', 'VERB', 'Verb', 'løpe, løper, løp, (har) løpt\nspise, spiser, spiste, (har) spist'],

    ['PUNCT', 'PUNCT', 'Punctuation', 'Period: .\nComma: ,\nParentheses: ()'],
    ['SYM', 'SYM', 'Symbol', '/, *  *, *'],
    ['X', 'X', 'Other', '[English] (And then he just) xfgh pdl jklw']
]
