#
# Wordless: Help - Changelog
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

from wordless_widgets import wordless_dialog

class Wordless_Dialog_Changelog(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        changelog = main.tr(f'''
            {main.settings_global['styles']['style_changelog']}
            <body>
                <div>
                    <h3>v1.0.0 - 02/25/2019</h3>
                    <hr>
                    <ul>
                        <li>&nbsp;First stable release of Wordless.</li>
                    </ul>
                </div>
            </body>
        ''')

        super().__init__(main, main.tr('Changelog'),
                         width = 450,
                         height = 420)

        text_edit_changelog = QTextEdit()

        text_edit_changelog.setHtml(changelog)
        text_edit_changelog.setReadOnly(True)
        text_edit_changelog.setContentsMargins(3, 3, 3, 3)

        self.wrapper_info.layout().addWidget(text_edit_changelog, 0, 0)
