# ----------------------------------------------------------------------
# Wordless: Tagsets - Universal POS tags - Basque
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

# Universal POS Tags: https://universaldependencies.org/eu/pos/
tagset_mapping = [
    ['ADJ', 'ADJ', 'Adjective', 'Following the noun: (etxe) handia\nPreceding the noun: goiko (etxea)'],
    ['ADP', 'ADP', 'Adposition', '[English] in, to, during'],
    ['ADV', 'ADV', 'Adverb', 'Following the verb: azkar (doa)\nPreceding the verb: (darama) sarritan\noso azkar'],
    ['AUX', 'AUX', 'Auxiliary', 'Tense auxiliaries: [English] has (done), is (doing), will (do)\nPassive auxiliaries: [English] was (done), got (done)\nModal auxiliaries: [English] should (do), must (do)\nVerbal copulas: [English] (He) is (a teacher.)\nAgreement auxiliaries: [K’iche’] la (2nd person singular formal), alaq (2nd person plural formal)'],
    ['CONJ', 'CONJ', 'Coordinating/subordinating conjunction', 'See CCONJ and SCONJ'],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', '[English] and, or, but'],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', '[English] (I believe) that (he will come.), if, while'],
    ['DET', 'DET', 'Determiner', 'Articles (a closed class indicating definiteness, specificity or givenness): [English] a, an, the\nPossessive determiners (which modify a nominal; note that some languages use PRON for similar words): [Czech] můj, tvůj, jeho, její, náš, váš, jejich\nDemonstrative determiners: [English] (I saw) this (car yesterday.)\nInterrogative determiners: [English] Which (car do you like?)\nRelative determiners: [English] (I wonder) which (car you like.)\nQuantity determiners (quantifiers):\n\tIndefinite: [English] any\n\tUniversal: [English] all\n\tNegative: [English] (We have) no (cars available.)'],
    ['INTJ', 'INTJ', 'Interjection', '[English] psst, ouch, bravo, hello'],
    ['NOUN', 'NOUN', 'Noun', 'neska, katu, zuhaitz, aire, edertasun'],
    ['PROPN', 'PROPN', 'Proper noun', 'Jon, Jon\nUkrainia, Ucraine\nMadril, Madrid'],
    ['NUM', 'NUM', 'Numeral', '0, 1, 2, 3, 4, 5, 2014, 1000000, 3.14159265359\n11/11/1918, 11:00\n[English] one, two, three, seventy-seven\nk (abbreviation for thousand), m (abbreviation for million)\nI, II, III, IV, V, MMXIV'],
    ['PART', 'PART', 'Particle', 'Possessive marker: [English] ’s\nNegation particle: [English] not; [German] nicht\nQuestion particle: [Japanese] か/ka (adding this particle to the end of a clause turns the clause into a question); [Turkish] mu\nSentence modality: [Czech] ať, kéž, nechť'],
    ['PRON', 'PRON', 'Pronoun', 'Personal pronouns: [English] I, you, he, she, it, we, they\nReflexive pronouns: [English] myself, yourself, himself, herself, itself, ourselves, yourselves, theirselves\nInterrogative pronouns: [English] who, What (do you think?)\nRelative pronouns (unlike SCONJ relativizers, relative pronouns play a nominal role in the relative clause): [English] (a cat) who (eats fish), that, which, (I wonder) what (you think.)\nIndefinite pronouns: [English] somebody, something, anybody, anything\nTotal pronouns: [English] everybody, everything\nNegative pronouns: [English] nobody, nothing\nPossessive pronouns (which usually stand alone as a nominal): [English] mine, yours, his, hers, its, ours, theirs\nAttributive possessive pronouns (in some languages; others use DET for similar words): [English] my, your'],
    ['VERB', 'VERB', 'Verb', 'Complete: daramat, dakarkio\nIncomplete: ekarri (du)'],

    ['PUNCT', 'PUNCT', 'Punctuation', 'Period: .\nComma: ,\nParentheses: ()'],
    ['SYM', 'SYM', 'Symbol', '$, %, §, ©\n+, −, ×, ÷, =, <, >\n:), ♥‿♥, 😝'],
    ['X', 'X', 'Other', '[English] (And then he just) xfgh pdl jklw']
]
