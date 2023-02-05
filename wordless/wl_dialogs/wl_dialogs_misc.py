# ----------------------------------------------------------------------
# Wordless: Dialogs - Miscellaneous
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import datetime
import time

from PyQt5.QtCore import QCoreApplication, Qt, QTimer
from PyQt5.QtWidgets import QLabel, QPushButton

from wordless.wl_dialogs import wl_dialogs
from wordless.wl_widgets import wl_labels, wl_layouts

_tr = QCoreApplication.translate

class Wl_Dialog_Progress(wl_dialogs.Wl_Dialog_Frameless):
    def __init__(self, main, text):
        super().__init__(main, width = 450)

        self.time_start = time.time()

        self.timer_time_elapsed = QTimer(self)

        self.label_progress = QLabel(text, self)
        self.label_time_elapsed = QLabel(_tr('Wl_Dialog_Progress', 'Elapsed time: 0:00:00'), self)
        self.label_processing = wl_labels.Wl_Label_Dialog(_tr('Wl_Dialog_Progress', 'Please wait. It may take a few seconds to several minutes for the operation to be completed.'), self)

        self.timer_time_elapsed.timeout.connect(self.update_elapsed_time)
        self.timer_time_elapsed.start(1000)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.label_progress, 0, 0)
        self.layout().addWidget(self.label_time_elapsed, 0, 1, Qt.AlignRight)
        self.layout().addWidget(self.label_processing, 1, 0, 1, 2)

        self.layout().setContentsMargins(20, 10, 20, 10)

    def update_elapsed_time(self):
        self.label_time_elapsed.setText(
            _tr('Wl_Dialog_Progress', 'Elapsed time: ')
            + str(datetime.timedelta(seconds = round(time.time() - self.time_start)))
        )

    def update_progress(self, text):
        self.label_progress.setText(text)

class Wl_Dialog_Progress_Process_Data(Wl_Dialog_Progress):
    def __init__(self, main):
        super().__init__(main, text = _tr('Wl_Dialog_Progress_Process_Data', 'Processing data...'))

class Wl_Dialog_Clr_Table(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = _tr('WL_Dialog_Clear_Table', 'Clear Table'),
            width = 420,
            no_buttons = True
        )

        self.label_confirm_clr = wl_labels.Wl_Label_Dialog(
            self.tr('''
                <div>
                    The results in the table have yet been exported. Do you really want to clear the table?
                </div>
            '''),
            self
        )

        self.button_yes = QPushButton(self.tr('Yes'), self)
        self.button_no = QPushButton(self.tr('No'), self)

        self.button_yes.clicked.connect(self.accept)
        self.button_no.clicked.connect(self.reject)

        self.wrapper_info.layout().addWidget(self.label_confirm_clr, 0, 0)

        self.wrapper_buttons.layout().addWidget(self.button_yes, 0, 1)
        self.wrapper_buttons.layout().addWidget(self.button_no, 0, 2)

        self.wrapper_buttons.layout().setColumnStretch(0, 1)

        self.set_fixed_height()

class Wl_Dialog_Clr_All_Tables(Wl_Dialog_Clr_Table):
    def __init__(self, main):
        super().__init__(main)

        self.setWindowTitle(self.tr('Clear All Tables'))
        self.label_confirm_clr.setText(self.tr('''
            <div>
                The results in some of the tables have yet been exported. Do you really want to clear all tables?
            </div>
        '''))

class Wl_Dialog_Restart_Required(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = _tr('Wl_Dialog_Restart_Required', 'Restart Wordless'),
            width = 450,
            no_buttons = True
        )

        self.label_restart_exit = wl_labels.Wl_Label_Dialog(
            self.tr('''
                <div>
                    Restart is required for the settings to take effect. Do you want to restart Wordless now?
                </div>

                <div style="font-weight: bold;">
                    Note: All unsaved data and figures will be lost.
                </div>
            '''),
            self
        )

        self.button_restart = QPushButton(self.tr('Restart'), self)
        self.button_cancel = QPushButton(self.tr('Cancel'), self)

        self.button_restart.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)

        self.wrapper_info.layout().addWidget(self.label_restart_exit, 0, 0)

        self.wrapper_buttons.layout().addWidget(self.button_restart, 0, 1)
        self.wrapper_buttons.layout().addWidget(self.button_cancel, 0, 2)

        self.wrapper_buttons.layout().setColumnStretch(0, 1)

        self.set_fixed_height()
