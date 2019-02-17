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
import os
import pickle
import platform
import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_checking import *
from wordless_help import *
from wordless_settings import *
from wordless_utils import *
from wordless_widgets import *

import wordless_file_area
import wordless_overview
import wordless_concordancer
import wordless_wordlist
import wordless_ngrams
import wordless_collocation
import wordless_colligation
import wordless_keywords

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

            time.sleep(0.025)

    def fade_out(self):
        while self.windowOpacity() > 0:
            self.setWindowOpacity(self.windowOpacity() - 0.05)

            time.sleep(0.025)

class Wordless_Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.threads_check_updates = []

        self.setWindowTitle(self.tr('Wordless'))
        self.setWindowIcon(QIcon('imgs/wordless_icon.png'))

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

        # Menu
        self.init_menu()

        # Work Area & File Area
        self.init_central_widget()

        # Status Bar
        self.statusBar().showMessage(self.tr('Ready!'))

        self.statusBar().setFixedHeight(22)
        self.statusBar().setStyleSheet('''
            QStatusBar {
                background-color: #D0D0D0;
            }
        ''')

        # Global Style
        self.setStyleSheet(self.settings_global['styles']['style_global'])

        # Check for updates on startup
        if self.settings_custom['updates']['update_settings']['check_updates_on_startup']:
            self.dialog_check_updates = self.help_check_updates(on_startup = True)

        self.load_settings()

    def closeEvent(self, event):
        reply = wordless_message_box.wordless_message_box_exit(self)

        if reply == QMessageBox.Yes:
            # Clear history of closed files
            self.settings_custom['files']['files_closed'].clear()

            # Layouts
            self.settings_custom['layouts']['central_widget'] = self.centralWidget().sizes()

            with open('wordless_settings.pkl', 'wb') as f:
                pickle.dump(self.settings_custom, f)

            event.accept()
        else:
            event.ignore()

    def init_menu(self):
        menu_file = self.menuBar().addMenu(self.tr('File'))
        menu_prefs = self.menuBar().addMenu(self.tr('Preferences'))
        menu_help = self.menuBar().addMenu(self.tr('Help'))

        # File
        menu_file_open_files = QAction(self.tr('Open File(s)...'), self)
        menu_file_open_files.setStatusTip(self.tr('Open file(s)'))

        menu_file_open_dir = QAction(self.tr('Open Folder...'), self)
        menu_file_open_dir.setStatusTip(self.tr('Open all files in folder'))

        menu_file_reopen = QAction(self.tr('Reopen Closed File(s)'), self)
        menu_file_reopen.setStatusTip(self.tr('Reopen closed file(s)'))

        menu_file_select_all = QAction(self.tr('Select All'), self)
        menu_file_select_all.setStatusTip(self.tr('Select all files'))

        menu_file_invert_selection = QAction(self.tr('Invert Selection'), self)
        menu_file_invert_selection.setStatusTip(self.tr('Invert file selection'))

        menu_file_deselect_all = QAction(self.tr('Deselect All'), self)
        menu_file_deselect_all.setStatusTip(self.tr('Deselect all files'))

        menu_file_close_selected = QAction(self.tr('Close Selected'), self)
        menu_file_close_selected.setStatusTip(self.tr('Close selected file(s)'))

        menu_file_close_all = QAction(self.tr('Close All'), self)
        menu_file_close_all.setStatusTip(self.tr('Close all files'))

        menu_file_exit = QAction(self.tr('Exit...'), self)
        menu_file_exit.setStatusTip(self.tr('Exit the program'))
        menu_file_exit.triggered.connect(self.close)

        menu_file.addAction(menu_file_open_files)
        menu_file.addAction(menu_file_open_dir)
        menu_file.addSeparator()
        menu_file.addAction(menu_file_reopen)
        menu_file.addSeparator()
        menu_file.addAction(menu_file_select_all)
        menu_file.addAction(menu_file_invert_selection)
        menu_file.addAction(menu_file_deselect_all)
        menu_file.addSeparator()
        menu_file.addAction(menu_file_close_selected)
        menu_file.addAction(menu_file_close_all)
        menu_file.addSeparator()
        menu_file.addAction(menu_file_exit)

        # Preferences
        menu_prefs_settings = QAction(self.tr('Settings'), self)
        menu_prefs_settings.setStatusTip(self.tr('Change settings'))
        menu_prefs_settings.triggered.connect(self.wordless_settings.load)

        menu_prefs_reset_layouts = QAction(self.tr('Reset Layouts'), self)
        menu_prefs_reset_layouts.setStatusTip(self.tr('Reset Layouts'))
        menu_prefs_reset_layouts.triggered.connect(self.prefs_reset_layouts)

        menu_prefs_show_status_bar = QAction(self.tr('Show Status Bar'), self, checkable = True)
        menu_prefs_show_status_bar.setStatusTip(self.tr('Show/Hide the status bar'))
        menu_prefs_show_status_bar.triggered.connect(self.prefs_show_status_bar)

        menu_prefs.addAction(menu_prefs_settings)
        menu_prefs.addAction(menu_prefs_reset_layouts)
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

        menu_help_changelog = QAction(self.tr('Changelog'), self)
        menu_help_changelog.setStatusTip(self.tr('Show Changelog'))
        menu_help_changelog.triggered.connect(self.help_changelog)

        menu_help_about = QAction(self.tr('About Wordless'), self)
        menu_help_about.setStatusTip(self.tr('Show information about Wordless'))
        menu_help_about.triggered.connect(self.help_about)

        menu_help.addAction(menu_help_citing)
        menu_help.addAction(menu_help_acks)
        menu_help.addSeparator()
        menu_help.addAction(menu_help_need_help)
        menu_help.addAction(menu_help_contributing)
        menu_help.addAction(menu_help_donating)
        menu_help.addSeparator()
        menu_help.addAction(menu_help_check_updates)
        menu_help.addAction(menu_help_changelog)
        menu_help.addAction(menu_help_about)

    # Preferences -> Show Status Bar
    def prefs_show_status_bar(self):
        self.settings_custom['menu']['prefs']['show_status_bar'] = self.find_menu_item(self.tr('Show Status Bar')).isChecked()

        if self.settings_custom['menu']['prefs']['show_status_bar']:
            self.statusBar().show()
        else:
            self.statusBar().hide()

    # Preferences -> Reset Layouts
    def prefs_reset_layouts(self):
        reply = wordless_message_box.wordless_message_box_reset_layouts(self)

        if reply:
            self.centralWidget().setSizes([self.height() - 210, 210])

    # Help -> Citing
    def help_citing(self):
        dialog_citing = wordless_citing.Wordless_Dialog_Citing(self)

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
        dialog_donating = wordless_donating.Wordless_Dialog_Donating(self)

        dialog_donating.open()

    # Help -> Check for Updates
    def help_check_updates(self, on_startup = False):
        dialog_check_updates = wordless_check_updates.Wordless_Dialog_Check_Updates(self)

        if not on_startup:
            dialog_check_updates.open()

    # Help -> Changelog
    def help_changelog(self):
        dialog_changelog = wordless_changelog.Wordless_Dialog_Changelog(self)

        dialog_changelog.open()

    # Help -> About Wordless
    def help_about(self):
        dialog_about = wordless_about.Wordless_Dialog_About(self)

        dialog_about.open()

    def init_central_widget(self):
        self.wordless_file_area = wordless_file_area.Wrapper_File_Area(self)
        self.init_work_area()

        wrapper_file_area = QWidget()

        wrapper_file_area.setLayout(QGridLayout())
        wrapper_file_area.layout().addWidget(self.wordless_file_area, 0, 0)

        if platform.system() == 'Windows':
            self.wordless_file_area.layout().setContentsMargins(2, 0, 2, 0)
            wrapper_file_area.layout().setContentsMargins(0, 0, 2, 0)
        else:
            wrapper_file_area.layout().setContentsMargins(0, 0, 0, 0)

        splitter_central_widget = wordless_layout.Wordless_Splitter(Qt.Vertical, self)
        splitter_central_widget.addWidget(self.wordless_work_area)
        splitter_central_widget.addWidget(wrapper_file_area)

        splitter_central_widget.setHandleWidth(1)
        splitter_central_widget.setObjectName('splitter-central-widget')
        splitter_central_widget.setStyleSheet('''
            QSplitter#splitter-central-widget {
                padding: 4px 6px;
            }
        ''')

        splitter_central_widget.setStretchFactor(0, 1)

        self.setCentralWidget(splitter_central_widget)

    def init_work_area(self):
        def load_settings():
            work_area_cur = self.settings_custom['work_area_cur']

            for i in range(self.wordless_work_area.count()):
                if self.wordless_work_area.tabText(i) == work_area_cur:
                    self.wordless_work_area.setCurrentIndex(i)

                    break

            work_area_changed()

        def work_area_changed():
            self.settings_custom['work_area_cur'] = self.wordless_work_area.tabText(self.wordless_work_area.currentIndex())

        self.wordless_work_area = QTabWidget(self)
        self.wordless_work_area.addTab(wordless_overview.Wrapper_Overview(self), self.tr('Overview'))
        self.wordless_work_area.addTab(wordless_concordancer.Wrapper_Concordancer(self), self.tr('Concordancer'))
        self.wordless_work_area.addTab(wordless_wordlist.Wrapper_Wordlist(self), self.tr('Wordlist'))
        self.wordless_work_area.addTab(wordless_ngrams.Wrapper_Ngrams(self), self.tr('N-grams'))
        self.wordless_work_area.addTab(wordless_collocation.Wrapper_Collocation(self), self.tr('Collocation'))
        self.wordless_work_area.addTab(wordless_colligation.Wrapper_Colligation(self), self.tr('Colligation'))
        self.wordless_work_area.addTab(wordless_keywords.Wrapper_Keywords(self), self.tr('Keywords'))

        self.wordless_work_area.currentChanged.connect(work_area_changed)

        load_settings()

    def load_settings(self):
        settings = copy.deepcopy(self.settings_custom)

        # Menu
        self.find_menu_item(self.tr('Show Status Bar')).setChecked(settings['menu']['prefs']['show_status_bar'])

        # Layouts
        self.centralWidget().setSizes(settings['layouts']['central_widget'])

    def find_menu_item(self, text, menu = None):
        menu_item = None

        if not menu:
            menu = self.menuBar()

        for action in menu.actions():
            if menu_item:
                break

            if action.menu():
                menu_item = self.find_menu_item(text, menu = action.menu())
            else:
                if action.text() == text:
                    menu_item = action

        return menu_item

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
    