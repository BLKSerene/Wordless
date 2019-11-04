#
# Wordless: Dialogs - Help
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import platform
import re

import requests

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_dialogs import wordless_dialog
from wordless_utils import wordless_threading
from wordless_widgets import (wordless_box, wordless_label, wordless_layout,
                              wordless_table)

class Wordless_Dialog_Citing(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Citing'),
                         width = 420,
                         no_button = True)

        self.label_citing = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    If you publish work that uses Wordless, please cite as follows.
                </div>
            '''),
            self
        )

        self.label_citation_sys = QLabel(self.tr('Citation System:'), self)
        self.combo_box_citation_sys = wordless_box.Wordless_Combo_Box(self)
        self.text_edit_citing = QTextEdit(self)
    
        self.button_copy = QPushButton(self.tr('Copy'), self)
        self.button_close = QPushButton(self.tr('Close'), self)
    
        self.combo_box_citation_sys.addItems([
            self.tr('MLA (8th Edition)'),
            self.tr('APA (6th Edition)'),
            self.tr('GB (GB/T 7714—2015)')
        ])
    
        self.button_copy.setFixedWidth(100)
        self.button_close.setFixedWidth(100)
    
        self.text_edit_citing.setFixedHeight(100)
        self.text_edit_citing.setReadOnly(True)
    
        self.combo_box_citation_sys.currentTextChanged.connect(self.citation_sys_changed)
    
        self.button_copy.clicked.connect(self.copy)
        self.button_close.clicked.connect(self.accept)
    
        layout_citation_sys = wordless_layout.Wordless_Layout()
        layout_citation_sys.addWidget(self.label_citation_sys, 0, 0)
        layout_citation_sys.addWidget(self.combo_box_citation_sys, 0, 1)
    
        layout_citation_sys.setColumnStretch(2, 1)
    
        self.wrapper_info.layout().addWidget(self.label_citing, 0, 0, 1, 2)
        self.wrapper_info.layout().addLayout(layout_citation_sys, 1, 0, 1, 2)
        self.wrapper_info.layout().addWidget(self.text_edit_citing, 2, 0, 1, 2)
    
        self.wrapper_buttons.layout().addWidget(self.button_copy, 0, 0)
        self.wrapper_buttons.layout().addWidget(self.button_close, 0, 1)

        self.load_settings()

        self.set_fixed_height()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['menu']['help']['citing'])

        self.combo_box_citation_sys.setCurrentText(settings['citation_sys'])

        self.citation_sys_changed()

    def citation_sys_changed(self):
        settings = self.main.settings_custom['menu']['help']['citing']

        settings['citation_sys'] = self.combo_box_citation_sys.currentText()

        if settings['citation_sys'] == self.tr('MLA (8th Edition)'):
            if self.main.ver:
                self.text_edit_citing.setHtml(f'Ye Lei. <i>Wordless</i>, version {self.main.ver}, 2019. <i>Github</i>, https://github.com/BLKSerene/Wordless.')
            else:
                self.text_edit_citing.setHtml('Ye Lei. <i>Wordless</i>, 2019. <i>Github</i>, https://github.com/BLKSerene/Wordless.')
        elif settings['citation_sys'] == self.tr('APA (6th Edition)'):
            if self.main.ver:
                self.text_edit_citing.setHtml(f'Ye, L. (2019). Wordless (Version {self.main.ver}) [Computer software]. Retrieved from https://github.com/BLKSerene/Wordless')
            else:
                self.text_edit_citing.setHtml('Ye, L. (2019). Wordless [Computer software]. Retrieved from https://github.com/BLKSerene/Wordless')
        elif settings['citation_sys'] == self.tr('GB (GB/T 7714—2015)'):
            if self.main.ver:
                self.text_edit_citing.setHtml(f'叶磊. Wordless version {self.main.ver}[CP]. (2019). https://github.com/BLKSerene/Wordless.')
            else:
                self.text_edit_citing.setHtml('叶磊. Wordless[CP]. (2019). https://github.com/BLKSerene/Wordless.')

    def copy(self):
        self.text_edit_citing.setFocus()
        self.text_edit_citing.selectAll()
        self.text_edit_citing.copy()

class Wordless_Dialog_Acks(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Acknowledgments'),
                         width = 550)

        self.ACKS_GENERAL = [
            # Python
            [
                '<a href="https://www.python.org">Python</a>',
                '3.7.5',
                'Guido van Rossum',
                '<a href="https://docs.python.org/3.7/license.html#psf-license-agreement-for-python-release">PSF</a>'
            ],
            # PyInstaller
            [
                '<a href="http://www.pyinstaller.org">PyInstaller</a>',
                '4.0.dev0+46286a1f4',
                'Hartmut Goebel',
                '<a href="https://github.com/pyinstaller/pyinstaller/blob/develop/COPYING.txt">PyInstaller</a>'
            ],
            # PyQt
            [
                '<a href="https://www.riverbankcomputing.com/software/pyqt/intro">PyQt</a>',
                '5.13.1',
                'Riverbank Computing Limited',
                '<a href="http://pyqt.sourceforge.net/Docs/PyQt5/introduction.html#license">GPL-3.0</a>'
            ],
            # pytest
            [
                '<a href="https://pytest.org">pytest</a>',
                '5.2.0',
                'Holger Krekel',
                '<a href="https://github.com/pytest-dev/pytest/blob/master/LICENSE">MIT</a>'
            ]
        ]

        self.ACKS_NLP = [
            # botok
            [
                '<a href="https://github.com/Esukhia/botok">botok</a>',
                '0.6.10',
                'Hélios Drupchen Hildt',
                '<a href="https://github.com/Esukhia/botok/blob/master/LICENSE">Apache-2.0</a>'
            ],
            # jieba
            [
                '<a href="https://github.com/fxsjy/jieba">jieba<br>(“结巴”中文分词)</a>',
                '0.39',
                'Sun Junyi (孙君意)',
                '<a href="https://github.com/fxsjy/jieba/blob/master/LICENSE">MIT</a>'
            ],
            # nagisa
            [
                '<a href="https://github.com/taishi-i/nagisa">nagisa</a>',
                '0.2.4',
                'Taishi Ikeda (池田大志)',
                '<a href="https://github.com/taishi-i/nagisa/blob/master/LICENSE.txt">MIT</a>'
            ],
            # NLTK
            [
                '<a href="http://www.nltk.org">NLTK</a>',
                '3.4.5',
                'Steven Bird, Liling Tan',
                '<a href="https://github.com/nltk/nltk/blob/develop/LICENSE.txt">Apache-2.0</a>'
            ],
            # pymorphy2
            [
                '<a href="https://github.com/kmike/pymorphy2">pymorphy2</a>',
                '0.8',
                'Mikhail Korobov',
                '<a href="https://github.com/kmike/pymorphy2/#pymorphy2">MIT</a>'
            ],
            # PyThaiNLP
            [
                '<a href="https://github.com/PyThaiNLP/pythainlp">PyThaiNLP</a>',
                '2.0.7',
                'Wannaphong Phatthiyaphaibun<br>(วรรณพงษ์ ภัททิยไพบูลย์)',
                '<a href="https://github.com/PyThaiNLP/pythainlp/blob/dev/LICENSE">Apache-2.0</a>'
            ],
            # razdel
            [
                '<a href="https://github.com/natasha/razdel">razdel</a>',
                '0.4.0',
                'Alexander Kukushkin',
                '<a href="https://github.com/natasha/razdel#%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F">MIT</a>'
            ],
            # Sacremoses
            [
                '<a href="https://github.com/alvations/sacremoses">Sacremoses</a>',
                '0.0.35',
                'Liling Tan',
                '<a href="https://github.com/alvations/sacremoses#license">LGPL-2.1</a>'
            ],
            # spaCy
            [
                '<a href="https://spacy.io">spaCy</a>',
                '2.2.2',
                'Matthew Honnibal, Ines Montani',
                '<a href="https://github.com/explosion/spaCy/blob/master/LICENSE">MIT</a>'
            ],
            # syntok
            [
                '<a href="https://github.com/fnl/syntok">syntok</a>',
                '1.2.1',
                'Florian Leitner',
                '<a href="https://github.com/fnl/syntok/blob/master/LICENSE">MIT</a>'
            ],
            # Underthesea
            [
                '<a href="https://github.com/undertheseanlp/underthesea">Underthesea</a>',
                '1.1.17',
                'Vu Anh',
                '<a href="https://github.com/undertheseanlp/underthesea/blob/master/LICENSE">GPL-3.0</a>'
            ]
        ]

        self.ACKS_PLOTTING = [
            # Matplotlib
            [
                '<a href="https://matplotlib.org">Matplotlib</a>',
                '3.1.1',
                'Matplotlib Development Team',
                '<a href="https://matplotlib.org/users/license.html">Matplotlib</a>'
            ],
            # NetworkX
            [
                '<a href="http://networkx.github.io">NetworkX</a>',
                '2.3',
                'Aric Hagberg, Dan Schult, Pieter Swart',
                '<a href="https://github.com/networkx/networkx/blob/master/LICENSE.txt">BSD-3-Clause</a>'
            ],
            # WordCloud
            [
                '<a href="https://amueller.github.io/word_cloud/">WordCloud</a>',
                '1.5.0',
                'Andreas Christian Mueller',
                '<a href="https://github.com/amueller/word_cloud/blob/master/LICENSE">MIT</a>'
            ]
        ]

        self.ACKS_MISC = [
            # Beautiful Soup
            [
                '<a href="https://www.crummy.com/software/BeautifulSoup/">Beautiful Soup</a>',
                '4.8.1',
                'Leonard Richardson',
                '<a href="https://bazaar.launchpad.net/~leonardr/beautifulsoup/bs4/view/head:/LICENSE">MIT</a>'
            ],
            # cChardet
            [
                '<a href="https://github.com/PyYoshi/cChardet">cChardet</a>',
                '2.1.4',
                'Yoshihiro Misawa',
                '<a href="https://github.com/PyYoshi/cChardet/blob/master/COPYING">MPL-1.0/GPL-2.0/LGPL-2.1</a>'
            ],
            # chardet
            [
                '<a href="https://github.com/chardet/chardet">chardet</a>',
                '3.0.4',
                'Daniel Blanchard',
                '<a href="https://github.com/chardet/chardet/blob/master/LICENSE">LGPL-2.1</a>'
            ],
            # langdetect
            [
                '<a href="https://github.com/Mimino666/langdetect">langdetect</a>',
                '1.0.7',
                'Michal Mimino Danilak',
                '<a href="https://github.com/Mimino666/langdetect/blob/master/LICENSE">Apache-2.0</a>'
            ],
            # langid.py
            [
                '<a href="https://github.com/saffsd/langid.py">langid.py</a>',
                '1.1.6',
                'Marco Lui',
                '<a href="https://github.com/saffsd/langid.py/blob/master/LICENSE">BSD-2-Clause</a>'
            ],
            # lxml
            [
                '<a href="https://lxml.de">lxml</a>',
                '4.4.1',
                'Stefan Behnel',
                '<a href="https://github.com/lxml/lxml/blob/master/doc/licenses/BSD.txt">BSD-3-Clause</a>'
            ],
            # NumPy
            [
                '<a href="https://numpy.org">NumPy</a>',
                '1.17.2',
                'NumPy Developers',
                '<a href="http://www.numpy.org/license.html">BSD-3-Clause</a>'
            ],
            # openpyxl
            [
                '<a href="https://openpyxl.readthedocs.io/en/stable/">openpyxl</a>',
                '3.0.0',
                'Eric Gazoni, Charlie Clark',
                '<a href="https://bitbucket.org/openpyxl/openpyxl/src/5983d4ba5c18b85171185e8b1ca136876ec52864/LICENCE.rst">MIT</a>'
            ],
            # python-docx
            [
                '<a href="https://github.com/python-openxml/python-docx">python-docx</a>',
                '0.8.10',
                'Steve Canny',
                '<a href="https://github.com/python-openxml/python-docx/blob/master/LICENSE">MIT</a>'
            ],
            # requests
            [
                '<a href="https://python-requests.org">requests</a>',
                '2.22.0',
                'Kenneth Reitz',
                '<a href="https://github.com/requests/requests/blob/master/LICENSE">Apache-2.0</a>'
            ],
            # SciPy
            [
                '<a href="https://www.scipy.org">SciPy</a>',
                '1.3.1',
                'SciPy Developers',
                '<a href="https://www.scipy.org/scipylib/license.html">BSD-3-Clause</a>'
            ],
            # xlrd
            [
                '<a href="https://github.com/python-excel/xlrd">xlrd</a>',
                '1.2.0',
                'Stephen John Machin',
                '<a href="https://github.com/python-excel/xlrd/blob/master/LICENSE">BSD-3-Clause/BSD-4-Clause</a>'
            ]
        ]

        self.ACKS_DATA = [
            # extra-stopwords
            [
                '<a href="https://github.com/Xangis/extra-stopwords">extra-stopwords</a>',
                '/',
                'Jason Champion',
                '<a href="https://github.com/Xangis/extra-stopwords/blob/master/LICENSE">MIT</a>'
            ],
            # grk-stoplist
            [
                '<a href="https://github.com/pharos-alexandria/grk-stoplist">grk-stoplist</a>',
                '/',
                'Annette von Stockhausen',
                '<a href="https://github.com/pharos-alexandria/grk-stoplist/blob/master/LICENSE">CC0-1.0</a>'
            ],
            # lemmalist-greek
            [
                '<a href="https://github.com/stenskjaer/lemmalist-greek">lemmalist-greek</a>',
                '/',
                'Michael Stenskjær Christensen',
                '<a href="https://github.com/stenskjaer/lemmalist-greek/blob/master/LICENSE">GPL-3.0</a>'
            ],
            # Lemmatization Lists
            [
                '<a href="https://github.com/michmech/lemmatization-lists">Lemmatization Lists</a>',
                '/',
                'Michal Boleslav Měchura',
                '<a href="https://github.com/michmech/lemmatization-lists/blob/master/LICENCE">ODbL</a>'
            ],
            # Stopwords ISO
            [
                '<a href="https://github.com/stopwords-iso/stopwords-iso">Stopwords ISO</a>',
                '0.4.0',
                'Gene Diaz',
                '<a href="https://github.com/stopwords-iso/stopwords-iso/blob/master/LICENSE">MIT</a>'
            ]
        ]

        self.label_acks = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    Wordless stands on the shoulders of giants. Thus, I would like to extend my thanks to the following open-source projects:
                </div>
            '''),
            self
        )
        self.label_browse_category = QLabel(self.tr('Browse by Category:'), self)
        self.combo_box_browse_category = wordless_box.Wordless_Combo_Box(self)

        self.table_acks = wordless_table.Wordless_Table(self,
                                                        headers = [
                                                            self.tr('Projects'),
                                                            self.tr('Version'),
                                                            self.tr('Author(s)'),
                                                            self.tr('License')
                                                        ])

        self.combo_box_browse_category.addItems([
            self.tr('General'),
            self.tr('Natural Language Processing'),
            self.tr('Plotting'),
            self.tr('Miscellaneous'),
            self.tr('Data')
        ])

        self.table_acks.setFixedHeight(250)

        self.combo_box_browse_category.currentTextChanged.connect(self.browse_category_changed)

        layout_browse_category = wordless_layout.Wordless_Layout()
        layout_browse_category.addWidget(self.label_browse_category, 0, 0)
        layout_browse_category.addWidget(self.combo_box_browse_category, 0, 1)

        layout_browse_category.setColumnStretch(2, 1)

        self.wrapper_info.layout().addWidget(self.label_acks, 0, 0)
        self.wrapper_info.layout().addLayout(layout_browse_category, 1, 0)
        self.wrapper_info.layout().addWidget(self.table_acks, 2, 0)

        self.load_settings()

        self.set_fixed_height()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['menu']['help']['acks'])

        self.combo_box_browse_category.setCurrentText(settings['browse_category'])

        self.browse_category_changed()

    def browse_category_changed(self):
        settings = self.main.settings_custom['menu']['help']['acks']

        settings['browse_category'] = self.combo_box_browse_category.currentText()

        if settings['browse_category'] == self.tr('General'):
            acks = self.ACKS_GENERAL
        elif settings['browse_category'] == self.tr('Natural Language Processing'):
            acks = self.ACKS_NLP
        elif settings['browse_category'] == self.tr('Plotting'):
            acks = self.ACKS_PLOTTING
        elif settings['browse_category'] == self.tr('Miscellaneous'):
            acks = self.ACKS_MISC
        elif settings['browse_category'] == self.tr('Data'):
            acks = self.ACKS_DATA

        self.table_acks.clear_table()

        self.table_acks.blockSignals(True)
        self.table_acks.setSortingEnabled(False)
        self.table_acks.setUpdatesEnabled(False)

        self.table_acks.setRowCount(len(acks))

        for i, (project, ver, authors, license) in enumerate(acks):
            # Add whitespace to each side of the cell
            project = project.replace('<br>', '&nbsp;<br>&nbsp;')
            ver = ver.replace('<br>', '&nbsp;<br>&nbsp;')
            authors = authors.replace('<br>', '&nbsp;<br>&nbsp;')
            license = license.replace('<br>', '&nbsp;<br>&nbsp;')

            project = f'&nbsp;{project}&nbsp;'
            ver = f'&nbsp;{ver}&nbsp;'
            authors = f'&nbsp;{authors}&nbsp;'
            license = f'&nbsp;{license}&nbsp;'

            self.table_acks.setCellWidget(i, 0, wordless_label.Wordless_Label_Html(project, self))
            self.table_acks.setCellWidget(i, 1, wordless_label.Wordless_Label_Html(ver, self))
            self.table_acks.setCellWidget(i, 2, wordless_label.Wordless_Label_Html(authors, self))
            self.table_acks.setCellWidget(i, 3, wordless_label.Wordless_Label_Html(license, self))

        self.table_acks.blockSignals(False)
        self.table_acks.setSortingEnabled(True)
        self.table_acks.setUpdatesEnabled(True)

        self.table_acks.itemChanged.emit(self.table_acks.item(0, 0))

class Wordless_Dialog_Need_Help(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Need Help?'),
                         width = 500,
                         height = 460)

        self.label_need_help = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    If you encounter a problem, find a bug, or require any further information, feel free to ask questions, submit bug reports, or provide feedback by <a href="https://github.com/BLKSerene/Wordless/issues/new">creating an issue</a> on Github if you fail to find the answer by searching <a href="https://github.com/BLKSerene/Wordless/issues">existing issues</a> first.
                </div>

                <div>
                    If you need to post sample texts or other information that cannot be shared or you do not want to share publicly, you may send me an email.
                </div>
            '''),
            self
        )

        self.table_need_help = wordless_table.Wordless_Table(self,
                                                             headers = [
                                                                 self.tr('Platforms'),
                                                                 self.tr('Contact Information')
                                                             ],
                                                             cols_stretch = [
                                                                 self.tr('Contact Information')
                                                             ])

        self.table_need_help.setRowCount(4)
        self.table_need_help.verticalHeader().setHidden(True)

        self.table_need_help.setCellWidget(0, 0, wordless_label.Wordless_Label_Html(self.tr('Home Page'), self))
        self.table_need_help.setCellWidget(0, 1, wordless_label.Wordless_Label_Html('<a href="https://github.com/BLKSerene/Wordless">https://github.com/BLKSerene/Wordless</a>', self))
        self.table_need_help.setCellWidget(1, 0, wordless_label.Wordless_Label_Html(self.tr('Documentation'), self))
        self.table_need_help.setCellWidget(1, 1, wordless_label.Wordless_Label_Html('<a href="https://github.com/BLKSerene/Wordless#-documentation">https://github.com/BLKSerene/Wordless#documentation</a>', self))
        self.table_need_help.setCellWidget(2, 0, wordless_label.Wordless_Label_Html(self.tr('Email'), self))
        self.table_need_help.setCellWidget(2, 1, wordless_label.Wordless_Label_Html('<a href="mailto:blkserene@gmail.com">blkserene@gmail.com</a><br><a href="mailto:blkserene@163.com">blkserene@163.com</a>', self))
        self.table_need_help.setCellWidget(3, 0, wordless_label.Wordless_Label_Html(self.tr('<a href="https://www.wechat.com/en/">WeChat</a> Official Account'), self))
        self.table_need_help.setCellWidget(3, 1, wordless_label.Wordless_Label_Html('<img src="imgs/wechat_official_account.dib">', self))

        self.label_need_help_note = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    <span style="color: #F00;"><b>Important Note</b></span>: I <b>CANNOT GUARANTEE</b> that all emails will always be checked or replied in time. I <b>WILL NOT REPLY</b> to irrelevant emails and I reserve the right to <b>BLOCK AND/OR REPORT</b> people who send me spam emails.
                </div>
            '''),
            self
        )

        self.wrapper_info.layout().addWidget(self.label_need_help, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_need_help, 1, 0)
        self.wrapper_info.layout().addWidget(self.label_need_help_note, 2, 0)

class Wordless_Dialog_Donating(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Donating'),
                         width = 450)

        self.label_donating = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    If you would like to support the development of Wordless, you may donate via <a href="https://www.paypal.com/">PayPal</a>, <a href="https://global.alipay.com/">Alipay</a>, or <a href="https://pay.weixin.qq.com/index.php/public/wechatpay_en">WeChat Pay</a>.
                </div>
            '''),
            self
        )
        self.label_donating_via = QLabel(self.tr('Donating via:'), self)
        self.combo_box_donating_via = wordless_box.Wordless_Combo_Box(self)
        self.label_donating_via_img = wordless_label.Wordless_Label_Html('', self)
        self.label_donating_note = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    <span style="color: #F00;"><b>Important Note</b></span>: I <b>WILL NOT PROVIDE</b> invoices, receipts, refund services, detailed spending reports, my contact information other than email addresses, my personal social media accounts, private email/phone support, or guarantees on bug fixes, enhancements, new features, or new releases of Wordless for donation.
                </div>
            '''),
            self
        )

        self.combo_box_donating_via.addItems([
            self.tr('PayPal'),
            self.tr('Alipay'),
            self.tr('WeChat Pay')
        ])

        self.combo_box_donating_via.currentTextChanged.connect(self.donating_via_changed)

        layout_donating_via = wordless_layout.Wordless_Layout()
        layout_donating_via.addWidget(self.label_donating_via, 0, 0)
        layout_donating_via.addWidget(self.combo_box_donating_via, 0, 1)

        layout_donating_via.setColumnStretch(2, 1)

        self.wrapper_info.layout().addWidget(self.label_donating, 0, 0)
        self.wrapper_info.layout().addLayout(layout_donating_via, 1, 0)
        self.wrapper_info.layout().addWidget(self.label_donating_via_img, 2, 0, Qt.AlignHCenter | Qt.AlignVCenter)
        self.wrapper_info.layout().addWidget(self.label_donating_note, 3, 0)

        # Calculate height
        donating_via_old = self.main.settings_custom['menu']['help']['donating']['donating_via']

        self.combo_box_donating_via.setCurrentText('PayPal')
        self.donating_via_changed()

        height_donating_via_paypal = self.label_donating_via_img.sizeHint().height()
        self.height_paypal = self.heightForWidth(self.width())

        self.combo_box_donating_via.setCurrentText('Alipay')
        self.donating_via_changed()

        height_donating_via_alipay = self.label_donating_via_img.sizeHint().height()
        self.height_alipay = self.heightForWidth(self.width()) + (height_donating_via_alipay - height_donating_via_paypal)

        self.main.settings_custom['menu']['help']['donating']['donating_via'] = donating_via_old

        self.load_settings()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['menu']['help']['donating'])

        self.combo_box_donating_via.setCurrentText(settings['donating_via'])

        self.donating_via_changed()

    def donating_via_changed(self):
        settings = self.main.settings_custom['menu']['help']['donating']

        settings['donating_via'] = self.combo_box_donating_via.currentText()

        if settings['donating_via'] == self.tr('PayPal'):
            self.label_donating_via_img.setText('<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=V2V54NYE2YD32"><img src="imgs/donating_paypal.gif"></a>')
        elif settings['donating_via'] == self.tr('Alipay'):
            self.label_donating_via_img.setText('<img src="imgs/donating_alipay.png">')
        elif settings['donating_via'] == self.tr('WeChat Pay'):
            self.label_donating_via_img.setText('<img src="imgs/donating_wechat_pay.png">')

        if 'height_alipay' in self.__dict__:
            if settings['donating_via'] == self.tr('PayPal'):
                self.setFixedHeight(self.height_paypal)
            elif settings['donating_via'] in [self.tr('Alipay'), self.tr('WeChat Pay')]:
                self.setFixedHeight(self.height_alipay)

        if platform.system() in ['Windows', 'Linux']:
            self.move_to_center()

class Worker_Check_Updates(QObject):
    check_updates_finished = pyqtSignal(str, str)

    def __init__(self, main):
        super().__init__()

        self.main = main
        self.stopped = False

    def check_updates(self):
        ver_new = ''

        try:
            r = requests.get('https://raw.githubusercontent.com/BLKSerene/Wordless/master/src/VERSION', timeout = 10)

            if r.status_code == 200:
                for line in r.text.splitlines():
                    if line and not line.startswith('#'):
                        ver_new = line.rstrip()

                if self.is_newer_version(ver_new):
                    updates_status = 'updates_available'
                else:
                    updates_status = 'no_updates'
            else:
                updates_status = 'network_error'
        except:
            updates_status = 'network_error'

        if self.stopped:
            updates_status == 'canceled'

        self.check_updates_finished.emit(updates_status, ver_new)

    def is_newer_version(self, ver_new):
        if self.main.ver:
            major_cur, minor_cur, patch_cur = line.split('.')
        else:
            return False

        if (int(major_cur) < int(major_new) or
            int(minor_cur) < int(minor_new) or
            int(patch_cur) < int(patch_new)):
            return True
        else:
            return False

    def stop(self):
        self.stopped = True

class Wordless_Dialog_Check_Updates(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main, on_startup = False):
        super().__init__(main, main.tr('Check for Updates'),
                         width = 420,
                         no_button = True)

        self.on_startup = on_startup

        self.label_check_updates = wordless_label.Wordless_Label_Dialog('', self)
        self.checkbox_check_updates_on_startup = QCheckBox(self.tr('Check for updates on startup'), self)
        
        self.button_try_again = QPushButton(self.tr('Try Again'), self)
        self.button_cancel = QPushButton(self.tr('Cancel'), self)

        self.checkbox_check_updates_on_startup.stateChanged.connect(self.check_updates_on_startup_changed)

        self.button_try_again.clicked.connect(self.check_updates)

        self.wrapper_info.layout().addWidget(self.label_check_updates, 0, 0)

        self.wrapper_buttons.layout().addWidget(self.checkbox_check_updates_on_startup, 0, 0)
        self.wrapper_buttons.layout().addWidget(self.button_try_again, 0, 2)
        self.wrapper_buttons.layout().addWidget(self.button_cancel, 0, 3)

        self.wrapper_buttons.layout().setColumnStretch(1, 1)

        self.load_settings()

        self.set_fixed_height()

    def check_updates(self):
        self.updates_status_changed('checking')

        self.main.worker_check_updates = Worker_Check_Updates(self.main)
        thread_check_updates = wordless_threading.Wordless_Thread(self.main.worker_check_updates)

        self.main.threads_check_updates.append(thread_check_updates)

        thread_check_updates.started.connect(self.main.worker_check_updates.check_updates)
        thread_check_updates.destroyed.connect(lambda: self.main.threads_check_updates.remove(thread_check_updates))

        if self.on_startup:
            self.main.worker_check_updates.check_updates_finished.connect(self.updates_status_changed_on_startup)

        self.main.worker_check_updates.check_updates_finished.connect(self.updates_status_changed)
        self.main.worker_check_updates.check_updates_finished.connect(thread_check_updates.quit)
        self.main.worker_check_updates.check_updates_finished.connect(self.main.worker_check_updates.deleteLater)

        thread_check_updates.start()

    def check_updates_stopped(self):
        self.main.worker_check_updates.stop()

        self.reject()

    def updates_status_changed(self, status, ver_new = ''):
        if status == 'checking':
            self.label_check_updates.set_text(self.tr('''
                <div>
                    Checking for updates...<br>
                    Please wait, it may take a few seconds.
                </div>
            '''))

            self.button_try_again.hide()
            self.button_cancel.setText(self.tr('Cancel'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.check_updates_stopped)
        elif status == 'no_updates':
            self.label_check_updates.set_text(self.tr('''
                <div>
                    Hooray, you are using the latest version of Wordless!
                </div>
            '''))

            self.button_try_again.hide()
            self.button_cancel.setText(self.tr('OK'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)
        elif status == 'updates_available':
            self.label_check_updates.set_text(self.tr(f'''
                <div>
                    Wordless v{ver_new} is out, click <a href="https://github.com/BLKSerene/Wordless/releases/tag/v{ver_new}"><b>HERE</b></a> to download the latest version of Wordless.
                </div>
            '''))

            self.button_try_again.hide()
            self.button_cancel.setText(self.tr('OK'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)
        elif status == 'network_error':
            self.label_check_updates.set_text(self.tr('''
                <div>
                    A network error occurred, please check your network settings and try again or <a href="https://github.com/BLKSerene/Wordless/releases">manually check for updates</a>.
                </div>
            '''))

            self.button_try_again.show()
            self.button_cancel.setText(self.tr('Close'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)

    def updates_status_changed_on_startup(self, status):
        if status == 'updates_available':
            self.open()
            self.setFocus()
        else:
            self.accept()

    def load_settings(self):
        settings = self.main.settings_custom['general']['update_settings']

        self.checkbox_check_updates_on_startup.setChecked(settings['check_updates_on_startup'])

        self.check_updates()

    def check_updates_on_startup_changed(self):
        settings = self.main.settings_custom['general']['update_settings']

        settings['check_updates_on_startup'] = self.checkbox_check_updates_on_startup.isChecked()

class Wordless_Dialog_Changelog(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        changelog = []

        try:
            with open('CHANGELOG.md', 'r', encoding = 'utf_8') as f:
                for line in f:
                    # Changelog headers
                    if line.startswith('## '):
                        release_ver = re.search(r'(?<=\[)[^\]]+?(?=\])', line).group()
                        release_link = re.search(r'(?<=\()[^\)]+?(?=\))', line).group()
                        release_date = re.search(r'(?<=\- )[0-9?]{2}/[0-9?]{2}/[0-9?]{4}', line).group()

                        changelog.append({
                            'release_ver': release_ver,
                            'release_link': release_link,
                            'release_date': release_date,
                            'changelog_sections': []
                        })

                    # Changelog section headers
                    elif line.startswith('### '):
                        changelog[-1]['changelog_sections'].append({
                            'section_header': line.replace('###', '').strip(),
                            'section_list': []
                        })
                    # Changelog section lists
                    elif line.startswith('- '):
                        changelog[-1]['changelog_sections'][-1]['section_list'].append(line.replace('-', '').strip())
        except:
            pass

        changelog_text = f'''
            {main.settings_global['styles']['style_changelog']}
            <body>
        '''

        for release in changelog:
            changelog_text += f'''
                <div class="changelog">
                    <div class="changelog-header"><a href="{release['release_link']}">{release['release_ver']}</a> - {release['release_date']}</div>
                    <hr>
            '''

            for changelog_section in release['changelog_sections']:
                changelog_text += f'''
                    <div class="changelog-section">
                        <div class="changelog-section-header">{changelog_section['section_header']}</div>
                        <ul>
                '''

                for item in changelog_section['section_list']:
                    changelog_text += f'''
                        <li>{item}</li>
                    '''

                changelog_text += f'''
                        </ul>
                    </div>
                '''

            changelog_text += f'''
                </div>
            '''

        changelog_text += f'''
            </body>
        '''

        super().__init__(main, main.tr('Changelog'),
                         width = 480,
                         height = 420)

        text_edit_changelog = wordless_box.Wordless_Text_Browser(self)

        text_edit_changelog.setHtml(changelog_text)

        self.wrapper_info.layout().addWidget(text_edit_changelog, 0, 0)

class Wordless_Dialog_About(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('About Wordless'))

        img_wordless_icon = QPixmap('imgs/wordless_icon_about.png')
        img_wordless_icon = img_wordless_icon.scaled(64, 64)

        label_about_icon = QLabel('', self)
        label_about_icon.setPixmap(img_wordless_icon)

        if main.ver:
            about_header = self.tr(f'Wordless Version {main.ver}')
        else:
            about_header = self.tr('Wordless')

        label_about_title = wordless_label.Wordless_Label_Dialog_No_Wrap(
            self.tr(f'''
                <div style="text-align: center;">
                    <h2>{about_header}</h2>
                    <div>
                        An Integrated Corpus Tool with Multi-Language Support<br>
                        for the Study of Language, Literature, and Translation
                    </div>
                </div>
            '''),
            self
        )
        label_about_copyright = wordless_label.Wordless_Label_Dialog_No_Wrap(
            self.tr('''
                <hr>
                <div style="text-align: center;">
                    Copyright (C) 2018-2019 Ye Lei (<span style="font-family: simsun">叶磊</span>)<br>
                    Licensed Under GNU GPLv3<br>
                    All Other Rights Reserved
                </div>
            '''),
            self
        )

        self.wrapper_info.layout().addWidget(label_about_icon, 0, 0)
        self.wrapper_info.layout().addWidget(label_about_title, 0, 1)
        self.wrapper_info.layout().addWidget(label_about_copyright, 1, 0, 1, 2)

        self.wrapper_info.layout().setColumnStretch(1, 1)
        self.wrapper_info.layout().setVerticalSpacing(0)

        self.set_fixed_size()
        self.setFixedWidth(self.width() + 10)
