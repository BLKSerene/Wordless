# ----------------------------------------------------------------------
# Wordless: Tagsets - Universal POS tags - English
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

# Universal POS Tags: https://universaldependencies.org/u/pos/
tagset_mapping = [
    ['ADJ', 'ADJ', 'Adjective', 'big, old, green, African, incomprehensible, first, second, third'],
    ['ADP', 'ADP', 'Adposition', 'in, to, during'],
    ['ADV', 'ADV', 'Adverb', 'very, well, exactly, tomorrow, up, down\nInterrogative/relative adverbs (including when used to mark a clause that is circumstantial, not interrogative or relative): where, when, how, why, whenever, wherever\nDemonstrative adverbs: here, there, now, then\nIndefinite adverbs: somewhere, sometime, anywhere, anytime\nTotality adverbs: everywhere, always\nNegative adverbs: nowhere, never; [German] usw.'],
    ['AUX', 'AUX', 'Auxiliary', 'Tense auxiliaries: has (done), is (doing), will (do)\nPassive auxiliaries: was (done), got (done)\nModal auxiliaries: should (do), must (do)\nVerbal copulas: (He) is (a teacher.)\nAgreement auxiliaries: [K’iche’] la (2nd person singular formal), alaq (2nd person plural formal)'],
    ['CONJ', 'CONJ', 'Coordinating/subordinating conjunction', 'See CCONJ and SCONJ'],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', 'and, or, but'],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', '(I believe) that (he will come.), if, while'],
    ['DET', 'DET', 'Determiner', 'Articles (a closed class indicating definiteness, specificity or givenness): a, an, the\nPossessive determiners (which modify a nominal; note that some languages use PRON for similar words): [Czech] můj, tvůj, jeho, její, náš, váš, jejich\nDemonstrative determiners: (I saw) this (car yesterday.)\nInterrogative determiners: Which (car do you like?)\nRelative determiners: (I wonder) which (car you like.)\nQuantity determiners (quantifiers):\n\tIndefinite: any\n\tUniversal: all\n\tNegative: (We have) no (cars available.)'],
    ['INTJ', 'INTJ', 'Interjection', 'psst, ouch, bravo, hello'],
    ['NOUN', 'NOUN', 'Noun', 'girl, tree, etc., beauty, decision'],
    ['PROPN', 'PROPN', 'Proper noun', 'Mary, John, London, NATO, HBO, john.doe@universal.org, http://universaldependencies.org/, 1-800-COMPANY'],
    ['NUM', 'NUM', 'Numeral', '0, 1, 2, 3, 4, 5, 2014, 1000000, 3.14159265359\n11/11/1918, 11:00\none, two, three, seventy-seven\nk (abbreviation for thousand), m (abbreviation for million)\nI, II, III, IV, V, MMXIV'],
    ['PART', 'PART', 'Particle', 'Possessive marker: ’s\nNegation particle: not; [German] nicht\nQuestion particle: [Japanese] か/ka (adding this particle to the end of a clause turns the clause into a question); [Turkish] mu\nSentence modality: [Czech] ať, kéž, nechť'],
    ['PRON', 'PRON', 'Pronoun', 'Personal pronouns: I, you, he, she, it, we, they\nReflexive pronouns: myself, yourself, himself, herself, itself, ourselves, yourselves, theirselves\nInterrogative pronouns: who, What (do you think?)\nRelative pronouns (unlike SCONJ relativizers, relative pronouns play a nominal role in the relative clause): (a cat) who (eats fish), that, which, (I wonder) what (you think.)\nIndefinite pronouns: somebody, something, anybody, anything\nTotal pronouns: everybody, everything\nNegative pronouns: nobody, nothing\nPossessive pronouns (which usually stand alone as a nominal): mine, yours, his, hers, its, ours, theirs\nAttributive possessive pronouns (in some languages; others use DET for similar words): my, your'],
    ['VERB', 'VERB', 'Verb', 'run, eat\nruns, ate\nrunning, eating'],

    ['PUNCT', 'PUNCT', 'Punctuation', 'Period: .\nComma: ,\nParentheses: ()'],
    ['SYM', 'SYM', 'Symbol', '$, %, §, ©\n+, −, ×, ÷, =, <, >\n:), ♥‿♥, 😝'],
    ['X', 'X', 'Other', '(And then he just) xfgh pdl jklw']
]
