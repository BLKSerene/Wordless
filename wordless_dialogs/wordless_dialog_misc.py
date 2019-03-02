#
# Wordless: Dialogs - Miscellaneous
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import datetime
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_dialogs import wordless_dialog
from wordless_widgets import wordless_label

class Wordless_Dialog_Progress(wordless_dialog.Wordless_Dialog_Frameless):
    def __init__(self, main, width, height):
        super().__init__(main, width, height)

        self.time_start = time.time()

        self.timer_time_elapsed = QTimer(self)

        self.label_progress = QLabel('', self)
        self.label_time_elapsed = QLabel(self.tr('Elapsed Time: 0:00:00'), self)
        self.label_processing = wordless_label.Wordless_Label_Dialog('', self)

        self.timer_time_elapsed.timeout.connect(self.update_elapsed_time)
        self.timer_time_elapsed.start(1000)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.label_progress, 0, 0)
        self.layout().addWidget(self.label_time_elapsed, 0, 1, Qt.AlignRight)
        self.layout().addWidget(self.label_processing, 1, 0, 1, 2)

        self.layout().setContentsMargins(20, 10, 20, 10)

    def update_elapsed_time(self):
        self.label_time_elapsed.setText(self.tr(f'''
            Elapsed Time: {datetime.timedelta(seconds = round(time.time() - self.time_start))}
        '''))

    def update_progress(self, text):
        self.label_progress.setText(text)

class Wordless_Dialog_Progress_Process_Data(Wordless_Dialog_Progress):
    def __init__(self, main):
        super().__init__(main,
                         width = 420,
                         height = 110)

        self.label_progress.setText(self.tr('Loading text ...'))
        
        self.label_processing.set_text(self.tr('''
            <div>
                Please wait while data is being processed. It may take a few seconds to several minutes depending on the total size of the selected files.
            </div>
        '''))

class Wordless_Dialog_Progress_Filter_Results(Wordless_Dialog_Progress):
    def __init__(self, main):
        super().__init__(main,
                         width = 420,
                         height = 110)

        self.label_progress.setText(self.tr('Filtering results ...'))
        
        self.label_processing.set_text(self.tr('''
            <div>
                Please wait while filtering is in progress. It may take a few seconds to several minutes depending on the number of items in results.
            </div>
        '''))

class Wordless_Dialog_Progress_Search_Results(Wordless_Dialog_Progress):
    def __init__(self, main):
        super().__init__(main,
                         width = 420,
                         height = 110)

        self.label_progress.setText(self.tr('Searching in results ...'))
        
        self.label_processing.set_text(self.tr('''
            <div>
                Please wait while searching is in progress. It may take a few seconds to several minutes depending on the number of items in results.
            </div>
        '''))

class Wordless_Dialog_Confirm_Exit(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Exit'),
                         width = 400,
                         height = 100,
                         no_button = True)

        self.label_confirm_exit = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    Are you sure you want to exit Wordless?
                </div>
                <div style="font-weight: bold;">
                    Note: All unsaved data and figures will be lost.
                </div>
            '''),
            self
        )

        self.checkbox_confirm_on_exit = QCheckBox(self.tr('Always confirm on exit'), self)
        self.button_exit = QPushButton(self.tr('Exit'), self)
        self.button_cancel = QPushButton(self.tr('Cancel'), self)

        self.checkbox_confirm_on_exit.stateChanged.connect(self.confirm_on_exit_changed)
        self.button_exit.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)

        self.wrapper_info.layout().addWidget(self.label_confirm_exit, 0, 0)

        self.wrapper_buttons.layout().addWidget(self.checkbox_confirm_on_exit, 0, 0)
        self.wrapper_buttons.layout().addWidget(self.button_exit, 0, 2)
        self.wrapper_buttons.layout().addWidget(self.button_cancel, 0, 3)

        self.wrapper_buttons.layout().setColumnStretch(1, 1)

        self.load_settings()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['general']['misc'])

        self.checkbox_confirm_on_exit.setChecked(settings['confirm_on_exit'])

    def confirm_on_exit_changed(self):
        settings = self.main.settings_custom['general']['misc']

        settings['confirm_on_exit'] = self.checkbox_confirm_on_exit.isChecked()
