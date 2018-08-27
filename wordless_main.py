#
# Wordless: An integrated tool for language & translation studies.
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import copy
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_utils import *

import wordless_settings
import groupbox_files
import tab_overview
import tab_concordancer
import tab_word_cluster
import tab_wordlist
import tab_ngrams
import tab_semantics

class Wordless_Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(self.tr('Wordless Version 1.0'))
        self.setWindowIcon(QIcon('images/wordless_icon.png'))

        self.init_settings()
        self.init_central_widget()

        self.init_menu()

        self.status_bar = self.statusBar()
        self.status_bar.showMessage(self.tr('Ready!'))

        self.setStyleSheet('* {font-family: Arial, sans-serif; color: #292929; font-size: 12px}')

    def init_settings(self):
        self.files = []
        self.files_closed = []

        self.file_langs = {
                              self.tr('Afrikaans'): 'af',
                              self.tr('Albanian'): 'sq',
                              self.tr('Arabic'): 'ar',
                              self.tr('Bengali'): 'bn',
                              self.tr('Bulgarian'): 'bg',
                              self.tr('Catalan, Valencian'): 'ca',
                              self.tr('Chinese (Simplified)'): 'zh-cn',
                              self.tr('Chinese (Traditional)'): 'zh-tw',
                              self.tr('Croatian'): 'hr',
                              self.tr('Czech'): 'cs',
                              self.tr('Danish'): 'da',
                              self.tr('Dutch, Flemish'): 'nl',
                              self.tr('English'): 'en',
                              self.tr('Estonian'): 'et',
                              self.tr('Finnish'): 'fi',
                              self.tr('French'): 'fr',
                              self.tr('German'): 'de',
                              self.tr('Greek'): 'el',
                              self.tr('Gujarati'): 'gu',
                              self.tr('Hebrew (modern)'): 'he',
                              self.tr('Hindi'): 'hi',
                              self.tr('Hungarian'): 'hu',
                              self.tr('Indonesian'): 'id',
                              self.tr('Italian'): 'it',
                              self.tr('Japanese'): 'ja',
                              self.tr('Kannada'): 'kn',
                              self.tr('Korean'): 'ko',
                              self.tr('Latvian'): 'lv',
                              self.tr('Lithuanian'): 'lt',
                              self.tr('Macedonian'): 'mk',
                              self.tr('Malayalam'): 'ml',
                              self.tr('Marathi'): 'mr',
                              self.tr('Nepali'): 'ne',
                              self.tr('Norwegian'): 'no',
                              self.tr('Panjabi, Punjabi'): 'pa',
                              self.tr('Persian'): 'fa',
                              self.tr('Polish'): 'pl',
                              self.tr('Portuguese'): 'pt',
                              self.tr('Romanian, Moldavian, Moldova'): 'ro',
                              self.tr('Russian'): 'ru',
                              self.tr('Slovak'): 'sk',
                              self.tr('Slovenian'): 'sl',
                              self.tr('Somali'): 'so',
                              self.tr('Spanish, Castilian'): 'es',
                              self.tr('Swahili'): 'sw',
                              self.tr('Swedish'): 'sv',
                              self.tr('Tagalog'): 'tl',
                              self.tr('Tamil'): 'ta',
                              self.tr('Telugu'): 'te',
                              self.tr('Thai'): 'th',
                              self.tr('Turkish'): 'tr',
                              self.tr('Ukrainian'): 'uk',
                              self.tr('Urdu'): 'ur',
                              self.tr('Vietnamese'): 'vi',
                              self.tr('Welsh'): 'cy'
                          }

        self.file_exts = {
                             '.txt': self.tr('Text File (*.txt)'),
                             '.htm': self.tr('HTML Page (*.htm; *.html)'),
                             '.html': self.tr('HTML Page (*.htm; *.html)')
                         }

        self.file_encodings = {
                                  self.tr('All Languages(UTF-8 Without BOM)'): 'utf_8',
                                  self.tr('All Languages(UTF-8 With BOM)'): 'utf_8_sig',
                                  self.tr('All Languages(UTF-16)'): 'utf_16',
                                  self.tr('All Languages(UTF-16 Big Endian)'): 'utf_16_be',
                                  self.tr('All Languages(UTF-16 Little Endian)'): 'utf_16_le',
                                  self.tr('All Languages(UTF-32)'): 'utf_32',
                                  self.tr('All Languages(UTF-32 Big Endian)'): 'utf_32_be',
                                  self.tr('All Languages(UTF-32 Little Endian)'): 'utf_32_le',
                                  self.tr('All Languages(UTF-7)'): 'utf_7',
                                  self.tr('All Languages(CP65001)'): 'cp65001',

                                  self.tr('Baltic Languages(CP775)'): 'cp775',
                                  self.tr('Baltic Languages(Windows-1257)'): 'cp1257',
                                  self.tr('Baltic Languages(ISO-8859-4)'): 'iso8859_4',
                                  self.tr('Baltic Languages(ISO-8859-13)'): 'iso8859_13',

                                  self.tr('Celtic Languages(ISO-8859-14)'): 'iso8859_14',

                                  self.tr('Nordic Languages(ISO-8859-10)'): 'iso8859_10',

                                  self.tr('Europe(HP Roman-8)'): 'hp_roman8',

                                  self.tr('Central Europe(Mac OS Central European)'): 'mac_centeuro',
                                  self.tr('Central Europe(Mac OS Latin 2)'): 'mac_latin2',

                                  self.tr('Central and Eastern Europe(CP852)'): 'cp852',
                                  self.tr('Central and Eastern Europe(Windows-1250)'): 'cp1250',
                                  self.tr('Central and Eastern Europe(ISO-8859-2)'): 'iso8859_2',
                                  self.tr('Central and Eastern Europe(Mac Latin)'): 'mac_latin2',

                                  self.tr('South-Eastern Europe(ISO-8859-16)'): 'iso8859_16',

                                  self.tr('Western Europe(EBCDIC 500)'): 'cp500',
                                  self.tr('Western Europe(CP850)'): 'cp850',
                                  self.tr('Western Europe(CP858)'): 'cp858',
                                  self.tr('Western Europe(CP1140)'): 'cp1140',
                                  self.tr('Western Europe(Windows-1252)'): 'windows_1252',
                                  self.tr('Western Europe(ISO-2022-JP-2)'): 'iso2022_jp_2',
                                  self.tr('Western Europe(ISO-8859-1)'): 'iso_8859_1',
                                  self.tr('Western Europe(ISO-8859-15)'): 'iso_8859_15',
                                  self.tr('Western Europe(Mac OS Roman)'): 'mac_roman',

                                  self.tr('Arabic(CP720)'): 'cp720',
                                  self.tr('Arabic(CP864)'): 'cp864',
                                  self.tr('Arabic(Windows-1256)'): 'cp1256',
                                  self.tr('Arabic(ISO-8859-6)'): 'iso_8859_6',
                                  self.tr('Arabic(Mac OS Arabic)'): 'mac_arabic',

                                  self.tr('Bulgarian(IBM855)'): 'cp855',
                                  self.tr('Bulgarian(Windows-1251)'): 'windows_1251',
                                  self.tr('Bulgarian(ISO-8859-5)'): 'iso_8859_5',
                                  self.tr('Bulgarian(Mac OS Cyrillic)'): 'mac_cyrillic',

                                  self.tr('Byelorussian(IBM855)'): 'cp855',
                                  self.tr('Byelorussian(Windows-1251)'): 'cp1251',
                                  self.tr('Byelorussian(ISO-8859-5)'): 'iso_8859_5',
                                  self.tr('Byelorussian(Mac OS Cyrillic)'): 'mac_cyrillic',

                                  self.tr('Canadian(CP863)'): 'cp863',

                                  self.tr('Simplified Chinese(GB2312)'): 'gb2312',
                                  self.tr('Simplified Chinese(HZ)'): 'hz_gb_2312',
                                  self.tr('Simplified Chinese(ISO-2022-JP-2)'): 'iso2022_jp_2',

                                  self.tr('Traditional Chinese(Big-5)'): 'big5',
                                  self.tr('Traditional Chinese(Big5-HKSCS)'): 'big5hkscs',
                                  self.tr('Traditional Chinese(CP950)'): 'cp950',

                                  self.tr('Unified Chinese(GBK)'): 'gbk',
                                  self.tr('Unified Chinese(GB18030)'): 'gb18030',

                                  self.tr('Croatian(Mac OS Croatian)'): 'mac_croatian',

                                  self.tr('Danish(CP865)'): 'cp865',

                                  self.tr('English(ASCII)'): 'ascii',
                                  self.tr('English(EBCDIC 037)'): 'cp037',
                                  self.tr('English(CP437)'): 'cp437',

                                  self.tr('Esperanto(ISO-8859-3)'): 'iso_8859_3',

                                  self.tr('German(EBCDIC 273)'): 'cp273',

                                  self.tr('Greek(CP737)'): 'cp737',
                                  self.tr('Greek(CP869)'): 'cp869',
                                  self.tr('Greek(CP875)'): 'cp875',
                                  self.tr('Greek(Windows-1253)'): 'windows_1253',
                                  self.tr('Greek(ISO-2022-JP-2)'): 'iso2022_jp_2',
                                  self.tr('Greek(ISO-8859-7)'): 'iso_8859_7',
                                  self.tr('Greek(Mac OS Greek)'): 'mac_greek',

                                  self.tr('Hebrew(EBCDIC 424)'): 'cp424',
                                  self.tr('Hebrew(CP856)'): 'cp856',
                                  self.tr('Hebrew(CP862)'): 'cp862',
                                  self.tr('Hebrew(Windows-1255)'): 'windows_1255',
                                  self.tr('Hebrew(ISO-8859-8)'): 'iso_8859_8',

                                  self.tr('Icelandic(CP861)'): 'cp861',
                                  self.tr('Icelandic(Mac OS Icelandic)'): 'mac_iceland',

                                  self.tr('Japanese(CP932)'): 'cp932',
                                  self.tr('Japanese(EUC-JP)'): 'euc_jp',
                                  self.tr('Japanese(EUC-JIS-2004)'): 'euc_jis_2004',
                                  self.tr('Japanese(EUC-JISx0213)'): 'euc_jisx0213',
                                  self.tr('Japanese(ISO-2022-JP)'): 'iso_2022_jp',
                                  self.tr('Japanese(ISO-2022-JP-1)'): 'iso2022_jp_1',
                                  self.tr('Japanese(ISO-2022-JP-2)'): 'iso2022_jp_2',
                                  self.tr('Japanese(ISO-2022-JP-2)'): 'iso2022_jp_2004',
                                  self.tr('Japanese(ISO-2022-JP-3)'): 'iso2022_jp_3',
                                  self.tr('Japanese(ISO-2022-JP-EXT)'): 'iso2022_jp_ext',
                                  self.tr('Japanese(Shift_JIS)'): 'shift_jis',
                                  self.tr('Japanese(Shift_JIS-2004)'): 'shift_jis_2004',
                                  self.tr('Japanese(Shift_JISx0213)'): 'shift_jisx0213',

                                  self.tr('Kazakh(KZ-1048)'): 'kz1048',
                                  self.tr('Kazakh(PTCP154)'): 'ptcp154',

                                  self.tr('Korean(Windows-949)'): 'cp949',
                                  self.tr('Korean(EUC-KR)'): 'euc_kr',
                                  self.tr('Korean(ISO-2022-JP-2)'): 'iso2022_jp_2',
                                  self.tr('Korean(ISO-2022-KR)'): 'iso_2022_kr',
                                  self.tr('Korean(JOHAB)'): 'johab',

                                  self.tr('Macedonian(IBM855)'): 'cp855',
                                  self.tr('Macedonian(Windows-1251)'): 'cp1251',
                                  self.tr('Macedonian(ISO-8859-5)'): 'iso_8859_5',
                                  self.tr('Macedonian(Mac OS Cyrillic)'): 'maccyrillic',

                                  self.tr('Maltese(ISO-8859-3)'): 'iso_8859_3',

                                  self.tr('Norwegian(CP865)'): 'cp865',

                                  self.tr('Persian(Mac OS Farsi)'): 'mac_farsi',

                                  self.tr('Portuguese(CP860)'): 'cp860',

                                  self.tr('Romanian(Mac OS Romanian)'): 'mac_romanian',

                                  self.tr('Russian(IBM855)'): 'ibm855',
                                  self.tr('Russian(IBM866)'): 'ibm866',
                                  self.tr('Russian(Windows-1251)'): 'windows_1251',
                                  self.tr('Russian(ISO-8859-5)'): 'iso_8859_5',
                                  self.tr('Russian(KOI8-R)'): 'koi8_r',
                                  self.tr('Russian(Mac OS Cyrillic)'): 'maccyrillic',

                                  self.tr('Serbian(IBM855)'): 'cp855',
                                  self.tr('Serbian(Windows-1251)'): 'cp1251',
                                  self.tr('Serbian(ISO-8859-5)'): 'iso8859_5',
                                  self.tr('Serbian(Mac OS Cyrillic)'): 'maccyrillic',

                                  self.tr('Tajik(KOI8-T)'): 'koi8_t',

                                  self.tr('Thai(CP874)'): 'cp874',
                                  self.tr('Thai(ISO-8859-11)'): 'iso8859_11',
                                  self.tr('Thai(TIS-620)'): 'tis_620',

                                  self.tr('Turkish(CP857)'): 'cp857',
                                  self.tr('Turkish(EBCDIC 1026)'): 'cp1026',
                                  self.tr('Turkish(Windows-1254)'): 'cp1254',
                                  self.tr('Turkish(ISO-8859-9)'): 'iso_8859_9',
                                  self.tr('Turkish(Mac OS Turkish)'): 'mac_turkish',

                                  self.tr('Ukranian(CP1125)'): 'cp1125',
                                  self.tr('Ukranian(KOI8-U)'): 'koi8_u',

                                  self.tr('Urdu(CP1006)'): 'cp1006',
                                  self.tr('Urdu(Mac OS Farsi)'): 'mac_farsi',

                                  self.tr('Vietnamese(CP1258)'): 'cp1258'
                              }

        self.default_settings = {
                                    'general': {
                                        'encoding_input': ('utf_8', 'All Languages'),
                                        'encoding_output': ('utf_8', 'All Languages'),

                                        'precision': 5,
                                        'style_highlight': 'border: 1px solid Red;'
                                    },
        
                                    'file': {
        
                                    },
        
                                    'overview': {
        
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
                                        'line_width_mode': 'Tokens',
        
                                        'number_lines': 25,
                                        'number_lines_no_limit': True,
        
                                        'punctuations': False,
        
                                        'sort_by': ['Offset', 'In Ascending Order'],
                                        'multi_sort_by': [['Offset', 'Ascending']],
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
        
                                    'word_cluster': {
                                        'words': True,
                                        'lowercase': True,
                                        'uppercase': True,
                                        'title_cased': True,
                                        'numerals': True,
                                        'punctuations': False,
        
                                        'cluster_size_sync': False,
                                        'cluster_size_min': 2,
                                        'cluster_size_max': 2,
                                        'search_term': '',
                                        'search_terms': [],
                                        'ignore_case': True,
                                        'lemmatized_forms': True,
                                        'whole_word': True,
                                        'regex': False,
                                        'multi_search': False,
                                        'search_term_position_left': True,
                                        'search_term_position_middle': True,
                                        'search_term_position_right': True,
                                        
                                        'cumulative': False,

                                        'freq_first_no_limit': True,
                                        'freq_first_min': 1,
                                        'freq_first_max': 1000,
                                        'freq_total_no_limit': True,
                                        'freq_total_min': 1,
                                        'freq_total_max': 1000,
                                        'rank_no_limit': True,
                                        'rank_min': 1,
                                        'rank_max': 50,
                                        'len_no_limit': True,
                                        'len_min': 1,
                                        'len_max': 20,
                                        'files_no_limit': True,
                                        'files_min': 1,
                                        'files_max': 100
                                    },
        
                                    'wordlist': {
                                        'words': True,
                                        'lowercase': True,
                                        'uppercase': True,
                                        'title_cased': True,
                                        'numerals': True,
                                        'punctuations': False,
        
                                        'ignore_case': True,
                                        'lemmatization': True,
        
                                        'cumulative': False,
        
                                        'freq_first_no_limit': True,
                                        'freq_first_min': 1,
                                        'freq_first_max': 1000,
                                        'freq_total_no_limit': True,
                                        'freq_total_min': 1,
                                        'freq_total_max': 1000,
                                        'rank_no_limit': True,
                                        'rank_min': 1,
                                        'rank_max': 50,
                                        'len_no_limit': True,
                                        'len_min': 1,
                                        'len_max': 20,
                                        'files_no_limit': True,
                                        'files_min': 1,
                                        'files_max': 100
                                    },
        
                                    'ngrams': {
                                        'words': True,
                                        'lowercase': True,
                                        'uppercase': True,
                                        'title_cased': True,
                                        'numerals': True,
                                        'punctuations': False,
        
                                        'ngram_size_sync': False,
                                        'ngram_size_min': 2,
                                        'ngram_size_max': 2,
                                        'ignore_case': True,
                                        'lemmatization': True,
        
                                        'cumulative': False,
        
                                        'freq_first_no_limit': True,
                                        'freq_first_min': 1,
                                        'freq_first_max': 1000,
                                        'freq_total_no_limit': True,
                                        'freq_total_min': 1,
                                        'freq_total_max': 1000,
                                        'rank_no_limit': True,
                                        'rank_min': 1,
                                        'rank_max': 50,
                                        'len_no_limit': True,
                                        'len_min': 1,
                                        'len_max': 20,
                                        'files_no_limit': True,
                                        'files_min': 1,
                                        'files_max': 100
                                    },
        
                                    'semantics': {
                                        'search_term': '',
                                        'search_mode': 'Word',
                                        'search_for': 'Synonyms',
        
                                        'degree_max': 10,
                                        'degree_no_limit': True,
                                        'depth_max': 5,
                                        'depth_no_limit': True,
                                        'recursive': True,
                                        'show_lemmas': True,
        
                                        'parts_of_speech': {
                                            'n': self.tr('Noun'),
                                            'v': self.tr('Verb'),
                                            'a': self.tr('Adjective'),
                                            's': self.tr('Adjective Satellite'),
                                            'r': self.tr('Adverb')
                                        }
                                    }
                                }

        self.settings = copy.deepcopy(self.default_settings)

        self.wordless_settings = wordless_settings.Wordless_Settings(self)

    def init_menu(self):
        def exit():
            reply = QMessageBox.question(self,
                                         self.tr('Exit Confirmation'),
                                         self.tr('Do you really want to quit?'),
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)

            if reply == QMessageBox.Yes:
                qApp.quit()

        def show_status_bar():
            if self.status_bar.isVisible():
                self.status_bar.hide()
            else:
                self.status_bar.show()

        def need_help():
            message_box = QMessageBox(QMessageBox.Information,
                                      self.tr('Need Help?'),
                                      self.tr('''
                                              <div style="line-height: 1.2; text-align: justify;">
                                                <div style="margin-bottom: 15px;">Should you need any further information or encounter any problems while using Wordless, please feel free to contact me, and I will reply as soon as possible.</div>
                                                <div style="margin-bottom: 5px">Home Page: <a href="https://github.com/BLKSerene/Wordless">https://github.com/BLKSerene/Wordless</div>
                                                <div>Email: blkserene@gmail.com</div>
                                              </div>
                                              '''),
                                      QMessageBox.Ok,
                                      self)

            message_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

            message_box.exec_()

        def feedback():
            QMessageBox.information(self,
                                    self.tr('Feedback'),
                                    self.tr('''
                                            <div style="margin-bottom: 5px;">If you find any bugs while using Wordless, you might want to report it via Github\'s bug tracker <a href="https://github.com/BLKSerene/Wordless/issues">Issues</a>.</div>
                                            <div>Feedback, enhancement proposals, feature requests and code contribution are also welcomed.</div>
                                            '''),
                                    QMessageBox.Ok)

        def citation():
            def citation_sys_changed():
                if combo_box_citation_sys.currentIndex() == 0:
                    text_edit_citation.setHtml('Ye Lei. Wordless, version 1.0, 2018, https://github.com/BLKSerene/Wordless.')
                elif combo_box_citation_sys.currentIndex() == 1:
                    text_edit_citation.setHtml('Ye, L. (2018) Wordless (Version 1.0) [Computer Software]. Retrieved from https://github.com/BLKSerene/Wordless')
                elif combo_box_citation_sys.currentIndex() == 2:
                    text_edit_citation.setHtml('Ye, Lei. <i>Wordless</i> (Version 1.0). Windows. Shanghai: Ye Lei, 2018.')
                elif combo_box_citation_sys.currentIndex() == 3:
                    text_edit_citation.setHtml('叶磊. Wordless version 1.0[CP]. (2018). https://github.com/BLKSerene/Wordless.')

                if combo_box_citation_sys.currentIndex() <= 2:
                    text_edit_citation.setFont(QFont('Times New Roman', 12))
                elif combo_box_citation_sys.currentIndex() == 3:
                    text_edit_citation.setFont(QFont('宋体', 12))

            def copy():
                text_edit_citation.setFocus()
                text_edit_citation.selectAll()
                text_edit_citation.copy()

            dialog_citation = QDialog(self)

            dialog_citation.setWindowTitle(self.tr('Citation'))

            dialog_citation.setFixedSize(dialog_citation.sizeHint().width(), 160)

            label_citation = QLabel(self.tr('If you publish work that uses Wordless, please cite Wordless as follows.'), self)
            label_citation_sys = QLabel(self.tr('Citation System:'), self)
            combo_box_citation_sys = QComboBox(self)
            text_edit_citation = QTextEdit(self)

            button_copy = QPushButton(self.tr('Copy'), self)
            button_close = QPushButton(self.tr('Close'), self)

            combo_box_citation_sys.addItems([
                                                 self.tr('MLA (8th Edition)'),
                                                 self.tr('APA (6th Edition)'),
                                                 self.tr('Chicago (17th Edition)'),
                                                 self.tr('GB (GB/T 7714—2015)')
                                            ])

            button_copy.setFixedWidth(100)
            button_close.setFixedWidth(100)

            text_edit_citation.setReadOnly(True)

            combo_box_citation_sys.currentTextChanged.connect(citation_sys_changed)
            button_copy.clicked.connect(copy)
            button_close.clicked.connect(dialog_citation.accept)

            layout_citation = QGridLayout()
            layout_citation.addWidget(label_citation, 0, 0, 1, 2)
            layout_citation.addWidget(label_citation_sys, 1, 0)
            layout_citation.addWidget(combo_box_citation_sys, 1, 1)
            layout_citation.addWidget(text_edit_citation, 2, 0, 1, 2)
            layout_citation.addWidget(button_copy, 3, 0, Qt.AlignHCenter)
            layout_citation.addWidget(button_close, 3, 1, Qt.AlignHCenter)

            dialog_citation.setLayout(layout_citation)

            citation_sys_changed()

            dialog_citation.exec_()

        def acknowledgements():
            QMessageBox.information(self,
                                    self.tr('Acknowledgements'),
                                    self.tr('''
                                            <div style="line-height: 1.5; margin-bottom: 5px;">Thanks a million for the following open-source projects on which Wordless is built on:</div>
                                            <table>
                                              <tr style="font-weight: bold;">
                                                <td>Name</td>
                                                <td>Version</td>
                                                <td>Author</td>
                                                <td>License</td>
                                              </tr>
                                              <tr>
                                                <td><a href="https://www.python.org/">Python</a></td>
                                                <td>3.6.6</td>
                                                <td><a href="https://www.python.org/psf/">Python Software Foundation</a></td>
                                                <td><a href="https://docs.python.org/3.6/license.html">PSF</a></td>
                                              </tr>
                                              <tr>
                                                <td><a href="https://www.crummy.com/software/BeautifulSoup/">Beautiful Soup</a></td>
                                                <td>4.6.3</td>
                                                <td><a href="https://www.crummy.com/self/contact.html">Leonard Richardson</a></td>
                                                <td><a href="https://bazaar.launchpad.net/~leonardr/beautifulsoup/bs4/view/head:/LICENSE">MIT</a></td>
                                              </tr>
                                              <tr>
                                                <td><a href="https://matplotlib.org/">Matplotlib</a></td>
                                                <td>2.2.3</td>
                                                <td><a href="https://github.com/matplotlib/matplotlib#contact">Matplotlib Development Team</a></td>
                                                <td><a href="https://matplotlib.org/users/license.html">Matplotlib</a></td>
                                              </tr>
                                              <tr>
                                                <td><a href="http://www.nltk.org/">NLTK</a></td>
                                                <td>3.3</td>
                                                <td><a href="http://www.nltk.org/contribute.html">NLTK Project</a></td>
                                                <td><a href="https://github.com/nltk/nltk/blob/develop/LICENSE.txt">Apache-2.0</a></td>
                                              </tr>
                                              <tr>
                                                <td><a href="http://networkx.github.io/">NetworkX</a></td>
                                                <td>2.1</td>
                                                <td><a href="https://github.com/networkx/networkx#license">NetworkX Developers</a></td>
                                                <td><a href="https://github.com/networkx/networkx/blob/master/LICENSE.txt">BSD-3-Clause</a></td>
                                              </tr>
                                              <tr>
                                                <td><a href="http://www.numpy.org/">NumPy</a></td>
                                                <td>1.15.1</td>
                                                <td>NumPy Developers</td>
                                                <td><a href="http://www.numpy.org/license.html">NumPy</a></td>
                                              </tr>
                                              <tr>
                                                <td><a href="https://www.riverbankcomputing.com/software/pyqt/intro">PyQt</a></td>
                                                <td>5.11.2</td>
                                                <td><a href="mailto:info@riverbankcomputing.com">Riverbank Computing Limited</a></td>
                                                <td><a href="http://pyqt.sourceforge.net/Docs/PyQt5/introduction.html#license">GPL-3.0</a></td>
                                              </tr>
                                              <tr>
                                                <td><a href="https://github.com/chardet/chardet">chardet</a></td>
                                                <td>3.0.4</td>
                                                <td><a href="mailto:dan.blanchard@gmail.com">Daniel Blanchard</a></td>
                                                <td><a href="https://github.com/chardet/chardet/blob/master/LICENSE">LGPL-2.1</a></td>
                                              </tr>
                                              <tr>
                                                <td><a href="https://github.com/Mimino666/langdetect">langdetect</a></td>
                                                <td>1.0.7</td>
                                                <td><a href="mailto:michal.danilak@gmail.com">Michal "Mimino" Danilak</a></td>
                                                <td><a href="https://github.com/Mimino666/langdetect/blob/master/LICENSE">Apache-2.0</a></td>
                                              </tr>
                                              <tr>
                                                <td><a href="https://lxml.de/">lxml</a></td>
                                                <td>4.2.4</td>
                                                <td><a href="http://consulting.behnel.de/">Stefan Behnel</a></td>
                                                <td><a href="https://github.com/lxml/lxml/blob/master/doc/licenses/BSD.txt">BSD-3-Clause</a></td>
                                              </tr>
                                              <tr>
                                                <td><a href="https://openpyxl.readthedocs.io/en/stable/#">openpyxl</a></td>
                                                <td>2.5.5</td>
                                                <td>Eric Gazoni, <a href="mailto:charlie.clark@clark-consulting.eu">Charlie Clark</a></td>
                                                <td><a href="https://bitbucket.org/openpyxl/openpyxl/src/5983d4ba5c18b85171185e8b1ca136876ec52864/LICENCE.rst?at=default&fileviewer=file-view-default">MIT</a></td>
                                              </tr>
                                              <tr>
                                                <td><a href="https://github.com/fxsjy/jieba">“结巴”中文分词</a></td>
                                                <td>0.39</td>
                                                <td><a href="mailto:ccnusjy@gmail.com">Sun Junyi</a></td>
                                                <td><a href="https://github.com/fxsjy/jieba/blob/master/LICENSE">MIT</a></td>
                                              </tr>
                                            </table>
                                            '''),
                                    QMessageBox.Ok)

        def about_wordless():
            QMessageBox.about(self,
                              self.tr('About Wordless'),
                              self.tr('''
                                      <div style="line-height: 1.2; text-align: center">
                                        <div style="margin-bottom: 5px; font-size: 16px; font-weight: bold;">Wordless Version 1.0</div>
                                        <div style="margin-bottom: 5px;">An integrated tool for language & translation studies.</div>
                                        <div>Designed and Developed by Ye Lei (叶磊)</div>
                                        <hr style="margin-bottom: 5px">
                                        <div style="margin-bottom: 5px">Licensed under GPL Version 3.0</div>
                                        <div>Copyright (C) 2018 Ye Lei</div>
                                      </div>'''))

        menu = self.menuBar()
        menu_file = menu.addMenu(self.tr('File'))
        menu_pref = menu.addMenu(self.tr('Preferences'))
        menu_help = menu.addMenu(self.tr('Help'))

        action_open_file = QAction(self.tr('Open File...'), self)
        action_open_file.setShortcut('Ctrl+O')
        action_open_file.setStatusTip(self.tr('Open a file'))
        action_open_file.triggered.connect(self.open_file)

        action_open_files = QAction(self.tr('Open Files...'), self)
        action_open_files.setStatusTip(self.tr('Open multile files'))
        action_open_files.triggered.connect(self.open_files)

        action_open_dir = QAction(self.tr('Open Folder...'), self)
        action_open_dir.setStatusTip(self.tr('Open a folder'))
        action_open_dir.triggered.connect(self.open_dir)

        action_close_selected = QAction(self.tr('Close Selected File(s)'), self)
        action_close_selected.setStatusTip(self.tr('Close selected file(s)'))
        action_close_selected.triggered.connect(self.close_selected)

        action_close_all = QAction(self.tr('Close All Files'), self)
        action_close_all.setStatusTip(self.tr('Close all files'))
        action_close_all.triggered.connect(self.close_all)

        self.action_reopen = QAction(self.tr('Reopen Closed File(s)'), self)
        self.action_reopen.setStatusTip(self.tr('Reopen closed file(s)'))
        self.action_reopen.triggered.connect(self.reopen)

        action_exit = QAction(self.tr('Exit...'), self)
        action_exit.setStatusTip(self.tr('Exit the program'))
        action_exit.triggered.connect(lambda: exit(self))

        self.action_reopen.setEnabled(False)

        menu_file.addAction(action_open_file)
        menu_file.addAction(action_open_files)
        menu_file.addAction(action_open_dir)
        menu_file.addSeparator()
        menu_file.addAction(action_close_selected)
        menu_file.addAction(action_close_all)
        menu_file.addSeparator()
        menu_file.addAction(self.action_reopen)
        menu_file.addSeparator()
        menu_file.addAction(action_exit)

        action_language = QAction(self.tr('Language'), self)
        action_language.setStatusTip(self.tr('Change display language'))

        action_settings = QAction(self.tr('Settings'), self)
        action_settings.setStatusTip(self.tr('Change settings'))
        action_settings.triggered.connect(self.wordless_settings.settings_load)

        action_show_status_bar = QAction(self.tr('Show Status Bar'), self, checkable = True)
        action_show_status_bar.setChecked(True)
        action_show_status_bar.setStatusTip(self.tr('Show/Hide the status bar'))
        action_show_status_bar.triggered.connect(lambda: show_status_bar(self))

        menu_pref.addAction(action_settings)
        menu_pref.addSeparator()
        menu_pref.addAction(action_show_status_bar)

        action_need_help = QAction(self.tr('Need Help?'), self)
        action_need_help.setStatusTip(self.tr('Show help information'))
        action_need_help.triggered.connect(need_help)

        action_feedback = QAction(self.tr('Feedback'), self)
        action_feedback.setStatusTip(self.tr('Show information about feedback'))
        action_feedback.triggered.connect(feedback)

        action_citation = QAction(self.tr('Citation'), self)
        action_citation.setStatusTip(self.tr('Show information about citation'))
        action_citation.triggered.connect(citation)

        action_acknowledgements = QAction(self.tr('Acknowledgements'), self)
        action_acknowledgements.setStatusTip(self.tr('Show acknowledgements'))
        action_acknowledgements.triggered.connect(acknowledgements)

        action_about_wordless = QAction(self.tr('About Wordless'), self)
        action_about_wordless.setStatusTip(self.tr('Show information about Wordless'))
        action_about_wordless.triggered.connect(about_wordless)

        menu_help.addAction(action_need_help)
        menu_help.addAction(action_feedback)
        menu_help.addSeparator()
        menu_help.addAction(action_citation)
        menu_help.addSeparator()
        menu_help.addAction(action_acknowledgements)
        menu_help.addAction(action_about_wordless)

    def init_central_widget(self):
        central_widget = QWidget(self)

        self.groupbox_files = groupbox_files.init(self)

        self.layout_central_widget = QGridLayout()
        self.layout_central_widget.addWidget(self.init_tabs(), 0, 0)
        self.layout_central_widget.addWidget(self.groupbox_files, 1, 0)

        self.layout_central_widget.setRowStretch(0, 5)
        self.layout_central_widget.setRowStretch(1, 1)

        central_widget.setLayout(self.layout_central_widget)

        self.setCentralWidget(central_widget)

    def init_tabs(self):
        def current_tab_changed():
            if tabs.currentIndex() == 5:
                self.groupbox_files.hide()

                self.layout_central_widget.setRowStretch(1, 0)
            else:
                self.groupbox_files.show()

                self.layout_central_widget.setRowStretch(1, 1)

        tabs = QTabWidget(self)

        tabs.addTab(tab_overview.init(self), self.tr('Overview'))
        tabs.addTab(tab_concordancer.init(self), self.tr('Concordancer'))
        tabs.addTab(tab_word_cluster.init(self), self.tr('Word Cluster'))
        tabs.addTab(tab_wordlist.init(self), self.tr('Wordlist'))
        tabs.addTab(tab_ngrams.init(self), self.tr('N-Grams'))
        tabs.addTab(tab_semantics.init(self), self.tr('Semantics'))

        tabs.currentChanged.connect(current_tab_changed)

        return tabs

if __name__ == '__main__':
    app = QApplication(sys.argv)

    wordless_main = Wordless_Main()
    wordless_main.showMaximized()

    sys.exit(app.exec_())
