# ----------------------------------------------------------------------
# Wordless: Tagsets - Universal POS tags - French
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

# Universal POS Tags: https://universaldependencies.org/fr/pos/
tagset_mapping = [
    ['ADJ', 'ADJ', 'Adjective', 'grand/grande/grands/grandes, vieux/vieille/vieilles'],
    ['ADP', 'ADP', 'Adposition', 'pour, de, à, dans'],
    ['ADV', 'ADV', 'Adverb', 'très (joli), (fondues) ensemble'],
    ['AUX', 'AUX', 'Auxiliary', 'être, avoir, faire'],
    ['CONJ', 'CONJ', 'Coordinating/subordinating conjunction', 'See CCONJ and SCONJ'],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', 'mais, ou, et, or, ni, car'],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', 'quand\nMultiword subordinating conjunction: (parce) que, (afin) que, (avant) que)'],
    ['DET', 'DET', 'Determiner', 'Articles (a closed class indicating definiteness, specificity or givenness): le, la, les\nPossessive determiners: mon, ton, son, ma, ta, sa, mes, tes, ses, notre, votre, leur, nos, vos, leurs\nDemonstrative determiners: (J’ai vu) ce (vélo hier.), cet, cette\nInterrogative determiners: quel, Quelle (couleur aimez-vous?)\nRelative determiners: quel, (Je me demande) quelle (couleur vous aimez.)\nQuantity/quantifier determiners: aucun'],
    ['INTJ', 'INTJ', 'Interjection', 'bref, bon, enfin'],
    ['NOUN', 'NOUN', 'Noun', 'fille, chat, arbre, air, beauté'],
    ['PROPN', 'PROPN', 'Proper noun', 'Pierre, ONU, Mexique'],
    ['NUM', 'NUM', 'Numeral', 'quatre, 4, IV'],
    ['PART', 'PART', 'Particle', 'Negation particle: ne'],
    ['PRON', 'PRON', 'Pronoun', 'Personal pronouns: je, tu, il\nDemonstrative pronouns: ceux\nReflexive pronouns: me, se\nInterrogative/relative pronouns: qui, que'],
    ['VERB', 'VERB', 'Verb', '(je) vois, (à) lire, (en) marchant'],

    ['PUNCT', 'PUNCT', 'Punctuation', 'Period: .\nComma: ,\nParentheses: ()'],
    ['SYM', 'SYM', 'Symbol', '$, %, §, ©\n+, −, ×, ÷, =, <, >\n:), ♥‿♥, 😝\njohn.doe@universal.org, http://universaldependencies.org/, 1-800-COMPANY'],
    ['X', 'X', 'Other', 'etc']
]
