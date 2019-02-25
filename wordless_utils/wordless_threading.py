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

class Wordless_Worker(QObject):
    def __init__(self, main):
        super().__init__()

        self.main = main

class Wordless_Worker_Process_Data(Wordless_Worker):
    progress_updated = pyqtSignal(str)

    def __init__(self, main, dialog_progress, data_received):
        super().__init__(main)

        self.progress_updated.connect(dialog_progress.update_progress)
        self.processing_finished.connect(data_received)

class Wordless_Thread(QThread):
    def __init__(self, worker):
        super().__init__()

        worker.moveToThread(self)

        self.finished.connect(worker.deleteLater)

class Wordless_Thread_Process_Data(Wordless_Thread):
    def __init__(self, worker_process_data):
        super().__init__(worker_process_data)

        self.started.connect(worker_process_data.process_data)

class Wordless_Thread_Search_Results(Wordless_Thread):
    def __init__(self, worker_search_results):
        super().__init__(worker_search_results)

        self.started.connect(worker_search_results.search_results)
