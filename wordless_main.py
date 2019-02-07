#
# Wordless: Main Window
#
# Copyright (C) 2018-2019  Ye Lei (叶磊))
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import ctypes
import os
import pickle
import sys
import threading
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import requests

from wordless_checking import *
from wordless_help import *
from wordless_settings import *
from wordless_utils import *
from wordless_widgets import *

import wordless_files

import tab_overview
import tab_concordancer
import tab_wordlist
import tab_ngrams
import tab_collocation
import tab_colligation
import tab_keywords

class Wordless_Loading(QSplashScreen):
    def __init__(self):
        super().__init__(QPixmap('imgs/wordless_loading.png'))

        self.setFont(QFont('Times New Roman', pointSize = 12))
        self.showMessage(self.tr('Loading Wordless...\nPlease wait, it may take a few seconds.'), alignment = Qt.AlignHCenter | Qt.AlignBottom, color = Qt.white)

    def fade_in(self):
        self.setWindowOpacity(0)
        self.show()

        while self.windowOpacity() < 1:
            self.setWindowOpacity(self.windowOpacity() + 0.05)

            time.sleep(0.05)

    def fade_out(self):
        while self.windowOpacity() > 0:
            self.setWindowOpacity(self.windowOpacity() - 0.05)

            time.sleep(0.05)

class Worker_Check_Updates(QObject):
    finished = pyqtSignal()
    check_updates_finished = pyqtSignal(str, str)

    def __init__(self, main):
        super().__init__()

        self.main = main
        self.stopped = False

    def check_updates(self):
        num_retries = 0
        version_new = ''

        try:
            r = requests.get('https://raw.githubusercontent.com/BLKSerene/Wordless/master/VERSION', timeout = 15)

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

class Wordless_Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.threads_check_updates = []

        self.setWindowTitle(self.tr('Wordless Version 1.0.0'))
        self.setWindowIcon(QIcon('imgs/wordless_icon.png'))

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('wordless')

        # Settings
        init_settings_global.init_settings_global(self)
        init_settings_default.init_settings_default(self)

        if os.path.exists('wordless_settings.pkl'):
            with open(r'wordless_settings.pkl', 'rb') as f:
                settings_custom = pickle.load(f)

            if wordless_checking_misc.check_custom_settings(settings_custom, self.settings_default):
                self.settings_custom = settings_custom
            else:
                self.settings_custom = copy.deepcopy(self.settings_default)
        else:
            self.settings_custom = copy.deepcopy(self.settings_default)

        self.wordless_settings = wordless_settings.Wordless_Settings(self)

        # Tabs
        tab_cur = self.settings_custom['tab_cur']

        self.init_central_widget()

        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == tab_cur:
                self.tabs.setCurrentIndex(i)

                break

        # Menu
        self.init_menu()

        # Status Bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage(self.tr('Ready!'))

        self.setStyleSheet(self.settings_global['styles']['style_global'])

        # Check for updates on startup
        if self.settings_custom['updates']['update_settings']['check_updates_on_startup']:
            self.dialog_check_updates = self.help_check_updates(on_startup = True)

    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                     self.tr('Exit Confirmation'),
                                     self.tr(f'''{self.settings_global['styles']['style_dialog']}
                                                 <body>
                                                     <div>Do you really want to quit?</div>
                                                 </body>
                                             '''),
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Reset some settings
            self.settings_custom['files']['files_closed'].clear()

            with open('wordless_settings.pkl', 'wb') as f:
                pickle.dump(self.settings_custom, f)

            event.accept()
        else:
            event.ignore()

    def init_menu(self):
        menu = self.menuBar()
        menu_file = menu.addMenu(self.tr('File'))
        menu_prefs = menu.addMenu(self.tr('Preferences'))
        menu_help = menu.addMenu(self.tr('Help'))

        # File
        menu_file_open_files = QAction(self.tr('Open File(s)...'), self)
        menu_file_open_files.setStatusTip(self.tr('Open file(s)'))
        menu_file_open_files.triggered.connect(self.open_files)

        menu_file_open_dir = QAction(self.tr('Open Folder...'), self)
        menu_file_open_dir.setStatusTip(self.tr('Open a folder'))
        menu_file_open_dir.triggered.connect(self.open_dir)

        menu_file_close_selected = QAction(self.tr('Close Selected File(s)'), self)
        menu_file_close_selected.setStatusTip(self.tr('Close selected file(s)'))
        menu_file_close_selected.triggered.connect(self.close_selected)

        menu_file_close_all = QAction(self.tr('Close All Files'), self)
        menu_file_close_all.setStatusTip(self.tr('Close all files'))
        menu_file_close_all.triggered.connect(self.close_all)

        menu_file_reopen = QAction(self.tr('Reopen Closed File(s)'), self)
        menu_file_reopen.setStatusTip(self.tr('Reopen closed file(s)'))
        menu_file_reopen.triggered.connect(self.reopen)

        menu_file_exit = QAction(self.tr('Exit...'), self)
        menu_file_exit.setStatusTip(self.tr('Exit the program'))
        menu_file_exit.triggered.connect(self.close)

        menu_file_reopen.setEnabled(False)

        menu_file.addAction(menu_file_open_files)
        menu_file.addAction(menu_file_open_dir)
        menu_file.addSeparator()
        menu_file.addAction(menu_file_close_selected)
        menu_file.addAction(menu_file_close_all)
        menu_file.addSeparator()
        menu_file.addAction(menu_file_reopen)
        menu_file.addSeparator()
        menu_file.addAction(menu_file_exit)

        # Preferences
        menu_prefs_settings = QAction(self.tr('Settings'), self)
        menu_prefs_settings.setStatusTip(self.tr('Change settings'))
        menu_prefs_settings.triggered.connect(self.wordless_settings.load)

        menu_prefs_show_status_bar = QAction(self.tr('Show Status Bar'), self, checkable = True)
        menu_prefs_show_status_bar.setChecked(True)
        menu_prefs_show_status_bar.setStatusTip(self.tr('Show/Hide the status bar'))
        menu_prefs_show_status_bar.triggered.connect(self.prefs_show_status_bar)

        menu_prefs.addAction(menu_prefs_settings)
        menu_prefs.addSeparator()
        menu_prefs.addAction(menu_prefs_show_status_bar)

        # Help
        menu_help_need_help = QAction(self.tr('Need Help?'), self)
        menu_help_need_help.setStatusTip(self.tr('Show help information'))
        menu_help_need_help.triggered.connect(self.help_need_help)

        menu_help_contributing = QAction(self.tr('Contributing'), self)
        menu_help_contributing.setStatusTip(self.tr('Show information about contributing'))
        menu_help_contributing.triggered.connect(self.help_contributing)

        menu_help_donating = QAction(self.tr('Donating'), self)
        menu_help_donating.setStatusTip(self.tr('Show information about donating'))
        menu_help_donating.triggered.connect(self.help_donating)

        menu_help_citing = QAction(self.tr('Citing'), self)
        menu_help_citing.setStatusTip(self.tr('Show information about citing'))
        menu_help_citing.triggered.connect(self.help_citing)

        menu_help_acks = QAction(self.tr('Acknowledgments'), self)
        menu_help_acks.setStatusTip(self.tr('Show acknowldgments'))
        menu_help_acks.triggered.connect(self.help_acks)

        menu_help_check_updates = QAction(self.tr('Check for Updates'), self)
        menu_help_check_updates.setStatusTip(self.tr('Check for the latest version of Wordless'))
        menu_help_check_updates.triggered.connect(self.help_check_updates)

        menu_help_about_wordless = QAction(self.tr('About Wordless'), self)
        menu_help_about_wordless.setStatusTip(self.tr('Show information about Wordless'))
        menu_help_about_wordless.triggered.connect(self.help_about_wordless)

        menu_help.addAction(menu_help_citing)
        menu_help.addAction(menu_help_acks)
        menu_help.addSeparator()
        menu_help.addAction(menu_help_need_help)
        menu_help.addAction(menu_help_contributing)
        menu_help.addAction(menu_help_donating)
        menu_help.addSeparator()
        menu_help.addAction(menu_help_check_updates)
        menu_help.addAction(menu_help_about_wordless)

    # Preferences -> Show Status Bar
    def prefs_show_status_bar(self):
        if self.status_bar.isVisible():
            self.status_bar.hide()
        else:
            self.status_bar.show()

    # Help -> Citing
    def help_citing(self):
        def citation_sys_changed():
            if combo_box_citation_sys.currentText() == self.tr('MLA (8th Edition)'):
                text_edit_citing.setHtml('Ye Lei. Wordless, version 1.0.0, 2019, https://github.com/BLKSerene/Wordless.')
            elif combo_box_citation_sys.currentText() == self.tr('APA (6th Edition)'):
                text_edit_citing.setHtml('Ye, L. (2019) Wordless (Version 1.0.0) [Computer Software]. Retrieved from https://github.com/BLKSerene/Wordless')
            elif combo_box_citation_sys.currentText() == self.tr('GB (GB/T 7714—2015)'):
                text_edit_citing.setHtml('叶磊. Wordless version 1.0.0[CP]. (2019). https://github.com/BLKSerene/Wordless.')

            if combo_box_citation_sys.currentText() == self.tr('GB (GB/T 7714—2015)'):
                text_edit_citing.setFont(QFont('宋体', 12))
            else:
                text_edit_citing.setFont(QFont('Times New Roman', 12))

        def copy():
            text_edit_citing.setFocus()
            text_edit_citing.selectAll()
            text_edit_citing.copy()

        dialog_citing = wordless_dialog.Wordless_Dialog_Info(self, self.tr('Citing'),
                                                             width = 400,
                                                             height = 150,
                                                             no_button = True)

        label_citing = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    If you publish work that uses Wordless, please cite as follows.
                </div>
            '''), self)
        label_citation_sys = QLabel(self.tr('Citation System:'), self)
        combo_box_citation_sys = wordless_box.Wordless_Combo_Box(self)
        text_edit_citing = QTextEdit(self)

        button_copy = QPushButton(self.tr('Copy'), self)
        button_close = QPushButton(self.tr('Close'), self)

        combo_box_citation_sys.addItems([
                                             self.tr('MLA (8th Edition)'),
                                             self.tr('APA (6th Edition)'),
                                             self.tr('GB (GB/T 7714—2015)')
                                        ])

        button_copy.setFixedWidth(100)
        button_close.setFixedWidth(100)

        text_edit_citing.setFixedHeight(100)
        text_edit_citing.setReadOnly(True)

        combo_box_citation_sys.currentTextChanged.connect(citation_sys_changed)

        button_copy.clicked.connect(copy)
        button_close.clicked.connect(dialog_citing.accept)

        layout_citation_sys = QGridLayout()
        layout_citation_sys.addWidget(label_citation_sys, 0, 0)
        layout_citation_sys.addWidget(combo_box_citation_sys, 0, 1)

        layout_citation_sys.setColumnStretch(2, 1)

        dialog_citing.wrapper_info.layout().addWidget(label_citing, 0, 0, 1, 2)
        dialog_citing.wrapper_info.layout().addLayout(layout_citation_sys, 1, 0, 1, 2)
        dialog_citing.wrapper_info.layout().addWidget(text_edit_citing, 2, 0, 1, 2)

        dialog_citing.wrapper_buttons.layout().addWidget(button_copy, 0, 0)
        dialog_citing.wrapper_buttons.layout().addWidget(button_close, 0, 1)

        citation_sys_changed()

        dialog_citing.open()

    # Help -> Acknowledgments
    def help_acks(self):
        dialog_acks = wordless_acks.Wordless_Dialog_Acks(self)

        dialog_acks.open()

    # Help -> Need Help?
    def help_need_help(self):
        message_box = wordless_message_box.Wordless_Message_Box_Info(
            main = self,
            title = self.tr('Need Help?'),
            text = self.tr('''
                <div>
                    If you encounter a problem, find a bug or require any further information, feel free to ask questions, submit bug reports or provide feedback by <a href="https://github.com/BLKSerene/Wordless/issues/new">creating an issue</a> on Github if you fail to find the answer by searching <a href="https://github.com/BLKSerene/Wordless/issues">existing issues</a> first.
                </div>

                <div>
                    If you need to post sample texts or other information that cannot be shared or you do not want to share publicly, you may <a href="mailto:blkserene@gmail.com">send me an email</a>.
                </div>

                <div>
                    <span style="color: #F00;"><b>Important Note</b></span>: I <b>CANNOT GUARANTEE</b> that all emails will always be checked or replied in time. I <b>WILL NOT REPLY</b> to irrelevant emails and I reserve the right to <b>BLOCK AND/OR REPORT</b> people who send me spam emails.
                </div>

                <div>
                    Home Page: <a href="https://github.com/BLKSerene/Wordless">https://github.com/BLKSerene/Wordless</a><br>
                    Documentation: <a href="https://github.com/BLKSerene/Wordless#documentation">https://github.com/BLKSerene/Wordless#documentation</a><br>
                    Email: <a href="mailto:blkserene@gmail.com">blkserene@gmail.com</a><br>
                    <a href="https://www.wechat.com/en/">WeChat</a> Official Account: Wordless
                </div>
            '''))

        message_box.open()

    # Help -> Contributing
    def help_contributing(self):
        message_box = wordless_message_box.Wordless_Message_Box_Info(
            main = self,
            title = self.tr('Contributing'),
            text = self.tr('''
                <div>
                    If you have an interest in helping the development of Wordless, you may contribute bug fixes, enhancements or new features by <a href="https://github.com/BLKSerene/Wordless/pulls">creating a pull request</a> on Github.
                </div>

                <div>
                    Besides, you may contribute by submitting enhancement proposals or feature requests, write tutorials or <a href ="https://github.com/BLKSerene/Wordless/wiki">Github Wiki</a> for Wordless, or helping me translate Wordless and its documentation to other languages.
                </div>
            '''))

        message_box.open()

    # Help -> Donating
    def help_donating(self):
        def donating_via_changed():
            if combo_box_donating_via.currentText() == self.tr('PayPal'):
                label_donating_via_img.setText('<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=SJ4RNZSVD766Y"><img src="imgs/donating_paypal.gif"></a>')

                dialog_donating.setFixedHeight(280)
            elif combo_box_donating_via.currentText() == self.tr('Alipay (Recommended)'):
                label_donating_via_img.setText('<img src="imgs/donating_alipay.png">')

                dialog_donating.setFixedHeight(530)
            elif combo_box_donating_via.currentText() == self.tr('WeChat'):
                label_donating_via_img.setText('<img src="imgs/donating_wechat.png">')

                dialog_donating.setFixedHeight(530)

            label_donating_via_img.adjustSize()
            dialog_donating.move_to_center()

        dialog_donating = wordless_dialog.Wordless_Dialog_Info(self, self.tr('Donating'),
                                                               width = 400,
                                                               height = 280)

        label_donating = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    If you would like to support the development of Wordless, you may donate via PayPal, Alipay (Recommended) or WeChat.
                </div>

                <div>
                    <span style="color: #F00;"><b>Important Note</b></span>: I <b>WILL NOT PROVIDE</b> refund services, private email/phone support, information concerning my social media, gurantees on bug fixes, enhancements, new features or new releases of Wordless, invoices, receipts or detailed weekly/monthly/yearly/etc. spending report for donation. 
                </div>
            '''), self)
        label_donating_via = QLabel(self.tr('Donating via:'), self)
        combo_box_donating_via = wordless_box.Wordless_Combo_Box(self)
        label_donating_via_img = wordless_label.Wordless_Label_Html('', self)

        combo_box_donating_via.addItems([
                                             self.tr('PayPal'),
                                             self.tr('Alipay (Recommended)'),
                                             self.tr('WeChat')
                                        ])

        combo_box_donating_via.currentTextChanged.connect(donating_via_changed)

        layout_donating_via = QGridLayout()
        layout_donating_via.addWidget(label_donating_via, 0, 0)
        layout_donating_via.addWidget(combo_box_donating_via, 0, 1)

        layout_donating_via.setColumnStretch(2, 1)

        dialog_donating.wrapper_info.layout().addWidget(label_donating, 0, 0)
        dialog_donating.wrapper_info.layout().addLayout(layout_donating_via, 1, 0)
        dialog_donating.wrapper_info.layout().addWidget(label_donating_via_img, 2, 0, Qt.AlignHCenter | Qt.AlignVCenter)

        donating_via_changed()

        dialog_donating.open()

    # Help -> Check for Updates
    def help_check_updates(self, on_startup = False):
        def load_settings():
            checkbox_check_updates_on_startup.setChecked(self.settings_custom['updates']['update_settings']['check_updates_on_startup'])

        def check_updates_on_startup_changed():
            self.settings_custom['updates']['update_settings']['check_updates_on_startup'] = checkbox_check_updates_on_startup.isChecked()

        def check_updates():
            updates_status_changed('checking')

            thread_check_updates = QThread()

            self.threads_check_updates.append(thread_check_updates)

            self.worker_check_updates = Worker_Check_Updates(self)
            self.worker_check_updates.moveToThread(thread_check_updates)

            thread_check_updates.started.connect(self.worker_check_updates.check_updates)
            thread_check_updates.finished.connect(thread_check_updates.deleteLater)
            thread_check_updates.destroyed.connect(lambda: self.threads_check_updates.remove(thread_check_updates))

            if on_startup:
                self.worker_check_updates.check_updates_finished.connect(self.updates_status_on_startup_changed)

            self.worker_check_updates.check_updates_finished.connect(updates_status_changed)
            self.worker_check_updates.finished.connect(thread_check_updates.quit)
            self.worker_check_updates.finished.connect(self.worker_check_updates.deleteLater)

            thread_check_updates.start()

        def check_updates_stopped():
            self.worker_check_updates.stop()

            dialog_check_updates.reject()

        def updates_status_changed(status, version_new = ''):
            if status == 'checking':
                label_check_updates.set_text(self.tr('''
                    <div>
                        Checking for updates...<br>
                        Please wait, it may take a few seconds.
                    </div>
                '''))

                button_try_again.hide()
                button_cancel.setText(self.tr('Cancel'))

                button_cancel.disconnect()
                button_cancel.clicked.connect(check_updates_stopped)
            elif status == 'no_updates':
                label_check_updates.set_text(self.tr('''
                    <div>
                        Hooray, you are using the latest version of Wordless!
                    </div>
                '''))

                button_try_again.hide()
                button_cancel.setText(self.tr('OK'))

                button_cancel.disconnect()
                button_cancel.clicked.connect(dialog_check_updates.accept)
            elif status == 'updates_available':
                label_check_updates.set_text(self.tr(f'''
                    <div>
                        Wordless v{version_new} is out, click <a href="https://github.com/BLKSerene/Wordless/releases"><b>HERE</b></a> to download the latest version of Wordless.
                    </div>
                '''))

                button_try_again.hide()
                button_cancel.setText(self.tr('OK'))

                button_cancel.disconnect()
                button_cancel.clicked.connect(dialog_check_updates.accept)
            elif status == 'network_error':
                label_check_updates.set_text(self.tr('''
                    <div>
                        A network error occurred, please check your network settings or try again later.
                    </div>
                '''))

                button_try_again.show()
                button_cancel.setText(self.tr('Close'))

                button_cancel.disconnect()
                button_cancel.clicked.connect(dialog_check_updates.accept)

        dialog_check_updates = wordless_dialog.Wordless_Dialog_Info(self, self.tr('Check for Updates'),
                                                                    width = 420,
                                                                    height = 100,
                                                                    no_button = True)

        label_check_updates = wordless_label.Wordless_Label_Dialog('', self)
        checkbox_check_updates_on_startup = QCheckBox(self.tr('Check for Updates on Startup'), self)
        
        button_try_again = QPushButton(self.tr('Try Again'), self)
        button_cancel = QPushButton(self.tr('Cancel'), self)

        checkbox_check_updates_on_startup.stateChanged.connect(check_updates_on_startup_changed)

        button_try_again.clicked.connect(check_updates)

        dialog_check_updates.wrapper_info.layout().addWidget(label_check_updates, 0, 0)

        dialog_check_updates.wrapper_buttons.layout().addWidget(checkbox_check_updates_on_startup, 0, 0)
        dialog_check_updates.wrapper_buttons.layout().addWidget(button_try_again, 0, 2)
        dialog_check_updates.wrapper_buttons.layout().addWidget(button_cancel, 0, 3)

        dialog_check_updates.wrapper_buttons.layout().setColumnStretch(1, 1)

        load_settings()
        check_updates()

        if not on_startup:
            dialog_check_updates.open()
        else:
            return dialog_check_updates

    # Help -> About Wordless
    def help_about_wordless(self):
        QMessageBox.about(
            self,
            self.tr('About Wordless'),
            self.tr(f'''
                {self.settings_global['styles']['style_dialog_about']}
                <body>
                    <h2>Wordless Version 1.0.0</h2>
                    <div>
                        An Integrated Corpus Tool with Multi-language Support<br>
                        for the Study of Language, Literature and Translation
                    </div>

                    <div>
                        Copyright (C)&nbsp;&nbsp;2018 Ye Lei (<span style="font-family: simsun">叶磊</span>)<br>
                        Licensed Under GNU GPLv3<br>
                        All Other Rights Reserved
                    </div>
                </body>
            '''))

    def init_central_widget(self):
        central_widget = QWidget(self)

        self.widget_files = wordless_files.init(self)

        central_widget.setLayout(QGridLayout())
        central_widget.layout().addWidget(self.init_tabs(), 0, 0)
        central_widget.layout().addWidget(self.widget_files, 1, 0)

        central_widget.layout().setRowStretch(0, 2)
        central_widget.layout().setRowStretch(1, 1)

        self.setCentralWidget(central_widget)

    def init_tabs(self):
        def tab_changed():
            self.settings_custom['tab_cur'] = self.tabs.tabText(self.tabs.currentIndex())

        self.tabs = QTabWidget(self)
        self.tabs.addTab(tab_overview.init(self), self.tr('Overview'))
        self.tabs.addTab(tab_concordancer.init(self), self.tr('Concordancer'))
        self.tabs.addTab(tab_wordlist.init(self), self.tr('Wordlist'))
        self.tabs.addTab(tab_ngrams.init(self), self.tr('N-grams'))
        self.tabs.addTab(tab_collocation.init(self), self.tr('Collocation'))
        self.tabs.addTab(tab_colligation.init(self), self.tr('Colligation'))
        self.tabs.addTab(tab_keywords.init(self), self.tr('Keywords'))

        self.tabs.currentChanged.connect(tab_changed)

        tab_changed()

        return self.tabs

    def updates_status_on_startup_changed(self, status):
        if status == 'updates_available':
            self.dialog_check_updates.open()
            self.dialog_check_updates.setFocus()
        else:
            self.dialog_check_updates.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    wordless_loading = Wordless_Loading()

    wordless_loading.fade_in()
    wordless_loading.raise_()

    app.processEvents()

    wordless_main = Wordless_Main()

    wordless_loading.fade_out()
    wordless_loading.finish(wordless_main)

    wordless_main.showMaximized()

    sys.exit(app.exec_())
    