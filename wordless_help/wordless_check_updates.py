#
# Wordless: Help - Check for Updates
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy

import requests

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_widgets import *

class Worker_Check_Updates(QObject):
    finished = pyqtSignal()
    check_updates_finished = pyqtSignal(str, str)

    def __init__(self, main):
        super().__init__()

        self.main = main
        self.stopped = False

    def check_updates(self):
        version_new = ''

        try:
            r = requests.get('https://raw.githubusercontent.com/BLKSerene/Wordless/master/VERSION', timeout = 10)

            if r.status_code == 200:
                for line in r.text.splitlines():
                    if line and not line.startswith('#'):
                        version_new = line.rstrip()

                if self.is_newer_version(version_new):
                    updates_status = 'updates_available'
                else:
                    updates_status = 'no_updates'
            else:
                updates_status = 'network_error'
        except:
            updates_status = 'network_error'

        if not self.stopped:
            self.check_updates_finished.emit(updates_status, version_new)

        self.finished.emit()

    def is_newer_version(self, version_new):
        with open('VERSION', 'r', encoding = 'utf_8') as f:
            for line in f.readlines():
                line = line.rstrip()

                if line and not line.startswith('#'):
                    major_cur, minor_cur, patch_cur = line.split('.')

        major_new, minor_new, patch_new = version_new.split('.')

        if (int(major_cur) < int(major_new) or
            int(minor_cur) < int(minor_new) or
            int(patch_cur) < int(patch_new)):
            return True
        else:
            return False

    def stop(self):
        self.stopped = True

class Wordless_Dialog_Check_Updates(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main, on_startup = False):
        super().__init__(main, main.tr('Check for Updates'),
                         width = 420,
                         height = 100,
                         no_button = True)

        self.on_startup = on_startup

        self.label_check_updates = wordless_label.Wordless_Label_Dialog('', self.main)
        self.checkbox_check_updates_on_startup = QCheckBox(self.tr('Check for Updates on Startup'), self)
        
        self.button_try_again = QPushButton(self.tr('Try Again'), self)
        self.button_cancel = QPushButton(self.tr('Cancel'), self)

        self.checkbox_check_updates_on_startup.stateChanged.connect(self.check_updates_on_startup_changed)

        self.button_try_again.clicked.connect(self.check_updates)

        self.wrapper_info.layout().addWidget(self.label_check_updates, 0, 0)

        self.wrapper_buttons.layout().addWidget(self.checkbox_check_updates_on_startup, 0, 0)
        self.wrapper_buttons.layout().addWidget(self.button_try_again, 0, 2)
        self.wrapper_buttons.layout().addWidget(self.button_cancel, 0, 3)

        self.wrapper_buttons.layout().setColumnStretch(1, 1)

        self.load_settings()

    def check_updates(self):
        self.updates_status_changed('checking')

        thread_check_updates = QThread()

        self.main.threads_check_updates.append(thread_check_updates)

        self.main.worker_check_updates = Worker_Check_Updates(self.main)
        self.main.worker_check_updates.moveToThread(thread_check_updates)

        thread_check_updates.started.connect(self.main.worker_check_updates.check_updates)
        thread_check_updates.finished.connect(thread_check_updates.deleteLater)
        thread_check_updates.destroyed.connect(lambda: self.main.threads_check_updates.remove(thread_check_updates))

        if self.on_startup:
            self.worker_check_updates.check_updates_finished.connect(self.updates_status_on_startup_changed)

        self.main.worker_check_updates.check_updates_finished.connect(self.updates_status_changed)
        self.main.worker_check_updates.finished.connect(thread_check_updates.quit)
        self.main.worker_check_updates.finished.connect(self.main.worker_check_updates.deleteLater)

        thread_check_updates.start()

    def check_updates_stopped(self):
        self.main.worker_check_updates.stop()

        self.reject()

    def updates_status_changed(self, status, version_new = ''):
        if status == 'checking':
            self.label_check_updates.set_text(self.tr('''
                <div>
                    Checking for updates...<br>
                    Please wait, it may take a few seconds.
                </div>
            '''))

            self.button_try_again.hide()
            self.button_cancel.setText(self.tr('Cancel'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.check_updates_stopped)
        elif status == 'no_updates':
            self.label_check_updates.set_text(self.tr('''
                <div>
                    Hooray, you are using the latest version of Wordless!
                </div>
            '''))

            self.button_try_again.hide()
            self.button_cancel.setText(self.tr('OK'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)
        elif status == 'updates_available':
            self.label_check_updates.set_text(self.tr(f'''
                <div>
                    Wordless v{version_new} is out, click <a href="https://github.com/BLKSerene/Wordless/releases"><b>HERE</b></a> to download the latest version of Wordless.
                </div>
            '''))

            self.button_try_again.hide()
            self.button_cancel.setText(self.tr('OK'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)
        elif status == 'network_error':
            self.label_check_updates.set_text(self.tr('''
                <div>
                    A network error occurred, please check your network settings or try again later.
                </div>
            '''))

            self.button_try_again.show()
            self.button_cancel.setText(self.tr('Close'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)

    def updates_status_on_startup_changed(self, status):
        if status == 'updates_available':
            self.open()
            self.setFocus()
        else:
            self.accept()

    def load_settings(self):
        settings = self.main.settings_custom['updates']

        self.checkbox_check_updates_on_startup.setChecked(settings['update_settings']['check_updates_on_startup'])

        self.check_updates()

    def check_updates_on_startup_changed(self):
        settings = self.main.settings_custom['updates']

        settings['update_settings']['check_updates_on_startup'] = self.checkbox_check_updates_on_startup.isChecked()
