#
# Wordless: Help - Citing
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_widgets import *

class Wordless_Dialog_Citing(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Citing'),
                         width = 400,
                         height = 150,
                         no_button = True)

        self.label_citing = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    If you publish work that uses Wordless, please cite as follows.
                </div>
            '''), self.main)

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
    
        layout_citation_sys = QGridLayout()
        layout_citation_sys.addWidget(self.label_citation_sys, 0, 0)
        layout_citation_sys.addWidget(self.combo_box_citation_sys, 0, 1)
    
        layout_citation_sys.setColumnStretch(2, 1)
    
        self.wrapper_info.layout().addWidget(self.label_citing, 0, 0, 1, 2)
        self.wrapper_info.layout().addLayout(layout_citation_sys, 1, 0, 1, 2)
        self.wrapper_info.layout().addWidget(self.text_edit_citing, 2, 0, 1, 2)
    
        self.wrapper_buttons.layout().addWidget(self.button_copy, 0, 0)
        self.wrapper_buttons.layout().addWidget(self.button_close, 0, 1)

        self.load_settings()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['menu']['help']['citing'])

        self.combo_box_citation_sys.setCurrentText(settings['citation_sys'])

        self.citation_sys_changed()

    def citation_sys_changed(self):
        settings = self.main.settings_custom['menu']['help']['citing']

        settings['citation_sys'] = self.combo_box_citation_sys.currentText()

        if settings['citation_sys'] == self.tr('MLA (8th Edition)'):
            self.text_edit_citing.setHtml('Ye Lei. Wordless, version 1.0.0, 2019, https://github.com/BLKSerene/Wordless.')
        elif settings['citation_sys'] == self.tr('APA (6th Edition)'):
            self.text_edit_citing.setHtml('Ye, L. (2019) Wordless (Version 1.0.0) [Computer Software]. Retrieved from https://github.com/BLKSerene/Wordless')
        elif settings['citation_sys'] == self.tr('GB (GB/T 7714—2015)'):
            self.text_edit_citing.setHtml('叶磊. Wordless version 1.0.0[CP]. (2019). https://github.com/BLKSerene/Wordless.')

        if settings['citation_sys'] == self.tr('GB (GB/T 7714—2015)'):
            self.text_edit_citing.setFont(QFont('宋体', 12))
        else:
            self.text_edit_citing.setFont(QFont('Times New Roman', 12))

    def copy(self):
        self.text_edit_citing.setFocus()
        self.text_edit_citing.selectAll()
        self.text_edit_citing.copy()
