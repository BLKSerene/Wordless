# ----------------------------------------------------------------------
# Wordless: Dialogs - Miscellaneous
# Copyright (C) 2018-2025  Ye Lei (叶磊)
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import datetime
import time

from PyQt5.QtCore import QCoreApplication, Qt, QTimer
from PyQt5.QtWidgets import QPushButton

from wordless.wl_dialogs import wl_dialogs
from wordless.wl_widgets import wl_labels, wl_layouts

_tr = QCoreApplication.translate

# self.tr() does not work in inherited classes
class Wl_Dialog_Progress(wl_dialogs.Wl_Dialog_Frameless):
    def __init__(self, main, text):
        super().__init__(main, width = 500)

        self.time_start = time.time()

        self.timer_time_elapsed = QTimer(self)

        self.label_progress = wl_labels.Wl_Label_Dialog(text, self, word_wrap = False)
        self.label_time_elapsed = wl_labels.Wl_Label_Dialog(_tr('Wl_Dialog_Progress', '<div>Elapsed time: 0:00:00</div>'), self, word_wrap = False)
        self.label_processing = wl_labels.Wl_Label_Dialog(_tr('Wl_Dialog_Progress', '''
                <div>Please wait. It may take a few seconds to several minutes for the operation to be completed.</div>
            '''),
            self
        )

        self.timer_time_elapsed.timeout.connect(self.update_elapsed_time)
        self.timer_time_elapsed.start(1000)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.label_progress, 0, 0)
        self.layout().addWidget(self.label_time_elapsed, 0, 1, Qt.AlignRight)
        self.layout().addWidget(self.label_processing, 1, 0, 1, 2)

        self.layout().setContentsMargins(20, 20, 20, 20)

    def update_elapsed_time(self):
        elapsed_time = datetime.timedelta(seconds = round(time.time() - self.time_start))

        self.label_time_elapsed.set_text(_tr('Wl_Dialog_Progress', '<div>Elapsed time: {}</div>').format(elapsed_time))

    def update_progress(self, text):
        self.label_progress.set_text(text)

class Wl_Dialog_Progress_Process_Data(Wl_Dialog_Progress):
    def __init__(self, main):
        super().__init__(main, text = _tr('wl_dialogs_misc', 'Processing data...'))

class Wl_Dialog_Progress_Download_Model(Wl_Dialog_Progress):
    def __init__(self, main):
        super().__init__(main, text = _tr('wl_dialogs_misc', 'Downloading model...'))

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
                <br>
                <div><b>Note: All unsaved data and figures will be lost.</b></div>
            '''),
            self
        )

        self.button_restart = QPushButton(self.tr('Restart'), self)
        self.button_cancel = QPushButton(self.tr('Cancel'), self)

        self.button_restart.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)

        self.layout_info.addWidget(self.label_restart_exit, 0, 0)

        self.layout_buttons.addWidget(self.button_restart, 0, 1)
        self.layout_buttons.addWidget(self.button_cancel, 0, 2)

        self.layout_buttons.setColumnStretch(0, 1)
