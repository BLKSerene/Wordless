#
# Wordless: Utilities - Threading
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

class Worker_Process_Data(QObject):
    progress_updated = pyqtSignal(str)

    def __init__(self, main, dialog_processing, data_received):
        super().__init__()

        self.main = main

        self.progress_updated.connect(dialog_processing.update_progress)
        self.processing_finished.connect(data_received)

class Thread_Process_Data(QThread):
    def __init__(self, worker_process_data):
        super().__init__()

        worker_process_data.moveToThread(self)

        self.started.connect(worker_process_data.process_data)
        self.finished.connect(worker_process_data.deleteLater)
