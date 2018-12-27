#
# Wordless: Mapping Table (Russian National Corpus Tagset -> Universal POS Tags)
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
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
    ['CONJ', 'CCONJ/SCONJ', 'Conjunction', 'и'],
    ['PRCL', 'PART', 'Particle', 'бы, же, лишь'],
    ['INTJ', 'INTJ', 'Interjection', 'ой']    
]
