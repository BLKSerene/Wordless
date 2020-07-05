#
# Wordless: Main Window
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
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
import subprocess
import sys
import time

# Fix working directory on macOS
if getattr(sys, '_MEIPASS', False):
    if platform.system() == 'Darwin':
        os.chdir(sys._MEIPASS)

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import matplotlib
import nltk

matplotlib.use('Qt5Agg')
# Force NLTK to prefer NLTK data under the Wordless folder
nltk.data.path.insert(0, os.path.join(os.getcwd(), 'nltk_data'))

from wl_checking import wl_checking_misc
from wl_dialogs import wl_dialog_misc, wl_dialog_help, wl_msg_box
from wl_settings import wl_settings, wl_settings_default, wl_settings_global
from wl_utils import wl_misc
from wl_widgets import wl_layout

import wl_file_area
import wl_overview
import wl_concordancer
import wl_wordlist
import wl_ngram
import wl_collocation
import wl_colligation
import wl_keyword

class Wl_Loading(QSplashScreen):
    def __init__(self):
        super().__init__(QPixmap(wl_misc.get_normalized_path('imgs/wl_loading.png')))

        msg_font = QFont('Times New Roman')
        msg_font.setPixelSize(14)

        self.setFont(msg_font)
        self.show_message(self.tr('Initializing Wordless ...'))

    def show_message(self, message):
        self.showMessage(
            f' {message}',
            color = Qt.white,
            alignment = Qt.AlignLeft | Qt.AlignBottom
        )

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

class Wl_Main(QMainWindow):
    def __init__(self, loading_window):
        super().__init__()

        self.loading_window = loading_window
        self.threads_check_updates = []

        # Version numbers
        self.ver = wl_misc.get_wl_ver()
        self.ver_major, self.ver_minor, self.ver_patch = wl_misc.split_wl_ver(self.ver)

        # Title
        self.setWindowTitle(self.tr(f'Wordless v{self.ver}'))

        # Icon
        self.setWindowIcon(QIcon(wl_misc.get_normalized_path('imgs/wl_icon.ico')))

        self.loading_window.show_message(self.tr('Loading settings ...'))

        # Default settings
        wl_settings_default.init_settings_default(self)

        # Custom settings
        path_settings = wl_misc.get_normalized_path('wl_settings.pickle')

        if os.path.exists(path_settings):
            with open(path_settings, 'rb') as f:
                settings_custom = pickle.load(f)

            if wl_checking_misc.check_custom_settings(settings_custom, self.settings_default):
                self.settings_custom = settings_custom
            else:
                self.settings_custom = copy.deepcopy(self.settings_default)
        else:
            self.settings_custom = copy.deepcopy(self.settings_default)

        # Global settings
        wl_settings_global.init_settings_global(self)

        # Settings
        self.wl_settings = wl_settings.Wl_Settings(self)

        self.loading_window.show_message(self.tr('Initializing main window ...'))

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

        # Check for updates on startup
        self.loading_window.show_message(self.tr('Check for updates ...'))

        if self.settings_custom['general']['update_settings']['check_updates_on_startup']:
            self.dialog_check_updates = self.help_check_updates(on_startup = True)

        self.loading_window.show_message(self.tr('Starting Wordless ...'))

        self.load_settings()

        # Fix layout on macOS
        if platform.system() == 'Darwin':
            self.fix_macos_layout(self)

    def fix_macos_layout(self, parent):
        for widget in parent.children():
            if widget.children():
                self.fix_macos_layout(widget)
            else:
                if isinstance(widget, QWidget) and not isinstance(widget, QPushButton):
                    widget.setAttribute(Qt.WA_LayoutUsesWidgetRect)

    def closeEvent(self, event):
        if self.settings_custom['general']['misc']['confirm_on_exit']:
            dialog_confirm_exit = wl_dialog_misc.Wl_Dialog_Confirm_Exit(self)
            result = dialog_confirm_exit.exec_()

            if result == QDialog.Accepted:
                self.save_settings()

                event.accept()
            elif result == QDialog.Rejected:
                event.ignore()
        else:
            event.accept()

    def init_menu(self):
        menu_file = self.menuBar().addMenu(self.tr('File'))
        menu_prefs = self.menuBar().addMenu(self.tr('Preferences'))
        menu_help = self.menuBar().addMenu(self.tr('Help'))

        # File
        menu_file_open_files = QAction(self.tr('Open File(s)...'), self)
        menu_file_open_files.setStatusTip(self.tr('Open file(s)'))

        menu_file_open_dir = QAction(self.tr('Open Folder...'), self)
        menu_file_open_dir.setStatusTip(self.tr('Open all files in folder'))

        menu_file_reopen = QAction(self.tr('Reopen Closed Files'), self)
        menu_file_reopen.setStatusTip(self.tr('Reopen closed files'))

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
        menu_prefs_settings.triggered.connect(self.wl_settings.load)

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
        if wl_msg_box.wl_msg_box_reset_layouts(self):
            self.centralWidget().setSizes([self.height() - 210, 210])

    # Help -> Citing
    def help_citing(self):
        dialog_citing = wl_dialog_help.Wl_Dialog_Citing(self)

        dialog_citing.open()

    # Help -> Acknowledgments
    def help_acks(self):
        dialog_acks = wl_dialog_help.Wl_Dialog_Acks(self)

        dialog_acks.open()

    # Help -> Need Help?
    def help_need_help(self):
        dialog_need_help = wl_dialog_help.Wl_Dialog_Need_Help(self)

        dialog_need_help.open()

    # Help -> Contributing
    def help_contributing(self):
        msg_box = wl_msg_box.Wl_Msg_Box_Info_Help(
            main = self,
            title = self.tr('Contributing'),
            text = self.tr('''
                <div>
                    If you have an interest in helping the development of Wordless, you may contribute bug fixes, enhancements, or new features by <a href="https://github.com/BLKSerene/Wordless/pulls">creating a pull request</a> on Github.
                </div>

                <div>
                    Besides, you may contribute by submitting enhancement proposals or feature requests, write tutorials or <a href ="https://github.com/BLKSerene/Wordless/wiki">Github Wiki</a> for Wordless, or helping me translate Wordless and its documentation to other languages.
                </div>
            ''')
        )

        msg_box.open()

    # Help -> Donating
    def help_donating(self):
        dialog_donating = wl_dialog_help.Wl_Dialog_Donating(self)

        dialog_donating.open()

    # Help -> Check for Updates
    def help_check_updates(self, on_startup = False):
        dialog_check_updates = wl_dialog_help.Wl_Dialog_Check_Updates(self, on_startup = on_startup)

        if not on_startup:
            dialog_check_updates.open()

    # Help -> Changelog
    def help_changelog(self):
        dialog_changelog = wl_dialog_help.Wl_Dialog_Changelog(self)

        dialog_changelog.open()

    # Help -> About Wordless
    def help_about(self):
        dialog_about = wl_dialog_help.Wl_Dialog_About(self)

        dialog_about.open()

    def init_central_widget(self):
        self.wl_file_area = wl_file_area.Wrapper_File_Area(self)
        self.init_work_area()

        wrapper_file_area = QWidget()

        wrapper_file_area.setLayout(wl_layout.Wl_Layout())
        wrapper_file_area.layout().addWidget(self.wl_file_area, 0, 0)

        if platform.system() == 'Windows':
            self.wl_file_area.layout().setContentsMargins(2, 0, 2, 0)
            wrapper_file_area.layout().setContentsMargins(0, 0, 2, 0)
        elif platform.system() == 'Darwin':
            wrapper_file_area.layout().setContentsMargins(3, 0, 3, 0)
        elif platform.system() == 'Linux':
            self.wl_file_area.layout().setContentsMargins(0, 0, 2, 0)
            wrapper_file_area.layout().setContentsMargins(0, 0, 0, 0)

        splitter_central_widget = wl_layout.Wl_Splitter(Qt.Vertical, self)
        splitter_central_widget.addWidget(self.wl_work_area)
        splitter_central_widget.addWidget(wrapper_file_area)

        if platform.system() in ['Windows', 'Linux']:
            splitter_central_widget.setHandleWidth(1)
        elif platform.system() == 'Darwin':
            splitter_central_widget.setHandleWidth(2)

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

            for i in range(self.wl_work_area.count()):
                if self.wl_work_area.tabText(i) == work_area_cur:
                    self.wl_work_area.setCurrentIndex(i)

                    break

            work_area_changed()

        def work_area_changed():
            self.settings_custom['work_area_cur'] = self.wl_work_area.tabText(self.wl_work_area.currentIndex())

        self.wl_work_area = QTabWidget(self)
        
        self.wl_work_area.addTab(
            wl_overview.Wrapper_Overview(self),
            self.tr('Overview')
        )
        self.wl_work_area.addTab(
            wl_concordancer.Wrapper_Concordancer(self),
            self.tr('Concordancer')
        )
        self.wl_work_area.addTab(
            wl_wordlist.Wrapper_Wordlist(self),
            self.tr('Wordlist')
        )
        self.wl_work_area.addTab(
            wl_ngram.Wrapper_Ngram(self),
            self.tr('N-gram')
        )
        self.wl_work_area.addTab(
            wl_collocation.Wrapper_Collocation(self),
            self.tr('Collocation')
        )
        self.wl_work_area.addTab(
            wl_colligation.Wrapper_Colligation(self),
            self.tr('Colligation')
        )
        self.wl_work_area.addTab(
            wl_keyword.Wrapper_Keyword(self),
            self.tr('Keyword')
        )

        self.wl_work_area.currentChanged.connect(work_area_changed)

        load_settings()

    def load_settings(self):
        settings = copy.deepcopy(self.settings_custom)

        # Fonts
        self.setStyleSheet(f'''
            font-family: {settings['general']['font_settings']['font_family']};
            font-size: {settings['general']['font_settings']['font_size']}px;
        ''')

        # Menu
        self.find_menu_item(self.tr('Show Status Bar')).setChecked(settings['menu']['prefs']['show_status_bar'])

        # Layouts
        self.centralWidget().setSizes(settings['layouts']['central_widget'])

    def save_settings(self):
        # Clear history of closed files
        self.settings_custom['files']['files_closed'].clear()

        # Layouts
        self.settings_custom['layouts']['central_widget'] = self.centralWidget().sizes()

        with open('wl_settings.pickle', 'wb') as f:
            pickle.dump(self.settings_custom, f)

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

    def restart(self):
        if getattr(sys, '_MEIPASS', False):
            if platform.system() == 'Windows':
                subprocess.Popen([wl_misc.get_normalized_path('Wordless.exe')])
            elif platform.system() == 'Darwin':
                subprocess.Popen([wl_misc.get_normalized_path('Wordless')])
            elif platform.system() == 'Linux':
                subprocess.Popen([wl_misc.get_normalized_path('Wordless')])
        else:
            if platform.system() == 'Windows':
                subprocess.Popen(['python', wl_misc.get_normalized_path(__file__)])
            elif platform.system() == 'Darwin':
                subprocess.Popen(['python3', wl_misc.get_normalized_path(__file__)])
            elif platform.system() == 'Linux':
                subprocess.Popen(['python3.7', wl_misc.get_normalized_path(__file__)])

        self.save_settings()
        sys.exit(0)

if __name__ == '__main__':
    wl_app = QApplication(sys.argv)

    wl_loading = Wl_Loading()

    wl_loading.raise_()
    wl_loading.fade_in()

    wl_app.processEvents()

    wl_main = Wl_Main(wl_loading)

    wl_loading.fade_out()
    wl_loading.finish(wl_main)

    wl_main.showMaximized()

    sys.exit(wl_app.exec_())
    