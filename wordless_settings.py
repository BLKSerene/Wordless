#
# Wordless: Settings
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import copy
import os
import pickle

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import nltk

from wordless_utils import *

class Wordless_Settings(QDialog):
    def __init__(self, parent):
        def item_clicked(item):
            self.settings_general.hide()
            self.settings_lemmatization.hide()

            if item.text(0) == 'General':
                self.settings_general.show()
            elif item.text(0) == 'Lemmatization':
                self.settings_lemmatization.show()

        super().__init__(parent)

        self.main = parent

        self.setWindowTitle(self.tr('Settings'))

        self.accepted.connect(self.settings_apply)

        self.tree_settings = wordless_tree.Wordless_Tree(self)

        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('General')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('Lemmatization')]))

        self.tree_settings.itemClicked.connect(item_clicked)

        button_restore_defaults = QPushButton(self.tr('Restore Defaults'), self)
        button_save = QPushButton(self.tr('Save'), self)
        button_apply = QPushButton(self.tr('Apply'), self)
        button_cancel = QPushButton(self.tr('Cancel'), self)

        button_restore_defaults.setFixedWidth(150)
        button_save.setFixedWidth(100)
        button_cancel.setFixedWidth(100)
        button_apply.setFixedWidth(100)

        button_restore_defaults.clicked.connect(self.restore_defaults)
        button_save.clicked.connect(self.accept)
        button_apply.clicked.connect(self.settings_apply)
        button_cancel.clicked.connect(self.reject)

        layout_settings_buttons = QGridLayout()
        layout_settings_buttons.addWidget(button_restore_defaults, 0, 0)
        layout_settings_buttons.addWidget(button_save, 0, 1)
        layout_settings_buttons.addWidget(button_apply, 0, 2)
        layout_settings_buttons.addWidget(button_cancel, 0, 3)

        layout_settings = QGridLayout()
        layout_settings.addWidget(self.tree_settings, 0, 0)
        layout_settings.addWidget(self.init_settings_general(), 0, 1)
        layout_settings.addWidget(self.init_settings_lemmatization(), 0, 1)
        layout_settings.addLayout(layout_settings_buttons, 1, 0, 1, 2, Qt.AlignRight)

        layout_settings.setColumnStretch(0, 1)
        layout_settings.setColumnStretch(1, 4)

        self.setLayout(layout_settings)

    def init_settings_general(self):
        self.settings_general = QWidget(self)

        group_box_encoding = QGroupBox(self.tr('Default Encodings'))

        self.label_encoding_input = QLabel(self.tr('Input Encoding:'), self)
        self.combo_box_encoding_input = wordless_widgets.Wordless_Combo_Box_Encoding(self.main)
        self.label_encoding_output = QLabel(self.tr('Output Encoding:'), self)
        self.combo_box_encoding_output = wordless_widgets.Wordless_Combo_Box_Encoding(self.main)

        layout_encoding = QGridLayout()
        layout_encoding.addWidget(self.label_encoding_input, 0, 0)
        layout_encoding.addWidget(self.combo_box_encoding_input, 0, 1)
        layout_encoding.addWidget(self.label_encoding_output, 1, 0)
        layout_encoding.addWidget(self.combo_box_encoding_output, 1, 1)

        group_box_encoding.setLayout(layout_encoding)

        self.label_precision = QLabel(self.tr('Precision:'), self)
        self.spin_box_precision = QSpinBox(self)

        self.spin_box_precision.setRange(0, 10)

        layout_settings_general = QGridLayout()
        layout_settings_general.addWidget(group_box_encoding, 0, 0, 1, 2, Qt.AlignTop)
        layout_settings_general.addWidget(self.label_precision, 1, 0, Qt.AlignTop)
        layout_settings_general.addWidget(self.spin_box_precision, 1, 1, Qt.AlignTop)

        self.settings_general.setLayout(layout_settings_general)

        return self.settings_general

    def init_settings_lemmatization(self):
        self.settings_lemmatization = QWidget(self)

        self.layout_settings_lemmatization = QGridLayout()

        self.settings_lemmatization.setLayout(self.layout_settings_lemmatization)

        return self.settings_lemmatization

    def settings_load(self, tab = 'General'):
        self.combo_box_encoding_input.setCurrentText(wordless_misc.convert_encoding(self.main, *self.main.settings['general']['encoding_input']))
        self.combo_box_encoding_output.setCurrentText(wordless_misc.convert_encoding(self.main, *self.main.settings['general']['encoding_output']))

        self.spin_box_precision.setValue(self.main.settings['general']['precision'])

        self.settings_general.hide()
        self.settings_lemmatization.hide()

        self.settings_general.show()

        self.exec()

    def restore_defaults(self):
        self.combo_box_encoding_input.setCurrentText(wordless_misc.convert_encoding(self.main, *self.main.default_settings['general']['encoding_input']))
        self.combo_box_encoding_output.setCurrentText(wordless_misc.convert_encoding(self.main, *self.main.default_settings['general']['encoding_output']))

        self.spin_box_precision.setValue(self.main.default_settings['general']['precision'])

    def settings_apply(self):
        self.main.settings['general']['encoding_input'] = wordless_misc.convert_encoding(self.main, self.combo_box_encoding_input.currentText())
        self.main.settings['general']['encoding_output'] = wordless_misc.convert_encoding(self.main, self.combo_box_encoding_output.currentText())
        self.main.settings['general']['precision'] = self.spin_box_precision.value()

def load_settings(main):
    main.file_langs = {
        main.tr('Afrikaans'): 'afr',
        main.tr('Albanian'): 'sqi',
        main.tr('Arabic'): 'ara',
        main.tr('Bengali'): 'ben',
        main.tr('Bulgarian'): 'bul',
        main.tr('Catalan'): 'cat',
        main.tr('Chinese (Simplified)'): 'zho-cn',
        main.tr('Chinese (Traditional)'): 'zho-tw',
        main.tr('Croatian'): 'hrv',
        main.tr('Czech'): 'ces',
        main.tr('Danish'): 'dan',
        main.tr('Dutch'): 'nld',
        main.tr('English'): 'eng',
        main.tr('Estonian'): 'est',
        main.tr('Finnish'): 'fin',
        main.tr('French'): 'fra',
        main.tr('Gaelic (Scots)'): 'gla',
        main.tr('German'): 'deu',
        main.tr('Greek'): 'ell',
        main.tr('Gujarati'): 'guj',
        main.tr('Hebrew'): 'heb',
        main.tr('Hindi'): 'hin',
        main.tr('Hungarian'): 'hun',
        main.tr('Indonesian'): 'ind',
        main.tr('Italian'): 'ita',
        main.tr('Japanese'): 'jpn',
        main.tr('Kannada'): 'kan',
        main.tr('Korean'): 'kor',
        main.tr('Latvian'): 'lav',
        main.tr('Lithuanian'): 'lit',
        main.tr('Macedonian'): 'mkd',
        main.tr('Malayalam'): 'mal',
        main.tr('Manx'): 'glv',
        main.tr('Marathi'): 'mar',
        main.tr('Nepali'): 'nep',
        main.tr('Norwegian'): 'nno',
        main.tr('Panjabi/Punjabi'): 'pan',
        main.tr('Persian'): 'fas',
        main.tr('Polish'): 'pol',
        main.tr('Portuguese'): 'por',
        main.tr('Romanian'): 'ron',
        main.tr('Russian'): 'rus',
        main.tr('Slovak'): 'slk',
        main.tr('Slovenian'): 'slv',
        main.tr('Somali'): 'som',
        main.tr('Spanish (Castilian)'): 'spa',
        main.tr('Swahili'): 'swa',
        main.tr('Swedish'): 'swe',
        main.tr('Tagalog'): 'tgl',
        main.tr('Tamil'): 'tam',
        main.tr('Telugu'): 'tel',
        main.tr('Thai'): 'tha',
        main.tr('Turkish'): 'tur',
        main.tr('Ukrainian'): 'ukr',
        main.tr('Urdu'): 'urd',
        main.tr('Vietnamese'): 'vie',
        main.tr('Welsh'): 'cym'
    }

    main.file_exts = {
        '.txt': main.tr('Text File (*.txt)'),
        '.htm': main.tr('HTML Page (*.htm; *.html)'),
        '.html': main.tr('HTML Page (*.htm; *.html)')
    }

    main.file_encodings = {
        main.tr('All Languages(UTF-8 Without BOM)'): 'utf_8',
        main.tr('All Languages(UTF-8 With BOM)'): 'utf_8_sig',
        main.tr('All Languages(UTF-16)'): 'utf_16',
        main.tr('All Languages(UTF-16 Big Endian)'): 'utf_16_be',
        main.tr('All Languages(UTF-16 Little Endian)'): 'utf_16_le',
        main.tr('All Languages(UTF-32)'): 'utf_32',
        main.tr('All Languages(UTF-32 Big Endian)'): 'utf_32_be',
        main.tr('All Languages(UTF-32 Little Endian)'): 'utf_32_le',
        main.tr('All Languages(UTF-7)'): 'utf_7',
        main.tr('All Languages(CP65001)'): 'cp65001',

        main.tr('Baltic Languages(CP775)'): 'cp775',
        main.tr('Baltic Languages(Windows-1257)'): 'cp1257',
        main.tr('Baltic Languages(ISO-8859-4)'): 'iso8859_4',
        main.tr('Baltic Languages(ISO-8859-13)'): 'iso8859_13',

        main.tr('Celtic Languages(ISO-8859-14)'): 'iso8859_14',

        main.tr('Nordic Languages(ISO-8859-10)'): 'iso8859_10',

        main.tr('Europe(HP Roman-8)'): 'hp_roman8',

        main.tr('Central Europe(Mac OS Central European)'): 'mac_centeuro',
        main.tr('Central Europe(Mac OS Latin 2)'): 'mac_latin2',

        main.tr('Central and Eastern Europe(CP852)'): 'cp852',
        main.tr('Central and Eastern Europe(Windows-1250)'): 'cp1250',
        main.tr('Central and Eastern Europe(ISO-8859-2)'): 'iso8859_2',
        main.tr('Central and Eastern Europe(Mac Latin)'): 'mac_latin2',

        main.tr('South-Eastern Europe(ISO-8859-16)'): 'iso8859_16',

        main.tr('Western Europe(EBCDIC 500)'): 'cp500',
        main.tr('Western Europe(CP850)'): 'cp850',
        main.tr('Western Europe(CP858)'): 'cp858',
        main.tr('Western Europe(CP1140)'): 'cp1140',
        main.tr('Western Europe(Windows-1252)'): 'windows_1252',
        main.tr('Western Europe(ISO-2022-JP-2)'): 'iso2022_jp_2',
        main.tr('Western Europe(ISO-8859-1)'): 'iso_8859_1',
        main.tr('Western Europe(ISO-8859-15)'): 'iso_8859_15',
        main.tr('Western Europe(Mac OS Roman)'): 'mac_roman',

        main.tr('Arabic(CP720)'): 'cp720',
        main.tr('Arabic(CP864)'): 'cp864',
        main.tr('Arabic(Windows-1256)'): 'cp1256',
        main.tr('Arabic(ISO-8859-6)'): 'iso_8859_6',
        main.tr('Arabic(Mac OS Arabic)'): 'mac_arabic',

        main.tr('Bulgarian(IBM855)'): 'cp855',
        main.tr('Bulgarian(Windows-1251)'): 'windows_1251',
        main.tr('Bulgarian(ISO-8859-5)'): 'iso_8859_5',
        main.tr('Bulgarian(Mac OS Cyrillic)'): 'mac_cyrillic',

        main.tr('Byelorussian(IBM855)'): 'cp855',
        main.tr('Byelorussian(Windows-1251)'): 'cp1251',
        main.tr('Byelorussian(ISO-8859-5)'): 'iso_8859_5',
        main.tr('Byelorussian(Mac OS Cyrillic)'): 'mac_cyrillic',

        main.tr('Canadian(CP863)'): 'cp863',

        main.tr('Simplified Chinese(GB2312)'): 'gb2312',
        main.tr('Simplified Chinese(HZ)'): 'hz_gb_2312',
        main.tr('Simplified Chinese(ISO-2022-JP-2)'): 'iso2022_jp_2',

        main.tr('Traditional Chinese(Big-5)'): 'big5',
        main.tr('Traditional Chinese(Big5-HKSCS)'): 'big5hkscs',
        main.tr('Traditional Chinese(CP950)'): 'cp950',

        main.tr('Unified Chinese(GBK)'): 'gbk',
        main.tr('Unified Chinese(GB18030)'): 'gb18030',

        main.tr('Croatian(Mac OS Croatian)'): 'mac_croatian',

        main.tr('Danish(CP865)'): 'cp865',

        main.tr('English(ASCII)'): 'ascii',
        main.tr('English(EBCDIC 037)'): 'cp037',
        main.tr('English(CP437)'): 'cp437',

        main.tr('Esperanto(ISO-8859-3)'): 'iso_8859_3',

        main.tr('German(EBCDIC 273)'): 'cp273',

        main.tr('Greek(CP737)'): 'cp737',
        main.tr('Greek(CP869)'): 'cp869',
        main.tr('Greek(CP875)'): 'cp875',
        main.tr('Greek(Windows-1253)'): 'windows_1253',
        main.tr('Greek(ISO-2022-JP-2)'): 'iso2022_jp_2',
        main.tr('Greek(ISO-8859-7)'): 'iso_8859_7',
        main.tr('Greek(Mac OS Greek)'): 'mac_greek',

        main.tr('Hebrew(EBCDIC 424)'): 'cp424',
        main.tr('Hebrew(CP856)'): 'cp856',
        main.tr('Hebrew(CP862)'): 'cp862',
        main.tr('Hebrew(Windows-1255)'): 'windows_1255',
        main.tr('Hebrew(ISO-8859-8)'): 'iso_8859_8',

        main.tr('Icelandic(CP861)'): 'cp861',
        main.tr('Icelandic(Mac OS Icelandic)'): 'mac_iceland',

        main.tr('Japanese(CP932)'): 'cp932',
        main.tr('Japanese(EUC-JP)'): 'euc_jp',
        main.tr('Japanese(EUC-JIS-2004)'): 'euc_jis_2004',
        main.tr('Japanese(EUC-JISx0213)'): 'euc_jisx0213',
        main.tr('Japanese(ISO-2022-JP)'): 'iso_2022_jp',
        main.tr('Japanese(ISO-2022-JP-1)'): 'iso2022_jp_1',
        main.tr('Japanese(ISO-2022-JP-2)'): 'iso2022_jp_2',
        main.tr('Japanese(ISO-2022-JP-2)'): 'iso2022_jp_2004',
        main.tr('Japanese(ISO-2022-JP-3)'): 'iso2022_jp_3',
        main.tr('Japanese(ISO-2022-JP-EXT)'): 'iso2022_jp_ext',
        main.tr('Japanese(Shift_JIS)'): 'shift_jis',
        main.tr('Japanese(Shift_JIS-2004)'): 'shift_jis_2004',
        main.tr('Japanese(Shift_JISx0213)'): 'shift_jisx0213',

        main.tr('Kazakh(KZ-1048)'): 'kz1048',
        main.tr('Kazakh(PTCP154)'): 'ptcp154',

        main.tr('Korean(Windows-949)'): 'cp949',
        main.tr('Korean(EUC-KR)'): 'euc_kr',
        main.tr('Korean(ISO-2022-JP-2)'): 'iso2022_jp_2',
        main.tr('Korean(ISO-2022-KR)'): 'iso_2022_kr',
        main.tr('Korean(JOHAB)'): 'johab',

        main.tr('Macedonian(IBM855)'): 'cp855',
        main.tr('Macedonian(Windows-1251)'): 'cp1251',
        main.tr('Macedonian(ISO-8859-5)'): 'iso_8859_5',
        main.tr('Macedonian(Mac OS Cyrillic)'): 'maccyrillic',

        main.tr('Maltese(ISO-8859-3)'): 'iso_8859_3',

        main.tr('Norwegian(CP865)'): 'cp865',

        main.tr('Persian(Mac OS Farsi)'): 'mac_farsi',

        main.tr('Portuguese(CP860)'): 'cp860',

        main.tr('Romanian(Mac OS Romanian)'): 'mac_romanian',

        main.tr('Russian(IBM855)'): 'ibm855',
        main.tr('Russian(IBM866)'): 'ibm866',
        main.tr('Russian(Windows-1251)'): 'windows_1251',
        main.tr('Russian(ISO-8859-5)'): 'iso_8859_5',
        main.tr('Russian(KOI8-R)'): 'koi8_r',
        main.tr('Russian(Mac OS Cyrillic)'): 'maccyrillic',

        main.tr('Serbian(IBM855)'): 'cp855',
        main.tr('Serbian(Windows-1251)'): 'cp1251',
        main.tr('Serbian(ISO-8859-5)'): 'iso8859_5',
        main.tr('Serbian(Mac OS Cyrillic)'): 'maccyrillic',

        main.tr('Tajik(KOI8-T)'): 'koi8_t',

        main.tr('Thai(CP874)'): 'cp874',
        main.tr('Thai(ISO-8859-11)'): 'iso8859_11',
        main.tr('Thai(TIS-620)'): 'tis_620',

        main.tr('Turkish(CP857)'): 'cp857',
        main.tr('Turkish(EBCDIC 1026)'): 'cp1026',
        main.tr('Turkish(Windows-1254)'): 'cp1254',
        main.tr('Turkish(ISO-8859-9)'): 'iso_8859_9',
        main.tr('Turkish(Mac OS Turkish)'): 'mac_turkish',

        main.tr('Ukranian(CP1125)'): 'cp1125',
        main.tr('Ukranian(KOI8-U)'): 'koi8_u',

        main.tr('Urdu(CP1006)'): 'cp1006',
        main.tr('Urdu(Mac OS Farsi)'): 'mac_farsi',

        main.tr('Vietnamese(CP1258)'): 'cp1258'
    }

    main.lemmatization = {
        'English': ['NLTK (NLTK Project)', 'Lemmatization List (Michal Boleslav Měchura)'],
        'Austurian': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Catalan': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Czech': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Estonian': ['Lemmatization List (Michal Boleslav Měchura)'],
        'French': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Galician': ['Lemmatization List (Michal Boleslav Měchura)'],
        'German': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Hungarian': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Irish': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Manx': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Italian': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Persian': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Polish': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Portuguese': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Romanian': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Scottish Gaelic': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Slovak': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Slovene': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Spanish': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Swedish': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Ukrainian': ['Lemmatization List (Michal Boleslav Měchura)'],
        'Welsh': ['Lemmatization List (Michal Boleslav Měchura)']
    }

    main.style_dialog = '''
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

            table th {
              font-weight: bold;
            }
          </style>
        </head>
    '''

    main.assoc_measures_bigram = {
        main.tr('Frequency'): nltk.collocations.BigramAssocMeasures().raw_freq,
        main.tr('Student\'s T-test'): nltk.collocations.BigramAssocMeasures().student_t,
        main.tr('Pearson\'s Chi-squared Test'): nltk.collocations.BigramAssocMeasures().chi_sq,
        main.tr('Phi Coefficient'): nltk.collocations.BigramAssocMeasures().phi_sq,
        main.tr('Pointwise Mutual Information'): nltk.collocations.BigramAssocMeasures().pmi,
        main.tr('Likelihood Ratios'): nltk.collocations.BigramAssocMeasures().likelihood_ratio,
        main.tr('Poisson-Stirling'): nltk.collocations.BigramAssocMeasures().poisson_stirling,
        main.tr('Jaccard Index'): nltk.collocations.BigramAssocMeasures().jaccard,
        main.tr('Fisher\'s Exact Test'): nltk.collocations.BigramAssocMeasures().fisher,
        main.tr('Dice\'s coefficient'): nltk.collocations.BigramAssocMeasures().dice
    }

    main.assoc_measures_trigram = {
        main.tr('Frequency'): nltk.collocations.TrigramAssocMeasures().raw_freq,
        main.tr('Student\'s T-test'): nltk.collocations.TrigramAssocMeasures().student_t,
        main.tr('Pearson\'s Chi-squared Test'): nltk.collocations.TrigramAssocMeasures().chi_sq,
        main.tr('Pointwise Mutual Information'): nltk.collocations.TrigramAssocMeasures().pmi,
        main.tr('Likelihood Ratios'): nltk.collocations.TrigramAssocMeasures().likelihood_ratio,
        main.tr('Poisson-Stirling'): nltk.collocations.TrigramAssocMeasures().poisson_stirling,
        main.tr('Jaccard Index'): nltk.collocations.TrigramAssocMeasures().jaccard
    }

    main.assoc_measures_quadgram = {
        main.tr('Frequency'): nltk.collocations.QuadgramAssocMeasures().raw_freq,
        main.tr('Student\'s T-test'): nltk.collocations.QuadgramAssocMeasures().student_t,
        main.tr('Pearson\'s Chi-squared Test'): nltk.collocations.QuadgramAssocMeasures().chi_sq,
        main.tr('Pointwise Mutual Information'): nltk.collocations.QuadgramAssocMeasures().pmi,
        main.tr('Likelihood Ratios'): nltk.collocations.QuadgramAssocMeasures().likelihood_ratio,
        main.tr('Poisson-Stirling'): nltk.collocations.QuadgramAssocMeasures().poisson_stirling,
        main.tr('Jaccard Index'): nltk.collocations.QuadgramAssocMeasures().jaccard
    }

    main.default_settings = {
        'general': {
            'encoding_input': ('utf_8', main.tr('All Languages')),
            'encoding_output': ('utf_8', main.tr('All Languages')),

            'font_monospaced': 'Consolas',

            'precision': 2,
            'style_highlight': 'border: 1px solid Red;'
        },
    
        'file': {
            'files_open': [],
            'files_closed': []
        },

        'lemmatization': {
            'English': 'NLTK (NLTK Project)',
            'Austurian': 'Lemmatization List (Michal Boleslav Měchura)',
            'Catalan': 'Lemmatization List (Michal Boleslav Měchura)',
            'Czech': 'Lemmatization List (Michal Boleslav Měchura)',
            'Estonian': 'Lemmatization List (Michal Boleslav Měchura)',
            'French': 'Lemmatization List (Michal Boleslav Měchura)',
            'Galician': 'Lemmatization List (Michal Boleslav Měchura)',
            'German': 'Lemmatization List (Michal Boleslav Měchura)',
            'Hungarian': 'Lemmatization List (Michal Boleslav Měchura)',
            'Irish': 'Lemmatization List (Michal Boleslav Měchura)',
            'Manx': 'Lemmatization List (Michal Boleslav Měchura)',
            'Italian': 'Lemmatization List (Michal Boleslav Měchura)',
            'Persian': 'Lemmatization List (Michal Boleslav Měchura)',
            'Polish': 'Lemmatization List (Michal Boleslav Měchura)',
            'Portuguese': 'Lemmatization List (Michal Boleslav Měchura)',
            'Romanian': 'Lemmatization List (Michal Boleslav Měchura)',
            'Scottish Gaelic': 'Lemmatization List (Michal Boleslav Měchura)',
            'Slovak': 'Lemmatization List (Michal Boleslav Měchura)',
            'Slovene': 'Lemmatization List (Michal Boleslav Měchura)',
            'Spanish': 'Lemmatization List (Michal Boleslav Měchura)',
            'Swedish': 'Lemmatization List (Michal Boleslav Měchura)',
            'Ukrainian': 'Lemmatization List (Michal Boleslav Měchura)',
            'Welsh': 'Lemmatization List (Michal Boleslav Měchura)'
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
            'words': True,
            'lowercase': True,
            'uppercase': True,
            'title_cased': True,
            'numerals': True,
            'punctuations': False,
    
            'ignore_case': True,
            'lemmatization': True,

            'show_pct': True,
            'show_cumulative': True,
            'show_breakdown': True,

            'rank_no_limit': False,
            'rank_min': 1,
            'rank_max': 50,
            'cumulative': False,
    
            'freq_no_limit': True,
            'freq_min': 0,
            'freq_max': 1000,
            'freq_apply_to': 'Total',
            'len_no_limit': True,
            'len_min': 1,
            'len_max': 20,
            'files_no_limit': True,
            'files_min': 1,
            'files_max': 100
        },
    
        'ngram': {
            'words': True,
            'lowercase': True,
            'uppercase': True,
            'title_cased': True,
            'numerals': True,
            'punctuations': False,
    
            'search_terms': [],
            'keyword_position_no_limit': True,
            'keyword_position_min': 1,
            'keyword_position_max': 2,
            'ignore_case': True,
            'lemmatization': True,
            'whole_word': True,
            'regex': False,
            'multi_search': False,
            'show_all': False,

            'ngram_size_sync': False,
            'ngram_size_min': 2,
            'ngram_size_max': 2,
            'allow_skipped_tokens': 0,

            'show_pct': True,
            'show_cumulative': True,
            'show_breakdown': True,
    
            'rank_no_limit': False,
            'rank_min': 1,
            'rank_max': 50,
            'cumulative': False,
    
            'freq_no_limit': True,
            'freq_min': 0,
            'freq_max': 1000,
            'freq_apply_to': 'Total',
            'len_no_limit': True,
            'len_min': 1,
            'len_max': 20,
            'files_no_limit': True,
            'files_min': 1,
            'files_max': 100
        },

        'collocation': {
            'words': True,
            'lowercase': True,
            'uppercase': True,
            'title_cased': True,
            'numerals': True,
            'punctuations': False,
    
            'search_terms': [],
            'ignore_case': True,
            'lemmatization': True,
            'whole_word': True,
            'regex': False,
            'multi_search': False,
            'show_all': False,

            'window_sync': False,
            'window_left': ['L', 1],
            'window_right': ['R', 1],
            'search_for': main.tr('Bigrams'),
            'assoc_measure': main.tr('Pearson\'s Chi-squared Test'),

            'show_pct': True,
            'show_cumulative': True,
            'show_breakdown': True,

    
            'rank_no_limit': False,
            'rank_min': 1,
            'rank_max': 50,
            'cumulative': False,

            'score_no_limit': True,
            'score_min': 1,
            'score_max': 1000,
            'score_apply_to': 'Total',
            'len_no_limit': True,
            'len_min': 1,
            'len_max': 20,
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

    if os.path.exists('wordless_settings.pkl'):
        with open(r'wordless_settings.pkl', 'rb') as f:
            main.settings = pickle.load(f)
    else:
        main.settings = copy.deepcopy(main.default_settings)

    main.wordless_settings = Wordless_Settings(main)
