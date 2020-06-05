#
# Wordless: Utilities - Threading
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
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
    worker_done = pyqtSignal()

    def __init__(self, main, dialog_progress, update_gui, **kwargs):
        super().__init__()

        self.main = main
        self.dialog_progress = dialog_progress

        # Additional arguments
        for key, val in kwargs.items():
            self.__dict__[key] = val

        self.progress_updated.connect(self.dialog_progress.update_progress)
        self.worker_done.connect(update_gui)
        self.worker_done.connect(self.dialog_progress.accept)

class Wordless_Worker_No_Progress(QObject):
    worker_done = pyqtSignal()

    def __init__(self, main, update_gui, **kwargs):
        super().__init__()

        self.main = main

        # Additional arguments
        for key, val in kwargs.items():
            self.__dict__[key] = val

        self.worker_done.connect(update_gui)

class Wordless_Thread(QThread):
    def __init__(self, worker):
        super().__init__()

        self.worker = worker

        self.worker.moveToThread(self)

        self.started.connect(worker.run)
        self.finished.connect(worker.deleteLater)

    def start_worker(self):
        self.start()

        self.worker.dialog_progress.exec_()

        self.quit()
        self.wait()

class Wordless_Thread_No_Progress(Wordless_Thread):
    def start_worker(self):
        self.start()

        self.quit()
