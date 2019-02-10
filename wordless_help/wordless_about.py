#
# Wordless: Help - About
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

class Wordless_Dialog_About(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('About Wordless'),
                         width = 420,
                         height = 150)

        label_about_icon = QLabel('', self)
        label_about_icon.setPixmap(QPixmap('imgs/wordless_icon.png'))

        label_about_title = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div style="text-align: center;">
                    <h2>Wordless Version 1.0.0</h2>
                    <div>
                        An Integrated Corpus Tool with Multi-language Support<br>
                        for the Study of Language, Literature and Translation
                    </div>
                </div>
            '''), self.main)
        label_about_copyright = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <hr>
                <div style="text-align: center;">
                    Copyright (C)&nbsp;&nbsp;2018 Ye Lei (<span style="font-family: simsun">叶磊</span>)<br>
                    Licensed Under GNU GPLv3<br>
                    All Other Rights Reserved
                </div>
            '''), self.main)

        self.wrapper_info.layout().addWidget(label_about_icon, 0, 0)
        self.wrapper_info.layout().addWidget(label_about_title, 0, 1)
        self.wrapper_info.layout().addWidget(label_about_copyright, 1, 0, 1, 2)

        self.wrapper_info.layout().setColumnStretch(1, 1)
        self.wrapper_info.layout().setVerticalSpacing(0)
