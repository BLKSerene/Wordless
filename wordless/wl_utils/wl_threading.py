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

from PyQt5 import QtCore

# Workers
class Wl_Worker(QtCore.QObject):
    progress_updated = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()

    def __init__(self, main, dialog_progress, **kwargs):
        super().__init__()

        self.main = main
        self._running = True
        self.dialog_progress = dialog_progress

        # Additional arguments
        for key, val in kwargs.items():
            self.__dict__[key] = val

        self.progress_updated.connect(self.dialog_progress.update_progress)

        if hasattr(self.dialog_progress, 'button_abort'):
            self.dialog_progress.button_abort.clicked.connect(self.stop)

    def stop(self):
        self._running = False

class Wl_Worker_No_Progress(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    def __init__(self, main, **kwargs):
        super().__init__()

        self.main = main
        self._running = True

        # Additional arguments
        for key, val in kwargs.items():
            self.__dict__[key] = val

    def stop(self):
        self._running = False

def start_worker_in_thread(worker, thread, update_gui = None):
    worker.moveToThread(thread)

    thread.started.connect(worker.run)

    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    # Wait for updating of the progress label
    worker.finished.connect(lambda: time.sleep(.01), QtCore.Qt.DirectConnection)

    if update_gui:
        worker.finished.connect(update_gui)

    if hasattr(worker, 'dialog_progress'):
        worker.finished.connect(worker.dialog_progress.accept)

    thread.finished.connect(thread.deleteLater)

    thread.start()

    if hasattr(worker, 'dialog_progress'):
        worker.dialog_progress.exec()
