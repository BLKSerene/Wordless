#
# Wordless: Tagsets - jieba Tagset
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

#
# jieba Tagset: https://gist.github.com/hscspring/c985355e0814f01437eaf8fd55fd7998
#
# Universal POS Tags: http://universaldependencies.org/u/pos/all.html
#

mappings = [
    ['a', 'ADJ', '形容词', ''],
    ['ad', 'ADJ', '副形词', ''],
    ['ag', 'ADJ', '形容词性语素', ''],
    ['an', 'ADJ', '名形词', ''],

    ['b', 'PART', '区别词', ''],

    ['c', 'CONJ', '连词', ''],

    ['d', 'ADV', '副词', ''],
    ['df', 'ADV', '', ''],
    ['dg', 'ADV', '副语素', ''],

    ['e', 'INTJ', '叹词', ''],
    ['eng', 'X', '英语单词', ''],

    ['f', 'ADP', '方位词', ''],

    ['g', 'X', '语素', ''],

    ['h', 'PART', '前接成分', ''],

    ['i', 'X', '成语', ''],

    ['j', 'X', '简称、略语', ''],

    ['k', 'PART', '后接成分', ''],

    ['l', 'X', '习用语', ''],

    ['m', 'NUM', '数词', ''],
    ['mg', 'NUM', '甲乙丙丁之类的数词', '甲, 乙, 丙, 丁'],
    ['mq', 'NUM', '数量词', ''],

    ['n', 'NOUN', '名词', ''],
    ['ng', 'NOUN', '名词性语素', ''],
    ['nr', 'PRONP', '人名', ''],
    ['nrfg', 'PRONP', '', ''],
    ['nrt', 'PRONP', '', ''],
    ['ns', 'PROPN', '地名', ''],
    ['nt', 'PROPN', '机构团体名', ''],
    ['nz', 'PROPN', '其他专名', ''],

    ['o', 'X', '拟声词', ''],

    ['p', 'ADP', '介词', ''],

    ['q', 'NUM', '量词', ''],

    ['r', 'PRON', '代词', ''],
    ['rg', 'PRON', '代词性语素', ''],
    ['rr', 'PRON', '人称代词', ''],
    ['rz', 'PRON', '指示代词', ''],

    ['s', 'PART', '处所词', ''],

    ['t', 'NOUN', '时间词', ''],
    ['tg', 'NOUN', '时语素', ''],

    ['u', 'PART', '助词', ''],
    ['ud', 'PART', '结构助词', '得'],
    ['ug', 'PART', '时态助词', ''],
    ['uj', 'PART', '结构助词', '的'],
    ['ul', 'PART', '时态助词', '了'],
    ['uv', 'PART', '结构助词', '地'],
    ['uz', 'PART', '时态助词', '着'],

    ['v', 'VERB', '动词', ''],
    ['vd', 'VERB', '副动词', ''],
    ['vg', 'VERB', '动词性语素', ''],
    ['vi', 'VERB', '不及物动词', ''],
    ['vn', 'VERB', '名动词', ''],
    ['vq', 'VERB', '', ''],

    ['x', 'PUNCT/SYM', '非语素词', ''],

    ['y', 'INTJ', '语气词', ''],

    ['z', 'PART', '状态词', ''],
    ['zg', 'PART', '状态词', ''],
]
