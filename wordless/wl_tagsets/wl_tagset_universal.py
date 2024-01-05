# ----------------------------------------------------------------------
# Wordless: Tagsets - Universal POS tags
# Copyright (C) 2018-2024  Ye Lei (叶磊)
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

# Universal POS Tags: http://universaldependencies.org/u/pos/all.html
MAPPINGS = [
    ['ADJ', 'ADJ', 'Adjectives', 'big, old, green, African, incomprehensible\nfirst, second, third'],
    ['ADP', 'ADP', 'Adposition', 'in, to, during'],
    ['ADV', 'ADV', 'Adverb', 'very, well, exactly, tomorrow, up, down\nwhere, when, how, why\nhere, there, now, then\nsomewhere, sometime, anywhere, anytime\neverywhere, always\nnowhere, never'],
    ['AUX', 'AUX', 'Auxiliary', 'has (done), is (doing), will (do)\nwas (done), got (done)\nshould (do), must (do)\nis (He is a teacher.)'],
    ['CONJ', 'CONJ', 'Conjunction', 'and, or, but\nthat (I believe that he will come), if, while'],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', 'and, or, but'],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', 'that (I believe that he will come), if, while'],
    ['DET', 'DET', 'Determiner', 'the, a, an\n[Czech] můj, tvůj, jeho, její, náš, váš, jejich; [English] my, your\nthis (I saw this car yesterday)\nwhich (Which car do you like?)\nwhich (I wonder which car you like.)\nany, all, no (We have no cars available.)'],
    ['INTJ', 'INTJ', 'Interjection', 'psst, ouch, bravo, hello'],
    ['NOUN', 'NOUN', 'Noun', 'girl, cat, tree, air, beauty'],
    ['PROPN', 'PROPN', 'Proper noun', 'Mary, John, London, NATO, HBO'],
    ['NUM', 'NUM', 'Numeral', '0, 1, 2, 3, 4, 5, 2014, 1000000, 3.14159265359\none, two, three, seventy-seven\nI, II, III, IV, V, MMXIV'],
    ['PART', 'PART', 'Particle', '[English] ‘s\n[English] not; [German] nicht\n[Japanese] か; [Turkish] mu\n[Czech] ať, kéž, nechť\n[Chinese] 了'],
    ['PRON', 'PRON', 'Pronoun', 'I, you, he, she it, we, they\nmyself, yourself, himself, herself, itself, ourselves, yourselves, theirselves\nwho, what (What do you think?)\nwho, what (I wonder what you think.)\nsomebody, something, anybody, anything\neverybody, everything\nnobody, nothing\nmine, yours, his, hers, its, ours, theirs'],
    ['VERB', 'VERB', 'Verb', 'run, eat\nruns, ate\nrunning, eating'],

    ['PUNCT', 'PUNCT', 'Punctuation', '. , ( )'],
    ['SYM', 'SYM', 'Symbol', '$, %, §, ©\n+, −, ×, ÷, =, <, >\n:), ♥‿♥, 😝\njohn.doe@universal.org, http://universaldependencies.org/, 1-800-COMPANY'],
    ['X', 'X', 'Other', 'xfgh, pdl, jklw']
]
