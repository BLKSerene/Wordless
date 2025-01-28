# ----------------------------------------------------------------------
# Wordless: Tagsets - Universal POS tags - Danish
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

# Reference: https://universaldependencies.org/da/pos/
tagset_mapping = [
    ['ADJ', 'ADJ', 'Adjective', 'gammel/gammelt/gamle, grøn/grønt/grønne, ufatlig/ufatligt/ufatlige'],
    ['ADP', 'ADP', 'Adposition', 'i, på, gennem'],
    ['ADV', 'ADV', 'Adverb', 'meget (vigtigt), væk, (jeg spiser) ikke (rejer), pludselig'],
    ['AUX', 'AUX', 'Auxiliary', 'Tense auxiliary: har (købt)\nModal auxiliary: kunne (tænke)\nPassive auxiliary: blev (fundet)\nCopula: var (grøn), er (en løsning)'],
    ['CONJ', 'CONJ', 'Coordinating/subordinating conjunction', 'See CCONJ and SCONJ'],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', 'og, eller, men'],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', 'da, hvis, (konstatere) at (manden har søgt hjælp)'],
    ['DET', 'DET', 'Determiner', 'Articles: en, et, den, det, de\nPossessive determiners: min (bil), deres (holdninger), dit (job)\nNegative determiners: (han har) ingen (empati)'],
    ['INTJ', 'INTJ', 'Interjection', 'Hmm!, Åh!, Hej!'],
    ['NOUN', 'NOUN', 'Noun', 'pige, kat, træ, luft, skønhed'],
    ['PROPN', 'PROPN', 'Proper noun', 'Anna, Otto\nSkåne, USA\nTexaco, Pirelli'],
    ['NUM', 'NUM', 'Numeral', '0, 1, 2, 3, 2014, 1 000 000, 3.000,15, 3,14159265359\net, to, tre, nitten\nI, II, III, IV, V, MMXIV'],
    ['PART', 'PART', 'Particle', '(det er muligt) at (ændre det)'],
    ['PRON', 'PRON', 'Pronoun', 'Personal (subject) pronouns: jeg, du, han, hun, det/den, vi, I, de\nPlaceholder personal pronoun: man (kan gå)\nPersonal (object)/reflexive pronouns: mig, dig, ham, henne, sig, os, hinanden\nDemonstrative pronouns: dette (er et svært spørgsmål)\nPossessive pronouns: vores\nInterrogative pronouns: hvad\nRelative pronouns: hvis\nIndefinite pronouns: nogen, noget\nTotality pronouns: alting\nNegative pronouns: ingen (af os)'],
    ['VERB', 'VERB', 'Verb', 'at vise, jeg viser, han viste\nat flyve, vi flyver, de fløj'],

    ['PUNCT', 'PUNCT', 'Punctuation', 'Period: .\nComma: ,\nParentheses: ()'],
    ['SYM', 'SYM', 'Symbol', '§'],
    ['X', 'X', 'Other', 'musik(- og billedprogrammer)']
]
