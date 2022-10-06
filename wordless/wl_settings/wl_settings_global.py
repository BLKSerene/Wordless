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

from PyQt5.QtCore import QCoreApplication

from wordless.wl_measures import (
    wl_measures_adjusted_freq,
    wl_measures_bayes_factor,
    wl_measures_dispersion,
    wl_measures_effect_size,
    wl_measures_statistical_significance
)

_tr = QCoreApplication.translate

def init_settings_global():
    return {
        'langs': {
            _tr('init_settings_global', 'Afrikaans'): ['afr', 'af', 'Indo-European'],
            _tr('init_settings_global', 'Albanian'): ['sqi', 'sq', 'Indo-European'],
            _tr('init_settings_global', 'Amharic'): ['amh', 'am', 'Afro-Asiatic'],
            _tr('init_settings_global', 'Arabic'): ['ara', 'ar', 'Afro-Asiatic'],
            _tr('init_settings_global', 'Armenian'): ['hye', 'hy', 'Indo-European'],
            _tr('init_settings_global', 'Assamese'): ['asm', 'as', 'Indo-European'],
            _tr('init_settings_global', 'Asturian'): ['ast', 'ast', 'Indo-European'],
            _tr('init_settings_global', 'Azerbaijani'): ['aze', 'az', 'Turkic'],
            _tr('init_settings_global', 'Basque'): ['eus', 'eu', 'Language isolate'],
            _tr('init_settings_global', 'Belarusian'): ['bel', 'be', 'Indo-European'],
            _tr('init_settings_global', 'Bengali'): ['ben', 'bn', 'Indo-European'],
            _tr('init_settings_global', 'Breton'): ['bre', 'br', 'Indo-European'],
            _tr('init_settings_global', 'Bulgarian'): ['bul', 'bg', 'Indo-European'],
            _tr('init_settings_global', 'Burmese'): ['mya', 'my', 'Sino-Tibetan'],
            _tr('init_settings_global', 'Catalan'): ['cat', 'ca', 'Indo-European'],
            _tr('init_settings_global', 'Chinese (Simplified)'): ['zho_cn', 'zh_cn', 'Sino-Tibetan'],
            _tr('init_settings_global', 'Chinese (Traditional)'): ['zho_tw', 'zh_tw', 'Sino-Tibetan'],
            _tr('init_settings_global', 'Croatian'): ['hrv', 'hr', 'Indo-European'],
            _tr('init_settings_global', 'Czech'): ['ces', 'cs', 'Indo-European'],
            _tr('init_settings_global', 'Danish'): ['dan', 'da', 'Indo-European'],
            _tr('init_settings_global', 'Dutch'): ['nld', 'nl', 'Indo-European'],
            _tr('init_settings_global', 'English (Middle)'): ['enm', 'enm', 'Indo-European'],
            _tr('init_settings_global', 'English (United Kingdom)'): ['eng_gb', 'en_gb', 'Indo-European'],
            _tr('init_settings_global', 'English (United States)'): ['eng_us', 'en_us', 'Indo-European'],
            _tr('init_settings_global', 'Esperanto'): ['epo', 'eo', 'Constructed'],
            _tr('init_settings_global', 'Estonian'): ['est', 'et', 'Uralic'],
            _tr('init_settings_global', 'Finnish'): ['fin', 'fi', 'Uralic'],
            _tr('init_settings_global', 'French'): ['fra', 'fr', 'Indo-European'],
            _tr('init_settings_global', 'Galician'): ['glg', 'gl', 'Indo-European'],
            _tr('init_settings_global', 'Georgian'): ['kat', 'ka', 'Kartvelian'],
            _tr('init_settings_global', 'German (Austria)'): ['deu_at', 'de_at', 'Indo-European'],
            _tr('init_settings_global', 'German (Germany)'): ['deu_de', 'de_de', 'Indo-European'],
            _tr('init_settings_global', 'German (Switzerland)'): ['deu_ch', 'de_ch', 'Indo-European'],
            _tr('init_settings_global', 'Greek (Ancient)'): ['grc', 'grc', 'Unclassified'],
            _tr('init_settings_global', 'Greek (Modern)'): ['ell', 'el', 'Indo-European'],
            _tr('init_settings_global', 'Gujarati'): ['guj', 'gu', 'Indo-European'],
            _tr('init_settings_global', 'Hausa'): ['hau', 'ha', 'Afro-Asiatic'],
            _tr('init_settings_global', 'Hebrew'): ['heb', 'he', 'Afro-Asiatic'],
            _tr('init_settings_global', 'Hindi'): ['hin', 'hi', 'Indo-European'],
            _tr('init_settings_global', 'Hungarian'): ['hun', 'hu', 'Uralic'],
            _tr('init_settings_global', 'Icelandic'): ['isl', 'is', 'Indo-European'],
            _tr('init_settings_global', 'Indonesian'): ['ind', 'id', 'Austronesian'],
            _tr('init_settings_global', 'Irish'): ['gle', 'ga', 'Indo-European'],
            _tr('init_settings_global', 'Italian'): ['ita', 'it', 'Indo-European'],
            _tr('init_settings_global', 'Japanese'): ['jpn', 'ja', 'Japonic'],
            _tr('init_settings_global', 'Kannada'): ['kan', 'kn', 'Dravidian'],
            _tr('init_settings_global', 'Kazakh'): ['kaz', 'kk', 'Turkic'],
            _tr('init_settings_global', 'Korean'): ['kor', 'ko', 'Koreanic'],
            _tr('init_settings_global', 'Kurdish'): ['kur', 'ku', 'Indo-European'],
            _tr('init_settings_global', 'Kyrgyz'): ['kir', 'ky', 'Turkic'],
            _tr('init_settings_global', 'Latin'): ['lat', 'la', 'Indo-European'],
            _tr('init_settings_global', 'Latvian'): ['lav', 'lv', 'Indo-European'],
            _tr('init_settings_global', 'Ligurian'): ['lij', 'lij', 'Unclassified'],
            _tr('init_settings_global', 'Lithuanian'): ['lit', 'lt', 'Indo-European'],
            _tr('init_settings_global', 'Lugbara'): ['lgg', 'lgg', 'Unclassified'],
            _tr('init_settings_global', 'Luxembourgish'): ['ltz', 'lb', 'Indo-European'],
            _tr('init_settings_global', 'Macedonian'): ['mkd', 'mk', 'Indo-European'],
            _tr('init_settings_global', 'Malay'): ['msa', 'ms', 'Austronesian'],
            _tr('init_settings_global', 'Malayalam'): ['mal', 'ml', 'Dravidian'],
            _tr('init_settings_global', 'Manx'): ['glv', 'gv', 'Indo-European'],
            _tr('init_settings_global', 'Marathi'): ['mar', 'mr', 'Indo-European'],
            _tr('init_settings_global', 'Meitei'): ['mni', 'mni', 'Sino-Tibetan'],
            _tr('init_settings_global', 'Mongolian'): ['mon', 'mn', 'Mongolic'],
            _tr('init_settings_global', 'Nepali'): ['nep', 'ne', 'Indo-European'],
            _tr('init_settings_global', 'Norwegian Bokmål'): ['nob', 'nb', 'Indo-European'],
            _tr('init_settings_global', 'Norwegian Nynorsk'): ['nno', 'nn', 'Indo-European'],
            _tr('init_settings_global', 'Oriya'): ['ori', 'or', 'Indo-European'],
            _tr('init_settings_global', 'Persian'): ['fas', 'fa', 'Indo-European'],
            _tr('init_settings_global', 'Polish'): ['pol', 'pl', 'Indo-European'],
            _tr('init_settings_global', 'Portuguese (Brazil)'): ['por_br', 'pt_br', 'Indo-European'],
            _tr('init_settings_global', 'Portuguese (Portugal)'): ['por_pt', 'pt_pt', 'Indo-European'],
            _tr('init_settings_global', 'Punjabi (Gurmukhi)'): ['pan_guru', 'pa_guru', 'Indo-European'],
            _tr('init_settings_global', 'Romanian'): ['ron', 'ro', 'Indo-European'],
            _tr('init_settings_global', 'Russian'): ['rus', 'ru', 'Indo-European'],
            _tr('init_settings_global', 'Sámi (Northern)'): ['sme', 'se', 'Uralic'],
            _tr('init_settings_global', 'Sanskrit'): ['san', 'sa', 'Indo-European'],
            _tr('init_settings_global', 'Scottish Gaelic'): ['gla', 'gd', 'Indo-European'],
            _tr('init_settings_global', 'Serbian (Cyrillic)'): ['srp_cyrl', 'sr_cyrl', 'Indo-European'],
            _tr('init_settings_global', 'Serbian (Latin)'): ['srp_latn', 'sr_latn', 'Indo-European'],
            _tr('init_settings_global', 'Sinhala'): ['sin', 'si', 'Indo-European'],
            _tr('init_settings_global', 'Slovak'): ['slk', 'sk', 'Indo-European'],
            _tr('init_settings_global', 'Slovenian'): ['slv', 'sl', 'Indo-European'],
            _tr('init_settings_global', 'Somali'): ['som', 'so', 'Afro-Asiatic'],
            _tr('init_settings_global', 'Sorbian (Lower)'): ['dsb', 'dsb', 'Indo-European'],
            _tr('init_settings_global', 'Sorbian (Upper)'): ['hsb', 'hsb', 'Indo-European'],
            _tr('init_settings_global', 'Sotho (Southern)'): ['sot', 'st', 'Niger-Congo'],
            _tr('init_settings_global', 'Spanish'): ['spa', 'es', 'Indo-European'],
            _tr('init_settings_global', 'Swahili'): ['swa', 'sw', 'Niger-Congo'],
            _tr('init_settings_global', 'Swedish'): ['swe', 'sv', 'Indo-European'],
            _tr('init_settings_global', 'Tagalog'): ['tgl', 'tl', 'Austronesian'],
            _tr('init_settings_global', 'Tajik'): ['tgk', 'tg', 'Indo-European'],
            _tr('init_settings_global', 'Tamil'): ['tam', 'ta', 'Dravidian'],
            _tr('init_settings_global', 'Tatar'): ['tat', 'tt', 'Turkic'],
            _tr('init_settings_global', 'Telugu'): ['tel', 'te', 'Dravidian'],
            _tr('init_settings_global', 'Tetun Dili'): ['tdt', 'tdt', 'Unclassified'],
            _tr('init_settings_global', 'Thai'): ['tha', 'th', 'Tai-Kadai'],
            _tr('init_settings_global', 'Tibetan'): ['bod', 'bo', 'Sino-Tibetan'],
            _tr('init_settings_global', 'Tigrinya'): ['tir', 'ti', 'Afro-Asiatic'],
            _tr('init_settings_global', 'Tswana'): ['tsn', 'tn', 'Niger-Congo'],
            _tr('init_settings_global', 'Turkish'): ['tur', 'tr', 'Turkic'],
            _tr('init_settings_global', 'Ukrainian'): ['ukr', 'uk', 'Indo-European'],
            _tr('init_settings_global', 'Urdu'): ['urd', 'ur', 'Indo-European'],
            _tr('init_settings_global', 'Vietnamese'): ['vie', 'vi', 'Austroasiatic'],
            _tr('init_settings_global', 'Welsh'): ['cym', 'cy', 'Indo-European'],
            _tr('init_settings_global', 'Yoruba'): ['yor', 'yo', 'Niger-Congo'],
            _tr('init_settings_global', 'Zulu'): ['zul', 'zu', 'Niger-Congo'],

            _tr('init_settings_global', 'Other Languages'): ['other', 'other', 'Unclassified']
        },

        'encodings': {
            _tr('init_settings_global', 'All Languages (UTF-8 without BOM)'): 'utf_8',
            _tr('init_settings_global', 'All Languages (UTF-8 with BOM)'): 'utf_8_sig',
            _tr('init_settings_global', 'All Languages (UTF-16 with BOM)'): 'utf_16',
            _tr('init_settings_global', 'All Languages (UTF-16BE without BOM)'): 'utf_16_be',
            _tr('init_settings_global', 'All Languages (UTF-16LE without BOM)'): 'utf_16_le',
            _tr('init_settings_global', 'All Languages (UTF-32 with BOM)'): 'utf_32',
            _tr('init_settings_global', 'All Languages (UTF-32BE without BOM)'): 'utf_32_be',
            _tr('init_settings_global', 'All Languages (UTF-32LE without BOM)'): 'utf_32_le',
            _tr('init_settings_global', 'All Languages (UTF-7)'): 'utf_7',

            _tr('init_settings_global', 'Arabic (CP720)'): 'cp720',
            _tr('init_settings_global', 'Arabic (CP864)'): 'cp864',
            _tr('init_settings_global', 'Arabic (ISO-8859-6)'): 'iso8859_6',
            _tr('init_settings_global', 'Arabic (Mac OS Arabic)'): 'mac_arabic',
            _tr('init_settings_global', 'Arabic (Windows-1256)'): 'cp1256',

            _tr('init_settings_global', 'Baltic Languages (CP775)'): 'cp775',
            _tr('init_settings_global', 'Baltic Languages (ISO-8859-13)'): 'iso8859_13',
            _tr('init_settings_global', 'Baltic Languages (Windows-1257)'): 'cp1257',

            _tr('init_settings_global', 'Celtic Languages (ISO-8859-14)'): 'iso8859_14',

            _tr('init_settings_global', 'Chinese (GB18030)'): 'gb18030',
            _tr('init_settings_global', 'Chinese (GBK)'): 'gbk',

            _tr('init_settings_global', 'Chinese (Simplified) (GB2312)'): 'gb2312',
            _tr('init_settings_global', 'Chinese (Simplified) (HZ)'): 'hz_gb_2312',

            _tr('init_settings_global', 'Chinese (Traditional) (Big-5)'): 'big5',
            _tr('init_settings_global', 'Chinese (Traditional) (Big5-HKSCS)'): 'big5hkscs',
            _tr('init_settings_global', 'Chinese (Traditional) (CP950)'): 'cp950',

            _tr('init_settings_global', 'Croatian (Mac OS Croatian)'): 'mac_croatian',

            _tr('init_settings_global', 'Cyrillic (CP855)'): 'cp855',
            _tr('init_settings_global', 'Cyrillic (CP866)'): 'cp866',
            _tr('init_settings_global', 'Cyrillic (ISO-8859-5)'): 'iso8859_5',
            _tr('init_settings_global', 'Cyrillic (Mac OS Cyrillic)'): 'mac_cyrillic',
            _tr('init_settings_global', 'Cyrillic (Windows-1251)'): 'cp1251',

            _tr('init_settings_global', 'English (ASCII)'): 'ascii',
            _tr('init_settings_global', 'English (EBCDIC 037)'): 'cp037',
            _tr('init_settings_global', 'English (CP437)'): 'cp437',

            _tr('init_settings_global', 'European (HP Roman-8)'): 'hp_roman8',

            _tr('init_settings_global', 'European (Central) (CP852)'): 'cp852',
            _tr('init_settings_global', 'European (Central) (ISO-8859-2)'): 'iso8859_2',
            _tr('init_settings_global', 'European (Central) (Mac OS Central European)'): 'mac_latin2',
            _tr('init_settings_global', 'European (Central) (Windows-1250)'): 'cp1250',

            _tr('init_settings_global', 'European (Northern) (ISO-8859-4)'): 'iso8859_4',

            _tr('init_settings_global', 'European (Southern) (ISO-8859-3)'): 'iso8859_3',
            _tr('init_settings_global', 'European (South-Eastern) (ISO-8859-16)'): 'iso8859_16',

            _tr('init_settings_global', 'European (Western) (EBCDIC 500)'): 'cp500',
            _tr('init_settings_global', 'European (Western) (CP850)'): 'cp850',
            _tr('init_settings_global', 'European (Western) (CP858)'): 'cp858',
            _tr('init_settings_global', 'European (Western) (CP1140)'): 'cp1140',
            _tr('init_settings_global', 'European (Western) (ISO-8859-1)'): 'latin_1',
            _tr('init_settings_global', 'European (Western) (ISO-8859-15)'): 'iso8859_15',
            _tr('init_settings_global', 'European (Western) (Mac OS Roman)'): 'mac_roman',
            _tr('init_settings_global', 'European (Western) (Windows-1252)'): 'windows_1252',

            _tr('init_settings_global', 'French (CP863)'): 'cp863',

            _tr('init_settings_global', 'German (EBCDIC 273)'): 'cp273',

            _tr('init_settings_global', 'Greek (CP737)'): 'cp737',
            _tr('init_settings_global', 'Greek (CP869)'): 'cp869',
            _tr('init_settings_global', 'Greek (CP875)'): 'cp875',
            _tr('init_settings_global', 'Greek (ISO-8859-7)'): 'iso8859_7',
            _tr('init_settings_global', 'Greek (Mac OS Greek)'): 'mac_greek',
            _tr('init_settings_global', 'Greek (Windows-1253)'): 'windows_1253',

            _tr('init_settings_global', 'Hebrew (CP856)'): 'cp856',
            _tr('init_settings_global', 'Hebrew (CP862)'): 'cp862',
            _tr('init_settings_global', 'Hebrew (EBCDIC 424)'): 'cp424',
            _tr('init_settings_global', 'Hebrew (ISO-8859-8)'): 'iso8859_8',
            _tr('init_settings_global', 'Hebrew (Windows-1255)'): 'windows_1255',

            _tr('init_settings_global', 'Icelandic (CP861)'): 'cp861',
            _tr('init_settings_global', 'Icelandic (Mac OS Icelandic)'): 'mac_iceland',

            _tr('init_settings_global', 'Japanese (CP932)'): 'cp932',
            _tr('init_settings_global', 'Japanese (EUC-JP)'): 'euc_jp',
            _tr('init_settings_global', 'Japanese (EUC-JIS-2004)'): 'euc_jis_2004',
            _tr('init_settings_global', 'Japanese (EUC-JISx0213)'): 'euc_jisx0213',
            _tr('init_settings_global', 'Japanese (ISO-2022-JP)'): 'iso2022_jp',
            _tr('init_settings_global', 'Japanese (ISO-2022-JP-1)'): 'iso2022_jp_1',
            _tr('init_settings_global', 'Japanese (ISO-2022-JP-2)'): 'iso2022_jp_2',
            _tr('init_settings_global', 'Japanese (ISO-2022-JP-2004)'): 'iso2022_jp_2004',
            _tr('init_settings_global', 'Japanese (ISO-2022-JP-3)'): 'iso2022_jp_3',
            _tr('init_settings_global', 'Japanese (ISO-2022-JP-EXT)'): 'iso2022_jp_ext',
            _tr('init_settings_global', 'Japanese (Shift_JIS)'): 'shift_jis',
            _tr('init_settings_global', 'Japanese (Shift_JIS-2004)'): 'shift_jis_2004',
            _tr('init_settings_global', 'Japanese (Shift_JISx0213)'): 'shift_jisx0213',

            _tr('init_settings_global', 'Kazakh (KZ-1048)'): 'kz1048',
            _tr('init_settings_global', 'Kazakh (PTCP154)'): 'ptcp154',

            _tr('init_settings_global', 'Korean (EUC-KR)'): 'euc_kr',
            _tr('init_settings_global', 'Korean (ISO-2022-KR)'): 'iso2022_kr',
            _tr('init_settings_global', 'Korean (JOHAB)'): 'johab',
            _tr('init_settings_global', 'Korean (UHC)'): 'cp949',

            _tr('init_settings_global', 'Nordic Languages (CP865)'): 'cp865',
            _tr('init_settings_global', 'Nordic Languages (ISO-8859-10)'): 'iso8859_10',

            _tr('init_settings_global', 'Persian/Urdu (Mac OS Farsi)'): 'mac_farsi',

            _tr('init_settings_global', 'Portuguese (CP860)'): 'cp860',

            _tr('init_settings_global', 'Romanian (Mac OS Romanian)'): 'mac_romanian',

            _tr('init_settings_global', 'Russian (KOI8-R)'): 'koi8_r',

            _tr('init_settings_global', 'Tajik (KOI8-T)'): 'koi8_t',

            _tr('init_settings_global', 'Thai (CP874)'): 'cp874',
            _tr('init_settings_global', 'Thai (ISO-8859-11)'): 'iso8859_11',

            _tr('init_settings_global', 'Turkish (CP857)'): 'cp857',
            _tr('init_settings_global', 'Turkish (EBCDIC 1026)'): 'cp1026',
            _tr('init_settings_global', 'Turkish (ISO-8859-9)'): 'iso8859_9',
            _tr('init_settings_global', 'Turkish (Mac OS Turkish)'): 'mac_turkish',
            _tr('init_settings_global', 'Turkish (Windows-1254)'): 'cp1254',

            _tr('init_settings_global', 'Ukrainian (CP1125)'): 'cp1125',
            _tr('init_settings_global', 'Ukrainian (KOI8-U)'): 'koi8_u',

            _tr('init_settings_global', 'Urdu (CP1006)'): 'cp1006',

            _tr('init_settings_global', 'Vietnamese (CP1258)'): 'cp1258',
        },

        'file_types': {
            'files': [
                _tr('init_settings_global', 'CSV File (*.csv)'),
                _tr('init_settings_global', 'Excel Workbook (*.xlsx)'),
                _tr('init_settings_global', 'HTML Page (*.htm; *.html)'),
                _tr('init_settings_global', 'PDF File (*.pdf)'),
                _tr('init_settings_global', 'Text File (*.txt)'),
                _tr('init_settings_global', 'Translation Memory File (*.tmx)'),
                _tr('init_settings_global', 'Word Document (*.docx)'),
                _tr('init_settings_global', 'XML File (*.xml)'),
                _tr('init_settings_global', 'All Files (*.*)')
            ],

            'exp_tables': [
                _tr('init_settings_global', 'CSV File (*.csv)'),
                _tr('init_settings_global', 'Excel Workbook (*.xlsx)')
            ],
            'exp_tables_concordancer': [
                _tr('init_settings_global', 'CSV File (*.csv)'),
                _tr('init_settings_global', 'Excel Workbook (*.xlsx)'),
                _tr('init_settings_global', 'Word Document (*.docx)')
            ],
            'exp_tables_concordancer_zapping': [
                _tr('init_settings_global', 'Word Document (*.docx)')
            ],

            'fonts': [
                _tr('init_settings_global', 'OpenType Font (*.otf)'),
                _tr('init_settings_global', 'TrueType Font (*.ttf)')
            ]
        },

        'lang_util_mappings': {
            'sentence_tokenizers': {
                _tr('init_settings_global', 'botok - Tibetan Sentence Tokenizer'): 'botok_bod',

                _tr('init_settings_global', 'NLTK - Czech Punkt Sentence Tokenizer'): 'nltk_punkt_ces',
                _tr('init_settings_global', 'NLTK - Danish Punkt Sentence Tokenizer'): 'nltk_punkt_dan',
                _tr('init_settings_global', 'NLTK - Dutch Punkt Sentence Tokenizer'): 'nltk_punkt_nld',
                _tr('init_settings_global', 'NLTK - English Punkt Sentence Tokenizer'): 'nltk_punkt_eng',
                _tr('init_settings_global', 'NLTK - Estonian Punkt Sentence Tokenizer'): 'nltk_punkt_est',
                _tr('init_settings_global', 'NLTK - Finnish Punkt Sentence Tokenizer'): 'nltk_punkt_fin',
                _tr('init_settings_global', 'NLTK - French Punkt Sentence Tokenizer'): 'nltk_punkt_fra',
                _tr('init_settings_global', 'NLTK - German Punkt Sentence Tokenizer'): 'nltk_punkt_deu',
                _tr('init_settings_global', 'NLTK - Greek Punkt Sentence Tokenizer'): 'nltk_punkt_ell',
                _tr('init_settings_global', 'NLTK - Italian Punkt Sentence Tokenizer'): 'nltk_punkt_ita',
                _tr('init_settings_global', 'NLTK - Malayalam Punkt Sentence Tokenizer'): 'nltk_punkt_mal',
                _tr('init_settings_global', 'NLTK - Norwegian Punkt Sentence Tokenizer'): 'nltk_punkt_nor',
                _tr('init_settings_global', 'NLTK - Polish Punkt Sentence Tokenizer'): 'nltk_punkt_pol',
                _tr('init_settings_global', 'NLTK - Portuguese Punkt Sentence Tokenizer'): 'nltk_punkt_por',
                _tr('init_settings_global', 'NLTK - Russian Punkt Sentence Tokenizer'): 'nltk_punkt_rus',
                _tr('init_settings_global', 'NLTK - Slovenian Punkt Sentence Tokenizer'): 'nltk_punkt_slv',
                _tr('init_settings_global', 'NLTK - Spanish Punkt Sentence Tokenizer'): 'nltk_punkt_spa',
                _tr('init_settings_global', 'NLTK - Swedish Punkt Sentence Tokenizer'): 'nltk_punkt_swe',
                _tr('init_settings_global', 'NLTK - Turkish Punkt Sentence Tokenizer'): 'nltk_punkt_tur',

                _tr('init_settings_global', 'PyThaiNLP - CRFCut'): 'pythainlp_crfcut',
                _tr('init_settings_global', 'PyThaiNLP - ThaiSumCut'): 'pythainlp_thaisumcut',

                _tr('init_settings_global', 'spaCy - Sentence Recognizer'): 'spacy_sentence_recognizer',
                _tr('init_settings_global', 'spaCy - Sentencizer'): 'spacy_sentencizer',

                _tr('init_settings_global', 'Underthesea - Vietnamese Sentence Tokenizer'): 'underthesea_vie',

                _tr('init_settings_global', 'Wordless - Chinese Sentence Tokenizer'): 'wordless_zho',
                _tr('init_settings_global', 'Wordless - Japanese Sentence Tokenizer'): 'wordless_jpn'
            },

            'word_tokenizers': {
                _tr('init_settings_global', 'botok - Tibetan Word Tokenizer'): 'botok_bod',
                _tr('init_settings_global', 'jieba - Chinese Word Tokenizer'): 'jieba_zho',

                _tr('init_settings_global', 'NLTK - NIST Tokenizer'): 'nltk_nist',
                _tr('init_settings_global', 'NLTK - NLTK Tokenizer'): 'nltk_nltk',
                _tr('init_settings_global', 'NLTK - Penn Treebank Tokenizer'): 'nltk_penn_treebank',
                _tr('init_settings_global', 'NLTK - Regular-Expression Tokenizer'): 'nltk_regex',
                _tr('init_settings_global', 'NLTK - Tok-tok Tokenizer'): 'nltk_tok_tok',
                _tr('init_settings_global', 'NLTK - Twitter Tokenizer'): 'nltk_twitter',

                _tr('init_settings_global', 'pkuseg - Chinese Word Tokenizer'): 'pkuseg_zho',

                _tr('init_settings_global', 'PyThaiNLP - Longest Matching'): 'pythainlp_longest_matching',
                _tr('init_settings_global', 'PyThaiNLP - Maximum Matching'): 'pythainlp_max_matching',
                _tr('init_settings_global', 'PyThaiNLP - Maximum Matching + TCC'): 'pythainlp_max_matching_tcc',
                _tr('init_settings_global', 'PyThaiNLP - NERCut'): 'pythainlp_nercut',

                _tr('init_settings_global', 'Sacremoses - Moses Tokenizer'): 'sacremoses_moses',

                _tr('init_settings_global', 'spaCy - Afrikaans Word Tokenizer'): 'spacy_afr',
                _tr('init_settings_global', 'spaCy - Albanian Word Tokenizer'): 'spacy_sqi',
                _tr('init_settings_global', 'spaCy - Amharic Word Tokenizer'): 'spacy_amh',
                _tr('init_settings_global', 'spaCy - Arabic Word Tokenizer'): 'spacy_ara',
                _tr('init_settings_global', 'spaCy - Armenian Word Tokenizer'): 'spacy_hye',
                _tr('init_settings_global', 'spaCy - Azerbaijani Word Tokenizer'): 'spacy_aze',
                _tr('init_settings_global', 'spaCy - Basque Word Tokenizer'): 'spacy_eus',
                _tr('init_settings_global', 'spaCy - Bengali Word Tokenizer'): 'spacy_ben',
                _tr('init_settings_global', 'spaCy - Bulgarian Word Tokenizer'): 'spacy_bul',
                _tr('init_settings_global', 'spaCy - Catalan Word Tokenizer'): 'spacy_cat',
                _tr('init_settings_global', 'spaCy - Chinese Word Tokenizer'): 'spacy_zho',
                _tr('init_settings_global', 'spaCy - Croatian Word Tokenizer'): 'spacy_hrv',
                _tr('init_settings_global', 'spaCy - Czech Word Tokenizer'): 'spacy_ces',
                _tr('init_settings_global', 'spaCy - Danish Word Tokenizer'): 'spacy_dan',
                _tr('init_settings_global', 'spaCy - Dutch Word Tokenizer'): 'spacy_nld',
                _tr('init_settings_global', 'spaCy - English Word Tokenizer'): 'spacy_eng',
                _tr('init_settings_global', 'spaCy - Estonian Word Tokenizer'): 'spacy_est',
                _tr('init_settings_global', 'spaCy - Finnish Word Tokenizer'): 'spacy_fin',
                _tr('init_settings_global', 'spaCy - French Word Tokenizer'): 'spacy_fra',
                _tr('init_settings_global', 'spaCy - German Word Tokenizer'): 'spacy_deu',
                _tr('init_settings_global', 'spaCy - Greek (Ancient) Word Tokenizer'): 'spacy_grc',
                _tr('init_settings_global', 'spaCy - Greek (Modern) Word Tokenizer'): 'spacy_ell',
                _tr('init_settings_global', 'spaCy - Gujarati Word Tokenizer'): 'spacy_guj',
                _tr('init_settings_global', 'spaCy - Hebrew Word Tokenizer'): 'spacy_heb',
                _tr('init_settings_global', 'spaCy - Hindi Word Tokenizer'): 'spacy_hin',
                _tr('init_settings_global', 'spaCy - Hungarian Word Tokenizer'): 'spacy_hun',
                _tr('init_settings_global', 'spaCy - Icelandic Word Tokenizer'): 'spacy_isl',
                _tr('init_settings_global', 'spaCy - Indonesian Word Tokenizer'): 'spacy_ind',
                _tr('init_settings_global', 'spaCy - Irish Word Tokenizer'): 'spacy_gle',
                _tr('init_settings_global', 'spaCy - Italian Word Tokenizer'): 'spacy_ita',
                _tr('init_settings_global', 'spaCy - Japanese Word Tokenizer'): 'spacy_jpn',
                _tr('init_settings_global', 'spaCy - Kannada Word Tokenizer'): 'spacy_kan',
                _tr('init_settings_global', 'spaCy - Kyrgyz Word Tokenizer'): 'spacy_kir',
                _tr('init_settings_global', 'spaCy - Latvian Word Tokenizer'): 'spacy_lav',
                _tr('init_settings_global', 'spaCy - Ligurian Word Tokenizer'): 'spacy_lij',
                _tr('init_settings_global', 'spaCy - Lithuanian Word Tokenizer'): 'spacy_lit',
                _tr('init_settings_global', 'spaCy - Luxembourgish Word Tokenizer'): 'spacy_ltz',
                _tr('init_settings_global', 'spaCy - Macedonian Word Tokenizer'): 'spacy_mkd',
                _tr('init_settings_global', 'spaCy - Malayalam Word Tokenizer'): 'spacy_mal',
                _tr('init_settings_global', 'spaCy - Marathi Word Tokenizer'): 'spacy_mar',
                _tr('init_settings_global', 'spaCy - Nepali Word Tokenizer'): 'spacy_nep',
                _tr('init_settings_global', 'spaCy - Norwegian Word Tokenizer'): 'spacy_nob',
                _tr('init_settings_global', 'spaCy - Persian Word Tokenizer'): 'spacy_fas',
                _tr('init_settings_global', 'spaCy - Polish Word Tokenizer'): 'spacy_pol',
                _tr('init_settings_global', 'spaCy - Portuguese Word Tokenizer'): 'spacy_por',
                _tr('init_settings_global', 'spaCy - Romanian Word Tokenizer'): 'spacy_ron',
                _tr('init_settings_global', 'spaCy - Russian Word Tokenizer'): 'spacy_rus',
                _tr('init_settings_global', 'spaCy - Sanskrit Word Tokenizer'): 'spacy_san',
                _tr('init_settings_global', 'spaCy - Serbian Word Tokenizer'): 'spacy_srp',
                _tr('init_settings_global', 'spaCy - Sinhala Word Tokenizer'): 'spacy_sin',
                _tr('init_settings_global', 'spaCy - Slovak Word Tokenizer'): 'spacy_slk',
                _tr('init_settings_global', 'spaCy - Slovenian Word Tokenizer'): 'spacy_slv',
                _tr('init_settings_global', 'spaCy - Sorbian (Lower) Word Tokenizer'): 'spacy_dsb',
                _tr('init_settings_global', 'spaCy - Sorbian (Upper) Word Tokenizer'): 'spacy_hsb',
                _tr('init_settings_global', 'spaCy - Spanish Word Tokenizer'): 'spacy_spa',
                _tr('init_settings_global', 'spaCy - Swedish Word Tokenizer'): 'spacy_swe',
                _tr('init_settings_global', 'spaCy - Tagalog Word Tokenizer'): 'spacy_tgl',
                _tr('init_settings_global', 'spaCy - Tamil Word Tokenizer'): 'spacy_tam',
                _tr('init_settings_global', 'spaCy - Tatar Word Tokenizer'): 'spacy_tat',
                _tr('init_settings_global', 'spaCy - Telugu Word Tokenizer'): 'spacy_tel',
                _tr('init_settings_global', 'spaCy - Tigrinya Word Tokenizer'): 'spacy_tir',
                _tr('init_settings_global', 'spaCy - Tswana Word Tokenizer'): 'spacy_tsn',
                _tr('init_settings_global', 'spaCy - Turkish Word Tokenizer'): 'spacy_tur',
                _tr('init_settings_global', 'spaCy - Ukrainian Word Tokenizer'): 'spacy_ukr',
                _tr('init_settings_global', 'spaCy - Urdu Word Tokenizer'): 'spacy_urd',
                _tr('init_settings_global', 'spaCy - Yoruba Word Tokenizer'): 'spacy_yor',

                _tr('init_settings_global', 'SudachiPy - Japanese Word Tokenizer (Split Mode A)'): 'sudachipy_jpn_split_mode_a',
                _tr('init_settings_global', 'SudachiPy - Japanese Word Tokenizer (Split Mode B)'): 'sudachipy_jpn_split_mode_b',
                _tr('init_settings_global', 'SudachiPy - Japanese Word Tokenizer (Split Mode C)'): 'sudachipy_jpn_split_mode_c',

                _tr('init_settings_global', 'Underthesea - Vietnamese Word Tokenizer'): 'underthesea_vie',

                _tr('init_settings_global', 'Wordless - Chinese Character Tokenizer'): 'wordless_zho_char',
                _tr('init_settings_global', 'Wordless - Japanese Kanji Tokenizer'): 'wordless_jpn_kanji'
            },

            'syl_tokenizers': {
                _tr('init_settings_global', 'NLTK - Legality Syllable Tokenizer'): 'nltk_legality',
                _tr('init_settings_global', 'NLTK - Sonority Sequencing Syllable Tokenizer'): 'nltk_sonority_sequencing',

                _tr('init_settings_global', 'Pyphen - Afrikaans Syllable Tokenizer'): 'pyphen_afr',
                _tr('init_settings_global', 'Pyphen - Albanian Syllable Tokenizer'): 'pyphen_sqi',
                _tr('init_settings_global', 'Pyphen - Belarusian Syllable Tokenizer'): 'pyphen_bel',
                _tr('init_settings_global', 'Pyphen - Bulgarian Syllable Tokenizer'): 'pyphen_bul',
                _tr('init_settings_global', 'Pyphen - Catalan Syllable Tokenizer'): 'pyphen_cat',
                _tr('init_settings_global', 'Pyphen - Croatian Syllable Tokenizer'): 'pyphen_hrv',
                _tr('init_settings_global', 'Pyphen - Czech Syllable Tokenizer'): 'pyphen_ces',
                _tr('init_settings_global', 'Pyphen - Danish Syllable Tokenizer'): 'pyphen_dan',
                _tr('init_settings_global', 'Pyphen - Dutch Syllable Tokenizer'): 'pyphen_nld',
                _tr('init_settings_global', 'Pyphen - English (United Kingdom) Syllable Tokenizer'): 'pyphen_eng_gb',
                _tr('init_settings_global', 'Pyphen - English (United States) Syllable Tokenizer'): 'pyphen_eng_us',
                _tr('init_settings_global', 'Pyphen - Esperanto Syllable Tokenizer'): 'pyphen_epo',
                _tr('init_settings_global', 'Pyphen - Estonian Syllable Tokenizer'): 'pyphen_est',
                _tr('init_settings_global', 'Pyphen - French Syllable Tokenizer'): 'pyphen_fra',
                _tr('init_settings_global', 'Pyphen - Galician Syllable Tokenizer'): 'pyphen_glg',
                _tr('init_settings_global', 'Pyphen - German (Austria) Syllable Tokenizer'): 'pyphen_deu_at',
                _tr('init_settings_global', 'Pyphen - German (Germany) Syllable Tokenizer'): 'pyphen_deu_de',
                _tr('init_settings_global', 'Pyphen - German (Switzerland) Syllable Tokenizer'): 'pyphen_deu_ch',
                _tr('init_settings_global', 'Pyphen - Greek (Modern) Syllable Tokenizer'): 'pyphen_ell',
                _tr('init_settings_global', 'Pyphen - Hungarian Syllable Tokenizer'): 'pyphen_hun',
                _tr('init_settings_global', 'Pyphen - Icelandic Syllable Tokenizer'): 'pyphen_isl',
                _tr('init_settings_global', 'Pyphen - Indonesian Syllable Tokenizer'): 'pyphen_ind',
                _tr('init_settings_global', 'Pyphen - Italian Syllable Tokenizer'): 'pyphen_ita',
                _tr('init_settings_global', 'Pyphen - Lithuanian Syllable Tokenizer'): 'pyphen_lit',
                _tr('init_settings_global', 'Pyphen - Latvian Syllable Tokenizer'): 'pyphen_lav',
                _tr('init_settings_global', 'Pyphen - Mongolian Syllable Tokenizer'): 'pyphen_mon',
                _tr('init_settings_global', 'Pyphen - Norwegian Bokmål Syllable Tokenizer'): 'pyphen_nob',
                _tr('init_settings_global', 'Pyphen - Norwegian Nynorsk Syllable Tokenizer'): 'pyphen_nno',
                _tr('init_settings_global', 'Pyphen - Polish Syllable Tokenizer'): 'pyphen_pol',
                _tr('init_settings_global', 'Pyphen - Portuguese (Brazil) Syllable Tokenizer'): 'pyphen_por_br',
                _tr('init_settings_global', 'Pyphen - Portuguese (Portugal) Syllable Tokenizer'): 'pyphen_por_pt',
                _tr('init_settings_global', 'Pyphen - Romanian Syllable Tokenizer'): 'pyphen_ron',
                _tr('init_settings_global', 'Pyphen - Russian Syllable Tokenizer'): 'pyphen_rus',
                _tr('init_settings_global', 'Pyphen - Serbian (Cyrillic) Syllable Tokenizer'): 'pyphen_srp_cyrl',
                _tr('init_settings_global', 'Pyphen - Serbian (Latin) Syllable Tokenizer'): 'pyphen_srp_latn',
                _tr('init_settings_global', 'Pyphen - Slovak Syllable Tokenizer'): 'pyphen_slk',
                _tr('init_settings_global', 'Pyphen - Slovenian Syllable Tokenizer'): 'pyphen_slv',
                _tr('init_settings_global', 'Pyphen - Spanish Syllable Tokenizer'): 'pyphen_spa',
                _tr('init_settings_global', 'Pyphen - Swedish Syllable Tokenizer'): 'pyphen_swe',
                _tr('init_settings_global', 'Pyphen - Telugu Syllable Tokenizer'): 'pyphen_tel',
                _tr('init_settings_global', 'Pyphen - Ukrainian Syllable Tokenizer'): 'pyphen_ukr',
                _tr('init_settings_global', 'Pyphen - Zulu Syllable Tokenizer'): 'pyphen_zul',

                _tr('init_settings_global', 'PyThaiNLP - Thai Syllable Tokenizer'): 'pythainlp_tha'
            },

            'pos_taggers': {
                _tr('init_settings_global', 'botok - Tibetan Part-of-speech Tagger'): 'botok_bod',
                _tr('init_settings_global', 'jieba - Chinese Part-of-speech Tagger'): 'jieba_zho',

                _tr('init_settings_global', 'NLTK - English Perceptron Part-of-speech Tagger'): 'nltk_perceptron_eng',
                _tr('init_settings_global', 'NLTK - Russian Perceptron Part-of-speech Tagger'): 'nltk_perceptron_rus',

                _tr('init_settings_global', 'pymorphy2 - Morphological Analyzer'): 'pymorphy2_morphological_analyzer',

                _tr('init_settings_global', 'PyThaiNLP - Perceptron Part-of-speech Tagger (LST20)'): 'pythainlp_perceptron_lst20',
                _tr('init_settings_global', 'PyThaiNLP - Perceptron Part-of-speech Tagger (ORCHID)'): 'pythainlp_perceptron_orchid',
                _tr('init_settings_global', 'PyThaiNLP - Perceptron Part-of-speech Tagger (PUD)'): 'pythainlp_perceptron_pud',

                _tr('init_settings_global', 'spaCy - Catalan Part-of-speech Tagger'): 'spacy_cat',
                _tr('init_settings_global', 'spaCy - Chinese Part-of-speech Tagger'): 'spacy_zho',
                _tr('init_settings_global', 'spaCy - Croatian Part-of-speech Tagger'): 'spacy_hrv',
                _tr('init_settings_global', 'spaCy - Danish Part-of-speech Tagger'): 'spacy_dan',
                _tr('init_settings_global', 'spaCy - Dutch Part-of-speech Tagger'): 'spacy_nld',
                _tr('init_settings_global', 'spaCy - English Part-of-speech Tagger'): 'spacy_eng',
                _tr('init_settings_global', 'spaCy - Finnish Part-of-speech Tagger'): 'spacy_fin',
                _tr('init_settings_global', 'spaCy - French Part-of-speech Tagger'): 'spacy_fra',
                _tr('init_settings_global', 'spaCy - German Part-of-speech Tagger'): 'spacy_deu',
                _tr('init_settings_global', 'spaCy - Greek (Modern) Part-of-speech Tagger'): 'spacy_ell',
                _tr('init_settings_global', 'spaCy - Italian Part-of-speech Tagger'): 'spacy_ita',
                _tr('init_settings_global', 'spaCy - Japanese Part-of-speech Tagger'): 'spacy_jpn',
                _tr('init_settings_global', 'spaCy - Lithuanian Part-of-speech Tagger'): 'spacy_lit',
                _tr('init_settings_global', 'spaCy - Macedonian Part-of-speech Tagger'): 'spacy_mkd',
                _tr('init_settings_global', 'spaCy - Norwegian Bokmål Part-of-speech Tagger'): 'spacy_nob',
                _tr('init_settings_global', 'spaCy - Polish Part-of-speech Tagger'): 'spacy_pol',
                _tr('init_settings_global', 'spaCy - Portuguese Part-of-speech Tagger'): 'spacy_por',
                _tr('init_settings_global', 'spaCy - Romanian Part-of-speech Tagger'): 'spacy_ron',
                _tr('init_settings_global', 'spaCy - Russian Part-of-speech Tagger'): 'spacy_rus',
                _tr('init_settings_global', 'spaCy - Spanish Part-of-speech Tagger'): 'spacy_spa',
                _tr('init_settings_global', 'spaCy - Swedish Part-of-speech Tagger'): 'spacy_swe',
                _tr('init_settings_global', 'spaCy - Ukrainian Part-of-speech Tagger'): 'spacy_ukr',

                _tr('init_settings_global', 'SudachiPy - Japanese Part-of-speech Tagger'): 'sudachipy_jpn',

                _tr('init_settings_global', 'Underthesea - Vietnamese Part-of-speech Tagger'): 'underthesea_vie'
            },

            'lemmatizers': {
                _tr('init_settings_global', 'botok - Tibetan Lemmatizer'): 'botok_bod',

                _tr('init_settings_global', 'NLTK - WordNet Lemmatizer'): 'nltk_wordnet',
                _tr('init_settings_global', 'pymorphy2 - Morphological Analyzer'): 'pymorphy2_morphological_analyzer',

                _tr('init_settings_global', 'simplemma - Albanian Lemmatizer'): 'simplemma_sqi',
                _tr('init_settings_global', 'simplemma - Armenian Lemmatizer'): 'simplemma_hye',
                _tr('init_settings_global', 'simplemma - Bulgarian Lemmatizer'): 'simplemma_bul',
                _tr('init_settings_global', 'simplemma - Catalan Lemmatizer'): 'simplemma_cat',
                _tr('init_settings_global', 'simplemma - Czech Lemmatizer'): 'simplemma_ces',
                _tr('init_settings_global', 'simplemma - Danish Lemmatizer'): 'simplemma_dan',
                _tr('init_settings_global', 'simplemma - Dutch Lemmatizer'): 'simplemma_nld',
                _tr('init_settings_global', 'simplemma - English Lemmatizer'): 'simplemma_eng',
                _tr('init_settings_global', 'simplemma - English (Middle) Lemmatizer'): 'simplemma_enm',
                _tr('init_settings_global', 'simplemma - Estonian Lemmatizer'): 'simplemma_est',
                _tr('init_settings_global', 'simplemma - Finnish Lemmatizer'): 'simplemma_fin',
                _tr('init_settings_global', 'simplemma - French Lemmatizer'): 'simplemma_fra',
                _tr('init_settings_global', 'simplemma - Galician Lemmatizer'): 'simplemma_glg',
                _tr('init_settings_global', 'simplemma - Georgian Lemmatizer'): 'simplemma_kat',
                _tr('init_settings_global', 'simplemma - German Lemmatizer'): 'simplemma_deu',
                _tr('init_settings_global', 'simplemma - Greek (Modern) Lemmatizer'): 'simplemma_ell',
                _tr('init_settings_global', 'simplemma - Hindi Lemmatizer'): 'simplemma_hin',
                _tr('init_settings_global', 'simplemma - Hungarian Lemmatizer'): 'simplemma_hun',
                _tr('init_settings_global', 'simplemma - Icelandic Lemmatizer'): 'simplemma_isl',
                _tr('init_settings_global', 'simplemma - Indonesian Lemmatizer'): 'simplemma_ind',
                _tr('init_settings_global', 'simplemma - Irish Lemmatizer'): 'simplemma_gle',
                _tr('init_settings_global', 'simplemma - Italian Lemmatizer'): 'simplemma_ita',
                _tr('init_settings_global', 'simplemma - Latin Lemmatizer'): 'simplemma_lat',
                _tr('init_settings_global', 'simplemma - Latvian Lemmatizer'): 'simplemma_lav',
                _tr('init_settings_global', 'simplemma - Lithuanian Lemmatizer'): 'simplemma_lit',
                _tr('init_settings_global', 'simplemma - Luxembourgish Lemmatizer'): 'simplemma_ltz',
                _tr('init_settings_global', 'simplemma - Macedonian Lemmatizer'): 'simplemma_mkd',
                _tr('init_settings_global', 'simplemma - Malay Lemmatizer'): 'simplemma_msa',
                _tr('init_settings_global', 'simplemma - Manx Lemmatizer'): 'simplemma_glv',
                _tr('init_settings_global', 'simplemma - Norwegian Bokmål Lemmatizer'): 'simplemma_nob',
                _tr('init_settings_global', 'simplemma - Norwegian Nynorsk Lemmatizer'): 'simplemma_nno',
                _tr('init_settings_global', 'simplemma - Persian Lemmatizer'): 'simplemma_fas',
                _tr('init_settings_global', 'simplemma - Polish Lemmatizer'): 'simplemma_pol',
                _tr('init_settings_global', 'simplemma - Portuguese Lemmatizer'): 'simplemma_por',
                _tr('init_settings_global', 'simplemma - Romanian Lemmatizer'): 'simplemma_ron',
                _tr('init_settings_global', 'simplemma - Russian Lemmatizer'): 'simplemma_rus',
                _tr('init_settings_global', 'simplemma - Sámi (Northern) Lemmatizer'): 'simplemma_sme',
                _tr('init_settings_global', 'simplemma - Scottish Gaelic Lemmatizer'): 'simplemma_gla',
                _tr('init_settings_global', 'simplemma - Serbo-Croatian Lemmatizer'): 'simplemma_srp_latn',
                _tr('init_settings_global', 'simplemma - Slovak Lemmatizer'): 'simplemma_slk',
                _tr('init_settings_global', 'simplemma - Slovenian Lemmatizer'): 'simplemma_slv',
                _tr('init_settings_global', 'simplemma - Spanish Lemmatizer'): 'simplemma_spa',
                _tr('init_settings_global', 'simplemma - Swahili Lemmatizer'): 'simplemma_swa',
                _tr('init_settings_global', 'simplemma - Swedish Lemmatizer'): 'simplemma_swe',
                _tr('init_settings_global', 'simplemma - Tagalog Lemmatizer'): 'simplemma_tgl',
                _tr('init_settings_global', 'simplemma - Turkish Lemmatizer'): 'simplemma_tur',
                _tr('init_settings_global', 'simplemma - Ukrainian Lemmatizer'): 'simplemma_ukr',
                _tr('init_settings_global', 'simplemma - Welsh Lemmatizer'): 'simplemma_cym',

                _tr('init_settings_global', 'spaCy - Bengali Lemmatizer'): 'spacy_ben',
                _tr('init_settings_global', 'spaCy - Catalan Lemmatizer'): 'spacy_cat',
                _tr('init_settings_global', 'spaCy - Croatian Lemmatizer'): 'spacy_hrv',
                _tr('init_settings_global', 'spaCy - Czech Lemmatizer'): 'spacy_ces',
                _tr('init_settings_global', 'spaCy - Danish Lemmatizer'): 'spacy_dan',
                _tr('init_settings_global', 'spaCy - Dutch Lemmatizer'): 'spacy_nld',
                _tr('init_settings_global', 'spaCy - English Lemmatizer'): 'spacy_eng',
                _tr('init_settings_global', 'spaCy - Finnish Lemmatizer'): 'spacy_fin',
                _tr('init_settings_global', 'spaCy - French Lemmatizer'): 'spacy_fra',
                _tr('init_settings_global', 'spaCy - German Lemmatizer'): 'spacy_deu',
                _tr('init_settings_global', 'spaCy - Greek (Ancient) Lemmatizer'): 'spacy_grc',
                _tr('init_settings_global', 'spaCy - Greek (Modern) Lemmatizer'): 'spacy_ell',
                _tr('init_settings_global', 'spaCy - Hungarian Lemmatizer'): 'spacy_hun',
                _tr('init_settings_global', 'spaCy - Indonesian Lemmatizer'): 'spacy_ind',
                _tr('init_settings_global', 'spaCy - Irish Lemmatizer'): 'spacy_gle',
                _tr('init_settings_global', 'spaCy - Italian Lemmatizer'): 'spacy_ita',
                _tr('init_settings_global', 'spaCy - Japanese Lemmatizer'): 'spacy_jpn',
                _tr('init_settings_global', 'spaCy - Lithuanian Lemmatizer'): 'spacy_lit',
                _tr('init_settings_global', 'spaCy - Luxembourgish Lemmatizer'): 'spacy_ltz',
                _tr('init_settings_global', 'spaCy - Macedonian Lemmatizer'): 'spacy_mkd',
                _tr('init_settings_global', 'spaCy - Norwegian Bokmål Lemmatizer'): 'spacy_nob',
                _tr('init_settings_global', 'spaCy - Persian Lemmatizer'): 'spacy_fas',
                _tr('init_settings_global', 'spaCy - Polish Lemmatizer'): 'spacy_pol',
                _tr('init_settings_global', 'spaCy - Portuguese Lemmatizer'): 'spacy_por',
                _tr('init_settings_global', 'spaCy - Romanian Lemmatizer'): 'spacy_ron',
                _tr('init_settings_global', 'spaCy - Russian Lemmatizer'): 'spacy_rus',
                _tr('init_settings_global', 'spaCy - Serbian (Cyrillic) Lemmatizer'): 'spacy_srp_cyrl',
                _tr('init_settings_global', 'spaCy - Spanish Lemmatizer'): 'spacy_spa',
                _tr('init_settings_global', 'spaCy - Swedish Lemmatizer'): 'spacy_swe',
                _tr('init_settings_global', 'spaCy - Tagalog Lemmatizer'): 'spacy_tgl',
                _tr('init_settings_global', 'spaCy - Turkish Lemmatizer'): 'spacy_tur',
                _tr('init_settings_global', 'spaCy - Ukrainian Lemmatizer'): 'spacy_ukr',
                _tr('init_settings_global', 'spaCy - Urdu Lemmatizer'): 'spacy_urd',

                _tr('init_settings_global', 'SudachiPy - Japanese Lemmatizer'): 'sudachipy_jpn'
            },

            'stop_word_lists': {
                _tr('init_settings_global', 'NLTK - Arabic Stop Word List'): 'nltk_ara',
                _tr('init_settings_global', 'NLTK - Azerbaijani Stop Word List'): 'nltk_aze',
                _tr('init_settings_global', 'NLTK - Danish Stop Word List'): 'nltk_dan',
                _tr('init_settings_global', 'NLTK - Dutch Stop Word List'): 'nltk_nld',
                _tr('init_settings_global', 'NLTK - English Stop Word List'): 'nltk_eng',
                _tr('init_settings_global', 'NLTK - Finnish Stop Word List'): 'nltk_fin',
                _tr('init_settings_global', 'NLTK - French Stop Word List'): 'nltk_fra',
                _tr('init_settings_global', 'NLTK - German Stop Word List'): 'nltk_deu',
                _tr('init_settings_global', 'NLTK - Greek (Modern) Stop Word List'): 'nltk_ell',
                _tr('init_settings_global', 'NLTK - Hungarian Stop Word List'): 'nltk_hun',
                _tr('init_settings_global', 'NLTK - Indonesian Stop Word List'): 'nltk_ind',
                _tr('init_settings_global', 'NLTK - Italian Stop Word List'): 'nltk_ita',
                _tr('init_settings_global', 'NLTK - Kazakh Stop Word List'): 'nltk_kaz',
                _tr('init_settings_global', 'NLTK - Nepali Stop Word List'): 'nltk_nep',
                _tr('init_settings_global', 'NLTK - Norwegian Bokmål Stop Word List'): 'nltk_nob',
                _tr('init_settings_global', 'NLTK - Norwegian Nynorsk Stop Word List'): 'nltk_nno',
                _tr('init_settings_global', 'NLTK - Portuguese Stop Word List'): 'nltk_por',
                _tr('init_settings_global', 'NLTK - Romanian Stop Word List'): 'nltk_ron',
                _tr('init_settings_global', 'NLTK - Russian Stop Word List'): 'nltk_rus',
                _tr('init_settings_global', 'NLTK - Slovenian Stop Word List'): 'nltk_slv',
                _tr('init_settings_global', 'NLTK - Spanish Stop Word List'): 'nltk_spa',
                _tr('init_settings_global', 'NLTK - Swedish Stop Word List'): 'nltk_swe',
                _tr('init_settings_global', 'NLTK - Tajik Stop Word List'): 'nltk_tgk',
                _tr('init_settings_global', 'NLTK - Turkish Stop Word List'): 'nltk_tur',

                _tr('init_settings_global', 'PyThaiNLP - Thai Stop Word List'): 'pythainlp_tha',

                _tr('init_settings_global', 'spaCy - Afrikaans Stop Word List'): 'spacy_afr',
                _tr('init_settings_global', 'spaCy - Albanian Stop Word List'): 'spacy_sqi',
                _tr('init_settings_global', 'spaCy - Amharic Stop Word List'): 'spacy_amh',
                _tr('init_settings_global', 'spaCy - Arabic Stop Word List'): 'spacy_ara',
                _tr('init_settings_global', 'spaCy - Armenian Stop Word List'): 'spacy_hye',
                _tr('init_settings_global', 'spaCy - Azerbaijani Stop Word List'): 'spacy_aze',
                _tr('init_settings_global', 'spaCy - Basque Stop Word List'): 'spacy_eus',
                _tr('init_settings_global', 'spaCy - Bengali Stop Word List'): 'spacy_ben',
                _tr('init_settings_global', 'spaCy - Bulgarian Stop Word List'): 'spacy_bul',
                _tr('init_settings_global', 'spaCy - Catalan Stop Word List'): 'spacy_cat',
                _tr('init_settings_global', 'spaCy - Chinese (Simplified) Stop Word List'): 'spacy_zho_cn',
                _tr('init_settings_global', 'spaCy - Chinese (Traditional) Stop Word List'): 'spacy_zho_tw',
                _tr('init_settings_global', 'spaCy - Croatian Stop Word List'): 'spacy_hrv',
                _tr('init_settings_global', 'spaCy - Czech Stop Word List'): 'spacy_ces',
                _tr('init_settings_global', 'spaCy - Danish Stop Word List'): 'spacy_dan',
                _tr('init_settings_global', 'spaCy - Dutch Stop Word List'): 'spacy_nld',
                _tr('init_settings_global', 'spaCy - English Stop Word List'): 'spacy_eng',
                _tr('init_settings_global', 'spaCy - Estonian Stop Word List'): 'spacy_est',
                _tr('init_settings_global', 'spaCy - Finnish Stop Word List'): 'spacy_fin',
                _tr('init_settings_global', 'spaCy - French Stop Word List'): 'spacy_fra',
                _tr('init_settings_global', 'spaCy - German Stop Word List'): 'spacy_deu',
                _tr('init_settings_global', 'spaCy - Greek (Ancient) Stop Word List'): 'spacy_grc',
                _tr('init_settings_global', 'spaCy - Greek (Modern) Stop Word List'): 'spacy_ell',
                _tr('init_settings_global', 'spaCy - Gujarati Stop Word List'): 'spacy_guj',
                _tr('init_settings_global', 'spaCy - Hebrew Stop Word List'): 'spacy_heb',
                _tr('init_settings_global', 'spaCy - Hindi Stop Word List'): 'spacy_hin',
                _tr('init_settings_global', 'spaCy - Hungarian Stop Word List'): 'spacy_hun',
                _tr('init_settings_global', 'spaCy - Icelandic Stop Word List'): 'spacy_isl',
                _tr('init_settings_global', 'spaCy - Indonesian Stop Word List'): 'spacy_ind',
                _tr('init_settings_global', 'spaCy - Irish Stop Word List'): 'spacy_gle',
                _tr('init_settings_global', 'spaCy - Italian Stop Word List'): 'spacy_ita',
                _tr('init_settings_global', 'spaCy - Japanese Stop Word List'): 'spacy_jpn',
                _tr('init_settings_global', 'spaCy - Kannada Stop Word List'): 'spacy_kan',
                _tr('init_settings_global', 'spaCy - Korean Stop Word List'): 'spacy_kor',
                _tr('init_settings_global', 'spaCy - Kyrgyz Stop Word List'): 'spacy_kir',
                _tr('init_settings_global', 'spaCy - Latvian Stop Word List'): 'spacy_lav',
                _tr('init_settings_global', 'spaCy - Ligurian Stop Word List'): 'spacy_lij',
                _tr('init_settings_global', 'spaCy - Lithuanian Stop Word List'): 'spacy_lit',
                _tr('init_settings_global', 'spaCy - Luxembourgish Stop Word List'): 'spacy_ltz',
                _tr('init_settings_global', 'spaCy - Macedonian Stop Word List'): 'spacy_mkd',
                _tr('init_settings_global', 'spaCy - Malayalam Stop Word List'): 'spacy_mal',
                _tr('init_settings_global', 'spaCy - Marathi Stop Word List'): 'spacy_mar',
                _tr('init_settings_global', 'spaCy - Nepali Stop Word List'): 'spacy_nep',
                _tr('init_settings_global', 'spaCy - Norwegian Bokmål Stop Word List'): 'spacy_nob',
                _tr('init_settings_global', 'spaCy - Persian Stop Word List'): 'spacy_fas',
                _tr('init_settings_global', 'spaCy - Polish Stop Word List'): 'spacy_pol',
                _tr('init_settings_global', 'spaCy - Portuguese Stop Word List'): 'spacy_por',
                _tr('init_settings_global', 'spaCy - Romanian Stop Word List'): 'spacy_ron',
                _tr('init_settings_global', 'spaCy - Russian Stop Word List'): 'spacy_rus',
                _tr('init_settings_global', 'spaCy - Sanskrit Stop Word List'): 'spacy_san',
                _tr('init_settings_global', 'spaCy - Serbian (Cyrillic) Stop Word List'): 'spacy_srp_cyrl',
                _tr('init_settings_global', 'spaCy - Serbian (Latin) Stop Word List'): 'spacy_srp_latn',
                _tr('init_settings_global', 'spaCy - Sinhala Stop Word List'): 'spacy_sin',
                _tr('init_settings_global', 'spaCy - Slovak Stop Word List'): 'spacy_slk',
                _tr('init_settings_global', 'spaCy - Slovenian Stop Word List'): 'spacy_slv',
                _tr('init_settings_global', 'spaCy - Sorbian (Lower) Stop Word List'): 'spacy_dsb',
                _tr('init_settings_global', 'spaCy - Sorbian (Upper) Stop Word List'): 'spacy_hsb',
                _tr('init_settings_global', 'spaCy - Spanish Stop Word List'): 'spacy_spa',
                _tr('init_settings_global', 'spaCy - Swedish Stop Word List'): 'spacy_swe',
                _tr('init_settings_global', 'spaCy - Tagalog Stop Word List'): 'spacy_tgl',
                _tr('init_settings_global', 'spaCy - Tamil Stop Word List'): 'spacy_tam',
                _tr('init_settings_global', 'spaCy - Tatar Stop Word List'): 'spacy_tat',
                _tr('init_settings_global', 'spaCy - Telugu Stop Word List'): 'spacy_tel',
                _tr('init_settings_global', 'spaCy - Thai Stop Word List'): 'spacy_tha',
                _tr('init_settings_global', 'spaCy - Tigrinya Stop Word List'): 'spacy_tir',
                _tr('init_settings_global', 'spaCy - Tswana Stop Word List'): 'spacy_tsn',
                _tr('init_settings_global', 'spaCy - Turkish Stop Word List'): 'spacy_tur',
                _tr('init_settings_global', 'spaCy - Ukrainian Stop Word List'): 'spacy_ukr',
                _tr('init_settings_global', 'spaCy - Urdu Stop Word List'): 'spacy_urd',
                _tr('init_settings_global', 'spaCy - Vietnamese Stop Word List'): 'spacy_vie',
                _tr('init_settings_global', 'spaCy - Yoruba Stop Word List'): 'spacy_yor',

                _tr('init_settings_global', 'stopword - Afrikaans Stop Word List'): 'stopword_afr',
                _tr('init_settings_global', 'stopword - Arabic Stop Word List'): 'stopword_ara',
                _tr('init_settings_global', 'stopword - Armenian Stop Word List'): 'stopword_hye',
                _tr('init_settings_global', 'stopword - Basque Stop Word List'): 'stopword_eus',
                _tr('init_settings_global', 'stopword - Bengali Stop Word List'): 'stopword_ben',
                _tr('init_settings_global', 'stopword - Breton Stop Word List'): 'stopword_bre',
                _tr('init_settings_global', 'stopword - Bulgarian Stop Word List'): 'stopword_bul',
                _tr('init_settings_global', 'stopword - Catalan Stop Word List'): 'stopword_cat',
                _tr('init_settings_global', 'stopword - Chinese (Simplified) Stop Word List'): 'stopword_zho_cn',
                _tr('init_settings_global', 'stopword - Chinese (Traditional) Stop Word List'): 'stopword_zho_tw',
                _tr('init_settings_global', 'stopword - Croatian Stop Word List'): 'stopword_hrv',
                _tr('init_settings_global', 'stopword - Czech Stop Word List'): 'stopword_ces',
                _tr('init_settings_global', 'stopword - Danish Stop Word List'): 'stopword_dan',
                _tr('init_settings_global', 'stopword - Dutch Stop Word List'): 'stopword_nld',
                _tr('init_settings_global', 'stopword - English Stop Word List'): 'stopword_eng',
                _tr('init_settings_global', 'stopword - Esperanto Stop Word List'): 'stopword_epo',
                _tr('init_settings_global', 'stopword - Estonian Stop Word List'): 'stopword_est',
                _tr('init_settings_global', 'stopword - Finnish Stop Word List'): 'stopword_fin',
                _tr('init_settings_global', 'stopword - French Stop Word List'): 'stopword_fra',
                _tr('init_settings_global', 'stopword - Galician Stop Word List'): 'stopword_glg',
                _tr('init_settings_global', 'stopword - German Stop Word List'): 'stopword_deu',
                _tr('init_settings_global', 'stopword - Greek (Modern) Stop Word List'): 'stopword_ell',
                _tr('init_settings_global', 'stopword - Gujarati Stop Word List'): 'stopword_guj',
                _tr('init_settings_global', 'stopword - Hausa Stop Word List'): 'stopword_hau',
                _tr('init_settings_global', 'stopword - Hebrew Stop Word List'): 'stopword_heb',
                _tr('init_settings_global', 'stopword - Hindi Stop Word List'): 'stopword_hin',
                _tr('init_settings_global', 'stopword - Hungarian Stop Word List'): 'stopword_hun',
                _tr('init_settings_global', 'stopword - Indonesian Stop Word List'): 'stopword_ind',
                _tr('init_settings_global', 'stopword - Irish Stop Word List'): 'stopword_gle',
                _tr('init_settings_global', 'stopword - Italian Stop Word List'): 'stopword_ita',
                _tr('init_settings_global', 'stopword - Japanese Stop Word List'): 'stopword_jpn',
                _tr('init_settings_global', 'stopword - Korean Stop Word List'): 'stopword_kor',
                _tr('init_settings_global', 'stopword - Kurdish Stop Word List'): 'stopword_kur',
                _tr('init_settings_global', 'stopword - Latin Stop Word List'): 'stopword_lat',
                _tr('init_settings_global', 'stopword - Latvian Stop Word List'): 'stopword_lav',
                _tr('init_settings_global', 'stopword - Lithuanian Stop Word List'): 'stopword_lit',
                _tr('init_settings_global', 'stopword - Lugbara Stop Word List'): 'stopword_lgg',
                _tr('init_settings_global', 'stopword - Malay Stop Word List'): 'stopword_msa',
                _tr('init_settings_global', 'stopword - Marathi Stop Word List'): 'stopword_mar',
                _tr('init_settings_global', 'stopword - Myanmar Stop Word List'): 'stopword_mya',
                _tr('init_settings_global', 'stopword - Norwegian Bokmål Stop Word List'): 'stopword_nob',
                _tr('init_settings_global', 'stopword - Persian Stop Word List'): 'stopword_fas',
                _tr('init_settings_global', 'stopword - Polish Stop Word List'): 'stopword_pol',
                _tr('init_settings_global', 'stopword - Portuguese (Brazil) Stop Word List'): 'stopword_por_br',
                _tr('init_settings_global', 'stopword - Portuguese (Portugal) Stop Word List'): 'stopword_por_pt',
                _tr('init_settings_global', 'stopword - Punjabi (Gurmukhi) Stop Word List'): 'stopword_pan_guru',
                _tr('init_settings_global', 'stopword - Romanian Stop Word List'): 'stopword_ron',
                _tr('init_settings_global', 'stopword - Russian Stop Word List'): 'stopword_rus',
                _tr('init_settings_global', 'stopword - Slovak Stop Word List'): 'stopword_slk',
                _tr('init_settings_global', 'stopword - Slovenian Stop Word List'): 'stopword_slv',
                _tr('init_settings_global', 'stopword - Somali Stop Word List'): 'stopword_som',
                _tr('init_settings_global', 'stopword - Sotho (Southern) Stop Word List'): 'stopword_sot',
                _tr('init_settings_global', 'stopword - Spanish Stop Word List'): 'stopword_spa',
                _tr('init_settings_global', 'stopword - Swahili Stop Word List'): 'stopword_swa',
                _tr('init_settings_global', 'stopword - Swedish Stop Word List'): 'stopword_swe',
                _tr('init_settings_global', 'stopword - Tagalog Stop Word List'): 'stopword_tgl',
                _tr('init_settings_global', 'stopword - Thai Stop Word List'): 'stopword_tha',
                _tr('init_settings_global', 'stopword - Turkish Stop Word List'): 'stopword_tur',
                _tr('init_settings_global', 'stopword - Ukrainian Stop Word List'): 'stopword_ukr',
                _tr('init_settings_global', 'stopword - Urdu Stop Word List'): 'stopword_urd',
                _tr('init_settings_global', 'stopword - Vietnamese Stop Word List'): 'stopword_vie',
                _tr('init_settings_global', 'stopword - Yoruba Stop Word List'): 'stopword_yor',
                _tr('init_settings_global', 'stopword - Zulu Stop Word List'): 'stopword_zul',

                _tr('init_settings_global', 'Custom List'): 'custom',
            }
        },

        'sentence_tokenizers': {
            'zho_cn': [
                'spacy_sentence_recognizer',
                'wordless_zho'
            ],

            'zho_tw': [
                'spacy_sentence_recognizer',
                'wordless_zho'
            ],

            'ces': [
                'nltk_punkt_ces',
                'spacy_sentencizer'
            ],

            'dan': [
                'nltk_punkt_dan',
                'spacy_sentence_recognizer'
            ],

            'nld': [
                'nltk_punkt_nld',
                'spacy_sentence_recognizer'
            ],

            'eng_gb': [
                'nltk_punkt_eng',
                'spacy_sentence_recognizer'
            ],

            'eng_us': [
                'nltk_punkt_eng',
                'spacy_sentence_recognizer'
            ],

            'est': [
                'nltk_punkt_est',
                'spacy_sentencizer'
            ],

            'fin': [
                'nltk_punkt_fin',
                'spacy_sentencizer'
            ],

            'fra': [
                'nltk_punkt_fra',
                'spacy_sentence_recognizer'
            ],

            'deu_at': [
                'nltk_punkt_deu',
                'spacy_sentence_recognizer'
            ],

            'deu_de': [
                'nltk_punkt_deu',
                'spacy_sentence_recognizer'
            ],

            'deu_ch': [
                'nltk_punkt_deu',
                'spacy_sentence_recognizer'
            ],

            'ell': [
                'nltk_punkt_ell',
                'spacy_sentence_recognizer'
            ],

            'ita': [
                'nltk_punkt_ita',
                'spacy_sentence_recognizer'
            ],

            'jpn': [
                'spacy_sentence_recognizer',
                'wordless_jpn'
            ],

            'lit': ['spacy_sentence_recognizer'],

            'mal': [
                'nltk_punkt_mal',
                'spacy_sentencizer'
            ],

            'nob': [
                'nltk_punkt_nor',
                'spacy_sentence_recognizer'
            ],

            'nno': [
                'nltk_punkt_nor',
                'spacy_sentencizer'
            ],

            'pol': [
                'nltk_punkt_pol',
                'spacy_sentence_recognizer'
            ],

            'por_br': [
                'nltk_punkt_por',
                'spacy_sentence_recognizer'
            ],

            'por_pt': [
                'nltk_punkt_por',
                'spacy_sentence_recognizer'
            ],

            'ron': ['spacy_sentence_recognizer'],

            'rus': [
                'nltk_punkt_rus',
                'spacy_sentence_recognizer'
            ],

            'slv': [
                'nltk_punkt_slv',
                'spacy_sentencizer'
            ],

            'spa': [
                'nltk_punkt_spa',
                'spacy_sentence_recognizer'
            ],

            'swe': [
                'nltk_punkt_swe',
                'spacy_sentencizer'
            ],

            'tha': [
                'pythainlp_crfcut',
                'pythainlp_thaisumcut'
            ],

            'bod': ['botok_bod'],

            'tur': [
                'nltk_punkt_tur',
                'spacy_sentencizer'
            ],

            'vie': ['underthesea_vie'],

            'other': [
                'nltk_punkt_eng',
                'spacy_sentencizer'
            ]
        },

        'word_tokenizers': {
            'afr': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_afr'
            ],

            'sqi': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_sqi'
            ],

            'amh': ['spacy_amh'],
            'ara': ['spacy_ara'],

            'hye': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_hye'
            ],

            'asm': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses'
            ],

            'aze': ['spacy_aze'],
            'eus': ['spacy_eus'],

            'ben': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_ben'
            ],

            'bul': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_bul'
            ],

            'cat': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
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
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_hrv'
            ],

            'ces': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_ces'
            ],

            'dan': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_dan'
            ],

            'nld': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_nld'
            ],

            'eng_gb': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_eng'
            ],

            'eng_us': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
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
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_fra'
            ],

            'deu_at': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_deu'
            ],

            'deu_de': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_deu'
            ],

            'deu_ch': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_deu'
            ],

            'grc': ['spacy_grc'],

            'ell': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_ell'
            ],

            'guj': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_guj'
            ],

            'heb': ['spacy_heb'],

            'hin': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_hin'
            ],

            'hun': [
                'sacremoses_moses',
                'spacy_hun'
            ],

            'isl': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_isl'
            ],

            'ind': ['spacy_ind'],

            'gle': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_gle'
            ],

            'ita': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_ita'
            ],

            'jpn': [
                'spacy_jpn',
                'sudachipy_jpn_split_mode_a', 'sudachipy_jpn_split_mode_b', 'sudachipy_jpn_split_mode_c',
                'wordless_jpn_kanji'
            ],

            'kan': [
                'sacremoses_moses',
                'spacy_kan'
            ],

            'kir': ['spacy_kir'],

            'lav': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_lav'
            ],

            'lij': ['spacy_lij'],

            'lit': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_lit'
            ],

            'ltz': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_ltz'
            ],

            'mkd': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_mkd'
            ],

            'mal': [
                'sacremoses_moses',
                'spacy_mal'
            ],

            'mar': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_mar'
            ],

            'mni': ['sacremoses_moses'],

            'nep': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_nep'
            ],

            'nob': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_nob'
            ],

            'ori': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses'
            ],

            'fas': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'spacy_fas'
            ],

            'pol': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_pol'
            ],

            'por_br': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_por'
            ],

            'por_pt': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_por'
            ],

            'pan_guru': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses'
            ],

            'ron': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_ron'
            ],

            'rus': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_rus'
            ],

            'san': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_san'
            ],

            'srp_cyrl': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_srp'
            ],

            'srp_latn': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_srp'
            ],

            'sin': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_sin'
            ],

            'slk': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_slk'
            ],

            'slv': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_slv'
            ],

            'dsb': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_dsb'
            ],

            'hsb': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_hsb'
            ],

            'spa': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_spa'
            ],

            'swe': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_swe'
            ],

            'tgl': ['spacy_tgl'],

            'tgk': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
            ],

            'tam': [
                'sacremoses_moses',
                'spacy_tam'
            ],

            'tat': ['spacy_tat'],

            'tel': [
                'sacremoses_moses',
                'spacy_tel'
            ],

            'tdt': ['sacremoses_moses'],

            'tha': [
                'pythainlp_longest_matching',
                'pythainlp_max_matching',
                'pythainlp_max_matching_tcc',
                'pythainlp_nercut'
            ],

            'bod': ['botok_bod'],
            'tir': ['spacy_tir'],
            'tsn': ['spacy_tsn'],
            'tur': ['spacy_tur'],

            'ukr': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_ukr'
            ],

            'urd': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_urd'
            ],

            'vie': [
                'nltk_tok_tok',
                'underthesea_vie'
            ],

            'yor': ['spacy_yor'],

            'other': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_eng'
            ]
        },

        'syl_tokenizers': {
            'afr': ['pyphen_afr'],
            'sqi': ['pyphen_sqi'],
            'bel': ['pyphen_bel'],
            'cat': ['pyphen_cat'],
            'bul': ['pyphen_bul'],
            'hrv': ['pyphen_hrv'],
            'ces': ['pyphen_ces'],
            'dan': ['pyphen_dan'],
            'nld': ['pyphen_nld'],

            'eng_gb': [
                'nltk_legality',
                'nltk_sonority_sequencing',
                'pyphen_eng_gb'
            ],

            'eng_us': [
                'nltk_legality',
                'nltk_sonority_sequencing',
                'pyphen_eng_us'
            ],

            'epo': ['pyphen_epo'],
            'est': ['pyphen_est'],
            'fra': ['pyphen_fra'],
            'glg': ['pyphen_glg'],
            'deu_at': ['pyphen_deu_at'],
            'deu_de': ['pyphen_deu_de'],
            'deu_ch': ['pyphen_deu_ch'],
            'ell': ['pyphen_ell'],
            'hun': ['pyphen_hun'],
            'isl': ['pyphen_isl'],
            'ind': ['pyphen_ind'],
            'ita': ['pyphen_ita'],
            'lit': ['pyphen_lit'],
            'lav': ['pyphen_lav'],
            'mon': ['pyphen_mon'],
            'nob': ['pyphen_nob'],
            'nno': ['pyphen_nno'],
            'pol': ['pyphen_pol'],
            'por_br': ['pyphen_por_br'],
            'por_pt': ['pyphen_por_pt'],
            'ron': ['pyphen_ron'],
            'rus': ['pyphen_rus'],
            'srp_cyrl': ['pyphen_srp_cyrl'],
            'srp_latn': ['pyphen_srp_latn'],
            'slk': ['pyphen_slk'],
            'slv': ['pyphen_slv'],
            'spa': ['pyphen_spa'],
            'swe': ['pyphen_swe'],
            'tel': ['pyphen_tel'],
            'tha': ['pythainlp_tha'],
            'ukr': ['pyphen_ukr'],
            'zul': ['pyphen_zul']
        },

        'pos_taggers': {
            'cat': ['spacy_cat'],

            'zho_cn': [
                'jieba_zho',
                'spacy_zho'
            ],

            'zho_tw': [
                'jieba_zho',
                'spacy_zho'
            ],

            'hrv': ['spacy_hrv'],
            'dan': ['spacy_dan',],
            'nld': ['spacy_nld'],

            'eng_gb': [
                'nltk_perceptron_eng',
                'spacy_eng'
            ],

            'eng_us': [
                'nltk_perceptron_eng',
                'spacy_eng'
            ],

            'fin': ['spacy_fin'],
            'fra': ['spacy_fra'],
            'deu_at': ['spacy_deu'],
            'deu_de': ['spacy_deu'],
            'deu_ch': ['spacy_deu'],
            'ell': ['spacy_ell'],
            'ita': ['spacy_ita'],

            'jpn': [
                'spacy_jpn',
                'sudachipy_jpn'
            ],

            'lit': ['spacy_lit'],
            'mkd': ['spacy_mkd'],
            'nob': ['spacy_nob'],
            'pol': ['spacy_pol'],
            'por_br': ['spacy_por'],
            'por_pt': ['spacy_por'],
            'ron': ['spacy_ron'],

            'rus': [
                'nltk_perceptron_rus',
                'pymorphy2_morphological_analyzer',
                'spacy_rus'
            ],

            'spa': ['spacy_spa'],
            'swe': ['spacy_swe'],

            'tha': [
                'pythainlp_perceptron_lst20',
                'pythainlp_perceptron_orchid',
                'pythainlp_perceptron_pud'
            ],

            'bod': ['botok_bod'],

            'ukr': [
                'pymorphy2_morphological_analyzer',
                'spacy_ukr'
            ],

            'vie': ['underthesea_vie']
        },

        'lemmatizers': {
            'sqi': ['simplemma_sqi'],
            'hye': ['simplemma_hye'],
            'ben': ['spacy_ben'],
            'bul': ['simplemma_bul',],

            'cat': [
                'simplemma_cat',
                'spacy_cat'
            ],

            'hrv': [
                'simplemma_hrv',
                'spacy_hrv'
            ],

            'ces': [
                'simplemma_ces',
                'spacy_ces'
            ],

            'dan': [
                'simplemma_dan',
                'spacy_dan'
            ],

            'nld': [
                'simplemma_nld',
                'spacy_nld'
            ],

            'enm': ['simplemma_enm'],

            'eng_gb': [
                'nltk_wordnet',
                'simplemma_eng',
                'spacy_eng'
            ],

            'eng_us': [
                'nltk_wordnet',
                'simplemma_eng',
                'spacy_eng'
            ],

            'est': ['simplemma_est'],

            'fin': [
                'simplemma_fin',
                'spacy_fin'
            ],

            'fra': [
                'simplemma_fra',
                'spacy_fra'
            ],

            'glg': ['simplemma_glg'],
            'kat': ['simplemma_kat'],

            'deu_at': [
                'simplemma_deu',
                'spacy_deu'
            ],

            'deu_de': [
                'simplemma_deu',
                'spacy_deu'
            ],

            'deu_ch': [
                'simplemma_deu',
                'spacy_deu'
            ],


            'grc': [
                'spacy_grc'
            ],

            'ell': [
                'simplemma_ell',
                'spacy_ell'
            ],

            'hin': ['simplemma_hin'],

            'hun': [
                'simplemma_hun',
                'spacy_hun'
            ],

            'isl': ['simplemma_isl'],

            'ind': [
                'simplemma_ind',
                'spacy_ind'
            ],

            'gle': [
                'simplemma_gle',
                'spacy_gle'
            ],

            'ita': [
                'simplemma_ita',
                'spacy_ita'
            ],

            'jpn': [
                'spacy_jpn',
                'sudachipy_jpn'
            ],

            'lat': ['simplemma_lat'],
            'lav': ['simplemma_lav'],

            'lit': [
                'simplemma_lit',
                'spacy_lit'
            ],

            'ltz': [
                'simplemma_ltz',
                'spacy_ltz'
            ],

            'mkd': [
                'simplemma_mkd',
                'spacy_mkd'
            ],

            'msa': ['simplemma_msa'],
            'glv': ['simplemma_glv'],

            'nob': [
                'simplemma_nob',
                'spacy_nob'
            ],

            'nno': ['simplemma_nno'],

            'fas': [
                'simplemma_fas',
                'spacy_fas'
            ],

            'pol': [
                'simplemma_pol',
                'spacy_pol'
            ],

            'por_br': [
                'simplemma_por',
                'spacy_por'
            ],

            'por_pt': [
                'simplemma_por',
                'spacy_por'
            ],

            'ron': [
                'simplemma_ron',
                'spacy_ron'
            ],

            'rus': [
                'simplemma_rus',
                'pymorphy2_morphological_analyzer',
                'spacy_rus'
            ],

            'sme': ['simplemma_sme'],
            'gla': ['simplemma_gla'],
            'srp_cyrl': ['spacy_srp_cyrl'],
            'srp_latn': ['simplemma_srp_latn'],
            'slk': ['simplemma_slk'],
            'slv': ['simplemma_slv'],

            'spa': [
                'simplemma_spa',
                'spacy_spa'
            ],

            'swa': ['simplemma_swa'],

            'swe': [
                'simplemma_swe',
                'spacy_swe'
            ],

            'tgl': [
                'simplemma_tgl',
                'spacy_tgl'
            ],

            'bod': ['botok_bod'],

            'tur': [
                'simplemma_tur',
                'spacy_tur'
            ],

            'ukr': [
                'simplemma_ukr',
                'pymorphy2_morphological_analyzer',
                'spacy_ukr'
            ],

            'urd': ['spacy_urd'],
            'cym': ['simplemma_cym']
        },

        'stop_word_lists': {
            'afr': [
                'spacy_afr',
                'stopword_afr'
            ],

            'sqi': ['spacy_sqi'],
            'amh': ['spacy_amh'],

            'ara': [
                'nltk_ara',
                'spacy_ara',
                'stopword_ara'
            ],

            'hye': [
                'spacy_hye',
                'stopword_hye'
            ],

            'aze': [
                'nltk_aze',
                'spacy_aze'
            ],

            'eus': [
                'spacy_eus',
                'stopword_eus'
            ],

            'ben': [
                'spacy_ben',
                'stopword_ben'
            ],

            'bre': ['stopword_bre'],

            'bul': [
                'spacy_bul',
                'stopword_bul'
            ],

            'cat': [
                'spacy_cat',
                'stopword_cat'
            ],

            'zho_cn': [
                'spacy_zho_cn',
                'stopword_zho_cn'
            ],

            'zho_tw': [
                'spacy_zho_tw',
                'stopword_zho_tw'
            ],

            'hrv': [
                'spacy_hrv',
                'stopword_hrv'
            ],

            'ces': [
                'spacy_ces',
                'stopword_ces'
            ],

            'dan': [
                'nltk_dan',
                'spacy_dan',
                'stopword_dan'
            ],

            'nld': [
                'nltk_nld',
                'spacy_nld',
                'stopword_nld'
            ],

            'eng_gb': [
                'nltk_eng',
                'spacy_eng',
                'stopword_eng'
            ],

            'eng_us': [
                'nltk_eng',
                'spacy_eng',
                'stopword_eng'
            ],

            'epo': ['stopword_epo'],

            'est': [
                'spacy_est',
                'stopword_est'
            ],

            'fin': [
                'nltk_fin',
                'spacy_fin',
                'stopword_fin'
            ],

            'fra': [
                'nltk_fra',
                'spacy_fra',
                'stopword_fra'
            ],

            'glg': ['stopword_glg'],

            'deu_at': [
                'nltk_deu',
                'spacy_deu',
                'stopword_deu'
            ],

            'deu_de': [
                'nltk_deu',
                'spacy_deu',
                'stopword_deu'
            ],

            'deu_ch': [
                'nltk_deu',
                'spacy_deu',
                'stopword_deu'
            ],

            'grc': ['spacy_grc'],

            'ell': [
                'nltk_ell',
                'spacy_ell',
                'stopword_ell'
            ],

            'guj': [
                'spacy_guj',
                'stopword_guj'
            ],

            'hau': ['stopword_hau'],

            'heb': [
                'spacy_heb',
                'stopword_heb'
            ],

            'hin': [
                'spacy_hin',
                'stopword_hin'
            ],

            'hun': [
                'nltk_hun',
                'spacy_hun',
                'stopword_hun'
            ],

            'isl': ['spacy_isl'],

            'ind': [
                'nltk_ind',
                'spacy_ind',
                'stopword_ind'
            ],

            'gle': [
                'spacy_gle',
                'stopword_gle'
            ],

            'ita': [
                'nltk_ita',
                'spacy_ita',
                'stopword_ita'
            ],

            'jpn': [
                'spacy_jpn',
                'stopword_jpn'
            ],

            'kan': ['spacy_kan'],
            'kaz': ['nltk_kaz'],

            'kor': [
                'spacy_kor',
                'stopword_kor'
            ],

            'kur': ['stopword_kur'],
            'kir': ['spacy_kir'],
            'lat': ['stopword_lat'],

            'lav': [
                'spacy_lav',
                'stopword_lav'
            ],

            'lij': ['spacy_lij'],

            'lit': [
                'spacy_lit',
                'stopword_lit'
            ],

            'lgg': ['stopword_lgg'],
            'ltz': ['spacy_ltz'],
            'mkd': ['spacy_mkd'],
            'msa': ['stopword_msa'],
            'mal': ['spacy_mal'],

            'mar': [
                'spacy_mar',
                'stopword_mar'
            ],

            'mya': ['stopword_mya'],

            'nep': [
                'nltk_nep',
                'spacy_nep'
            ],

            'nob': [
                'nltk_nob',
                'spacy_nob',
                'stopword_nob'
            ],

            'nno': ['nltk_nno'],

            'fas': [
                'spacy_fas',
                'stopword_fas'
            ],

            'pol': [
                'spacy_pol',
                'stopword_pol'
            ],

            'por_br': [
                'nltk_por',
                'spacy_por',
                'stopword_por_br'
            ],

            'por_pt': [
                'nltk_por',
                'spacy_por',
                'stopword_por_pt'
            ],

            'pan_guru': ['stopword_pan_guru'],

            'ron': [
                'nltk_ron',
                'spacy_ron',
                'stopword_ron'
            ],

            'rus': [
                'nltk_rus',
                'spacy_rus',
                'stopword_rus'
            ],

            'san': ['spacy_san'],
            'srp_cyrl': ['spacy_srp_cyrl'],
            'srp_latn': ['spacy_srp_latn'],
            'sin': ['spacy_sin'],

            'slk': [
                'spacy_slk',
                'stopword_slk'
            ],

            'slv': [
                'nltk_slv',
                'spacy_slv',
                'stopword_slv'
            ],

            'som': ['stopword_som'],
            'dsb': ['spacy_dsb'],
            'hsb': ['spacy_hsb'],
            'sot': ['stopword_sot'],

            'spa': [
                'nltk_spa',
                'spacy_spa',
                'stopword_spa'
            ],

            'swa': ['stopword_swa'],

            'swe': [
                'nltk_swe',
                'spacy_swe',
                'stopword_swe'
            ],

            'tgl': [
                'spacy_tgl',
                'stopword_tgl'
            ],

            'tgk': ['nltk_tgk'],
            'tam': ['spacy_tam'],
            'tat': ['spacy_tat'],
            'tel': ['spacy_tel'],

            'tha': [
                'pythainlp_tha',
                'spacy_tha',
                'stopword_tha'
            ],

            'tir': ['spacy_tir'],
            'tsn': ['spacy_tsn'],

            'tur': [
                'nltk_tur',
                'spacy_tur',
                'stopword_tur'
            ],

            'ukr': [
                'spacy_ukr',
                'stopword_ukr'
            ],

            'urd': [
                'spacy_urd',
                'stopword_urd'
            ],

            'vie': [
                'spacy_vie',
                'stopword_vie'
            ],

            'yor': [
                'spacy_yor',
                'stopword_yor'
            ],

            'zul': ['stopword_zul'],

            'other': []
        },

        'measures_dispersion': {
            _tr('init_settings_global', 'None'): {
                'col_text': None,
                'func': None
            },

            _tr('init_settings_global', "Carroll's D₂"): {
                'col_text': _tr('init_settings_global', "Carroll's D₂"),
                'func': wl_measures_dispersion.carrolls_d2
            },

            _tr('init_settings_global', "Gries's DP"): {
                'col_text': _tr('init_settings_global', "Gries's DP"),
                'func': wl_measures_dispersion.griess_dp
            },

            _tr('init_settings_global', "Gries's DPnorm"): {
                'col_text': _tr('init_settings_global', "Gries's DPnorm"),
                'func': wl_measures_dispersion.griess_dp_norm
            },

            _tr('init_settings_global', "Juilland's D"): {
                'col_text': _tr('init_settings_global', "Juilland's D"),
                'func': wl_measures_dispersion.juillands_d
            },

            _tr('init_settings_global', "Lyne's D₃"): {
                'col_text': _tr('init_settings_global', "Lyne's D₃"),
                'func': wl_measures_dispersion.lynes_d3
            },

            _tr('init_settings_global', "Rosengren's S"): {
                'col_text': _tr('init_settings_global', "Rosengren's S"),
                'func': wl_measures_dispersion.rosengrens_s
            },

            _tr('init_settings_global', "Zhang's Distributional Consistency"): {
                'col_text': _tr('init_settings_global', "Zhang's DC"),
                'func': wl_measures_dispersion.zhangs_distributional_consistency
            }
        },

        'measures_adjusted_freq': {
            _tr('init_settings_global', 'None'): {
                'col_text': None,
                'func': None
            },

            _tr('init_settings_global', "Carroll's Um"): {
                'col_text': _tr('init_settings_global', "Carroll's Um"),
                'func': wl_measures_adjusted_freq.carrolls_um
            },

            _tr('init_settings_global', "Engwall's FM"): {
                'col_text': _tr('init_settings_global', "Engwall's FM"),
                'func': wl_measures_adjusted_freq.engwalls_fm
            },

            _tr('init_settings_global', "Juilland's U"): {
                'col_text': _tr('init_settings_global', "Juilland's U"),
                'func': wl_measures_adjusted_freq.juillands_u
            },

            _tr('init_settings_global', "Kromer's UR"): {
                'col_text': _tr('init_settings_global', "Kromer's UR"),
                'func': wl_measures_adjusted_freq.kromers_ur
            },

            _tr('init_settings_global', "Rosengren's KF"): {
                'col_text': _tr('init_settings_global', "Rosengren's KF"),
                'func': wl_measures_adjusted_freq.rosengrens_kf
            }
        },

        'tests_statistical_significance': {
            _tr('init_settings_global', 'None'): {
                'col_text': None,
                'func': None,
                'to_sections': None,
                'collocation_extractor': True,
                'keyword_extractor': True
            },

            _tr('init_settings_global', "Fisher's Exact Test"): {
                # There is no test statistic for Fisher's exact test
                'col_text': None,
                'func': wl_measures_statistical_significance.fishers_exact_test,
                'to_sections': False,
                'collocation_extractor': True,
                'keyword_extractor': True
            },

            _tr('init_settings_global', 'Log-likelihood Ratio Test'): {
                'col_text': _tr('init_settings_global', 'Log-likelihood Ratio'),
                'func': wl_measures_statistical_significance.log_likelihood_ratio_test,
                'to_sections': False,
                'collocation_extractor': True,
                'keyword_extractor': True
            },

            _tr('init_settings_global', 'Mann-Whitney U Test'): {
                'col_text': _tr('init_settings_global', 'U1'),
                'func': wl_measures_statistical_significance.mann_whitney_u_test,
                'to_sections': True,
                'collocation_extractor': False,
                'keyword_extractor': True
            },

            _tr('init_settings_global', "Pearson's Chi-squared Test"): {
                'col_text': _tr('init_settings_global', 'χ2'),
                'func': wl_measures_statistical_significance.pearsons_chi_squared_test,
                'to_sections': False,
                'collocation_extractor': True,
                'keyword_extractor': True
            },

            _tr('init_settings_global', "Student's t-test (1-sample)"): {
                'col_text': _tr('init_settings_global', 't-statistic'),
                'func': wl_measures_statistical_significance.students_t_test_1_sample,
                'to_sections': False,
                'collocation_extractor': True,
                'keyword_extractor': True
            },

            _tr('init_settings_global', "Student's t-test (2-sample)"): {
                'col_text': _tr('init_settings_global', 't-statistic'),
                'func': wl_measures_statistical_significance.students_t_test_2_sample,
                'to_sections': True,
                'collocation_extractor': False,
                'keyword_extractor': True
            },

            _tr('init_settings_global', "Welch's t-test"): {
                'col_text': _tr('init_settings_global', 't-statistic'),
                'func': wl_measures_statistical_significance.welchs_t_test,
                'to_sections': True,
                'collocation_extractor': False,
                'keyword_extractor': True
            },

            _tr('init_settings_global', 'z-score'): {
                'col_text': _tr('init_settings_global', 'z-score'),
                'func': wl_measures_statistical_significance.z_score,
                'to_sections': False,
                'collocation_extractor': True,
                'keyword_extractor': True
            },

            _tr('init_settings_global', 'z-score (Berry-Rogghe)'): {
                'col_text': _tr('init_settings_global', 'z-score'),
                'func': wl_measures_statistical_significance.z_score_berry_rogghe,
                'to_sections': False,
                'collocation_extractor': True,
                'keyword_extractor': False
            }
        },

        'measures_bayes_factor': {
            _tr('init_settings_global', 'None'): {
                'func': None,
                'to_sections': None,
                'collocation_extractor': True,
                'keyword_extractor': True
            },

            _tr('init_settings_global', 'Log-likelihood Ratio Test'): {
                'func': wl_measures_bayes_factor.bayes_factor_log_likelihood_ratio_test,
                'to_sections': False,
                'collocation_extractor': True,
                'keyword_extractor': True
            },

            _tr('init_settings_global', "Student's t-test (2-sample)"): {
                'func': wl_measures_bayes_factor.bayes_factor_students_t_test_2_sample,
                'to_sections': True,
                'collocation_extractor': False,
                'keyword_extractor': True
            },
        },

        'measures_effect_size': {
            _tr('init_settings_global', 'None'): {
                'col_text': None,
                'func': None
            },

            _tr('init_settings_global', '%DIFF'): {
                'col_text': _tr('init_settings_global', '%DIFF'),
                'func': wl_measures_effect_size.pct_diff
            },

            _tr('init_settings_global', 'Cubic Association Ratio'): {
                'col_text': _tr('init_settings_global', 'IM³'),
                'func': wl_measures_effect_size.im3
            },

            _tr('init_settings_global', "Dice's Coefficient"): {
                'col_text': _tr('init_settings_global', "Dice's Coefficient"),
                'func': wl_measures_effect_size.dices_coeff
            },

            _tr('init_settings_global', 'Difference Coefficient'): {
                'col_text': _tr('init_settings_global', 'Difference Coefficient'),
                'func': wl_measures_effect_size.diff_coeff
            },

            _tr('init_settings_global', 'Jaccard Index'): {
                'col_text': _tr('init_settings_global', 'Jaccard Index'),
                'func': wl_measures_effect_size.jaccard_index
            },

            _tr('init_settings_global', 'Log-Frequency Biased MD'): {
                'col_text': _tr('init_settings_global', 'LFMD'),
                'func': wl_measures_effect_size.lfmd
            },

            _tr('init_settings_global', "Kilgarriff's Ratio"): {
                'col_text': _tr('init_settings_global', "Kilgarriff's Ratio"),
                'func': wl_measures_effect_size.kilgarriffs_ratio
            },

            _tr('init_settings_global', 'logDice'): {
                'col_text': _tr('init_settings_global', 'logDice'),
                'func': wl_measures_effect_size.log_dice
            },

            _tr('init_settings_global', 'Log Ratio'): {
                'col_text': _tr('init_settings_global', 'Log Ratio'),
                'func': wl_measures_effect_size.log_ratio
            },

            _tr('init_settings_global', 'MI.log-f'): {
                'col_text': _tr('init_settings_global', 'MI.log-f'),
                'func': wl_measures_effect_size.mi_log_f
            },

            _tr('init_settings_global', 'Minimum Sensitivity'): {
                'col_text': _tr('init_settings_global', 'Minimum Sensitivity'),
                'func': wl_measures_effect_size.min_sensitivity
            },

            _tr('init_settings_global', 'Mutual Dependency'): {
                'col_text': _tr('init_settings_global', 'MD'),
                'func': wl_measures_effect_size.md
            },

            _tr('init_settings_global', 'Mutual Expectation'): {
                'col_text': _tr('init_settings_global', 'ME'),
                'func': wl_measures_effect_size.me
            },

            _tr('init_settings_global', 'Mutual Information'): {
                'col_text': _tr('init_settings_global', 'MI'),
                'func': wl_measures_effect_size.mi
            },

            _tr('init_settings_global', 'Odds Ratio'): {
                'col_text': _tr('init_settings_global', 'Odds Ratio'),
                'func': wl_measures_effect_size.odds_ratio
            },

            _tr('init_settings_global', 'Pointwise Mutual Information'): {
                'col_text': _tr('init_settings_global', 'PMI'),
                'func': wl_measures_effect_size.pmi
            },

            _tr('init_settings_global', 'Poisson Collocation Measure'): {
                'col_text': _tr('init_settings_global', 'Poisson Collocation Measure'),
                'func': wl_measures_effect_size.poisson_collocation_measure
            },

            _tr('init_settings_global', 'Squared Phi Coefficient'): {
                'col_text': _tr('init_settings_global', 'φ2'),
                'func': wl_measures_effect_size.squared_phi_coeff
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

                            line-height: 120%;
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
