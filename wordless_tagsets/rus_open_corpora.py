#
# Wordless: Tagsets - OpenCorpora Tagset
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

#
# OpenCorpora Tagset: https://pymorphy2.readthedocs.io/en/latest/user/grammemes.html
#
# Universal POS Tags: http://universaldependencies.org/u/pos/all.html
#

mappings = [
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
