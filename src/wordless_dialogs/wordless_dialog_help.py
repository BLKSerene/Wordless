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

import requests

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_dialogs import wordless_dialog
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
            self.text_edit_citing.setHtml('Ye Lei. Wordless, version 1.1.0, 2019, https://github.com/BLKSerene/Wordless.')
        elif settings['citation_sys'] == self.tr('APA (6th Edition)'):
            self.text_edit_citing.setHtml('Ye, L. (2019) Wordless (Version 1.1.0) [Computer Software]. Retrieved from https://github.com/BLKSerene/Wordless')
        elif settings['citation_sys'] == self.tr('GB (GB/T 7714—2015)'):
            self.text_edit_citing.setHtml('叶磊. Wordless version 1.1.0[CP]. (2019). https://github.com/BLKSerene/Wordless.')

    def copy(self):
        self.text_edit_citing.setFocus()
        self.text_edit_citing.selectAll()
        self.text_edit_citing.copy()

class Wordless_Dialog_Acks(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Acknowledgments'),
                         width = 580)

        self.ACKS_GENERAL = [
            [
                '<a href="https://www.python.org/">Python</a>',
                '3.7.2',
                'Guido van Rossum, Python Software Foundation',
                '<a href="https://docs.python.org/3.7/license.html#psf-license-agreement-for-python-release">PSF</a>'
            ],

            [
                '<a href="https://www.riverbankcomputing.com/software/pyqt/intro">PyQt</a>',
                '5.12.1',
                'Riverbank Computing Limited',
                '<a href="http://pyqt.sourceforge.net/Docs/PyQt5/introduction.html#license">GPL-3.0</a>'
            ]
        ]

        self.ACKS_NLP = [
            [
                main.tr('<a href="https://github.com/fxsjy/jieba">jieba</a>'),
                '0.39',
                'Sun Junyi',
                '<a href="https://github.com/fxsjy/jieba/blob/master/LICENSE">MIT</a>'
            ],

            [
                '<a href="https://github.com/taishi-i/nagisa">nagisa</a>',
                '0.2.1',
                'Taishi Ikeda (池田大志)',
                '<a href="https://github.com/taishi-i/nagisa/blob/master/LICENSE.txt">MIT</a>'
            ],

            [
                '<a href="http://www.nltk.org/">NLTK</a>',
                '3.4',
                'Steven Bird, Liling Tan',
                '<a href="https://github.com/nltk/nltk/blob/develop/LICENSE.txt">Apache-2.0</a>'
            ],

            [
                '<a href="https://github.com/Esukhia/pybo">pybo</a>',
                '0.4.2',
                'Hélios Drupchen Hildt',
                '<a href="https://github.com/Esukhia/pybo/blob/master/LICENSE">Apache-2.0</a>'
            ],

            [
                '<a href="https://github.com/kmike/pymorphy2/">pymorphy2</a>',
                '0.8',
                'Mikhail Korobov',
                '<a href="https://github.com/kmike/pymorphy2/#pymorphy2">MIT</a>'
            ],

            [
                '<a href="https://github.com/PyThaiNLP/pythainlp">PyThaiNLP</a>',
                '1.7.4',
                'Wannaphong Phatthiyaphaibun (วรรณพงษ์ ภัททิยไพบูลย์)',
                '<a href="https://github.com/PyThaiNLP/pythainlp/blob/dev/LICENSE">Apache-2.0</a>'
            ],

            [
                '<a href="https://github.com/alvations/sacremoses">SacreMoses</a>',
                '0.0.13',
                'Liling Tan',
                '<a href="https://github.com/alvations/sacremoses#license">LGPL-2.1</a>'
            ],

            [
                '<a href="https://spacy.io/">spaCy</a>',
                '2.1.3',
                'Matthew Honnibal, Ines Montani',
                '<a href="https://github.com/explosion/spaCy/blob/master/LICENSE">MIT</a>'
            ],

            [
                '<a href="https://github.com/undertheseanlp/underthesea">Underthesea</a>',
                '1.1.15',
                'Vu Anh',
                '<a href="https://github.com/undertheseanlp/underthesea/blob/master/LICENSE">GPL-3.0</a>'
            ]
        ]

        self.ACKS_PLOTTING = [
            [
                '<a href="https://matplotlib.org/">Matplotlib</a>',
                '3.0.3',
                'Matplotlib Development Team',
                '<a href="https://matplotlib.org/users/license.html">Matplotlib</a>'
            ],

            [
                '<a href="https://amueller.github.io/word_cloud/">wordcloud</a>',
                '1.5.0',
                'Andreas Christian Mueller',
                '<a href="https://github.com/amueller/word_cloud/blob/master/LICENSE">MIT</a>'
            ]
        ]

        self.ACKS_MISC = [
            [
                '<a href="https://www.crummy.com/software/BeautifulSoup/">Beautiful Soup</a>',
                '4.7.1',
                'Leonard Richardson',
                '<a href="https://bazaar.launchpad.net/~leonardr/beautifulsoup/bs4/view/head:/LICENSE">MIT</a>'
            ],

            [
                '<a href="https://github.com/PyYoshi/cChardet">cChardet</a>',
                '2.1.4',
                'Yoshihiro Misawa',
                '<a href="https://github.com/PyYoshi/cChardet/blob/master/COPYING">MPL-1.0/GPL-2.0/LGPL-2.1</a>'
            ],

            [
                '<a href="https://github.com/chardet/chardet">chardet</a>',
                '3.0.4',
                'Daniel Blanchard',
                '<a href="https://github.com/chardet/chardet/blob/master/LICENSE">LGPL-2.1</a>'
            ],

            [
                '<a href="https://github.com/Mimino666/langdetect">langdetect</a>',
                '1.0.7',
                'Michal Mimino Danilak',
                '<a href="https://github.com/Mimino666/langdetect/blob/master/LICENSE">Apache-2.0</a>'
            ],

            [
                '<a href="https://github.com/saffsd/langid.py">langid.py</a>',
                '1.1.6',
                'Marco Lui',
                '<a href="https://github.com/saffsd/langid.py/blob/master/LICENSE">BSD-2-Clause</a>'
            ],

            [
                '<a href="https://lxml.de/">lxml</a>',
                '4.3.3',
                'Stefan Behnel',
                '<a href="https://github.com/lxml/lxml/blob/master/doc/licenses/BSD.txt">BSD-3-Clause</a>'
            ],

            [
                '<a href="http://www.numpy.org/">NumPy</a>',
                '1.16.2',
                'NumPy Developers',
                '<a href="http://www.numpy.org/license.html">BSD-3-Clause</a>'
            ],

            [
                '<a href="https://openpyxl.readthedocs.io/en/stable/">openpyxl</a>',
                '2.6.1',
                'Eric Gazoni, Charlie Clark',
                '<a href="https://bitbucket.org/openpyxl/openpyxl/src/5983d4ba5c18b85171185e8b1ca136876ec52864/LICENCE.rst">MIT</a>'
            ],

            [
                '<a href="http://www.pyinstaller.org/">PyInstaller</a>',
                '3.5.dev0+cb8d10af6',
                'Hartmut Goebel',
                '<a href="https://github.com/pyinstaller/pyinstaller/blob/develop/COPYING.txt">PyInstaller</a>'
            ],

            [
                '<a href="https://github.com/python-openxml/python-docx">python-docx</a>',
                '0.8.10',
                'Steve Canny',
                '<a href="https://github.com/python-openxml/python-docx/blob/master/LICENSE">MIT</a>'
            ],

            [
                '<a href="http://python-requests.org">requests</a>',
                '2.21.0',
                'Kenneth Reitz',
                '<a href="https://github.com/requests/requests/blob/master/LICENSE">Apache-2.0</a>'
            ],

            [
                '<a href="https://www.scipy.org/">SciPy</a>',
                '1.2.1',
                'SciPy Developers',
                '<a href="https://www.scipy.org/scipylib/license.html">BSD-3-Clause</a>'
            ],

            [
                '<a href="https://github.com/python-excel/xlrd">xlrd</a>',
                '1.2.0',
                'Stephen John Machin',
                '<a href="https://github.com/python-excel/xlrd/blob/master/LICENSE">BSD-3-Clause/BSD-4-Clause</a>'
            ]
        ]

        self.ACKS_DATA = [
            [
                '<a href="https://github.com/pharos-alexandria/grk-stoplist">grk-stoplist</a>',
                '/',
                'Annette von Stockhausen',
                '<a href="https://github.com/pharos-alexandria/grk-stoplist/blob/master/LICENSE">CC0-1.0</a>'
            ],

            [
                '<a href="https://github.com/stenskjaer/lemmalist-greek">lemmalist-greek</a>',
                '/',
                'Michael Stenskjær Christensen',
                '<a href="https://github.com/stenskjaer/lemmalist-greek/blob/master/LICENSE">GPL-3.0</a>'
            ],

            [
                '<a href="https://github.com/michmech/lemmatization-lists">Lemmatization Lists</a>',
                '/',
                'Michal Boleslav Měchura',
                '<a href="https://github.com/michmech/lemmatization-lists/blob/master/LICENCE">ODbL</a>'
            ],

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
                                                            self.tr('Name'),
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

        for i, (name, ver, authors, license) in enumerate(acks):
            self.table_acks.setCellWidget(i, 0, wordless_label.Wordless_Label_Html(name, self))
            self.table_acks.setCellWidget(i, 1, wordless_label.Wordless_Label_Html(ver, self))
            self.table_acks.setCellWidget(i, 2, wordless_label.Wordless_Label_Html(authors, self))
            self.table_acks.setCellWidget(i, 3, wordless_label.Wordless_Label_Html(license, self))

            self.table_acks.cellWidget(i, 1).setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table_acks.cellWidget(i, 3).setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.table_acks.blockSignals(False)
        self.table_acks.setSortingEnabled(True)
        self.table_acks.setUpdatesEnabled(True)

        self.table_acks.itemChanged.emit(self.table_acks.item(0, 0))

class Wordless_Dialog_Donating(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Donating'),
                         width = 450)

        self.label_donating = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    If you would like to support the development of Wordless, you may donate via PayPal, Alipay or WeChat.
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
                    <span style="color: #F00;"><b>Important Note</b></span>: I <b>WILL NOT PROVIDE</b> refund services, private email/phone support, information concerning my social media, gurantees on bug fixes, enhancements, new features or new releases of Wordless, invoices, receipts or detailed weekly/monthly/yearly/etc. spending report for donation. 
                </div>
            '''),
            self
        )

        self.combo_box_donating_via.addItems([
            self.tr('PayPal'),
            self.tr('Alipay'),
            self.tr('WeChat')
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
        elif settings['donating_via'] == self.tr('WeChat'):
            self.label_donating_via_img.setText('<img src="imgs/donating_wechat.png">')

        if 'height_alipay' in self.__dict__:
            if settings['donating_via'] == self.tr('PayPal'):
                self.setFixedHeight(self.height_paypal)
            elif settings['donating_via'] in [self.tr('Alipay'), self.tr('WeChat')]:
                self.setFixedHeight(self.height_alipay)

        if platform.system() in ['Windows', 'Linux']:
            self.move_to_center()

class Worker_Check_Updates(QObject):
    finished = pyqtSignal()
    check_updates_finished = pyqtSignal(str, str)

    def __init__(self, main):
        super().__init__()

        self.main = main
        self.stopped = False

    def check_updates(self):
        version_new = ''

        try:
            r = requests.get('https://raw.githubusercontent.com/BLKSerene/Wordless/master/src/VERSION', timeout = 10)

            if r.status_code == 200:
                for line in r.text.splitlines():
                    if line and not line.startswith('#'):
                        version_new = line.rstrip()

                if self.is_newer_version(version_new):
                    updates_status = 'updates_available'
                else:
                    updates_status = 'no_updates'
            else:
                updates_status = 'network_error'
        except:
            updates_status = 'network_error'

        if not self.stopped:
            self.check_updates_finished.emit(updates_status, version_new)

        self.finished.emit()

    def is_newer_version(self, version_new):
        with open('VERSION', 'r', encoding = 'utf_8') as f:
            for line in f.readlines():
                line = line.rstrip()

                if line and not line.startswith('#'):
                    major_cur, minor_cur, patch_cur = line.split('.')

        major_new, minor_new, patch_new = version_new.split('.')

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

        thread_check_updates = QThread()

        self.main.threads_check_updates.append(thread_check_updates)

        self.main.worker_check_updates = Worker_Check_Updates(self.main)
        self.main.worker_check_updates.moveToThread(thread_check_updates)

        thread_check_updates.started.connect(self.main.worker_check_updates.check_updates)
        thread_check_updates.finished.connect(thread_check_updates.deleteLater)
        thread_check_updates.destroyed.connect(lambda: self.main.threads_check_updates.remove(thread_check_updates))

        if self.on_startup:
            self.worker_check_updates.check_updates_finished.connect(self.updates_status_on_startup_changed)

        self.main.worker_check_updates.check_updates_finished.connect(self.updates_status_changed)
        self.main.worker_check_updates.finished.connect(thread_check_updates.quit)
        self.main.worker_check_updates.finished.connect(self.main.worker_check_updates.deleteLater)

        thread_check_updates.start()

    def check_updates_stopped(self):
        self.main.worker_check_updates.stop()

        self.reject()

    def updates_status_changed(self, status, version_new = ''):
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
                    Wordless v{version_new} is out, click <a href="https://github.com/BLKSerene/Wordless/releases"><b>HERE</b></a> to download the latest version of Wordless.
                </div>
            '''))

            self.button_try_again.hide()
            self.button_cancel.setText(self.tr('OK'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)
        elif status == 'network_error':
            self.label_check_updates.set_text(self.tr('''
                <div>
                    A network error occurred, please check your network settings or try again later.
                </div>
            '''))

            self.button_try_again.show()
            self.button_cancel.setText(self.tr('Close'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)

    def updates_status_on_startup_changed(self, status):
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
        changelog = main.tr(f'''
            {main.settings_global['styles']['style_changelog']}
            <body>
                <div class="changelog">
                    <div class="changelog-header"><a href="https://github.com/BLKSerene/Wordless/releases/tag/v1.0.0">v1.0.0</a> - 03/17/2019</div>
                    <hr>

                    <div class="changelog-section">
                        <ul>
                            <li>First release</li>
                        </ul>
                    </div>
                </div>

                <div class="changelog">
                    <div class="changelog-header"><a href="https://github.com/BLKSerene/Wordless/releases/tag/v1.1.0">v1.1.0</a> - 03/25/2019</div>
                    <hr>

                    <div class="changelog-section">
                        <div class="changelog-section-header">New Features</div>
                        <ul>
                            <li>Add "Settings → General → Font Settings"</li>
                        </ul>
                    </div>

                    <div class="changelog-section">
                        <div class="changelog-section-header">Improvements</div>
                        <ul>
                            <li>Disable mouse wheel event when combo boxes and spin boxes are not focused (<a href="https://github.com/BLKSerene/Wordless/issues/2">#2</a>)</li>
                            <li>Update hint messages</li>
                            <li>Update layout</li>
                            <li>Update spaCy's sentencizer</li>
                        </ul>
                    </div>

                    <div class="changelog-section">
                        <div class="changelog-section-header">Bug Fixes</div>
                        <ul>
                            <li>Fix "Context Settings"</li>
                            <li>Fix error message when loading files</li>
                            <li>Fix "Open Folder"</li>
                            <li>Fix searching in results after results are sorted in "Concordancer"</li>
                            <li>Fix "Settings → Sentence Tokenization / Word Tokenization / Word Detokenization / POS Tagging / Lemmatization → Preview"</li>
                            <li>Fix spaCy's sentence/word tokenizers</li>
                            <li>Fix Wordless's Chinese/Japanese character tokenizer</li>
                        </ul>
                    </div>

                    <div class="changelog-section">
                        <div class="changelog-section-header">Dependency Updates</div>
                        <ul>
                            <li>Update lxml to 4.3.3</li>
                            <li>Update PyQt to 5.12.1</li>
                            <li>Update SacreMoses to 0.0.13</li>
                            <li>Update spaCy to 2.1.3</li>
                        </ul>
                    </div>
                </div>
            </body>
        ''')

        super().__init__(main, main.tr('Changelog'),
                         width = 480,
                         height = 420)

        text_edit_changelog = wordless_box.Wordless_Text_Browser(self)

        text_edit_changelog.setHtml(changelog)

        self.wrapper_info.layout().addWidget(text_edit_changelog, 0, 0)

class Wordless_Dialog_About(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('About Wordless'))

        label_about_icon = QLabel('', self)

        img_wordless_icon = QPixmap('imgs/wordless_icon_about.png')
        img_wordless_icon = img_wordless_icon.scaled(64, 64)

        label_about_icon.setPixmap(img_wordless_icon)

        label_about_title = wordless_label.Wordless_Label_Dialog_No_Wrap(
            self.tr('''
                <div style="text-align: center;">
                    <h2>Wordless Version 1.1.0</h2>
                    <div>
                        An Integrated Corpus Tool with Multi-language Support<br>
                        for the Study of Language, Literature and Translation
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
