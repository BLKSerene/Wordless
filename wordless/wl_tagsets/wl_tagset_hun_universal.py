# ----------------------------------------------------------------------
# Wordless: Tagsets - Universal POS tags - Hungarian
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

# Universal POS Tags: https://universaldependencies.org/hu/pos/
tagset_mapping = [
    ['ADJ', 'ADJ', 'Adjective', '[English] big, old, green, African, incomprehensible, first, second, third'],
    ['ADP', 'ADP', 'Adposition', '[English] in, to, during'],
    ['ADV', 'ADV', 'Adverb', '[English] very, well, exactly, tomorrow, up, down\nInterrogative/relative adverbs (including when used to mark a clause that is circumstantial, not interrogative or relative): [English] where, when, how, why, whenever, wherever\nDemonstrative adverbs: [English] here, there, now, then\nIndefinite adverbs: [English] somewhere, sometime, anywhere, anytime\nTotality adverbs: [English] everywhere, always\nNegative adverbs: [English] nowhere, never; [German] usw.'],
    ['AUX', 'AUX', 'Auxiliary', 'volna, fog, talál, szokott'],
    ['CONJ', 'CONJ', 'Coordinating/subordinating conjunction', 'See CCONJ and SCONJ'],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', '[English] and, or, but'],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', '[English] (I believe) that (he will come.), if, while'],
    ['DET', 'DET', 'Determiner', 'azokat (a könyveket)'],
    ['INTJ', 'INTJ', 'Interjection', '[English] psst, ouch, bravo, hello'],
    ['NOUN', 'NOUN', 'Noun', '[English] girl, tree, etc., beauty, decision'],
    ['PROPN', 'PROPN', 'Proper noun', '[English] Mary, John, London, NATO, HBO, john.doe@universal.org, http://universaldependencies.org/, 1-800-COMPANY'],
    ['NUM', 'NUM', 'Numeral', '0, 1, 2, 3, 4, 5, 2014, 1000000, 3.14159265359\n11/11/1918, 11:00\none, two, three, seventy-seven\nk (abbreviation for thousand), m (abbreviation for million)\nI, II, III, IV, V, MMXIV'],
    ['PART', 'PART', 'Particle', '(Nem) ette (meg a levest.)'],
    ['PRON', 'PRON', 'Pronoun', 'Personal pronouns: [English] I, you, he, she, it, we, they\nReflexive pronouns: [English] myself, yourself, himself, herself, itself, ourselves, yourselves, theirselves\nInterrogative pronouns: [English] who, What (do you think?)\nRelative pronouns (unlike SCONJ relativizers, relative pronouns play a nominal role in the relative clause): [English] (a cat) who (eats fish), that, which, (I wonder) what (you think.)\nIndefinite pronouns: [English] somebody, something, anybody, anything\nTotal pronouns: [English] everybody, everything\nNegative pronouns: [English] nobody, nothing\nPossessive pronouns (which usually stand alone as a nominal): [English] mine, yours, his, hers, its, ours, theirs\nAttributive possessive pronouns (in some languages; others use DET for similar words): [English] my, your'],
    ['VERB', 'VERB', 'Verb', 'Látom (a madarat.), Látok (egy madarat.)'],

    ['PUNCT', 'PUNCT', 'Punctuation', 'Period: .\nComma: ,\nParentheses: ()'],
    ['SYM', 'SYM', 'Symbol', '$, %, §, ©\n+, −, ×, ÷, =, <, >\n:), ♥‿♥, 😝'],
    ['X', 'X', 'Other', '[English] (And then he just) xfgh pdl jklw']
]
