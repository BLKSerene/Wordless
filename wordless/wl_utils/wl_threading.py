# ----------------------------------------------------------------------
# Wordless: Utilities - Threading
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

import time

from PyQt5.QtCore import (
    pyqtSignal,
    QObject,
    Qt,
    QThread
)

# Workers
class Wl_Worker(QObject):
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

        # Wait for updating of the progress label
        self.worker_done.connect(lambda: time.sleep(.01), Qt.DirectConnection)
        self.worker_done.connect(update_gui)
        self.worker_done.connect(self.dialog_progress.accept)

class Wl_Worker_No_Progress(QObject):
    worker_done = pyqtSignal()

    def __init__(self, main, update_gui, **kwargs):
        super().__init__()

        self.main = main

        # Additional arguments
        for key, val in kwargs.items():
            self.__dict__[key] = val

        self.worker_done.connect(update_gui)

class Wl_Worker_No_Callback(QObject):
    progress_updated = pyqtSignal(str)
    worker_done = pyqtSignal()

    def __init__(self, main, dialog_progress, **kwargs):
        super().__init__()

        self.main = main
        self.dialog_progress = dialog_progress

        # Additional arguments
        for key, val in kwargs.items():
            self.__dict__[key] = val

        self.progress_updated.connect(self.dialog_progress.update_progress)

        # Wait for updating of the progress label
        self.worker_done.connect(lambda: time.sleep(.01), Qt.DirectConnection)
        self.worker_done.connect(self.dialog_progress.accept)

# Threads
class Wl_Thread(QThread):
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

class Wl_Thread_No_Progress(Wl_Thread):
    def start_worker(self):
        self.start()

        self.quit()
