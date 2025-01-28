# ----------------------------------------------------------------------
# Wordless: Tagsets - Russian National Corpus
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
#     [Dead] http://www.ruscorpora.ru/en/corpora-morph.html
#     https://github.com/nltk/nltk/pull/2152
tagset_mapping = [
    ['A', 'ADJ', 'Adjective', ''],

    ['A=m', 'ADJ', 'Adjective (masculine)', ''],
    ['A=f', 'ADJ', 'Adjective (feminine)', ''],
    ['A=n', 'ADJ', 'Adjective (neuter)', ''],

    ['A=sg', 'ADJ', 'Adjective (singular)', ''],
    ['A=pl', 'ADJ', 'Adjective (plural)', ''],

    ['A=gen', 'ADJ', 'Adjective (genitive)', ''],
    ['A=ins', 'ADJ', 'Adjective (instrumental)', ''],

    ['A=brev', 'ADJ', 'Adjective (short form)', ''],
    ['A=plen', 'ADJ', 'Adjective (full form)', ''],

    ['A=comp', 'ADJ', 'Adjective (comparative)', ''],
    ['A=comp=anom', 'ADJ', 'Adjective (comparative, anomalous form)', ''],
    ['A=comp2', 'ADJ', 'Adjective (prefix по + comparative)', ''],

    ['ADV', 'ADV', 'Adverb', ''],

    ['ADV=comp', 'ADV', 'Adverb (comparative)', ''],
    ['ADV=comp=anom', 'ADV', 'Adverb (comparative, anomalous form)', ''],
    ['ADV=comp2', 'ADV', 'Adverb (prefix по + comparative)', ''],

    ['ADV=anom', 'ADV', 'Adverb (anomalous form)', ''],
    ['ADV=distort', 'ADV', 'Adverb (distorted form)', ''],
    ['ADV=abbr', 'ADV', 'Adverb (abbreviation)', ''],

    ['CONJ', 'CONJ', 'Conjunction', ''],
    ['CONJ=distort', 'CONJ', 'Conjunction (distorted form)', ''],

    ['INTJ', 'INTJ', 'Interjection', ''],
    ['INTJ=distort', 'INTJ', 'Interjection (distorted form)', ''],

    ['INIT=abbr', 'PROPN', 'Initials (abbreviation)', ''],

    ['S', 'NOUN', 'Noun', ''],

    ['S=m', 'NOUN', 'Noun (masculine)', ''],
    ['S=f', 'NOUN', 'Noun (feminine)', ''],
    ['S=n', 'NOUN', 'Noun (neuter)', ''],

    ['S=pl', 'NOUN', 'Noun (plural)', ''],

    ['S=persn', 'PROPN', 'Noun (first name)', ''],
    ['S=famn', 'PROPN', 'Noun (family name)', ''],

    ['NUM', 'NUM', 'Numeral', ''],

    ['NUM=m', 'NUM', 'Numeral (masculine)', ''],
    ['NUM=f', 'NUM', 'Numeral (feminine)', ''],
    ['NUM=n', 'NUM', 'Numeral (neuter)', ''],

    ['NUM=nom', 'NUM', 'Numeral (nominative)', ''],
    ['NUM=nom=distort', 'NUM', 'Numeral (nominative, distorted form)', ''],
    ['NUM=gen', 'NUM', 'Numeral (genitive)', ''],
    ['NUM=gen=distort', 'NUM', 'Numeral (genitive, distorted form)', ''],
    ['NUM=gen=ciph', 'NUM', 'Numeral (genitive, numeral recording)', ''],
    ['NUM=dat', 'NUM', 'Numeral (dative)', ''],
    ['NUM=dat=ciph', 'NUM', 'Numeral (dative, numeral recording)', ''],
    ['NUM=dat2', 'NUM', 'Numeral (second dative)', ''],
    ['NUM=acc', 'NUM', 'Numeral (accusative)', ''],
    ['NUM=acc=anom', 'NUM', 'Numeral (accusative, anomalous form)', ''],
    ['NUM=acc=distort', 'NUM', 'Numeral (accusative, distorted form)', ''],
    ['NUM=acc=ciph', 'NUM', 'Numeral (accusative, numeral recording)', ''],
    ['NUM=ins', 'NUM', 'Numeral (instrumental)', ''],
    ['NUM=ins=ciph', 'NUM', 'Numeral (instrumental, numeral recording)', ''],
    ['NUM=loc', 'NUM', 'Numeral (locative)', ''],
    ['NUM=loc=ciph', 'NUM', 'Numeral (locative, numeral recording)', ''],

    ['NUM=comp', 'NUM', 'Numeral (comparative)', ''],
    ['NUM=comp2', 'NUM', 'Numeral (prefix по + comparative)', ''],
    ['NUM=distort', 'NUM', 'Numeral (distorted form)', ''],
    ['NUM=ciph', 'NUM', 'Numeral (numeral recording)', ''],

    ['ANUM', 'ADJ', 'Numeral adjective', ''],

    ['ANUM=m', 'ADJ', 'Numeral adjective (masculine)', ''],
    ['ANUM=f', 'ADJ', 'Numeral adjective (feminine)', ''],
    ['A-NUM=f', 'ADJ', 'Numeral adjective (feminine)', ''],
    ['ANUM=n', 'ADJ', 'Numeral adjective (neuter)', ''],

    ['ANUM=sg', 'ADJ', 'Numeral adjective (singular)', ''],
    ['ANUM=pl', 'ADJ', 'Numeral adjective (plural)', ''],

    ['ANUM=nom', 'ADJ', 'Numeral adjective (nominative)', ''],
    ['ANUM=gen', 'ADJ', 'Numeral adjective (genitive)', ''],

    ['ANUM=ciph', 'ADJ', 'Numeral adjective (numeral recording)', ''],

    ['PRAEDIC', 'PART', 'Predicative', ''],
    ['PRAEDIC=comp', 'PART', 'Predicative (comparative)', ''],
    ['PRAEDIC=comp=anom', 'PART', 'Predicative (comparative, Anolamous form)', ''],
    ['PRAEDIC=comp2', 'PART', 'Predicative (prefix по + comparative)', ''],
    ['PRAEDIC=distort', 'PART', 'Predicative (distorted form)', ''],

    ['PARENTH', 'PART', 'Parenthesis', ''],
    ['PARENTH=distort', 'PART', 'Parenthesis (distorted form)', ''],
    ['PARENTH=abbr', 'PART', 'Parenthesis (abbreviation)', ''],

    ['PART', 'PART', 'Particle', ''],
    ['PART=anom', 'PART', 'Particle (anomolous form)', ''],
    ['PART=distort', 'PART', 'Particle (distorted form)', ''],

    ['PR', 'ADP', 'Preposition', ''],
    ['PR=anom', 'ADP', 'Preposition (anomalous form)', ''],
    ['PR=distort', 'ADP', 'Preposition (distorted form)', ''],
    ['PR=abbr', 'ADP', 'Preposition (abbreviation)', ''],

    ['A-PRO', 'PRON', 'Pronoun', ''],

    ['A-PRO=m', 'PRON', 'Pronoun (masculine)', ''],
    ['A-PRO=f', 'PRON', 'Pronoun (feminine)', ''],
    ['A-PRO=n', 'PRON', 'Pronoun (neuter)', ''],

    ['A-PRO=sg', 'PRON', 'Pronoun (singular)', ''],
    ['A-PRO=pl', 'PRON', 'Pronoun (plural)', ''],

    ['A-PRO=dat', 'PRON', 'Pronoun (dative)', ''],

    ['S-PRO', 'PRON', 'Pronoun', ''],

    ['S-PRO=m', 'PRON', 'Pronoun (masculine)', ''],
    ['S-PRO=f', 'PRON', 'Pronoun (feminine)', ''],
    ['S-PRO=n', 'PRON', 'Pronoun (neuter)', ''],
    ['S-PRO=n=sg', 'PRON', 'Pronoun (neuter, singular)', ''],

    ['S-PRO=pl', 'PRON', 'Pronoun (plural)', ''],

    ['S-PRO=gen', 'PRON', 'Pronoun (genitive)', ''],
    ['S-PRO=dat', 'PRON', 'Pronoun (dative)', ''],
    ['S-PRO=acc', 'PRON', 'Pronoun (accusative)', ''],
    ['S-PRO=ins', 'PRON', 'Pronoun (instrumental)', ''],
    ['S-PRO=loc', 'PRON', 'Pronoun (locative)', ''],

    ['ADV-PRO', 'PRON', 'Adverbial pronoun', ''],

    ['ADV-PRO=comp', 'PRON', 'Adverbial pronoun (comparative)', ''],
    ['ADV-PRO=comp2', 'PRON', 'Adverbial pronoun (prefix по + comparative)', ''],
    ['ADV-PRO=anom', 'PRON', 'Adverbial pronoun (anomalous form)', ''],
    ['ADV-PRO=distort', 'PRON', 'Adverbial pronoun (distorted form)', ''],
    ['ADV-PRO=abbr', 'PRON', 'Adverbial pronoun (abbreviation)', ''],

    ['PRAEDIC-PRO', 'PRON', 'Predicative pronoun', ''],

    ['PRAEDIC-PRO=dat', 'PRON', 'Predicative pronoun (dative)', ''],
    ['PRAEDIC-PRO=ins', 'PRON', 'Predicative pronoun (instrumental)', ''],

    ['V', 'VERB', 'Verb', ''],

    ['NONLEX', 'PUNCT/SYM', 'Non-lexical', ''],
    ['NONLEX=abbr', 'PUNCT/SYM', 'Non-lexical (abbreviation)', '']
]
