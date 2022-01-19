# ----------------------------------------------------------------------
# Wordless: Dialogs - Miscellaneous
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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

import copy
import datetime
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_dialogs
from wl_widgets import wl_labels, wl_layouts

class Wl_Dialog_Progress(wl_dialogs.Wl_Dialog_Frameless):
    def __init__(self, main, text):
        super().__init__(main, width = 450)

        self.time_start = time.time()

        self.timer_time_elapsed = QTimer(self)

        self.label_progress = QLabel(text, self)
        self.label_time_elapsed = QLabel(self.tr('Elapsed Time: 0:00:00'), self)
        self.label_processing = wl_labels.Wl_Label_Dialog(self.tr('Please wait. It may take a few seconds to several minutes for the operation to be completed.'), self)

        self.timer_time_elapsed.timeout.connect(self.update_elapsed_time)
        self.timer_time_elapsed.start(1000)

        self.setLayout(wl_layouts.Wl_Layout())
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

class Wl_Dialog_Progress_Process_Data(Wl_Dialog_Progress):
    def __init__(self, main):
        super().__init__(main, text = main.tr('Processing data...'))

class WL_Dialog_Clear_Table(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = main.tr('Clear Table'),
            width = 420,
            no_buttons = True
        )

        self.label_confirm_clear = wl_labels.Wl_Label_Dialog(
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

        self.wrapper_info.layout().addWidget(self.label_confirm_clear, 0, 0)

        self.wrapper_buttons.layout().addWidget(self.button_yes, 0, 1)
        self.wrapper_buttons.layout().addWidget(self.button_no, 0, 2)

        self.wrapper_buttons.layout().setColumnStretch(0, 1)

        self.set_fixed_height()

class Wl_Dialog_Restart_Required(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = main.tr('Restart Wordless'),
            width = 420,
            no_buttons = True
        )

        self.label_restart_exit = wl_labels.Wl_Label_Dialog(
            self.tr('''
                <div>
                    Restart is required for font settings to take effect. Do you want to restart Wordless now?
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

class Wl_Dialog_Confirm_Exit(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = main.tr('Exit Wordless'),
            width = 420,
            no_buttons = True
        )

        self.label_confirm_exit = wl_labels.Wl_Label_Dialog(
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

        self.set_fixed_height()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['general']['misc'])

        self.checkbox_confirm_on_exit.setChecked(settings['confirm_on_exit'])

    def confirm_on_exit_changed(self):
        settings = self.main.settings_custom['general']['misc']

        settings['confirm_on_exit'] = self.checkbox_confirm_on_exit.isChecked()
