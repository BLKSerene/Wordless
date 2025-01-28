# ----------------------------------------------------------------------
# Wordless: Tagsets - Universal POS tags - Portuguese
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

# Universal POS Tags: https://universaldependencies.org/pt/pos/
tagset_mapping = [
    ['ADJ', 'ADJ', 'Adjective', 'grande, velho, verde, incompreensível, primeiro, segundo, terceiro'],
    ['ADP', 'ADP', 'Adposition', 'em, de, para, a, durante'],
    ['ADV', 'ADV', 'Adverb', 'muito, bem, exatamente, amanhã, acima, abaixo\nInterrogative or exclamative adverbs: onde, quando, como, por que\nDemonstrative adverbs: aqui, ali, agora, depois\nTotality adverbs: sempre\nNegative adverbs: nunca, sem'],
    ['AUX', 'AUX', 'Auxiliary', 'Tense auxiliary: ir (futuro perifrástico)\nModal auxiliary (+ infinitive): poder, dever, continuar\nPassive auxiliary: ser, ter, ir'],
    ['CONJ', 'CONJ', 'Coordinating/subordinating conjunction', 'See CCONJ and SCONJ'],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', 'e, ou, mas'],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', '(que as in Ele disse) que (ele viria.), se, porque'],
    ['DET', 'DET', 'Determiner', 'Articles (a closed class indicating definiteness, specificity or givenness): o, a, os, as\nPossessive determiners: meu, teu, seu, minha, meus, dele, nosso\nDemonstrative determiners: este, isto, esta, aquele\nInterrogative determiners: qual\nRelative determiners: que\nQuantity/quantifier determiners: nenhum, todos'],
    ['INTJ', 'INTJ', 'Interjection', 'bingo, claro, pronto, é'],
    ['NOUN', 'NOUN', 'Noun', 'menina, gato, árvore, ar, beleza'],
    ['PROPN', 'PROPN', 'Proper noun', 'Maria, João\nLondres, Goiânia\nONG, EUA'],
    ['NUM', 'NUM', 'Numeral', '0, 1, 2, 3, 4, 5, 2014, 1000000, 3.14159265359\num, dois, três, trinta e sete\nI, II, III, IV, V, MMXIV'],
    ['PART', 'PART', 'Particle', 'Negative particles: não, nem\nPrefixes: anti-, ex-, pós-, vice-, primeiro-, pró-, infra-'],
    ['PRON', 'PRON', 'Pronoun', 'Clitic pronouns (including reflexive pronouns): se, me, te, lhe\nDemonstrative pronouns: isto, esse, aquilo\nPersonal pronouns: eu, tu, ele, vocês\nIndefinite pronouns: um, outro, qualquer\nPossessive pronouns: meu, seu, dele\nInterrogative pronouns: que, quanto, qual\nRelative pronouns: que, cujo, qual\nTotality pronouns: todo, todas\nNegative pronouns: nenhum, ninguém'],
    ['VERB', 'VERB', 'Verb', 'correr, comer\ncorreu, comia\ncorrendo, comendo'],

    ['PUNCT', 'PUNCT', 'Punctuation', 'Period: .\nComma: ,\nParentheses: ()\nQuotes: «, », “'],
    ['SYM', 'SYM', 'Symbol', '$, %, §, ©\n+, −, ×, ÷, =, <, >\n:), ♥‿♥, 😝\njohn.doe@universal.org, http://universaldependencies.org/, 1-800-COMPANY'],
    ['X', 'X', 'Other', '[English] (And then he just) xfgh pdl jklw']
]
