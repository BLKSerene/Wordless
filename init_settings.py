#
# Wordless: Initialization of Settings
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import copy
import os
import pickle

import nltk

def init_settings(main):
    init_settings_global(main)
    init_settings_default(main)

    if os.path.exists('wordless_settings.pkl'):
        with open(r'wordless_settings.pkl', 'rb') as f:
            main.settings_custom = pickle.load(f)
    else:
        main.settings_custom = copy.deepcopy(main.settings_default)

def init_settings_global(main):
    main.settings_global = {
        'langs': {
            main.tr('Afrikaans'): 'afr',
            main.tr('Armenian'): 'hye',
            main.tr('Asturian'): 'ast',
            main.tr('Albanian'): 'sqi',
            main.tr('Arabic'): 'ara',
            main.tr('Azerbaijani'): 'aze',
            main.tr('Basque'): 'eus',
            main.tr('Belarusian'): 'bel',
            main.tr('Bengali'): 'ben',
            main.tr('Breton'): 'bre',
            main.tr('Bulgarian'): 'bul',
            main.tr('Catalan'): 'cat',
            main.tr('Chinese (Simplified)'): 'zho_CN',
            main.tr('Chinese (Traditional)'): 'zho_TW',
            main.tr('Croatian'): 'hrv',
            main.tr('Czech'): 'ces',
            main.tr('Danish'): 'dan',
            main.tr('Dutch'): 'nld',
            main.tr('English'): 'eng',
            main.tr('Esperanto'): 'epo',
            main.tr('Estonian'): 'est',
            main.tr('Finnish'): 'fin',
            main.tr('French'): 'fra',
            main.tr('Galician'): 'glg',
            main.tr('German'): 'deu',
            main.tr('Greek'): 'ell',
            main.tr('Gujarati'): 'guj',
            main.tr('Hausa'): 'hau',
            main.tr('Hebrew'): 'heb',
            main.tr('Hindi'): 'hin',
            main.tr('Hungarian'): 'hun',
            main.tr('Indonesian'): 'ind',
            main.tr('Irish'): 'gle',
            main.tr('Islandic'): 'isl',
            main.tr('Italian'): 'ita',
            main.tr('Japanese'): 'jpn',
            main.tr('Kannada'): 'kan',
            main.tr('Kazakh'): 'kaz',
            main.tr('Korean'): 'kor',
            main.tr('Kurdish'): 'kur',
            main.tr('Latin'): 'lat',
            main.tr('Latvian'): 'lav',
            main.tr('Lithuanian'): 'lit',
            main.tr('Macedonian'): 'mkd',
            main.tr('Malay'): 'msa',
            main.tr('Malayalam'): 'mal',
            main.tr('Maltese'): 'mlt',
            main.tr('Manx'): 'glv',
            main.tr('Marathi'): 'mar',
            main.tr('Nepali'): 'nep',
            main.tr('Norwegian'): 'nor',
            main.tr('Punjabi'): 'pan',
            main.tr('Persian'): 'fas',
            main.tr('Polish'): 'pol',
            main.tr('Portuguese'): 'por',
            main.tr('Romanian'): 'ron',
            main.tr('Russian'): 'rus',
            main.tr('Scottish Gaelic'): 'gla',
            main.tr('Serbian'): 'srp',
            main.tr('Slovak'): 'slk',
            main.tr('Slovene'): 'slv',
            main.tr('Sotho, Southern'): 'sot',
            main.tr('Somali'): 'som',
            main.tr('Spanish'): 'spa',
            main.tr('Swahili'): 'swa',
            main.tr('Swedish'): 'swe',
            main.tr('Tagalog'): 'tgl',
            main.tr('Tajik'): 'tgk',
            main.tr('Tamil'): 'tam',
            main.tr('Telugu'): 'tel',
            main.tr('Thai'): 'tha',
            main.tr('Turkish'): 'tur',
            main.tr('Ukrainian'): 'ukr',
            main.tr('Urdu'): 'urd',
            main.tr('Vietnamese'): 'vie',
            main.tr('Welsh'): 'cym',
            main.tr('Yoruba'): 'yor',
            main.tr('Zulu'): 'zul',

            main.tr('Other Languages'): 'other'
        },

        'lang_codes': {
            'afr': 'af',
            'hye': 'hy',
            'ast': 'ast',
            'sqi': 'sq',
            'ara': 'ar',
            'aze': 'az',
            'eus': 'eu',
            'bel': 'be',
            'ben': 'bn',
            'bre': 'br',
            'bul': 'bg',
            'cat': 'ca',
            'zho_CN': 'zh_CN',
            'zho_TW': 'zh_TW',
            'hrv': 'hr',
            'ces': 'cs',
            'dan': 'da',
            'nld': 'nl',
            'eng': 'en',
            'epo': 'eo',
            'est': 'et',
            'fin': 'fi',
            'fra': 'fr',
            'glg': 'gl',
            'deu': 'de',
            'ell': 'el',
            'guj': 'gu',
            'hau': 'ha',
            'heb': 'he',
            'hin': 'hi',
            'hun': 'hu',
            'ind': 'id',
            'gle': 'ga',
            'isl': 'is',
            'ita': 'it',
            'jpn': 'ja',
            'kan': 'kn',
            'kaz': 'kk',
            'kor': 'ko',
            'kur': 'ku',
            'lat': 'la',
            'lav': 'lv',
            'lit': 'lt',
            'mkd': 'mk',
            'msa': 'ms',
            'mal': 'ml',
            'mlt': 'mt',
            'glv': 'gv',
            'mar': 'mr',
            'nep': 'ne',
            'nor': 'no',
            'pan': 'pa',
            'fas': 'fa',
            'pol': 'pl',
            'por': 'pt',
            'ron': 'ro',
            'rus': 'ru',
            'gla': 'gd',
            'srp': 'sr',
            'slk': 'sk',
            'slv': 'sl',
            'sot': 'st',
            'som': 'so',
            'spa': 'es',
            'swa': 'sw',
            'swe': 'sv',
            'tgl': 'tl',
            'tgk': 'tg',
            'tam': 'ta',
            'tel': 'te',
            'tha': 'th',
            'tur': 'tr',
            'ukr': 'uk',
            'urd': 'ur',
            'vie': 'vi',
            'cym': 'cy',
            'yor': 'yo',
            'zul': 'zu',

            'other': 'other',
        },

        'file_exts': {
            '.txt': main.tr('Text File (*.txt)'),
            '.htm': main.tr('HTML Page (*.htm; *.html)'),
            '.html': main.tr('HTML Page (*.htm; *.html)')
        },

        'file_encodings': {
            main.tr('All Languages (UTF-8 Without BOM)'): 'utf_8',
            main.tr('All Languages (UTF-8 with BOM)'): 'utf_8_sig',
            main.tr('All Languages (UTF-16 with BOM)'): 'utf_16',
            main.tr('All Languages (UTF-16 Big Endian Without BOM)'): 'utf_16_be',
            main.tr('All Languages (UTF-16 Little Endian Without BOM)'): 'utf_16_le',
            main.tr('All Languages (UTF-32 with BOM)'): 'utf_32',
            main.tr('All Languages (UTF-32 Big Endian Without BOM)'): 'utf_32_be',
            main.tr('All Languages (UTF-32 Little Endian Without BOM)'): 'utf_32_le',
            main.tr('All Languages (UTF-7)'): 'utf_7',
            main.tr('All Languages (CP65001)'): 'cp65001',

            main.tr('Baltic Languages (CP775)'): 'cp775',
            main.tr('Baltic Languages (Windows-1257)'): 'cp1257',
            main.tr('Baltic Languages (ISO-8859-4)'): 'iso8859_4',
            main.tr('Baltic Languages (ISO-8859-13)'): 'iso8859_13',

            main.tr('Celtic Languages (ISO-8859-14)'): 'iso8859_14',

            main.tr('Nordic Languages (ISO-8859-10)'): 'iso8859_10',

            main.tr('Europe (HP Roman-8)'): 'hp_roman8',

            main.tr('Central Europe (Mac OS Central European)'): 'mac_centeuro',
            main.tr('Central Europe (Mac OS Latin 2)'): 'mac_latin2',

            main.tr('Central and Eastern Europe (CP852)'): 'cp852',
            main.tr('Central and Eastern Europe (Windows-1250)'): 'cp1250',
            main.tr('Central and Eastern Europe (ISO-8859-2)'): 'iso8859_2',
            main.tr('Central and Eastern Europe (Mac Latin)'): 'mac_latin2',

            main.tr('South-Eastern Europe (ISO-8859-16)'): 'iso8859_16',

            main.tr('Western Europe (EBCDIC 500)'): 'cp500',
            main.tr('Western Europe (CP850)'): 'cp850',
            main.tr('Western Europe (CP858)'): 'cp858',
            main.tr('Western Europe (CP1140)'): 'cp1140',
            main.tr('Western Europe (Windows-1252)'): 'windows_1252',
            main.tr('Western Europe (ISO-2022-JP-2)'): 'iso2022_jp_2',
            main.tr('Western Europe (ISO-8859-1)'): 'iso_8859_1',
            main.tr('Western Europe (ISO-8859-15)'): 'iso_8859_15',
            main.tr('Western Europe (Mac OS Roman)'): 'mac_roman',

            main.tr('Arabic (CP720)'): 'cp720',
            main.tr('Arabic (CP864)'): 'cp864',
            main.tr('Arabic (Windows-1256)'): 'cp1256',
            main.tr('Arabic (ISO-8859-6)'): 'iso_8859_6',
            main.tr('Arabic (Mac OS Arabic)'): 'mac_arabic',

            main.tr('Bulgarian (IBM855)'): 'cp855',
            main.tr('Bulgarian (Windows-1251)'): 'windows_1251',
            main.tr('Bulgarian (ISO-8859-5)'): 'iso_8859_5',
            main.tr('Bulgarian (Mac OS Cyrillic)'): 'mac_cyrillic',

            main.tr('Belarusian (IBM855)'): 'cp855',
            main.tr('Belarusian (Windows-1251)'): 'cp1251',
            main.tr('Belarusian (ISO-8859-5)'): 'iso_8859_5',
            main.tr('Belarusian (Mac OS Cyrillic)'): 'mac_cyrillic',

            main.tr('Canadian French (CP863)'): 'cp863',

            main.tr('Simplified Chinese (GB2312)'): 'gb2312',
            main.tr('Simplified Chinese (HZ)'): 'hz_gb_2312',
            main.tr('Simplified Chinese (ISO-2022-JP-2)'): 'iso2022_jp_2',

            main.tr('Traditional Chinese (Big-5)'): 'big5',
            main.tr('Traditional Chinese (Big5-HKSCS)'): 'big5hkscs',
            main.tr('Traditional Chinese (CP950)'): 'cp950',

            main.tr('Unified Chinese (GBK)'): 'gbk',
            main.tr('Unified Chinese (GB18030)'): 'gb18030',

            main.tr('Croatian (Mac OS Croatian)'): 'mac_croatian',

            main.tr('Danish (CP865)'): 'cp865',

            main.tr('English (ASCII)'): 'ascii',
            main.tr('English (EBCDIC 037)'): 'cp037',
            main.tr('English (CP437)'): 'cp437',

            main.tr('Esperanto (ISO-8859-3)'): 'iso_8859_3',

            main.tr('German (EBCDIC 273)'): 'cp273',

            main.tr('Greek (CP737)'): 'cp737',
            main.tr('Greek (CP869)'): 'cp869',
            main.tr('Greek (CP875)'): 'cp875',
            main.tr('Greek (Windows-1253)'): 'windows_1253',
            main.tr('Greek (ISO-2022-JP-2)'): 'iso2022_jp_2',
            main.tr('Greek (ISO-8859-7)'): 'iso_8859_7',
            main.tr('Greek (Mac OS Greek)'): 'mac_greek',

            main.tr('Hebrew (EBCDIC 424)'): 'cp424',
            main.tr('Hebrew (CP856)'): 'cp856',
            main.tr('Hebrew (CP862)'): 'cp862',
            main.tr('Hebrew (Windows-1255)'): 'windows_1255',
            main.tr('Hebrew (ISO-8859-8)'): 'iso_8859_8',

            main.tr('Icelandic (CP861)'): 'cp861',
            main.tr('Icelandic (Mac OS Icelandic)'): 'mac_iceland',

            main.tr('Japanese (CP932)'): 'cp932',
            main.tr('Japanese (EUC-JP)'): 'euc_jp',
            main.tr('Japanese (EUC-JIS-2004)'): 'euc_jis_2004',
            main.tr('Japanese (EUC-JISx0213)'): 'euc_jisx0213',
            main.tr('Japanese (ISO-2022-JP)'): 'iso_2022_jp',
            main.tr('Japanese (ISO-2022-JP-1)'): 'iso2022_jp_1',
            main.tr('Japanese (ISO-2022-JP-2)'): 'iso2022_jp_2',
            main.tr('Japanese (ISO-2022-JP-2)'): 'iso2022_jp_2004',
            main.tr('Japanese (ISO-2022-JP-3)'): 'iso2022_jp_3',
            main.tr('Japanese (ISO-2022-JP-EXT)'): 'iso2022_jp_ext',
            main.tr('Japanese (Shift_JIS)'): 'shift_jis',
            main.tr('Japanese (Shift_JIS-2004)'): 'shift_jis_2004',
            main.tr('Japanese (Shift_JISx0213)'): 'shift_jisx0213',

            main.tr('Kazakh (KZ-1048)'): 'kz1048',
            main.tr('Kazakh (PTCP154)'): 'ptcp154',

            main.tr('Korean (Windows-949)'): 'cp949',
            main.tr('Korean (EUC-KR)'): 'euc_kr',
            main.tr('Korean (ISO-2022-JP-2)'): 'iso2022_jp_2',
            main.tr('Korean (ISO-2022-KR)'): 'iso_2022_kr',
            main.tr('Korean (JOHAB)'): 'johab',

            main.tr('Macedonian (IBM855)'): 'cp855',
            main.tr('Macedonian (Windows-1251)'): 'cp1251',
            main.tr('Macedonian (ISO-8859-5)'): 'iso_8859_5',
            main.tr('Macedonian (Mac OS Cyrillic)'): 'maccyrillic',

            main.tr('Maltese (ISO-8859-3)'): 'iso_8859_3',

            main.tr('Norwegian (CP865)'): 'cp865',

            main.tr('Persian (Mac OS Farsi)'): 'mac_farsi',

            main.tr('Portuguese (CP860)'): 'cp860',

            main.tr('Romanian (Mac OS Romanian)'): 'mac_romanian',

            main.tr('Russian (IBM855)'): 'ibm855',
            main.tr('Russian (IBM866)'): 'ibm866',
            main.tr('Russian (Windows-1251)'): 'windows_1251',
            main.tr('Russian (ISO-8859-5)'): 'iso_8859_5',
            main.tr('Russian (KOI8-R)'): 'koi8_r',
            main.tr('Russian (Mac OS Cyrillic)'): 'maccyrillic',

            main.tr('Serbian (IBM855)'): 'cp855',
            main.tr('Serbian (Windows-1251)'): 'cp1251',
            main.tr('Serbian (ISO-8859-5)'): 'iso8859_5',
            main.tr('Serbian (Mac OS Cyrillic)'): 'maccyrillic',

            main.tr('Tajik (KOI8-T)'): 'koi8_t',

            main.tr('Thai (CP874)'): 'cp874',
            main.tr('Thai (ISO-8859-11)'): 'iso8859_11',
            main.tr('Thai (TIS-620)'): 'tis_620',

            main.tr('Turkish (CP857)'): 'cp857',
            main.tr('Turkish (EBCDIC 1026)'): 'cp1026',
            main.tr('Turkish (Windows-1254)'): 'cp1254',
            main.tr('Turkish (ISO-8859-9)'): 'iso_8859_9',
            main.tr('Turkish (Mac OS Turkish)'): 'mac_turkish',

            main.tr('Ukrainian (CP1125)'): 'cp1125',
            main.tr('Ukrainian (KOI8-U)'): 'koi8_u',

            main.tr('Urdu (CP1006)'): 'cp1006',
            main.tr('Urdu (Mac OS Farsi)'): 'mac_farsi',

            main.tr('Vietnamese (CP1258)'): 'cp1258'
        },

        'sentence_tokenizers': {
            'eng': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],

            'zho_CN': [
                main.tr('Wordless - Chinese Sentence Tokenizer'),
                main.tr('HanLP - Standard Tokenizer'),
                main.tr('HanLP - Basic Tokenizer'),
                main.tr('HanLP - NLP Tokenizer'),
                main.tr('HanLP - Speed Tokenizer'),
            ],
            'zho_TW': [
                main.tr('Wordless - Chinese Sentence Tokenizer'),
                main.tr('HanLP - Standard Tokenizer'),
                main.tr('HanLP - Basic Tokenizer'),
                main.tr('HanLP - NLP Tokenizer'),
                main.tr('HanLP - Speed Tokenizer'),
                main.tr('HanLP - Traditional Chinese Tokenizer'),
            ],
            'ces': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],
            'dan': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],
            'nld': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],
            'est': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],
            'fin': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],
            'fra': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],
            'deu': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],
            'ell': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],
            'ita': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],
            'nor': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],
            'pol': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],
            'por': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],
            'slv': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],
            'spa': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],
            'swe': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],
            'tur': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],

            'other': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ]
        },

        'word_tokenizers': {
            'eng': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],

            'zho_CN': [
                main.tr('jieba - With HMM'),
                main.tr('jieba - Without HMM'),
                main.tr('HanLP - Standard Tokenizer'),
                main.tr('HanLP - Basic Tokenizer'),
                main.tr('HanLP - NLP Tokenizer'),
                main.tr('HanLP - Speed Tokenizer'),
                main.tr('HanLP - URL Tokenizer'),
                main.tr('HanLP - CRF Lexical Analyzer'),
                main.tr('HanLP - Perceptron Lexical Analyzer'),
                main.tr('HanLP - Dijkstra Segmenter'),
                main.tr('HanLP - N-shortest Path Segmenter'),
                main.tr('HanLP - Viterbi Segmenter')
            ],
            'zho_TW': [
                main.tr('jieba - With HMM'),
                main.tr('jieba - Without HMM'),
                main.tr('HanLP - Standard Tokenizer'),
                main.tr('HanLP - Basic Tokenizer'),
                main.tr('HanLP - NLP Tokenizer'),
                main.tr('HanLP - Speed Tokenizer'),
                main.tr('HanLP - Traditional Chinese Tokenizer'),
                main.tr('HanLP - URL Tokenizer'),
                main.tr('HanLP - CRF Lexical Analyzer'),
                main.tr('HanLP - Perceptron Lexical Analyzer'),
                main.tr('HanLP - Dijkstra Segmenter'),
                main.tr('HanLP - N-shortest Path Segmenter'),
                main.tr('HanLP - Viterbi Segmenter')
            ],
            'ces': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],
            'dan': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],
            'nld': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],
            'est': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],
            'fin': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],
            'fra': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],
            'deu': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],
            'ell': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],
            'ita': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],
            'nor': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],
            'pol': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],
            'por': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],
            'slv': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],
            'spa': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],
            'swe': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],
            'tur': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ],

            'other': [
                main.tr('NLTK - Treebank Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('NLTK - Word Punctuation Tokenizer'),
                main.tr('PyDelphin - Repp Tokenizer'),
            ]
        },

        'pos_taggers': {
            'eng': {
                main.tr('NLTK - Perceptron POS Tagger'): 'Penn Treebank'
            },

            'zho_CN': {
                main.tr('jieba'): 'jieba',
                main.tr('HanLP - CRF Lexical Analyzer'): 'HanLP',
                main.tr('HanLP - Perceptron Lexical Analyzer'): 'HanLP'
            },
            'zho_TW': {
                main.tr('jieba'): 'jieba',
                main.tr('HanLP - CRF Lexical Analyzer'): 'HanLP',
                main.tr('HanLP - Perceptron Lexical Analyzer'): 'HanLP'
            },
            'rus': {
                main.tr('NLTK - Perceptron POS Tagger'): 'Russian National Corpus'
            }
        },

        'tagsets': {
            # English
            'Penn Treebank': 'en-ptb',
            # Chinese
            'jieba': 'zho_jieba',
            'HanLP': 'zho_hanlp',
            # Russian
            'Russian National Corpus': 'rus_russian_national_corpus'
        },

        'lemmatizers': {
            'eng': [
                'NLTK',
                'e_lemma.txt',
                'Lemmatization Lists'
            ],

            'ast': [
                'Lemmatization Lists'
            ],
            'bul': [
                'Lemmatization Lists'
            ],
            'cat': [
                'Lemmatization Lists'
            ],
            'ces': [
                'Lemmatization Lists'
            ],
            'est': [
                'Lemmatization Lists'
            ],
            'fra': [
                'Lemmatization Lists'
            ],
            'glg': [
                'Lemmatization Lists'
            ],
            'deu': [
                'Lemmatization Lists'
            ],
            'hun': [
                'Lemmatization Lists'
            ],
            'gle': [
                'Lemmatization Lists'
            ],
            'ita': [
                'Lemmatization Lists'
            ],
            'glv': [
                'Lemmatization Lists'
            ],
            'fas': [
                'Lemmatization Lists'
            ],
            'por': [
                'Lemmatization Lists'
            ],
            'ron': [
                'Lemmatization Lists'
            ],
            'gla': [
                'Lemmatization Lists'
            ],
            'slk': [
                'Lemmatization Lists'
            ],
            'slv': [
                'Lemmatization Lists'
            ],
            'spa': [
                'Lemmatization Lists'
            ],
            'swe': [
                'Lemmatization Lists'
            ],
            'ukr': [
                'Lemmatization Lists'
            ],
            'cym': [
                'Lemmatization Lists'
            ]
        },

        'stop_words': {
            'eng': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],

            'afr': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'ara': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'hye': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'aze': [
                'NLTK'
            ],
            'eus': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'ben': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'bre': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'bul': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'cat': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'zho_CN': [
                'HanLP',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'zho_TW': [
                'HanLP',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'hrv': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'ces': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'dan': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'nld': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'epo': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'est': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'fin': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'fra': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'glg': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'deu': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'ell': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'hau': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'heb': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'hin': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'hun': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'ind': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'gle': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'ita': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'jpn': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'kaz': [
                'NLTK'
            ],
            'kor': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'kur': [
                'Stopwords ISO'
            ],
            'lat': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'lav': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'mar': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'msa': [
                'Stopwords ISO'
            ],
            'nep': [
                'NLTK'
            ],
            'nor': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'fas': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'pol': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'por': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'ron': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'rus': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'slk': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'slv': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'sot': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'som': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'spa': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'swa': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'swe': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'tgl': [
                'Stopwords ISO'
            ],
            'tha': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'tur': [
                'NLTK',
                'Stopwords ISO',
                'stopwords-json'
            ],
            'ukr': [
                'Stopwords ISO'
            ],
            'urd': [
                'Stopwords ISO'
            ],
            'vie': [
                'Stopwords ISO'
            ],
            'yor': [
                'Stopwords ISO',
                'stopwords-json'
            ],
            'zul': [
                'Stopwords ISO',
                'stopwords-json'
            ]
        },

        'assoc_measures': {
            main.tr('Frequency'): nltk.collocations.BigramAssocMeasures().raw_freq,
            main.tr('Student\'s T-test'): nltk.collocations.BigramAssocMeasures().student_t,
            main.tr('Pearson\'s Chi-squared Test'): nltk.collocations.BigramAssocMeasures().chi_sq,
            main.tr('Phi Coefficient'): nltk.collocations.BigramAssocMeasures().phi_sq,
            main.tr('Pointwise Mutual Information'): nltk.collocations.BigramAssocMeasures().pmi,
            main.tr('Likelihood Ratio'): nltk.collocations.BigramAssocMeasures().likelihood_ratio,
            main.tr('Poisson-Stirling'): nltk.collocations.BigramAssocMeasures().poisson_stirling,
            main.tr('Jaccard Index'): nltk.collocations.BigramAssocMeasures().jaccard,
            main.tr('Fisher\'s Exact Test'): nltk.collocations.BigramAssocMeasures().fisher,
            main.tr('Dice\'s Coefficient'): nltk.collocations.BigramAssocMeasures().dice
        },

        'style_dialog': '''
            <head>
              <style>
                * {
                  margin: 0;
                  border: 0;
                  padding: 0;

                  line-height: 1.2;
                  text-align: justify;
                }

                h1 {
                  margin-bottom: 10px;
                  font-size: 16px;
                  font-weight: bold;
                }

                p {
                  margin-bottom: 5px;
                }
              </style>
            </head>
        '''
    }

def init_settings_default(main):
    main.settings_default = {
        'general': {
            'encoding_input': ('utf_8', main.tr('All Languages')),
            'encoding_output': ('utf_8', main.tr('All Languages')),

            'precision_decimal': 2,
            'precision_pct': 2,

            'font_monospaced': 'Consolas',

            'style_highlight': 'border: 1px solid Red;'
        },

        'sentence_tokenization': {
            'sentence_tokenizers': {
                'eng': main.tr('NLTK - Punkt Sentence Tokenizer'),

                'zho_CN': main.tr('Wordless - Chinese Sentence Tokenizer'),
                'zho_TW': main.tr('Wordless - Chinese Sentence Tokenizer'),
                'ces': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'dan': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'nld': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'est': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'fin': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'fra': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'deu': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'ell': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'ita': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'nor': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'pol': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'por': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'slv': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'spa': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'swe': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'tur': main.tr('NLTK - Punkt Sentence Tokenizer'),

                'other': main.tr('NLTK - Punkt Sentence Tokenizer'),
            },

            'preview_lang': 'eng',
            'preview_samples': ''
        },

        'word_tokenization': {
            'word_tokenizers': {
                'eng': main.tr('NLTK - Treebank Tokenizer'),
                'zho_CN': main.tr('jieba - With HMM'),
                'zho_TW': main.tr('jieba - With HMM'),
                'ces': main.tr('NLTK - Treebank Tokenizer'),
                'dan': main.tr('NLTK - Treebank Tokenizer'),
                'nld': main.tr('NLTK - Treebank Tokenizer'),
                'est': main.tr('NLTK - Treebank Tokenizer'),
                'fin': main.tr('NLTK - Treebank Tokenizer'),
                'fra': main.tr('NLTK - Treebank Tokenizer'),
                'deu': main.tr('NLTK - Treebank Tokenizer'),
                'ell': main.tr('NLTK - Treebank Tokenizer'),
                'ita': main.tr('NLTK - Treebank Tokenizer'),
                'nor': main.tr('NLTK - Treebank Tokenizer'),
                'pol': main.tr('NLTK - Treebank Tokenizer'),
                'por': main.tr('NLTK - Treebank Tokenizer'),
                'slv': main.tr('NLTK - Treebank Tokenizer'),
                'spa': main.tr('NLTK - Treebank Tokenizer'),
                'swe': main.tr('NLTK - Treebank Tokenizer'),
                'tur': main.tr('NLTK - Treebank Tokenizer'),

                'other': main.tr('NLTK - Treebank Tokenizer')
            },

            'preview_lang': 'eng',
            'preview_samples': ''
        },

        'pos_tagging': {
            'pos_taggers': {
                'eng': main.tr('NLTK - Perceptron POS Tagger'),

                'zho_CN': main.tr('jieba'),
                'zho_TW':  main.tr('jieba'),
                'rus': main.tr('NLTK - Perceptron POS Tagger')
            },

            'tagsets': {
                'eng': 'Penn Treebank',

                'zho_CN': 'jieba',
                'zho_TW':  'jieba',
                'rus': 'Russian National Corpus'
            },

            'preview_lang': 'eng',
            'preview_samples': ''
        },

        'lemmatization': {
            'lemmatizers': {
                'eng': 'NLTK',

                'ast': 'Lemmatization Lists',
                'bul': 'Lemmatization Lists',
                'cat': 'Lemmatization Lists',
                'ces': 'Lemmatization Lists',
                'est': 'Lemmatization Lists',
                'fra': 'Lemmatization Lists',
                'gla': 'Lemmatization Lists',
                'glg': 'Lemmatization Lists',
                'deu': 'Lemmatization Lists',
                'hun': 'Lemmatization Lists',
                'gle': 'Lemmatization Lists',
                'ita': 'Lemmatization Lists',
                'glv': 'Lemmatization Lists',
                'fas': 'Lemmatization Lists',
                'por': 'Lemmatization Lists',
                'ron': 'Lemmatization Lists',
                'slk': 'Lemmatization Lists',
                'slv': 'Lemmatization Lists',
                'spa': 'Lemmatization Lists',
                'swe': 'Lemmatization Lists',
                'ukr': 'Lemmatization Lists',
                'cym': 'Lemmatization Lists'
            },

            'preview_lang': 'eng',
            'preview_samples': '',

        },

        'stop_words': {
            'stop_words': {
                'eng': 'NLTK',

                'afr': 'Stopwords ISO',
                'ara': 'NLTK',
                'hye': 'Stopwords ISO',
                'aze': 'NLTK',
                'eus': 'Stopwords ISO',
                'ben': 'Stopwords ISO',
                'bre': 'Stopwords ISO',
                'bul': 'Stopwords ISO',
                'cat': 'Stopwords ISO',
                'zho_CN': 'HanLP',
                'zho_TW': 'HanLP',
                'hrv': 'Stopwords ISO',
                'ces': 'Stopwords ISO',
                'dan': 'NLTK',
                'nld': 'NLTK',
                'epo': 'Stopwords ISO',
                'est': 'Stopwords ISO',
                'fin': 'NLTK',
                'fra': 'NLTK',
                'glg': 'Stopwords ISO',
                'deu': 'NLTK',
                'ell': 'NLTK',
                'hau': 'Stopwords ISO',
                'heb': 'Stopwords ISO',
                'hin': 'Stopwords ISO',
                'hun': 'NLTK',
                'ind': 'NLTK',
                'gle': 'Stopwords ISO',
                'ita': 'NLTK',
                'jpn': 'Stopwords ISO',
                'kaz': 'NLTK',
                'kor': 'Stopwords ISO',
                'kur': 'Stopwords ISO',
                'lat': 'Stopwords ISO',
                'lav': 'Stopwords ISO',
                'mar': 'Stopwords ISO',
                'msa': 'Stopwords ISO',
                'nep': 'NLTK',
                'nor': 'NLTK',
                'fas': 'Stopwords ISO',
                'pol': 'Stopwords ISO',
                'por': 'NLTK',
                'ron': 'NLTK',
                'rus': 'NLTK',
                'slk': 'Stopwords ISO',
                'slv': 'Stopwords ISO',
                'sot': 'Stopwords ISO',
                'som': 'Stopwords ISO',
                'spa': 'NLTK',
                'swa': 'Stopwords ISO',
                'swe': 'NLTK',
                'tgl': 'Stopwords ISO',
                'tha': 'Stopwords ISO',
                'tur': 'NLTK',
                'ukr': 'Stopwords ISO',
                'urd': 'Stopwords ISO',
                'vie': 'Stopwords ISO',
                'yor': 'Stopwords ISO',
                'zul': 'Stopwords ISO',
            },

            'preview_lang': 'eng',
        },

        'file': {
            'files_open': [],
            'files_closed': [],
            'root_path': '.',

            'subfolders': True,

            'auto_detect_encoding': True,
            'auto_detect_lang': True
        },

        'overview': {
            'words': True,
            'lowercase': True,
            'uppercase': True,
            'title_case': True,
            'treat_as_lowercase': True,
            'lemmatize': False,
            'filter_stop_words': False,

            'nums': True,
            'puncs': False,

            'base_sttr': 1000,

            'show_pct': True,
            'show_cumulative': False,
            'show_breakdown': True,
        },
    
        'concordancer': {
            'search_term': '',
            'search_terms': [],
            'ignore_case': True,
            'lemmatized_forms': True,
            'whole_word': True,
            'regex': False,
            'multi_search': False,
    
            'line_width_char': 80,
            'line_width_token': 20,
            'line_width_mode': main.tr('Tokens'),
    
            'number_lines': 25,
            'number_lines_no_limit': True,
    
            'punctuations': False,
    
            'sort_by': [main.tr('Offset'), main.tr('In Ascending Order')],
            'multi_sort_by': [[main.tr('Offset'), main.tr('Ascending')]],
            'multi_sort_colors': [
                '#bb302d',
                '#c2691d',
                '#cbbe01',
                '#569834',
                '#428989',
                '#172e7c',
                '#811570'
            ],
            'multi_sort': False
        },
    
        'wordlist': {
            'search_results': {
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_word': True,
                'use_regex': False,
                'multi_search_mode': False
            },

            'words': True,
            'lowercase': True,
            'uppercase': True,
            'title_case': True,
            'treat_as_lowercase': True,
            'lemmatize': False,
            'filter_stop_words': False,

            'nums': True,
            'puncs': False,

            'show_pct': True,
            'show_cumulative': False,
            'show_breakdown': True,

            'rank_no_limit': False,
            'rank_min': 1,
            'rank_max': 50,

            'use_pct': False,
            'use_cumulative': False,
    
            'freq_no_limit': True,
            'freq_min': 0,
            'freq_max': 1000,

            'apply_to': main.tr('Total'),

            'len_no_limit': True,
            'len_min': 1,
            'len_max': 20,

            'files_no_limit': True,
            'files_min': 1,
            'files_max': 100
        },
    
        'ngram': {
            'search_results': {
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_word': True,
                'use_regex': False,
                'multi_search_mode': False
            },
            
            'words': True,
            'lowercase': True,
            'uppercase': True,
            'title_case': True,
            'treat_as_lowercase': True,
            'lemmatize': False,
            'filter_stop_words': False,

            'nums': True,
            'puncs': False,
    
            'show_all': False,
            'search_term': '',
            'search_terms': [],
            'keyword_position_no_limit': True,
            'keyword_position_min': 1,
            'keyword_position_max': 2,

            'ignore_case': True,
            'match_inflected_forms': True,
            'match_whole_word': True,
            'use_regex': False,
            'multi_search_mode': False,

            'ngram_size_sync': False,
            'ngram_size_min': 2,
            'ngram_size_max': 2,
            'allow_skipped_tokens': 0,

            'show_pct': True,
            'show_cumulative': False,
            'show_breakdown': True,
    
            'rank_no_limit': False,
            'rank_min': 1,
            'rank_max': 50,

            'use_pct': False,
            'use_cumulative': False,
    
            'freq_no_limit': True,
            'freq_min': 0,
            'freq_max': 1000,
            
            'apply_to': main.tr('Total'),

            'len_no_limit': True,
            'len_min': 1,
            'len_max': 20,

            'files_no_limit': True,
            'files_min': 1,
            'files_max': 100
        },

        'collocation': {
            'search_results': {
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_word': True,
                'use_regex': False,
                'multi_search_mode': False
            },

            'words': True,
            'lowercase': True,
            'uppercase': True,
            'title_case': True,
            'treat_as_lowercase': True,
            'lemmatize': False,
            'filter_stop_words': False,

            'nums': True,
            'puncs': False,
    
            'search_term': '',
            'search_terms': [],
            'ignore_case': True,
            'match_inflected_forms': True,
            'match_whole_word': True,
            'use_regex': False,
            'multi_search_mode': False,
            'show_all': False,

            'window_sync': False,
            'window_left': -5,
            'window_right': 5,
            'assoc_measure': main.tr('Pearson\'s Chi-squared Test'),

            'show_pct': True,
            'show_cumulative': False,
            'show_breakdown_position': True,
            'show_breakdown_file': True,

            'use_data': main.tr('Score (Right)'),
            'use_pct': False,
            'use_cumulative': False,

            'rank_no_limit': False,
            'rank_min': 1,
            'rank_max': 50,

            'freq_left_no_limit': True,
            'freq_left_min': 0,
            'freq_left_max': 1000,
            'freq_right_no_limit': True,
            'freq_right_min': 0,
            'freq_right_max': 1000,

            'score_left_no_limit': True,
            'score_left_min': 0,
            'score_left_max': 100,
            'score_right_no_limit': True,
            'score_right_min': 0,
            'score_right_max': 100,
            
            'apply_to': main.tr('Total'),

            'len_no_limit': True,
            'len_min': 1,
            'len_max': 20,

            'files_no_limit': True,
            'files_min': 1,
            'files_max': 100
        },

        'colligation': {
            'search_results': {
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_word': True,
                'use_regex': False,
                'multi_search_mode': False
            },

            'treat_as_lowercase': True,
            'lemmatize': False,

            'puncs': False,
    
            'search_term': '',
            'search_terms': [],
            'search_type': main.tr('Token'),

            'ignore_case': True,
            'match_inflected_forms': True,
            'match_whole_word': True,
            'use_regex': False,
            'multi_search_mode': False,
            'show_all': False,

            'window_sync': False,
            'window_left': -5,
            'window_right': 5,
            'assoc_measure': main.tr('Pearson\'s Chi-squared Test'),

            'show_pct': True,
            'show_cumulative': False,
            'show_breakdown_position': True,
            'show_breakdown_file': True,

            'use_data': main.tr('Score (Right)'),
            'use_pct': False,
            'use_cumulative': False,

            'rank_no_limit': False,
            'rank_min': 1,
            'rank_max': 50,

            'freq_left_no_limit': True,
            'freq_left_min': 0,
            'freq_left_max': 1000,
            'freq_right_no_limit': True,
            'freq_right_min': 0,
            'freq_right_max': 1000,

            'score_left_no_limit': True,
            'score_left_min': 0,
            'score_left_max': 100,
            'score_right_no_limit': True,
            'score_right_min': 0,
            'score_right_max': 100,
            
            'apply_to': main.tr('Total'),

            'files_no_limit': True,
            'files_min': 1,
            'files_max': 100
        },
    
        'semantics': {
            'search_term': '',
            'search_mode': main.tr('Word'),
            'search_for': main.tr('Synonyms'),
    
            'degree_max': 10,
            'degree_no_limit': True,
            'depth_max': 5,
            'depth_no_limit': True,
            'recursive': True,
            'show_lemmas': True,
    
            'parts_of_speech': {
                'n': main.tr('Noun'),
                'v': main.tr('Verb'),
                'a': main.tr('Adjective'),
                's': main.tr('Adjective Satellite'),
                'r': main.tr('Adverb')
            }
        }
    }
