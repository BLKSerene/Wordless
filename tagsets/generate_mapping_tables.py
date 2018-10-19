#
# Wordless: Generators of Mapping Tables (Different Tagsets -> Universal Part-of-speech Tagset)
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

#
# Universal Part-of-speech Tagset: https://github.com/slavpetrov/universal-pos-tags/blob/master/README
#
# VERB - verbs (all tenses and modes)
# NOUN - nouns (common and proper)
# PRON - pronouns 
# ADJ - adjectives
# ADV - adverbs
# ADP - adpositions (prepositions and postpositions)
# CONJ - conjunctions
# DET - determiners
# NUM - cardinal numbers
# PRT - particles or other function words
# X - other: foreign words, typos, abbreviations
# . - punctuation
#

import nltk

POS = {
    'A': 'ADJ',
    'A-PRO': 'PRON',
    'ADV': 'ADV',
    'ADV-PRO': 'PRON',
    'ANUM': 'ADJ',
    'CONJ': 'CONJ',
    'INTJ': 'X',
    'NONLEX': '.',
    'NUM': 'NUM',
    'PARENTH': 'PRT',
    'PART': 'PRT',
    'PR': 'ADP',
    'PRAEDIC': 'PRT',
    'PRAEDIC-PRO': 'PRON',
    'S': 'NOUN',
    'S-PRO': 'PRON',
    'V': 'VERB',
}

GRAM_CATEGORIES = [
    'm',
    'f',
    'm-f',
    'n',

    'anim',
    'inan',

    'sg',
    'pl',

    'nom',
    'gen',
    'dat',
    'acc',
    'ins',
    'ioc',
    'gen2',
    'acc2',
    'loc2',
    'voc',
    'adnum',

    'brev',
    'plen',

    'comp',
    'comp2',
    'supr',

    'pf',
    'ipf',

    'intr',
    'tran',

    'act',
    'pass',
    'med',

    'inf',
    'partcp',
    'ger',

    'indic',
    'imper',
    'imper2',

    'praet',
    'praes',
    'fut',

    '1p',
    '2p',
    '3p',

    'persn',
    'patrn',
    'famn',
    '0',

    'anom',
    'distort',
    'ciph',
    'INIT',
    'abbr',
]

def generate_tagset_russian_national_corpus():
    with open('rus_russian_national_corpus.txt', 'w', encoding = 'utf_8') as f:
        f.write(
'''#
# Wordless: Mapping Table (Russian National Corpus Tagset -> Universal Part-of-speech Tagset)
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

#
# Russian National Corpus Tagset: http://www.ruscorpora.ru/en/corpora-morph.html
#
# Universal Part-of-speech Tagset: https://github.com/slavpetrov/universal-pos-tags/blob/master/README
#

''')

        for tag_pos, tag_universal in POS.items():
            f.write(f'{tag_pos}\t{tag_universal}\n')

            for tag_gramm_category in GRAM_CATEGORIES:
                f.write(f'{tag_pos}={tag_gramm_category}\t{tag_universal}\n')

if __name__ == '__main__':
    generate_tagset_russian_national_corpus()
