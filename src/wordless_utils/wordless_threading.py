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
    worker_done = pyqtSignal()

    def __init__(self, main, dialog_progress, update_gui):
        super().__init__()

        self.main = main

        self.progress_updated.connect(dialog_progress.update_progress)
        self.worker_done.connect(update_gui)

class Wordless_Thread(QThread):
    def __init__(self, worker):
        super().__init__()

        worker.moveToThread(self)

        try:
            self.started.connect(worker.run)
        except:
            pass
        self.finished.connect(worker.deleteLater)
