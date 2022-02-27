# ----------------------------------------------------------------------
# Wordless: Settings - Global Settings
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

from wl_measures import (
    wl_measures_adjusted_freq,
    wl_measures_dispersion,
    wl_measures_effect_size,
    wl_measures_statistical_significance
)

def init_settings_global(main):
    main.settings_global = {
        'langs': {
            main.tr('Afrikaans'):               ['afr', 'af', 'Indo-European'],
            main.tr('Akkadian'):                ['akk', 'akk', 'Afro-Asiatic'],
            main.tr('Albanian'):                ['sqi', 'sq', 'Indo-European'],
            main.tr('Amharic'):                 ['amh', 'am', 'Afro-Asiatic'],
            main.tr('Arabic'):                  ['ara', 'ar', 'Afro-Asiatic'],
            main.tr('Arabic (Standard)'):       ['arb', 'arb', 'Afro-Asiatic'],
            main.tr('Armenian'):                ['hye', 'hy', 'Indo-European'],
            main.tr('Assamese'):                ['asm', 'as', 'Indo-European'],
            main.tr('Asturian'):                ['ast', 'ast', 'Indo-European'],
            main.tr('Azerbaijani'):             ['aze', 'az', 'Turkic'],
            main.tr('Basque'):                  ['eus', 'eu', 'Language isolate'],
            main.tr('Belarusian'):              ['bel', 'be', 'Indo-European'],
            main.tr('Bengali'):                 ['ben', 'bn', 'Indo-European'],
            main.tr('Breton'):                  ['bre', 'br', 'Indo-European'],
            main.tr('Bulgarian'):               ['bul', 'bg', 'Indo-European'],
            main.tr('Catalan'):                 ['cat', 'ca', 'Indo-European'],
            main.tr('Chinese (Simplified)'):    ['zho_cn', 'zh_cn', 'Sino-Tibetan'],
            main.tr('Chinese (Traditional)'):   ['zho_tw', 'zh_tw', 'Sino-Tibetan'],
            main.tr('Coptic'):                  ['cop', 'cop', 'Unclassified'],
            main.tr('Croatian'):                ['hrv', 'hr', 'Indo-European'],
            main.tr('Czech'):                   ['ces', 'cs', 'Indo-European'],
            main.tr('Danish'):                  ['dan', 'da', 'Indo-European'],
            main.tr('Dutch'):                   ['nld', 'nl', 'Indo-European'],
            main.tr('English (Middle)'):        ['enm', 'enm', 'Indo-European'],
            main.tr('English (Old)'):           ['ang', 'ang', 'Indo-European'],
            main.tr('English (United Kingdom)'):['eng_gb', 'en_gb', 'Indo-European'],
            main.tr('English (United States)'): ['eng_us', 'en_us', 'Indo-European'],
            main.tr('Esperanto'):               ['epo', 'eo', 'Constructed'],
            main.tr('Estonian'):                ['est', 'et', 'Uralic'],
            main.tr('Finnish'):                 ['fin', 'fi', 'Uralic'],
            main.tr('French'):                  ['fra', 'fr', 'Indo-European'],
            main.tr('French (Old)'):            ['fro', 'fro', 'Indo-European'],
            main.tr('Galician'):                ['glg', 'gl', 'Indo-European'],
            main.tr('German (Austria)'):        ['deu_at', 'de_at', 'Indo-European'],
            main.tr('German (Germany)'):        ['deu_de', 'de_de', 'Indo-European'],
            main.tr('German (Middle High)'):    ['gmh', 'gmh', 'Unclassified'],
            main.tr('German (Switzerland)'):    ['deu_ch', 'de_ch', 'Indo-European'],
            main.tr('Greek (Ancient)'):         ['grc', 'grc', 'Unclassified'],
            main.tr('Greek (Modern)'):          ['ell', 'el', 'Indo-European'],
            main.tr('Gujarati'):                ['guj', 'gu', 'Indo-European'],
            main.tr('Hausa'):                   ['hau', 'ha', 'Afro-Asiatic'],
            main.tr('Hebrew'):                  ['heb', 'he', 'Afro-Asiatic'],
            main.tr('Hindi'):                   ['hin', 'hi', 'Indo-European'],
            main.tr('Hungarian'):               ['hun', 'hu', 'Uralic'],
            main.tr('Icelandic'):               ['isl', 'is', 'Indo-European'],
            main.tr('Indonesian'):              ['ind', 'id', 'Austronesian'],
            main.tr('Irish'):                   ['gle', 'ga', 'Indo-European'],
            main.tr('Italian'):                 ['ita', 'it', 'Indo-European'],
            main.tr('Japanese'):                ['jpn', 'ja', 'Japonic'],
            main.tr('Kannada'):                 ['kan', 'kn', 'Dravidian'],
            main.tr('Kazakh'):                  ['kaz', 'kk', 'Turkic'],
            main.tr('Korean'):                  ['kor', 'ko', 'Koreanic'],
            main.tr('Kurdish'):                 ['kur', 'ku', 'Indo-European'],
            main.tr('Kyrgyz'):                  ['kir', 'ky', 'Turkic'],
            main.tr('Latin'):                   ['lat', 'la', 'Indo-European'],
            main.tr('Latvian'):                 ['lav', 'lv', 'Indo-European'],
            main.tr('Ligurian'):                ['lij', 'lij', 'Unclassified'],
            main.tr('Lithuanian'):              ['lit', 'lt', 'Indo-European'],
            main.tr('Luxembourgish'):           ['ltz', 'lb', 'Indo-European'],
            main.tr('Macedonian'):              ['mkd', 'mk', 'Indo-European'],
            main.tr('Malay'):                   ['msa', 'ms', 'Austronesian'],
            main.tr('Malayalam'):               ['mal', 'ml', 'Dravidian'],
            main.tr('Manx'):                    ['glv', 'gv', 'Indo-European'],
            main.tr('Marathi'):                 ['mar', 'mr', 'Indo-European'],
            main.tr('Marathi (Old)'):           ['omr', 'omr', 'Unclassified'],
            main.tr('Meitei'):                  ['mni', 'mni', 'Sino-Tibetan'],
            main.tr('Mongolian'):               ['mon', 'mn', 'Mongolic'],
            main.tr('Nepali'):                  ['nep', 'ne', 'Indo-European'],
            main.tr('Norse (Old)'):             ['non', 'non', 'Indo-European'],
            main.tr('Norwegian Bokmål'):        ['nob', 'nb', 'Indo-European'],
            main.tr('Norwegian Nynorsk'):       ['nno', 'nn', 'Indo-European'],
            main.tr('Oriya'):                   ['ori', 'or', 'Indo-European'],
            main.tr('Persian'):                 ['fas', 'fa', 'Indo-European'],
            main.tr('Polish'):                  ['pol', 'pl', 'Indo-European'],
            main.tr('Portuguese (Brazil)'):     ['por_br', 'pt_br', 'Indo-European'],
            main.tr('Portuguese (Portugal)'):   ['por_pt', 'pt_pt', 'Indo-European'],
            main.tr('Punjabi'):                 ['pan', 'pa', 'Indo-European'],
            main.tr('Romanian'):                ['ron', 'ro', 'Indo-European'],
            main.tr('Russian'):                 ['rus', 'ru', 'Indo-European'],
            main.tr('Sanskrit'):                ['san', 'sa', 'Indo-European'],
            main.tr('Scottish Gaelic'):         ['gla', 'gd', 'Indo-European'],
            main.tr('Serbian (Cyrillic)'):      ['srp_cyrl', 'sr_cyrl', 'Indo-European'],
            main.tr('Serbian (Latin)'):         ['srp_latn', 'sr_latn', 'Indo-European'],
            main.tr('Sinhala'):                 ['sin', 'si', 'Indo-European'],
            main.tr('Slovak'):                  ['slk', 'sk', 'Indo-European'],
            main.tr('Slovenian'):               ['slv', 'sl', 'Indo-European'],
            main.tr('Somali'):                  ['som', 'so', 'Afro-Asiatic'],
            main.tr('Sotho (Southern)'):        ['sot', 'st', 'Niger-Congo'],
            main.tr('Spanish'):                 ['spa', 'es', 'Indo-European'],
            main.tr('Swahili'):                 ['swa', 'sw', 'Niger-Congo'],
            main.tr('Swedish'):                 ['swe', 'sv', 'Indo-European'],
            main.tr('Tagalog'):                 ['tgl', 'tl', 'Austronesian'],
            main.tr('Tajik'):                   ['tgk', 'tg', 'Indo-European'],
            main.tr('Tamil'):                   ['tam', 'ta', 'Dravidian'],
            main.tr('Tatar'):                   ['tat', 'tt', 'Turkic'],
            main.tr('Telugu'):                  ['tel', 'te', 'Dravidian'],
            main.tr('Tetun Dili'):              ['tdt', 'tdt', 'Unclassified'],
            main.tr('Thai'):                    ['tha', 'th', 'Tai-Kadai'],
            main.tr('Tibetan'):                 ['bod', 'bo', 'Sino-Tibetan'],
            main.tr('Tigrinya'):                ['tir', 'ti', 'Afro-Asiatic'],
            main.tr('Tswana'):                  ['tsn', 'tn', 'Niger-Congo'],
            main.tr('Turkish'):                 ['tur', 'tr', 'Turkic'],
            main.tr('Ukrainian'):               ['ukr', 'uk', 'Indo-European'],
            main.tr('Urdu'):                    ['urd', 'ur', 'Indo-European'],
            main.tr('Vietnamese'):              ['vie', 'vi', 'Austroasiatic'],
            main.tr('Welsh'):                   ['cym', 'cy', 'Indo-European'],
            main.tr('Yoruba'):                  ['yor', 'yo', 'Niger-Congo'],
            main.tr('Zulu'):                    ['zul', 'zu', 'Niger-Congo'],

            main.tr('Other Languages'):         ['other', 'other', 'Unclassified']
        },

        'encodings': {
            main.tr('All Languages (UTF-8 without BOM)'): 'utf_8',
            main.tr('All Languages (UTF-8 with BOM)'): 'utf_8_sig',
            main.tr('All Languages (UTF-16 with BOM)'): 'utf_16',
            main.tr('All Languages (UTF-16BE without BOM)'): 'utf_16_be',
            main.tr('All Languages (UTF-16LE without BOM)'): 'utf_16_le',
            main.tr('All Languages (UTF-32 with BOM)'): 'utf_32',
            main.tr('All Languages (UTF-32BE without BOM)'): 'utf_32_be',
            main.tr('All Languages (UTF-32LE without BOM)'): 'utf_32_le',
            main.tr('All Languages (UTF-7)'): 'utf_7',

            main.tr('Arabic (CP720)'): 'cp720',
            main.tr('Arabic (CP864)'): 'cp864',
            main.tr('Arabic (ISO-8859-6)'): 'iso8859_6',
            main.tr('Arabic (Mac OS Arabic)'): 'mac_arabic',
            main.tr('Arabic (Windows-1256)'): 'cp1256',

            main.tr('Baltic Languages (CP775)'): 'cp775',
            main.tr('Baltic Languages (ISO-8859-13)'): 'iso8859_13',
            main.tr('Baltic Languages (Windows-1257)'): 'cp1257',

            main.tr('Celtic Languages (ISO-8859-14)'): 'iso8859_14',

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

            main.tr('European (HP Roman-8)'): 'hp_roman8',

            main.tr('European (Central) (CP852)'): 'cp852',
            main.tr('European (Central) (ISO-8859-2)'): 'iso8859_2',
            main.tr('European (Central) (Mac OS Central European)'): 'mac_latin2',
            main.tr('European (Central) (Windows-1250)'): 'cp1250',

            main.tr('European (Northern) (ISO-8859-4)'): 'iso8859_4',

            main.tr('European (Southern) (ISO-8859-3)'): 'iso8859_3',
            main.tr('European (South-Eastern) (ISO-8859-16)'): 'iso8859_16',

            main.tr('European (Western) (EBCDIC 500)'): 'cp500',
            main.tr('European (Western) (CP850)'): 'cp850',
            main.tr('European (Western) (CP858)'): 'cp858',
            main.tr('European (Western) (CP1140)'): 'cp1140',
            main.tr('European (Western) (ISO-8859-1)'): 'latin_1',
            main.tr('European (Western) (ISO-8859-15)'): 'iso8859_15',
            main.tr('European (Western) (Mac OS Roman)'): 'mac_roman',
            main.tr('European (Western) (Windows-1252)'): 'windows_1252',

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
            main.tr('Korean (UHC)'): 'cp949',

            main.tr('Nordic Languages (CP865)'): 'cp865',
            main.tr('Nordic Languages (ISO-8859-10)'): 'iso8859_10',

            main.tr('Persian/Urdu (Mac OS Farsi)'): 'mac_farsi',

            main.tr('Portuguese (CP860)'): 'cp860',

            main.tr('Romanian (Mac OS Romanian)'): 'mac_romanian',

            main.tr('Russian (KOI8-R)'): 'koi8_r',

            main.tr('Tajik (KOI8-T)'): 'koi8_t',

            main.tr('Thai (CP874)'): 'cp874',
            main.tr('Thai (ISO-8859-11)'): 'iso8859_11',

            main.tr('Turkish (CP857)'): 'cp857',
            main.tr('Turkish (EBCDIC 1026)'): 'cp1026',
            main.tr('Turkish (ISO-8859-9)'): 'iso8859_9',
            main.tr('Turkish (Mac OS Turkish)'): 'mac_turkish',
            main.tr('Turkish (Windows-1254)'): 'cp1254',

            main.tr('Ukrainian (CP1125)'): 'cp1125',
            main.tr('Ukrainian (KOI8-U)'): 'koi8_u',

            main.tr('Urdu (CP1006)'): 'cp1006',

            main.tr('Vietnamese (CP1258)'): 'cp1258',
        },

        'file_types': {
            'files': [
                main.tr('CSV File(*.csv)'),
                main.tr('Excel Workbook (*.xlsx)'),
                main.tr('HTML Page (*.htm; *.html)'),
                main.tr('Text File (*.txt)'),
                main.tr('Translation Memory File (*.tmx)'),
                main.tr('Word Document (*.docx)'),
                main.tr('XML File (*.xml)'),
                main.tr('All Files (*.*)')
            ],

            'exp_tables': [
                main.tr('CSV File (*.csv)'),
                main.tr('Excel Workbook (*.xlsx)')
            ],

            'exp_tables_concordancer': [
                main.tr('CSV File (*.csv)'),
                main.tr('Excel Workbook (*.xlsx)'),
                main.tr('Word Document (*.docx)')
            ]
        },

        'lang_util_mappings': {
            'sentence_tokenizers': {
                main.tr('botok - Tibetan Sentence Tokenizer'): 'botok_bod',
                main.tr('NLTK - Punkt Sentence Tokenizer'): 'nltk_punkt',
                main.tr('PyThaiNLP - CRFCut'): 'pythainlp_crfcut',

                main.tr('spaCy - Sentence Recognizer'): 'spacy_sentence_recognizer',
                main.tr('spaCy - Sentencizer'): 'spacy_sentencizer',

                main.tr('Tokenizer - Icelandic Sentence Tokenizer'): 'tokenizer_isl',
                main.tr('Underthesea - Vietnamese Sentence Tokenizer'): 'underthesea_vie',

                main.tr('Wordless - Chinese Sentence Tokenizer'): 'wordless_zho',
                main.tr('Wordless - Japanese Sentence Tokenizer'): 'wordless_jpn'
            },

            'word_tokenizers': {
                main.tr('botok - Tibetan Word Tokenizer'): 'botok_bod',
                main.tr('jieba - Chinese Word Tokenizer'): 'jieba_zho',
                main.tr('nagisa - Japanese Word Tokenizer'): 'nagisa_jpn',

                main.tr('NLTK - NIST Tokenizer'): 'nltk_nist',
                main.tr('NLTK - NLTK Tokenizer'): 'nltk_nltk',
                main.tr('NLTK - Penn Treebank Tokenizer'): 'nltk_penn_treebank',
                main.tr('NLTK - Tok-tok Tokenizer'): 'nltk_tok_tok',
                main.tr('NLTK - Twitter Tokenizer'): 'nltk_twitter',

                main.tr('pkuseg - Chinese Word Tokenizer'): 'pkuseg_zho',

                main.tr('PyThaiNLP - Longest Matching'): 'pythainlp_longest_matching',
                main.tr('PyThaiNLP - Maximum Matching'): 'pythainlp_max_matching',
                main.tr('PyThaiNLP - Maximum Matching + TCC'): 'pythainlp_max_matching_tcc',
                main.tr('PyThaiNLP - Maximum Matching + TCC (Safe Mode)'): 'pythainlp_max_matching_tcc_safe_mode',
                main.tr('PyThaiNLP - NERCut'): 'pythainlp_nercut',

                main.tr('Sacremoses - Moses Tokenizer'): 'sacremoses_moses',

                main.tr('spaCy - Afrikaans Word Tokenizer'): 'spacy_afr',
                main.tr('spaCy - Albanian Word Tokenizer'): 'spacy_sqi',
                main.tr('spaCy - Amharic Word Tokenizer'): 'spacy_amh',
                main.tr('spaCy - Arabic Word Tokenizer'): 'spacy_ara',
                main.tr('spaCy - Armenian Word Tokenizer'): 'spacy_hye',
                main.tr('spaCy - Azerbaijani Word Tokenizer'): 'spacy_aze',
                main.tr('spaCy - Basque Word Tokenizer'): 'spacy_eus',
                main.tr('spaCy - Bengali Word Tokenizer'): 'spacy_ben',
                main.tr('spaCy - Bulgarian Word Tokenizer'): 'spacy_bul',
                main.tr('spaCy - Catalan Word Tokenizer'): 'spacy_cat',
                main.tr('spaCy - Chinese Word Tokenizer'): 'spacy_zho',
                main.tr('spaCy - Croatian Word Tokenizer'): 'spacy_hrv',
                main.tr('spaCy - Czech Word Tokenizer'): 'spacy_ces',
                main.tr('spaCy - Danish Word Tokenizer'): 'spacy_dan',
                main.tr('spaCy - Dutch Word Tokenizer'): 'spacy_nld',
                main.tr('spaCy - English Word Tokenizer'): 'spacy_eng',
                main.tr('spaCy - Estonian Word Tokenizer'): 'spacy_est',
                main.tr('spaCy - Finnish Word Tokenizer'): 'spacy_fin',
                main.tr('spaCy - French Word Tokenizer'): 'spacy_fra',
                main.tr('spaCy - German Word Tokenizer'): 'spacy_deu',
                main.tr('spaCy - Greek (Ancient) Word Tokenizer'): 'spacy_grc',
                main.tr('spaCy - Greek (Modern) Word Tokenizer'): 'spacy_ell',
                main.tr('spaCy - Gujarati Word Tokenizer'): 'spacy_guj',
                main.tr('spaCy - Hebrew Word Tokenizer'): 'spacy_heb',
                main.tr('spaCy - Hindi Word Tokenizer'): 'spacy_hin',
                main.tr('spaCy - Hungarian Word Tokenizer'): 'spacy_hun',
                main.tr('spaCy - Icelandic Word Tokenizer'): 'spacy_isl',
                main.tr('spaCy - Indonesian Word Tokenizer'): 'spacy_ind',
                main.tr('spaCy - Irish Word Tokenizer'): 'spacy_gle',
                main.tr('spaCy - Italian Word Tokenizer'): 'spacy_ita',
                main.tr('spaCy - Japanese Word Tokenizer'): 'spacy_jpn',
                main.tr('spaCy - Kannada Word Tokenizer'): 'spacy_kan',
                main.tr('spaCy - Kyrgyz Word Tokenizer'): 'spacy_kir',
                main.tr('spaCy - Latvian Word Tokenizer'): 'spacy_lav',
                main.tr('spaCy - Ligurian Word Tokenizer'): 'spacy_lij',
                main.tr('spaCy - Lithuanian Word Tokenizer'): 'spacy_lit',
                main.tr('spaCy - Luxembourgish Word Tokenizer'): 'spacy_ltz',
                main.tr('spaCy - Macedonian Word Tokenizer'): 'spacy_mkd',
                main.tr('spaCy - Malayalam Word Tokenizer'): 'spacy_mal',
                main.tr('spaCy - Marathi Word Tokenizer'): 'spacy_mar',
                main.tr('spaCy - Nepali Word Tokenizer'): 'spacy_nep',
                main.tr('spaCy - Norwegian Word Tokenizer'): 'spacy_nob',
                main.tr('spaCy - Persian Word Tokenizer'): 'spacy_fas',
                main.tr('spaCy - Polish Word Tokenizer'): 'spacy_pol',
                main.tr('spaCy - Portuguese Word Tokenizer'): 'spacy_por',
                main.tr('spaCy - Romanian Word Tokenizer'): 'spacy_ron',
                main.tr('spaCy - Russian Word Tokenizer'): 'spacy_rus',
                main.tr('spaCy - Sanskrit Word Tokenizer'): 'spacy_san',
                main.tr('spaCy - Serbian Word Tokenizer'): 'spacy_srp',
                main.tr('spaCy - Sinhala Word Tokenizer'): 'spacy_sin',
                main.tr('spaCy - Slovak Word Tokenizer'): 'spacy_slk',
                main.tr('spaCy - Slovenian Word Tokenizer'): 'spacy_slv',
                main.tr('spaCy - Spanish Word Tokenizer'): 'spacy_spa',
                main.tr('spaCy - Swedish Word Tokenizer'): 'spacy_swe',
                main.tr('spaCy - Tagalog Word Tokenizer'): 'spacy_tgl',
                main.tr('spaCy - Tamil Word Tokenizer'): 'spacy_tam',
                main.tr('spaCy - Tatar Word Tokenizer'): 'spacy_tat',
                main.tr('spaCy - Telugu Word Tokenizer'): 'spacy_tel',
                main.tr('spaCy - Tigrinya Word Tokenizer'): 'spacy_tir',
                main.tr('spaCy - Tswana Word Tokenizer'): 'spacy_tsn',
                main.tr('spaCy - Turkish Word Tokenizer'): 'spacy_tur',
                main.tr('spaCy - Ukrainian Word Tokenizer'): 'spacy_ukr',
                main.tr('spaCy - Urdu Word Tokenizer'): 'spacy_urd',
                main.tr('spaCy - Yoruba Word Tokenizer'): 'spacy_yor',

                main.tr('SudachiPy - Japanese Word Tokenizer (Split Mode A)'): 'sudachipy_jpn_split_mode_a',
                main.tr('SudachiPy - Japanese Word Tokenizer (Split Mode B)'): 'sudachipy_jpn_split_mode_b',
                main.tr('SudachiPy - Japanese Word Tokenizer (Split Mode C)'): 'sudachipy_jpn_split_mode_c',

                main.tr('Tokenizer - Icelandic Word Tokenizer'): 'tokenizer_isl',
                main.tr('Underthesea - Vietnamese Word Tokenizer'): 'underthesea_vie',

                main.tr('Wordless - Chinese Character Tokenizer'): 'wordless_zho_char',
                main.tr('Wordless - Japanese Kanji Tokenizer'): 'wordless_jpn_kanji'
            },

            'syl_tokenizers': {
                main.tr('Pyphen - Afrikaans Syllable Tokenizer'): 'pyphen_afr',
                main.tr('Pyphen - Albanian Syllable Tokenizer'): 'pyphen_sqi',
                main.tr('Pyphen - Belarusian Syllable Tokenizer'): 'pyphen_bel',
                main.tr('Pyphen - Bulgarian Syllable Tokenizer'): 'pyphen_bul',
                main.tr('Pyphen - Croatian Syllable Tokenizer'): 'pyphen_hrv',
                main.tr('Pyphen - Czech Syllable Tokenizer'): 'pyphen_ces',
                main.tr('Pyphen - Danish Syllable Tokenizer'): 'pyphen_dan',
                main.tr('Pyphen - Dutch Syllable Tokenizer'): 'pyphen_nld',
                main.tr('Pyphen - English (United Kingdom) Syllable Tokenizer'): 'pyphen_eng_gb',
                main.tr('Pyphen - English (United States) Syllable Tokenizer'): 'pyphen_eng_us',
                main.tr('Pyphen - Esporanto Syllable Tokenizer'): 'pyphen_epo',
                main.tr('Pyphen - Estonian Syllable Tokenizer'): 'pyphen_est',
                main.tr('Pyphen - French Syllable Tokenizer'): 'pyphen_fra',
                main.tr('Pyphen - Galician Syllable Tokenizer'): 'pyphen_glg',
                main.tr('Pyphen - German (Austria) Syllable Tokenizer'): 'pyphen_deu_at',
                main.tr('Pyphen - German (Germany) Syllable Tokenizer'): 'pyphen_deu_de',
                main.tr('Pyphen - German (Switzerland) Syllable Tokenizer'): 'pyphen_deu_ch',
                main.tr('Pyphen - Greek (Modern) Syllable Tokenizer'): 'pyphen_ell',
                main.tr('Pyphen - Hungarian Syllable Tokenizer'): 'pyphen_hun',
                main.tr('Pyphen - Icelandic Syllable Tokenizer'): 'pyphen_isl',
                main.tr('Pyphen - Indonesian Syllable Tokenizer'): 'pyphen_ind',
                main.tr('Pyphen - Italian Syllable Tokenizer'): 'pyphen_ita',
                main.tr('Pyphen - Lithuanian Syllable Tokenizer'): 'pyphen_lit',
                main.tr('Pyphen - Latvian Syllable Tokenizer'): 'pyphen_lav',
                main.tr('Pyphen - Mongolian Syllable Tokenizer'): 'pyphen_mon',
                main.tr('Pyphen - Norwegian Bokmål Syllable Tokenizer'): 'pyphen_nob',
                main.tr('Pyphen - Norwegian Nynorsk Syllable Tokenizer'): 'pyphen_nno',
                main.tr('Pyphen - Polish Syllable Tokenizer'): 'pyphen_pol',
                main.tr('Pyphen - Portuguese (Brazil) Syllable Tokenizer'): 'pyphen_por_br',
                main.tr('Pyphen - Portuguese (Portugal) Syllable Tokenizer'): 'pyphen_por_pt',
                main.tr('Pyphen - Romanian Syllable Tokenizer'): 'pyphen_ron',
                main.tr('Pyphen - Russian Syllable Tokenizer'): 'pyphen_rus',
                main.tr('Pyphen - Serbian (Cyrillic) Syllable Tokenizer'): 'pyphen_srp_cyrl',
                main.tr('Pyphen - Serbian (Latin) Syllable Tokenizer'): 'pyphen_srp_latn',
                main.tr('Pyphen - Slovak Syllable Tokenizer'): 'pyphen_slk',
                main.tr('Pyphen - Slovenian Syllable Tokenizer'): 'pyphen_slv',
                main.tr('Pyphen - Spanish Syllable Tokenizer'): 'pyphen_spa',
                main.tr('Pyphen - Swedish Syllable Tokenizer'): 'pyphen_swe',
                main.tr('Pyphen - Telugu Syllable Tokenizer'): 'pyphen_tel',
                main.tr('Pyphen - Ukrainian Syllable Tokenizer'): 'pyphen_ukr',
                main.tr('Pyphen - Zulu Syllable Tokenizer'): 'pyphen_zul',

                main.tr('PyThaiNLP - Thai Syllable Tokenizer'): 'pythainlp_tha',
                main.tr('ssg - Thai Syllable Tokenizer'): 'ssg_tha'
            },

            'pos_taggers': {
                main.tr('botok - Tibetan POS Tagger'): 'botok_bod',
                main.tr('jieba - Chinese POS Tagger'): 'jieba_zho',
                main.tr('nagisa - Japanese POS Tagger'): 'nagisa_jpn',
                main.tr('NLTK - Perceptron POS Tagger'): 'nltk_perceptron',
                main.tr('pymorphy2 - Morphological Analyzer'): 'pymorphy2_morphological_analyzer',

                main.tr('PyThaiNLP - Perceptron POS Tagger (LST20)'): 'pythainlp_perceptron_lst20',
                main.tr('PyThaiNLP - Perceptron POS Tagger (ORCHID)'): 'pythainlp_perceptron_orchid',
                main.tr('PyThaiNLP - Perceptron POS Tagger (PUD)'): 'pythainlp_perceptron_pud',

                main.tr('spaCy - Catalan POS Tagger'): 'spacy_cat',
                main.tr('spaCy - Chinese POS Tagger'): 'spacy_zho',
                main.tr('spaCy - Danish POS Tagger'): 'spacy_dan',
                main.tr('spaCy - Dutch POS Tagger'): 'spacy_nld',
                main.tr('spaCy - English POS Tagger'): 'spacy_eng',
                main.tr('spaCy - French POS Tagger'): 'spacy_fra',
                main.tr('spaCy - German POS Tagger'): 'spacy_deu',
                main.tr('spaCy - Greek (Modern) POS Tagger'): 'spacy_ell',
                main.tr('spaCy - Italian POS Tagger'): 'spacy_ita',
                main.tr('spaCy - Japanese POS Tagger'): 'spacy_jpn',
                main.tr('spaCy - Lithuanian POS Tagger'): 'spacy_lit',
                main.tr('spaCy - Macedonian POS Tagger'): 'spacy_mkd',
                main.tr('spaCy - Norwegian Bokmål POS Tagger'): 'spacy_nob',
                main.tr('spaCy - Polish POS Tagger'): 'spacy_pol',
                main.tr('spaCy - Portuguese POS Tagger'): 'spacy_por',
                main.tr('spaCy - Romanian POS Tagger'): 'spacy_ron',
                main.tr('spaCy - Russian POS Tagger'): 'spacy_rus',
                main.tr('spaCy - Spanish POS Tagger'): 'spacy_spa',

                main.tr('SudachiPy - Japanese POS Tagger'): 'sudachipy_jpn',

                main.tr('Underthesea - Vietnamese POS Tagger'): 'underthesea_vie'
            },

            'lemmatizers': {
                main.tr('botok - Tibetan Lemmatizer'): 'botok_bod',

                main.tr('Lemmatization Lists - Asturian Lemma List'): 'lemmatization_lists_ast',
                main.tr('Lemmatization Lists - Bulgarian Lemma List'): 'lemmatization_lists_bul',
                main.tr('Lemmatization Lists - Catalan Lemma List'): 'lemmatization_lists_cat',
                main.tr('Lemmatization Lists - Czech Lemma List'): 'lemmatization_lists_ces',
                main.tr('Lemmatization Lists - English Lemma List'): 'lemmatization_lists_eng',
                main.tr('Lemmatization Lists - Estonian Lemma List'): 'lemmatization_lists_est',
                main.tr('Lemmatization Lists - French Lemma List'): 'lemmatization_lists_fra',
                main.tr('Lemmatization Lists - Galician Lemma List'): 'lemmatization_lists_glg',
                main.tr('Lemmatization Lists - German Lemma List'): 'lemmatization_lists_deu',
                main.tr('Lemmatization Lists - Hungarian Lemma List'): 'lemmatization_lists_hun',
                main.tr('Lemmatization Lists - Irish Lemma List'): 'lemmatization_lists_gle',
                main.tr('Lemmatization Lists - Italian Lemma List'): 'lemmatization_lists_ita',
                main.tr('Lemmatization Lists - Manx Lemma List'): 'lemmatization_lists_glv',
                main.tr('Lemmatization Lists - Persian Lemma List'): 'lemmatization_lists_fas',
                main.tr('Lemmatization Lists - Portuguese Lemma List'): 'lemmatization_lists_por',
                main.tr('Lemmatization Lists - Romanian Lemma List'): 'lemmatization_lists_ron',
                main.tr('Lemmatization Lists - Russian Lemma List'): 'lemmatization_lists_rus',
                main.tr('Lemmatization Lists - Scottish Gaelic Lemma List'): 'lemmatization_lists_gla',
                main.tr('Lemmatization Lists - Slovak Lemma List'): 'lemmatization_lists_slk',
                main.tr('Lemmatization Lists - Slovenian Lemma List'): 'lemmatization_lists_slv',
                main.tr('Lemmatization Lists - Spanish Lemma List'): 'lemmatization_lists_spa',
                main.tr('Lemmatization Lists - Swedish Lemma List'): 'lemmatization_lists_swe',
                main.tr('Lemmatization Lists - Ukrainian Lemma List'): 'lemmatization_lists_ukr',
                main.tr('Lemmatization Lists - Welsh Lemma List'): 'lemmatization_lists_cym',

                main.tr('NLTK - WordNet Lemmatizer'): 'nltk_wordnet',
                main.tr('pymorphy2 - Morphological Analyzer'): 'pymorphy2_morphological_analyzer',

                main.tr('spaCy - Bengali Lemmatizer'): 'spacy_ben',
                main.tr('spaCy - Catalan Lemmatizer'): 'spacy_cat',
                main.tr('spaCy - Croatian Lemmatizer'): 'spacy_hrv',
                main.tr('spaCy - Czech Lemmatizer'): 'spacy_ces',
                main.tr('spaCy - Danish Lemmatizer'): 'spacy_dan',
                main.tr('spaCy - Dutch Lemmatizer'): 'spacy_nld',
                main.tr('spaCy - English Lemmatizer'): 'spacy_eng',
                main.tr('spaCy - French Lemmatizer'): 'spacy_fra',
                main.tr('spaCy - German Lemmatizer'): 'spacy_deu',
                main.tr('spaCy - Greek (Ancient) Lemmatizer'): 'spacy_grc',
                main.tr('spaCy - Greek (Modern) Lemmatizer'): 'spacy_ell',
                main.tr('spaCy - Hungarian Lemmatizer'): 'spacy_hun',
                main.tr('spaCy - Indonesian Lemmatizer'): 'spacy_ind',
                main.tr('spaCy - Irish Lemmatizer'): 'spacy_gle',
                main.tr('spaCy - Italian Lemmatizer'): 'spacy_ita',
                main.tr('spaCy - Japanese Lemmatizer'): 'spacy_jpn',
                main.tr('spaCy - Lithuanian Lemmatizer'): 'spacy_lit',
                main.tr('spaCy - Luxembourgish Lemmatizer'): 'spacy_ltz',
                main.tr('spaCy - Macedonian Lemmatizer'): 'spacy_mkd',
                main.tr('spaCy - Norwegian Bokmål Lemmatizer'): 'spacy_nob',
                main.tr('spaCy - Persian Lemmatizer'): 'spacy_fas',
                main.tr('spaCy - Polish Lemmatizer'): 'spacy_pol',
                main.tr('spaCy - Portuguese Lemmatizer'): 'spacy_por',
                main.tr('spaCy - Romanian Lemmatizer'): 'spacy_ron',
                main.tr('spaCy - Russian Lemmatizer'): 'spacy_rus',
                main.tr('spaCy - Serbian (Cyrillic) Lemmatizer'): 'spacy_srp_cyrl',
                main.tr('spaCy - Spanish Lemmatizer'): 'spacy_spa',
                main.tr('spaCy - Swedish Lemmatizer'): 'spacy_swe',
                main.tr('spaCy - Tagalog Lemmatizer'): 'spacy_tgl',
                main.tr('spaCy - Turkish Lemmatizer'): 'spacy_tur',
                main.tr('spaCy - Urdu Lemmatizer'): 'spacy_urd',

                main.tr('SudachiPy - Japanese Lemmatizer'): 'sudachipy_jpn'
            },

            'stop_word_lists': {
                main.tr('Custom List'): 'custom',
                main.tr('CLTK - Akkadian Stop Word List'): 'cltk_akk',
                main.tr('CLTK - Arabic (Standard) Stop Word List'): 'cltk_arb',
                main.tr('CLTK - Coptic Stop Word List'): 'cltk_cop',
                main.tr('CLTK - English (Middle) Stop Word List'): 'cltk_enm',
                main.tr('CLTK - English (Old) Stop Word List'): 'cltk_ang',
                main.tr('CLTK - French (Old) Stop Word List'): 'cltk_fro',
                main.tr('CLTK - German (Middle High) Stop Word List'): 'cltk_gmh',
                main.tr('CLTK - Greek (Ancient) Stop Word List'): 'cltk_grc',
                main.tr('CLTK - Hindi Stop Word List'): 'cltk_hin',
                main.tr('CLTK - Latin Stop Word List'): 'cltk_lat',
                main.tr('CLTK - Marathi (Old) Stop Word List'): 'cltk_omr',
                main.tr('CLTK - Norse (Old) Stop Word List'): 'cltk_non',
                main.tr('CLTK - Punjabi Stop Word List'): 'cltk_pan',
                main.tr('CLTK - Sanskrit Stop Word List'): 'cltk_san',

                main.tr('extra-stopwords - Albanian Stop Word List'): 'extra_stopwords_sqi',
                main.tr('extra-stopwords - Arabic Stop Word List'): 'extra_stopwords_ara',
                main.tr('extra-stopwords - Armenian Stop Word List'): 'extra_stopwords_hye',
                main.tr('extra-stopwords - Basque Stop Word List'): 'extra_stopwords_eus',
                main.tr('extra-stopwords - Belarusian Stop Word List'): 'extra_stopwords_bel',
                main.tr('extra-stopwords - Bengali Stop Word List'): 'extra_stopwords_ben',
                main.tr('extra-stopwords - Bulgarian Stop Word List'): 'extra_stopwords_bul',
                main.tr('extra-stopwords - Catalan Stop Word List'): 'extra_stopwords_cat',
                main.tr('extra-stopwords - Chinese (Simplified) Stop Word List'): 'extra_stopwords_zho_cn',
                main.tr('extra-stopwords - Chinese (Traditional) Stop Word List'): 'extra_stopwords_zho_tw',
                main.tr('extra-stopwords - Croatian Stop Word List'): 'extra_stopwords_hrv',
                main.tr('extra-stopwords - Czech Stop Word List'): 'extra_stopwords_ces',
                main.tr('extra-stopwords - Danish Stop Word List'): 'extra_stopwords_dan',
                main.tr('extra-stopwords - Dutch Stop Word List'): 'extra_stopwords_nld',
                main.tr('extra-stopwords - English Stop Word List'): 'extra_stopwords_eng',
                main.tr('extra-stopwords - Estonian Stop Word List'): 'extra_stopwords_est',
                main.tr('extra-stopwords - Finnish Stop Word List'): 'extra_stopwords_fin',
                main.tr('extra-stopwords - French Stop Word List'): 'extra_stopwords_fra',
                main.tr('extra-stopwords - Galician Stop Word List'): 'extra_stopwords_glg',
                main.tr('extra-stopwords - German Stop Word List'): 'extra_stopwords_deu',
                main.tr('extra-stopwords - Greek (Modern) Stop Word List'): 'extra_stopwords_ell',
                main.tr('extra-stopwords - Hausa Stop Word List'): 'extra_stopwords_hau',
                main.tr('extra-stopwords - Hebrew Stop Word List'): 'extra_stopwords_heb',
                main.tr('extra-stopwords - Hindi Stop Word List'): 'extra_stopwords_hin',
                main.tr('extra-stopwords - Hungarian Stop Word List'): 'extra_stopwords_hun',
                main.tr('extra-stopwords - Icelandic Stop Word List'): 'extra_stopwords_isl',
                main.tr('extra-stopwords - Indonesian Stop Word List'): 'extra_stopwords_ind',
                main.tr('extra-stopwords - Irish Stop Word List'): 'extra_stopwords_gle',
                main.tr('extra-stopwords - Italian Stop Word List'): 'extra_stopwords_ita',
                main.tr('extra-stopwords - Japanese Stop Word List'): 'extra_stopwords_jpn',
                main.tr('extra-stopwords - Korean Stop Word List'): 'extra_stopwords_kor',
                main.tr('extra-stopwords - Kurdish Stop Word List'): 'extra_stopwords_kur',
                main.tr('extra-stopwords - Latvian Stop Word List'): 'extra_stopwords_lav',
                main.tr('extra-stopwords - Lithuanian Stop Word List'): 'extra_stopwords_lit',
                main.tr('extra-stopwords - Malay Stop Word List'): 'extra_stopwords_msa',
                main.tr('extra-stopwords - Marathi Stop Word List'): 'extra_stopwords_mar',
                main.tr('extra-stopwords - Mongolian Stop Word List'): 'extra_stopwords_mon',
                main.tr('extra-stopwords - Nepali Stop Word List'): 'extra_stopwords_nep',
                main.tr('extra-stopwords - Norwegian Bokmål Stop Word List'): 'extra_stopwords_nob',
                main.tr('extra-stopwords - Norwegian Bokmål Stop Word List'): 'extra_stopwords_nno',
                main.tr('extra-stopwords - Persian Stop Word List'): 'extra_stopwords_fas',
                main.tr('extra-stopwords - Polish Stop Word List'): 'extra_stopwords_pol',
                main.tr('extra-stopwords - Portuguese Stop Word List'): 'extra_stopwords_por',
                main.tr('extra-stopwords - Romanian Stop Word List'): 'extra_stopwords_ron',
                main.tr('extra-stopwords - Russian Stop Word List'): 'extra_stopwords_rus',
                main.tr('extra-stopwords - Serbian (Cyrillic) Stop Word List'): 'extra_stopwords_srp_cyrl',
                main.tr('extra-stopwords - Serbian (Latin) Stop Word List'): 'extra_stopwords_srp_latn',
                main.tr('extra-stopwords - Slovak Stop Word List'): 'extra_stopwords_slk',
                main.tr('extra-stopwords - Slovenian Stop Word List'): 'extra_stopwords_slv',
                main.tr('extra-stopwords - Spanish Stop Word List'): 'extra_stopwords_spa',
                main.tr('extra-stopwords - Swahili Stop Word List'): 'extra_stopwords_swa',
                main.tr('extra-stopwords - Swedish Stop Word List'): 'extra_stopwords_swe',
                main.tr('extra-stopwords - Tagalog Stop Word List'): 'extra_stopwords_tgl',
                main.tr('extra-stopwords - Telugu Stop Word List'): 'extra_stopwords_tel',
                main.tr('extra-stopwords - Thai Stop Word List'): 'extra_stopwords_tha',
                main.tr('extra-stopwords - Turkish Stop Word List'): 'extra_stopwords_tur',
                main.tr('extra-stopwords - Ukrainian Stop Word List'): 'extra_stopwords_ukr',
                main.tr('extra-stopwords - Urdu Stop Word List'): 'extra_stopwords_urd',
                main.tr('extra-stopwords - Vietnamese Stop Word List'): 'extra_stopwords_vie',
                main.tr('extra-stopwords - Yoruba Stop Word List'): 'extra_stopwords_yor',

                main.tr('NLTK - Arabic Stop Word List'): 'nltk_ara',
                main.tr('NLTK - Azerbaijani Stop Word List'): 'nltk_aze',
                main.tr('NLTK - Danish Stop Word List'): 'nltk_dan',
                main.tr('NLTK - Dutch Stop Word List'): 'nltk_nld',
                main.tr('NLTK - English Stop Word List'): 'nltk_eng',
                main.tr('NLTK - Finnish Stop Word List'): 'nltk_fin',
                main.tr('NLTK - French Stop Word List'): 'nltk_fra',
                main.tr('NLTK - German Stop Word List'): 'nltk_deu',
                main.tr('NLTK - Greek (Modern) Stop Word List'): 'nltk_ell',
                main.tr('NLTK - Hungarian Stop Word List'): 'nltk_hun',
                main.tr('NLTK - Indonesian Stop Word List'): 'nltk_ind',
                main.tr('NLTK - Italian Stop Word List'): 'nltk_ita',
                main.tr('NLTK - Kazakh Stop Word List'): 'nltk_kaz',
                main.tr('NLTK - Nepali Stop Word List'): 'nltk_nep',
                main.tr('NLTK - Norwegian Bokmål Stop Word List'): 'nltk_nob',
                main.tr('NLTK - Norwegian Nynorsk Stop Word List'): 'nltk_nno',
                main.tr('NLTK - Portuguese Stop Word List'): 'nltk_por',
                main.tr('NLTK - Romanian Stop Word List'): 'nltk_ron',
                main.tr('NLTK - Russian Stop Word List'): 'nltk_rus',
                main.tr('NLTK - Slovenian Stop Word List'): 'nltk_slv',
                main.tr('NLTK - Spanish Stop Word List'): 'nltk_spa',
                main.tr('NLTK - Swedish Stop Word List'): 'nltk_swe',
                main.tr('NLTK - Tajik Stop Word List'): 'nltk_tgk',
                main.tr('NLTK - Turkish Stop Word List'): 'nltk_tur',

                main.tr('PyThaiNLP - Thai Stop Word List'): 'pythainlp_tha',

                main.tr('spaCy - Afrikaans Stop Word List'): 'spacy_afr',
                main.tr('spaCy - Albanian Stop Word List'): 'spacy_sqi',
                main.tr('spaCy - Amharic Stop Word List'): 'spacy_amh',
                main.tr('spaCy - Arabic Stop Word List'): 'spacy_ara',
                main.tr('spaCy - Armenian Stop Word List'): 'spacy_hye',
                main.tr('spaCy - Azerbaijani Stop Word List'): 'spacy_aze',
                main.tr('spaCy - Basque Stop Word List'): 'spacy_eus',
                main.tr('spaCy - Bengali Stop Word List'): 'spacy_ben',
                main.tr('spaCy - Bulgarian Stop Word List'): 'spacy_bul',
                main.tr('spaCy - Catalan Stop Word List'): 'spacy_cat',
                main.tr('spaCy - Chinese (Simplified) Stop Word List'): 'spacy_zho_cn',
                main.tr('spaCy - Chinese (Traditional) Stop Word List'): 'spacy_zho_tw',
                main.tr('spaCy - Croatian Stop Word List'): 'spacy_hrv',
                main.tr('spaCy - Czech Stop Word List'): 'spacy_ces',
                main.tr('spaCy - Danish Stop Word List'): 'spacy_dan',
                main.tr('spaCy - Dutch Stop Word List'): 'spacy_nld',
                main.tr('spaCy - English Stop Word List'): 'spacy_eng',
                main.tr('spaCy - Estonian Stop Word List'): 'spacy_est',
                main.tr('spaCy - Finnish Stop Word List'): 'spacy_fin',
                main.tr('spaCy - French Stop Word List'): 'spacy_fra',
                main.tr('spaCy - German Stop Word List'): 'spacy_deu',
                main.tr('spaCy - Greek (Ancient) Stop Word List'): 'spacy_grc',
                main.tr('spaCy - Greek (Modern) Stop Word List'): 'spacy_ell',
                main.tr('spaCy - Gujarati Stop Word List'): 'spacy_guj',
                main.tr('spaCy - Hebrew Stop Word List'): 'spacy_heb',
                main.tr('spaCy - Hindi Stop Word List'): 'spacy_hin',
                main.tr('spaCy - Hungarian Stop Word List'): 'spacy_hun',
                main.tr('spaCy - Icelandic Stop Word List'): 'spacy_isl',
                main.tr('spaCy - Indonesian Stop Word List'): 'spacy_ind',
                main.tr('spaCy - Irish Stop Word List'): 'spacy_gle',
                main.tr('spaCy - Italian Stop Word List'): 'spacy_ita',
                main.tr('spaCy - Japanese Stop Word List'): 'spacy_jpn',
                main.tr('spaCy - Kannada Stop Word List'): 'spacy_kan',
                main.tr('spaCy - Korean Stop Word List'): 'spacy_kor',
                main.tr('spaCy - Kyrgyz Stop Word List'): 'spacy_kir',
                main.tr('spaCy - Latvian Stop Word List'): 'spacy_lav',
                main.tr('spaCy - Ligurian Stop Word List'): 'spacy_lij',
                main.tr('spaCy - Lithuanian Stop Word List'): 'spacy_lit',
                main.tr('spaCy - Luxembourgish Stop Word List'): 'spacy_ltz',
                main.tr('spaCy - Macedonian Stop Word List'): 'spacy_mkd',
                main.tr('spaCy - Malayalam Stop Word List'): 'spacy_mal',
                main.tr('spaCy - Marathi Stop Word List'): 'spacy_mar',
                main.tr('spaCy - Nepali Stop Word List'): 'spacy_nep',
                main.tr('spaCy - Norwegian Bokmål Stop Word List'): 'spacy_nob',
                main.tr('spaCy - Persian Stop Word List'): 'spacy_fas',
                main.tr('spaCy - Polish Stop Word List'): 'spacy_pol',
                main.tr('spaCy - Portuguese Stop Word List'): 'spacy_por',
                main.tr('spaCy - Romanian Stop Word List'): 'spacy_ron',
                main.tr('spaCy - Russian Stop Word List'): 'spacy_rus',
                main.tr('spaCy - Sanskrit Stop Word List'): 'spacy_san',
                main.tr('spaCy - Serbian (Cyrillic) Stop Word List'): 'spacy_srp_cyrl',
                main.tr('spaCy - Serbian (Latin) Stop Word List'): 'spacy_srp_latn',
                main.tr('spaCy - Sinhala Stop Word List'): 'spacy_sin',
                main.tr('spaCy - Slovak Stop Word List'): 'spacy_slk',
                main.tr('spaCy - Slovenian Stop Word List'): 'spacy_slv',
                main.tr('spaCy - Spanish Stop Word List'): 'spacy_spa',
                main.tr('spaCy - Swedish Stop Word List'): 'spacy_swe',
                main.tr('spaCy - Tagalog Stop Word List'): 'spacy_tgl',
                main.tr('spaCy - Tamil Stop Word List'): 'spacy_tam',
                main.tr('spaCy - Tatar Stop Word List'): 'spacy_tat',
                main.tr('spaCy - Telugu Stop Word List'): 'spacy_tel',
                main.tr('spaCy - Thai Stop Word List'): 'spacy_tha',
                main.tr('spaCy - Tigrinya Stop Word List'): 'spacy_tir',
                main.tr('spaCy - Tswana Stop Word List'): 'spacy_tsn',
                main.tr('spaCy - Turkish Stop Word List'): 'spacy_tur',
                main.tr('spaCy - Ukrainian Stop Word List'): 'spacy_ukr',
                main.tr('spaCy - Urdu Stop Word List'): 'spacy_urd',
                main.tr('spaCy - Vietnamese Stop Word List'): 'spacy_vie',
                main.tr('spaCy - Yoruba Stop Word List'): 'spacy_yor',

                main.tr('Stopwords ISO - Afrikaans Stop Word List'): 'stopwords_iso_afr',
                main.tr('Stopwords ISO - Arabic Stop Word List'): 'stopwords_iso_ara',
                main.tr('Stopwords ISO - Armenian Stop Word List'): 'stopwords_iso_hye',
                main.tr('Stopwords ISO - Basque Stop Word List'): 'stopwords_iso_eus',
                main.tr('Stopwords ISO - Bengali Stop Word List'): 'stopwords_iso_ben',
                main.tr('Stopwords ISO - Breton Stop Word List'): 'stopwords_iso_bre',
                main.tr('Stopwords ISO - Bulgarian Stop Word List'): 'stopwords_iso_bul',
                main.tr('Stopwords ISO - Catalan Stop Word List'): 'stopwords_iso_cat',
                main.tr('Stopwords ISO - Chinese (Simplified) Stop Word List'): 'stopwords_iso_zho_cn',
                main.tr('Stopwords ISO - Chinese (Traditional) Stop Word List'): 'stopwords_iso_zho_tw',
                main.tr('Stopwords ISO - Croatian Stop Word List'): 'stopwords_iso_hrv',
                main.tr('Stopwords ISO - Czech Stop Word List'): 'stopwords_iso_ces',
                main.tr('Stopwords ISO - Danish Stop Word List'): 'stopwords_iso_dan',
                main.tr('Stopwords ISO - Dutch Stop Word List'): 'stopwords_iso_nld',
                main.tr('Stopwords ISO - English Stop Word List'): 'stopwords_iso_eng',
                main.tr('Stopwords ISO - Esperanto Stop Word List'): 'stopwords_iso_epo',
                main.tr('Stopwords ISO - Estonian Stop Word List'): 'stopwords_iso_est',
                main.tr('Stopwords ISO - Finnish Stop Word List'): 'stopwords_iso_fin',
                main.tr('Stopwords ISO - French Stop Word List'): 'stopwords_iso_fra',
                main.tr('Stopwords ISO - Galician Stop Word List'): 'stopwords_iso_glg',
                main.tr('Stopwords ISO - German Stop Word List'): 'stopwords_iso_deu',
                main.tr('Stopwords ISO - Greek (Modern) Stop Word List'): 'stopwords_iso_ell',
                main.tr('Stopwords ISO - Gujarati Stop Word List'): 'stopwords_iso_guj',
                main.tr('Stopwords ISO - Hausa Stop Word List'): 'stopwords_iso_hau',
                main.tr('Stopwords ISO - Hebrew Stop Word List'): 'stopwords_iso_heb',
                main.tr('Stopwords ISO - Hindi Stop Word List'): 'stopwords_iso_hin',
                main.tr('Stopwords ISO - Hungarian Stop Word List'): 'stopwords_iso_hun',
                main.tr('Stopwords ISO - Indonesian Stop Word List'): 'stopwords_iso_ind',
                main.tr('Stopwords ISO - Irish Stop Word List'): 'stopwords_iso_gle',
                main.tr('Stopwords ISO - Italian Stop Word List'): 'stopwords_iso_ita',
                main.tr('Stopwords ISO - Japanese Stop Word List'): 'stopwords_iso_jpn',
                main.tr('Stopwords ISO - Korean Stop Word List'): 'stopwords_iso_kor',
                main.tr('Stopwords ISO - Kurdish Stop Word List'): 'stopwords_iso_kur',
                main.tr('Stopwords ISO - Latin Stop Word List'): 'stopwords_iso_lat',
                main.tr('Stopwords ISO - Latvian Stop Word List'): 'stopwords_iso_lav',
                main.tr('Stopwords ISO - Lithuanian Stop Word List'): 'stopwords_iso_lit',
                main.tr('Stopwords ISO - Malay Stop Word List'): 'stopwords_iso_msa',
                main.tr('Stopwords ISO - Marathi Stop Word List'): 'stopwords_iso_mar',
                main.tr('Stopwords ISO - Norwegian Stop Word List'): 'stopwords_iso_nob',
                main.tr('Stopwords ISO - Norwegian Stop Word List'): 'stopwords_iso_nno',
                main.tr('Stopwords ISO - Persian Stop Word List'): 'stopwords_iso_fas',
                main.tr('Stopwords ISO - Polish Stop Word List'): 'stopwords_iso_pol',
                main.tr('Stopwords ISO - Portuguese Stop Word List'): 'stopwords_iso_por',
                main.tr('Stopwords ISO - Romanian Stop Word List'): 'stopwords_iso_ron',
                main.tr('Stopwords ISO - Russian Stop Word List'): 'stopwords_iso_rus',
                main.tr('Stopwords ISO - Slovak Stop Word List'): 'stopwords_iso_slk',
                main.tr('Stopwords ISO - Slovenian Stop Word List'): 'stopwords_iso_slv',
                main.tr('Stopwords ISO - Somali Stop Word List'): 'stopwords_iso_som',
                main.tr('Stopwords ISO - Sotho (Southern) Stop Word List'): 'stopwords_iso_sot',
                main.tr('Stopwords ISO - Spanish Stop Word List'): 'stopwords_iso_spa',
                main.tr('Stopwords ISO - Swahili Stop Word List'): 'stopwords_iso_swa',
                main.tr('Stopwords ISO - Swedish Stop Word List'): 'stopwords_iso_swe',
                main.tr('Stopwords ISO - Tagalog Stop Word List'): 'stopwords_iso_tgl',
                main.tr('Stopwords ISO - Thai Stop Word List'): 'stopwords_iso_tha',
                main.tr('Stopwords ISO - Turkish Stop Word List'): 'stopwords_iso_tur',
                main.tr('Stopwords ISO - Ukrainian Stop Word List'): 'stopwords_iso_ukr',
                main.tr('Stopwords ISO - Urdu Stop Word List'): 'stopwords_iso_urd',
                main.tr('Stopwords ISO - Vietnamese Stop Word List'): 'stopwords_iso_vie',
                main.tr('Stopwords ISO - Yoruba Stop Word List'): 'stopwords_iso_yor',
                main.tr('Stopwords ISO - Zulu Stop Word List'): 'stopwords_iso_zul'
            }
        },

        'sentence_tokenizers': {
            'afr': [
                'spacy_sentencizer'
            ],

            'sqi': [
                'spacy_sentencizer'
            ],

            'amh': [
                'spacy_sentencizer'
            ],

            'ara': [
                'spacy_sentencizer'
            ],

            'hye': [
                'spacy_sentencizer'
            ],

            'aze': [
                'spacy_sentencizer'
            ],

            'eus': [
                'spacy_sentencizer'
            ],

            'ben': [
                'spacy_sentencizer'
            ],

            'bul': [
                'spacy_sentencizer'
            ],

            'cat': [
                'spacy_sentencizer'
            ],

            'zho_cn': [
                'spacy_sentence_recognizer',
                'wordless_zho'
            ],
            'zho_tw': [
                'spacy_sentence_recognizer',
                'wordless_zho'
            ],

            'hrv': [
                'spacy_sentencizer'
            ],

            'ces': [
                'nltk_punkt',
                'spacy_sentencizer'
            ],

            'dan': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],

            'nld': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],

            'eng_gb': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],
            'eng_us': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],

            'est': [
                'nltk_punkt',
                'spacy_sentencizer'
            ],

            'fin': [
                'nltk_punkt',
                'spacy_sentencizer'
            ],

            'fra': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],

            'deu_at': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],
            'deu_de': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],
            'deu_ch': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],

            'grc': [
                'spacy_sentencizer'
            ],
            'ell': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],

            'guj': [
                'spacy_sentencizer'
            ],

            'heb': [
                'spacy_sentencizer'
            ],

            'hin': [
                'spacy_sentencizer'
            ],

            'hun': [
                'spacy_sentencizer'
            ],

            'isl': [
                'spacy_sentencizer',
                'tokenizer_isl'
            ],

            'ind': [
                'spacy_sentencizer'
            ],

            'gle': [
                'spacy_sentencizer'
            ],

            'ita': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],

            'jpn': [
                'spacy_sentence_recognizer',
                'wordless_jpn'
            ],

            'kan': [
                'spacy_sentencizer'
            ],

            'kir': [
                'spacy_sentencizer'
            ],

            'lav': [
                'spacy_sentencizer'
            ],

            'lij': [
                'spacy_sentencizer'
            ],

            'lit': [
                'spacy_sentence_recognizer'
            ],

            'ltz': [
                'spacy_sentencizer'
            ],

            'mkd': [
                'spacy_sentencizer'
            ],

            'mal': [
                'spacy_sentencizer'
            ],

            'mar': [
                'spacy_sentencizer'
            ],

            'nep': [
                'spacy_sentencizer'
            ],

            'nob': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],

            'nno': [
                'nltk_punkt'
            ],

            'fas': [
                'spacy_sentencizer'
            ],

            'pol': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],

            'por_br': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],
            'por_pt': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],

            'ron': [
                'spacy_sentence_recognizer'
            ],

            'rus': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],

            'san': [
                'spacy_sentencizer'
            ],

            'srp_cyrl': [
                'spacy_sentencizer'
            ],
            'srp_latn': [
                'spacy_sentencizer'
            ],

            'sin': [
                'spacy_sentencizer'
            ],

            'slk': [
                'spacy_sentencizer'
            ],

            'slv': [
                'nltk_punkt',
                'spacy_sentencizer'
            ],

            'spa': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ],

            'swe': [
                'nltk_punkt',
                'spacy_sentencizer'
            ],

            'tgl': [
                'spacy_sentencizer'
            ],

            'tam': [
                'spacy_sentencizer'
            ],

            'tat': [
                'spacy_sentencizer'
            ],

            'tel': [
                'spacy_sentencizer'
            ],

            'tha': [
                'pythainlp_crfcut'
            ],

            'bod': [
                'botok_bod'
            ],

            'tir': [
                'spacy_sentencizer'
            ],

            'tsn': [
                'spacy_sentencizer'
            ],

            'tur': [
                'nltk_punkt',
                'spacy_sentencizer'
            ],

            'ukr': [
                'spacy_sentencizer'
            ],

            'urd': [
                'spacy_sentencizer'
            ],

            'vie': [
                'underthesea_vie'
            ],

            'yor': [
                'spacy_sentencizer'
            ],

            'other': [
                'nltk_punkt',
                'spacy_sentence_recognizer'
            ]
        },

        'word_tokenizers': {
            'afr': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_afr'
            ],

            'sqi': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_sqi'
            ],

            'amh': [
                'spacy_amh'
            ],

            'ara': [
                'spacy_ara'
            ],

            'hye': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_hye'
            ],

            'asm': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses'
            ],

            'aze': [
                'spacy_aze'
            ],

            'eus': [
                'spacy_eus'
            ],

            'ben': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_ben'
            ],

            'bul': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_bul'
            ],

            'cat': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_cat'
            ],

            'zho_cn': [
                'jieba_zho',
                'pkuseg_zho',
                'spacy_zho',
                'wordless_zho_char'
            ],
            'zho_tw': [
                'jieba_zho',
                'pkuseg_zho',
                'spacy_zho',
                'wordless_zho_char'
            ],

            'hrv': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_hrv'
            ],

            'ces': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_ces'
            ],

            'dan': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_dan'
            ],

            'nld': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_nld'
            ],

            'eng_gb': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_eng'
            ],
            'eng_us': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_eng'
            ],

            'est': [
                'sacremoses_moses',
                'spacy_est'
            ],

            'fin': [
                'sacremoses_moses',
                'spacy_fin'
            ],

            'fra': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_fra'
            ],

            'deu_at': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_deu'
            ],
            'deu_de': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_deu'
            ],
            'deu_ch': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_deu'
            ],

            'grc': [
                'spacy_grc'
            ],
            'ell': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_ell'
            ],

            'guj': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_guj'
            ],

            'heb': [
                'spacy_heb'
            ],

            'hin': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_hin'
            ],

            'hun': [
                'sacremoses_moses',
                'spacy_hun'
            ],

            'isl': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_isl',
                'tokenizer_isl'
            ],

            'ind': [
                'spacy_ind'
            ],

            'gle': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_gle'
            ],

            'ita': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_ita'
            ],

            'jpn': [
                'nagisa_jpn',
                'spacy_jpn',
                'sudachipy_jpn_split_mode_a',
                'sudachipy_jpn_split_mode_b',
                'sudachipy_jpn_split_mode_c',
                'wordless_jpn_kanji'
            ],

            'kan': [
                'sacremoses_moses',
                'spacy_kan'
            ],

            'kir': [
                'spacy_kir'
            ],

            'lav': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_lav'
            ],

            'lij': [
                'spacy_lij'
            ],

            'lit': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_lit'
            ],

            'ltz': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_ltz'
            ],

            'mkd': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_mkd'
            ],

            'mal': [
                'sacremoses_moses',
                'spacy_mal'
            ],

            'mar': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_mar'
            ],

            'mni': [
                'sacremoses_moses'
            ],

            'nep': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_nep'
            ],

            'nob': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_nob'
            ],

            'ori': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses'
            ],

            'fas': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_tok_tok', 'nltk_twitter',
                'spacy_fas'
            ],

            'pol': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_pol'
            ],

            'por_br': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_por'
            ],
            'por_pt': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_por'
            ],

            'pan': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses'
            ],

            'ron': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_ron'
            ],

            'rus': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_rus'
            ],

            'san': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_san'
            ],

            'srp_cyrl': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_srp'
            ],
            'srp_latn': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_srp'
            ],

            'sin': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_sin'
            ],

            'slk': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_slk'
            ],

            'slv': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_slv'
            ],

            'spa': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_spa'
            ],

            'swe': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_swe'
            ],

            'tgl': [
                'spacy_tgl'
            ],

            'tgk': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_tok_tok', 'nltk_twitter',
            ],

            'tam': [
                'sacremoses_moses',
                'spacy_tam'
            ],

            'tat': [
                'spacy_tat'
            ],

            'tel': [
                'sacremoses_moses',
                'spacy_tel'
            ],

            'tdt': [
                'sacremoses_moses'
            ],

            'tha': [
                'pythainlp_longest_matching',
                'pythainlp_max_matching',
                'pythainlp_max_matching_tcc',
                'pythainlp_max_matching_tcc_safe_mode',
                'pythainlp_nercut'
            ],

            'bod': [
                'botok_bod'
            ],

            'tir': [
                'spacy_tir'
            ],

            'tsn': [
                'spacy_tsn'
            ],

            'tur': [
                'spacy_tur'
            ],

            'ukr': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_ukr'
            ],

            'urd': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_twitter',
                'spacy_urd'
            ],

            'vie': [
                'nltk_tok_tok',
                'underthesea_vie'
            ],

            'yor': [
                'spacy_yor'
            ],

            'other': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_eng'
            ]
        },

        'syl_tokenizers': {
            'afr': [
                'pyphen_afr'
            ],

            'sqi': [
                'pyphen_sqi'
            ],

            'bel': [
                'pyphen_bel'
            ],

            'bul': [
                'pyphen_bul'
            ],

            'hrv': [
                'pyphen_hrv'
            ],

            'ces': [
                'pyphen_ces'
            ],

            'dan': [
                'pyphen_dan'
            ],

            'nld': [
                'pyphen_nld'
            ],

            'eng_gb': [
                'pyphen_eng_gb'
            ],
            'eng_us': [
                'pyphen_eng_us'
            ],

            'epo': [
                'pyphen_epo'
            ],

            'est': [
                'pyphen_est'
            ],

            'fra': [
                'pyphen_fra'
            ],

            'glg': [
                'pyphen_glg'
            ],

            'deu_at': [
                'pyphen_deu_at'
            ],
            'deu_de': [
                'pyphen_deu_de'
            ],
            'deu_ch': [
                'pyphen_deu_ch'
            ],

            'ell': [
                'pyphen_ell'
            ],

            'hun': [
                'pyphen_hun'
            ],

            'isl': [
                'pyphen_isl'
            ],

            'ind': [
                'pyphen_ind'
            ],

            'ita': [
                'pyphen_ita'
            ],

            'lit': [
                'pyphen_lit'
            ],

            'lav': [
                'pyphen_lav'
            ],

            'mon': [
                'pyphen_mon'
            ],

            'nob': [
                'pyphen_nob'
            ],
            'nno': [
                'pyphen_nno'
            ],

            'pol': [
                'pyphen_pol'
            ],

            'por_br': [
                'pyphen_por_br'
            ],
            'por_pt': [
                'pyphen_por_pt'
            ],

            'ron': [
                'pyphen_ron'
            ],

            'rus': [
                'pyphen_rus'
            ],

            'srp_cyrl': [
                'pyphen_srp_cyrl'
            ],
            'srp_latn': [
                'pyphen_srp_latn'
            ],

            'slk': [
                'pyphen_slk'
            ],

            'slv': [
                'pyphen_slv'
            ],

            'spa': [
                'pyphen_spa'
            ],

            'swe': [
                'pyphen_swe'
            ],

            'tel': [
                'pyphen_tel'
            ],

            'tha': [
                'pythainlp_tha',
                'ssg_tha'
            ],

            'ukr': [
                'pyphen_ukr'
            ],

            'zul': [
                'pyphen_zul'
            ]
        },

        'pos_taggers': {
            'cat': [
                'spacy_cat'
            ],

            'zho_cn': [
                'jieba_zho',
                'spacy_zho'
            ],
            'zho_tw': [
                'jieba_zho',
                'spacy_zho'
            ],

            'dan': [
                'spacy_dan',
            ],

            'nld': [
                'spacy_nld'
            ],

            'eng_gb': [
                'nltk_perceptron',
                'spacy_eng'
            ],
            'eng_us': [
                'nltk_perceptron',
                'spacy_eng'
            ],

            'fra': [
                'spacy_fra'
            ],

            'deu_at': [
                'spacy_deu'
            ],
            'deu_de': [
                'spacy_deu'
            ],
            'deu_ch': [
                'spacy_deu'
            ],

            'ell': [
                'spacy_ell'
            ],

            'ita': [
                'spacy_ita'
            ],

            'jpn': [
                'nagisa_jpn',
                'spacy_jpn',
                'sudachipy_jpn'
            ],

            'lit': [
                'spacy_lit'
            ],

            'mkd': [
                'spacy_mkd'
            ],

            'nob': [
                'spacy_nob'
            ],

            'pol': [
                'spacy_pol'
            ],

            'por_br': [
                'spacy_por'
            ],
            'por_pt': [
                'spacy_por'
            ],

            'ron': [
                'spacy_ron'
            ],

            'rus': [
                'nltk_perceptron',
                'pymorphy2_morphological_analyzer',
                'spacy_rus'
            ],

            'spa': [
                'spacy_spa'
            ],

            'tha': [
                'pythainlp_perceptron_lst20',
                'pythainlp_perceptron_orchid',
                'pythainlp_perceptron_pud'
            ],

            'bod': [
                'botok_bod'
            ],

            'ukr': [
                'pymorphy2_morphological_analyzer'
            ],

            'vie': [
                'underthesea_vie'
            ]
        },

        'lemmatizers': {
            'ast': [
                'lemmatization_lists_ast'
            ],

            'ben': [
                'spacy_ben'
            ],

            'bul': [
                'lemmatization_lists_bul'
            ],

            'cat': [
                'lemmatization_lists_cat',
                'spacy_cat'
            ],

            'hrv': [
                'spacy_hrv'
            ],

            'ces': [
                'lemmatization_lists_ces',
                'spacy_ces'
            ],

            'dan': [
                'spacy_dan'
            ],

            'nld': [
                'spacy_nld'
            ],

            'eng_gb': [
                'lemmatization_lists_eng',
                'nltk_wordnet',
                'spacy_eng'
            ],
            'eng_us': [
                'lemmatization_lists_eng',
                'nltk_wordnet',
                'spacy_eng'
            ],

            'est': [
                'lemmatization_lists_est'
            ],

            'fra': [
                'lemmatization_lists_fra',
                'spacy_fra'
            ],

            'glg': [
                'lemmatization_lists_glg'
            ],

            'deu_at': [
                'lemmatization_lists_deu',
                'spacy_deu'
            ],
            'deu_de': [
                'lemmatization_lists_deu',
                'spacy_deu'
            ],
            'deu_ch': [
                'lemmatization_lists_deu',
                'spacy_deu'
            ],

            'grc': [
                'spacy_grc'
            ],
            'ell': [
                'spacy_ell'
            ],

            'hun': [
                'lemmatization_lists_hun',
                'spacy_hun'
            ],

            'ind': [
                'spacy_ind'
            ],

            'gle': [
                'lemmatization_lists_gle',
                'spacy_gle'
            ],

            'ita': [
                'lemmatization_lists_ita',
                'spacy_ita'
            ],

            'jpn': [
                'spacy_jpn',
                'sudachipy_jpn'
            ],

            'lit': [
                'spacy_lit'
            ],

            'ltz': [
                'spacy_ltz'
            ],

            'mkd': [
                'spacy_mkd'
            ],

            'glv': [
                'lemmatization_lists_glv'
            ],

            'nob': [
                'spacy_nob'
            ],

            'fas': [
                'lemmatization_lists_fas',
                'spacy_fas'
            ],

            'pol': [
                'spacy_pol'
            ],

            'por_br': [
                'lemmatization_lists_por',
                'spacy_por'
            ],
            'por_pt': [
                'lemmatization_lists_por',
                'spacy_por'
            ],

            'ron': [
                'lemmatization_lists_ron',
                'spacy_ron'
            ],

            'rus': [
                'lemmatization_lists_rus',
                'pymorphy2_morphological_analyzer',
                'spacy_rus'
            ],

            'gla': [
                'lemmatization_lists_gla'
            ],

            'srp_cyrl': [
                'spacy_srp_cyrl'
            ],

            'slk': [
                'lemmatization_lists_slk'
            ],

            'slv': [
                'lemmatization_lists_slv'
            ],

            'spa': [
                'lemmatization_lists_spa',
                'spacy_spa'
            ],

            'swe': [
                'lemmatization_lists_swe',
                'spacy_swe'
            ],

            'tgl': [
                'spacy_tgl'
            ],

            'bod': [
                'botok_bod'
            ],

            'tur': [
                'spacy_tur'
            ],

            'ukr': [
                'lemmatization_lists_ukr',
                'pymorphy2_morphological_analyzer'
            ],

            'urd': [
                'spacy_urd'
            ],

            'cym': [
                'lemmatization_lists_cym'
            ]
        },

        'stop_word_lists': {
            'afr': [
                'spacy_afr',
                'stopwords_iso_afr',
                'custom'
            ],

            'akk': [
                'cltk_akk',
                'custom'
            ],

            'sqi': [
                'extra_stopwords_sqi',
                'spacy_sqi',
                'custom'
            ],

            'amh': [
                'spacy_amh',
                'custom'
            ],

            'ara': [
                'extra_stopwords_ara',
                'nltk_ara',
                'spacy_ara',
                'stopwords_iso_ara',
                'custom'
            ],

            'arb': [
                'cltk_arb',
                'custom'
            ],

            'hye': [
                'extra_stopwords_hye',
                'spacy_hye',
                'stopwords_iso_hye',
                'custom'
            ],

            'aze': [
                'nltk_aze',
                'spacy_aze',
                'custom'
            ],

            'eus': [
                'extra_stopwords_eus',
                'spacy_eus',
                'stopwords_iso_eus',
                'custom'
            ],

            'bel': [
                'extra_stopwords_bel',
                'custom'
            ],

            'ben': [
                'extra_stopwords_ben',
                'spacy_ben',
                'stopwords_iso_ben',
                'custom'
            ],

            'bre': [
                'stopwords_iso_bre',
                'custom'
            ],

            'bul': [
                'extra_stopwords_bul',
                'spacy_bul',
                'stopwords_iso_bul',
                'custom'
            ],

            'cat': [
                'extra_stopwords_cat',
                'spacy_cat',
                'stopwords_iso_cat',
                'custom'
            ],

            'zho_cn': [
                'extra_stopwords_zho_cn',
                'spacy_zho_cn',
                'stopwords_iso_zho_cn',
                'custom'
            ],
            'zho_tw': [
                'extra_stopwords_zho_tw',
                'spacy_zho_tw',
                'stopwords_iso_zho_tw',
                'custom'
            ],

            'cop': [
                'cltk_cop',
                'custom'
            ],

            'hrv': [
                'extra_stopwords_hrv',
                'spacy_hrv',
                'stopwords_iso_hrv',
                'custom'
            ],

            'ces': [
                'extra_stopwords_ces',
                'spacy_ces',
                'stopwords_iso_ces',
                'custom'
            ],

            'dan': [
                'extra_stopwords_dan',
                'nltk_dan',
                'spacy_dan',
                'stopwords_iso_dan',
                'custom'
            ],

            'nld': [
                'extra_stopwords_nld',
                'nltk_nld',
                'spacy_nld',
                'stopwords_iso_nld',
                'custom'
            ],

            'enm': [
                'cltk_enm',
                'custom'
            ],
            'ang': [
                'cltk_ang',
                'custom'
            ],
            'eng_gb': [
                'extra_stopwords_eng',
                'nltk_eng',
                'spacy_eng',
                'stopwords_iso_eng',
                'custom'
            ],
            'eng_us': [
                'extra_stopwords_eng',
                'nltk_eng',
                'spacy_eng',
                'stopwords_iso_eng',
                'custom'
            ],

            'epo': [
                'stopwords_iso_epo',
                'custom'
            ],

            'est': [
                'extra_stopwords_est',
                'spacy_est',
                'stopwords_iso_est',
                'custom'
            ],

            'fin': [
                'extra_stopwords_fin',
                'nltk_fin',
                'spacy_fin',
                'stopwords_iso_fin',
                'custom'
            ],

            'fra': [
                'extra_stopwords_fra',
                'nltk_fra',
                'spacy_fra',
                'stopwords_iso_fra',
                'custom'
            ],
            'fro': [
                'cltk_fro',
                'custom'
            ],

            'glg': [
                'extra_stopwords_glg',
                'stopwords_iso_glg',
                'custom'
            ],

            'deu_at': [
                'extra_stopwords_deu',
                'nltk_deu',
                'spacy_deu',
                'stopwords_iso_deu',
                'custom'
            ],
            'deu_de': [
                'extra_stopwords_deu',
                'nltk_deu',
                'spacy_deu',
                'stopwords_iso_deu',
                'custom'
            ],
            'gmh': [
                'cltk_gmh',
                'custom'
            ],
            'deu_ch': [
                'extra_stopwords_deu',
                'nltk_deu',
                'spacy_deu',
                'stopwords_iso_deu',
                'custom'
            ],

            'grc': [
                'cltk_grc',
                'spacy_grc',
                'custom'
            ],
            'ell': [
                'extra_stopwords_ell',
                'nltk_ell',
                'spacy_ell',
                'stopwords_iso_ell',
                'custom'
            ],

            'guj': [
                'spacy_guj',
                'stopwords_iso_guj',
                'custom'
            ],

            'hau': [
                'extra_stopwords_hau',
                'stopwords_iso_hau',
                'custom'
            ],

            'heb': [
                'extra_stopwords_heb',
                'spacy_heb',
                'stopwords_iso_heb',
                'custom'
            ],

            'hin': [
                'cltk_hin',
                'extra_stopwords_hin',
                'spacy_hin',
                'stopwords_iso_hin',
                'custom'
            ],

            'hun': [
                'extra_stopwords_hun',
                'nltk_hun',
                'spacy_hun',
                'stopwords_iso_hun',
                'custom'
            ],

            'isl': [
                'extra_stopwords_isl',
                'spacy_isl',
                'custom'
            ],

            'ind': [
                'extra_stopwords_ind',
                'nltk_ind',
                'spacy_ind',
                'stopwords_iso_ind',
                'custom'
            ],

            'gle': [
                'extra_stopwords_gle',
                'spacy_gle',
                'stopwords_iso_gle',
                'custom'
            ],

            'ita': [
                'extra_stopwords_ita',
                'nltk_ita',
                'spacy_ita',
                'stopwords_iso_ita',
                'custom'
            ],

            'jpn': [
                'extra_stopwords_jpn',
                'spacy_jpn',
                'stopwords_iso_jpn',
                'custom'
            ],

            'kan': [
                'spacy_kan',
                'custom'
            ],

            'kaz': [
                'nltk_kaz',
                'custom'
            ],

            'kor': [
                'extra_stopwords_kor',
                'spacy_kor',
                'stopwords_iso_kor',
                'custom'
            ],

            'kur': [
                'extra_stopwords_kur',
                'stopwords_iso_kur',
                'custom'
            ],

            'kir': [
                'spacy_kir',
                'custom'
            ],

            'lat': [
                'cltk_lat',
                'stopwords_iso_lat',
                'custom'
            ],

            'lav': [
                'extra_stopwords_lav',
                'spacy_lav',
                'stopwords_iso_lav',
                'custom'
            ],

            'lij': [
                'spacy_lij',
                'custom'
            ],

            'lit': [
                'extra_stopwords_lit',
                'spacy_lit',
                'stopwords_iso_lit',
                'custom'
            ],

            'ltz': [
                'spacy_ltz',
                'custom'
            ],

            'mkd': [
                'spacy_mkd',
                'custom'
            ],

            'msa': [
                'extra_stopwords_msa',
                'stopwords_iso_msa',
                'custom'
            ],

            'mal': [
                'spacy_mal',
                'custom'
            ],

            'mar': [
                'extra_stopwords_mar',
                'spacy_mar',
                'stopwords_iso_mar',
                'custom'
            ],

            'omr': [
                'cltk_omr',
                'custom'
            ],

            'mon': [
                'extra_stopwords_mon',
                'custom'
            ],

            'nep': [
                'extra_stopwords_nep',
                'nltk_nep',
                'spacy_nep',
                'custom'
            ],

            'non': [
                'cltk_non',
                'custom'
            ],
            'nob': [
                'extra_stopwords_nob',
                'nltk_nob',
                'spacy_nob',
                'stopwords_iso_nob',
                'custom'
            ],
            'nno': [
                'extra_stopwords_nno',
                'nltk_nno',
                'stopwords_iso_nno',
                'custom'
            ],

            'fas': [
                'extra_stopwords_fas',
                'spacy_fas',
                'stopwords_iso_fas',
                'custom'
            ],

            'pol': [
                'extra_stopwords_pol',
                'spacy_pol',
                'stopwords_iso_pol',
                'custom'
            ],

            'por_br': [
                'extra_stopwords_por',
                'nltk_por',
                'spacy_por',
                'stopwords_iso_por',
                'custom'
            ],
            'por_pt': [
                'extra_stopwords_por',
                'nltk_por',
                'spacy_por',
                'stopwords_iso_por',
                'custom'
            ],

            'pan': [
                'cltk_pan',
                'custom'
            ],

            'ron': [
                'extra_stopwords_ron',
                'nltk_ron',
                'spacy_ron',
                'stopwords_iso_ron',
                'custom'
            ],

            'rus': [
                'extra_stopwords_rus',
                'nltk_rus',
                'spacy_rus',
                'stopwords_iso_rus',
                'custom'
            ],

            'san': [
                'cltk_san',
                'spacy_san',
                'custom'
            ],

            'srp_cyrl': [
                'extra_stopwords_srp_cyrl',
                'spacy_srp_cyrl',
                'custom'
            ],
            'srp_latn': [
                'extra_stopwords_srp_latn',
                'spacy_srp_latn',
                'custom'
            ],

            'sin': [
                'spacy_sin',
                'custom'
            ],

            'slk': [
                'extra_stopwords_slk',
                'spacy_slk',
                'stopwords_iso_slk',
                'custom'
            ],

            'slv': [
                'extra_stopwords_slv',
                'nltk_slv',
                'spacy_slv',
                'stopwords_iso_slv',
                'custom'
            ],

            'som': [
                'stopwords_iso_som',
                'custom'
            ],

            'sot': [
                'stopwords_iso_sot',
                'custom'
            ],

            'spa': [
                'extra_stopwords_spa',
                'nltk_spa',
                'spacy_spa',
                'stopwords_iso_spa',
                'custom'
            ],

            'swa': [
                'extra_stopwords_swa',
                'stopwords_iso_swa',
                'custom'
            ],

            'swe': [
                'extra_stopwords_swe',
                'nltk_swe',
                'spacy_swe',
                'stopwords_iso_swe',
                'custom'
            ],

            'tgl': [
                'extra_stopwords_tgl',
                'spacy_tgl',
                'stopwords_iso_tgl',
                'custom'
            ],

            'tgk': [
                'nltk_tgk',
                'custom'
            ],

            'tam': [
                'spacy_tam',
                'custom'
            ],

            'tat': [
                'spacy_tat',
                'custom'
            ],

            'tel': [
                'extra_stopwords_tel',
                'spacy_tel',
                'custom'
            ],

            'tha': [
                'extra_stopwords_tha',
                'pythainlp_tha',
                'spacy_tha',
                'stopwords_iso_tha',
                'custom'
            ],

            'tir': [
                'spacy_tir',
                'custom'
            ],

            'tsn': [
                'spacy_tsn',
                'custom'
            ],

            'tur': [
                'extra_stopwords_tur',
                'nltk_tur',
                'spacy_tur',
                'stopwords_iso_tur',
                'custom'
            ],

            'ukr': [
                'extra_stopwords_ukr',
                'spacy_ukr',
                'stopwords_iso_ukr',
                'custom'
            ],

            'urd': [
                'extra_stopwords_urd',
                'spacy_urd',
                'stopwords_iso_urd',
                'custom'
            ],

            'vie': [
                'extra_stopwords_vie',
                'spacy_vie',
                'stopwords_iso_vie',
                'custom'
            ],

            'yor': [
                'extra_stopwords_yor',
                'spacy_yor',
                'stopwords_iso_yor',
                'custom'
            ],

            'zul': [
                'stopwords_iso_zul',
                'custom'
            ],

            'other': [
                'custom'
            ]
        },

        'measures_dispersion': {
            main.tr("Carroll's D₂"): {
                'col': main.tr("Carroll's D₂"),
                'func': wl_measures_dispersion.carrolls_d2
            },

            main.tr("Gries's DP"): {
                'col': main.tr("Gries's DP"),
                'func': wl_measures_dispersion.griess_dp
            },

            main.tr("Gries's DPnorm"): {
                'col': main.tr("Gries's DPnorm"),
                'func': wl_measures_dispersion.griess_dp_norm
            },

            main.tr("Juilland's D"): {
                'col': main.tr("Juilland's D"),
                'func': wl_measures_dispersion.juillands_d
            },

            main.tr("Lyne's D₃"): {
                'col': main.tr("Lyne's D₃"),
                'func': wl_measures_dispersion.lynes_d3
            },

            main.tr("Rosengren's S"): {
                'col': main.tr("Rosengren's S"),
                'func': wl_measures_dispersion.rosengrens_s
            },

            main.tr("Zhang's Distributional Consistency"): {
                'col': main.tr("Zhang's DC"),
                'func': wl_measures_dispersion.zhangs_distributional_consistency
            }
        },

        'measures_adjusted_freq': {
            main.tr("Carroll's Um"): {
                'col': main.tr("Carroll's Um"),
                'func': wl_measures_adjusted_freq.carrolls_um
            },

            main.tr("Engwall's FM"): {
                'col': main.tr("Engwall's FM"),
                'func': wl_measures_adjusted_freq.engwalls_fm
            },

            main.tr("Juilland's U"): {
                'col': main.tr("Juilland's U"),
                'func': wl_measures_adjusted_freq.juillands_u
            },

            main.tr("Kromer's UR"): {
                'col': main.tr("Kromer's UR"),
                'func': wl_measures_adjusted_freq.kromers_ur
            },

            main.tr("Rosengren's KF"): {
                'col': main.tr("Rosengren's KF"),
                'func': wl_measures_adjusted_freq.rosengrens_kf
            }
        },

        'tests_significance': {
            'collocation_extractor': {
                main.tr("Berry-Rogghe's z-score"): {
                    'cols': [
                        main.tr("Berry-Rogghe's z-score"),
                        main.tr('p-value'),
                        None
                    ],

                    'func': wl_measures_statistical_significance.berry_rogghes_z_score
                },

                main.tr("Fisher's Exact Test"): {
                    'cols': [
                        None,
                        main.tr('p-value'),
                        None
                    ],

                    'func': wl_measures_statistical_significance.fishers_exact_test
                },

                main.tr('Log-likelihood Ratio Test'): {
                    'cols': [
                        main.tr('Log-likelihood Ratio'),
                        main.tr('p-value'),
                        main.tr('Bayes Factor')
                    ],

                    'func': wl_measures_statistical_significance.log_likehood_ratio_test
                },

                main.tr("Pearson's Chi-squared Test"): {
                    'cols': [
                        main.tr('χ2'),
                        main.tr('p-value'),
                        None
                    ],

                    'func': wl_measures_statistical_significance.pearsons_chi_squared_test
                },

                main.tr("Student's t-test (1-sample)"): {
                    'cols': [
                        main.tr('t-statistic'),
                        main.tr('p-value'),
                        None
                    ],

                    'func': wl_measures_statistical_significance.students_t_test_1_sample
                },

                main.tr('z-score'): {
                    'cols': [
                        main.tr('z-score'),
                        main.tr('p-value'),
                        None
                    ],

                    'func': wl_measures_statistical_significance.z_score
                }
            },

            'keyword_extractor': {
                main.tr("Fisher's Exact Test"): {
                    'cols': [
                        None,
                        main.tr('p-value'),
                        None
                    ],

                    'func': wl_measures_statistical_significance.fishers_exact_test
                },

                main.tr('Log-likelihood Ratio Test'): {
                    'cols': [
                        main.tr('Log-likelihood Ratio'),
                        main.tr('p-value'),
                        main.tr('Bayes Factor')
                    ],

                    'func': wl_measures_statistical_significance.log_likehood_ratio_test
                },

                main.tr('Mann-Whitney U Test'): {
                    'cols': [
                        main.tr('U Statistic'),
                        main.tr('p-value'),
                        None
                    ],

                    'func': wl_measures_statistical_significance.mann_whitney_u_test
                },

                main.tr("Pearson's Chi-squared Test"): {
                    'cols': [
                        main.tr('χ2'),
                        main.tr('p-value'),
                        None
                    ],

                    'func': wl_measures_statistical_significance.pearsons_chi_squared_test
                },

                main.tr("Student's t-test (2-sample)"): {
                    'cols': [
                        main.tr('t-statistic'),
                        main.tr('p-value'),
                        main.tr('Bayes Factor')
                    ],

                    'func': wl_measures_statistical_significance.students_t_test_2_sample
                }
            }
        },

        'measures_effect_size': {
            'collocation_extractor': {
                main.tr('Cubic Association Ratio'): {
                    'col': main.tr('IM³'),
                    'func': wl_measures_effect_size.im3
                },

                main.tr("Dice's Coefficient"): {
                    'col': main.tr("Dice's Coefficient"),
                    'func': wl_measures_effect_size.dices_coeff
                },

                main.tr('Jaccard Index'): {
                    'col': main.tr('Jaccard Index'),
                    'func': wl_measures_effect_size.jaccard_index
                },

                main.tr('Log-Frequency Biased MD'): {
                    'col': main.tr('LFMD'),
                    'func': wl_measures_effect_size.lfmd
                },

                main.tr('logDice'): {
                    'col': main.tr('logDice'),
                    'func': wl_measures_effect_size.log_dice
                },

                main.tr('MI.log-f'): {
                    'col': main.tr('MI.log-f'),
                    'func': wl_measures_effect_size.mi_log_f
                },

                main.tr('Minimum Sensitivity'): {
                    'col': main.tr('Minimum Sensitivity'),
                    'func': wl_measures_effect_size.min_sensitivity
                },

                main.tr('Mutual Dependency'): {
                    'col': main.tr('MD'),
                    'func': wl_measures_effect_size.md
                },

                main.tr('Mutual Expectation'): {
                    'col': main.tr('ME'),
                    'func': wl_measures_effect_size.me
                },

                main.tr('Mutual Information'): {
                    'col': main.tr('MI'),
                    'func': wl_measures_effect_size.mi
                },

                main.tr('Pointwise Mutual Information'): {
                    'col': main.tr('PMI'),
                    'func': wl_measures_effect_size.pmi
                },

                main.tr('Poisson Collocation Measure'): {
                    'col': main.tr('Poisson Collocation Measure'),
                    'func': wl_measures_effect_size.poisson_collocation_measure
                },

                main.tr('Squared Phi Coefficient'): {
                    'col': main.tr('φ2'),
                    'func': wl_measures_effect_size.squared_phi_coeff
                }
            },

            'keyword_extractor': {
                main.tr('%DIFF'): {
                    'col': main.tr('%DIFF'),
                    'func': wl_measures_effect_size.pct_diff
                },

                main.tr('Difference Coefficient'): {
                    'col': main.tr('Difference Coefficient'),
                    'func': wl_measures_effect_size.diff_coeff
                },

                main.tr("Kilgarriff's Ratio"): {
                    'col': main.tr("Kilgarriff's Ratio"),
                    'func': wl_measures_effect_size.kilgarriffs_ratio
                },

                main.tr('Log Ratio'): {
                    'col': main.tr('Log Ratio'),
                    'func': wl_measures_effect_size.log_ratio
                },

                main.tr('Odds Ratio'): {
                    'col': main.tr('Odds Ratio'),
                    'func': wl_measures_effect_size.odds_ratio
                }
            }
        },

        'styles': {
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
                            margin-bottom: 3px;
                        }
                        div:last-child {
                            margin-bottom: 0;
                        }

                        ul {
                            margin-bottom: 3px;
                        }
                        ul:last-child {
                            margin-bottom: 0;
                        }

                        li {
                            margin-left: -30px;
                        }
                    </style>
                </head>
            '''
        }
    }
