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
    progress_updated = pyqtSignal(str)

    def __init__(self, main, dialog_progress):
        super().__init__()

        self.main = main

        self.progress_updated.connect(dialog_progress.update_progress)

class Wordless_Worker_Process_Data(Wordless_Worker):
    def __init__(self, main, dialog_progress, data_received):
        super().__init__(main, dialog_progress)

        self.processing_finished.connect(data_received)

class Wordless_Worker_Filter_Results(Wordless_Worker):
    filtering_finished = pyqtSignal()

    def __init__(self, main, dialog_filter_results, dialog_progress, data_received):
        super().__init__(main, dialog_progress)

        self.dialog = dialog_filter_results

        self.filtering_finished.connect(data_received)

class Wordless_Worker_Fetch_Data(Wordless_Worker):
    def __init__(self, main, dialog_progress, data_received):
        super().__init__(main, dialog_progress)

        self.fetching_finished.connect(data_received)

class Wordless_Thread(QThread):
    def __init__(self, worker):
        super().__init__()

        worker.moveToThread(self)

        self.finished.connect(worker.deleteLater)

class Wordless_Thread_Add_Files(Wordless_Thread):
    def __init__(self, worker_add_files):
        super().__init__(worker_add_files)

        self.started.connect(worker_add_files.add_files)

class Wordless_Thread_Process_Data(Wordless_Thread):
    def __init__(self, worker_process_data):
        super().__init__(worker_process_data)

        self.started.connect(worker_process_data.process_data)

class Wordless_Thread_Filter_Results(Wordless_Thread):
    def __init__(self, worker_filter_results):
        super().__init__(worker_filter_results)

        self.started.connect(worker_filter_results.filter_results)

class Wordless_Thread_Search_Results(Wordless_Thread):
    def __init__(self, worker_search_results):
        super().__init__(worker_search_results)

        self.started.connect(worker_search_results.search_results)

class Wordless_Thread_Fetch_Data(Wordless_Thread):
    def __init__(self, worker_fetch_data):
        super().__init__(worker_fetch_data)

        self.started.connect(worker_fetch_data.fetch_data)
