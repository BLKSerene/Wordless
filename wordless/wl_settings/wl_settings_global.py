# ----------------------------------------------------------------------
# Wordless: Settings - Global Settings
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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
        # Language names should be always capitalized
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
            _tr('init_settings_global', 'Ganda'): ['lug', 'lg', 'Niger-Congo'],
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

            _tr('init_settings_global', 'Other languages'): ['other', 'other', 'Unclassified']
        },

        # Language and geographical names should be always capitalized
        # Case of encoding names are preserved
        'encodings': {
            _tr('init_settings_global', 'All languages (UTF-8 without BOM)'): 'utf_8',
            _tr('init_settings_global', 'All languages (UTF-8 with BOM)'): 'utf_8_sig',
            _tr('init_settings_global', 'All languages (UTF-16 with BOM)'): 'utf_16',
            _tr('init_settings_global', 'All languages (UTF-16BE without BOM)'): 'utf_16_be',
            _tr('init_settings_global', 'All languages (UTF-16LE without BOM)'): 'utf_16_le',
            _tr('init_settings_global', 'All languages (UTF-32 with BOM)'): 'utf_32',
            _tr('init_settings_global', 'All languages (UTF-32BE without BOM)'): 'utf_32_be',
            _tr('init_settings_global', 'All languages (UTF-32LE without BOM)'): 'utf_32_le',
            _tr('init_settings_global', 'All languages (UTF-7)'): 'utf_7',

            _tr('init_settings_global', 'Arabic (CP720)'): 'cp720',
            _tr('init_settings_global', 'Arabic (CP864)'): 'cp864',
            _tr('init_settings_global', 'Arabic (ISO-8859-6)'): 'iso8859_6',
            _tr('init_settings_global', 'Arabic (Mac OS Arabic)'): 'mac_arabic',
            _tr('init_settings_global', 'Arabic (Windows-1256)'): 'cp1256',

            _tr('init_settings_global', 'Baltic languages (CP775)'): 'cp775',
            _tr('init_settings_global', 'Baltic languages (ISO-8859-13)'): 'iso8859_13',
            _tr('init_settings_global', 'Baltic languages (Windows-1257)'): 'cp1257',

            _tr('init_settings_global', 'Celtic languages (ISO-8859-14)'): 'iso8859_14',

            _tr('init_settings_global', 'Chinese (GB18030)'): 'gb18030',
            _tr('init_settings_global', 'Chinese (GBK)'): 'gbk',

            _tr('init_settings_global', 'Chinese (Simplified) (GB2312)'): 'gb2312',
            _tr('init_settings_global', 'Chinese (Simplified) (HZ)'): 'hz',

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

            _tr('init_settings_global', 'European (Southeastern) (ISO-8859-16)'): 'iso8859_16',

            _tr('init_settings_global', 'European (Western) (EBCDIC 500)'): 'cp500',
            _tr('init_settings_global', 'European (Western) (CP850)'): 'cp850',
            _tr('init_settings_global', 'European (Western) (CP858)'): 'cp858',
            _tr('init_settings_global', 'European (Western) (CP1140)'): 'cp1140',
            _tr('init_settings_global', 'European (Western) (ISO-8859-1)'): 'latin_1',
            _tr('init_settings_global', 'European (Western) (ISO-8859-15)'): 'iso8859_15',
            _tr('init_settings_global', 'European (Western) (Mac OS Roman)'): 'mac_roman',
            _tr('init_settings_global', 'European (Western) (Windows-1252)'): 'cp1252',

            _tr('init_settings_global', 'French (CP863)'): 'cp863',

            _tr('init_settings_global', 'German (EBCDIC 273)'): 'cp273',

            _tr('init_settings_global', 'Greek (CP737)'): 'cp737',
            _tr('init_settings_global', 'Greek (CP869)'): 'cp869',
            _tr('init_settings_global', 'Greek (CP875)'): 'cp875',
            _tr('init_settings_global', 'Greek (ISO-8859-7)'): 'iso8859_7',
            _tr('init_settings_global', 'Greek (Mac OS Greek)'): 'mac_greek',
            _tr('init_settings_global', 'Greek (Windows-1253)'): 'cp1253',

            _tr('init_settings_global', 'Hebrew (CP856)'): 'cp856',
            _tr('init_settings_global', 'Hebrew (CP862)'): 'cp862',
            _tr('init_settings_global', 'Hebrew (EBCDIC 424)'): 'cp424',
            _tr('init_settings_global', 'Hebrew (ISO-8859-8)'): 'iso8859_8',
            _tr('init_settings_global', 'Hebrew (Windows-1255)'): 'cp1255',

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

            _tr('init_settings_global', 'Nordic languages (CP865)'): 'cp865',
            _tr('init_settings_global', 'Nordic languages (ISO-8859-10)'): 'iso8859_10',

            _tr('init_settings_global', 'Persian/Urdu (Mac OS Farsi)'): 'mac_farsi',

            _tr('init_settings_global', 'Portuguese (CP860)'): 'cp860',

            _tr('init_settings_global', 'Romanian (Mac OS Romanian)'): 'mac_romanian',

            _tr('init_settings_global', 'Russian (KOI8-R)'): 'koi8_r',

            _tr('init_settings_global', 'Tajik (KOI8-T)'): 'koi8_t',

            _tr('init_settings_global', 'Thai (CP874)'): 'cp874',
            _tr('init_settings_global', 'Thai (ISO-8859-11)'): 'iso8859_11',
            _tr('init_settings_global', 'Thai (TIS-620)'): 'tis_620',

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

        # Names of file types are always pluralized but not capitalized
        'file_types': {
            'files': [
                _tr('init_settings_global', 'CSV files (*.csv)'),
                _tr('init_settings_global', 'Excel workbooks (*.xlsx)'),
                _tr('init_settings_global', 'HTML pages (*.htm; *.html)'),
                _tr('init_settings_global', 'PDF files (*.pdf)'),
                _tr('init_settings_global', 'Text files (*.txt)'),
                _tr('init_settings_global', 'Translation memory files (*.tmx)'),
                _tr('init_settings_global', 'Word documents (*.docx)'),
                _tr('init_settings_global', 'XML files (*.xml)'),
                _tr('init_settings_global', 'All files (*.*)')
            ],

            'exp_tables': [
                _tr('init_settings_global', 'CSV files (*.csv)'),
                _tr('init_settings_global', 'Excel workbooks (*.xlsx)')
            ],
            'exp_tables_concordancer': [
                _tr('init_settings_global', 'CSV files (*.csv)'),
                _tr('init_settings_global', 'Excel workbooks (*.xlsx)'),
                _tr('init_settings_global', 'Word documents (*.docx)')
            ],
            'exp_tables_concordancer_zapping': [
                _tr('init_settings_global', 'Word documents (*.docx)')
            ],

            'fonts': [
                _tr('init_settings_global', 'OpenType fonts (*.otf)'),
                _tr('init_settings_global', 'TrueType fonts (*.ttf)'),
                _tr('init_settings_global', 'All files (*.*)')
            ],

            # All image formats supported by Pillow
            # Reference: https://stackoverflow.com/questions/71112986/retrieve-a-list-of-supported-read-file-extensions-formats
            'masks': [
                _tr('init_settings_global', 'Blizzard mipmap format (*.blp)'),
                _tr('init_settings_global', 'Windows bitmaps (*.bmp)'),
                _tr('init_settings_global', 'Window cursor files (*.cur)'),
                _tr('init_settings_global', 'Multi-page PCX files (*.dcx)'),
                _tr('init_settings_global', 'DirectDraw surface (*.dds)'),
                _tr('init_settings_global', 'Device-independent bitmaps (*.dib)'),
                _tr('init_settings_global', 'Encapsulated PostScript (*.eps, *.ps)'),
                _tr('init_settings_global', 'Flexible image transport system (*.fit, *.fits)'),
                _tr('init_settings_global', 'Autodesk animation files (*.flc, *.fli)'),
                _tr('init_settings_global', 'Fox Engine textures (*.ftex)'),
                _tr('init_settings_global', 'GIMP brush files (*.gbr)'),
                _tr('init_settings_global', 'Graphics interchange format (*.gif)'),
                _tr('init_settings_global', 'Apple icon images (*.icns)'),
                _tr('init_settings_global', 'Windows icon files (*.ico)'),
                _tr('init_settings_global', 'IPTC/NAA newsphoto files (*.iim)'),
                _tr('init_settings_global', 'IM files (*.im)'),
                _tr('init_settings_global', 'Image Tools image files (*)'),
                _tr('init_settings_global', 'JPEG files (*.jfif, *.jpe, *.jpeg, *.jpg)'),
                _tr('init_settings_global', 'JPEG 2000 files (*.j2c, *.j2k, *.jp2, *.jpc, *.jpf, *.jpx)'),
                _tr('init_settings_global', 'McIDAS area files (*)'),
                _tr('init_settings_global', 'Microsoft paint files (*.msp)'),
                _tr('init_settings_global', 'PhotoCD files (*.pcd)'),
                _tr('init_settings_global', 'Picture exchange (*.pcx)'),
                _tr('init_settings_global', 'PIXAR raster files (*.pxr)'),
                _tr('init_settings_global', 'Portable network graphics (*.apng, *.png)'),
                _tr('init_settings_global', 'Portable pixmap format (*.pbm, *.pgm, *.pnm, *.ppm)'),
                _tr('init_settings_global', 'Photoshop PSD files (*.psd)'),
                _tr('init_settings_global', 'Sun raster files (*.ras)'),
                _tr('init_settings_global', 'Silicon graphics images (*.bw, *.rgb, *.rgba, *.sgi)'),
                _tr('init_settings_global', 'SPIDER files (*)'),
                _tr('init_settings_global', 'Truevision TGA (*.icb, *.tga, *.vda, *.vst)'),
                _tr('init_settings_global', 'TIFF files (*.tif, *.tiff)'),
                _tr('init_settings_global', 'WebP files (*.webp)'),
                _tr('init_settings_global', 'Windows metafiles (*.emf, *.wmf)'),
                _tr('init_settings_global', 'X bitmaps (*.xbm)'),
                _tr('init_settings_global', 'X pixmaps (*.xpm)'),
                _tr('init_settings_global', 'XV thumbnails (*)'),
                _tr('init_settings_global', 'All files (*.*)')
            ],
        },

        # Only language names and proper nouns are capitalized in names of language utilities
        'lang_util_mappings': {
            'sentence_tokenizers': {
                _tr('init_settings_global', 'botok - Tibetan sentence tokenizer'): 'botok_bod',

                _tr('init_settings_global', 'NLTK - Czech Punkt sentence tokenizer'): 'nltk_punkt_ces',
                _tr('init_settings_global', 'NLTK - Danish Punkt sentence tokenizer'): 'nltk_punkt_dan',
                _tr('init_settings_global', 'NLTK - Dutch Punkt sentence tokenizer'): 'nltk_punkt_nld',
                _tr('init_settings_global', 'NLTK - English Punkt sentence tokenizer'): 'nltk_punkt_eng',
                _tr('init_settings_global', 'NLTK - Estonian Punkt sentence tokenizer'): 'nltk_punkt_est',
                _tr('init_settings_global', 'NLTK - Finnish Punkt sentence tokenizer'): 'nltk_punkt_fin',
                _tr('init_settings_global', 'NLTK - French Punkt sentence tokenizer'): 'nltk_punkt_fra',
                _tr('init_settings_global', 'NLTK - German Punkt sentence tokenizer'): 'nltk_punkt_deu',
                _tr('init_settings_global', 'NLTK - Greek Punkt sentence tokenizer'): 'nltk_punkt_ell',
                _tr('init_settings_global', 'NLTK - Italian Punkt sentence tokenizer'): 'nltk_punkt_ita',
                _tr('init_settings_global', 'NLTK - Malayalam Punkt sentence tokenizer'): 'nltk_punkt_mal',
                _tr('init_settings_global', 'NLTK - Norwegian Punkt sentence tokenizer'): 'nltk_punkt_nor',
                _tr('init_settings_global', 'NLTK - Polish Punkt sentence tokenizer'): 'nltk_punkt_pol',
                _tr('init_settings_global', 'NLTK - Portuguese Punkt sentence tokenizer'): 'nltk_punkt_por',
                _tr('init_settings_global', 'NLTK - Russian Punkt sentence tokenizer'): 'nltk_punkt_rus',
                _tr('init_settings_global', 'NLTK - Slovenian Punkt sentence tokenizer'): 'nltk_punkt_slv',
                _tr('init_settings_global', 'NLTK - Spanish Punkt sentence tokenizer'): 'nltk_punkt_spa',
                _tr('init_settings_global', 'NLTK - Swedish Punkt sentence tokenizer'): 'nltk_punkt_swe',
                _tr('init_settings_global', 'NLTK - Turkish Punkt sentence tokenizer'): 'nltk_punkt_tur',

                _tr('init_settings_global', 'PyThaiNLP - CRFCut'): 'pythainlp_crfcut',
                _tr('init_settings_global', 'PyThaiNLP - ThaiSumCut'): 'pythainlp_thaisumcut',

                _tr('init_settings_global', 'spaCy - Catalan sentence recognizer'): 'spacy_sentence_recognizer_cat',
                _tr('init_settings_global', 'spaCy - Chinese sentence recognizer'): 'spacy_sentence_recognizer_zho',
                _tr('init_settings_global', 'spaCy - Croatian sentence recognizer'): 'spacy_sentence_recognizer_hrv',
                _tr('init_settings_global', 'spaCy - Danish sentence recognizer'): 'spacy_sentence_recognizer_dan',
                _tr('init_settings_global', 'spaCy - Dutch sentence recognizer'): 'spacy_sentence_recognizer_nld',
                _tr('init_settings_global', 'spaCy - English sentence recognizer'): 'spacy_sentence_recognizer_eng',
                _tr('init_settings_global', 'spaCy - Finnish sentence recognizer'): 'spacy_sentence_recognizer_fin',
                _tr('init_settings_global', 'spaCy - French sentence recognizer'): 'spacy_sentence_recognizer_fra',
                _tr('init_settings_global', 'spaCy - German sentence recognizer'): 'spacy_sentence_recognizer_deu',
                _tr('init_settings_global', 'spaCy - Greek (Modern) sentence recognizer'): 'spacy_sentence_recognizer_ell',
                _tr('init_settings_global', 'spaCy - Italian sentence recognizer'): 'spacy_sentence_recognizer_ita',
                _tr('init_settings_global', 'spaCy - Japanese sentence recognizer'): 'spacy_sentence_recognizer_jpn',
                _tr('init_settings_global', 'spaCy - Lithuanian sentence recognizer'): 'spacy_sentence_recognizer_lit',
                _tr('init_settings_global', 'spaCy - Macedonian sentence recognizer'): 'spacy_sentence_recognizer_mkd',
                _tr('init_settings_global', 'spaCy - Norwegian Bokmål sentence recognizer'): 'spacy_sentence_recognizer_nob',
                _tr('init_settings_global', 'spaCy - Polish sentence recognizer'): 'spacy_sentence_recognizer_pol',
                _tr('init_settings_global', 'spaCy - Portuguese sentence recognizer'): 'spacy_sentence_recognizer_por',
                _tr('init_settings_global', 'spaCy - Romanian sentence recognizer'): 'spacy_sentence_recognizer_ron',
                _tr('init_settings_global', 'spaCy - Russian sentence recognizer'): 'spacy_sentence_recognizer_rus',
                _tr('init_settings_global', 'spaCy - Spanish sentence recognizer'): 'spacy_sentence_recognizer_spa',
                _tr('init_settings_global', 'spaCy - Swedish sentence recognizer'): 'spacy_sentence_recognizer_swe',
                _tr('init_settings_global', 'spaCy - Ukrainian sentence recognizer'): 'spacy_sentence_recognizer_ukr',
                _tr('init_settings_global', 'spaCy - Sentencizer'): 'spacy_sentencizer',

                _tr('init_settings_global', 'Underthesea - Vietnamese sentence tokenizer'): 'underthesea_vie'
            },

            'word_tokenizers': {
                _tr('init_settings_global', 'botok - Tibetan word tokenizer'): 'botok_bod',
                _tr('init_settings_global', 'jieba - Chinese word tokenizer'): 'jieba_zho',

                _tr('init_settings_global', 'NLTK - NIST tokenizer'): 'nltk_nist',
                _tr('init_settings_global', 'NLTK - NLTK tokenizer'): 'nltk_nltk',
                _tr('init_settings_global', 'NLTK - Penn Treebank tokenizer'): 'nltk_penn_treebank',
                _tr('init_settings_global', 'NLTK - Regular-expression tokenizer'): 'nltk_regex',
                _tr('init_settings_global', 'NLTK - Tok-tok tokenizer'): 'nltk_tok_tok',
                _tr('init_settings_global', 'NLTK - Twitter tokenizer'): 'nltk_twitter',

                _tr('init_settings_global', 'pkuseg - Chinese word tokenizer'): 'pkuseg_zho',

                _tr('init_settings_global', 'PyThaiNLP - Longest matching'): 'pythainlp_longest_matching',
                _tr('init_settings_global', 'PyThaiNLP - Maximum matching'): 'pythainlp_max_matching',
                _tr('init_settings_global', 'PyThaiNLP - Maximum matching + TCC'): 'pythainlp_max_matching_tcc',
                _tr('init_settings_global', 'PyThaiNLP - NERCut'): 'pythainlp_nercut',

                _tr('init_settings_global', 'Sacremoses - Moses tokenizer'): 'sacremoses_moses',

                _tr('init_settings_global', 'spaCy - Afrikaans word tokenizer'): 'spacy_afr',
                _tr('init_settings_global', 'spaCy - Albanian word tokenizer'): 'spacy_sqi',
                _tr('init_settings_global', 'spaCy - Amharic word tokenizer'): 'spacy_amh',
                _tr('init_settings_global', 'spaCy - Arabic word tokenizer'): 'spacy_ara',
                _tr('init_settings_global', 'spaCy - Armenian word tokenizer'): 'spacy_hye',
                _tr('init_settings_global', 'spaCy - Azerbaijani word tokenizer'): 'spacy_aze',
                _tr('init_settings_global', 'spaCy - Basque word tokenizer'): 'spacy_eus',
                _tr('init_settings_global', 'spaCy - Bengali word tokenizer'): 'spacy_ben',
                _tr('init_settings_global', 'spaCy - Bulgarian word tokenizer'): 'spacy_bul',
                _tr('init_settings_global', 'spaCy - Catalan word tokenizer'): 'spacy_cat',
                _tr('init_settings_global', 'spaCy - Chinese word tokenizer'): 'spacy_zho',
                _tr('init_settings_global', 'spaCy - Croatian word tokenizer'): 'spacy_hrv',
                _tr('init_settings_global', 'spaCy - Czech word tokenizer'): 'spacy_ces',
                _tr('init_settings_global', 'spaCy - Danish word tokenizer'): 'spacy_dan',
                _tr('init_settings_global', 'spaCy - Dutch word tokenizer'): 'spacy_nld',
                _tr('init_settings_global', 'spaCy - English word tokenizer'): 'spacy_eng',
                _tr('init_settings_global', 'spaCy - Estonian word tokenizer'): 'spacy_est',
                _tr('init_settings_global', 'spaCy - Finnish word tokenizer'): 'spacy_fin',
                _tr('init_settings_global', 'spaCy - French word tokenizer'): 'spacy_fra',
                _tr('init_settings_global', 'spaCy - Ganda word tokenizer'): 'spacy_lug',
                _tr('init_settings_global', 'spaCy - German word tokenizer'): 'spacy_deu',
                _tr('init_settings_global', 'spaCy - Greek (Ancient) word tokenizer'): 'spacy_grc',
                _tr('init_settings_global', 'spaCy - Greek (Modern) word tokenizer'): 'spacy_ell',
                _tr('init_settings_global', 'spaCy - Gujarati word tokenizer'): 'spacy_guj',
                _tr('init_settings_global', 'spaCy - Hebrew word tokenizer'): 'spacy_heb',
                _tr('init_settings_global', 'spaCy - Hindi word tokenizer'): 'spacy_hin',
                _tr('init_settings_global', 'spaCy - Hungarian word tokenizer'): 'spacy_hun',
                _tr('init_settings_global', 'spaCy - Icelandic word tokenizer'): 'spacy_isl',
                _tr('init_settings_global', 'spaCy - Indonesian word tokenizer'): 'spacy_ind',
                _tr('init_settings_global', 'spaCy - Irish word tokenizer'): 'spacy_gle',
                _tr('init_settings_global', 'spaCy - Italian word tokenizer'): 'spacy_ita',
                _tr('init_settings_global', 'spaCy - Japanese word tokenizer'): 'spacy_jpn',
                _tr('init_settings_global', 'spaCy - Kannada word tokenizer'): 'spacy_kan',
                _tr('init_settings_global', 'spaCy - Kyrgyz word tokenizer'): 'spacy_kir',
                _tr('init_settings_global', 'spaCy - Latin word tokenizer'): 'spacy_lat',
                _tr('init_settings_global', 'spaCy - Latvian word tokenizer'): 'spacy_lav',
                _tr('init_settings_global', 'spaCy - Ligurian word tokenizer'): 'spacy_lij',
                _tr('init_settings_global', 'spaCy - Lithuanian word tokenizer'): 'spacy_lit',
                _tr('init_settings_global', 'spaCy - Luxembourgish word tokenizer'): 'spacy_ltz',
                _tr('init_settings_global', 'spaCy - Macedonian word tokenizer'): 'spacy_mkd',
                _tr('init_settings_global', 'spaCy - Malayalam word tokenizer'): 'spacy_mal',
                _tr('init_settings_global', 'spaCy - Marathi word tokenizer'): 'spacy_mar',
                _tr('init_settings_global', 'spaCy - Nepali word tokenizer'): 'spacy_nep',
                _tr('init_settings_global', 'spaCy - Norwegian word tokenizer'): 'spacy_nob',
                _tr('init_settings_global', 'spaCy - Persian word tokenizer'): 'spacy_fas',
                _tr('init_settings_global', 'spaCy - Polish word tokenizer'): 'spacy_pol',
                _tr('init_settings_global', 'spaCy - Portuguese word tokenizer'): 'spacy_por',
                _tr('init_settings_global', 'spaCy - Romanian word tokenizer'): 'spacy_ron',
                _tr('init_settings_global', 'spaCy - Russian word tokenizer'): 'spacy_rus',
                _tr('init_settings_global', 'spaCy - Sanskrit word tokenizer'): 'spacy_san',
                _tr('init_settings_global', 'spaCy - Serbian word tokenizer'): 'spacy_srp',
                _tr('init_settings_global', 'spaCy - Sinhala word tokenizer'): 'spacy_sin',
                _tr('init_settings_global', 'spaCy - Slovak word tokenizer'): 'spacy_slk',
                _tr('init_settings_global', 'spaCy - Slovenian word tokenizer'): 'spacy_slv',
                _tr('init_settings_global', 'spaCy - Sorbian (Lower) word tokenizer'): 'spacy_dsb',
                _tr('init_settings_global', 'spaCy - Sorbian (Upper) word tokenizer'): 'spacy_hsb',
                _tr('init_settings_global', 'spaCy - Spanish word tokenizer'): 'spacy_spa',
                _tr('init_settings_global', 'spaCy - Swedish word tokenizer'): 'spacy_swe',
                _tr('init_settings_global', 'spaCy - Tagalog word tokenizer'): 'spacy_tgl',
                _tr('init_settings_global', 'spaCy - Tamil word tokenizer'): 'spacy_tam',
                _tr('init_settings_global', 'spaCy - Tatar word tokenizer'): 'spacy_tat',
                _tr('init_settings_global', 'spaCy - Telugu word tokenizer'): 'spacy_tel',
                _tr('init_settings_global', 'spaCy - Tigrinya word tokenizer'): 'spacy_tir',
                _tr('init_settings_global', 'spaCy - Tswana word tokenizer'): 'spacy_tsn',
                _tr('init_settings_global', 'spaCy - Turkish word tokenizer'): 'spacy_tur',
                _tr('init_settings_global', 'spaCy - Ukrainian word tokenizer'): 'spacy_ukr',
                _tr('init_settings_global', 'spaCy - Urdu word tokenizer'): 'spacy_urd',
                _tr('init_settings_global', 'spaCy - Yoruba word tokenizer'): 'spacy_yor',

                _tr('init_settings_global', 'SudachiPy - Japanese word tokenizer (split mode A)'): 'sudachipy_jpn_split_mode_a',
                _tr('init_settings_global', 'SudachiPy - Japanese word tokenizer (split mode B)'): 'sudachipy_jpn_split_mode_b',
                _tr('init_settings_global', 'SudachiPy - Japanese word tokenizer (split mode C)'): 'sudachipy_jpn_split_mode_c',

                _tr('init_settings_global', 'Underthesea - Vietnamese word tokenizer'): 'underthesea_vie',

                _tr('init_settings_global', 'Wordless - Chinese character tokenizer'): 'wordless_zho_char',
                _tr('init_settings_global', 'Wordless - Japanese kanji tokenizer'): 'wordless_jpn_kanji'
            },

            'syl_tokenizers': {
                _tr('init_settings_global', 'NLTK - Legality syllable tokenizer'): 'nltk_legality',
                _tr('init_settings_global', 'NLTK - Sonority sequencing syllable tokenizer'): 'nltk_sonority_sequencing',

                _tr('init_settings_global', 'Pyphen - Afrikaans syllable tokenizer'): 'pyphen_afr',
                _tr('init_settings_global', 'Pyphen - Albanian syllable tokenizer'): 'pyphen_sqi',
                _tr('init_settings_global', 'Pyphen - Belarusian syllable tokenizer'): 'pyphen_bel',
                _tr('init_settings_global', 'Pyphen - Bulgarian syllable tokenizer'): 'pyphen_bul',
                _tr('init_settings_global', 'Pyphen - Catalan syllable tokenizer'): 'pyphen_cat',
                _tr('init_settings_global', 'Pyphen - Croatian syllable tokenizer'): 'pyphen_hrv',
                _tr('init_settings_global', 'Pyphen - Czech syllable tokenizer'): 'pyphen_ces',
                _tr('init_settings_global', 'Pyphen - Danish syllable tokenizer'): 'pyphen_dan',
                _tr('init_settings_global', 'Pyphen - Dutch syllable tokenizer'): 'pyphen_nld',
                _tr('init_settings_global', 'Pyphen - English (United Kingdom) syllable tokenizer'): 'pyphen_eng_gb',
                _tr('init_settings_global', 'Pyphen - English (United States) syllable tokenizer'): 'pyphen_eng_us',
                _tr('init_settings_global', 'Pyphen - Esperanto syllable tokenizer'): 'pyphen_epo',
                _tr('init_settings_global', 'Pyphen - Estonian syllable tokenizer'): 'pyphen_est',
                _tr('init_settings_global', 'Pyphen - French syllable tokenizer'): 'pyphen_fra',
                _tr('init_settings_global', 'Pyphen - Galician syllable tokenizer'): 'pyphen_glg',
                _tr('init_settings_global', 'Pyphen - German (Austria) syllable tokenizer'): 'pyphen_deu_at',
                _tr('init_settings_global', 'Pyphen - German (Germany) syllable tokenizer'): 'pyphen_deu_de',
                _tr('init_settings_global', 'Pyphen - German (Switzerland) syllable tokenizer'): 'pyphen_deu_ch',
                _tr('init_settings_global', 'Pyphen - Greek (Modern) syllable tokenizer'): 'pyphen_ell',
                _tr('init_settings_global', 'Pyphen - Hungarian syllable tokenizer'): 'pyphen_hun',
                _tr('init_settings_global', 'Pyphen - Icelandic syllable tokenizer'): 'pyphen_isl',
                _tr('init_settings_global', 'Pyphen - Indonesian syllable tokenizer'): 'pyphen_ind',
                _tr('init_settings_global', 'Pyphen - Italian syllable tokenizer'): 'pyphen_ita',
                _tr('init_settings_global', 'Pyphen - Lithuanian syllable tokenizer'): 'pyphen_lit',
                _tr('init_settings_global', 'Pyphen - Latvian syllable tokenizer'): 'pyphen_lav',
                _tr('init_settings_global', 'Pyphen - Mongolian syllable tokenizer'): 'pyphen_mon',
                _tr('init_settings_global', 'Pyphen - Norwegian Bokmål syllable tokenizer'): 'pyphen_nob',
                _tr('init_settings_global', 'Pyphen - Norwegian Nynorsk syllable tokenizer'): 'pyphen_nno',
                _tr('init_settings_global', 'Pyphen - Polish syllable tokenizer'): 'pyphen_pol',
                _tr('init_settings_global', 'Pyphen - Portuguese (Brazil) syllable tokenizer'): 'pyphen_por_br',
                _tr('init_settings_global', 'Pyphen - Portuguese (Portugal) syllable tokenizer'): 'pyphen_por_pt',
                _tr('init_settings_global', 'Pyphen - Romanian syllable tokenizer'): 'pyphen_ron',
                _tr('init_settings_global', 'Pyphen - Russian syllable tokenizer'): 'pyphen_rus',
                _tr('init_settings_global', 'Pyphen - Serbian (Cyrillic) syllable tokenizer'): 'pyphen_srp_cyrl',
                _tr('init_settings_global', 'Pyphen - Serbian (Latin) syllable tokenizer'): 'pyphen_srp_latn',
                _tr('init_settings_global', 'Pyphen - Slovak syllable tokenizer'): 'pyphen_slk',
                _tr('init_settings_global', 'Pyphen - Slovenian syllable tokenizer'): 'pyphen_slv',
                _tr('init_settings_global', 'Pyphen - Spanish syllable tokenizer'): 'pyphen_spa',
                _tr('init_settings_global', 'Pyphen - Swedish syllable tokenizer'): 'pyphen_swe',
                _tr('init_settings_global', 'Pyphen - Telugu syllable tokenizer'): 'pyphen_tel',
                _tr('init_settings_global', 'Pyphen - Thai syllable tokenizer'): 'pyphen_tha',
                _tr('init_settings_global', 'Pyphen - Ukrainian syllable tokenizer'): 'pyphen_ukr',
                _tr('init_settings_global', 'Pyphen - Zulu syllable tokenizer'): 'pyphen_zul',

                _tr('init_settings_global', 'PyThaiNLP - Thai syllable tokenizer'): 'pythainlp_tha'
            },

            'pos_taggers': {
                _tr('init_settings_global', 'botok - Tibetan part-of-speech tagger'): 'botok_bod',
                _tr('init_settings_global', 'jieba - Chinese part-of-speech tagger'): 'jieba_zho',

                _tr('init_settings_global', 'NLTK - English perceptron part-of-speech tagger'): 'nltk_perceptron_eng',
                _tr('init_settings_global', 'NLTK - Russian perceptron part-of-speech tagger'): 'nltk_perceptron_rus',

                _tr('init_settings_global', 'pymorphy2 - Morphological analyzer'): 'pymorphy2_morphological_analyzer',

                _tr('init_settings_global', 'PyThaiNLP - Perceptron part-of-speech tagger (LST20)'): 'pythainlp_perceptron_lst20',
                _tr('init_settings_global', 'PyThaiNLP - Perceptron part-of-speech tagger (ORCHID)'): 'pythainlp_perceptron_orchid',
                _tr('init_settings_global', 'PyThaiNLP - Perceptron part-of-speech tagger (PUD)'): 'pythainlp_perceptron_pud',

                _tr('init_settings_global', 'spaCy - Catalan part-of-speech tagger'): 'spacy_cat',
                _tr('init_settings_global', 'spaCy - Chinese part-of-speech tagger'): 'spacy_zho',
                _tr('init_settings_global', 'spaCy - Croatian part-of-speech tagger'): 'spacy_hrv',
                _tr('init_settings_global', 'spaCy - Danish part-of-speech tagger'): 'spacy_dan',
                _tr('init_settings_global', 'spaCy - Dutch part-of-speech tagger'): 'spacy_nld',
                _tr('init_settings_global', 'spaCy - English part-of-speech tagger'): 'spacy_eng',
                _tr('init_settings_global', 'spaCy - Finnish part-of-speech tagger'): 'spacy_fin',
                _tr('init_settings_global', 'spaCy - French part-of-speech tagger'): 'spacy_fra',
                _tr('init_settings_global', 'spaCy - German part-of-speech tagger'): 'spacy_deu',
                _tr('init_settings_global', 'spaCy - Greek (Modern) part-of-speech tagger'): 'spacy_ell',
                _tr('init_settings_global', 'spaCy - Italian part-of-speech tagger'): 'spacy_ita',
                _tr('init_settings_global', 'spaCy - Japanese part-of-speech tagger'): 'spacy_jpn',
                _tr('init_settings_global', 'spaCy - Lithuanian part-of-speech tagger'): 'spacy_lit',
                _tr('init_settings_global', 'spaCy - Macedonian part-of-speech tagger'): 'spacy_mkd',
                _tr('init_settings_global', 'spaCy - Norwegian Bokmål part-of-speech tagger'): 'spacy_nob',
                _tr('init_settings_global', 'spaCy - Polish part-of-speech tagger'): 'spacy_pol',
                _tr('init_settings_global', 'spaCy - Portuguese part-of-speech tagger'): 'spacy_por',
                _tr('init_settings_global', 'spaCy - Romanian part-of-speech tagger'): 'spacy_ron',
                _tr('init_settings_global', 'spaCy - Russian part-of-speech tagger'): 'spacy_rus',
                _tr('init_settings_global', 'spaCy - Spanish part-of-speech tagger'): 'spacy_spa',
                _tr('init_settings_global', 'spaCy - Swedish part-of-speech tagger'): 'spacy_swe',
                _tr('init_settings_global', 'spaCy - Ukrainian part-of-speech tagger'): 'spacy_ukr',

                _tr('init_settings_global', 'SudachiPy - Japanese part-of-speech tagger'): 'sudachipy_jpn',

                _tr('init_settings_global', 'Underthesea - Vietnamese part-of-speech tagger'): 'underthesea_vie'
            },

            'lemmatizers': {
                _tr('init_settings_global', 'botok - Tibetan lemmatizer'): 'botok_bod',

                _tr('init_settings_global', 'NLTK - WordNet lemmatizer'): 'nltk_wordnet',
                _tr('init_settings_global', 'pymorphy2 - Morphological analyzer'): 'pymorphy2_morphological_analyzer',

                _tr('init_settings_global', 'simplemma - Albanian lemmatizer'): 'simplemma_sqi',
                _tr('init_settings_global', 'simplemma - Armenian lemmatizer'): 'simplemma_hye',
                _tr('init_settings_global', 'simplemma - Asturian lemmatizer'): 'simplemma_ast',
                _tr('init_settings_global', 'simplemma - Bulgarian lemmatizer'): 'simplemma_bul',
                _tr('init_settings_global', 'simplemma - Catalan lemmatizer'): 'simplemma_cat',
                _tr('init_settings_global', 'simplemma - Czech lemmatizer'): 'simplemma_ces',
                _tr('init_settings_global', 'simplemma - Danish lemmatizer'): 'simplemma_dan',
                _tr('init_settings_global', 'simplemma - Dutch lemmatizer'): 'simplemma_nld',
                _tr('init_settings_global', 'simplemma - English lemmatizer'): 'simplemma_eng',
                _tr('init_settings_global', 'simplemma - English (Middle) lemmatizer'): 'simplemma_enm',
                _tr('init_settings_global', 'simplemma - Estonian lemmatizer'): 'simplemma_est',
                _tr('init_settings_global', 'simplemma - Finnish lemmatizer'): 'simplemma_fin',
                _tr('init_settings_global', 'simplemma - French lemmatizer'): 'simplemma_fra',
                _tr('init_settings_global', 'simplemma - Galician lemmatizer'): 'simplemma_glg',
                _tr('init_settings_global', 'simplemma - Georgian lemmatizer'): 'simplemma_kat',
                _tr('init_settings_global', 'simplemma - German lemmatizer'): 'simplemma_deu',
                _tr('init_settings_global', 'simplemma - Greek (Modern) lemmatizer'): 'simplemma_ell',
                _tr('init_settings_global', 'simplemma - Hindi lemmatizer'): 'simplemma_hin',
                _tr('init_settings_global', 'simplemma - Hungarian lemmatizer'): 'simplemma_hun',
                _tr('init_settings_global', 'simplemma - Icelandic lemmatizer'): 'simplemma_isl',
                _tr('init_settings_global', 'simplemma - Indonesian lemmatizer'): 'simplemma_ind',
                _tr('init_settings_global', 'simplemma - Irish lemmatizer'): 'simplemma_gle',
                _tr('init_settings_global', 'simplemma - Italian lemmatizer'): 'simplemma_ita',
                _tr('init_settings_global', 'simplemma - Latin lemmatizer'): 'simplemma_lat',
                _tr('init_settings_global', 'simplemma - Latvian lemmatizer'): 'simplemma_lav',
                _tr('init_settings_global', 'simplemma - Lithuanian lemmatizer'): 'simplemma_lit',
                _tr('init_settings_global', 'simplemma - Luxembourgish lemmatizer'): 'simplemma_ltz',
                _tr('init_settings_global', 'simplemma - Macedonian lemmatizer'): 'simplemma_mkd',
                _tr('init_settings_global', 'simplemma - Malay lemmatizer'): 'simplemma_msa',
                _tr('init_settings_global', 'simplemma - Manx lemmatizer'): 'simplemma_glv',
                _tr('init_settings_global', 'simplemma - Norwegian Bokmål lemmatizer'): 'simplemma_nob',
                _tr('init_settings_global', 'simplemma - Norwegian Nynorsk lemmatizer'): 'simplemma_nno',
                _tr('init_settings_global', 'simplemma - Persian lemmatizer'): 'simplemma_fas',
                _tr('init_settings_global', 'simplemma - Polish lemmatizer'): 'simplemma_pol',
                _tr('init_settings_global', 'simplemma - Portuguese lemmatizer'): 'simplemma_por',
                _tr('init_settings_global', 'simplemma - Romanian lemmatizer'): 'simplemma_ron',
                _tr('init_settings_global', 'simplemma - Russian lemmatizer'): 'simplemma_rus',
                _tr('init_settings_global', 'simplemma - Sámi (Northern) lemmatizer'): 'simplemma_sme',
                _tr('init_settings_global', 'simplemma - Scottish Gaelic lemmatizer'): 'simplemma_gla',
                _tr('init_settings_global', 'simplemma - Serbo-Croatian lemmatizer'): 'simplemma_srp_latn',
                _tr('init_settings_global', 'simplemma - Slovak lemmatizer'): 'simplemma_slk',
                _tr('init_settings_global', 'simplemma - Slovenian lemmatizer'): 'simplemma_slv',
                _tr('init_settings_global', 'simplemma - Spanish lemmatizer'): 'simplemma_spa',
                _tr('init_settings_global', 'simplemma - Swahili lemmatizer'): 'simplemma_swa',
                _tr('init_settings_global', 'simplemma - Swedish lemmatizer'): 'simplemma_swe',
                _tr('init_settings_global', 'simplemma - Tagalog lemmatizer'): 'simplemma_tgl',
                _tr('init_settings_global', 'simplemma - Turkish lemmatizer'): 'simplemma_tur',
                _tr('init_settings_global', 'simplemma - Ukrainian lemmatizer'): 'simplemma_ukr',
                _tr('init_settings_global', 'simplemma - Welsh lemmatizer'): 'simplemma_cym',

                _tr('init_settings_global', 'spaCy - Bengali lemmatizer'): 'spacy_ben',
                _tr('init_settings_global', 'spaCy - Catalan lemmatizer'): 'spacy_cat',
                _tr('init_settings_global', 'spaCy - Croatian lemmatizer'): 'spacy_hrv',
                _tr('init_settings_global', 'spaCy - Czech lemmatizer'): 'spacy_ces',
                _tr('init_settings_global', 'spaCy - Danish lemmatizer'): 'spacy_dan',
                _tr('init_settings_global', 'spaCy - Dutch lemmatizer'): 'spacy_nld',
                _tr('init_settings_global', 'spaCy - English lemmatizer'): 'spacy_eng',
                _tr('init_settings_global', 'spaCy - Finnish lemmatizer'): 'spacy_fin',
                _tr('init_settings_global', 'spaCy - French lemmatizer'): 'spacy_fra',
                _tr('init_settings_global', 'spaCy - German lemmatizer'): 'spacy_deu',
                _tr('init_settings_global', 'spaCy - Greek (Ancient) lemmatizer'): 'spacy_grc',
                _tr('init_settings_global', 'spaCy - Greek (Modern) lemmatizer'): 'spacy_ell',
                _tr('init_settings_global', 'spaCy - Hungarian lemmatizer'): 'spacy_hun',
                _tr('init_settings_global', 'spaCy - Indonesian lemmatizer'): 'spacy_ind',
                _tr('init_settings_global', 'spaCy - Irish lemmatizer'): 'spacy_gle',
                _tr('init_settings_global', 'spaCy - Italian lemmatizer'): 'spacy_ita',
                _tr('init_settings_global', 'spaCy - Japanese lemmatizer'): 'spacy_jpn',
                _tr('init_settings_global', 'spaCy - Lithuanian lemmatizer'): 'spacy_lit',
                _tr('init_settings_global', 'spaCy - Luxembourgish lemmatizer'): 'spacy_ltz',
                _tr('init_settings_global', 'spaCy - Macedonian lemmatizer'): 'spacy_mkd',
                _tr('init_settings_global', 'spaCy - Norwegian Bokmål lemmatizer'): 'spacy_nob',
                _tr('init_settings_global', 'spaCy - Persian lemmatizer'): 'spacy_fas',
                _tr('init_settings_global', 'spaCy - Polish lemmatizer'): 'spacy_pol',
                _tr('init_settings_global', 'spaCy - Portuguese lemmatizer'): 'spacy_por',
                _tr('init_settings_global', 'spaCy - Romanian lemmatizer'): 'spacy_ron',
                _tr('init_settings_global', 'spaCy - Russian lemmatizer'): 'spacy_rus',
                _tr('init_settings_global', 'spaCy - Serbian lemmatizer'): 'spacy_srp',
                _tr('init_settings_global', 'spaCy - Spanish lemmatizer'): 'spacy_spa',
                _tr('init_settings_global', 'spaCy - Swedish lemmatizer'): 'spacy_swe',
                _tr('init_settings_global', 'spaCy - Tagalog lemmatizer'): 'spacy_tgl',
                _tr('init_settings_global', 'spaCy - Turkish lemmatizer'): 'spacy_tur',
                _tr('init_settings_global', 'spaCy - Ukrainian lemmatizer'): 'spacy_ukr',
                _tr('init_settings_global', 'spaCy - Urdu lemmatizer'): 'spacy_urd',

                _tr('init_settings_global', 'SudachiPy - Japanese lemmatizer'): 'sudachipy_jpn'
            },

            'stop_word_lists': {
                _tr('init_settings_global', 'NLTK - Arabic stop word list'): 'nltk_ara',
                _tr('init_settings_global', 'NLTK - Azerbaijani stop word list'): 'nltk_aze',
                _tr('init_settings_global', 'NLTK - Basque stop word list'): 'nltk_eus',
                _tr('init_settings_global', 'NLTK - Bengali stop word list'): 'nltk_ben',
                _tr('init_settings_global', 'NLTK - Catalan stop word list'): 'nltk_cat',
                _tr('init_settings_global', 'NLTK - Chinese (Simplified) stop word list'): 'nltk_zho_cn',
                _tr('init_settings_global', 'NLTK - Chinese (Traditional) stop word list'): 'nltk_zho_tw',
                _tr('init_settings_global', 'NLTK - Danish stop word list'): 'nltk_dan',
                _tr('init_settings_global', 'NLTK - Dutch stop word list'): 'nltk_nld',
                _tr('init_settings_global', 'NLTK - English stop word list'): 'nltk_eng',
                _tr('init_settings_global', 'NLTK - Finnish stop word list'): 'nltk_fin',
                _tr('init_settings_global', 'NLTK - French stop word list'): 'nltk_fra',
                _tr('init_settings_global', 'NLTK - German stop word list'): 'nltk_deu',
                _tr('init_settings_global', 'NLTK - Greek (Modern) stop word list'): 'nltk_ell',
                _tr('init_settings_global', 'NLTK - Hebrew stop word list'): 'nltk_heb',
                _tr('init_settings_global', 'NLTK - Hungarian stop word list'): 'nltk_hun',
                _tr('init_settings_global', 'NLTK - Indonesian stop word list'): 'nltk_ind',
                _tr('init_settings_global', 'NLTK - Italian stop word list'): 'nltk_ita',
                _tr('init_settings_global', 'NLTK - Kazakh stop word list'): 'nltk_kaz',
                _tr('init_settings_global', 'NLTK - Nepali stop word list'): 'nltk_nep',
                _tr('init_settings_global', 'NLTK - Norwegian stop word list'): 'nltk_nor',
                _tr('init_settings_global', 'NLTK - Portuguese stop word list'): 'nltk_por',
                _tr('init_settings_global', 'NLTK - Romanian stop word list'): 'nltk_ron',
                _tr('init_settings_global', 'NLTK - Russian stop word list'): 'nltk_rus',
                _tr('init_settings_global', 'NLTK - Slovenian stop word list'): 'nltk_slv',
                _tr('init_settings_global', 'NLTK - Spanish stop word list'): 'nltk_spa',
                _tr('init_settings_global', 'NLTK - Swedish stop word list'): 'nltk_swe',
                _tr('init_settings_global', 'NLTK - Tajik stop word list'): 'nltk_tgk',
                _tr('init_settings_global', 'NLTK - Turkish stop word list'): 'nltk_tur',

                _tr('init_settings_global', 'PyThaiNLP - Thai stop word list'): 'pythainlp_tha',

                _tr('init_settings_global', 'stopword - Afrikaans stop word list'): 'stopword_afr',
                _tr('init_settings_global', 'stopword - Arabic stop word list'): 'stopword_ara',
                _tr('init_settings_global', 'stopword - Armenian stop word list'): 'stopword_hye',
                _tr('init_settings_global', 'stopword - Basque stop word list'): 'stopword_eus',
                _tr('init_settings_global', 'stopword - Bengali stop word list'): 'stopword_ben',
                _tr('init_settings_global', 'stopword - Breton stop word list'): 'stopword_bre',
                _tr('init_settings_global', 'stopword - Bulgarian stop word list'): 'stopword_bul',
                _tr('init_settings_global', 'stopword - Catalan stop word list'): 'stopword_cat',
                _tr('init_settings_global', 'stopword - Chinese (Simplified) stop word list'): 'stopword_zho_cn',
                _tr('init_settings_global', 'stopword - Chinese (Traditional) stop word list'): 'stopword_zho_tw',
                _tr('init_settings_global', 'stopword - Croatian stop word list'): 'stopword_hrv',
                _tr('init_settings_global', 'stopword - Czech stop word list'): 'stopword_ces',
                _tr('init_settings_global', 'stopword - Danish stop word list'): 'stopword_dan',
                _tr('init_settings_global', 'stopword - Dutch stop word list'): 'stopword_nld',
                _tr('init_settings_global', 'stopword - English stop word list'): 'stopword_eng',
                _tr('init_settings_global', 'stopword - Esperanto stop word list'): 'stopword_epo',
                _tr('init_settings_global', 'stopword - Estonian stop word list'): 'stopword_est',
                _tr('init_settings_global', 'stopword - Finnish stop word list'): 'stopword_fin',
                _tr('init_settings_global', 'stopword - French stop word list'): 'stopword_fra',
                _tr('init_settings_global', 'stopword - Galician stop word list'): 'stopword_glg',
                _tr('init_settings_global', 'stopword - German stop word list'): 'stopword_deu',
                _tr('init_settings_global', 'stopword - Greek (Modern) stop word list'): 'stopword_ell',
                _tr('init_settings_global', 'stopword - Gujarati stop word list'): 'stopword_guj',
                _tr('init_settings_global', 'stopword - Hausa stop word list'): 'stopword_hau',
                _tr('init_settings_global', 'stopword - Hebrew stop word list'): 'stopword_heb',
                _tr('init_settings_global', 'stopword - Hindi stop word list'): 'stopword_hin',
                _tr('init_settings_global', 'stopword - Hungarian stop word list'): 'stopword_hun',
                _tr('init_settings_global', 'stopword - Indonesian stop word list'): 'stopword_ind',
                _tr('init_settings_global', 'stopword - Irish stop word list'): 'stopword_gle',
                _tr('init_settings_global', 'stopword - Italian stop word list'): 'stopword_ita',
                _tr('init_settings_global', 'stopword - Japanese stop word list'): 'stopword_jpn',
                _tr('init_settings_global', 'stopword - Korean stop word list'): 'stopword_kor',
                _tr('init_settings_global', 'stopword - Kurdish stop word list'): 'stopword_kur',
                _tr('init_settings_global', 'stopword - Latin stop word list'): 'stopword_lat',
                _tr('init_settings_global', 'stopword - Latvian stop word list'): 'stopword_lav',
                _tr('init_settings_global', 'stopword - Lithuanian stop word list'): 'stopword_lit',
                _tr('init_settings_global', 'stopword - Lugbara stop word list'): 'stopword_lgg',
                _tr('init_settings_global', 'stopword - Malay stop word list'): 'stopword_msa',
                _tr('init_settings_global', 'stopword - Marathi stop word list'): 'stopword_mar',
                _tr('init_settings_global', 'stopword - Myanmar stop word list'): 'stopword_mya',
                _tr('init_settings_global', 'stopword - Norwegian Bokmål stop word list'): 'stopword_nob',
                _tr('init_settings_global', 'stopword - Persian stop word list'): 'stopword_fas',
                _tr('init_settings_global', 'stopword - Polish stop word list'): 'stopword_pol',
                _tr('init_settings_global', 'stopword - Portuguese (Brazil) stop word list'): 'stopword_por_br',
                _tr('init_settings_global', 'stopword - Portuguese (Portugal) stop word list'): 'stopword_por_pt',
                _tr('init_settings_global', 'stopword - Punjabi (Gurmukhi) stop word list'): 'stopword_pan_guru',
                _tr('init_settings_global', 'stopword - Romanian stop word list'): 'stopword_ron',
                _tr('init_settings_global', 'stopword - Russian stop word list'): 'stopword_rus',
                _tr('init_settings_global', 'stopword - Slovak stop word list'): 'stopword_slk',
                _tr('init_settings_global', 'stopword - Slovenian stop word list'): 'stopword_slv',
                _tr('init_settings_global', 'stopword - Somali stop word list'): 'stopword_som',
                _tr('init_settings_global', 'stopword - Sotho (Southern) stop word list'): 'stopword_sot',
                _tr('init_settings_global', 'stopword - Spanish stop word list'): 'stopword_spa',
                _tr('init_settings_global', 'stopword - Swahili stop word list'): 'stopword_swa',
                _tr('init_settings_global', 'stopword - Swedish stop word list'): 'stopword_swe',
                _tr('init_settings_global', 'stopword - Tagalog stop word list'): 'stopword_tgl',
                _tr('init_settings_global', 'stopword - Thai stop word list'): 'stopword_tha',
                _tr('init_settings_global', 'stopword - Turkish stop word list'): 'stopword_tur',
                _tr('init_settings_global', 'stopword - Ukrainian stop word list'): 'stopword_ukr',
                _tr('init_settings_global', 'stopword - Urdu stop word list'): 'stopword_urd',
                _tr('init_settings_global', 'stopword - Vietnamese stop word list'): 'stopword_vie',
                _tr('init_settings_global', 'stopword - Yoruba stop word list'): 'stopword_yor',
                _tr('init_settings_global', 'stopword - Zulu stop word list'): 'stopword_zul',

                _tr('init_settings_global', 'Custom stop word list'): 'custom',
            },

            'dependency_parsers':{
                _tr('init_settings_global', 'spaCy - Catalan dependency parser'): 'spacy_cat',
                _tr('init_settings_global', 'spaCy - Chinese dependency parser'): 'spacy_zho',
                _tr('init_settings_global', 'spaCy - Croatian dependency parser'): 'spacy_hrv',
                _tr('init_settings_global', 'spaCy - Danish dependency parser'): 'spacy_dan',
                _tr('init_settings_global', 'spaCy - Dutch dependency parser'): 'spacy_nld',
                _tr('init_settings_global', 'spaCy - English dependency parser'): 'spacy_eng',
                _tr('init_settings_global', 'spaCy - Finnish dependency parser'): 'spacy_fin',
                _tr('init_settings_global', 'spaCy - French dependency parser'): 'spacy_fra',
                _tr('init_settings_global', 'spaCy - German dependency parser'): 'spacy_deu',
                _tr('init_settings_global', 'spaCy - Greek (Modern) dependency parser'): 'spacy_ell',
                _tr('init_settings_global', 'spaCy - Italian dependency parser'): 'spacy_ita',
                _tr('init_settings_global', 'spaCy - Japanese dependency parser'): 'spacy_jpn',
                _tr('init_settings_global', 'spaCy - Lithuanian dependency parser'): 'spacy_lit',
                _tr('init_settings_global', 'spaCy - Macedonian dependency parser'): 'spacy_mkd',
                _tr('init_settings_global', 'spaCy - Norwegian Bokmål dependency parser'): 'spacy_nob',
                _tr('init_settings_global', 'spaCy - Polish dependency parser'): 'spacy_pol',
                _tr('init_settings_global', 'spaCy - Portuguese dependency parser'): 'spacy_por',
                _tr('init_settings_global', 'spaCy - Romanian dependency parser'): 'spacy_ron',
                _tr('init_settings_global', 'spaCy - Russian dependency parser'): 'spacy_rus',
                _tr('init_settings_global', 'spaCy - Spanish dependency parser'): 'spacy_spa',
                _tr('init_settings_global', 'spaCy - Swedish dependency parser'): 'spacy_swe',
                _tr('init_settings_global', 'spaCy - Ukrainian dependency parser'): 'spacy_ukr'
            }
        },

        'sentence_tokenizers': {
            'cat': ['spacy_sentence_recognizer_cat'],
            'zho_cn': ['spacy_sentence_recognizer_zho',],
            'zho_tw': ['spacy_sentence_recognizer_zho'],
            'hrv': ['spacy_sentence_recognizer_hrv'],

            'ces': [
                'nltk_punkt_ces',
                'spacy_sentencizer'
            ],

            'dan': [
                'nltk_punkt_dan',
                'spacy_sentence_recognizer_dan'
            ],

            'nld': [
                'nltk_punkt_nld',
                'spacy_sentence_recognizer_nld'
            ],

            'eng_gb': [
                'nltk_punkt_eng',
                'spacy_sentence_recognizer_eng'
            ],

            'eng_us': [
                'nltk_punkt_eng',
                'spacy_sentence_recognizer_eng'
            ],

            'est': [
                'nltk_punkt_est',
                'spacy_sentencizer'
            ],

            'fin': [
                'nltk_punkt_fin',
                'spacy_sentence_recognizer_fin'
            ],

            'fra': [
                'nltk_punkt_fra',
                'spacy_sentence_recognizer_fra'
            ],

            'deu_at': [
                'nltk_punkt_deu',
                'spacy_sentence_recognizer_deu'
            ],

            'deu_de': [
                'nltk_punkt_deu',
                'spacy_sentence_recognizer_deu'
            ],

            'deu_ch': [
                'nltk_punkt_deu',
                'spacy_sentence_recognizer_deu'
            ],

            'ell': [
                'nltk_punkt_ell',
                'spacy_sentence_recognizer_ell'
            ],

            'ita': [
                'nltk_punkt_ita',
                'spacy_sentence_recognizer_ita'
            ],

            'jpn': ['spacy_sentence_recognizer_jpn'],
            'lit': ['spacy_sentence_recognizer_lit'],
            'mkd': ['spacy_sentence_recognizer_mkd'],

            'mal': [
                'nltk_punkt_mal',
                'spacy_sentencizer'
            ],

            'nob': [
                'nltk_punkt_nor',
                'spacy_sentence_recognizer_nob'
            ],

            'nno': [
                'nltk_punkt_nor',
                'spacy_sentencizer'
            ],

            'pol': [
                'nltk_punkt_pol',
                'spacy_sentence_recognizer_pol'
            ],

            'por_br': [
                'nltk_punkt_por',
                'spacy_sentence_recognizer_por'
            ],

            'por_pt': [
                'nltk_punkt_por',
                'spacy_sentence_recognizer_por'
            ],

            'ron': ['spacy_sentence_recognizer_ron'],

            'rus': [
                'nltk_punkt_rus',
                'spacy_sentence_recognizer_rus'
            ],

            'slv': [
                'nltk_punkt_slv',
                'spacy_sentencizer'
            ],

            'spa': [
                'nltk_punkt_spa',
                'spacy_sentence_recognizer_spa'
            ],

            'swe': [
                'nltk_punkt_swe',
                'spacy_sentence_recognizer_swe'
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

            'ukr': ['spacy_sentence_recognizer_ukr'],
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

            'lug': ['spacy_lug'],

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

            'lat': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_lat'
            ],

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

            'tha': [
                'pyphen_tha',
                'pythainlp_tha'
            ],

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
            'ast': ['simplemma_ast'],
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
            'srp_cyrl': ['spacy_srp'],
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
            'afr': ['stopword_afr'],

            'ara': [
                'nltk_ara',
                'stopword_ara'
            ],

            'hye': ['stopword_hye'],
            'aze': ['nltk_aze'],

            'eus': [
                'nltk_eus',
                'stopword_eus'
            ],

            'ben': [
                'nltk_ben',
                'stopword_ben'
            ],

            'bre': ['stopword_bre'],
            'bul': ['stopword_bul'],

            'cat': [
                'nltk_cat',
                'stopword_cat'
            ],

            'zho_cn': [
                'nltk_zho_cn',
                'stopword_zho_cn'
            ],

            'zho_tw': [
                'nltk_zho_tw',
                'stopword_zho_tw'
            ],

            'hrv': ['stopword_hrv'],
            'ces': ['stopword_ces'],

            'dan': [
                'nltk_dan',
                'stopword_dan'
            ],

            'nld': [
                'nltk_nld',
                'stopword_nld'
            ],

            'eng_gb': [
                'nltk_eng',
                'stopword_eng'
            ],

            'eng_us': [
                'nltk_eng',
                'stopword_eng'
            ],

            'epo': ['stopword_epo'],
            'est': ['stopword_est'],

            'fin': [
                'nltk_fin',
                'stopword_fin'
            ],

            'fra': [
                'nltk_fra',
                'stopword_fra'
            ],

            'glg': ['stopword_glg'],

            'deu_at': [
                'nltk_deu',
                'stopword_deu'
            ],

            'deu_de': [
                'nltk_deu',
                'stopword_deu'
            ],

            'deu_ch': [
                'nltk_deu',
                'stopword_deu'
            ],

            'ell': [
                'nltk_ell',
                'stopword_ell'
            ],

            'guj': ['stopword_guj'],
            'hau': ['stopword_hau'],

            'heb': [
                'nltk_heb',
                'stopword_heb'
            ],

            'hin': ['stopword_hin'],

            'hun': [
                'nltk_hun',
                'stopword_hun'
            ],

            'ind': [
                'nltk_ind',
                'stopword_ind'
            ],

            'gle': ['stopword_gle'],

            'ita': [
                'nltk_ita',
                'stopword_ita'
            ],

            'jpn': ['stopword_jpn'],
            'kaz': ['nltk_kaz'],
            'kor': ['stopword_kor'],
            'kur': ['stopword_kur'],
            'lat': ['stopword_lat'],
            'lav': ['stopword_lav'],
            'lit': ['stopword_lit'],
            'lgg': ['stopword_lgg'],
            'msa': ['stopword_msa'],
            'mar': ['stopword_mar'],
            'mya': ['stopword_mya'],
            'nep': ['nltk_nep'],

            'nob': [
                'nltk_nor',
                'stopword_nob'
            ],

            'nno': ['nltk_nor'],
            'fas': ['stopword_fas'],
            'pol': ['stopword_pol'],

            'por_br': [
                'nltk_por',
                'stopword_por_br'
            ],

            'por_pt': [
                'nltk_por',
                'stopword_por_pt'
            ],

            'pan_guru': ['stopword_pan_guru'],

            'ron': [
                'nltk_ron',
                'stopword_ron'
            ],

            'rus': [
                'nltk_rus',
                'stopword_rus'
            ],

            'slk': ['stopword_slk'],

            'slv': [
                'nltk_slv',
                'stopword_slv'
            ],

            'som': ['stopword_som'],
            'sot': ['stopword_sot'],

            'spa': [
                'nltk_spa',
                'stopword_spa'
            ],

            'swa': ['stopword_swa'],

            'swe': [
                'nltk_swe',
                'stopword_swe'
            ],

            'tgl': ['stopword_tgl'],
            'tgk': ['nltk_tgk'],

            'tha': [
                'pythainlp_tha',
                'stopword_tha'
            ],

            'tur': [
                'nltk_tur',
                'stopword_tur'
            ],

            'ukr': ['stopword_ukr'],
            'urd': ['stopword_urd'],
            'vie': ['stopword_vie'],
            'yor': ['stopword_yor'],
            'zul': ['stopword_zul'],

            'other': []
        },

        'dependency_parsers': {
            'cat': ['spacy_cat'],
            'zho_cn': ['spacy_zho'],
            'zho_tw': ['spacy_zho'],
            'hrv': ['spacy_hrv'],
            'dan': ['spacy_dan'],
            'nld': ['spacy_nld'],
            'eng_gb': ['spacy_eng'],
            'eng_us': ['spacy_eng'],
            'fin': ['spacy_fin'],
            'fra': ['spacy_fra'],
            'deu_at': ['spacy_deu'],
            'deu_de': ['spacy_deu'],
            'deu_ch': ['spacy_deu'],
            'ell': ['spacy_ell'],
            'ita': ['spacy_ita'],
            'jpn': ['spacy_jpn'],
            'lit': ['spacy_lit'],
            'mkd': ['spacy_mkd'],
            'nob': ['spacy_nob'],
            'pol': ['spacy_pol'],
            'por_br': ['spacy_por'],
            'por_pt': ['spacy_por'],
            'ron': ['spacy_ron'],
            'rus': ['spacy_rus'],
            'spa': ['spacy_spa'],
            'swe': ['spacy_swe'],
            'ukr': ['spacy_ukr']
        },

        'measures_dispersion': {
            _tr('init_settings_global', 'None'): {
                'col_text': None,
                'func': None,
                'type': ''
            },

            _tr('init_settings_global', 'Average Logarithmic Distance'): {
                'col_text': _tr('init_settings_global', 'ALD'),
                'func': wl_measures_dispersion.ald,
                'type': 'dist_based'
            },

            _tr('init_settings_global', 'Average Reduced Frequency'): {
                'col_text': _tr('init_settings_global', 'ARF'),
                'func': wl_measures_dispersion.arf,
                'type': 'dist_based'
            },

            _tr('init_settings_global', 'Average Waiting Time'): {
                'col_text': _tr('init_settings_global', 'AWT'),
                'func': wl_measures_dispersion.awt,
                'type': 'dist_based'
            },

            _tr('init_settings_global', "Carroll's D₂"): {
                'col_text': _tr('init_settings_global', "Carroll's D₂"),
                'func': wl_measures_dispersion.carrolls_d2,
                'type': 'parts_based'
            },

            _tr('init_settings_global', "Gries's DP"): {
                'col_text': _tr('init_settings_global', "Gries's DP"),
                'func': wl_measures_dispersion.griess_dp,
                'type': 'parts_based'
            },

            _tr('init_settings_global', "Juilland's D"): {
                'col_text': _tr('init_settings_global', "Juilland's D"),
                'func': wl_measures_dispersion.juillands_d,
                'type': 'parts_based'
            },

            _tr('init_settings_global', "Lyne's D₃"): {
                'col_text': _tr('init_settings_global', "Lyne's D₃"),
                'func': wl_measures_dispersion.lynes_d3,
                'type': 'parts_based'
            },

            _tr('init_settings_global', "Rosengren's S"): {
                'col_text': _tr('init_settings_global', "Rosengren's S"),
                'func': wl_measures_dispersion.rosengrens_s,
                'type': 'parts_based'
            },

            _tr('init_settings_global', "Zhang's Distributional Consistency"): {
                'col_text': _tr('init_settings_global', "Zhang's DC"),
                'func': wl_measures_dispersion.zhangs_distributional_consistency,
                'type': 'parts_based'
            }
        },

        'measures_adjusted_freq': {
            _tr('init_settings_global', 'None'): {
                'col_text': None,
                'func': None,
                'type': ''
            },

            _tr('init_settings_global', 'Average Logarithmic Distance'): {
                'col_text': _tr('init_settings_global', 'f-ALD'),
                'func': wl_measures_adjusted_freq.fald,
                'type': 'dist_based'
            },

            _tr('init_settings_global', 'Average Reduced Frequency'): {
                'col_text': _tr('init_settings_global', 'f-ARF'),
                'func': wl_measures_adjusted_freq.farf,
                'type': 'dist_based'
            },

            _tr('init_settings_global', 'Average Waiting Time'): {
                'col_text': _tr('init_settings_global', 'f-AWT'),
                'func': wl_measures_adjusted_freq.fawt,
                'type': 'dist_based'
            },

            _tr('init_settings_global', "Carroll's Uₘ"): {
                'col_text': _tr('init_settings_global', "Carroll's Uₘ"),
                'func': wl_measures_adjusted_freq.carrolls_um,
                'type': 'parts_based'
            },

            _tr('init_settings_global', "Engwall's FM"): {
                'col_text': _tr('init_settings_global', "Engwall's FM"),
                'func': wl_measures_adjusted_freq.engwalls_fm,
                'type': 'parts_based'
            },

            _tr('init_settings_global', "Juilland's U"): {
                'col_text': _tr('init_settings_global', "Juilland's U"),
                'func': wl_measures_adjusted_freq.juillands_u,
                'type': 'parts_based'
            },

            _tr('init_settings_global', "Kromer's UR"): {
                'col_text': _tr('init_settings_global', "Kromer's UR"),
                'func': wl_measures_adjusted_freq.kromers_ur,
                'type': 'parts_based'
            },

            _tr('init_settings_global', "Rosengren's KF"): {
                'col_text': _tr('init_settings_global', "Rosengren's KF"),
                'func': wl_measures_adjusted_freq.rosengrens_kf,
                'type': 'parts_based'
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
