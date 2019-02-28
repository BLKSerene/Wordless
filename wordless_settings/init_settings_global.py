#
# Wordless: Settings - Global Settings
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

from wordless_measures import *

def init_settings_global(main):
    main.settings_global = {
        'langs': {
            main.tr('Afrikaans'): 'afr',
            main.tr('Albanian'): 'sqi',
            main.tr('Amharric'): 'amh',
            main.tr('Arabic'): 'ara',
            main.tr('Aragonese'): 'arg',
            main.tr('Armenian'): 'hye',
            main.tr('Assamese'): 'asm',
            main.tr('Asturian'): 'ast', # Lemmatization
            main.tr('Azerbaijani'): 'aze',
            main.tr('Basque'): 'eus',
            main.tr('Belarusian'): 'bel',
            main.tr('Bengali'): 'ben',
            main.tr('Bosnian'): 'bos',
            main.tr('Breton'): 'bre',
            main.tr('Bulgarian'): 'bul',
            main.tr('Catalan'): 'cat',
            main.tr('Chinese (Simplified)'): 'zho_cn',
            main.tr('Chinese (Traditional)'): 'zho_tw',
            main.tr('Croatian'): 'hrv',
            main.tr('Czech'): 'ces',
            main.tr('Danish'): 'dan',
            main.tr('Dutch'): 'nld',
            main.tr('Dzongkha'): 'dzo',
            main.tr('English'): 'eng',
            main.tr('Esperanto'): 'epo',
            main.tr('Estonian'): 'est',
            main.tr('Faroese'): 'fao',
            main.tr('Finnish'): 'fin',
            main.tr('French'): 'fra',
            main.tr('Galician'): 'glg',
            main.tr('Georgian'): 'kat',
            main.tr('German'): 'deu',
            main.tr('Greek (Ancient)'): 'grc', # Stop Words & Lemmatization
            main.tr('Greek (Modern)'): 'ell',
            main.tr('Gujarati'): 'guj',
            main.tr('Haitian'): 'hat',
            main.tr('Hausa'): 'hau', # Stop Words
            main.tr('Hebrew'): 'heb',
            main.tr('Hindi'): 'hin',
            main.tr('Hungarian'): 'hun',
            main.tr('Indonesian'): 'ind',
            main.tr('Irish'): 'gle',
            main.tr('Islandic'): 'isl',
            main.tr('Italian'): 'ita',
            main.tr('Japanese'): 'jpn',
            main.tr('Javanese'): 'jav',
            main.tr('Kannada'): 'kan',
            main.tr('Kazakh'): 'kaz',
            main.tr('Khmer'): 'khm',
            main.tr('Kinyarwanda'): 'kin',
            main.tr('Korean'): 'kor',
            main.tr('Kurdish'): 'kur',
            main.tr('Kyrgyz'): 'kir',
            main.tr('Lao'): 'lao',
            main.tr('Latin'): 'lat',
            main.tr('Latvian'): 'lav',
            main.tr('Lithuanian'): 'lit',
            main.tr('Luxembourg'): 'ltz',
            main.tr('Macedonian'): 'mkd',
            main.tr('Malagasy'): 'mlg',
            main.tr('Malay'): 'msa',
            main.tr('Malayalam'): 'mal',
            main.tr('Maltese'): 'mlt',
            main.tr('Manx'): 'glv', # Lemmatization
            main.tr('Marathi'): 'mar',
            main.tr('Mongolian'): 'mon',
            main.tr('Nepali'): 'nep',
            main.tr('Norwegian Bokmål'): 'nob',
            main.tr('Norwegian Nynorsk'): 'nno',
            main.tr('Occitan'): 'oci',
            main.tr('Oriya'): 'ori',
            main.tr('Pashto'): 'pus',
            main.tr('Persian'): 'fas',
            main.tr('Polish'): 'pol',
            main.tr('Portuguese'): 'por',
            main.tr('Punjabi'): 'pan',
            main.tr('Quechua'): 'que',
            main.tr('Romanian'): 'ron',
            main.tr('Russian'): 'rus',
            main.tr('Sami (Northern)'): 'sme',
            main.tr('Scottish Gaelic'): 'gla', # Lemmatization
            main.tr('Serbian'): 'srp',
            main.tr('Sinhala'): 'sin',
            main.tr('Slovak'): 'slk',
            main.tr('Slovenian'): 'slv',
            main.tr('Somali'): 'som', # Stop Words
            main.tr('Sotho (Southern)'): 'sot', # Stop Words
            main.tr('Spanish'): 'spa',
            main.tr('Swahili'): 'swa',
            main.tr('Swedish'): 'swe',
            main.tr('Tagalog'): 'tgl',
            main.tr('Tajik'): 'tgk', # Word Tokenization
            main.tr('Tamil'): 'tam',
            main.tr('Tatar'): 'tat', # Stop Words
            main.tr('Telugu'): 'tel',
            main.tr('Thai'): 'tha',
            main.tr('Tibetan'): 'bod', # Word Tokenization, POS Tagging, Lemmatization
            main.tr('Turkish'): 'tur',
            main.tr('Ukrainian'): 'ukr',
            main.tr('Urdu'): 'urd',
            main.tr('Uyghur'): 'uig',
            main.tr('Vietnamese'): 'vie',
            main.tr('Volapük'): 'vol',
            main.tr('Walloon'): 'wln',
            main.tr('Welsh'): 'cym',
            main.tr('Xhosa'): 'xho',
            main.tr('Yoruba'): 'yor', # Stop Words
            main.tr('Zulu'): 'zul',

            main.tr('Other Languages'): 'other'
        },

        'lang_codes': {
            'afr': 'af',
            'amh': 'am',
            'ara': 'ar',
            'arg': 'an',
            'asm': 'as',
            'ast': 'ast', # Lemmatization
            'aze': 'az',
            'bel': 'be',
            'ben': 'bn',
            'bod': 'bo', # Word Tokenization, POS Tagging, Lemmatization
            'bos': 'bs',
            'bre': 'br',
            'bul': 'bg',
            'cat': 'ca',
            'ces': 'cs',
            'cym': 'cy',
            'dan': 'da',
            'deu': 'de',
            'dzo': 'dz',
            'ell': 'el',
            'eng': 'en',
            'epo': 'eo',
            'est': 'et',
            'eus': 'eu',
            'fao': 'fo',
            'fas': 'fa',
            'fin': 'fi',
            'fra': 'fr',
            'gla': 'gd', # Lemmatization
            'gle': 'ga',
            'glg': 'gl',
            'glv': 'gv', # Lemmatization
            'grc': 'grc', # Stop Words & Lemmatization
            'guj': 'gu',
            'hat': 'ht',
            'hau': 'ha',
            'heb': 'he',
            'hin': 'hi',
            'hrv': 'hr',
            'hun': 'hu',
            'hye': 'hy',
            'ind': 'id',
            'isl': 'is',
            'ita': 'it',
            'jav': 'jv',
            'jpn': 'ja',
            'kan': 'kn',
            'kat': 'ka',
            'kaz': 'kk',
            'khm': 'km',
            'kin': 'rw',
            'kir': 'ky',
            'kor': 'ko',
            'kur': 'ku',
            'lao': 'lo',
            'lat': 'la',
            'lav': 'lv',
            'lit': 'lt',
            'ltz': 'lb',
            'mal': 'ml',
            'mar': 'mr',
            'mkd': 'mk',
            'mlg': 'mg',
            'mlt': 'mt',
            'mon': 'mn',
            'msa': 'ms',
            'nep': 'ne',
            'nld': 'nl',
            'nno': 'nn',
            'nob': 'nb',
            'oci': 'oc',
            'ori': 'or',
            'pan': 'pa',
            'pol': 'pl',
            'por': 'pt',
            'pus': 'ps',
            'que': 'qu',
            'ron': 'ro',
            'rus': 'ru',
            'sin': 'si',
            'slk': 'sk',
            'slv': 'sl',
            'sme': 'se',
            'som': 'so', # Stop Words
            'sot': 'st', # Stop Words
            'spa': 'es',
            'sqi': 'sq',
            'srp': 'sr',
            'swa': 'sw',
            'swe': 'sv',
            'tam': 'ta',
            'tat': 'tt', # Stop Words
            'tel': 'te',
            'tgk': 'tg',
            'tgl': 'tl',
            'tha': 'th',
            'tur': 'tr',
            'uig': 'ug',
            'ukr': 'uk',
            'urd': 'ur',
            'vie': 'vi',
            'vol': 'vo',
            'wln': 'wa',
            'xho': 'xh',
            'yor': 'yo',
            'zho_cn': 'zh_cn',
            'zho_tw': 'zh_tw',
            'zul': 'zu',

            'other': 'other',
        },

        'text_types': {
            main.tr('Untokenized / Untagged'): ('untokenized', 'untagged'),
            main.tr('Untokenized / Tagged (Non-POS)'): ('untokenized', 'tagged_non_pos'),

            main.tr('Tokenized / Untagged'): ('tokenized', 'untagged'),
            main.tr('Tokenized / Tagged (POS)'): ('tokenized', 'tagged_pos'),
            main.tr('Tokenized / Tagged (Non-POS)'): ('tokenized', 'tagged_non_pos'),
            main.tr('Tokenized / Tagged (Both)'): ('tokenized', 'tagged_both')
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

            main.tr('Arabic (CP720)'): 'cp720',
            main.tr('Arabic (CP864)'): 'cp864',
            main.tr('Arabic (ISO-8859-6)'): 'iso8859_6',
            main.tr('Arabic (Mac OS Arabic)'): 'mac_arabic',
            main.tr('Arabic (Windows-1256)'): 'cp1256',

            main.tr('Baltic Languages (CP775)'): 'cp775',
            main.tr('Baltic Languages (ISO-8859-13)'): 'iso8859_13',
            main.tr('Baltic Languages (Windows-1257)'): 'cp1257',

            main.tr('Celtic Languages (ISO-8859-14)'): 'iso8859_14',

            main.tr('Central European (CP852)'): 'cp852',
            main.tr('Central European (ISO-8859-2)'): 'iso8859_2',
            main.tr('Central European (Mac OS Central European)'): 'mac_latin2',
            main.tr('Central European (Windows-1250)'): 'cp1250',

            main.tr('Chinese (GB18030)'): 'gb18030',
            main.tr('Chinese (GBK)'): 'gbk',

            main.tr('Chinese (Simplified) (GB2312)'): 'gb2312',
            main.tr('Chinese (Simplified) (HZ)'): 'hz_gb_2312',

            main.tr('Chinese (Traditional) (Big-5)'): 'big5',
            main.tr('Chinese (Traditional) (Big5-HKSCS)'): 'big5hkscs',
            main.tr('Chinese (Traditional) (CP950)'): 'cp950',

            main.tr('Croatian (Mac OS Croatian)'): 'mac_croatian',

            main.tr('Cyrillic (CP855)'): 'cp855',
            main.tr('Cyrillic (CP866)'): 'cp866',
            main.tr('Cyrillic (ISO-8859-5)'): 'iso8859_5',
            main.tr('Cyrillic (Mac OS Cyrillic)'): 'mac_cyrillic',
            main.tr('Cyrillic (Windows-1251)'): 'cp1251',

            main.tr('English (ASCII)'): 'ascii',
            main.tr('English (EBCDIC 037)'): 'cp037',
            main.tr('English (CP437)'): 'cp437',

            main.tr('Esperanto/Maltese (ISO-8859-3)'): 'iso8859_3',

            main.tr('European (HP Roman-8)'): 'hp_roman8',

            main.tr('French (CP863)'): 'cp863',

            main.tr('German (EBCDIC 273)'): 'cp273',

            main.tr('Greek (CP737)'): 'cp737',
            main.tr('Greek (CP869)'): 'cp869',
            main.tr('Greek (CP875)'): 'cp875',
            main.tr('Greek (ISO-8859-7)'): 'iso8859_7',
            main.tr('Greek (Mac OS Greek)'): 'mac_greek',
            main.tr('Greek (Windows-1253)'): 'windows_1253',

            main.tr('Hebrew (CP856)'): 'cp856',
            main.tr('Hebrew (CP862)'): 'cp862',
            main.tr('Hebrew (EBCDIC 424)'): 'cp424',
            main.tr('Hebrew (ISO-8859-8)'): 'iso8859_8',
            main.tr('Hebrew (Windows-1255)'): 'windows_1255',

            main.tr('Icelandic (CP861)'): 'cp861',
            main.tr('Icelandic (Mac OS Icelandic)'): 'mac_iceland',

            main.tr('Japanese (CP932)'): 'cp932',
            main.tr('Japanese (EUC-JP)'): 'euc_jp',
            main.tr('Japanese (EUC-JIS-2004)'): 'euc_jis_2004',
            main.tr('Japanese (EUC-JISx0213)'): 'euc_jisx0213',
            main.tr('Japanese (ISO-2022-JP)'): 'iso2022_jp',
            main.tr('Japanese (ISO-2022-JP-1)'): 'iso2022_jp_1',
            main.tr('Japanese (ISO-2022-JP-2)'): 'iso2022_jp_2',
            main.tr('Japanese (ISO-2022-JP-2004)'): 'iso2022_jp_2004',
            main.tr('Japanese (ISO-2022-JP-3)'): 'iso2022_jp_3',
            main.tr('Japanese (ISO-2022-JP-EXT)'): 'iso2022_jp_ext',
            main.tr('Japanese (Shift_JIS)'): 'shift_jis',
            main.tr('Japanese (Shift_JIS-2004)'): 'shift_jis_2004',
            main.tr('Japanese (Shift_JISx0213)'): 'shift_jisx0213',

            main.tr('Kazakh (KZ-1048)'): 'kz1048',
            main.tr('Kazakh (PTCP154)'): 'ptcp154',

            main.tr('Korean (EUC-KR)'): 'euc_kr',
            main.tr('Korean (ISO-2022-KR)'): 'iso2022_kr',
            main.tr('Korean (JOHAB)'): 'johab',
            main.tr('Korean (Windows-949)'): 'cp949',

            main.tr('Nordic Languages (CP865)'): 'cp865',
            main.tr('Nordic Languages (ISO-8859-10)'): 'iso8859_10',

            main.tr('North European (ISO-8859-4)'): 'iso8859_4',

            main.tr('Persian (Mac OS Farsi)'): 'mac_farsi',

            main.tr('Portuguese (CP860)'): 'cp860',

            main.tr('Romanian (Mac OS Romanian)'): 'mac_romanian',

            main.tr('Russian (KOI8-R)'): 'koi8_r',

            main.tr('South-Eastern European (ISO-8859-16)'): 'iso8859_16',

            main.tr('Tajik (KOI8-T)'): 'koi8_t',

            main.tr('Thai (CP874)'): 'cp874',
            main.tr('Thai (ISO-8859-11)'): 'iso8859_11',
            main.tr('Thai (TIS-620)'): 'tis_620',

            main.tr('Turkish (CP857)'): 'cp857',
            main.tr('Turkish (EBCDIC 1026)'): 'cp1026',
            main.tr('Turkish (ISO-8859-9)'): 'iso8859_9',
            main.tr('Turkish (Mac OS Turkish)'): 'mac_turkish',
            main.tr('Turkish (Windows-1254)'): 'cp1254',

            main.tr('Ukrainian (CP1125)'): 'cp1125',
            main.tr('Ukrainian (KOI8-U)'): 'koi8_u',

            main.tr('Urdu (CP1006)'): 'cp1006',
            main.tr('Urdu (Mac OS Farsi)'): 'mac_farsi',

            main.tr('Vietnamese (CP1258)'): 'cp1258',

            main.tr('Western European (EBCDIC 500)'): 'cp500',
            main.tr('Western European (CP850)'): 'cp850',
            main.tr('Western European (CP858)'): 'cp858',
            main.tr('Western European (CP1140)'): 'cp1140',
            main.tr('Western European (ISO-8859-1)'): 'latin_1',
            main.tr('Western European (ISO-8859-15)'): 'iso8859_15',
            main.tr('Western European (Mac OS Roman)'): 'mac_roman',
            main.tr('Western European (Windows-1252)'): 'windows_1252',
        },

        'file_types': {
            'files': [
                main.tr('Text File (*.txt)'),
                main.tr('Word Document (*.docx)'),
                main.tr('Excel Workbook (*.xls; *.xlsx)'),
                main.tr('CSV File(*.csv)'),
                main.tr('HTML Page (*.htm; *.html)'),
                main.tr('Translation Memory File (*.tmx)'),
                main.tr('Lyrics File (*.lrc)'),
                main.tr('All Files (*.*)')
            ],

            'export_tables': [
                main.tr('Excel Workbook (*.xlsx)'),
                main.tr('CSV File (*.csv)')
            ]
        },

        'sentence_tokenizers': {
            'zho_cn': [
                main.tr('Wordless - Chinese Sentence Tokenizer')
            ],

            'zho_tw': [
                main.tr('Wordless - Chinese Sentence Tokenizer')
            ],

            'ces': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],

            'dan': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],

            'nld': [
                main.tr('NLTK - Punkt Sentence Tokenizer'),
                main.tr('spaCy - Dutch Sentence Tokenizer')
            ],

            'eng': [
                main.tr('NLTK - Punkt Sentence Tokenizer'),
                main.tr('spaCy - English Sentence Tokenizer')
            ],

            'est': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],

            'fin': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],

            'fra': [
                main.tr('NLTK - Punkt Sentence Tokenizer'),
                main.tr('spaCy - French Sentence Tokenizer')
            ],

            'deu': [
                main.tr('NLTK - Punkt Sentence Tokenizer'),
                main.tr('spaCy - German Sentence Tokenizer')
            ],

            'ell': [
                main.tr('NLTK - Punkt Sentence Tokenizer'),
                main.tr('spaCy - Greek (Modern) Sentence Tokenizer')
            ],

            'ita': [
                main.tr('NLTK - Punkt Sentence Tokenizer'),
                main.tr('spaCy - Italian Sentence Tokenizer')
            ],

            'jpn': [
                main.tr('Wordless - Japanese Sentence Tokenizer')
            ],

            'nob': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],

            'nno': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],

            'pol': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],

            'por': [
                main.tr('NLTK - Punkt Sentence Tokenizer'),
                main.tr('spaCy - Portuguese Sentence Tokenizer')
            ],

            'slv': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],

            'spa': [
                main.tr('NLTK - Punkt Sentence Tokenizer'),
                main.tr('spaCy - Spanish Sentence Tokenizer')
            ],

            'swe': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],

            'tha': [
                main.tr('PyThaiNLP - Thai Sentence Tokenizer')
            ],

            'tur': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ],

            'vie': [
                main.tr('Underthesea - Vietnamese Sentence Tokenizer')
            ],

            'other': [
                main.tr('NLTK - Punkt Sentence Tokenizer')
            ]
        },

        'word_tokenizers': {
            'ara': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Arabic Word Tokenizer')
            ],

            'ben': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Bengali Word Tokenizer')
            ],

            'cat': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Catalan Word Tokenizer')
            ],

            'zho_cn': [
                main.tr('jieba - Chinese Word Tokenizer'),
                main.tr('Wordless - Chinese Character Tokenizer')
            ],

            'zho_tw': [
                main.tr('jieba - Chinese Word Tokenizer'),
                main.tr('Wordless - Chinese Character Tokenizer')
            ],

            'hrv': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Croatian Word Tokenizer')
            ],

            'ces': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer')
            ],

            'dan': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Danish Word Tokenizer')
            ],

            'nld': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Dutch Word Tokenizer')
            ],

            'eng': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - English Word Tokenizer')
            ],

            'fin': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Finnish Word Tokenizer')
            ],

            'fra': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - French Word Tokenizer')
            ],

            'deu': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - German Word Tokenizer')
            ],

            'ell': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Greek (Modern) Word Tokenizer')
            ],

            'heb': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Hebrew Word Tokenizer')
            ],

            'hin': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Hindi Word Tokenizer')
            ],

            'hun': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Hungarian Word Tokenizer')
            ],

            'isl': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer')
            ],

            'ind': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Indonesian Word Tokenizer')
            ],

            'gle': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Irish Word Tokenizer')
            ],

            'ita': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Italian Word Tokenizer')
            ],

            'jpn': [
                main.tr('nagisa - Japanese Word Tokenizer'),
                main.tr('Wordless - Japanese Kanji Tokenizer')
            ],

            'kan': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Kannada Word Tokenizer')
            ],

            'lav': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer')
            ],

            'nob': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Norwegian Bokmål Word Tokenizer')
            ],

            'fas': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Persian Word Tokenizer')
            ],

            'pol': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Polish Word Tokenizer')
            ],

            'por': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Portuguese Word Tokenizer')
            ],

            'ron': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Romanian Word Tokenizer')
            ],

            'rus': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Russian Word Tokenizer')
            ],

            'sin': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Sinhala Word Tokenizer')
            ],

            'slk': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer')
            ],

            'slv': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer')
            ],

            'spa': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Spanish Word Tokenizer')
            ],

            'swe': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Swedish Word Tokenizer')
            ],

            'tgk': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer')
            ],

            'tam': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Tamil Word Tokenizer')
            ],

            'tat': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Tatar Word Tokenizer')
            ],

            'tel': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Telugu Word Tokenizer')
            ],

            'tha': [
                main.tr('PyThaiNLP - Maximum Matching Algorithm + TCC'),
                main.tr('PyThaiNLP - Maximum Matching Algorithm'),
                main.tr('PyThaiNLP - Longest Matching'),
            ],

            'bod': [
                main.tr('pybo - Tibetan Word Tokenizer')
            ],

            'tur': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Turkish Word Tokenizer')
            ],

            'ukr': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Ukrainian Word Tokenizer')
            ],

            'urd': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - Urdu Word Tokenizer')
            ],

            'vie': [
                main.tr('Underthesea - Vietnamese Word Tokenizer')
            ],

            'other': [
                main.tr('NLTK - Penn Treebank Tokenizer'),
                main.tr('NLTK - NIST Tokenizer'),
                main.tr('NLTK - Tok-tok Tokenizer'),
                main.tr('NLTK - Twitter Tokenizer'),
                main.tr('SacreMoses - Moses Tokenizer'),
                main.tr('SacreMoses - Penn Treebank Tokenizer'),
                main.tr('spaCy - English Word Tokenizer')
            ]
        },

        'word_detokenizers': {
            'cat': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'zho_cn': [
                main.tr('Wordless - Chinese Word Detokenizer')
            ],

            'zho_tw': [
                main.tr('Wordless - Chinese Word Detokenizer')
            ],

            'ces': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'nld': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'eng': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'fin': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'fra': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'deu': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'ell': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'hun': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'isl': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'jpn': [
                main.tr('Wordless - Japanese Word Detokenizer')
            ],

            'lav': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'pol': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'por': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'ron': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'rus': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'slk': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'slv': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'spa': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'swe': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'tam': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ],

            'tha': [
                main.tr('Wordless - Thai Word Detokenizer')
            ],

            'bod': [
                main.tr('Wordless - Tibetan Word Detokenizer')
            ],

            'other': [
                main.tr('NLTK - Penn Treebank Detokenizer'),
                main.tr('SacreMoses - Moses Detokenizer')
            ]
        },

        'pos_taggers': {
            'zho_cn': [
                main.tr('jieba - Chinese POS Tagger')
            ],

            'zho_tw': [
                main.tr('jieba - Chinese POS Tagger')
            ],

            'nld': [
                main.tr('spaCy - Dutch POS Tagger')
            ],

            'eng': [
                main.tr('NLTK - Perceptron POS Tagger'),
                main.tr('spaCy - English POS Tagger')
            ],

            'fra': [
                main.tr('spaCy - French POS Tagger')
            ],

            'deu': [
                main.tr('spaCy - German POS Tagger')
            ],

            'ell': [
                main.tr('spaCy - Greek (Modern) POS Tagger')
            ],

            'ita': [
                main.tr('spaCy - Italian POS Tagger')
            ],

            'jpn': [
                main.tr('nagisa - Japanese POS Tagger')
            ],

            'por': [
                main.tr('spaCy - Portuguese POS Tagger')
            ],

            'rus': [
                main.tr('NLTK - Perceptron POS Tagger'),
                main.tr('pymorphy2 - Morphological Analyzer')
            ],

            'spa': [
                main.tr('spaCy - Spanish POS Tagger'),
            ],

            'tha': [
                main.tr('PyThaiNLP - Perceptron POS Tagger - ORCHID Corpus'),
                main.tr('PyThaiNLP - Perceptron POS Tagger - PUD Corpus')
            ],

            'bod': [
                main.tr('pybo - Tibetan POS Tagger')
            ],

            'ukr': [
                main.tr('pymorphy2 - Morphological Analyzer')
            ],

            'vie': [
                main.tr('Underthesea - Vietnamese POS Tagger')
            ]
        },

        'lemmatizers': {
            'ast': [
                main.tr('Lemmatization Lists - Asturian Lemma List')
            ],

            'bul': [
                main.tr('Lemmatization Lists - Bulgarian Lemma List')
            ],

            'cat': [
                main.tr('Lemmatization Lists - Catalan Lemma List')
            ],

            'ces': [
                main.tr('Lemmatization Lists - Czech Lemma List')
            ],

            'nld': [
                main.tr('spaCy - Dutch Lemmatizer')
            ],

            'eng': [
                main.tr('Lemmatization Lists - English Lemma List'),
                main.tr('NLTK - WordNet Lemmatizer'),
                main.tr('spaCy - English Lemmatizer')
            ],

            'est': [
                main.tr('Lemmatization Lists - Estonian Lemma List')
            ],

            'fra': [
                main.tr('Lemmatization Lists - French Lemma List'),
                main.tr('spaCy - French Lemmatizer')
            ],

            'glg': [
                main.tr('Lemmatization Lists - Galician Lemma List')
            ],

            'deu': [
                main.tr('Lemmatization Lists - German Lemma List'),
                main.tr('spaCy - German Lemmatizer')
            ],

            'grc': [
                main.tr('lemmalist-greek - Greek (Ancient) Lemma List')
            ],

            'ell': [
                main.tr('spaCy - Greek (Modern) Lemmatizer')
            ],

            'hun': [
                main.tr('Lemmatization Lists - Hungarian Lemma List')
            ],

            'gle': [
                main.tr('Lemmatization Lists - Irish Lemma List')
            ],

            'ita': [
                main.tr('Lemmatization Lists - Italian Lemma List'),
                main.tr('spaCy - Italian Lemmatizer')
            ],

            'glv': [
                main.tr('Lemmatization Lists - Manx Lemma List')
            ],

            'fas': [
                main.tr('Lemmatization Lists - Persian Lemma List')
            ],

            'por': [
                main.tr('Lemmatization Lists - Portuguese Lemma List'),
                main.tr('spaCy - Portuguese Lemmatizer')
            ],

            'ron': [
                main.tr('Lemmatization Lists - Romanian Lemma List')
            ],

            'rus': [
                main.tr('pymorphy2 - Morphological Analyzer')
            ],

            'gla': [
                main.tr('Lemmatization Lists - Scottish Gaelic Lemma List')
            ],

            'slk': [
                main.tr('Lemmatization Lists - Slovak Lemma List')
            ],

            'slv': [
                main.tr('Lemmatization Lists - Slovenian Lemma List')
            ],

            'spa': [
                main.tr('Lemmatization Lists - Spanish Lemma List'),
                main.tr('spaCy - Spanish Lemmatizer')
            ],

            'swe': [
                main.tr('Lemmatization Lists - Swedish Lemma List')
            ],

            'bod': [
                main.tr('pybo - Tibetan Lemmatizer')
            ],

            'ukr': [
                main.tr('Lemmatization Lists - Ukrainian Lemma List'),
                main.tr('pymorphy2 - Morphological Analyzer')
            ],

            'cym': [
                main.tr('Lemmatization Lists - Welsh Lemma List')
            ]
        },

        'stop_words': {
            'afr': [
                main.tr('Stopwords ISO - Afrikaans Stop Words'),
                main.tr('Custom List')
            ],

            'ara': [
                main.tr('NLTK - Arabic Stop Words'),
                main.tr('spaCy - Arabic Stop Words'),
                main.tr('Stopwords ISO - Arabic Stop Words'),
                main.tr('Custom List')
            ],

            'hye': [
                main.tr('Stopwords ISO - Armenian Stop Words'),
                main.tr('Custom List')
            ],

            'aze': [
                main.tr('NLTK - Azerbaijani Stop Words'),
                main.tr('Custom List')
            ],

            'eus': [
                main.tr('Stopwords ISO - Basque Stop Words'),
                main.tr('Custom List')
            ],

            'ben': [
                main.tr('spaCy - Bengali Stop Words'),
                main.tr('Stopwords ISO - Bengali Stop Words'),
                main.tr('Custom List')
            ],

            'bre': [
                main.tr('Stopwords ISO - Breton Stop Words'),
                main.tr('Custom List')
            ],

            'bul': [
                main.tr('Stopwords ISO - Bulgarian Stop Words'),
                main.tr('Custom List')
            ],

            'cat': [
                main.tr('spaCy - Catalan Stop Words'),
                main.tr('Stopwords ISO - Catalan Stop Words'),
                main.tr('Custom List')
            ],

            'zho_cn': [
                main.tr('spaCy - Chinese (Simplified) Stop Words'),
                main.tr('Stopwords ISO - Chinese (Simplified) Stop Words'),
                main.tr('Custom List')
            ],

            'zho_tw': [
                main.tr('spaCy - Chinese (Traditional) Stop Words'),
                main.tr('Stopwords ISO - Chinese (Traditional) Stop Words'),
                main.tr('Custom List')
            ],

            'hrv': [
                main.tr('spaCy - Croatian Stop Words'),
                main.tr('Stopwords ISO - Croatian Stop Words'),
                main.tr('Custom List')
            ],

            'ces': [
                main.tr('Stopwords ISO - Czech Stop Words'),
                main.tr('Custom List')
            ],

            'dan': [
                main.tr('NLTK - Danish Stop Words'),
                main.tr('spaCy - Danish Stop Words'),
                main.tr('Stopwords ISO - Danish Stop Words'),
                main.tr('Custom List')
            ],

            'nld': [
                main.tr('NLTK - Dutch Stop Words'),
                main.tr('spaCy - Dutch Stop Words'),
                main.tr('Stopwords ISO - Dutch Stop Words'),
                main.tr('Custom List')
            ],

            'eng': [
                main.tr('NLTK - English Stop Words'),
                main.tr('spaCy - English Stop Words'),
                main.tr('Stopwords ISO - English Stop Words'),
                main.tr('Custom List')
            ],

            'epo': [
                main.tr('Stopwords ISO - Esperanto Stop Words'),
                main.tr('Custom List')
            ],

            'est': [
                main.tr('Stopwords ISO - Estonian Stop Words'),
                main.tr('Custom List')
            ],

            'fin': [
                main.tr('NLTK - Finnish Stop Words'),
                main.tr('spaCy - Finnish Stop Words'),
                main.tr('Stopwords ISO - Finnish Stop Words'),
                main.tr('Custom List')
            ],

            'fra': [
                main.tr('NLTK - French Stop Words'),
                main.tr('spaCy - French Stop Words'),
                main.tr('Stopwords ISO - French Stop Words'),
                main.tr('Custom List')
            ],

            'glg': [
                main.tr('Stopwords ISO - Galician Stop Words'),
                main.tr('Custom List')
            ],

            'deu': [
                main.tr('NLTK - German Stop Words'),
                main.tr('spaCy - German Stop Words'),
                main.tr('Stopwords ISO - German Stop Words'),
                main.tr('Custom List')
            ],

            'grc': [
                main.tr('grk-stoplist - Greek (Ancient) Stop Words'),
                main.tr('Custom List')
            ],

            'ell': [
                main.tr('NLTK - Greek Stop Words'),
                main.tr('spaCy - Greek Stop Words'),
                main.tr('Stopwords ISO - Greek Stop Words'),
                main.tr('Custom List')
            ],

            'hau': [
                main.tr('Stopwords ISO - Hausa Stop Words'),
                main.tr('Custom List')
            ],

            'heb': [
                main.tr('spaCy - Hebrew Stop Words'),
                main.tr('Stopwords ISO - Hebrew Stop Words'),
                main.tr('Custom List')
            ],

            'hin': [
                main.tr('spaCy - Hindi Stop Words'),
                main.tr('Stopwords ISO - Hindi Stop Words'),
                main.tr('Custom List')
            ],

            'hun': [
                main.tr('NLTK - Hungarian Stop Words'),
                main.tr('spaCy - Hungarian Stop Words'),
                main.tr('Stopwords ISO - Hungarian Stop Words'),
                main.tr('Custom List')
            ],

            'ind': [
                main.tr('NLTK - Indonesian Stop Words'),
                main.tr('spaCy - Indonesian Stop Words'),
                main.tr('Stopwords ISO - Indonesian Stop Words'),
                main.tr('Custom List')
            ],

            'gle': [
                main.tr('spaCy - Irish Stop Words'),
                main.tr('Stopwords ISO - Irish Stop Words'),
                main.tr('Custom List')
            ],

            'ita': [
                main.tr('NLTK - Italian Stop Words'),
                main.tr('spaCy - Italian Stop Words'),
                main.tr('Stopwords ISO - Italian Stop Words'),
                main.tr('Custom List')
            ],

            'jpn': [
                main.tr('spaCy - Japanese Stop Words'),
                main.tr('Stopwords ISO - Japanese Stop Words'),
                main.tr('Custom List')
            ],

            'kaz': [
                main.tr('NLTK - Kazakh Stop Words'),
                main.tr('Custom List')
            ],

            'kor': [
                main.tr('Stopwords ISO - Korean Stop Words'),
                main.tr('Custom List')
            ],

            'kur': [
                main.tr('Stopwords ISO - Kurdish Stop Words'),
                main.tr('Custom List')
            ],

            'lat': [
                main.tr('Stopwords ISO - Latin Stop Words'),
                main.tr('Custom List')
            ],

            'lav': [
                main.tr('Stopwords ISO - Latvian Stop Words'),
                main.tr('Custom List')
            ],

            'mar': [
                main.tr('Stopwords ISO - Marathi Stop Words'),
                main.tr('Custom List')
            ],

            'msa': [
                main.tr('Stopwords ISO - Malay Stop Words'),
                main.tr('Custom List')
            ],

            'nep': [
                main.tr('NLTK - Nepali Stop Words'),
                main.tr('Custom List')
            ],

            'nob': [
                main.tr('NLTK - Norwegian Bokmål Stop Words'),
                main.tr('spaCy - Norwegian Bokmål Stop Words'),
                main.tr('Stopwords ISO - Norwegian Bokmål Stop Words'),
                main.tr('Custom List')
            ],

            'nno': [
                main.tr('NLTK - Norwegian Nynorsk Stop Words'),
                main.tr('Stopwords ISO - Norwegian Nynorsk Stop Words'),
                main.tr('Custom List')
            ],

            'fas': [
                main.tr('spaCy - Persian Stop Words'),
                main.tr('Stopwords ISO - Persian Stop Words'),
                main.tr('Custom List')
            ],

            'pol': [
                main.tr('spaCy - Polish Stop Words'),
                main.tr('Stopwords ISO - Polish Stop Words'),
                main.tr('Custom List')
            ],

            'por': [
                main.tr('NLTK - Portuguese Stop Words'),
                main.tr('spaCy - Portuguese Stop Words'),
                main.tr('Stopwords ISO - Portuguese Stop Words'),
                main.tr('Custom List')
            ],

            'ron': [
                main.tr('NLTK - Romanian Stop Words'),
                main.tr('spaCy - Romanian Stop Words'),
                main.tr('Stopwords ISO - Romanian Stop Words'),
                main.tr('Custom List')
            ],

            'rus': [
                main.tr('NLTK - Russian Stop Words'),
                main.tr('spaCy - Russian Stop Words'),
                main.tr('Stopwords ISO - Russian Stop Words'),
                main.tr('Custom List')
            ],

            'sin': [
                main.tr('spaCy - Sinhala Stop Words'),
                main.tr('Custom List')
            ],

            'slk': [
                main.tr('Stopwords ISO - Slovak Stop Words'),
                main.tr('Custom List')
            ],

            'slv': [
                main.tr('Stopwords ISO - Slovenian Stop Words'),
                main.tr('Custom List')
            ],

            'sot': [
                main.tr('Stopwords ISO - Sotho (Southern) Stop Words'),
                main.tr('Custom List')
            ],

            'som': [
                main.tr('Stopwords ISO - Somali Stop Words'),
                main.tr('Custom List')
            ],

            'spa': [
                main.tr('NLTK - Spanish Stop Words'),
                main.tr('spaCy - Spanish Stop Words'),
                main.tr('Stopwords ISO - Spanish Stop Words'),
                main.tr('Custom List')
            ],

            'swa': [
                main.tr('Stopwords ISO - Swahili Stop Words'),
                main.tr('Custom List')
            ],

            'swe': [
                main.tr('NLTK - Swedish Stop Words'),
                main.tr('spaCy - Swedish Stop Words'),
                main.tr('Stopwords ISO - Swedish Stop Words'),
                main.tr('Custom List')
            ],

            'tgl': [
                main.tr('Stopwords ISO - Tagalog Stop Words'),
                main.tr('Custom List')
            ],

            'tat': [
                main.tr('spaCy - Tatar Stop Words'),
                main.tr('Custom List')
            ],

            'tel': [
                main.tr('spaCy - Telugu Stop Words'),
                main.tr('Custom List')
            ],

            'tha': [
                main.tr('PyThaiNLP - Thai Stop Words'),
                main.tr('spaCy - Thai Stop Words'),
                main.tr('Stopwords ISO - Thai Stop Words'),
                main.tr('Custom List')
            ],

            'tur': [
                main.tr('NLTK - Turkish Stop Words'),
                main.tr('spaCy - Turkish Stop Words'),
                main.tr('Stopwords ISO - Turkish Stop Words'),
                main.tr('Custom List')
            ],

            'ukr': [
                main.tr('Stopwords ISO - Ukrainian Stop Words'),
                main.tr('Custom List')
            ],

            'urd': [
                main.tr('spaCy - Urdu Stop Words'),
                main.tr('Stopwords ISO - Urdu Stop Words'),
                main.tr('Custom List')
            ],

            'vie': [
                main.tr('spaCy - Vietnamese Stop Words'),
                main.tr('Stopwords ISO - Vietnamese Stop Words'),
                main.tr('Custom List')
            ],

            'yor': [
                main.tr('Stopwords ISO - Yoruba Stop Words'),
                main.tr('Custom List')
            ],

            'zul': [
                main.tr('Stopwords ISO - Zulu Stop Words'),
                main.tr('Custom List')
            ],

            'other': [
                main.tr('Custom List')
            ]
        },

        'measures_dispersion': {
            main.tr('Juilland\'s D'): {
                'col': main.tr('Juilland\'s D'),
                'func': measures_dispersion.juillands_d
            },

            main.tr('Carroll\'s D₂'): {
                'col': main.tr('Carroll\'s D₂'),
                'func': measures_dispersion.carrolls_d2
            },

            main.tr('Lyne\'s D₃'): {
                'col': main.tr('Lyne\'s D₃'),
                'func': measures_dispersion.lynes_d3
            },

            main.tr('Rosengren\'s S'): {
                'col': main.tr('Rosengren\'s S'),
                'func': measures_dispersion.rosengrens_s
            },

            main.tr('Zhang\'s Distributional Consistency'): {
                'col': main.tr('Zhang\'s DC'),
                'func': measures_dispersion.zhangs_distributional_consistency
            },

            main.tr('Gries\'s DP'): {
                'col': main.tr('Gries\'s DP'),
                'func': measures_dispersion.griess_dp
            },

            main.tr('Gries\'s DPₙₒᵣₘ'): {
                'col': main.tr('Gries\'s DPₙₒᵣₘ'),
                'func': measures_dispersion.griess_dp_norm
            }
        },

        'measures_adjusted_freq': {
            main.tr('Juilland\'s U'): {
                'col': main.tr('Juilland\'s U'),
                'func': measures_adjusted_freq.juillands_u
            },

            main.tr('Carroll\'s Uₘ'): {
                'col': main.tr('Carroll\'s Uₘ'),
                'func': measures_adjusted_freq.carrolls_um
            },

            main.tr('Rosengren\'s KF'): {
                'col': main.tr('Rosengren\'s KF'),
                'func': measures_adjusted_freq.rosengrens_kf
            },

            main.tr('Engwall\'s FM'): {
                'col': main.tr('Engwall\'s FM'),
                'func': measures_adjusted_freq.engwalls_fm
            },

            main.tr('Kromer\'s Uᵣ'): {
                'col': main.tr('Kromer\'s Uᵣ'),
                'func': measures_adjusted_freq.kromers_ur
            }
        },

        'tests_significance': {
            'collocation': {
                main.tr('z-score'): {
                    'cols': [
                        main.tr('z-score'),
                        main.tr('p-value'),
                        None
                    ],

                    'func': measures_statistical_significance.z_score
                },

                main.tr('Student\'s t-test (One-sample)'): {
                    'cols': [
                        main.tr('t-statistic'),
                        main.tr('p-value'),
                        None
                    ],

                    'func': measures_statistical_significance.students_t_test_one_sample
                },

                main.tr('Pearson\'s Chi-squared Test'): {
                    'cols': [
                        main.tr('χ2'),
                        main.tr('p-value'),
                        None
                    ],

                    'func': measures_statistical_significance.pearsons_chi_squared_test
                },

                main.tr('Log-likelihood Ratio Test'): {
                    'cols': [
                        main.tr('Log-likelihood Ratio'),
                        main.tr('p-value'),
                        main.tr('Bayes Factor')
                    ],

                    'func': measures_statistical_significance.log_likehood_ratio_test
                },

                main.tr('Fisher\'s Exact Test'): {
                    'cols': [
                        None,
                        main.tr('p-value'),
                        None
                    ],

                    'func': measures_statistical_significance.fishers_exact_test
                }
            },

            'keywords': {
                main.tr('Student\'s t-test (Two-sample)'): {
                    'cols': [
                        main.tr('t-statistic'),
                        main.tr('p-value'),
                        main.tr('Bayes Factor')
                    ],

                    'func': measures_statistical_significance.students_t_test_two_sample
                },

                main.tr('Pearson\'s Chi-squared Test'): {
                    'cols': [
                        main.tr('χ2'),
                        main.tr('p-value'),
                        None
                    ],

                    'func': measures_statistical_significance.pearsons_chi_squared_test
                },


                main.tr('Fisher\'s Exact Test'): {
                    'cols': [
                        None,
                        main.tr('p-value'),
                        None
                    ],

                    'func': measures_statistical_significance.fishers_exact_test
                },

                main.tr('Log-likelihood Ratio Test'): {
                    'cols': [
                        main.tr('Log-likelihood Ratio'),
                        main.tr('p-value'),
                        main.tr('Bayes Factor')
                    ],

                    'func': measures_statistical_significance.log_likehood_ratio_test
                },

                main.tr('Mann-Whitney U Test'): {
                    'cols': [
                        main.tr('U Statistic'),
                        main.tr('p-value'),
                        None
                    ],

                    'func': measures_statistical_significance.mann_whitney_u_test
                }
            }
        },

        'measures_effect_size': {
            'collocation': {
                main.tr('Pointwise Mutual Information'): {
                    'col': main.tr('PMI'),
                    'func': measures_effect_size.pmi
                },

                main.tr('Mutual Dependency'): {
                    'col': main.tr('MD'),
                    'func': measures_effect_size.mutual_dependency
                },

                main.tr('Log-Frequency Biased MD'): {
                    'col': main.tr('LFMD'),
                    'func': measures_effect_size.log_freq_biased_md
                },

                main.tr('Cubic Association Ratio'): {
                    'col': main.tr('Cubic Association Ratio'),
                    'func': measures_effect_size.cubic_association_ratio
                },

                main.tr('MI.log-f'): {
                    'col': main.tr('MI.log-f'),
                    'func': measures_effect_size.mi_lof_f
                },

                main.tr('Mutual Information'): {
                    'col': main.tr('MI'),
                    'func': measures_effect_size.mi
                },

                main.tr('Squared Phi Coefficient'): {
                    'col': main.tr('φ2'),
                    'func': measures_effect_size.squared_phi_coeff
                },

                main.tr('Dice\'s Coefficient'): {
                    'col': main.tr('Dice\'s Coefficient'),
                    'func': measures_effect_size.dices_coeff
                },

                main.tr('logDice'): {
                    'col': main.tr('logDice'),
                    'func': measures_effect_size.log_dice
                },

                main.tr('Mutual Expectation'): {
                    'col': main.tr('Mutual Expectation'),
                    'func': measures_effect_size.mutual_expectation
                },

                main.tr('Jaccard Index'): {
                    'col': main.tr('Jaccard Index'),
                    'func': measures_effect_size.jaccard_index
                },

                main.tr('Minimum Sensitivity'): {
                    'col': main.tr('Minimum Sensitivity'),
                    'func': measures_effect_size.min_sensitivity
                }
            },

            'keywords': {
                main.tr('Kilgarriff\'s Ratio'): {
                    'col': main.tr('Kilgarriff\'s Ratio'),
                    'func': measures_effect_size.kilgarriffs_ratio
                },

                main.tr('Odds Ratio'): {
                    'col': main.tr('Odds Ratio'),
                    'func': measures_effect_size.odds_ratio
                },

                main.tr('Log Ratio'): {
                    'col': main.tr('Log Ratio'),
                    'func': measures_effect_size.log_ratio
                },

                main.tr('Difference Coefficient'): {
                    'col': main.tr('Difference Coefficient'),
                    'func': measures_effect_size.diff_coeff
                },

                main.tr('%DIFF'): {
                    'col': main.tr('%DIFF'),
                    'func': measures_effect_size.pct_diff
                }
            }
        },

        'styles': {
            'style_global': '''
                  font-family: Arial;
                  font-size: 12px;
            ''',

            'style_dialog': '''
                <head>
                    <style>
                        * {
                            outline: none;
                            margin: 0;
                            border: 0;
                            padding: 0;

                            line-height: 1.2;
                            text-align: justify;
                        }

                        div {
                            margin-bottom: 5px;
                        }

                        ul {
                            margin-bottom: 5px;
                        }

                        li {
                            margin-left: -30px;
                        }
                    </style>
                </head>
            ''',

            'style_changelog': '''
                <head>
                    <style>
                        * {
                            outline: none;
                            margin: 0;
                            border: 0;
                            padding: 0;

                            text-align: justify;
                        }

                        ul {
                            line-height: 1.2;
                            margin-bottom: 10px;
                        }

                        li {
                            margin-left: -30px;
                        }
                    </style>
                </head>
            ''',

            'style_hints': '''
                color: #777;
            '''
        }
    }
