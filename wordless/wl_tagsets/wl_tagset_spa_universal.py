# ----------------------------------------------------------------------
# Wordless: Tagsets - Universal POS tags - Spanish
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

# Universal POS Tags: https://universaldependencies.org/es/pos/
tagset_mapping = [
    ['ADJ', 'ADJ', 'Adjective', 'grande, viejo, verde, incomprensible, primero, segundo, tercero'],
    ['ADP', 'ADP', 'Adposition', 'a, ante, bajo, cabe, con, contra, de, desde, en, entre, hacia, hasta, para, por, según, sin, sobre, tras'],
    ['ADV', 'ADV', 'Adverb', 'muy, bien, exactamente, mañana, arriba, abajo\nInterrogative adverbs: dónde, cuándo\nRelative adverbs (depending on context, these can be also subordinating conjunctions): donde, cuando\nDemonstrative adverbs: aquí, allí, ahora, después\nTotality adverbs: siempre\nNegative adverbs: nunca'],
    ['AUX', 'AUX', 'Auxiliary', 'Copulas: ser, estar\npassive: ser (la sentencia fue publicada)\nProgressive: estar (mis hijos están estudiando inglés)\nPerfect tenses: haber (ha venido hoy)'],
    ['CONJ', 'CONJ', 'Coordinating/subordinating conjunction', 'See CCONJ and SCONJ'],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', '(María) y (Juan están estudiando.), (Quiero ir al cine,) pero (no tengo tiempo.), (Puedes estudiar inglés) o (francés.)\n(padre) e (hijo), (siete) u (ocho)'],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', 'Complementizers: como, que, mientras, si\nAdverbial clause introducers when introducing a clause, not a nominal: como, cuando, ya que / porque'],
    ['DET', 'DET', 'Determiner', 'Articles: definite - el, la, los, las; indefinite - un, una, unos, unas\nDemonstratives: este, esta, estos, estas, ese, esa, esos, esas, aquel, aquella, aquellos, aquellas\nPossessives: mi, mis, tu, tus, su, sus, nuestro, nuestra, nuestros, nuestras, vuestro, vuestra, vuestros, vuestras\nQuantifiers: todo, toda, todos, todas, mucho, mucha, muchos, muchas, poco, poca, pocos, pocas, algún, alguna, algunos, algunas, ningún, ninguna, bastantes, varios, varias\nStressed possessives: mío, mía, míos, mías, tuyo, tuya, tuyos, tuyas, suyo, suya, suyos, suyas, nuestro, nuestra, nuestros, nuestras, vuestro, vuestra, vuestros, vuestras'],
    ['INTJ', 'INTJ', 'Interjection', 'psst, ay, bravo, hola, Sí(, porque…), No(, no lo creo)'],
    ['NOUN', 'NOUN', 'Noun', 'chica, gato, árbol, aire, belleza'],
    ['PROPN', 'PROPN', 'Proper noun', 'Madrid, Antonio, Los Ángeles'],
    ['NUM', 'NUM', 'Numeral', 'Definite cardinal numerals: uno, dos, tres\nFractions: media, tercio'],
    ['PART', 'PART', 'Particle', 'Possessive marker: [English] ’s\nNegation particle: [English] not; [German] nicht\nQuestion particle: [Japanese] か/ka (adding this particle to the end of a clause turns the clause into a question); [Turkish] mu\nSentence modality: [Czech] ať, kéž, nechť'],
    ['PRON', 'PRON', 'Pronoun', 'Personal: yo, tú, él\nReflexive: me, te, se\nDemonstrative: este, ese, aquel\nRelative: que, quien, cual\nInterrogative/exclamatory: quién, qué, cuál\nIndefinite: alguien, algo, ninguno\nPossessive: mío, tuyo, suyo'],
    ['VERB', 'VERB', 'Verb', '[English] run, eat\n[English] runs, ate\n[English] running, eating'],

    ['PUNCT', 'PUNCT', 'Punctuation', 'Period: .\nComma: ,\nParentheses: ()'],
    ['SYM', 'SYM', 'Symbol', '$, +'],
    ['X', 'X', 'Other', '[English] (And then he just) xfgh pdl jklw']
]
