#
# Wordless: Help - Acknowledgments
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_widgets import *

class Wordless_Dialog_Acks(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        self.acks_general = [
            [
                '<a href="https://www.python.org/">Python</a>',
                '3.7.2',
                'Guido van Rossum, Python Software Foundation',
                '<a href="https://docs.python.org/3.7/license.html#psf-license-agreement-for-python-release">PSF</a>'
            ],

            [
                '<a href="https://www.riverbankcomputing.com/software/pyqt/intro">PyQt</a>',
                '5.11.3',
                'Riverbank Computing Limited',
                '<a href="http://pyqt.sourceforge.net/Docs/PyQt5/introduction.html#license">GPL-3.0/Commercial</a>'
            ]
        ]

        self.acks_nlp = [
            [
                main.tr('<a href="https://github.com/fxsjy/jieba">jieba</a>'),
                '0.39',
                'Sun Junyi',
                '<a href="https://github.com/fxsjy/jieba/blob/master/LICENSE">MIT</a>'
            ],

            [
                '<a href="https://github.com/taishi-i/nagisa">nagisa</a>',
                '0.2.0',
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
                '0.3.0',
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
                '1.7.2',
                'Wannaphong Phatthiyaphaibun (วรรณพงษ์ ภัททิยไพบูลย์)',
                '<a href="https://github.com/PyThaiNLP/pythainlp/blob/dev/LICENSE">Apache-2.0</a>'
            ],

            [
                '<a href="https://github.com/alvations/sacremoses">SacreMoses</a>',
                '0.0.7',
                'Liling Tan',
                '<a href="https://github.com/alvations/sacremoses#license">LGPL-2.1</a>'
            ],

            [
                '<a href="https://spacy.io/">spaCy</a>',
                '2.0.18',
                'Matthew Honnibal, Ines Montani',
                '<a href="https://github.com/explosion/spaCy/blob/master/LICENSE">MIT</a>'
            ],

            [
                '<a href="https://github.com/undertheseanlp/underthesea">Underthesea</a>',
                '1.1.11',
                'Vu Anh',
                '<a href="https://github.com/undertheseanlp/underthesea/blob/master/LICENSE">GPL-3.0</a>'
            ]
        ]

        self.acks_plotting = [
            [
                '<a href="https://matplotlib.org/">Matplotlib</a>',
                '3.0.2',
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

        self.acks_misc = [
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
                '4.3.0',
                'Stefan Behnel',
                '<a href="https://github.com/lxml/lxml/blob/master/doc/licenses/BSD.txt">BSD-3-Clause</a>'
            ],

            [
                '<a href="http://www.numpy.org/">NumPy</a>',
                '1.16.1',
                'NumPy Developers',
                '<a href="http://www.numpy.org/license.html">BSD-3-Clause</a>'
            ],

            [
                '<a href="https://openpyxl.readthedocs.io/en/stable/">openpyxl</a>',
                '2.5.14',
                'Eric Gazoni, Charlie Clark',
                '<a href="https://bitbucket.org/openpyxl/openpyxl/src/5983d4ba5c18b85171185e8b1ca136876ec52864/LICENCE.rst">MIT</a>'
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
                '1.2.0',
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

        self.acks_data = [
            [
                '<a href="https://github.com/pharos-alexandria/grk-stoplist">grk-stoplist</a>',
                '/',
                'Annette von Stockhausen',
                '<a href="https://github.com/pharos-alexandria/grk-stoplist/blob/master/LICENSE">CC0-1.0</a>'
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

        super().__init__(main, main.tr('Acknowledgments'),
                         width = 560,
                         height = 350)

        self.label_acks = wordless_label.Wordless_Label_Dialog(self.tr('''
            <div>
                Wordless stands on the shoulders of giants. Thus, I would like to extend my thanks to the following open-source projects:
            </div>
        '''), self.main)
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

        self.combo_box_browse_category.currentTextChanged.connect(self.browse_category_changed)

        layout_browse_category = QGridLayout()
        layout_browse_category.addWidget(self.label_browse_category, 0, 0)
        layout_browse_category.addWidget(self.combo_box_browse_category, 0, 1)

        layout_browse_category.setColumnStretch(2, 1)

        self.wrapper_info.layout().addWidget(self.label_acks, 0, 0)
        self.wrapper_info.layout().addLayout(layout_browse_category, 1, 0)
        self.wrapper_info.layout().addWidget(self.table_acks, 2, 0)

        self.browse_category_changed()

    def browse_category_changed(self):
        if self.combo_box_browse_category.currentText() == self.tr('General'):
            acks = self.acks_general
        elif self.combo_box_browse_category.currentText() == self.tr('Natural Language Processing'):
            acks = self.acks_nlp
        elif self.combo_box_browse_category.currentText() == self.tr('Plotting'):
            acks = self.acks_plotting
        elif self.combo_box_browse_category.currentText() == self.tr('Miscellaneous'):
            acks = self.acks_misc
        elif self.combo_box_browse_category.currentText() == self.tr('Data'):
            acks = self.acks_data

        self.table_acks.clear_table()

        self.table_acks.setRowCount(len(acks))

        for i, (name, ver, authors, license) in enumerate(acks):
            self.table_acks.setCellWidget(i, 0, wordless_label.Wordless_Label_Html(name, self))
            self.table_acks.setCellWidget(i, 1, wordless_label.Wordless_Label_Html(ver, self))
            self.table_acks.setCellWidget(i, 2, wordless_label.Wordless_Label_Html(authors, self))
            self.table_acks.setCellWidget(i, 3, wordless_label.Wordless_Label_Html(license, self))

            self.table_acks.cellWidget(i, 1).setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table_acks.cellWidget(i, 3).setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
