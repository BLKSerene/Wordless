# ----------------------------------------------------------------------
# Wordless: Settings - Global settings
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

from PyQt5.QtCore import QCoreApplication

from wordless.wl_measures import (
    wl_measures_adjusted_freq,
    wl_measures_bayes_factor,
    wl_measures_dispersion,
    wl_measures_effect_size,
    wl_measures_statistical_significance
)

_tr = QCoreApplication.translate

# Use function instead of constant to defer translation until QTranslator is initialized
def init_settings_global():
    SETTINGS_GLOBAL = {
        # Language names should be always capitalized
        'langs': {
            _tr('wl_settings_global', 'Afrikaans'): ['afr', 'af'],
            _tr('wl_settings_global', 'Albanian'): ['sqi', 'sq'],
            _tr('wl_settings_global', 'Amharic'): ['amh', 'am'],
            _tr('wl_settings_global', 'Arabic'): ['ara', 'ar'],
            _tr('wl_settings_global', 'Armenian (Classical)'): ['xcl', 'xcl'],
            _tr('wl_settings_global', 'Armenian (Eastern)'): ['hye', 'hy'],
            _tr('wl_settings_global', 'Armenian (Western)'): ['hyw', 'hyw'],
            _tr('wl_settings_global', 'Assamese'): ['asm', 'as'],
            _tr('wl_settings_global', 'Asturian'): ['ast', 'ast'],
            _tr('wl_settings_global', 'Azerbaijani'): ['aze', 'az'],
            _tr('wl_settings_global', 'Basque'): ['eus', 'eu'],
            _tr('wl_settings_global', 'Belarusian'): ['bel', 'be'],
            _tr('wl_settings_global', 'Bengali'): ['ben', 'bn'],
            _tr('wl_settings_global', 'Bulgarian'): ['bul', 'bg'],
            _tr('wl_settings_global', 'Burmese'): ['mya', 'my'],
            _tr('wl_settings_global', 'Buryat (Russia)'): ['bxr', 'bxr'],
            _tr('wl_settings_global', 'Catalan'): ['cat', 'ca'],
            _tr('wl_settings_global', 'Chinese (Classical)'): ['lzh', 'lzh'],
            _tr('wl_settings_global', 'Chinese (Simplified)'): ['zho_cn', 'zh_cn'],
            _tr('wl_settings_global', 'Chinese (Traditional)'): ['zho_tw', 'zh_tw'],
            _tr('wl_settings_global', 'Church Slavonic (Old)'): ['chu', 'cu'],
            _tr('wl_settings_global', 'Coptic'): ['cop', 'cop'],
            _tr('wl_settings_global', 'Croatian'): ['hrv', 'hr'],
            _tr('wl_settings_global', 'Czech'): ['ces', 'cs'],
            _tr('wl_settings_global', 'Danish'): ['dan', 'da'],
            _tr('wl_settings_global', 'Dutch'): ['nld', 'nl'],
            _tr('wl_settings_global', 'English (Middle)'): ['enm', 'enm'],
            _tr('wl_settings_global', 'English (Old)'): ['ang', 'ang'],
            _tr('wl_settings_global', 'English (United Kingdom)'): ['eng_gb', 'en_gb'],
            _tr('wl_settings_global', 'English (United States)'): ['eng_us', 'en_us'],
            _tr('wl_settings_global', 'Erzya'): ['myv', 'myv'],
            _tr('wl_settings_global', 'Esperanto'): ['epo', 'eo'],
            _tr('wl_settings_global', 'Estonian'): ['est', 'et'],
            _tr('wl_settings_global', 'Faroese'): ['fao', 'fo'],
            _tr('wl_settings_global', 'Finnish'): ['fin', 'fi'],
            _tr('wl_settings_global', 'French'): ['fra', 'fr'],
            _tr('wl_settings_global', 'French (Old)'): ['fro', 'fro'],
            _tr('wl_settings_global', 'Galician'): ['glg', 'gl'],
            _tr('wl_settings_global', 'Georgian'): ['kat', 'ka'],
            _tr('wl_settings_global', 'German (Austria)'): ['deu_at', 'de_at'],
            _tr('wl_settings_global', 'German (Germany)'): ['deu_de', 'de_de'],
            _tr('wl_settings_global', 'German (Switzerland)'): ['deu_ch', 'de_ch'],
            _tr('wl_settings_global', 'Gothic'): ['got', 'got'],
            _tr('wl_settings_global', 'Greek (Ancient)'): ['grc', 'grc'],
            _tr('wl_settings_global', 'Greek (Modern)'): ['ell', 'el'],
            _tr('wl_settings_global', 'Gujarati'): ['guj', 'gu'],
            _tr('wl_settings_global', 'Hebrew (Ancient)'): ['hbo', 'hbo'],
            _tr('wl_settings_global', 'Hebrew (Modern)'): ['heb', 'he'],
            _tr('wl_settings_global', 'Hindi'): ['hin', 'hi'],
            _tr('wl_settings_global', 'Hungarian'): ['hun', 'hu'],
            _tr('wl_settings_global', 'Icelandic'): ['isl', 'is'],
            _tr('wl_settings_global', 'Indonesian'): ['ind', 'id'],
            _tr('wl_settings_global', 'Irish'): ['gle', 'ga'],
            _tr('wl_settings_global', 'Italian'): ['ita', 'it'],
            _tr('wl_settings_global', 'Japanese'): ['jpn', 'ja'],
            _tr('wl_settings_global', 'Kannada'): ['kan', 'kn'],
            _tr('wl_settings_global', 'Kazakh'): ['kaz', 'kk'],
            _tr('wl_settings_global', 'Khmer'): ['khm', 'km'],
            _tr('wl_settings_global', 'Korean'): ['kor', 'ko'],
            _tr('wl_settings_global', 'Kurdish (Kurmanji)'): ['kmr', 'kmr'],
            _tr('wl_settings_global', 'Kyrgyz'): ['kir', 'ky'],
            _tr('wl_settings_global', 'Lao'): ['lao', 'lo'],
            _tr('wl_settings_global', 'Latin'): ['lat', 'la'],
            _tr('wl_settings_global', 'Latvian'): ['lav', 'lv'],
            _tr('wl_settings_global', 'Ligurian'): ['lij', 'lij'],
            _tr('wl_settings_global', 'Lithuanian'): ['lit', 'lt'],
            _tr('wl_settings_global', 'Luganda'): ['lug', 'lg'],
            _tr('wl_settings_global', 'Luxembourgish'): ['ltz', 'lb'],
            _tr('wl_settings_global', 'Macedonian'): ['mkd', 'mk'],
            _tr('wl_settings_global', 'Malay'): ['msa', 'ms'],
            _tr('wl_settings_global', 'Malayalam'): ['mal', 'ml'],
            _tr('wl_settings_global', 'Maltese'): ['mlt', 'mt'],
            _tr('wl_settings_global', 'Manx'): ['glv', 'gv'],
            _tr('wl_settings_global', 'Marathi'): ['mar', 'mr'],
            _tr('wl_settings_global', 'Meitei (Meitei script)'): ['mni_mtei', 'mni_mtei'],
            _tr('wl_settings_global', 'Mongolian'): ['mon', 'mn'],
            _tr('wl_settings_global', 'Nepali'): ['nep', 'ne'],
            _tr('wl_settings_global', 'Nigerian Pidgin'): ['pcm', 'pcm'],
            _tr('wl_settings_global', 'Norwegian (Bokmål)'): ['nob', 'nb'],
            _tr('wl_settings_global', 'Norwegian (Nynorsk)'): ['nno', 'nn'],
            _tr('wl_settings_global', 'Odia'): ['ori', 'or'],
            _tr('wl_settings_global', 'Persian'): ['fas', 'fa'],
            _tr('wl_settings_global', 'Polish'): ['pol', 'pl'],
            _tr('wl_settings_global', 'Pomak'): ['qpm', 'qpm'],
            _tr('wl_settings_global', 'Portuguese (Brazil)'): ['por_br', 'pt_br'],
            _tr('wl_settings_global', 'Portuguese (Portugal)'): ['por_pt', 'pt_pt'],
            _tr('wl_settings_global', 'Punjabi (Gurmukhi script)'): ['pan_guru', 'pa_guru'],
            _tr('wl_settings_global', 'Romanian'): ['ron', 'ro'],
            _tr('wl_settings_global', 'Russian'): ['rus', 'ru'],
            _tr('wl_settings_global', 'Russian (Old)'): ['orv', 'orv'],
            _tr('wl_settings_global', 'Sámi (Northern)'): ['sme', 'se'],
            _tr('wl_settings_global', 'Sanskrit'): ['san', 'sa'],
            _tr('wl_settings_global', 'Scottish Gaelic'): ['gla', 'gd'],
            _tr('wl_settings_global', 'Serbian (Cyrillic script)'): ['srp_cyrl', 'sr_cyrl'],
            _tr('wl_settings_global', 'Serbian (Latin script)'): ['srp_latn', 'sr_latn'],
            _tr('wl_settings_global', 'Sindhi'): ['snd', 'sd'],
            _tr('wl_settings_global', 'Sinhala'): ['sin', 'si'],
            _tr('wl_settings_global', 'Slovak'): ['slk', 'sk'],
            _tr('wl_settings_global', 'Slovene'): ['slv', 'sl'],
            _tr('wl_settings_global', 'Sorbian (Lower)'): ['dsb', 'dsb'],
            _tr('wl_settings_global', 'Sorbian (Upper)'): ['hsb', 'hsb'],
            _tr('wl_settings_global', 'Spanish'): ['spa', 'es'],
            _tr('wl_settings_global', 'Swahili'): ['swa', 'sw'],
            _tr('wl_settings_global', 'Swedish'): ['swe', 'sv'],
            _tr('wl_settings_global', 'Tagalog'): ['tgl', 'tl'],
            _tr('wl_settings_global', 'Tajik'): ['tgk', 'tg'],
            _tr('wl_settings_global', 'Tamil'): ['tam', 'ta'],
            _tr('wl_settings_global', 'Tatar'): ['tat', 'tt'],
            _tr('wl_settings_global', 'Telugu'): ['tel', 'te'],
            _tr('wl_settings_global', 'Tetun (Dili)'): ['tdt', 'tdt'],
            _tr('wl_settings_global', 'Thai'): ['tha', 'th'],
            _tr('wl_settings_global', 'Tibetan'): ['bod', 'bo'],
            _tr('wl_settings_global', 'Tigrinya'): ['tir', 'ti'],
            _tr('wl_settings_global', 'Tswana'): ['tsn', 'tn'],
            _tr('wl_settings_global', 'Turkish'): ['tur', 'tr'],
            _tr('wl_settings_global', 'Ukrainian'): ['ukr', 'uk'],
            _tr('wl_settings_global', 'Urdu'): ['urd', 'ur'],
            _tr('wl_settings_global', 'Uyghur'): ['uig', 'ug'],
            _tr('wl_settings_global', 'Vietnamese'): ['vie', 'vi'],
            _tr('wl_settings_global', 'Welsh'): ['cym', 'cy'],
            _tr('wl_settings_global', 'Wolof'): ['wol', 'wo'],
            _tr('wl_settings_global', 'Yoruba'): ['yor', 'yo'],
            _tr('wl_settings_global', 'Zulu'): ['zul', 'zu'],

            _tr('wl_settings_global', 'Other languages'): ['other', 'other']
        },

        # Language and geographical names should be always capitalized
        # Case of encoding names are preserved
        'encodings': {
            _tr('wl_settings_global', 'All languages (UTF-8 without BOM)'): 'utf_8',
            _tr('wl_settings_global', 'All languages (UTF-8 with BOM)'): 'utf_8_sig',
            _tr('wl_settings_global', 'All languages (UTF-16 with BOM)'): 'utf_16',
            _tr('wl_settings_global', 'All languages (UTF-16BE without BOM)'): 'utf_16_be',
            _tr('wl_settings_global', 'All languages (UTF-16LE without BOM)'): 'utf_16_le',
            _tr('wl_settings_global', 'All languages (UTF-32 with BOM)'): 'utf_32',
            _tr('wl_settings_global', 'All languages (UTF-32BE without BOM)'): 'utf_32_be',
            _tr('wl_settings_global', 'All languages (UTF-32LE without BOM)'): 'utf_32_le',
            _tr('wl_settings_global', 'All languages (UTF-7)'): 'utf_7',

            _tr('wl_settings_global', 'Arabic (CP720)'): 'cp720',
            _tr('wl_settings_global', 'Arabic (CP864)'): 'cp864',
            _tr('wl_settings_global', 'Arabic (ISO-8859-6)'): 'iso8859_6',
            _tr('wl_settings_global', 'Arabic (Mac OS Arabic)'): 'mac_arabic',
            _tr('wl_settings_global', 'Arabic (Windows-1256)'): 'cp1256',

            _tr('wl_settings_global', 'Baltic languages (CP775)'): 'cp775',
            _tr('wl_settings_global', 'Baltic languages (ISO-8859-13)'): 'iso8859_13',
            _tr('wl_settings_global', 'Baltic languages (Windows-1257)'): 'cp1257',

            _tr('wl_settings_global', 'Celtic languages (ISO-8859-14)'): 'iso8859_14',

            _tr('wl_settings_global', 'Chinese (GB18030)'): 'gb18030',
            _tr('wl_settings_global', 'Chinese (GBK)'): 'gbk',

            _tr('wl_settings_global', 'Chinese (Simplified) (GB2312)'): 'gb2312',
            _tr('wl_settings_global', 'Chinese (Simplified) (HZ)'): 'hz',

            _tr('wl_settings_global', 'Chinese (Traditional) (Big-5)'): 'big5',
            _tr('wl_settings_global', 'Chinese (Traditional) (Big5-HKSCS)'): 'big5hkscs',
            _tr('wl_settings_global', 'Chinese (Traditional) (CP950)'): 'cp950',

            _tr('wl_settings_global', 'Croatian (Mac OS Croatian)'): 'mac_croatian',

            _tr('wl_settings_global', 'Cyrillic (CP855)'): 'cp855',
            _tr('wl_settings_global', 'Cyrillic (CP866)'): 'cp866',
            _tr('wl_settings_global', 'Cyrillic (ISO-8859-5)'): 'iso8859_5',
            _tr('wl_settings_global', 'Cyrillic (Mac OS Cyrillic)'): 'mac_cyrillic',
            _tr('wl_settings_global', 'Cyrillic (Windows-1251)'): 'cp1251',

            _tr('wl_settings_global', 'English (ASCII)'): 'ascii',
            _tr('wl_settings_global', 'English (EBCDIC 037)'): 'cp037',
            _tr('wl_settings_global', 'English (CP437)'): 'cp437',

            _tr('wl_settings_global', 'European (HP Roman-8)'): 'hp_roman8',

            _tr('wl_settings_global', 'European (Central) (CP852)'): 'cp852',
            _tr('wl_settings_global', 'European (Central) (ISO-8859-2)'): 'iso8859_2',
            _tr('wl_settings_global', 'European (Central) (Mac OS Central European)'): 'mac_latin2',
            _tr('wl_settings_global', 'European (Central) (Windows-1250)'): 'cp1250',

            _tr('wl_settings_global', 'European (Northern) (ISO-8859-4)'): 'iso8859_4',

            _tr('wl_settings_global', 'European (Southern) (ISO-8859-3)'): 'iso8859_3',

            _tr('wl_settings_global', 'European (Southeastern) (ISO-8859-16)'): 'iso8859_16',

            _tr('wl_settings_global', 'European (Western) (EBCDIC 500)'): 'cp500',
            _tr('wl_settings_global', 'European (Western) (CP850)'): 'cp850',
            _tr('wl_settings_global', 'European (Western) (CP858)'): 'cp858',
            _tr('wl_settings_global', 'European (Western) (CP1140)'): 'cp1140',
            _tr('wl_settings_global', 'European (Western) (ISO-8859-1)'): 'latin_1',
            _tr('wl_settings_global', 'European (Western) (ISO-8859-15)'): 'iso8859_15',
            _tr('wl_settings_global', 'European (Western) (Mac OS Roman)'): 'mac_roman',
            _tr('wl_settings_global', 'European (Western) (Windows-1252)'): 'cp1252',

            _tr('wl_settings_global', 'French (CP863)'): 'cp863',

            _tr('wl_settings_global', 'German (EBCDIC 273)'): 'cp273',

            _tr('wl_settings_global', 'Greek (CP737)'): 'cp737',
            _tr('wl_settings_global', 'Greek (CP869)'): 'cp869',
            _tr('wl_settings_global', 'Greek (CP875)'): 'cp875',
            _tr('wl_settings_global', 'Greek (ISO-8859-7)'): 'iso8859_7',
            _tr('wl_settings_global', 'Greek (Mac OS Greek)'): 'mac_greek',
            _tr('wl_settings_global', 'Greek (Windows-1253)'): 'cp1253',

            _tr('wl_settings_global', 'Hebrew (CP856)'): 'cp856',
            _tr('wl_settings_global', 'Hebrew (CP862)'): 'cp862',
            _tr('wl_settings_global', 'Hebrew (EBCDIC 424)'): 'cp424',
            _tr('wl_settings_global', 'Hebrew (ISO-8859-8)'): 'iso8859_8',
            _tr('wl_settings_global', 'Hebrew (Windows-1255)'): 'cp1255',

            _tr('wl_settings_global', 'Icelandic (CP861)'): 'cp861',
            _tr('wl_settings_global', 'Icelandic (Mac OS Icelandic)'): 'mac_iceland',

            _tr('wl_settings_global', 'Japanese (CP932)'): 'cp932',
            _tr('wl_settings_global', 'Japanese (EUC-JP)'): 'euc_jp',
            _tr('wl_settings_global', 'Japanese (EUC-JIS-2004)'): 'euc_jis_2004',
            _tr('wl_settings_global', 'Japanese (EUC-JISx0213)'): 'euc_jisx0213',
            _tr('wl_settings_global', 'Japanese (ISO-2022-JP)'): 'iso2022_jp',
            _tr('wl_settings_global', 'Japanese (ISO-2022-JP-1)'): 'iso2022_jp_1',
            _tr('wl_settings_global', 'Japanese (ISO-2022-JP-2)'): 'iso2022_jp_2',
            _tr('wl_settings_global', 'Japanese (ISO-2022-JP-2004)'): 'iso2022_jp_2004',
            _tr('wl_settings_global', 'Japanese (ISO-2022-JP-3)'): 'iso2022_jp_3',
            _tr('wl_settings_global', 'Japanese (ISO-2022-JP-EXT)'): 'iso2022_jp_ext',
            _tr('wl_settings_global', 'Japanese (Shift_JIS)'): 'shift_jis',
            _tr('wl_settings_global', 'Japanese (Shift_JIS-2004)'): 'shift_jis_2004',
            _tr('wl_settings_global', 'Japanese (Shift_JISx0213)'): 'shift_jisx0213',

            _tr('wl_settings_global', 'Kazakh (KZ-1048)'): 'kz1048',
            _tr('wl_settings_global', 'Kazakh (PTCP154)'): 'ptcp154',

            _tr('wl_settings_global', 'Korean (EUC-KR)'): 'euc_kr',
            _tr('wl_settings_global', 'Korean (ISO-2022-KR)'): 'iso2022_kr',
            _tr('wl_settings_global', 'Korean (JOHAB)'): 'johab',
            _tr('wl_settings_global', 'Korean (UHC)'): 'cp949',

            _tr('wl_settings_global', 'Nordic languages (CP865)'): 'cp865',
            _tr('wl_settings_global', 'Nordic languages (ISO-8859-10)'): 'iso8859_10',

            _tr('wl_settings_global', 'Persian/Urdu (Mac OS Farsi)'): 'mac_farsi',

            _tr('wl_settings_global', 'Portuguese (CP860)'): 'cp860',

            _tr('wl_settings_global', 'Romanian (Mac OS Romanian)'): 'mac_romanian',

            _tr('wl_settings_global', 'Russian (KOI8-R)'): 'koi8_r',

            _tr('wl_settings_global', 'Tajik (KOI8-T)'): 'koi8_t',

            _tr('wl_settings_global', 'Thai (CP874)'): 'cp874',
            _tr('wl_settings_global', 'Thai (ISO-8859-11)'): 'iso8859_11',
            _tr('wl_settings_global', 'Thai (TIS-620)'): 'tis_620',

            _tr('wl_settings_global', 'Turkish (CP857)'): 'cp857',
            _tr('wl_settings_global', 'Turkish (EBCDIC 1026)'): 'cp1026',
            _tr('wl_settings_global', 'Turkish (ISO-8859-9)'): 'iso8859_9',
            _tr('wl_settings_global', 'Turkish (Mac OS Turkish)'): 'mac_turkish',
            _tr('wl_settings_global', 'Turkish (Windows-1254)'): 'cp1254',

            _tr('wl_settings_global', 'Ukrainian (CP1125)'): 'cp1125',
            _tr('wl_settings_global', 'Ukrainian (KOI8-U)'): 'koi8_u',

            _tr('wl_settings_global', 'Urdu (CP1006)'): 'cp1006',

            _tr('wl_settings_global', 'Vietnamese (CP1258)'): 'cp1258',
        },

        # Names of file types are always pluralized but not capitalized
        'file_types': {
            'files': [
                _tr('wl_settings_global', 'CSV files (*.csv)'),
                _tr('wl_settings_global', 'Excel workbooks (*.xlsx)'),
                _tr('wl_settings_global', 'HTML pages (*.htm; *.html)'),
                _tr('wl_settings_global', 'Lyrics files (*.lrc)'),
                _tr('wl_settings_global', 'PDF files (*.pdf)'),
                _tr('wl_settings_global', 'PowerPoint presentations (*.pptx)'),
                _tr('wl_settings_global', 'Text files (*.txt)'),
                _tr('wl_settings_global', 'Translation memory files (*.tmx)'),
                _tr('wl_settings_global', 'Word documents (*.docx)'),
                _tr('wl_settings_global', 'XML files (*.xml)'),
                _tr('wl_settings_global', 'All files (*.*)')
            ],

            'exp_tables': [
                _tr('wl_settings_global', 'CSV files (*.csv)'),
                _tr('wl_settings_global', 'Excel workbooks (*.xlsx)')
            ],
            'exp_tables_concordancer': [
                _tr('wl_settings_global', 'CSV files (*.csv)'),
                _tr('wl_settings_global', 'Excel workbooks (*.xlsx)'),
                _tr('wl_settings_global', 'Word documents (*.docx)')
            ],
            'exp_tables_concordancer_zapping': [
                _tr('wl_settings_global', 'Word documents (*.docx)')
            ],

            'fonts': [
                _tr('wl_settings_global', 'OpenType fonts (*.otf)'),
                _tr('wl_settings_global', 'TrueType fonts (*.ttf)'),
                _tr('wl_settings_global', 'All files (*.*)')
            ],

            # All image formats supported by Pillow
            # Reference: https://stackoverflow.com/questions/71112986/retrieve-a-list-of-supported-read-file-extensions-formats
            'masks': [
                _tr('wl_settings_global', 'Blizzard mipmap format (*.blp)'),
                _tr('wl_settings_global', 'Windows bitmaps (*.bmp)'),
                _tr('wl_settings_global', 'Window cursor files (*.cur)'),
                _tr('wl_settings_global', 'Multi-page PCX files (*.dcx)'),
                _tr('wl_settings_global', 'DirectDraw surface (*.dds)'),
                _tr('wl_settings_global', 'Device-independent bitmaps (*.dib)'),
                _tr('wl_settings_global', 'Encapsulated PostScript (*.eps, *.ps)'),
                _tr('wl_settings_global', 'Flexible image transport system (*.fit, *.fits)'),
                _tr('wl_settings_global', 'Autodesk animation files (*.flc, *.fli)'),
                _tr('wl_settings_global', 'Fox Engine textures (*.ftex)'),
                _tr('wl_settings_global', 'GIMP brush files (*.gbr)'),
                _tr('wl_settings_global', 'Graphics interchange format (*.gif)'),
                _tr('wl_settings_global', 'Apple icon images (*.icns)'),
                _tr('wl_settings_global', 'Windows icon files (*.ico)'),
                _tr('wl_settings_global', 'IPTC/NAA newsphoto files (*.iim)'),
                _tr('wl_settings_global', 'IM files (*.im)'),
                _tr('wl_settings_global', 'Image Tools image files (*)'),
                _tr('wl_settings_global', 'JPEG files (*.jfif, *.jpe, *.jpeg, *.jpg)'),
                _tr('wl_settings_global', 'JPEG 2000 files (*.j2c, *.j2k, *.jp2, *.jpc, *.jpf, *.jpx)'),
                _tr('wl_settings_global', 'McIDAS area files (*)'),
                _tr('wl_settings_global', 'Microsoft Paint files (*.msp)'),
                _tr('wl_settings_global', 'PhotoCD files (*.pcd)'),
                _tr('wl_settings_global', 'Picture exchange (*.pcx)'),
                _tr('wl_settings_global', 'PIXAR raster files (*.pxr)'),
                _tr('wl_settings_global', 'Portable network graphics (*.apng, *.png)'),
                _tr('wl_settings_global', 'Portable pixmap format (*.pbm, *.pgm, *.pnm, *.ppm)'),
                _tr('wl_settings_global', 'Photoshop PSD files (*.psd)'),
                _tr('wl_settings_global', 'Sun raster files (*.ras)'),
                _tr('wl_settings_global', 'Silicon graphics images (*.bw, *.rgb, *.rgba, *.sgi)'),
                _tr('wl_settings_global', 'SPIDER files (*)'),
                _tr('wl_settings_global', 'Truevision TGA (*.icb, *.tga, *.vda, *.vst)'),
                _tr('wl_settings_global', 'TIFF files (*.tif, *.tiff)'),
                _tr('wl_settings_global', 'WebP files (*.webp)'),
                _tr('wl_settings_global', 'Windows metafiles (*.emf, *.wmf)'),
                _tr('wl_settings_global', 'X bitmaps (*.xbm)'),
                _tr('wl_settings_global', 'X pixmaps (*.xpm)'),
                _tr('wl_settings_global', 'XV thumbnails (*)'),
                _tr('wl_settings_global', 'All files (*.*)')
            ],
        },

        # Only language names and proper nouns are capitalized in names of language utilities
        'mapping_lang_utils': {
            'sentence_tokenizers': {
                _tr('wl_settings_global', 'botok - Tibetan sentence tokenizer'): 'botok_bod',
                _tr('wl_settings_global', 'khmer-nltk - Khmer sentence tokenizer'): 'khmer_nltk_khm',
                _tr('wl_settings_global', 'LaoNLP - Lao sentence tokenizer'): 'laonlp_lao',

                _tr('wl_settings_global', 'NLTK - Czech Punkt sentence tokenizer'): 'nltk_punkt_ces',
                _tr('wl_settings_global', 'NLTK - Danish Punkt sentence tokenizer'): 'nltk_punkt_dan',
                _tr('wl_settings_global', 'NLTK - Dutch Punkt sentence tokenizer'): 'nltk_punkt_nld',
                _tr('wl_settings_global', 'NLTK - English Punkt sentence tokenizer'): 'nltk_punkt_eng',
                _tr('wl_settings_global', 'NLTK - Estonian Punkt sentence tokenizer'): 'nltk_punkt_est',
                _tr('wl_settings_global', 'NLTK - Finnish Punkt sentence tokenizer'): 'nltk_punkt_fin',
                _tr('wl_settings_global', 'NLTK - French Punkt sentence tokenizer'): 'nltk_punkt_fra',
                _tr('wl_settings_global', 'NLTK - German Punkt sentence tokenizer'): 'nltk_punkt_deu',
                _tr('wl_settings_global', 'NLTK - Greek Punkt sentence tokenizer'): 'nltk_punkt_ell',
                _tr('wl_settings_global', 'NLTK - Italian Punkt sentence tokenizer'): 'nltk_punkt_ita',
                _tr('wl_settings_global', 'NLTK - Norwegian (Bokmål) Punkt sentence tokenizer'): 'nltk_punkt_nob',
                _tr('wl_settings_global', 'NLTK - Polish Punkt sentence tokenizer'): 'nltk_punkt_pol',
                _tr('wl_settings_global', 'NLTK - Portuguese Punkt sentence tokenizer'): 'nltk_punkt_por',
                _tr('wl_settings_global', 'NLTK - Russian Punkt sentence tokenizer'): 'nltk_punkt_rus',
                _tr('wl_settings_global', 'NLTK - Slovene Punkt sentence tokenizer'): 'nltk_punkt_slv',
                _tr('wl_settings_global', 'NLTK - Spanish Punkt sentence tokenizer'): 'nltk_punkt_spa',
                _tr('wl_settings_global', 'NLTK - Swedish Punkt sentence tokenizer'): 'nltk_punkt_swe',
                _tr('wl_settings_global', 'NLTK - Turkish Punkt sentence tokenizer'): 'nltk_punkt_tur',

                'PyThaiNLP - CRFCut': 'pythainlp_crfcut',
                'PyThaiNLP - ThaiSumCut': 'pythainlp_thaisumcut',

                _tr('wl_settings_global', 'spaCy - Catalan dependency parser'): 'spacy_dependency_parser_cat',
                _tr('wl_settings_global', 'spaCy - Chinese dependency parser'): 'spacy_dependency_parser_zho',
                _tr('wl_settings_global', 'spaCy - Croatian dependency parser'): 'spacy_dependency_parser_hrv',
                _tr('wl_settings_global', 'spaCy - Danish dependency parser'): 'spacy_dependency_parser_dan',
                _tr('wl_settings_global', 'spaCy - Dutch dependency parser'): 'spacy_dependency_parser_nld',
                _tr('wl_settings_global', 'spaCy - English dependency parser'): 'spacy_dependency_parser_eng',
                _tr('wl_settings_global', 'spaCy - Finnish dependency parser'): 'spacy_dependency_parser_fin',
                _tr('wl_settings_global', 'spaCy - French dependency parser'): 'spacy_dependency_parser_fra',
                _tr('wl_settings_global', 'spaCy - German dependency parser'): 'spacy_dependency_parser_deu',
                _tr('wl_settings_global', 'spaCy - Greek (Modern) dependency parser'): 'spacy_dependency_parser_ell',
                _tr('wl_settings_global', 'spaCy - Italian dependency parser'): 'spacy_dependency_parser_ita',
                _tr('wl_settings_global', 'spaCy - Japanese dependency parser'): 'spacy_dependency_parser_jpn',
                _tr('wl_settings_global', 'spaCy - Korean dependency parser'): 'spacy_dependency_parser_kor',
                _tr('wl_settings_global', 'spaCy - Lithuanian dependency parser'): 'spacy_dependency_parser_lit',
                _tr('wl_settings_global', 'spaCy - Macedonian dependency parser'): 'spacy_dependency_parser_mkd',
                _tr('wl_settings_global', 'spaCy - Norwegian (Bokmål) dependency parser'): 'spacy_dependency_parser_nob',
                _tr('wl_settings_global', 'spaCy - Polish dependency parser'): 'spacy_dependency_parser_pol',
                _tr('wl_settings_global', 'spaCy - Portuguese dependency parser'): 'spacy_dependency_parser_por',
                _tr('wl_settings_global', 'spaCy - Romanian dependency parser'): 'spacy_dependency_parser_ron',
                _tr('wl_settings_global', 'spaCy - Russian dependency parser'): 'spacy_dependency_parser_rus',
                _tr('wl_settings_global', 'spaCy - Slovene dependency parser'): 'spacy_dependency_parser_slv',
                _tr('wl_settings_global', 'spaCy - Spanish dependency parser'): 'spacy_dependency_parser_spa',
                _tr('wl_settings_global', 'spaCy - Swedish dependency parser'): 'spacy_dependency_parser_swe',
                _tr('wl_settings_global', 'spaCy - Ukrainian dependency parser'): 'spacy_dependency_parser_ukr',

                _tr('wl_settings_global', 'spaCy - Croatian sentence recognizer'): 'spacy_sentence_recognizer_hrv',
                _tr('wl_settings_global', 'spaCy - Dutch sentence recognizer'): 'spacy_sentence_recognizer_nld',
                _tr('wl_settings_global', 'spaCy - Finnish sentence recognizer'): 'spacy_sentence_recognizer_fin',
                _tr('wl_settings_global', 'spaCy - Greek (Modern) sentence recognizer'): 'spacy_sentence_recognizer_ell',
                _tr('wl_settings_global', 'spaCy - Italian sentence recognizer'): 'spacy_sentence_recognizer_ita',
                _tr('wl_settings_global', 'spaCy - Korean sentence recognizer'): 'spacy_sentence_recognizer_kor',
                _tr('wl_settings_global', 'spaCy - Lithuanian sentence recognizer'): 'spacy_sentence_recognizer_lit',
                _tr('wl_settings_global', 'spaCy - Macedonian sentence recognizer'): 'spacy_sentence_recognizer_mkd',
                _tr('wl_settings_global', 'spaCy - Norwegian (Bokmål) sentence recognizer'): 'spacy_sentence_recognizer_nob',
                _tr('wl_settings_global', 'spaCy - Polish sentence recognizer'): 'spacy_sentence_recognizer_pol',
                _tr('wl_settings_global', 'spaCy - Portuguese sentence recognizer'): 'spacy_sentence_recognizer_por',
                _tr('wl_settings_global', 'spaCy - Romanian sentence recognizer'): 'spacy_sentence_recognizer_ron',
                _tr('wl_settings_global', 'spaCy - Russian sentence recognizer'): 'spacy_sentence_recognizer_rus',
                _tr('wl_settings_global', 'spaCy - Swedish sentence recognizer'): 'spacy_sentence_recognizer_swe',

                _tr('wl_settings_global', 'spaCy - Sentencizer'): 'spacy_sentencizer',

                _tr('wl_settings_global', 'Stanza - Afrikaans sentence tokenizer'): 'stanza_afr',
                _tr('wl_settings_global', 'Stanza - Arabic sentence tokenizer'): 'stanza_ara',
                _tr('wl_settings_global', 'Stanza - Armenian (Classical) sentence tokenizer'): 'stanza_xcl',
                _tr('wl_settings_global', 'Stanza - Armenian (Eastern) sentence tokenizer'): 'stanza_hye',
                _tr('wl_settings_global', 'Stanza - Armenian (Western) sentence tokenizer'): 'stanza_hyw',
                _tr('wl_settings_global', 'Stanza - Basque sentence tokenizer'): 'stanza_eus',
                _tr('wl_settings_global', 'Stanza - Belarusian sentence tokenizer'): 'stanza_bel',
                _tr('wl_settings_global', 'Stanza - Bulgarian sentence tokenizer'): 'stanza_bul',
                _tr('wl_settings_global', 'Stanza - Burmese sentence tokenizer'): 'stanza_mya',
                _tr('wl_settings_global', 'Stanza - Buryat (Russia) sentence tokenizer'): 'stanza_bxr',
                _tr('wl_settings_global', 'Stanza - Catalan sentence tokenizer'): 'stanza_cat',
                _tr('wl_settings_global', 'Stanza - Chinese (Classical) sentence tokenizer'): 'stanza_lzh',
                _tr('wl_settings_global', 'Stanza - Chinese (Simplified) sentence tokenizer'): 'stanza_zho_cn',
                _tr('wl_settings_global', 'Stanza - Chinese (Traditional) sentence tokenizer'): 'stanza_zho_tw',
                _tr('wl_settings_global', 'Stanza - Church Slavonic (Old) sentence tokenizer'): 'stanza_chu',
                _tr('wl_settings_global', 'Stanza - Coptic sentence tokenizer'): 'stanza_cop',
                _tr('wl_settings_global', 'Stanza - Croatian sentence tokenizer'): 'stanza_hrv',
                _tr('wl_settings_global', 'Stanza - Czech sentence tokenizer'): 'stanza_ces',
                _tr('wl_settings_global', 'Stanza - Danish sentence tokenizer'): 'stanza_dan',
                _tr('wl_settings_global', 'Stanza - Dutch sentence tokenizer'): 'stanza_nld',
                _tr('wl_settings_global', 'Stanza - English sentence tokenizer'): 'stanza_eng',
                _tr('wl_settings_global', 'Stanza - English (Old) sentence tokenizer'): 'stanza_ang',
                _tr('wl_settings_global', 'Stanza - Erzya sentence tokenizer'): 'stanza_myv',
                _tr('wl_settings_global', 'Stanza - Estonian sentence tokenizer'): 'stanza_est',
                _tr('wl_settings_global', 'Stanza - Faroese sentence tokenizer'): 'stanza_fao',
                _tr('wl_settings_global', 'Stanza - Finnish sentence tokenizer'): 'stanza_fin',
                _tr('wl_settings_global', 'Stanza - French sentence tokenizer'): 'stanza_fra',
                _tr('wl_settings_global', 'Stanza - French (Old) sentence tokenizer'): 'stanza_fro',
                _tr('wl_settings_global', 'Stanza - Galician sentence tokenizer'): 'stanza_glg',
                _tr('wl_settings_global', 'Stanza - German sentence tokenizer'): 'stanza_deu',
                _tr('wl_settings_global', 'Stanza - Gothic sentence tokenizer'): 'stanza_got',
                _tr('wl_settings_global', 'Stanza - Greek (Ancient) sentence tokenizer'): 'stanza_grc',
                _tr('wl_settings_global', 'Stanza - Greek (Modern) sentence tokenizer'): 'stanza_ell',
                _tr('wl_settings_global', 'Stanza - Hebrew (Ancient) sentence tokenizer'): 'stanza_hbo',
                _tr('wl_settings_global', 'Stanza - Hebrew (Modern) sentence tokenizer'): 'stanza_heb',
                _tr('wl_settings_global', 'Stanza - Hindi sentence tokenizer'): 'stanza_hin',
                _tr('wl_settings_global', 'Stanza - Hungarian sentence tokenizer'): 'stanza_hun',
                _tr('wl_settings_global', 'Stanza - Icelandic sentence tokenizer'): 'stanza_isl',
                _tr('wl_settings_global', 'Stanza - Indonesian sentence tokenizer'): 'stanza_ind',
                _tr('wl_settings_global', 'Stanza - Irish sentence tokenizer'): 'stanza_gle',
                _tr('wl_settings_global', 'Stanza - Italian sentence tokenizer'): 'stanza_ita',
                _tr('wl_settings_global', 'Stanza - Japanese sentence tokenizer'): 'stanza_jpn',
                _tr('wl_settings_global', 'Stanza - Kazakh sentence tokenizer'): 'stanza_kaz',
                _tr('wl_settings_global', 'Stanza - Korean sentence tokenizer'): 'stanza_kor',
                _tr('wl_settings_global', 'Stanza - Kurdish (Kurmanji) sentence tokenizer'): 'stanza_kmr',
                _tr('wl_settings_global', 'Stanza - Kyrgyz sentence tokenizer'): 'stanza_kir',
                _tr('wl_settings_global', 'Stanza - Latin sentence tokenizer'): 'stanza_lat',
                _tr('wl_settings_global', 'Stanza - Latvian sentence tokenizer'): 'stanza_lav',
                _tr('wl_settings_global', 'Stanza - Ligurian sentence tokenizer'): 'stanza_lij',
                _tr('wl_settings_global', 'Stanza - Lithuanian sentence tokenizer'): 'stanza_lit',
                _tr('wl_settings_global', 'Stanza - Maltese sentence tokenizer'): 'stanza_mlt',
                _tr('wl_settings_global', 'Stanza - Manx sentence tokenizer'): 'stanza_glv',
                _tr('wl_settings_global', 'Stanza - Marathi sentence tokenizer'): 'stanza_mar',
                _tr('wl_settings_global', 'Stanza - Nigerian Pidgin sentence tokenizer'): 'stanza_pcm',
                _tr('wl_settings_global', 'Stanza - Norwegian (Bokmål) sentence tokenizer'): 'stanza_nob',
                _tr('wl_settings_global', 'Stanza - Norwegian (Nynorsk) sentence tokenizer'): 'stanza_nno',
                _tr('wl_settings_global', 'Stanza - Persian sentence tokenizer'): 'stanza_fas',
                _tr('wl_settings_global', 'Stanza - Polish sentence tokenizer'): 'stanza_pol',
                _tr('wl_settings_global', 'Stanza - Pomak sentence tokenizer'): 'stanza_qpm',
                _tr('wl_settings_global', 'Stanza - Portuguese sentence tokenizer'): 'stanza_por',
                _tr('wl_settings_global', 'Stanza - Romanian sentence tokenizer'): 'stanza_ron',
                _tr('wl_settings_global', 'Stanza - Russian sentence tokenizer'): 'stanza_rus',
                _tr('wl_settings_global', 'Stanza - Russian (Old) sentence tokenizer'): 'stanza_orv',
                _tr('wl_settings_global', 'Stanza - Sámi (Northern) sentence tokenizer'): 'stanza_sme',
                _tr('wl_settings_global', 'Stanza - Sanskrit sentence tokenizer'): 'stanza_san',
                _tr('wl_settings_global', 'Stanza - Scottish Gaelic sentence tokenizer'): 'stanza_gla',
                _tr('wl_settings_global', 'Stanza - Serbian (Latin script) sentence tokenizer'): 'stanza_srp_latn',
                _tr('wl_settings_global', 'Stanza - Sindhi sentence tokenizer'): 'stanza_snd',
                _tr('wl_settings_global', 'Stanza - Slovak sentence tokenizer'): 'stanza_slk',
                _tr('wl_settings_global', 'Stanza - Slovene sentence tokenizer'): 'stanza_slv',
                _tr('wl_settings_global', 'Stanza - Sorbian (Upper) sentence tokenizer'): 'stanza_hsb',
                _tr('wl_settings_global', 'Stanza - Spanish sentence tokenizer'): 'stanza_spa',
                _tr('wl_settings_global', 'Stanza - Swedish sentence tokenizer'): 'stanza_swe',
                _tr('wl_settings_global', 'Stanza - Tamil sentence tokenizer'): 'stanza_tam',
                _tr('wl_settings_global', 'Stanza - Telugu sentence tokenizer'): 'stanza_tel',
                _tr('wl_settings_global', 'Stanza - Thai sentence tokenizer'): 'stanza_tha',
                _tr('wl_settings_global', 'Stanza - Turkish sentence tokenizer'): 'stanza_tur',
                _tr('wl_settings_global', 'Stanza - Ukrainian sentence tokenizer'): 'stanza_ukr',
                _tr('wl_settings_global', 'Stanza - Urdu sentence tokenizer'): 'stanza_urd',
                _tr('wl_settings_global', 'Stanza - Uyghur sentence tokenizer'): 'stanza_uig',
                _tr('wl_settings_global', 'Stanza - Vietnamese sentence tokenizer'): 'stanza_vie',
                _tr('wl_settings_global', 'Stanza - Welsh sentence tokenizer'): 'stanza_cym',
                _tr('wl_settings_global', 'Stanza - Wolof sentence tokenizer'): 'stanza_wol',

                _tr('wl_settings_global', 'Underthesea - Vietnamese sentence tokenizer'): 'underthesea_vie'
            },

            'word_tokenizers': {
                _tr('wl_settings_global', 'botok - Tibetan word tokenizer'): 'botok_bod',
                _tr('wl_settings_global', 'khmer-nltk - Khmer word tokenizer'): 'khmer_nltk_khm',
                _tr('wl_settings_global', 'LaoNLP - Lao word tokenizer'): 'laonlp_lao',

                _tr('wl_settings_global', 'NLTK - NIST tokenizer'): 'nltk_nist',
                _tr('wl_settings_global', 'NLTK - NLTK tokenizer'): 'nltk_nltk',
                _tr('wl_settings_global', 'NLTK - Penn Treebank tokenizer'): 'nltk_penn_treebank',
                _tr('wl_settings_global', 'NLTK - Regular-expression tokenizer'): 'nltk_regex',
                _tr('wl_settings_global', 'NLTK - Tok-tok tokenizer'): 'nltk_tok_tok',
                _tr('wl_settings_global', 'NLTK - Twitter tokenizer'): 'nltk_twitter',

                _tr('wl_settings_global', 'pkuseg - Chinese word tokenizer'): 'pkuseg_zho',

                _tr('wl_settings_global', 'PyThaiNLP - Longest matching'): 'pythainlp_longest_matching',
                _tr('wl_settings_global', 'PyThaiNLP - Maximum matching'): 'pythainlp_max_matching',
                _tr('wl_settings_global', 'PyThaiNLP - Maximum matching + TCC'): 'pythainlp_max_matching_tcc',
                'PyThaiNLP - NERCut': 'pythainlp_nercut',

                'python-mecab-ko - MeCab': 'python_mecab_ko_mecab',
                _tr('wl_settings_global', 'Sacremoses - Moses tokenizer'): 'sacremoses_moses',

                _tr('wl_settings_global', 'spaCy - Afrikaans word tokenizer'): 'spacy_afr',
                _tr('wl_settings_global', 'spaCy - Albanian word tokenizer'): 'spacy_sqi',
                _tr('wl_settings_global', 'spaCy - Amharic word tokenizer'): 'spacy_amh',
                _tr('wl_settings_global', 'spaCy - Arabic word tokenizer'): 'spacy_ara',
                _tr('wl_settings_global', 'spaCy - Armenian word tokenizer'): 'spacy_hye',
                _tr('wl_settings_global', 'spaCy - Azerbaijani word tokenizer'): 'spacy_aze',
                _tr('wl_settings_global', 'spaCy - Basque word tokenizer'): 'spacy_eus',
                _tr('wl_settings_global', 'spaCy - Bengali word tokenizer'): 'spacy_ben',
                _tr('wl_settings_global', 'spaCy - Bulgarian word tokenizer'): 'spacy_bul',
                _tr('wl_settings_global', 'spaCy - Catalan word tokenizer'): 'spacy_cat',
                _tr('wl_settings_global', 'spaCy - Chinese word tokenizer'): 'spacy_zho',
                _tr('wl_settings_global', 'spaCy - Croatian word tokenizer'): 'spacy_hrv',
                _tr('wl_settings_global', 'spaCy - Czech word tokenizer'): 'spacy_ces',
                _tr('wl_settings_global', 'spaCy - Danish word tokenizer'): 'spacy_dan',
                _tr('wl_settings_global', 'spaCy - Dutch word tokenizer'): 'spacy_nld',
                _tr('wl_settings_global', 'spaCy - English word tokenizer'): 'spacy_eng',
                _tr('wl_settings_global', 'spaCy - Estonian word tokenizer'): 'spacy_est',
                _tr('wl_settings_global', 'spaCy - Faroese word tokenizer'): 'spacy_fao',
                _tr('wl_settings_global', 'spaCy - Finnish word tokenizer'): 'spacy_fin',
                _tr('wl_settings_global', 'spaCy - French word tokenizer'): 'spacy_fra',
                _tr('wl_settings_global', 'spaCy - German word tokenizer'): 'spacy_deu',
                _tr('wl_settings_global', 'spaCy - Greek (Ancient) word tokenizer'): 'spacy_grc',
                _tr('wl_settings_global', 'spaCy - Greek (Modern) word tokenizer'): 'spacy_ell',
                _tr('wl_settings_global', 'spaCy - Gujarati word tokenizer'): 'spacy_guj',
                _tr('wl_settings_global', 'spaCy - Hebrew (Modern) word tokenizer'): 'spacy_heb',
                _tr('wl_settings_global', 'spaCy - Hindi word tokenizer'): 'spacy_hin',
                _tr('wl_settings_global', 'spaCy - Hungarian word tokenizer'): 'spacy_hun',
                _tr('wl_settings_global', 'spaCy - Icelandic word tokenizer'): 'spacy_isl',
                _tr('wl_settings_global', 'spaCy - Indonesian word tokenizer'): 'spacy_ind',
                _tr('wl_settings_global', 'spaCy - Irish word tokenizer'): 'spacy_gle',
                _tr('wl_settings_global', 'spaCy - Italian word tokenizer'): 'spacy_ita',
                _tr('wl_settings_global', 'spaCy - Japanese word tokenizer'): 'spacy_jpn',
                _tr('wl_settings_global', 'spaCy - Kannada word tokenizer'): 'spacy_kan',
                _tr('wl_settings_global', 'spaCy - Korean word tokenizer'): 'spacy_kor',
                _tr('wl_settings_global', 'spaCy - Kyrgyz word tokenizer'): 'spacy_kir',
                _tr('wl_settings_global', 'spaCy - Latin word tokenizer'): 'spacy_lat',
                _tr('wl_settings_global', 'spaCy - Latvian word tokenizer'): 'spacy_lav',
                _tr('wl_settings_global', 'spaCy - Ligurian word tokenizer'): 'spacy_lij',
                _tr('wl_settings_global', 'spaCy - Lithuanian word tokenizer'): 'spacy_lit',
                _tr('wl_settings_global', 'spaCy - Luganda word tokenizer'): 'spacy_lug',
                _tr('wl_settings_global', 'spaCy - Luxembourgish word tokenizer'): 'spacy_ltz',
                _tr('wl_settings_global', 'spaCy - Macedonian word tokenizer'): 'spacy_mkd',
                _tr('wl_settings_global', 'spaCy - Malay word tokenizer'): 'spacy_msa',
                _tr('wl_settings_global', 'spaCy - Malayalam word tokenizer'): 'spacy_mal',
                _tr('wl_settings_global', 'spaCy - Marathi word tokenizer'): 'spacy_mar',
                _tr('wl_settings_global', 'spaCy - Nepali word tokenizer'): 'spacy_nep',
                _tr('wl_settings_global', 'spaCy - Norwegian (Bokmål) word tokenizer'): 'spacy_nob',
                _tr('wl_settings_global', 'spaCy - Norwegian (Nynorsk) word tokenizer'): 'spacy_nno',
                _tr('wl_settings_global', 'spaCy - Persian word tokenizer'): 'spacy_fas',
                _tr('wl_settings_global', 'spaCy - Polish word tokenizer'): 'spacy_pol',
                _tr('wl_settings_global', 'spaCy - Portuguese word tokenizer'): 'spacy_por',
                _tr('wl_settings_global', 'spaCy - Romanian word tokenizer'): 'spacy_ron',
                _tr('wl_settings_global', 'spaCy - Russian word tokenizer'): 'spacy_rus',
                _tr('wl_settings_global', 'spaCy - Sanskrit word tokenizer'): 'spacy_san',
                _tr('wl_settings_global', 'spaCy - Serbian (Cyrillic script) word tokenizer'): 'spacy_srp',
                _tr('wl_settings_global', 'spaCy - Sinhala word tokenizer'): 'spacy_sin',
                _tr('wl_settings_global', 'spaCy - Slovak word tokenizer'): 'spacy_slk',
                _tr('wl_settings_global', 'spaCy - Slovene word tokenizer'): 'spacy_slv',
                _tr('wl_settings_global', 'spaCy - Sorbian (Lower) word tokenizer'): 'spacy_dsb',
                _tr('wl_settings_global', 'spaCy - Sorbian (Upper) word tokenizer'): 'spacy_hsb',
                _tr('wl_settings_global', 'spaCy - Spanish word tokenizer'): 'spacy_spa',
                _tr('wl_settings_global', 'spaCy - Swedish word tokenizer'): 'spacy_swe',
                _tr('wl_settings_global', 'spaCy - Tagalog word tokenizer'): 'spacy_tgl',
                _tr('wl_settings_global', 'spaCy - Tamil word tokenizer'): 'spacy_tam',
                _tr('wl_settings_global', 'spaCy - Tatar word tokenizer'): 'spacy_tat',
                _tr('wl_settings_global', 'spaCy - Telugu word tokenizer'): 'spacy_tel',
                _tr('wl_settings_global', 'spaCy - Tigrinya word tokenizer'): 'spacy_tir',
                _tr('wl_settings_global', 'spaCy - Tswana word tokenizer'): 'spacy_tsn',
                _tr('wl_settings_global', 'spaCy - Turkish word tokenizer'): 'spacy_tur',
                _tr('wl_settings_global', 'spaCy - Ukrainian word tokenizer'): 'spacy_ukr',
                _tr('wl_settings_global', 'spaCy - Urdu word tokenizer'): 'spacy_urd',
                _tr('wl_settings_global', 'spaCy - Yoruba word tokenizer'): 'spacy_yor',

                _tr('wl_settings_global', 'Stanza - Afrikaans word tokenizer'): 'stanza_afr',
                _tr('wl_settings_global', 'Stanza - Arabic word tokenizer'): 'stanza_ara',
                _tr('wl_settings_global', 'Stanza - Armenian (Classical) word tokenizer'): 'stanza_xcl',
                _tr('wl_settings_global', 'Stanza - Armenian (Eastern) word tokenizer'): 'stanza_hye',
                _tr('wl_settings_global', 'Stanza - Armenian (Western) word tokenizer'): 'stanza_hyw',
                _tr('wl_settings_global', 'Stanza - Basque word tokenizer'): 'stanza_eus',
                _tr('wl_settings_global', 'Stanza - Belarusian word tokenizer'): 'stanza_bel',
                _tr('wl_settings_global', 'Stanza - Bulgarian word tokenizer'): 'stanza_bul',
                _tr('wl_settings_global', 'Stanza - Burmese word tokenizer'): 'stanza_mya',
                _tr('wl_settings_global', 'Stanza - Buryat (Russia) word tokenizer'): 'stanza_bxr',
                _tr('wl_settings_global', 'Stanza - Catalan word tokenizer'): 'stanza_cat',
                _tr('wl_settings_global', 'Stanza - Chinese (Classical) word tokenizer'): 'stanza_lzh',
                _tr('wl_settings_global', 'Stanza - Chinese (Simplified) word tokenizer'): 'stanza_zho_cn',
                _tr('wl_settings_global', 'Stanza - Chinese (Traditional) word tokenizer'): 'stanza_zho_tw',
                _tr('wl_settings_global', 'Stanza - Church Slavonic (Old) word tokenizer'): 'stanza_chu',
                _tr('wl_settings_global', 'Stanza - Coptic word tokenizer'): 'stanza_cop',
                _tr('wl_settings_global', 'Stanza - Croatian word tokenizer'): 'stanza_hrv',
                _tr('wl_settings_global', 'Stanza - Czech word tokenizer'): 'stanza_ces',
                _tr('wl_settings_global', 'Stanza - Danish word tokenizer'): 'stanza_dan',
                _tr('wl_settings_global', 'Stanza - Dutch word tokenizer'): 'stanza_nld',
                _tr('wl_settings_global', 'Stanza - English word tokenizer'): 'stanza_eng',
                _tr('wl_settings_global', 'Stanza - English (Old) word tokenizer'): 'stanza_ang',
                _tr('wl_settings_global', 'Stanza - Erzya word tokenizer'): 'stanza_myv',
                _tr('wl_settings_global', 'Stanza - Estonian word tokenizer'): 'stanza_est',
                _tr('wl_settings_global', 'Stanza - Faroese word tokenizer'): 'stanza_fao',
                _tr('wl_settings_global', 'Stanza - Finnish word tokenizer'): 'stanza_fin',
                _tr('wl_settings_global', 'Stanza - French word tokenizer'): 'stanza_fra',
                _tr('wl_settings_global', 'Stanza - French (Old) word tokenizer'): 'stanza_fro',
                _tr('wl_settings_global', 'Stanza - Galician word tokenizer'): 'stanza_glg',
                _tr('wl_settings_global', 'Stanza - German word tokenizer'): 'stanza_deu',
                _tr('wl_settings_global', 'Stanza - Gothic word tokenizer'): 'stanza_got',
                _tr('wl_settings_global', 'Stanza - Greek (Ancient) word tokenizer'): 'stanza_grc',
                _tr('wl_settings_global', 'Stanza - Greek (Modern) word tokenizer'): 'stanza_ell',
                _tr('wl_settings_global', 'Stanza - Hebrew (Ancient) word tokenizer'): 'stanza_hbo',
                _tr('wl_settings_global', 'Stanza - Hebrew (Modern) word tokenizer'): 'stanza_heb',
                _tr('wl_settings_global', 'Stanza - Hindi word tokenizer'): 'stanza_hin',
                _tr('wl_settings_global', 'Stanza - Hungarian word tokenizer'): 'stanza_hun',
                _tr('wl_settings_global', 'Stanza - Icelandic word tokenizer'): 'stanza_isl',
                _tr('wl_settings_global', 'Stanza - Indonesian word tokenizer'): 'stanza_ind',
                _tr('wl_settings_global', 'Stanza - Irish word tokenizer'): 'stanza_gle',
                _tr('wl_settings_global', 'Stanza - Italian word tokenizer'): 'stanza_ita',
                _tr('wl_settings_global', 'Stanza - Japanese word tokenizer'): 'stanza_jpn',
                _tr('wl_settings_global', 'Stanza - Kazakh word tokenizer'): 'stanza_kaz',
                _tr('wl_settings_global', 'Stanza - Korean word tokenizer'): 'stanza_kor',
                _tr('wl_settings_global', 'Stanza - Kurdish (Kurmanji) word tokenizer'): 'stanza_kmr',
                _tr('wl_settings_global', 'Stanza - Kyrgyz word tokenizer'): 'stanza_kir',
                _tr('wl_settings_global', 'Stanza - Latin word tokenizer'): 'stanza_lat',
                _tr('wl_settings_global', 'Stanza - Latvian word tokenizer'): 'stanza_lav',
                _tr('wl_settings_global', 'Stanza - Ligurian word tokenizer'): 'stanza_lij',
                _tr('wl_settings_global', 'Stanza - Lithuanian word tokenizer'): 'stanza_lit',
                _tr('wl_settings_global', 'Stanza - Maltese word tokenizer'): 'stanza_mlt',
                _tr('wl_settings_global', 'Stanza - Manx word tokenizer'): 'stanza_glv',
                _tr('wl_settings_global', 'Stanza - Marathi word tokenizer'): 'stanza_mar',
                _tr('wl_settings_global', 'Stanza - Nigerian Pidgin word tokenizer'): 'stanza_pcm',
                _tr('wl_settings_global', 'Stanza - Norwegian (Bokmål) word tokenizer'): 'stanza_nob',
                _tr('wl_settings_global', 'Stanza - Norwegian (Nynorsk) word tokenizer'): 'stanza_nno',
                _tr('wl_settings_global', 'Stanza - Persian word tokenizer'): 'stanza_fas',
                _tr('wl_settings_global', 'Stanza - Polish word tokenizer'): 'stanza_pol',
                _tr('wl_settings_global', 'Stanza - Pomak word tokenizer'): 'stanza_qpm',
                _tr('wl_settings_global', 'Stanza - Portuguese word tokenizer'): 'stanza_por',
                _tr('wl_settings_global', 'Stanza - Romanian word tokenizer'): 'stanza_ron',
                _tr('wl_settings_global', 'Stanza - Russian word tokenizer'): 'stanza_rus',
                _tr('wl_settings_global', 'Stanza - Russian (Old) word tokenizer'): 'stanza_orv',
                _tr('wl_settings_global', 'Stanza - Sámi (Northern) word tokenizer'): 'stanza_sme',
                _tr('wl_settings_global', 'Stanza - Sanskrit word tokenizer'): 'stanza_san',
                _tr('wl_settings_global', 'Stanza - Scottish Gaelic word tokenizer'): 'stanza_gla',
                _tr('wl_settings_global', 'Stanza - Serbian (Latin script) word tokenizer'): 'stanza_srp_latn',
                _tr('wl_settings_global', 'Stanza - Sindhi word tokenizer'): 'stanza_snd',
                _tr('wl_settings_global', 'Stanza - Slovak word tokenizer'): 'stanza_slk',
                _tr('wl_settings_global', 'Stanza - Slovene word tokenizer'): 'stanza_slv',
                _tr('wl_settings_global', 'Stanza - Sorbian (Upper) word tokenizer'): 'stanza_hsb',
                _tr('wl_settings_global', 'Stanza - Spanish word tokenizer'): 'stanza_spa',
                _tr('wl_settings_global', 'Stanza - Swedish word tokenizer'): 'stanza_swe',
                _tr('wl_settings_global', 'Stanza - Tamil word tokenizer'): 'stanza_tam',
                _tr('wl_settings_global', 'Stanza - Telugu word tokenizer'): 'stanza_tel',
                _tr('wl_settings_global', 'Stanza - Thai word tokenizer'): 'stanza_tha',
                _tr('wl_settings_global', 'Stanza - Turkish word tokenizer'): 'stanza_tur',
                _tr('wl_settings_global', 'Stanza - Ukrainian word tokenizer'): 'stanza_ukr',
                _tr('wl_settings_global', 'Stanza - Urdu word tokenizer'): 'stanza_urd',
                _tr('wl_settings_global', 'Stanza - Uyghur word tokenizer'): 'stanza_uig',
                _tr('wl_settings_global', 'Stanza - Vietnamese word tokenizer'): 'stanza_vie',
                _tr('wl_settings_global', 'Stanza - Welsh word tokenizer'): 'stanza_cym',
                _tr('wl_settings_global', 'Stanza - Wolof word tokenizer'): 'stanza_wol',

                _tr('wl_settings_global', 'SudachiPy - Japanese word tokenizer (split mode A)'): 'sudachipy_jpn_split_mode_a',
                _tr('wl_settings_global', 'SudachiPy - Japanese word tokenizer (split mode B)'): 'sudachipy_jpn_split_mode_b',
                _tr('wl_settings_global', 'SudachiPy - Japanese word tokenizer (split mode C)'): 'sudachipy_jpn_split_mode_c',

                _tr('wl_settings_global', 'Underthesea - Vietnamese word tokenizer'): 'underthesea_vie',

                _tr('wl_settings_global', 'Wordless - Chinese character tokenizer'): 'wordless_zho_char',
                _tr('wl_settings_global', 'Wordless - Japanese kanji tokenizer'): 'wordless_jpn_kanji'
            },

            'syl_tokenizers': {
                _tr('wl_settings_global', 'NLTK - Legality syllable tokenizer'): 'nltk_legality',
                _tr('wl_settings_global', 'NLTK - Sonority sequencing syllable tokenizer'): 'nltk_sonority_sequencing',

                _tr('wl_settings_global', 'Pyphen - Afrikaans syllable tokenizer'): 'pyphen_afr',
                _tr('wl_settings_global', 'Pyphen - Albanian syllable tokenizer'): 'pyphen_sqi',
                _tr('wl_settings_global', 'Pyphen - Basque syllable tokenizer'): 'pyphen_eus',
                _tr('wl_settings_global', 'Pyphen - Belarusian syllable tokenizer'): 'pyphen_bel',
                _tr('wl_settings_global', 'Pyphen - Bulgarian syllable tokenizer'): 'pyphen_bul',
                _tr('wl_settings_global', 'Pyphen - Catalan syllable tokenizer'): 'pyphen_cat',
                _tr('wl_settings_global', 'Pyphen - Croatian syllable tokenizer'): 'pyphen_hrv',
                _tr('wl_settings_global', 'Pyphen - Czech syllable tokenizer'): 'pyphen_ces',
                _tr('wl_settings_global', 'Pyphen - Danish syllable tokenizer'): 'pyphen_dan',
                _tr('wl_settings_global', 'Pyphen - Dutch syllable tokenizer'): 'pyphen_nld',
                _tr('wl_settings_global', 'Pyphen - English (United Kingdom) syllable tokenizer'): 'pyphen_eng_gb',
                _tr('wl_settings_global', 'Pyphen - English (United States) syllable tokenizer'): 'pyphen_eng_us',
                _tr('wl_settings_global', 'Pyphen - Esperanto syllable tokenizer'): 'pyphen_epo',
                _tr('wl_settings_global', 'Pyphen - Estonian syllable tokenizer'): 'pyphen_est',
                _tr('wl_settings_global', 'Pyphen - French syllable tokenizer'): 'pyphen_fra',
                _tr('wl_settings_global', 'Pyphen - Galician syllable tokenizer'): 'pyphen_glg',
                _tr('wl_settings_global', 'Pyphen - German (Austria) syllable tokenizer'): 'pyphen_deu_at',
                _tr('wl_settings_global', 'Pyphen - German (Germany) syllable tokenizer'): 'pyphen_deu_de',
                _tr('wl_settings_global', 'Pyphen - German (Switzerland) syllable tokenizer'): 'pyphen_deu_ch',
                _tr('wl_settings_global', 'Pyphen - Greek (Modern) syllable tokenizer'): 'pyphen_ell',
                _tr('wl_settings_global', 'Pyphen - Hungarian syllable tokenizer'): 'pyphen_hun',
                _tr('wl_settings_global', 'Pyphen - Icelandic syllable tokenizer'): 'pyphen_isl',
                _tr('wl_settings_global', 'Pyphen - Indonesian syllable tokenizer'): 'pyphen_ind',
                _tr('wl_settings_global', 'Pyphen - Italian syllable tokenizer'): 'pyphen_ita',
                _tr('wl_settings_global', 'Pyphen - Lithuanian syllable tokenizer'): 'pyphen_lit',
                _tr('wl_settings_global', 'Pyphen - Latvian syllable tokenizer'): 'pyphen_lav',
                _tr('wl_settings_global', 'Pyphen - Mongolian syllable tokenizer'): 'pyphen_mon',
                _tr('wl_settings_global', 'Pyphen - Norwegian (Bokmål) syllable tokenizer'): 'pyphen_nob',
                _tr('wl_settings_global', 'Pyphen - Norwegian (Nynorsk) syllable tokenizer'): 'pyphen_nno',
                _tr('wl_settings_global', 'Pyphen - Polish syllable tokenizer'): 'pyphen_pol',
                _tr('wl_settings_global', 'Pyphen - Portuguese (Brazil) syllable tokenizer'): 'pyphen_por_br',
                _tr('wl_settings_global', 'Pyphen - Portuguese (Portugal) syllable tokenizer'): 'pyphen_por_pt',
                _tr('wl_settings_global', 'Pyphen - Romanian syllable tokenizer'): 'pyphen_ron',
                _tr('wl_settings_global', 'Pyphen - Russian syllable tokenizer'): 'pyphen_rus',
                _tr('wl_settings_global', 'Pyphen - Serbian (Cyrillic script) syllable tokenizer'): 'pyphen_srp_cyrl',
                _tr('wl_settings_global', 'Pyphen - Serbian (Latin script) syllable tokenizer'): 'pyphen_srp_latn',
                _tr('wl_settings_global', 'Pyphen - Slovak syllable tokenizer'): 'pyphen_slk',
                _tr('wl_settings_global', 'Pyphen - Slovene syllable tokenizer'): 'pyphen_slv',
                _tr('wl_settings_global', 'Pyphen - Spanish syllable tokenizer'): 'pyphen_spa',
                _tr('wl_settings_global', 'Pyphen - Swedish syllable tokenizer'): 'pyphen_swe',
                _tr('wl_settings_global', 'Pyphen - Telugu syllable tokenizer'): 'pyphen_tel',
                _tr('wl_settings_global', 'Pyphen - Thai syllable tokenizer'): 'pyphen_tha',
                _tr('wl_settings_global', 'Pyphen - Ukrainian syllable tokenizer'): 'pyphen_ukr',
                _tr('wl_settings_global', 'Pyphen - Zulu syllable tokenizer'): 'pyphen_zul',

                'PyThaiNLP - Han-solo': 'pythainlp_han_solo',
                _tr('wl_settings_global', 'PyThaiNLP - Syllable dictionary'): 'pythainlp_syl_dict'
            },

            'pos_taggers': {
                _tr('wl_settings_global', 'botok - Tibetan part-of-speech tagger'): 'botok_bod',
                _tr('wl_settings_global', 'khmer-nltk - Khmer part-of-speech tagger'): 'khmer_nltk_khm',

                'LaoNLP - SeqLabeling': 'laonlp_seqlabeling',
                _tr('wl_settings_global', 'LaoNLP - Yunshan Cup 2020'): 'laonlp_yunshan_cup_2020',

                _tr('wl_settings_global', 'NLTK - English perceptron part-of-speech tagger'): 'nltk_perceptron_eng',
                _tr('wl_settings_global', 'NLTK - Russian perceptron part-of-speech tagger'): 'nltk_perceptron_rus',

                _tr('wl_settings_global', 'pymorphy3 - Morphological analyzer'): 'pymorphy3_morphological_analyzer',
                'python-mecab-ko - MeCab': 'python_mecab_ko_mecab',

                _tr('wl_settings_global', 'PyThaiNLP - Perceptron part-of-speech tagger (Blackboard)'): 'pythainlp_perceptron_blackboard',
                _tr('wl_settings_global', 'PyThaiNLP - Perceptron part-of-speech tagger (ORCHID)'): 'pythainlp_perceptron_orchid',
                _tr('wl_settings_global', 'PyThaiNLP - Perceptron part-of-speech tagger (PUD)'): 'pythainlp_perceptron_pud',

                _tr('wl_settings_global', 'spaCy - Catalan part-of-speech tagger'): 'spacy_cat',
                _tr('wl_settings_global', 'spaCy - Chinese part-of-speech tagger'): 'spacy_zho',
                _tr('wl_settings_global', 'spaCy - Croatian part-of-speech tagger'): 'spacy_hrv',
                _tr('wl_settings_global', 'spaCy - Danish part-of-speech tagger'): 'spacy_dan',
                _tr('wl_settings_global', 'spaCy - Dutch part-of-speech tagger'): 'spacy_nld',
                _tr('wl_settings_global', 'spaCy - English part-of-speech tagger'): 'spacy_eng',
                _tr('wl_settings_global', 'spaCy - Finnish part-of-speech tagger'): 'spacy_fin',
                _tr('wl_settings_global', 'spaCy - French part-of-speech tagger'): 'spacy_fra',
                _tr('wl_settings_global', 'spaCy - German part-of-speech tagger'): 'spacy_deu',
                _tr('wl_settings_global', 'spaCy - Greek (Modern) part-of-speech tagger'): 'spacy_ell',
                _tr('wl_settings_global', 'spaCy - Italian part-of-speech tagger'): 'spacy_ita',
                _tr('wl_settings_global', 'spaCy - Japanese part-of-speech tagger'): 'spacy_jpn',
                _tr('wl_settings_global', 'spaCy - Korean part-of-speech tagger'): 'spacy_kor',
                _tr('wl_settings_global', 'spaCy - Lithuanian part-of-speech tagger'): 'spacy_lit',
                _tr('wl_settings_global', 'spaCy - Macedonian part-of-speech tagger'): 'spacy_mkd',
                _tr('wl_settings_global', 'spaCy - Norwegian (Bokmål) part-of-speech tagger'): 'spacy_nob',
                _tr('wl_settings_global', 'spaCy - Polish part-of-speech tagger'): 'spacy_pol',
                _tr('wl_settings_global', 'spaCy - Portuguese part-of-speech tagger'): 'spacy_por',
                _tr('wl_settings_global', 'spaCy - Romanian part-of-speech tagger'): 'spacy_ron',
                _tr('wl_settings_global', 'spaCy - Russian part-of-speech tagger'): 'spacy_rus',
                _tr('wl_settings_global', 'spaCy - Slovene part-of-speech tagger'): 'spacy_slv',
                _tr('wl_settings_global', 'spaCy - Spanish part-of-speech tagger'): 'spacy_spa',
                _tr('wl_settings_global', 'spaCy - Swedish part-of-speech tagger'): 'spacy_swe',
                _tr('wl_settings_global', 'spaCy - Ukrainian part-of-speech tagger'): 'spacy_ukr',

                _tr('wl_settings_global', 'Stanza - Afrikaans part-of-speech tagger'): 'stanza_afr',
                _tr('wl_settings_global', 'Stanza - Arabic part-of-speech tagger'): 'stanza_ara',
                _tr('wl_settings_global', 'Stanza - Armenian (Classical) part-of-speech tagger'): 'stanza_xcl',
                _tr('wl_settings_global', 'Stanza - Armenian (Eastern) part-of-speech tagger'): 'stanza_hye',
                _tr('wl_settings_global', 'Stanza - Armenian (Western) part-of-speech tagger'): 'stanza_hyw',
                _tr('wl_settings_global', 'Stanza - Basque part-of-speech tagger'): 'stanza_eus',
                _tr('wl_settings_global', 'Stanza - Belarusian part-of-speech tagger'): 'stanza_bel',
                _tr('wl_settings_global', 'Stanza - Bulgarian part-of-speech tagger'): 'stanza_bul',
                _tr('wl_settings_global', 'Stanza - Buryat (Russia) part-of-speech tagger'): 'stanza_bxr',
                _tr('wl_settings_global', 'Stanza - Catalan part-of-speech tagger'): 'stanza_cat',
                _tr('wl_settings_global', 'Stanza - Chinese (Classical) part-of-speech tagger'): 'stanza_lzh',
                _tr('wl_settings_global', 'Stanza - Chinese (Simplified) part-of-speech tagger'): 'stanza_zho_cn',
                _tr('wl_settings_global', 'Stanza - Chinese (Traditional) part-of-speech tagger'): 'stanza_zho_tw',
                _tr('wl_settings_global', 'Stanza - Church Slavonic (Old) part-of-speech tagger'): 'stanza_chu',
                _tr('wl_settings_global', 'Stanza - Coptic part-of-speech tagger'): 'stanza_cop',
                _tr('wl_settings_global', 'Stanza - Croatian part-of-speech tagger'): 'stanza_hrv',
                _tr('wl_settings_global', 'Stanza - Czech part-of-speech tagger'): 'stanza_ces',
                _tr('wl_settings_global', 'Stanza - Danish part-of-speech tagger'): 'stanza_dan',
                _tr('wl_settings_global', 'Stanza - Dutch part-of-speech tagger'): 'stanza_nld',
                _tr('wl_settings_global', 'Stanza - English part-of-speech tagger'): 'stanza_eng',
                _tr('wl_settings_global', 'Stanza - English (Old) part-of-speech tagger'): 'stanza_ang',
                _tr('wl_settings_global', 'Stanza - Erzya part-of-speech tagger'): 'stanza_myv',
                _tr('wl_settings_global', 'Stanza - Estonian part-of-speech tagger'): 'stanza_est',
                _tr('wl_settings_global', 'Stanza - Faroese part-of-speech tagger'): 'stanza_fao',
                _tr('wl_settings_global', 'Stanza - Finnish part-of-speech tagger'): 'stanza_fin',
                _tr('wl_settings_global', 'Stanza - French part-of-speech tagger'): 'stanza_fra',
                _tr('wl_settings_global', 'Stanza - French (Old) part-of-speech tagger'): 'stanza_fro',
                _tr('wl_settings_global', 'Stanza - Galician part-of-speech tagger'): 'stanza_glg',
                _tr('wl_settings_global', 'Stanza - German part-of-speech tagger'): 'stanza_deu',
                _tr('wl_settings_global', 'Stanza - Gothic part-of-speech tagger'): 'stanza_got',
                _tr('wl_settings_global', 'Stanza - Greek (Ancient) part-of-speech tagger'): 'stanza_grc',
                _tr('wl_settings_global', 'Stanza - Greek (Modern) part-of-speech tagger'): 'stanza_ell',
                _tr('wl_settings_global', 'Stanza - Hebrew (Ancient) part-of-speech tagger'): 'stanza_hbo',
                _tr('wl_settings_global', 'Stanza - Hebrew (Modern) part-of-speech tagger'): 'stanza_heb',
                _tr('wl_settings_global', 'Stanza - Hindi part-of-speech tagger'): 'stanza_hin',
                _tr('wl_settings_global', 'Stanza - Hungarian part-of-speech tagger'): 'stanza_hun',
                _tr('wl_settings_global', 'Stanza - Icelandic part-of-speech tagger'): 'stanza_isl',
                _tr('wl_settings_global', 'Stanza - Indonesian part-of-speech tagger'): 'stanza_ind',
                _tr('wl_settings_global', 'Stanza - Irish part-of-speech tagger'): 'stanza_gle',
                _tr('wl_settings_global', 'Stanza - Italian part-of-speech tagger'): 'stanza_ita',
                _tr('wl_settings_global', 'Stanza - Japanese part-of-speech tagger'): 'stanza_jpn',
                _tr('wl_settings_global', 'Stanza - Kazakh part-of-speech tagger'): 'stanza_kaz',
                _tr('wl_settings_global', 'Stanza - Korean part-of-speech tagger'): 'stanza_kor',
                _tr('wl_settings_global', 'Stanza - Kurdish (Kurmanji) part-of-speech tagger'): 'stanza_kmr',
                _tr('wl_settings_global', 'Stanza - Kyrgyz part-of-speech tagger'): 'stanza_kir',
                _tr('wl_settings_global', 'Stanza - Latin part-of-speech tagger'): 'stanza_lat',
                _tr('wl_settings_global', 'Stanza - Latvian part-of-speech tagger'): 'stanza_lav',
                _tr('wl_settings_global', 'Stanza - Ligurian part-of-speech tagger'): 'stanza_lij',
                _tr('wl_settings_global', 'Stanza - Lithuanian part-of-speech tagger'): 'stanza_lit',
                _tr('wl_settings_global', 'Stanza - Maltese part-of-speech tagger'): 'stanza_mlt',
                _tr('wl_settings_global', 'Stanza - Manx part-of-speech tagger'): 'stanza_glv',
                _tr('wl_settings_global', 'Stanza - Marathi part-of-speech tagger'): 'stanza_mar',
                _tr('wl_settings_global', 'Stanza - Nigerian Pidgin part-of-speech tagger'): 'stanza_pcm',
                _tr('wl_settings_global', 'Stanza - Norwegian (Bokmål) part-of-speech tagger'): 'stanza_nob',
                _tr('wl_settings_global', 'Stanza - Norwegian (Nynorsk) part-of-speech tagger'): 'stanza_nno',
                _tr('wl_settings_global', 'Stanza - Persian part-of-speech tagger'): 'stanza_fas',
                _tr('wl_settings_global', 'Stanza - Polish part-of-speech tagger'): 'stanza_pol',
                _tr('wl_settings_global', 'Stanza - Pomak part-of-speech tagger'): 'stanza_qpm',
                _tr('wl_settings_global', 'Stanza - Portuguese part-of-speech tagger'): 'stanza_por',
                _tr('wl_settings_global', 'Stanza - Romanian part-of-speech tagger'): 'stanza_ron',
                _tr('wl_settings_global', 'Stanza - Russian part-of-speech tagger'): 'stanza_rus',
                _tr('wl_settings_global', 'Stanza - Russian (Old) part-of-speech tagger'): 'stanza_orv',
                _tr('wl_settings_global', 'Stanza - Sámi (Northern) part-of-speech tagger'): 'stanza_sme',
                _tr('wl_settings_global', 'Stanza - Sanskrit part-of-speech tagger'): 'stanza_san',
                _tr('wl_settings_global', 'Stanza - Scottish Gaelic part-of-speech tagger'): 'stanza_gla',
                _tr('wl_settings_global', 'Stanza - Serbian (Latin script) part-of-speech tagger'): 'stanza_srp_latn',
                _tr('wl_settings_global', 'Stanza - Sindhi part-of-speech tagger'): 'stanza_snd',
                _tr('wl_settings_global', 'Stanza - Slovak part-of-speech tagger'): 'stanza_slk',
                _tr('wl_settings_global', 'Stanza - Slovene part-of-speech tagger'): 'stanza_slv',
                _tr('wl_settings_global', 'Stanza - Sorbian (Upper) part-of-speech tagger'): 'stanza_hsb',
                _tr('wl_settings_global', 'Stanza - Spanish part-of-speech tagger'): 'stanza_spa',
                _tr('wl_settings_global', 'Stanza - Swedish part-of-speech tagger'): 'stanza_swe',
                _tr('wl_settings_global', 'Stanza - Tamil part-of-speech tagger'): 'stanza_tam',
                _tr('wl_settings_global', 'Stanza - Telugu part-of-speech tagger'): 'stanza_tel',
                _tr('wl_settings_global', 'Stanza - Turkish part-of-speech tagger'): 'stanza_tur',
                _tr('wl_settings_global', 'Stanza - Ukrainian part-of-speech tagger'): 'stanza_ukr',
                _tr('wl_settings_global', 'Stanza - Urdu part-of-speech tagger'): 'stanza_urd',
                _tr('wl_settings_global', 'Stanza - Uyghur part-of-speech tagger'): 'stanza_uig',
                _tr('wl_settings_global', 'Stanza - Vietnamese part-of-speech tagger'): 'stanza_vie',
                _tr('wl_settings_global', 'Stanza - Welsh part-of-speech tagger'): 'stanza_cym',
                _tr('wl_settings_global', 'Stanza - Wolof part-of-speech tagger'): 'stanza_wol',

                _tr('wl_settings_global', 'SudachiPy - Japanese part-of-speech tagger'): 'sudachipy_jpn',
                _tr('wl_settings_global', 'Underthesea - Vietnamese part-of-speech tagger'): 'underthesea_vie'
            },

            'lemmatizers': {
                _tr('wl_settings_global', 'botok - Tibetan lemmatizer'): 'botok_bod',
                _tr('wl_settings_global', 'NLTK - WordNet lemmatizer'): 'nltk_wordnet',
                _tr('wl_settings_global', 'pymorphy3 - Morphological analyzer'): 'pymorphy3_morphological_analyzer',

                _tr('wl_settings_global', 'simplemma - Albanian lemmatizer'): 'simplemma_sqi',
                _tr('wl_settings_global', 'simplemma - Armenian lemmatizer'): 'simplemma_hye',
                _tr('wl_settings_global', 'simplemma - Asturian lemmatizer'): 'simplemma_ast',
                _tr('wl_settings_global', 'simplemma - Bulgarian lemmatizer'): 'simplemma_bul',
                _tr('wl_settings_global', 'simplemma - Catalan lemmatizer'): 'simplemma_cat',
                _tr('wl_settings_global', 'simplemma - Czech lemmatizer'): 'simplemma_ces',
                _tr('wl_settings_global', 'simplemma - Danish lemmatizer'): 'simplemma_dan',
                _tr('wl_settings_global', 'simplemma - Dutch lemmatizer'): 'simplemma_nld',
                _tr('wl_settings_global', 'simplemma - English lemmatizer'): 'simplemma_eng',
                _tr('wl_settings_global', 'simplemma - English (Middle) lemmatizer'): 'simplemma_enm',
                _tr('wl_settings_global', 'simplemma - Estonian lemmatizer'): 'simplemma_est',
                _tr('wl_settings_global', 'simplemma - Finnish lemmatizer'): 'simplemma_fin',
                _tr('wl_settings_global', 'simplemma - French lemmatizer'): 'simplemma_fra',
                _tr('wl_settings_global', 'simplemma - Galician lemmatizer'): 'simplemma_glg',
                _tr('wl_settings_global', 'simplemma - Georgian lemmatizer'): 'simplemma_kat',
                _tr('wl_settings_global', 'simplemma - German lemmatizer'): 'simplemma_deu',
                _tr('wl_settings_global', 'simplemma - Greek (Modern) lemmatizer'): 'simplemma_ell',
                _tr('wl_settings_global', 'simplemma - Hindi lemmatizer'): 'simplemma_hin',
                _tr('wl_settings_global', 'simplemma - Hungarian lemmatizer'): 'simplemma_hun',
                _tr('wl_settings_global', 'simplemma - Icelandic lemmatizer'): 'simplemma_isl',
                _tr('wl_settings_global', 'simplemma - Indonesian lemmatizer'): 'simplemma_ind',
                _tr('wl_settings_global', 'simplemma - Irish lemmatizer'): 'simplemma_gle',
                _tr('wl_settings_global', 'simplemma - Italian lemmatizer'): 'simplemma_ita',
                _tr('wl_settings_global', 'simplemma - Latin lemmatizer'): 'simplemma_lat',
                _tr('wl_settings_global', 'simplemma - Latvian lemmatizer'): 'simplemma_lav',
                _tr('wl_settings_global', 'simplemma - Lithuanian lemmatizer'): 'simplemma_lit',
                _tr('wl_settings_global', 'simplemma - Luxembourgish lemmatizer'): 'simplemma_ltz',
                _tr('wl_settings_global', 'simplemma - Macedonian lemmatizer'): 'simplemma_mkd',
                _tr('wl_settings_global', 'simplemma - Malay lemmatizer'): 'simplemma_msa',
                _tr('wl_settings_global', 'simplemma - Manx lemmatizer'): 'simplemma_glv',
                _tr('wl_settings_global', 'simplemma - Norwegian (Bokmål) lemmatizer'): 'simplemma_nob',
                _tr('wl_settings_global', 'simplemma - Norwegian (Nynorsk) lemmatizer'): 'simplemma_nno',
                _tr('wl_settings_global', 'simplemma - Persian lemmatizer'): 'simplemma_fas',
                _tr('wl_settings_global', 'simplemma - Polish lemmatizer'): 'simplemma_pol',
                _tr('wl_settings_global', 'simplemma - Portuguese lemmatizer'): 'simplemma_por',
                _tr('wl_settings_global', 'simplemma - Romanian lemmatizer'): 'simplemma_ron',
                _tr('wl_settings_global', 'simplemma - Russian lemmatizer'): 'simplemma_rus',
                _tr('wl_settings_global', 'simplemma - Sámi (Northern) lemmatizer'): 'simplemma_sme',
                _tr('wl_settings_global', 'simplemma - Scottish Gaelic lemmatizer'): 'simplemma_gla',
                _tr('wl_settings_global', 'simplemma - Serbo-Croatian lemmatizer'): 'simplemma_hbs',
                _tr('wl_settings_global', 'simplemma - Slovak lemmatizer'): 'simplemma_slk',
                _tr('wl_settings_global', 'simplemma - Slovene lemmatizer'): 'simplemma_slv',
                _tr('wl_settings_global', 'simplemma - Spanish lemmatizer'): 'simplemma_spa',
                _tr('wl_settings_global', 'simplemma - Swahili lemmatizer'): 'simplemma_swa',
                _tr('wl_settings_global', 'simplemma - Swedish lemmatizer'): 'simplemma_swe',
                _tr('wl_settings_global', 'simplemma - Tagalog lemmatizer'): 'simplemma_tgl',
                _tr('wl_settings_global', 'simplemma - Turkish lemmatizer'): 'simplemma_tur',
                _tr('wl_settings_global', 'simplemma - Ukrainian lemmatizer'): 'simplemma_ukr',
                _tr('wl_settings_global', 'simplemma - Welsh lemmatizer'): 'simplemma_cym',

                _tr('wl_settings_global', 'spaCy - Bengali lemmatizer'): 'spacy_ben',
                _tr('wl_settings_global', 'spaCy - Catalan lemmatizer'): 'spacy_cat',
                _tr('wl_settings_global', 'spaCy - Croatian lemmatizer'): 'spacy_hrv',
                _tr('wl_settings_global', 'spaCy - Czech lemmatizer'): 'spacy_ces',
                _tr('wl_settings_global', 'spaCy - Danish lemmatizer'): 'spacy_dan',
                _tr('wl_settings_global', 'spaCy - Dutch lemmatizer'): 'spacy_nld',
                _tr('wl_settings_global', 'spaCy - English lemmatizer'): 'spacy_eng',
                _tr('wl_settings_global', 'spaCy - Finnish lemmatizer'): 'spacy_fin',
                _tr('wl_settings_global', 'spaCy - French lemmatizer'): 'spacy_fra',
                _tr('wl_settings_global', 'spaCy - German lemmatizer'): 'spacy_deu',
                _tr('wl_settings_global', 'spaCy - Greek (Ancient) lemmatizer'): 'spacy_grc',
                _tr('wl_settings_global', 'spaCy - Greek (Modern) lemmatizer'): 'spacy_ell',
                _tr('wl_settings_global', 'spaCy - Hungarian lemmatizer'): 'spacy_hun',
                _tr('wl_settings_global', 'spaCy - Indonesian lemmatizer'): 'spacy_ind',
                _tr('wl_settings_global', 'spaCy - Irish lemmatizer'): 'spacy_gle',
                _tr('wl_settings_global', 'spaCy - Italian lemmatizer'): 'spacy_ita',
                _tr('wl_settings_global', 'spaCy - Japanese lemmatizer'): 'spacy_jpn',
                _tr('wl_settings_global', 'spaCy - Korean lemmatizer'): 'spacy_kor',
                _tr('wl_settings_global', 'spaCy - Lithuanian lemmatizer'): 'spacy_lit',
                _tr('wl_settings_global', 'spaCy - Luxembourgish lemmatizer'): 'spacy_ltz',
                _tr('wl_settings_global', 'spaCy - Macedonian lemmatizer'): 'spacy_mkd',
                _tr('wl_settings_global', 'spaCy - Norwegian (Bokmål) lemmatizer'): 'spacy_nob',
                _tr('wl_settings_global', 'spaCy - Persian lemmatizer'): 'spacy_fas',
                _tr('wl_settings_global', 'spaCy - Polish lemmatizer'): 'spacy_pol',
                _tr('wl_settings_global', 'spaCy - Portuguese lemmatizer'): 'spacy_por',
                _tr('wl_settings_global', 'spaCy - Romanian lemmatizer'): 'spacy_ron',
                _tr('wl_settings_global', 'spaCy - Russian lemmatizer'): 'spacy_rus',
                _tr('wl_settings_global', 'spaCy - Serbian (Cyrillic script) lemmatizer'): 'spacy_srp',
                _tr('wl_settings_global', 'spaCy - Slovene lemmatizer'): 'spacy_slv',
                _tr('wl_settings_global', 'spaCy - Spanish lemmatizer'): 'spacy_spa',
                _tr('wl_settings_global', 'spaCy - Swedish lemmatizer'): 'spacy_swe',
                _tr('wl_settings_global', 'spaCy - Tagalog lemmatizer'): 'spacy_tgl',
                _tr('wl_settings_global', 'spaCy - Turkish lemmatizer'): 'spacy_tur',
                _tr('wl_settings_global', 'spaCy - Ukrainian lemmatizer'): 'spacy_ukr',
                _tr('wl_settings_global', 'spaCy - Urdu lemmatizer'): 'spacy_urd',

                _tr('wl_settings_global', 'Stanza - Afrikaans lemmatizer'): 'stanza_afr',
                _tr('wl_settings_global', 'Stanza - Arabic lemmatizer'): 'stanza_ara',
                _tr('wl_settings_global', 'Stanza - Armenian (Classical) lemmatizer'): 'stanza_xcl',
                _tr('wl_settings_global', 'Stanza - Armenian (Eastern) lemmatizer'): 'stanza_hye',
                _tr('wl_settings_global', 'Stanza - Armenian (Western) lemmatizer'): 'stanza_hyw',
                _tr('wl_settings_global', 'Stanza - Basque lemmatizer'): 'stanza_eus',
                _tr('wl_settings_global', 'Stanza - Belarusian lemmatizer'): 'stanza_bel',
                _tr('wl_settings_global', 'Stanza - Bulgarian lemmatizer'): 'stanza_bul',
                _tr('wl_settings_global', 'Stanza - Buryat (Russia) lemmatizer'): 'stanza_bxr',
                _tr('wl_settings_global', 'Stanza - Catalan lemmatizer'): 'stanza_cat',
                _tr('wl_settings_global', 'Stanza - Chinese (Classical) lemmatizer'): 'stanza_lzh',
                _tr('wl_settings_global', 'Stanza - Chinese (Simplified) lemmatizer'): 'stanza_zho_cn',
                _tr('wl_settings_global', 'Stanza - Chinese (Traditional) lemmatizer'): 'stanza_zho_tw',
                _tr('wl_settings_global', 'Stanza - Church Slavonic (Old) lemmatizer'): 'stanza_chu',
                _tr('wl_settings_global', 'Stanza - Coptic lemmatizer'): 'stanza_cop',
                _tr('wl_settings_global', 'Stanza - Croatian lemmatizer'): 'stanza_hrv',
                _tr('wl_settings_global', 'Stanza - Czech lemmatizer'): 'stanza_ces',
                _tr('wl_settings_global', 'Stanza - Danish lemmatizer'): 'stanza_dan',
                _tr('wl_settings_global', 'Stanza - Dutch lemmatizer'): 'stanza_nld',
                _tr('wl_settings_global', 'Stanza - English lemmatizer'): 'stanza_eng',
                _tr('wl_settings_global', 'Stanza - English (Old) lemmatizer'): 'stanza_ang',
                _tr('wl_settings_global', 'Stanza - Erzya lemmatizer'): 'stanza_myv',
                _tr('wl_settings_global', 'Stanza - Estonian lemmatizer'): 'stanza_est',
                _tr('wl_settings_global', 'Stanza - Finnish lemmatizer'): 'stanza_fin',
                _tr('wl_settings_global', 'Stanza - French lemmatizer'): 'stanza_fra',
                _tr('wl_settings_global', 'Stanza - French (Old) lemmatizer'): 'stanza_fro',
                _tr('wl_settings_global', 'Stanza - Galician lemmatizer'): 'stanza_glg',
                _tr('wl_settings_global', 'Stanza - German lemmatizer'): 'stanza_deu',
                _tr('wl_settings_global', 'Stanza - Gothic lemmatizer'): 'stanza_got',
                _tr('wl_settings_global', 'Stanza - Greek (Ancient) lemmatizer'): 'stanza_grc',
                _tr('wl_settings_global', 'Stanza - Greek (Modern) lemmatizer'): 'stanza_ell',
                _tr('wl_settings_global', 'Stanza - Hebrew (Ancient) lemmatizer'): 'stanza_hbo',
                _tr('wl_settings_global', 'Stanza - Hebrew (Modern) lemmatizer'): 'stanza_heb',
                _tr('wl_settings_global', 'Stanza - Hindi lemmatizer'): 'stanza_hin',
                _tr('wl_settings_global', 'Stanza - Hungarian lemmatizer'): 'stanza_hun',
                _tr('wl_settings_global', 'Stanza - Icelandic lemmatizer'): 'stanza_isl',
                _tr('wl_settings_global', 'Stanza - Indonesian lemmatizer'): 'stanza_ind',
                _tr('wl_settings_global', 'Stanza - Irish lemmatizer'): 'stanza_gle',
                _tr('wl_settings_global', 'Stanza - Italian lemmatizer'): 'stanza_ita',
                _tr('wl_settings_global', 'Stanza - Japanese lemmatizer'): 'stanza_jpn',
                _tr('wl_settings_global', 'Stanza - Kazakh lemmatizer'): 'stanza_kaz',
                _tr('wl_settings_global', 'Stanza - Korean lemmatizer'): 'stanza_kor',
                _tr('wl_settings_global', 'Stanza - Kurdish (Kurmanji) lemmatizer'): 'stanza_kmr',
                _tr('wl_settings_global', 'Stanza - Kyrgyz lemmatizer'): 'stanza_kir',
                _tr('wl_settings_global', 'Stanza - Latin lemmatizer'): 'stanza_lat',
                _tr('wl_settings_global', 'Stanza - Latvian lemmatizer'): 'stanza_lav',
                _tr('wl_settings_global', 'Stanza - Ligurian lemmatizer'): 'stanza_lij',
                _tr('wl_settings_global', 'Stanza - Lithuanian lemmatizer'): 'stanza_lit',
                _tr('wl_settings_global', 'Stanza - Manx lemmatizer'): 'stanza_glv',
                _tr('wl_settings_global', 'Stanza - Marathi lemmatizer'): 'stanza_mar',
                _tr('wl_settings_global', 'Stanza - Nigerian Pidgin lemmatizer'): 'stanza_pcm',
                _tr('wl_settings_global', 'Stanza - Norwegian (Bokmål) lemmatizer'): 'stanza_nob',
                _tr('wl_settings_global', 'Stanza - Norwegian (Nynorsk) lemmatizer'): 'stanza_nno',
                _tr('wl_settings_global', 'Stanza - Persian lemmatizer'): 'stanza_fas',
                _tr('wl_settings_global', 'Stanza - Polish lemmatizer'): 'stanza_pol',
                _tr('wl_settings_global', 'Stanza - Pomak lemmatizer'): 'stanza_qpm',
                _tr('wl_settings_global', 'Stanza - Portuguese lemmatizer'): 'stanza_por',
                _tr('wl_settings_global', 'Stanza - Romanian lemmatizer'): 'stanza_ron',
                _tr('wl_settings_global', 'Stanza - Russian lemmatizer'): 'stanza_rus',
                _tr('wl_settings_global', 'Stanza - Russian (Old) lemmatizer'): 'stanza_orv',
                _tr('wl_settings_global', 'Stanza - Sámi (Northern) lemmatizer'): 'stanza_sme',
                _tr('wl_settings_global', 'Stanza - Sanskrit lemmatizer'): 'stanza_san',
                _tr('wl_settings_global', 'Stanza - Scottish Gaelic lemmatizer'): 'stanza_gla',
                _tr('wl_settings_global', 'Stanza - Serbian (Latin script) lemmatizer'): 'stanza_srp_latn',
                _tr('wl_settings_global', 'Stanza - Slovak lemmatizer'): 'stanza_slk',
                _tr('wl_settings_global', 'Stanza - Slovene lemmatizer'): 'stanza_slv',
                _tr('wl_settings_global', 'Stanza - Sorbian (Upper) lemmatizer'): 'stanza_hsb',
                _tr('wl_settings_global', 'Stanza - Spanish lemmatizer'): 'stanza_spa',
                _tr('wl_settings_global', 'Stanza - Swedish lemmatizer'): 'stanza_swe',
                _tr('wl_settings_global', 'Stanza - Tamil lemmatizer'): 'stanza_tam',
                _tr('wl_settings_global', 'Stanza - Turkish lemmatizer'): 'stanza_tur',
                _tr('wl_settings_global', 'Stanza - Ukrainian lemmatizer'): 'stanza_ukr',
                _tr('wl_settings_global', 'Stanza - Urdu lemmatizer'): 'stanza_urd',
                _tr('wl_settings_global', 'Stanza - Uyghur lemmatizer'): 'stanza_uig',
                _tr('wl_settings_global', 'Stanza - Welsh lemmatizer'): 'stanza_cym',
                _tr('wl_settings_global', 'Stanza - Wolof lemmatizer'): 'stanza_wol',

                _tr('wl_settings_global', 'SudachiPy - Japanese lemmatizer'): 'sudachipy_jpn'
            },

            'stop_word_lists': {
                _tr('wl_settings_global', 'LaoNLP - Lao stop word list'): 'laonlp_lao',

                _tr('wl_settings_global', 'NLTK - Arabic stop word list'): 'nltk_ara',
                _tr('wl_settings_global', 'NLTK - Azerbaijani stop word list'): 'nltk_aze',
                _tr('wl_settings_global', 'NLTK - Basque stop word list'): 'nltk_eus',
                _tr('wl_settings_global', 'NLTK - Bengali stop word list'): 'nltk_ben',
                _tr('wl_settings_global', 'NLTK - Catalan stop word list'): 'nltk_cat',
                _tr('wl_settings_global', 'NLTK - Chinese (Simplified) stop word list'): 'nltk_zho_cn',
                _tr('wl_settings_global', 'NLTK - Chinese (Traditional) stop word list'): 'nltk_zho_tw',
                _tr('wl_settings_global', 'NLTK - Danish stop word list'): 'nltk_dan',
                _tr('wl_settings_global', 'NLTK - Dutch stop word list'): 'nltk_nld',
                _tr('wl_settings_global', 'NLTK - English stop word list'): 'nltk_eng',
                _tr('wl_settings_global', 'NLTK - Finnish stop word list'): 'nltk_fin',
                _tr('wl_settings_global', 'NLTK - French stop word list'): 'nltk_fra',
                _tr('wl_settings_global', 'NLTK - German stop word list'): 'nltk_deu',
                _tr('wl_settings_global', 'NLTK - Greek (Modern) stop word list'): 'nltk_ell',
                _tr('wl_settings_global', 'NLTK - Hebrew (Modern) stop word list'): 'nltk_heb',
                _tr('wl_settings_global', 'NLTK - Hungarian stop word list'): 'nltk_hun',
                _tr('wl_settings_global', 'NLTK - Indonesian stop word list'): 'nltk_ind',
                _tr('wl_settings_global', 'NLTK - Italian stop word list'): 'nltk_ita',
                _tr('wl_settings_global', 'NLTK - Kazakh stop word list'): 'nltk_kaz',
                _tr('wl_settings_global', 'NLTK - Nepali stop word list'): 'nltk_nep',
                _tr('wl_settings_global', 'NLTK - Norwegian (Bokmål) stop word list'): 'nltk_nob',
                _tr('wl_settings_global', 'NLTK - Portuguese stop word list'): 'nltk_por',
                _tr('wl_settings_global', 'NLTK - Romanian stop word list'): 'nltk_ron',
                _tr('wl_settings_global', 'NLTK - Russian stop word list'): 'nltk_rus',
                _tr('wl_settings_global', 'NLTK - Slovene stop word list'): 'nltk_slv',
                _tr('wl_settings_global', 'NLTK - Spanish stop word list'): 'nltk_spa',
                _tr('wl_settings_global', 'NLTK - Swedish stop word list'): 'nltk_swe',
                _tr('wl_settings_global', 'NLTK - Tajik stop word list'): 'nltk_tgk',
                _tr('wl_settings_global', 'NLTK - Turkish stop word list'): 'nltk_tur',

                _tr('wl_settings_global', 'PyThaiNLP - Thai stop word list'): 'pythainlp_tha',

                _tr('wl_settings_global', 'Custom stop word list'): 'custom',
            },

            'dependency_parsers':{
                _tr('wl_settings_global', 'spaCy - Catalan dependency parser'): 'spacy_cat',
                _tr('wl_settings_global', 'spaCy - Chinese dependency parser'): 'spacy_zho',
                _tr('wl_settings_global', 'spaCy - Croatian dependency parser'): 'spacy_hrv',
                _tr('wl_settings_global', 'spaCy - Danish dependency parser'): 'spacy_dan',
                _tr('wl_settings_global', 'spaCy - Dutch dependency parser'): 'spacy_nld',
                _tr('wl_settings_global', 'spaCy - English dependency parser'): 'spacy_eng',
                _tr('wl_settings_global', 'spaCy - Finnish dependency parser'): 'spacy_fin',
                _tr('wl_settings_global', 'spaCy - French dependency parser'): 'spacy_fra',
                _tr('wl_settings_global', 'spaCy - German dependency parser'): 'spacy_deu',
                _tr('wl_settings_global', 'spaCy - Greek (Modern) dependency parser'): 'spacy_ell',
                _tr('wl_settings_global', 'spaCy - Italian dependency parser'): 'spacy_ita',
                _tr('wl_settings_global', 'spaCy - Japanese dependency parser'): 'spacy_jpn',
                _tr('wl_settings_global', 'spaCy - Korean dependency parser'): 'spacy_kor',
                _tr('wl_settings_global', 'spaCy - Lithuanian dependency parser'): 'spacy_lit',
                _tr('wl_settings_global', 'spaCy - Macedonian dependency parser'): 'spacy_mkd',
                _tr('wl_settings_global', 'spaCy - Norwegian (Bokmål) dependency parser'): 'spacy_nob',
                _tr('wl_settings_global', 'spaCy - Polish dependency parser'): 'spacy_pol',
                _tr('wl_settings_global', 'spaCy - Portuguese dependency parser'): 'spacy_por',
                _tr('wl_settings_global', 'spaCy - Romanian dependency parser'): 'spacy_ron',
                _tr('wl_settings_global', 'spaCy - Russian dependency parser'): 'spacy_rus',
                _tr('wl_settings_global', 'spaCy - Slovene dependency parser'): 'spacy_slv',
                _tr('wl_settings_global', 'spaCy - Spanish dependency parser'): 'spacy_spa',
                _tr('wl_settings_global', 'spaCy - Swedish dependency parser'): 'spacy_swe',
                _tr('wl_settings_global', 'spaCy - Ukrainian dependency parser'): 'spacy_ukr',

                _tr('wl_settings_global', 'Stanza - Afrikaans dependency parser'): 'stanza_afr',
                _tr('wl_settings_global', 'Stanza - Arabic dependency parser'): 'stanza_ara',
                _tr('wl_settings_global', 'Stanza - Armenian (Classical) dependency parser'): 'stanza_xcl',
                _tr('wl_settings_global', 'Stanza - Armenian (Eastern) dependency parser'): 'stanza_hye',
                _tr('wl_settings_global', 'Stanza - Armenian (Western) dependency parser'): 'stanza_hyw',
                _tr('wl_settings_global', 'Stanza - Basque dependency parser'): 'stanza_eus',
                _tr('wl_settings_global', 'Stanza - Belarusian dependency parser'): 'stanza_bel',
                _tr('wl_settings_global', 'Stanza - Bulgarian dependency parser'): 'stanza_bul',
                _tr('wl_settings_global', 'Stanza - Buryat (Russia) dependency parser'): 'stanza_bxr',
                _tr('wl_settings_global', 'Stanza - Catalan dependency parser'): 'stanza_cat',
                _tr('wl_settings_global', 'Stanza - Chinese (Classical) dependency parser'): 'stanza_lzh',
                _tr('wl_settings_global', 'Stanza - Chinese (Simplified) dependency parser'): 'stanza_zho_cn',
                _tr('wl_settings_global', 'Stanza - Chinese (Traditional) dependency parser'): 'stanza_zho_tw',
                _tr('wl_settings_global', 'Stanza - Church Slavonic (Old) dependency parser'): 'stanza_chu',
                _tr('wl_settings_global', 'Stanza - Coptic dependency parser'): 'stanza_cop',
                _tr('wl_settings_global', 'Stanza - Croatian dependency parser'): 'stanza_hrv',
                _tr('wl_settings_global', 'Stanza - Czech dependency parser'): 'stanza_ces',
                _tr('wl_settings_global', 'Stanza - Danish dependency parser'): 'stanza_dan',
                _tr('wl_settings_global', 'Stanza - Dutch dependency parser'): 'stanza_nld',
                _tr('wl_settings_global', 'Stanza - English dependency parser'): 'stanza_eng',
                _tr('wl_settings_global', 'Stanza - English (Old) dependency parser'): 'stanza_ang',
                _tr('wl_settings_global', 'Stanza - Erzya dependency parser'): 'stanza_myv',
                _tr('wl_settings_global', 'Stanza - Estonian dependency parser'): 'stanza_est',
                _tr('wl_settings_global', 'Stanza - Faroese dependency parser'): 'stanza_fao',
                _tr('wl_settings_global', 'Stanza - Finnish dependency parser'): 'stanza_fin',
                _tr('wl_settings_global', 'Stanza - French dependency parser'): 'stanza_fra',
                _tr('wl_settings_global', 'Stanza - French (Old) dependency parser'): 'stanza_fro',
                _tr('wl_settings_global', 'Stanza - Galician dependency parser'): 'stanza_glg',
                _tr('wl_settings_global', 'Stanza - German dependency parser'): 'stanza_deu',
                _tr('wl_settings_global', 'Stanza - Gothic dependency parser'): 'stanza_got',
                _tr('wl_settings_global', 'Stanza - Greek (Ancient) dependency parser'): 'stanza_grc',
                _tr('wl_settings_global', 'Stanza - Greek (Modern) dependency parser'): 'stanza_ell',
                _tr('wl_settings_global', 'Stanza - Hebrew (Ancient) dependency parser'): 'stanza_hbo',
                _tr('wl_settings_global', 'Stanza - Hebrew (Modern) dependency parser'): 'stanza_heb',
                _tr('wl_settings_global', 'Stanza - Hindi dependency parser'): 'stanza_hin',
                _tr('wl_settings_global', 'Stanza - Hungarian dependency parser'): 'stanza_hun',
                _tr('wl_settings_global', 'Stanza - Icelandic dependency parser'): 'stanza_isl',
                _tr('wl_settings_global', 'Stanza - Indonesian dependency parser'): 'stanza_ind',
                _tr('wl_settings_global', 'Stanza - Irish dependency parser'): 'stanza_gle',
                _tr('wl_settings_global', 'Stanza - Italian dependency parser'): 'stanza_ita',
                _tr('wl_settings_global', 'Stanza - Japanese dependency parser'): 'stanza_jpn',
                _tr('wl_settings_global', 'Stanza - Kazakh dependency parser'): 'stanza_kaz',
                _tr('wl_settings_global', 'Stanza - Korean dependency parser'): 'stanza_kor',
                _tr('wl_settings_global', 'Stanza - Kurdish (Kurmanji) dependency parser'): 'stanza_kmr',
                _tr('wl_settings_global', 'Stanza - Kyrgyz dependency parser'): 'stanza_kir',
                _tr('wl_settings_global', 'Stanza - Latin dependency parser'): 'stanza_lat',
                _tr('wl_settings_global', 'Stanza - Latvian dependency parser'): 'stanza_lav',
                _tr('wl_settings_global', 'Stanza - Ligurian dependency parser'): 'stanza_lij',
                _tr('wl_settings_global', 'Stanza - Lithuanian dependency parser'): 'stanza_lit',
                _tr('wl_settings_global', 'Stanza - Maltese dependency parser'): 'stanza_mlt',
                _tr('wl_settings_global', 'Stanza - Manx dependency parser'): 'stanza_glv',
                _tr('wl_settings_global', 'Stanza - Marathi dependency parser'): 'stanza_mar',
                _tr('wl_settings_global', 'Stanza - Nigerian Pidgin dependency parser'): 'stanza_pcm',
                _tr('wl_settings_global', 'Stanza - Norwegian (Bokmål) dependency parser'): 'stanza_nob',
                _tr('wl_settings_global', 'Stanza - Norwegian (Nynorsk) dependency parser'): 'stanza_nno',
                _tr('wl_settings_global', 'Stanza - Persian dependency parser'): 'stanza_fas',
                _tr('wl_settings_global', 'Stanza - Polish dependency parser'): 'stanza_pol',
                _tr('wl_settings_global', 'Stanza - Pomak dependency parser'): 'stanza_qpm',
                _tr('wl_settings_global', 'Stanza - Portuguese dependency parser'): 'stanza_por',
                _tr('wl_settings_global', 'Stanza - Romanian dependency parser'): 'stanza_ron',
                _tr('wl_settings_global', 'Stanza - Russian dependency parser'): 'stanza_rus',
                _tr('wl_settings_global', 'Stanza - Russian (Old) dependency parser'): 'stanza_orv',
                _tr('wl_settings_global', 'Stanza - Sámi (Northern) dependency parser'): 'stanza_sme',
                _tr('wl_settings_global', 'Stanza - Sanskrit dependency parser'): 'stanza_san',
                _tr('wl_settings_global', 'Stanza - Scottish Gaelic dependency parser'): 'stanza_gla',
                _tr('wl_settings_global', 'Stanza - Serbian (Latin script) dependency parser'): 'stanza_srp_latn',
                _tr('wl_settings_global', 'Stanza - Sindhi dependency parser'): 'stanza_snd',
                _tr('wl_settings_global', 'Stanza - Slovak dependency parser'): 'stanza_slk',
                _tr('wl_settings_global', 'Stanza - Slovene dependency parser'): 'stanza_slv',
                _tr('wl_settings_global', 'Stanza - Sorbian (Upper) dependency parser'): 'stanza_hsb',
                _tr('wl_settings_global', 'Stanza - Spanish dependency parser'): 'stanza_spa',
                _tr('wl_settings_global', 'Stanza - Swedish dependency parser'): 'stanza_swe',
                _tr('wl_settings_global', 'Stanza - Tamil dependency parser'): 'stanza_tam',
                _tr('wl_settings_global', 'Stanza - Telugu dependency parser'): 'stanza_tel',
                _tr('wl_settings_global', 'Stanza - Turkish dependency parser'): 'stanza_tur',
                _tr('wl_settings_global', 'Stanza - Ukrainian dependency parser'): 'stanza_ukr',
                _tr('wl_settings_global', 'Stanza - Urdu dependency parser'): 'stanza_urd',
                _tr('wl_settings_global', 'Stanza - Uyghur dependency parser'): 'stanza_uig',
                _tr('wl_settings_global', 'Stanza - Vietnamese dependency parser'): 'stanza_vie',
                _tr('wl_settings_global', 'Stanza - Welsh dependency parser'): 'stanza_cym',
                _tr('wl_settings_global', 'Stanza - Wolof dependency parser'): 'stanza_wol'
            },

            'sentiment_analyzers': {
                _tr('wl_settings_global', 'Stanza - Chinese (Simplified) sentiment analyzer'): 'stanza_zho_cn',
                _tr('wl_settings_global', 'Stanza - German sentiment analyzer'): 'stanza_deu',
                _tr('wl_settings_global', 'Stanza - English sentiment analyzer'): 'stanza_eng',
                _tr('wl_settings_global', 'Stanza - Marathi sentiment analyzer'): 'stanza_mar',
                _tr('wl_settings_global', 'Stanza - Spanish sentiment analyzer'): 'stanza_spa',
                _tr('wl_settings_global', 'Stanza - Vietnamese sentiment analyzer'): 'stanza_vie',

                _tr('wl_settings_global', 'Underthesea - Vietnamese sentiment analyzer'): 'underthesea_vie',

                _tr('wl_settings_global', 'VADER - Afrikaans sentiment analyzer'): 'vader_afr',
                _tr('wl_settings_global', 'VADER - Albanian sentiment analyzer'): 'vader_sqi',
                _tr('wl_settings_global', 'VADER - Amharic sentiment analyzer'): 'vader_amh',
                _tr('wl_settings_global', 'VADER - Arabic sentiment analyzer'): 'vader_ara',
                _tr('wl_settings_global', 'VADER - Armenian sentiment analyzer'): 'vader_hye',
                _tr('wl_settings_global', 'VADER - Assamese sentiment analyzer'): 'vader_asm',
                _tr('wl_settings_global', 'VADER - Azerbaijani sentiment analyzer'): 'vader_aze',
                _tr('wl_settings_global', 'VADER - Basque sentiment analyzer'): 'vader_eus',
                _tr('wl_settings_global', 'VADER - Belarusian sentiment analyzer'): 'vader_bel',
                _tr('wl_settings_global', 'VADER - Bengali sentiment analyzer'): 'vader_ben',
                _tr('wl_settings_global', 'VADER - Bulgarian sentiment analyzer'): 'vader_bul',
                _tr('wl_settings_global', 'VADER - Burmese sentiment analyzer'): 'vader_mya',
                _tr('wl_settings_global', 'VADER - Catalan sentiment analyzer'): 'vader_cat',
                _tr('wl_settings_global', 'VADER - Chinese (Simplified) sentiment analyzer'): 'vader_zho_cn',
                _tr('wl_settings_global', 'VADER - Chinese (Traditional) sentiment analyzer'): 'vader_zho_tw',
                _tr('wl_settings_global', 'VADER - Croatian sentiment analyzer'): 'vader_hrv',
                _tr('wl_settings_global', 'VADER - Czech sentiment analyzer'): 'vader_ces',
                _tr('wl_settings_global', 'VADER - Danish sentiment analyzer'): 'vader_dan',
                _tr('wl_settings_global', 'VADER - Dutch sentiment analyzer'): 'vader_nld',
                _tr('wl_settings_global', 'VADER - English sentiment analyzer'): 'vader_eng',
                _tr('wl_settings_global', 'VADER - Esperanto sentiment analyzer'): 'vader_epo',
                _tr('wl_settings_global', 'VADER - Estonian sentiment analyzer'): 'vader_est',
                _tr('wl_settings_global', 'VADER - Finnish sentiment analyzer'): 'vader_fin',
                _tr('wl_settings_global', 'VADER - French sentiment analyzer'): 'vader_fra',
                _tr('wl_settings_global', 'VADER - Galician sentiment analyzer'): 'vader_glg',
                _tr('wl_settings_global', 'VADER - Georgian sentiment analyzer'): 'vader_kat',
                _tr('wl_settings_global', 'VADER - German sentiment analyzer'): 'vader_deu',
                _tr('wl_settings_global', 'VADER - Greek (Modern) sentiment analyzer'): 'vader_ell',
                _tr('wl_settings_global', 'VADER - Gujarati sentiment analyzer'): 'vader_guj',
                _tr('wl_settings_global', 'VADER - Hebrew (Modern) sentiment analyzer'): 'vader_heb',
                _tr('wl_settings_global', 'VADER - Hindi sentiment analyzer'): 'vader_hin',
                _tr('wl_settings_global', 'VADER - Hungarian sentiment analyzer'): 'vader_hun',
                _tr('wl_settings_global', 'VADER - Icelandic sentiment analyzer'): 'vader_isl',
                _tr('wl_settings_global', 'VADER - Indonesian sentiment analyzer'): 'vader_ind',
                _tr('wl_settings_global', 'VADER - Irish sentiment analyzer'): 'vader_gle',
                _tr('wl_settings_global', 'VADER - Italian sentiment analyzer'): 'vader_ita',
                _tr('wl_settings_global', 'VADER - Japanese sentiment analyzer'): 'vader_jpn',
                _tr('wl_settings_global', 'VADER - Kannada sentiment analyzer'): 'vader_kan',
                _tr('wl_settings_global', 'VADER - Kazakh sentiment analyzer'): 'vader_kaz',
                _tr('wl_settings_global', 'VADER - Khmer sentiment analyzer'): 'vader_khm',
                _tr('wl_settings_global', 'VADER - Korean sentiment analyzer'): 'vader_kor',
                _tr('wl_settings_global', 'VADER - Kurdish (Kurmanji) sentiment analyzer'): 'vader_kmr',
                _tr('wl_settings_global', 'VADER - Kyrgyz sentiment analyzer'): 'vader_kir',
                _tr('wl_settings_global', 'VADER - Lao sentiment analyzer'): 'vader_lao',
                _tr('wl_settings_global', 'VADER - Latin sentiment analyzer'): 'vader_lat',
                _tr('wl_settings_global', 'VADER - Latvian sentiment analyzer'): 'vader_lav',
                _tr('wl_settings_global', 'VADER - Lithuanian sentiment analyzer'): 'vader_lit',
                _tr('wl_settings_global', 'VADER - Luganda sentiment analyzer'): 'vader_lug',
                _tr('wl_settings_global', 'VADER - Luxembourgish sentiment analyzer'): 'vader_ltz',
                _tr('wl_settings_global', 'VADER - Macedonian sentiment analyzer'): 'vader_mkd',
                _tr('wl_settings_global', 'VADER - Malay sentiment analyzer'): 'vader_msa',
                _tr('wl_settings_global', 'VADER - Malayalam sentiment analyzer'): 'vader_mal',
                _tr('wl_settings_global', 'VADER - Maltese sentiment analyzer'): 'vader_mlt',
                _tr('wl_settings_global', 'VADER - Marathi sentiment analyzer'): 'vader_mar',
                _tr('wl_settings_global', 'VADER - Meitei (Meitei script) sentiment analyzer'): 'vader_mni_mtei',
                _tr('wl_settings_global', 'VADER - Mongolian sentiment analyzer'): 'vader_mon',
                _tr('wl_settings_global', 'VADER - Nepali sentiment analyzer'): 'vader_nep',
                # References:
                #     https://support.google.com/translate/thread/1818911/norwegin-translate-is-in-bokm%C3%A5l-or-nynorsk?hl=en
                #     https://www.quora.com/How-does-Google-Translate-do-with-Norwegian-language-as-Norwegian-has-two-official-forms
                _tr('wl_settings_global', 'VADER - Norwegian (Bokmål) sentiment analyzer'): 'vader_nob',
                _tr('wl_settings_global', 'VADER - Odia sentiment analyzer'): 'vader_ori',
                _tr('wl_settings_global', 'VADER - Persian sentiment analyzer'): 'vader_fas',
                _tr('wl_settings_global', 'VADER - Polish sentiment analyzer'): 'vader_pol',
                _tr('wl_settings_global', 'VADER - Portuguese sentiment analyzer'): 'vader_por',
                _tr('wl_settings_global', 'VADER - Punjabi (Gurmukhi script) sentiment analyzer'): 'vader_pan_guru',
                _tr('wl_settings_global', 'VADER - Romanian sentiment analyzer'): 'vader_ron',
                _tr('wl_settings_global', 'VADER - Russian sentiment analyzer'): 'vader_rus',
                _tr('wl_settings_global', 'VADER - Sanskrit sentiment analyzer'): 'vader_san',
                _tr('wl_settings_global', 'VADER - Scottish Gaelic sentiment analyzer'): 'vader_gla',
                _tr('wl_settings_global', 'VADER - Serbian (Cyrillic script) sentiment analyzer'): 'vader_srp_cyrl',
                _tr('wl_settings_global', 'VADER - Sindhi sentiment analyzer'): 'vader_snd',
                _tr('wl_settings_global', 'VADER - Sinhala sentiment analyzer'): 'vader_sin',
                _tr('wl_settings_global', 'VADER - Slovak sentiment analyzer'): 'vader_slk',
                _tr('wl_settings_global', 'VADER - Slovene sentiment analyzer'): 'vader_slv',
                _tr('wl_settings_global', 'VADER - Spanish sentiment analyzer'): 'vader_spa',
                _tr('wl_settings_global', 'VADER - Swahili sentiment analyzer'): 'vader_swa',
                _tr('wl_settings_global', 'VADER - Swedish sentiment analyzer'): 'vader_swe',
                _tr('wl_settings_global', 'VADER - Tagalog sentiment analyzer'): 'vader_tgl',
                _tr('wl_settings_global', 'VADER - Tajik sentiment analyzer'): 'vader_tgk',
                _tr('wl_settings_global', 'VADER - Tamil sentiment analyzer'): 'vader_tam',
                _tr('wl_settings_global', 'VADER - Tatar sentiment analyzer'): 'vader_tat',
                _tr('wl_settings_global', 'VADER - Telugu sentiment analyzer'): 'vader_tel',
                _tr('wl_settings_global', 'VADER - Thai sentiment analyzer'): 'vader_tha',
                _tr('wl_settings_global', 'VADER - Tigrinya sentiment analyzer'): 'vader_tir',
                _tr('wl_settings_global', 'VADER - Turkish sentiment analyzer'): 'vader_tur',
                _tr('wl_settings_global', 'VADER - Ukrainian sentiment analyzer'): 'vader_ukr',
                _tr('wl_settings_global', 'VADER - Urdu sentiment analyzer'): 'vader_urd',
                _tr('wl_settings_global', 'VADER - Uyghur sentiment analyzer'): 'vader_uig',
                _tr('wl_settings_global', 'VADER - Welsh sentiment analyzer'): 'vader_cym',
                _tr('wl_settings_global', 'VADER - Yoruba sentiment analyzer'): 'vader_yor',
                _tr('wl_settings_global', 'VADER - Zulu sentiment analyzer'): 'vader_zul'
            }
        },

        'sentence_tokenizers': {
            'afr': [
                'spacy_sentencizer',
                'stanza_afr'
            ],

            'ara': [
                'spacy_sentencizer',
                'stanza_ara'
            ],

            'xcl': [
                'spacy_sentencizer',
                'stanza_xcl'
            ],
            'hye': [
                'spacy_sentencizer',
                'stanza_hye'
            ],
            'hyw': [
                'spacy_sentencizer',
                'stanza_hyw'
            ],

            'eus': [
                'spacy_sentencizer',
                'stanza_eus'
            ],

            'bel': [
                'spacy_sentencizer',
                'stanza_bel'
            ],

            'bul': [
                'spacy_sentencizer',
                'stanza_bul'
            ],

            'mya': [
                'spacy_sentencizer',
                'stanza_mya'
            ],

            'bxr': [
                'spacy_sentencizer',
                'stanza_bxr'
            ],

            'cat': [
                'spacy_dependency_parser_cat',
                'spacy_sentencizer',
                'stanza_cat'
            ],

            'lzh': [
                'spacy_sentencizer',
                'stanza_lzh'
            ],
            'zho_cn': [
                'spacy_dependency_parser_zho',
                'spacy_sentencizer',
                'stanza_zho_cn'
            ],
            'zho_tw': [
                'spacy_dependency_parser_zho',
                'spacy_sentencizer',
                'stanza_zho_tw'
            ],

            'chu': [
                'spacy_sentencizer',
                'stanza_chu'
            ],

            'cop': [
                'spacy_sentencizer',
                'stanza_cop'
            ],

            'hrv': [
                'spacy_dependency_parser_hrv',
                'spacy_sentence_recognizer_hrv',
                'spacy_sentencizer',
                'stanza_hrv'
            ],

            'ces': [
                'nltk_punkt_ces',
                'spacy_sentencizer',
                'stanza_ces'
            ],

            'dan': [
                'nltk_punkt_dan',
                'spacy_dependency_parser_dan',
                'spacy_sentencizer',
                'stanza_dan'
            ],

            'nld': [
                'nltk_punkt_nld',
                'spacy_dependency_parser_nld',
                'spacy_sentence_recognizer_nld',
                'spacy_sentencizer',
                'stanza_nld'
            ],

            'ang': [
                'spacy_sentencizer',
                'stanza_ang'
            ],
            'eng_gb': [
                'nltk_punkt_eng',
                'spacy_dependency_parser_eng',
                'spacy_sentencizer',
                'stanza_eng'
            ],
            'eng_us': [
                'nltk_punkt_eng',
                'spacy_dependency_parser_eng',
                'spacy_sentencizer',
                'stanza_eng'
            ],

            'myv': [
                'spacy_sentencizer',
                'stanza_myv'
            ],

            'est': [
                'nltk_punkt_est',
                'spacy_sentencizer',
                'stanza_est'
            ],

            'fao': [
                'spacy_sentencizer',
                'stanza_fao'
            ],

            'fin': [
                'nltk_punkt_fin',
                'spacy_dependency_parser_fin',
                'spacy_sentence_recognizer_fin',
                'spacy_sentencizer',
                'stanza_fin'
            ],

            'fra': [
                'nltk_punkt_fra',
                'spacy_dependency_parser_fra',
                'spacy_sentencizer',
                'stanza_fra'
            ],
            'fro': [
                'spacy_sentencizer',
                'stanza_fro'
            ],

            'glg': [
                'spacy_sentencizer',
                'stanza_glg'
            ],

            'deu_at': [
                'nltk_punkt_deu',
                'spacy_dependency_parser_deu',
                'spacy_sentencizer',
                'stanza_deu'
            ],
            'deu_de': [
                'nltk_punkt_deu',
                'spacy_dependency_parser_deu',
                'spacy_sentencizer',
                'stanza_deu'
            ],
            'deu_ch': [
                'nltk_punkt_deu',
                'spacy_dependency_parser_deu',
                'spacy_sentencizer',
                'stanza_deu'
            ],

            'got': [
                'spacy_sentencizer',
                'stanza_got'
            ],

            'grc': [
                'spacy_sentencizer',
                'stanza_grc'
            ],
            'ell': [
                'nltk_punkt_ell',
                'spacy_dependency_parser_ell',
                'spacy_sentence_recognizer_ell',
                'spacy_sentencizer',
                'stanza_ell'
            ],

            'hbo': [
                'spacy_sentencizer',
                'stanza_hbo'
            ],
            'heb': [
                'spacy_sentencizer',
                'stanza_heb'
            ],

            'hin': [
                'spacy_sentencizer',
                'stanza_hin'
            ],

            'hun': [
                'spacy_sentencizer',
                'stanza_hun'
            ],

            'isl': [
                'spacy_sentencizer',
                'stanza_isl'
            ],

            'ind': [
                'spacy_sentencizer',
                'stanza_ind'
            ],

            'gle': [
                'spacy_sentencizer',
                'stanza_gle'
            ],

            'ita': [
                'nltk_punkt_ita',
                'spacy_dependency_parser_ita',
                'spacy_sentence_recognizer_ita',
                'spacy_sentencizer',
                'stanza_ita'
            ],

            'jpn': [
                'spacy_dependency_parser_jpn',
                'spacy_sentencizer',
                'stanza_jpn'
            ],

            'khm': ['khmer_nltk_khm'],

            'kaz': [
                'spacy_sentencizer',
                'stanza_kaz'
            ],

            'kor': [
                'spacy_dependency_parser_kor',
                'spacy_sentence_recognizer_kor',
                'spacy_sentencizer',
                'stanza_kor'
            ],

            'kmr': [
                'spacy_sentencizer',
                'stanza_kmr'
            ],

            'kir': [
                'spacy_sentencizer',
                'stanza_kir'
            ],

            'lao': [
                'laonlp_lao',
                'spacy_sentencizer'
            ],

            'lat': [
                'spacy_sentencizer',
                'stanza_lat'
            ],

            'lav': [
                'spacy_sentencizer',
                'stanza_lav'
            ],

            'lij': [
                'spacy_sentencizer',
                'stanza_lij'
            ],

            'lit': [
                'spacy_dependency_parser_lit',
                'spacy_sentence_recognizer_lit',
                'spacy_sentencizer',
                'stanza_lit'
            ],

            'mkd': [
                'spacy_dependency_parser_mkd',
                'spacy_sentence_recognizer_mkd',
                'spacy_sentencizer'
            ],

            'mal': ['spacy_sentencizer'],

            'mlt': [
                'spacy_sentencizer',
                'stanza_mlt'
            ],

            'glv': [
                'spacy_sentencizer',
                'stanza_glv'
            ],

            'mar': [
                'spacy_sentencizer',
                'stanza_mar'
            ],

            'pcm': [
                'spacy_sentencizer',
                'stanza_pcm'
            ],

            'nob': [
                'nltk_punkt_nob',
                'spacy_dependency_parser_nob',
                'spacy_sentence_recognizer_nob',
                'spacy_sentencizer',
                'stanza_nob'
            ],

            'nno': [
                'spacy_sentencizer',
                'stanza_nno'
            ],

            'fas': [
                'spacy_sentencizer',
                'stanza_fas'
            ],

            'pol': [
                'nltk_punkt_pol',
                'spacy_dependency_parser_pol',
                'spacy_sentence_recognizer_pol',
                'spacy_sentencizer',
                'stanza_pol'
            ],

            'qpm': [
                'spacy_sentencizer',
                'stanza_qpm'
            ],

            'por_br': [
                'nltk_punkt_por',
                'spacy_dependency_parser_por',
                'spacy_sentence_recognizer_por',
                'spacy_sentencizer',
                'stanza_por'
            ],
            'por_pt': [
                'nltk_punkt_por',
                'spacy_dependency_parser_por',
                'spacy_sentence_recognizer_por',
                'spacy_sentencizer',
                'stanza_por'
            ],

            'ron': [
                'spacy_dependency_parser_ron',
                'spacy_sentence_recognizer_ron',
                'spacy_sentencizer',
                'stanza_ron'
            ],

            'rus': [
                'nltk_punkt_rus',
                'spacy_dependency_parser_rus',
                'spacy_sentence_recognizer_rus',
                'spacy_sentencizer',
                'stanza_rus'
            ],
            'orv': [
                'spacy_sentencizer',
                'stanza_orv'
            ],

            'sme': [
                'spacy_sentencizer',
                'stanza_sme'
            ],

            'san': [
                'spacy_sentencizer',
                'stanza_san'
            ],

            'gla': [
                'spacy_sentencizer',
                'stanza_gla'
            ],

            'srp_latn': [
                'spacy_sentencizer',
                'stanza_srp_latn'
            ],

            'snd': [
                'spacy_sentencizer',
                'stanza_snd'
            ],

            'slk': [
                'spacy_sentencizer',
                'stanza_slk'
            ],

            'slv': [
                'nltk_punkt_slv',
                'spacy_dependency_parser_slv',
                'spacy_sentencizer',
                'stanza_slv'
            ],

            'hsb': [
                'spacy_sentencizer',
                'stanza_hsb'
            ],

            'spa': [
                'nltk_punkt_spa',
                'spacy_dependency_parser_spa',
                'spacy_sentencizer',
                'stanza_spa'
            ],

            'swe': [
                'nltk_punkt_swe',
                'spacy_dependency_parser_swe',
                'spacy_sentence_recognizer_swe',
                'spacy_sentencizer',
                'stanza_swe'
            ],

            'tam': [
                'spacy_sentencizer',
                'stanza_tam'
            ],

            'tel': [
                'spacy_sentencizer',
                'stanza_tel'
            ],

            'tha': [
                'pythainlp_crfcut',
                'pythainlp_thaisumcut',
                'stanza_tha'
            ],

            'bod': ['botok_bod'],

            'tur': [
                'nltk_punkt_tur',
                'spacy_sentencizer',
                'stanza_tur'
            ],

            'ukr': [
                'spacy_dependency_parser_ukr',
                'spacy_sentencizer',
                'stanza_ukr'
            ],

            'urd': [
                'spacy_sentencizer',
                'stanza_urd'
            ],

            'uig': [
                'spacy_sentencizer',
                'stanza_uig'
            ],

            'vie': [
                'underthesea_vie',
                'stanza_vie'
            ],

            'cym': [
                'spacy_sentencizer',
                'stanza_cym'
            ],

            'wol': [
                'spacy_sentencizer',
                'stanza_wol'
            ],

            'other': [
                'nltk_punkt_eng',
                'spacy_sentencizer',
                'stanza_eng'
            ]
        },

        'word_tokenizers': {
            'afr': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_afr',
                'stanza_afr'
            ],

            'sqi': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_sqi'
            ],

            'amh': ['spacy_amh'],

            'ara': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_ara',
                'stanza_ara'
            ],

            'xcl': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_xcl'
            ],
            'hye': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_hye',
                'stanza_hye'
            ],
            'hyw': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_hyw'
            ],

            'asm': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses'
            ],

            'aze': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_aze'
            ],

            'eus': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_eus',
                'stanza_eus'
            ],

            'ben': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_ben'
            ],

            'bel': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_bel'
            ],

            'bul': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_bul',
                'stanza_bul'
            ],

            'mya': ['stanza_mya'],

            'bxr': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_bxr'
            ],

            'cat': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_cat',
                'stanza_cat'
            ],

            'lzh': ['stanza_lzh'],
            'zho_cn': [
                'pkuseg_zho',
                'spacy_zho',
                'stanza_zho_cn',
                'wordless_zho_char'
            ],
            'zho_tw': [
                'pkuseg_zho',
                'spacy_zho',
                'stanza_zho_tw',
                'wordless_zho_char'
            ],

            'chu': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_chu'
            ],

            'cop': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_cop'
            ],

            'hrv': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_hrv',
                'stanza_hrv'
            ],

            'ces': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_ces',
                'stanza_ces'
            ],

            'dan': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_dan',
                'stanza_dan'
            ],

            'nld': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_nld',
                'stanza_nld'
            ],

            'ang': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_ang'
            ],
            'eng_gb': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_eng',
                'stanza_eng'
            ],
            'eng_us': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_eng',
                'stanza_eng'
            ],

            'myv': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_myv'
            ],

            'est': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_est',
                'stanza_est'
            ],

            'fao': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_fao',
                'stanza_fao'
            ],

            'fin': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_fin',
                'stanza_fin'
            ],

            'fra': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_fra',
                'stanza_fra'
            ],
            'fro': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_fro'
            ],

            'glg': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_glg'
            ],

            'lug': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_lug'
            ],

            'deu_at': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_deu',
                'stanza_deu'
            ],
            'deu_de': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_deu',
                'stanza_deu'
            ],
            'deu_ch': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_deu',
                'stanza_deu'
            ],

            'got': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_got'
            ],

            'grc': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_grc',
                'stanza_grc'
            ],
            'ell': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_ell',
                'stanza_ell'
            ],

            'guj': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_guj'
            ],

            'hbo': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_hbo'
            ],
            'heb': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_heb',
                'stanza_heb'
            ],

            'hin': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_hin',
                'stanza_hin'
            ],

            'hun': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_hun',
                'stanza_hun'
            ],

            'isl': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_isl',
                'stanza_isl'
            ],

            'ind': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_ind',
                'stanza_ind'
            ],

            'gle': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_gle',
                'stanza_gle'
            ],

            'ita': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_ita',
                'stanza_ita'
            ],

            'jpn': [
                'spacy_jpn',
                'stanza_jpn',
                'sudachipy_jpn_split_mode_a', 'sudachipy_jpn_split_mode_b', 'sudachipy_jpn_split_mode_c',
                'wordless_jpn_kanji'
            ],

            'kan': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_kan'
            ],

            'kaz': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_kaz'
            ],

            'khm': ['khmer_nltk_khm'],

            'kor': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'python_mecab_ko_mecab',
                'spacy_kor',
                'stanza_kor'
            ],

            'kmr': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_kmr'
            ],

            'kir': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_kir',
                'stanza_kir'
            ],

            'lao': ['laonlp_lao'],

            'lat': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_lat',
                'stanza_lat'
            ],

            'lav': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_lav',
                'stanza_lav'
            ],

            'lij': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_lij',
                'stanza_lij'
            ],

            'lit': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_lit',
                'stanza_lit'
            ],

            'ltz': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_ltz'
            ],

            'mkd': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_mkd'
            ],

            'msa': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_msa'
            ],

            'mal': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_mal'
            ],

            'mlt': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_mlt'
            ],

            'glv': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_glv'
            ],

            'mar': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_mar',
                'stanza_mar'
            ],

            'pcm': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_pcm'
            ],

            'mni_mtei': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses'
            ],

            'nep': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_nep'
            ],

            'nob': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_nob',
                'stanza_nob'
            ],
            'nno': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_nno',
                'stanza_nno'
            ],

            'ori': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses'
            ],

            'fas': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'spacy_fas',
                'stanza_fas'
            ],

            'pol': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_pol',
                'stanza_pol'
            ],

            'qpm': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_qpm'
            ],

            'por_br': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_por',
                'stanza_por'
            ],
            'por_pt': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_por',
                'stanza_por'
            ],

            'pan_guru': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses'
            ],

            'ron': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_ron',
                'stanza_ron'
            ],

            'rus': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_rus',
                'stanza_rus'
            ],
            'orv': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_orv'
            ],

            'sme': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_sme'
            ],

            'san': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_san',
                'stanza_san'
            ],

            'gla': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_gla'
            ],

            'srp_cyrl': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_srp'
            ],

            'srp_latn': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_srp',
                'stanza_srp_latn'
            ],

            'snd': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_snd'
            ],

            'sin': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_sin'
            ],

            'slk': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_slk',
                'stanza_slk'
            ],

            'slv': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_slv',
                'stanza_slv'
            ],

            'dsb': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_dsb'
            ],

            'hsb': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_hsb',
                'stanza_hsb'
            ],

            'spa': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_spa',
                'stanza_spa'
            ],

            'swe': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_swe',
                'stanza_swe'
            ],

            'tgl': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_tgl'
            ],

            'tgk': ['nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter'],

            'tam': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_tam',
                'stanza_tam'
            ],

            'tat': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_tat'
            ],

            'tel': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_tel',
                'stanza_tel'
            ],

            'tdt': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'sacremoses_moses'
            ],

            'tha': [
                'pythainlp_longest_matching',
                'pythainlp_max_matching',
                'pythainlp_max_matching_tcc',
                'pythainlp_nercut',
                'stanza_tha'
            ],

            'bod': ['botok_bod'],

            'tir': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_tir'
            ],

            'tsn': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_tsn'
            ],

            'tur': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_tur',
                'stanza_tur'
            ],

            'ukr': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_ukr',
                'stanza_ukr'
            ],

            'urd': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_urd',
                'stanza_urd'
            ],

            'uig': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_uig'
            ],

            'vie': [
                'nltk_tok_tok',
                'underthesea_vie',
                'stanza_vie'
            ],

            'cym': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_cym'
            ],

            'wol': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'stanza_wol'
            ],

            'yor': [
                'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter',
                'spacy_yor'
            ],

            'other': [
                'nltk_nist', 'nltk_nltk', 'nltk_penn_treebank', 'nltk_regex', 'nltk_tok_tok', 'nltk_twitter',
                'sacremoses_moses',
                'spacy_eng',
                'stanza_eng'
            ]
        },

        'syl_tokenizers': {
            'afr': ['pyphen_afr'],
            'sqi': ['pyphen_sqi'],
            'eus': ['pyphen_eus'],
            'bel': ['pyphen_bel'],
            'bul': ['pyphen_bul'],
            'cat': ['pyphen_cat'],
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
                'pythainlp_han_solo',
                'pythainlp_syl_dict'
            ],

            'ukr': ['pyphen_ukr'],
            'zul': ['pyphen_zul']
        },

        'pos_taggers': {
            'afr': ['stanza_afr'],
            'ara': ['stanza_ara'],
            'xcl': ['stanza_xcl'],
            'hye': ['stanza_hye'],
            'hyw': ['stanza_hyw'],
            'eus': ['stanza_eus'],
            'bel': ['stanza_bel'],
            'bul': ['stanza_bul'],
            'bxr': ['stanza_bxr'],

            'cat': [
                'spacy_cat',
                'stanza_cat'
            ],

            'lzh': ['stanza_lzh'],
            'zho_cn': [
                'spacy_zho',
                'stanza_zho_cn'
            ],
            'zho_tw': [
                'spacy_zho',
                'stanza_zho_tw'
            ],

            'chu': ['stanza_chu'],
            'cop': ['stanza_cop'],

            'hrv': [
                'spacy_hrv',
                'stanza_hrv'
            ],

            'ces': ['stanza_ces'],

            'dan': [
                'spacy_dan',
                'stanza_dan'
            ],

            'nld': [
                'spacy_nld',
                'stanza_nld'
            ],

            'ang': ['stanza_ang'],
            'eng_gb': [
                'nltk_perceptron_eng',
                'spacy_eng',
                'stanza_eng'
            ],
            'eng_us': [
                'nltk_perceptron_eng',
                'spacy_eng',
                'stanza_eng'
            ],

            'myv': ['stanza_myv'],
            'est': ['stanza_est'],
            'fao': ['stanza_fao'],

            'fin': [
                'spacy_fin',
                'stanza_fin'
            ],

            'fra': [
                'spacy_fra',
                'stanza_fra'
            ],
            'fro': ['stanza_fro'],

            'glg': ['stanza_glg'],

            'deu_at': [
                'spacy_deu',
                'stanza_deu'
            ],
            'deu_de': [
                'spacy_deu',
                'stanza_deu'
            ],
            'deu_ch': [
                'spacy_deu',
                'stanza_deu'
            ],

            'got': ['stanza_got'],

            'grc': ['stanza_grc'],
            'ell': [
                'spacy_ell',
                'stanza_ell'
            ],

            'hbo': ['stanza_hbo'],
            'heb': ['stanza_heb'],
            'hin': ['stanza_hin'],
            'hun': ['stanza_hun'],
            'isl': ['stanza_isl'],
            'ind': ['stanza_ind'],
            'gle': ['stanza_gle'],

            'ita': [
                'spacy_ita',
                'stanza_ita'
            ],

            'jpn': [
                'spacy_jpn',
                'stanza_jpn',
                'sudachipy_jpn'
            ],

            'kaz': ['stanza_kaz'],
            'khm': ['khmer_nltk_khm'],

            'kor': [
                'python_mecab_ko_mecab',
                'spacy_kor',
                'stanza_kor'
            ],

            'kmr': ['stanza_kmr'],
            'kir': ['stanza_kir'],

            'lao': [
                'laonlp_seqlabeling',
                'laonlp_yunshan_cup_2020'
            ],

            'lat': ['stanza_lat'],
            'lav': ['stanza_lav'],
            'lij': ['stanza_lij'],

            'lit': [
                'spacy_lit',
                'stanza_lit'
            ],

            'mkd': ['spacy_mkd'],
            'mlt': ['stanza_mlt'],
            'glv': ['stanza_glv'],
            'mar': ['stanza_mar'],
            'pcm': ['stanza_pcm'],

            'nob': [
                'spacy_nob',
                'stanza_nob'
            ],

            'nno': ['stanza_nno'],
            'fas': ['stanza_fas'],

            'pol': [
                'spacy_pol',
                'stanza_pol'
            ],

            'qpm': ['stanza_qpm'],

            'por_br': [
                'spacy_por',
                'stanza_por'
            ],
            'por_pt': [
                'spacy_por',
                'stanza_por'
            ],

            'ron': [
                'spacy_ron',
                'stanza_ron'
            ],


            'rus': [
                'nltk_perceptron_rus',
                'pymorphy3_morphological_analyzer',
                'spacy_rus',
                'stanza_rus'
            ],
            'orv': ['stanza_orv'],

            'sme': ['stanza_sme'],
            'san': ['stanza_san'],
            'gla': ['stanza_gla'],
            'srp_latn': ['stanza_srp_latn'],
            'snd': ['stanza_snd'],
            'slk': ['stanza_slk'],

            'slv': [
                'spacy_slv',
                'stanza_slv']
            ,

            'hsb': ['stanza_hsb'],

            'spa': [
                'spacy_spa',
                'stanza_spa'
            ],

            'swe': [
                'spacy_swe',
                'stanza_swe'
            ],

            'tam': ['stanza_tam'],
            'tel': ['stanza_tel'],

            'tha': [
                'pythainlp_perceptron_blackboard',
                'pythainlp_perceptron_orchid',
                'pythainlp_perceptron_pud'
            ],

            'bod': ['botok_bod'],
            'tur': ['stanza_tur'],

            'ukr': [
                'pymorphy3_morphological_analyzer',
                'spacy_ukr',
                'stanza_ukr'
            ],

            'urd': ['stanza_urd'],
            'uig': ['stanza_uig'],

            'vie': [
                'stanza_vie',
                'underthesea_vie'
            ],

            'cym': ['stanza_cym'],
            'wol': ['stanza_wol']
        },

        'lemmatizers': {
            'afr': ['stanza_afr'],
            'sqi': ['simplemma_sqi'],
            'ara': ['stanza_ara'],

            'xcl': ['stanza_xcl'],
            'hye': [
                'simplemma_hye',
                'stanza_hye'
            ],
            'hyw': ['stanza_hyw'],

            'ast': ['simplemma_ast'],
            'eus': ['stanza_eus'],
            'bel': ['stanza_bel'],
            'ben': ['spacy_ben'],

            'bul': [
                'simplemma_bul',
                'stanza_bul'
            ],

            'bxr': ['stanza_bxr'],

            'cat': [
                'simplemma_cat',
                'spacy_cat',
                'stanza_cat'
            ],

            'lzh': ['stanza_lzh'],
            'zho_cn': ['stanza_zho_cn'],
            'zho_tw': ['stanza_zho_tw'],
            'chu': ['stanza_chu'],
            'cop': ['stanza_cop'],

            'hrv': [
                'simplemma_hbs',
                'spacy_hrv',
                'stanza_hrv'
            ],

            'ces': [
                'simplemma_ces',
                'spacy_ces',
                'stanza_ces'
            ],

            'dan': [
                'simplemma_dan',
                'spacy_dan',
                'stanza_dan'
            ],

            'nld': [
                'simplemma_nld',
                'spacy_nld',
                'stanza_nld'
            ],

            'enm': ['simplemma_enm'],
            'ang': ['stanza_ang'],
            'eng_gb': [
                'nltk_wordnet',
                'simplemma_eng',
                'spacy_eng',
                'stanza_eng'
            ],
            'eng_us': [
                'nltk_wordnet',
                'simplemma_eng',
                'spacy_eng',
                'stanza_eng'
            ],

            'myv': ['stanza_myv'],

            'est': [
                'simplemma_est',
                'stanza_est'
            ],

            'fin': [
                'simplemma_fin',
                'spacy_fin',
                'stanza_fin'
            ],

            'fra': [
                'simplemma_fra',
                'spacy_fra',
                'stanza_fra'
            ],
            'fro': ['stanza_fro'],

            'glg': [
                'simplemma_glg',
                'stanza_glg'
            ],

            'kat': ['simplemma_kat'],

            'deu_at': [
                'simplemma_deu',
                'spacy_deu',
                'stanza_deu'
            ],
            'deu_de': [
                'simplemma_deu',
                'spacy_deu',
                'stanza_deu'
            ],
            'deu_ch': [
                'simplemma_deu',
                'spacy_deu',
                'stanza_deu'
            ],

            'got': ['stanza_got'],

            'grc': [
                'spacy_grc',
                'stanza_grc'
            ],
            'ell': [
                'simplemma_ell',
                'spacy_ell',
                'stanza_ell'
            ],

            'hbo': ['stanza_hbo'],
            'heb': ['stanza_heb'],

            'hin': [
                'simplemma_hin',
                'stanza_hin'
            ],

            'hun': [
                'simplemma_hun',
                'spacy_hun',
                'stanza_hun'
            ],

            'isl': [
                'simplemma_isl',
                'stanza_isl'
            ],

            'ind': [
                'simplemma_ind',
                'spacy_ind',
                'stanza_ind'
            ],

            'gle': [
                'simplemma_gle',
                'spacy_gle',
                'stanza_gle'
            ],

            'ita': [
                'simplemma_ita',
                'spacy_ita',
                'stanza_ita'
            ],

            'jpn': [
                'spacy_jpn',
                'stanza_jpn',
                'sudachipy_jpn'
            ],

            'kaz': ['stanza_kaz'],

            'kor': [
                'spacy_kor',
                'stanza_kor'
            ],

            'kmr': ['stanza_kmr'],
            'kir': ['stanza_kir'],

            'lat': [
                'simplemma_lat',
                'stanza_lat'
            ],

            'lav': [
                'simplemma_lav',
                'stanza_lav'
            ],

            'lij': ['stanza_lij'],

            'lit': [
                'simplemma_lit',
                'spacy_lit',
                'stanza_lit'
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

            'glv': [
                'simplemma_glv',
                'stanza_glv'
            ],

            'mar': ['stanza_mar'],
            'pcm': ['stanza_pcm'],

            'nob': [
                'simplemma_nob',
                'spacy_nob',
                'stanza_nob'
            ],
            'nno': [
                'simplemma_nno',
                'stanza_nno'
            ],

            'fas': [
                'simplemma_fas',
                'spacy_fas',
                'stanza_fas'
            ],

            'pol': [
                'simplemma_pol',
                'spacy_pol',
                'stanza_pol'
            ],

            'qpm': ['stanza_qpm'],

            'por_br': [
                'simplemma_por',
                'spacy_por',
                'stanza_por'
            ],
            'por_pt': [
                'simplemma_por',
                'spacy_por',
                'stanza_por'
            ],

            'ron': [
                'simplemma_ron',
                'spacy_ron',
                'stanza_ron'
            ],

            'rus': [
                'simplemma_rus',
                'pymorphy3_morphological_analyzer',
                'spacy_rus',
                'stanza_rus'
            ],
            'orv': ['stanza_orv'],

            'sme': [
                'simplemma_sme',
                'stanza_sme'
            ],

            'san': ['stanza_san'],

            'gla': [
                'simplemma_gla',
                'stanza_gla'
            ],

            'srp_cyrl': ['spacy_srp'],
            'srp_latn': [
                'simplemma_hbs',
                'stanza_srp_latn'
            ],

            'slk': [
                'simplemma_slk',
                'stanza_slk'
            ],

            'slv': [
                'simplemma_slv',
                'spacy_slv',
                'stanza_slv'
            ],

            'hsb': ['stanza_hsb'],

            'spa': [
                'simplemma_spa',
                'spacy_spa',
                'stanza_spa'
            ],

            'swa': ['simplemma_swa'],

            'swe': [
                'simplemma_swe',
                'spacy_swe',
                'stanza_swe'
            ],

            'tgl': [
                'simplemma_tgl',
                'spacy_tgl'
            ],

            'tam': ['stanza_tam'],
            'bod': ['botok_bod'],

            'tur': [
                'simplemma_tur',
                'spacy_tur',
                'stanza_tur'
            ],

            'ukr': [
                'pymorphy3_morphological_analyzer',
                'simplemma_ukr',
                'spacy_ukr',
                'stanza_ukr'
            ],

            'urd': [
                'spacy_urd',
                'stanza_urd'
            ],

            'uig': ['stanza_uig'],

            'cym': [
                'simplemma_cym',
                'stanza_cym'
            ],

            'wol': ['stanza_wol']
        },

        'stop_word_lists': {
            'ara': ['nltk_ara'],
            'aze': ['nltk_aze'],
            'eus': ['nltk_eus'],
            'ben': ['nltk_ben'],
            'cat': ['nltk_cat'],
            'zho_cn': ['nltk_zho_cn'],
            'zho_tw': ['nltk_zho_tw'],
            'dan': ['nltk_dan'],
            'nld': ['nltk_nld'],
            'eng_gb': ['nltk_eng'],
            'eng_us': ['nltk_eng'],
            'fin': ['nltk_fin'],
            'fra': ['nltk_fra'],
            'deu_at': ['nltk_deu'],
            'deu_de': ['nltk_deu'],
            'deu_ch': ['nltk_deu'],
            'ell': ['nltk_ell'],
            'heb': ['nltk_heb'],
            'hun': ['nltk_hun'],
            'ind': ['nltk_ind'],
            'ita': ['nltk_ita'],
            'kaz': ['nltk_kaz'],
            'lao': ['laonlp_lao'],
            'nep': ['nltk_nep'],
            'nob': ['nltk_nob'],
            'por_br': ['nltk_por'],
            'por_pt': ['nltk_por'],
            'ron': ['nltk_ron'],
            'rus': ['nltk_rus'],
            'slv': ['nltk_slv'],
            'spa': ['nltk_spa'],
            'swe': ['nltk_swe'],
            'tgk': ['nltk_tgk'],
            'tha': ['pythainlp_tha'],
            'tur': ['nltk_tur'],

            'other': []
        },

        'dependency_parsers': {
            'afr': ['stanza_afr'],
            'ara': ['stanza_ara'],
            'xcl': ['stanza_xcl'],
            'hye': ['stanza_hye'],
            'hyw': ['stanza_hyw'],
            'eus': ['stanza_eus'],
            'bel': ['stanza_bel'],
            'bul': ['stanza_bul'],
            'bxr': ['stanza_bxr'],

            'cat': [
                'spacy_cat',
                'stanza_cat'
            ],

            'lzh': ['stanza_lzh'],
            'zho_cn': [
                'spacy_zho',
                'stanza_zho_cn'
            ],
            'zho_tw': [
                'spacy_zho',
                'stanza_zho_tw'
            ],

            'chu': ['stanza_chu'],
            'cop': ['stanza_cop'],

            'hrv': [
                'spacy_hrv',
                'stanza_hrv'
            ],

            'ces': ['stanza_ces'],

            'dan': [
                'spacy_dan',
                'stanza_dan'
            ],

            'nld': [
                'spacy_nld',
                'stanza_nld'
            ],

            'ang': ['stanza_ang'],
            'eng_gb': [
                'spacy_eng',
                'stanza_eng'
            ],
            'eng_us': [
                'spacy_eng',
                'stanza_eng'
            ],

            'myv': ['stanza_myv'],
            'est': ['stanza_est'],
            'fao': ['stanza_fao'],

            'fin': [
                'spacy_fin',
                'stanza_fin'
            ],

            'fra': [
                'spacy_fra',
                'stanza_fra'
            ],
            'fro': ['stanza_fro'],

            'glg': ['stanza_glg'],

            'deu_at': [
                'spacy_deu',
                'stanza_deu'
            ],
            'deu_de': [
                'spacy_deu',
                'stanza_deu'
            ],
            'deu_ch': [
                'spacy_deu',
                'stanza_deu'
            ],

            'got': ['stanza_got'],

            'grc': ['stanza_grc'],
            'ell': [
                'spacy_ell',
                'stanza_ell'
            ],

            'hbo': ['stanza_hbo'],
            'heb': ['stanza_heb'],
            'hin': ['stanza_hin'],
            'hun': ['stanza_hun'],
            'isl': ['stanza_isl'],
            'ind': ['stanza_ind'],
            'gle': ['stanza_gle'],

            'ita': [
                'spacy_ita',
                'stanza_ita'
            ],

            'jpn': [
                'spacy_jpn',
                'stanza_jpn'
            ],

            'kaz': ['stanza_kaz'],

            'kor': [
                'spacy_kor',
                'stanza_kor'
            ],

            'kmr': ['stanza_kmr'],
            'kir': ['stanza_kir'],
            'lat': ['stanza_lat'],
            'lav': ['stanza_lav'],
            'lij': ['stanza_lij'],

            'lit': [
                'spacy_lit',
                'stanza_lit'
            ],

            'mkd': ['spacy_mkd'],
            'mlt': ['stanza_mlt'],
            'glv': ['stanza_glv'],
            'mar': ['stanza_mar'],
            'pcm': ['stanza_pcm'],

            'nob': [
                'spacy_nob',
                'stanza_nob'
            ],

            'nno': ['stanza_nno'],
            'fas': ['stanza_fas'],

            'pol': [
                'spacy_pol',
                'stanza_pol'
            ],

            'qpm': ['stanza_qpm'],

            'por_br': [
                'spacy_por',
                'stanza_por'
            ],
            'por_pt': [
                'spacy_por',
                'stanza_por'
            ],

            'ron': [
                'spacy_ron',
                'stanza_ron'
            ],

            'rus': [
                'spacy_rus',
                'stanza_rus'
            ],
            'orv': ['stanza_orv'],

            'sme': ['stanza_sme'],
            'san': ['stanza_san'],
            'gla': ['stanza_gla'],
            'srp_latn': ['stanza_srp_latn'],
            'snd': ['stanza_snd'],
            'slk': ['stanza_slk'],

            'slv': [
                'spacy_slv',
                'stanza_slv'
            ],

            'hsb': ['stanza_hsb'],

            'spa': [
                'spacy_spa',
                'stanza_spa'
            ],

            'swe': [
                'spacy_swe',
                'stanza_swe'
            ],

            'tam': ['stanza_tam'],
            'tel': ['stanza_tel'],
            'tur': ['stanza_tur'],

            'ukr': [
                'spacy_ukr',
                'stanza_ukr'
            ],

            'urd': ['stanza_urd'],
            'uig': ['stanza_uig'],
            'vie': ['stanza_vie'],
            'cym': ['stanza_cym'],
            'wol': ['stanza_wol']
        },

        'sentiment_analyzers': {
            'afr': ['vader_afr'],
            'sqi': ['vader_sqi'],
            'amh': ['vader_amh'],
            'ara': ['vader_ara'],
            'hye': ['vader_hye'],
            'hyw': ['vader_hye'],
            'asm': ['vader_asm'],
            'aze': ['vader_aze'],
            'eus': ['vader_eus'],
            'bel': ['vader_bel'],
            'ben': ['vader_ben'],
            'bul': ['vader_bul'],
            'mya': ['vader_mya'],
            'cat': ['vader_cat'],

            'zho_cn': [
                'stanza_zho_cn',
                'vader_zho_cn'
            ],

            'zho_tw': ['vader_zho_tw'],
            'hrv': ['vader_hrv'],
            'ces': ['vader_ces'],
            'dan': ['vader_dan'],
            'nld': ['vader_nld'],

            'eng_gb': [
                'stanza_eng',
                'vader_eng'
            ],
            'eng_us': [
                'stanza_eng',
                'vader_eng'
            ],

            'epo': ['vader_epo'],
            'est': ['vader_est'],
            'fin': ['vader_fin'],
            'fra': ['vader_fra'],
            'glg': ['vader_glg'],
            'kat': ['vader_kat'],

            'deu_at': [
                'stanza_deu',
                'vader_deu'
            ],
            'deu_de': [
                'stanza_deu',
                'vader_deu'
            ],
            'deu_ch': [
                'stanza_deu',
                'vader_deu'
            ],

            'ell': ['vader_ell'],
            'guj': ['vader_guj'],
            'heb': ['vader_heb'],
            'hin': ['vader_hin'],
            'hun': ['vader_hun'],
            'isl': ['vader_isl'],
            'ind': ['vader_ind'],
            'gle': ['vader_gle'],
            'ita': ['vader_ita'],
            'jpn': ['vader_jpn'],
            'kan': ['vader_kan'],
            'kaz': ['vader_kaz'],
            'khm': ['vader_khm'],
            'kor': ['vader_kor'],
            'kmr': ['vader_kmr'],
            'kir': ['vader_kir'],
            'lao': ['vader_lao'],
            'lat': ['vader_lat'],
            'lav': ['vader_lav'],
            'lit': ['vader_lit'],
            'lug': ['vader_lug'],
            'ltz': ['vader_ltz'],
            'mkd': ['vader_mkd'],
            'msa': ['vader_msa'],
            'mal': ['vader_mal'],
            'mlt': ['vader_mlt'],

            'mar': [
                'stanza_mar',
                'vader_mar'
            ],

            'mni_mtei': ['vader_mni_mtei'],
            'mon': ['vader_mon'],
            'nep': ['vader_nep'],
            'nob': ['vader_nob'],
            'ori': ['vader_ori'],
            'fas': ['vader_fas'],
            'pol': ['vader_pol'],
            'por_pt': ['vader_por'],
            'por_br': ['vader_por'],
            'pan_guru': ['vader_pan_guru'],
            'ron': ['vader_ron'],
            'rus': ['vader_rus'],
            'san': ['vader_san'],
            'gla': ['vader_gla'],
            'srp_cyrl': ['vader_srp_cyrl'],
            'srp_latn': ['vader_srp_cyrl'],
            'snd': ['vader_snd'],
            'sin': ['vader_sin'],
            'slk': ['vader_slk'],
            'slv': ['vader_slv'],

            'spa': [
                'stanza_spa',
                'vader_spa'
            ],

            'swa': ['vader_swa'],
            'swe': ['vader_swe'],
            'tgl': ['vader_tgl'],
            'tgk': ['vader_tgk'],
            'tam': ['vader_tam'],
            'tat': ['vader_tat'],
            'tel': ['vader_tel'],
            'tha': ['vader_tha'],
            'tir': ['vader_tir'],
            'tur': ['vader_tur'],
            'ukr': ['vader_ukr'],
            'urd': ['vader_urd'],
            'uig': ['vader_uig'],

            'vie': [
                'stanza_vie',
                'underthesea_vie'
            ],

            'cym': ['vader_cym'],
            'yor': ['vader_yor'],
            'zul': ['vader_zul']
        },

        # Only people's names are capitalized and case of measure names are preserved as in original papers
        'mapping_measures': {
            'dispersion': {
                _tr('wl_settings_global', 'None'): 'none',
                _tr('wl_settings_global', 'Average logarithmic distance'): 'ald',
                _tr('wl_settings_global', 'Average reduced frequency'): 'arf',
                _tr('wl_settings_global', 'Average waiting time'): 'awt',
                _tr('wl_settings_global', "Carroll's D₂"): 'carrolls_d2',
                _tr('wl_settings_global', "Gries's DP"): 'griess_dp',
                _tr('wl_settings_global', "Juilland's D"): 'juillands_d',
                _tr('wl_settings_global', "Lyne's D₃"): 'lynes_d3',
                _tr('wl_settings_global', "Rosengren's S"): 'rosengrens_s',
                _tr('wl_settings_global', "Zhang's Distributional Consistency"): 'zhangs_dc'
            },

            'adjusted_freq': {
                _tr('wl_settings_global', 'None'): 'none',
                _tr('wl_settings_global', 'Average logarithmic distance'): 'fald',
                _tr('wl_settings_global', 'Average reduced frequency'): 'farf',
                _tr('wl_settings_global', 'Average waiting time'): 'fawt',
                _tr('wl_settings_global', "Carroll's Uₘ"): 'carrolls_um',
                _tr('wl_settings_global', "Engwall's FM"): 'engwalls_fm',
                _tr('wl_settings_global', "Juilland's U"): 'juillands_u',
                _tr('wl_settings_global', "Kromer's UR"): 'kromers_ur',
                _tr('wl_settings_global', "Rosengren's KF"): 'rosengrens_kf'
            },

            'statistical_significance': {
                _tr('wl_settings_global', 'None'): 'none',
                _tr('wl_settings_global', "Fisher's exact test"): 'fishers_exact_test',
                _tr('wl_settings_global', 'Log-likelihood ratio test'): 'log_likelihood_ratio_test',
                _tr('wl_settings_global', 'Mann-Whitney U test'): 'mann_whitney_u_test',
                _tr('wl_settings_global', "Pearson's chi-squared test"): 'pearsons_chi_squared_test',
                _tr('wl_settings_global', "Student's t-test (1-sample)"): 'students_t_test_1_sample',
                _tr('wl_settings_global', "Student's t-test (2-sample)"): 'students_t_test_2_sample',
                _tr('wl_settings_global', 'Z-test'): 'z_test',
                _tr('wl_settings_global', 'Z-test (Berry-Rogghe)'): 'z_test_berry_rogghe'
            },

            'bayes_factor': {
                _tr('wl_settings_global', 'None'): 'none',
                _tr('wl_settings_global', 'Log-likelihood ratio test'): 'log_likelihood_ratio_test',
                _tr('wl_settings_global', "Student's t-test (2-sample)"): 'students_t_test_2_sample'
            },

            'effect_size': {
                _tr('wl_settings_global', 'None'): 'none',
                _tr('wl_settings_global', 'Conditional probability'): 'conditional_probability',
                'ΔP': 'delta_p',
                _tr('wl_settings_global', 'Dice-Sørensen coefficient'): 'dice_sorensen_coeff',
                _tr('wl_settings_global', 'Difference coefficient'): 'diff_coeff',
                _tr('wl_settings_global', 'Jaccard index'): 'jaccard_index',
                _tr('wl_settings_global', "Kilgarriff's ratio"): 'kilgarriffs_ratio',
                'logDice': 'log_dice',
                _tr('wl_settings_global', 'Log Ratio'): 'log_ratio',
                'MI.log-f': 'mi_log_f',
                _tr('wl_settings_global', 'Minimum sensitivity'): 'min_sensitivity',
                _tr('wl_settings_global', 'Mutual Expectation'): 'me',
                _tr('wl_settings_global', 'Mutual information'): 'mi',
                _tr('wl_settings_global', 'Mutual information (normalized)'): 'nmi',
                _tr('wl_settings_global', 'μ-value'): 'mu_val',
                _tr('wl_settings_global', 'Odds ratio'): 'or',
                '%DIFF': 'pct_diff',
                _tr('wl_settings_global', 'Pointwise mutual information'): 'pmi',
                _tr('wl_settings_global', 'Pointwise mutual information (cubic)'): 'im3',
                _tr('wl_settings_global', 'Pointwise mutual information (normalized)'): 'npmi',
                _tr('wl_settings_global', 'Pointwise mutual information (squared)'): 'im2',
                _tr('wl_settings_global', 'Poisson collocation measure'): 'poisson_collocation_measure',
                _tr('wl_settings_global', 'Relative risk'): 'rr',
                _tr('wl_settings_global', 'Squared phi coefficient'): 'squared_phi_coeff'
            }
        },

        # Column headers are capitalized
        'measures_dispersion': {
            'none': {
                'col_text': None,
                'func': None,
                'type': None
            },

            'ald': {
                'col_text': 'ALD',
                'func': wl_measures_dispersion.ald,
                'type': 'dist_based'
            },

            'arf': {
                'col_text': 'ARF',
                'func': wl_measures_dispersion.arf,
                'type': 'dist_based'
            },

            'awt': {
                'col_text': 'AWT',
                'func': wl_measures_dispersion.awt,
                'type': 'dist_based'
            },

            'carrolls_d2': {
                'col_text': _tr('wl_settings_global', "Carroll's D₂"),
                'func': wl_measures_dispersion.carrolls_d2,
                'type': 'parts_based'
            },

            'griess_dp': {
                'col_text': _tr('wl_settings_global', "Gries's DP"),
                'func': wl_measures_dispersion.griess_dp,
                'type': 'parts_based'
            },

            'juillands_d': {
                'col_text': _tr('wl_settings_global', "Juilland's D"),
                'func': wl_measures_dispersion.juillands_d,
                'type': 'parts_based'
            },

            'lynes_d3': {
                'col_text': _tr('wl_settings_global', "Lyne's D₃"),
                'func': wl_measures_dispersion.lynes_d3,
                'type': 'parts_based'
            },

            'rosengrens_s': {
                'col_text': _tr('wl_settings_global', "Rosengren's S"),
                'func': wl_measures_dispersion.rosengrens_s,
                'type': 'parts_based'
            },

            'zhangs_dc': {
                'col_text': _tr('wl_settings_global', "Zhang's DC"),
                'func': wl_measures_dispersion.zhangs_distributional_consistency,
                'type': 'parts_based'
            }
        },

        'measures_adjusted_freq': {
            'none': {
                'col_text': None,
                'func': None,
                'type': None
            },

            'fald': {
                'col_text': 'f-ALD',
                'func': wl_measures_adjusted_freq.fald,
                'type': 'dist_based'
            },

            'farf': {
                'col_text': 'f-ARF',
                'func': wl_measures_adjusted_freq.farf,
                'type': 'dist_based'
            },

            'fawt': {
                'col_text': 'f-AWT',
                'func': wl_measures_adjusted_freq.fawt,
                'type': 'dist_based'
            },

            'carrolls_um': {
                'col_text': _tr('wl_settings_global', "Carroll's Uₘ"),
                'func': wl_measures_adjusted_freq.carrolls_um,
                'type': 'parts_based'
            },

            'engwalls_fm': {
                'col_text': _tr('wl_settings_global', "Engwall's FM"),
                'func': wl_measures_adjusted_freq.engwalls_fm,
                'type': 'parts_based'
            },

            'juillands_u': {
                'col_text': _tr('wl_settings_global', "Juilland's U"),
                'func': wl_measures_adjusted_freq.juillands_u,
                'type': 'parts_based'
            },

            'kromers_ur': {
                'col_text': _tr('wl_settings_global', "Kromer's UR"),
                'func': wl_measures_adjusted_freq.kromers_ur,
                'type': 'parts_based'
            },

            'rosengrens_kf': {
                'col_text': _tr('wl_settings_global', "Rosengren's KF"),
                'func': wl_measures_adjusted_freq.rosengrens_kf,
                'type': 'parts_based'
            }
        },

        'tests_statistical_significance': {
            'none': {
                'col_text': None,
                'func': None,
                'to_sections': False,
                'collocation': True,
                'keyword': True
            },

            'fishers_exact_test': {
                # There is no test statistic for Fisher's exact test
                'col_text': None,
                'func': wl_measures_statistical_significance.fishers_exact_test,
                'to_sections': False,
                'collocation': True,
                'keyword': True
            },

            'log_likelihood_ratio_test': {
                'col_text': _tr('wl_settings_global', 'Log-likelihood Ratio'),
                'func': wl_measures_statistical_significance.log_likelihood_ratio_test,
                'to_sections': False,
                'collocation': True,
                'keyword': True
            },

            'mann_whitney_u_test': {
                'col_text': 'U1',
                'func': wl_measures_statistical_significance.mann_whitney_u_test,
                'to_sections': True,
                'collocation': False,
                'keyword': True
            },

            'pearsons_chi_squared_test': {
                'col_text': 'χ2',
                'func': wl_measures_statistical_significance.pearsons_chi_squared_test,
                'to_sections': False,
                'collocation': True,
                'keyword': True
            },

            'students_t_test_1_sample': {
                'col_text': _tr('wl_settings_global', 't-statistic'),
                'func': wl_measures_statistical_significance.students_t_test_1_sample,
                'to_sections': False,
                'collocation': True,
                'keyword': False
            },

            'students_t_test_2_sample': {
                'col_text': _tr('wl_settings_global', 't-statistic'),
                'func': wl_measures_statistical_significance.students_t_test_2_sample,
                'to_sections': True,
                'collocation': False,
                'keyword': True
            },

            'z_test': {
                'col_text': _tr('wl_settings_global', 'z-score'),
                'func': wl_measures_statistical_significance.z_test,
                'to_sections': False,
                'collocation': True,
                'keyword': False
            },

            'z_test_berry_rogghe': {
                'col_text': _tr('wl_settings_global', 'z-score'),
                'func': wl_measures_statistical_significance.z_test_berry_rogghe,
                'to_sections': False,
                'collocation': True,
                'keyword': False
            }
        },

        'measures_bayes_factor': {
            'none': {
                'func': None,
                'to_sections': None,
                'collocation': True,
                'keyword': True
            },

            'log_likelihood_ratio_test': {
                'func': wl_measures_bayes_factor.bayes_factor_log_likelihood_ratio_test,
                'to_sections': False,
                'collocation': True,
                'keyword': True
            },

            'students_t_test_2_sample': {
                'func': wl_measures_bayes_factor.bayes_factor_students_t_test_2_sample,
                'to_sections': True,
                'collocation': False,
                'keyword': True
            },
        },

        'measures_effect_size': {
            'none': {
                'col_text': None,
                'func': None,
                'collocation': True,
                'keyword': True
            },

            'conditional_probability': {
                'col_text': 'P',
                'func': wl_measures_effect_size.conditional_probability,
                'collocation': True,
                'keyword': False
            },

            'delta_p': {
                'col_text': 'ΔP',
                'func': wl_measures_effect_size.delta_p,
                'collocation': True,
                'keyword': False
            },

            'dice_sorensen_coeff': {
                'col_text': _tr('wl_settings_global', 'Dice-Sørensen Coefficient'),
                'func': wl_measures_effect_size.dice_sorensen_coeff,
                'collocation': True,
                'keyword': False
            },

            'diff_coeff': {
                'col_text': _tr('wl_settings_global', 'Difference Coefficient'),
                'func': wl_measures_effect_size.diff_coeff,
                'collocation': False,
                'keyword': True
            },

            'jaccard_index': {
                'col_text': _tr('wl_settings_global', 'Jaccard Index'),
                'func': wl_measures_effect_size.jaccard_index,
                'collocation': True,
                'keyword': False
            },

            'kilgarriffs_ratio': {
                'col_text': _tr('wl_settings_global', "Kilgarriff's Ratio"),
                'func': wl_measures_effect_size.kilgarriffs_ratio,
                'collocation': False,
                'keyword': True
            },

            'log_dice': {
                'col_text': 'logDice',
                'func': wl_measures_effect_size.log_dice,
                'collocation': True,
                'keyword': False
            },

            'log_ratio': {
                'col_text': _tr('wl_settings_global', 'Log Ratio'),
                'func': wl_measures_effect_size.log_ratio,
                'collocation': True,
                'keyword': True
            },

            'mi_log_f': {
                'col_text': 'MI.log-f',
                'func': wl_measures_effect_size.mi_log_f,
                'collocation': True,
                'keyword': False
            },

            'min_sensitivity': {
                'col_text': _tr('wl_settings_global', 'Minimum Sensitivity'),
                'func': wl_measures_effect_size.min_sensitivity,
                'collocation': True,
                'keyword': False
            },

            'me': {
                'col_text': 'ME',
                'func': wl_measures_effect_size.me,
                'collocation': True,
                'keyword': False
            },

            'mi': {
                'col_text': 'MI',
                'func': wl_measures_effect_size.mi,
                'collocation': True,
                'keyword': True
            },

            'nmi': {
                'col_text': 'NMI',
                'func': wl_measures_effect_size.nmi,
                'collocation': True,
                'keyword': True
            },

            'mu_val': {
                'col_text': 'μ-value',
                'func': wl_measures_effect_size.mu_val,
                'collocation': True,
                'keyword': False
            },

            'or': {
                'col_text': 'OR',
                # "or" is a Python keyword
                'func': wl_measures_effect_size.odds_ratio,
                'collocation': True,
                'keyword': True
            },

            'pct_diff': {
                'col_text': '%DIFF',
                'func': wl_measures_effect_size.pct_diff,
                'collocation': False,
                'keyword': True
            },

            'pmi': {
                'col_text': 'PMI',
                'func': wl_measures_effect_size.pmi,
                'collocation': True,
                'keyword': True
            },

            'im3': {
                'col_text': 'IM³',
                'func': wl_measures_effect_size.im3,
                'collocation': True,
                'keyword': True
            },

            'npmi': {
                'col_text': 'NPMI',
                'func': wl_measures_effect_size.npmi,
                'collocation': True,
                'keyword': True
            },

            'im2': {
                'col_text': 'IM²',
                'func': wl_measures_effect_size.im2,
                'collocation': True,
                'keyword': True
            },

            'poisson_collocation_measure': {
                'col_text': _tr('wl_settings_global', 'Poisson Collocation Measure'),
                'func': wl_measures_effect_size.poisson_collocation_measure,
                'collocation': True,
                'keyword': False
            },

            'rr': {
                'col_text': 'RR',
                'func': wl_measures_effect_size.rr,
                'collocation': True,
                'keyword': True
            },

            'squared_phi_coeff': {
                'col_text': 'φ2',
                'func': wl_measures_effect_size.squared_phi_coeff,
                'collocation': True,
                'keyword': False
            }
        },

        'styles': {
            'style_dialog': '''
                <head><style>
                    * {
                        margin: 0;
                        line-height: 120%;
                    }
                </style></head>
            '''
        }
    }

    # Custom stop word lists (preserve order of language names)
    stop_word_lists = SETTINGS_GLOBAL['stop_word_lists'].copy()

    SETTINGS_GLOBAL['stop_word_lists'].clear()

    for lang in SETTINGS_GLOBAL['langs'].values():
        lang_code = lang[0]

        SETTINGS_GLOBAL['stop_word_lists'][lang_code] = stop_word_lists.get(lang_code, []) + ['custom']

    return SETTINGS_GLOBAL
