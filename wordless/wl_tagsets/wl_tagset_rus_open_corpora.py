# ----------------------------------------------------------------------
# Wordless: Tagsets - OpenCorpora
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

# Reference: https://pymorphy2.readthedocs.io/en/latest/user/grammemes.html
tagset_mapping = [
    ['NOUN', 'NOUN', 'Noun', 'хомяк'],
    ['ADJF', 'ADJ', 'Adjective (full)', 'хороший'],
    ['ADJS', 'ADJ', 'Adjective (short)', 'хорош'],
    ['COMP', 'ADJ', 'Comparative', 'лучше, получше, выше'],
    ['VERB', 'VERB', 'Verb (personal form)', 'говорю, говорит, говорил'],
    ['INFN', 'VERB', 'Verb (infinitive)', 'говорить, сказать'],
    ['PRTF', 'VERB', 'Participle (full)', 'прочитавший, прочитанная'],
    ['PRTS', 'VERB', 'Participle (short)', 'прочитана'],
    ['GRND', 'VERB', 'Verbal adverb', 'прочитав, рассказывая'],
    ['NUMR', 'NUM', 'Numeral', 'три, пятьдесят'],
    ['ADVB', 'ADV', 'Adverb', 'круто'],
    ['NPRO', 'PRON', 'Pronoun-noun', 'он'],
    ['PRED', 'PART', 'Predicative', 'некогда'],
    ['PREP', 'ADP', 'Preposition', 'в'],
    ['CONJ', 'CONJ', 'Conjunction', 'и'],
    ['PRCL', 'PART', 'Particle', 'бы, же, лишь'],
    ['INTJ', 'INTJ', 'Interjection', 'ой'],

    ['LATN', 'X', 'Токен состоит из латинских букв', 'foo-bar, Maßstab'],
    ['NUMB', 'NUM', 'Число', '204, 3.14'],
    ['ROMN', 'X', 'Римское число', 'XI'],

    ['PNCT', 'PUNCT', 'Пунктуация', ', ! ? …'],
    ['UNKN', 'SYM/X', 'Токен не удалось разобрать', '']
]
