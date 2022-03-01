# ----------------------------------------------------------------------
# Wordless: Main Window
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import copy
import csv
import os
import pickle
import platform
import re
import subprocess
import sys
import time
import traceback

# Fix working directory on macOS
if getattr(sys, '_MEIPASS', False):
    if platform.system() == 'Darwin':
        os.chdir(sys._MEIPASS)

import matplotlib
import nltk
import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pythainlp
import underthesea.file_utils

# Use Qt backend for Matplotlib
matplotlib.use('Qt5Agg')

if getattr(sys, '_MEIPASS', False):
    # Modify path of NLTK's data files
    nltk.data.path = [os.path.join(os.getcwd(), 'nltk_data')]

    # Modify path of PyThaiNLP's data files
    PYTHAINLP_DEFAULT_DATA_DIR = os.path.realpath(pythainlp.tools.PYTHAINLP_DEFAULT_DATA_DIR)
    pythainlp.corpus._CORPUS_DB_PATH = os.path.join(PYTHAINLP_DEFAULT_DATA_DIR, pythainlp.corpus._CORPUS_DB_FILENAME)
    pythainlp.tools.path.get_pythainlp_data_path = lambda: PYTHAINLP_DEFAULT_DATA_DIR

    # Modify path of Underthesea's data files
    underthesea.file_utils.UNDERTHESEA_FOLDER = '.underthesea'

from wl_checking import wl_checking_misc
from wl_dialogs import wl_dialogs, wl_dialogs_misc, wl_msg_boxes
from wl_settings import wl_settings, wl_settings_default, wl_settings_global
from wl_utils import wl_misc, wl_threading
from wl_widgets import wl_boxes, wl_labels, wl_layouts, wl_tables

import wl_file_area
import wl_profiler
import wl_concordancer
import wl_concordancer_parallel
import wl_wordlist_generator
import wl_ngram_generator
import wl_collocation_extractor
import wl_colligation_extractor
import wl_keyword_extractor

class Wl_Loading(QSplashScreen):
    def __init__(self):
        super().__init__(QPixmap(wl_misc.get_normalized_path('imgs/wl_loading.png')))

        msg_font = QFont('Times New Roman')
        msg_font.setPixelSize(14)

        self.setFont(msg_font)
        self.show_message(self.tr('Initializing Wordless...'))

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

        # Icon
        self.setWindowIcon(QIcon(wl_misc.get_normalized_path('imgs/wl_icon.ico')))
        # Title
        self.setWindowTitle('Wordless')

        # Version numbers
        self.ver = wl_misc.get_wl_ver()
        self.ver_major, self.ver_minor, self.ver_patch = wl_misc.split_wl_ver(self.ver)
        # Email
        self.email = 'blkserene@gmail.com'
        self.email_html = '<a href="mailto:blkserene@gmail.com">blkserene@gmail.com</a>'

        self.loading_window = loading_window
        self.threads_check_updates = []

        self.loading_window.show_message(self.tr('Loading settings...'))

        # Default settings
        wl_settings_default.init_settings_default(self)

        # Custom settings
        if os.path.exists('wl_settings.pickle'):
            with open('wl_settings.pickle', 'rb') as f:
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

        self.loading_window.show_message(self.tr('Initializing main window...'))

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

        self.load_settings()

        # Fix layout on macOS
        if platform.system() == 'Darwin':
            self.fix_macos_layout(self)

        self.loading_window.show_message(self.tr('Starting Wordless...'))

    def fix_macos_layout(self, parent):
        for widget in parent.children():
            if widget.children():
                self.fix_macos_layout(widget)
            else:
                if isinstance(widget, QWidget) and not isinstance(widget, QPushButton):
                    widget.setAttribute(Qt.WA_LayoutUsesWidgetRect)

    def closeEvent(self, event):
        if self.settings_custom['general']['misc']['confirm_on_exit']:
            dialog_confirm_exit = wl_dialogs_misc.Wl_Dialog_Confirm_Exit(self)
            result = dialog_confirm_exit.exec_()

            if result == QDialog.Accepted:
                self.save_settings()

                event.accept()
            elif result == QDialog.Rejected:
                event.ignore()
        else:
            event.accept()

    def init_menu(self):
        self.menu_file = self.menuBar().addMenu(self.tr('&File'))
        self.menu_prefs = self.menuBar().addMenu(self.tr('&Preferences'))
        self.menu_help = self.menuBar().addMenu(self.tr('&Help'))

        # File
        self.action_file_open_files = self.menu_file.addAction(self.tr('&Open Files...'))
        self.action_file_open_files.setShortcut(QKeySequence('Ctrl+O'))
        self.action_file_open_files.setStatusTip(self.tr('Open files'))
        self.action_file_open_dir = self.menu_file.addAction(self.tr('Open &Folder...'))
        self.action_file_open_dir.setStatusTip(self.tr('Open all files in the folder'))
        self.action_file_reopen = self.menu_file.addAction(self.tr('&Reopen Closed Files'))
        self.action_file_reopen.setStatusTip(self.tr('Reopen closed files'))

        self.menu_file.addSeparator()

        self.action_file_select_all = self.menu_file.addAction(self.tr('S&elect All'))
        self.action_file_select_all.setShortcut(QKeySequence('Ctrl+A'))
        self.action_file_select_all.setStatusTip(self.tr('Select all files'))
        self.action_file_deselect_all = self.menu_file.addAction(self.tr('&Deselect All'))
        self.action_file_deselect_all.setShortcut(QKeySequence('Ctrl+D'))
        self.action_file_deselect_all.setStatusTip(self.tr('Deselect all files'))
        self.action_file_invert_selection = self.menu_file.addAction(self.tr('&Invert Selection'))
        self.action_file_invert_selection.setShortcut(QKeySequence('Ctrl+Shift+I'))
        self.action_file_invert_selection.setStatusTip(self.tr('Invert file selection'))

        self.menu_file.addSeparator()

        self.action_file_close_selected = self.menu_file.addAction(self.tr('&Close Selected'))
        self.action_file_close_selected.setShortcut(QKeySequence('Ctrl+W'))
        self.action_file_close_selected.setStatusTip(self.tr('Close selected file(s)'))
        self.action_file_close_all = self.menu_file.addAction(self.tr('C&lose All'))
        self.action_file_close_all.setShortcut(QKeySequence('Ctrl+Shift+W'))
        self.action_file_close_all.setStatusTip(self.tr('Close all files'))

        self.menu_file.addSeparator()

        self.action_file_exit = self.menu_file.addAction(self.tr('&Exit...'))
        self.action_file_exit.setShortcut(QKeySequence('Ctrl+Q'))
        self.action_file_exit.setStatusTip(self.tr('Exit the program'))
        self.action_file_exit.triggered.connect(self.close)

        # Preferences
        self.action_prefs_settings = self.menu_prefs.addAction(self.tr('&Settings'))
        self.action_prefs_settings.setStatusTip(self.tr('Change settings'))
        self.action_prefs_settings.triggered.connect(self.wl_settings.load)
        self.menu_prefs_display_lang = self.menu_prefs.addMenu(self.tr('&Display Language'))
        self.menu_prefs_display_lang.setStatusTip(self.tr('Change display language'))

        self.action_group_prefs_display_lang = QActionGroup(self.menu_prefs_display_lang)
        self.action_group_prefs_display_lang.setExclusive(True)

        for action_lang, action_text in [
            ['zho_cn', self.tr('中文（简体）')],
            ['eng_us', self.tr('English (United States)')]
        ]:
            self.__dict__[f'action_prefs_display_lang_{action_lang}'] = self.menu_prefs_display_lang.addAction(action_text)
            self.__dict__[f'action_prefs_display_lang_{action_lang}'].lang = action_lang
            self.__dict__[f'action_prefs_display_lang_{action_lang}'].setCheckable(True)
            self.__dict__[f'action_prefs_display_lang_{action_lang}'].triggered.connect(self.prefs_display_lang)

            self.action_group_prefs_display_lang.addAction(self.__dict__[f'action_prefs_display_lang_{action_lang}'])

        self.menu_prefs.addSeparator()

        self.action_prefs_reset_layouts = self.menu_prefs.addAction(self.tr('&Reset Layouts'))
        self.action_prefs_reset_layouts.setStatusTip(self.tr('Reset layouts'))
        self.action_prefs_reset_layouts.triggered.connect(self.prefs_reset_layouts)

        self.menu_prefs.addSeparator()

        self.action_prefs_show_status_bar = self.menu_prefs.addAction(self.tr('&Show Status Bar'))
        self.action_prefs_show_status_bar.setCheckable(True)
        self.action_prefs_show_status_bar.setStatusTip(self.tr('Show/Hide the status bar'))
        self.action_prefs_show_status_bar.triggered.connect(self.prefs_show_status_bar)

        # Help
        self.action_help_citing = self.menu_help.addAction(self.tr('&Citing'))
        self.action_help_citing.setStatusTip(self.tr('Show information about citing'))
        self.action_help_citing.triggered.connect(self.help_citing)
        self.action_help_acks = self.menu_help.addAction(self.tr('&Acknowledgments'))
        self.action_help_acks.setStatusTip(self.tr('Show acknowldgments'))
        self.action_help_acks.triggered.connect(self.help_acks)

        self.menu_help.addSeparator()

        self.action_help_need_help = self.menu_help.addAction(self.tr('&Need Help?'))
        self.action_help_need_help.setStatusTip(self.tr('Show help information'))
        self.action_help_need_help.triggered.connect(self.help_need_help)
        self.action_help_contributing = self.menu_help.addAction(self.tr('C&ontributing'))
        self.action_help_contributing.setStatusTip(self.tr('Show information about contributing'))
        self.action_help_contributing.triggered.connect(self.help_contributing)
        self.action_help_donating = self.menu_help.addAction(self.tr('&Donating'))
        self.action_help_donating.setStatusTip(self.tr('Show information about donating'))
        self.action_help_donating.triggered.connect(self.help_donating)

        self.menu_help.addSeparator()

        self.action_help_check_updates = self.menu_help.addAction(self.tr('Check &for Updates'))
        self.action_help_check_updates.setStatusTip(self.tr('Check for updates of Wordless'))
        self.action_help_check_updates.triggered.connect(self.help_check_updates)
        self.action_help_changelog = self.menu_help.addAction(self.tr('C&hangelog'))
        self.action_help_changelog.setStatusTip(self.tr('Show Changelog'))
        self.action_help_changelog.triggered.connect(self.help_changelog)
        self.action_help_about = self.menu_help.addAction(self.tr('About &Wordless'))
        self.action_help_about.setStatusTip(self.tr('Show information about Wordless'))
        self.action_help_about.triggered.connect(self.help_about)

    # Preferences - Display Language
    def prefs_display_lang(self):
        for action in self.action_group_prefs_display_lang.actions():
            if action.isChecked():
                if action.lang != self.settings_custom['menu']['prefs']['display_lang']:
                    if wl_dialogs_misc.Wl_Dialog_Restart_Required(self).exec_() == QDialog.Accepted:
                        self.settings_custom['menu']['prefs']['display_lang'] = action.lang

                        self.restart()
                    else:
                        self.__dict__[f"action_prefs_display_lang_{self.settings_custom['menu']['prefs']['display_lang']}"].setChecked(True)

                break

    # Preferences - Reset Layouts
    def prefs_reset_layouts(self):
        if wl_msg_boxes.wl_msg_box_question(
            main = self,
            title = self.tr('Reset Layouts'),
            text = self.tr('''
                <div>Do you want to reset all layouts to their default settings?</div>
            ''')
        ):
            self.centralWidget().setSizes([self.height() - 210, 210])

    # Preferences - Show Status Bar
    def prefs_show_status_bar(self):
        self.settings_custom['menu']['prefs']['show_status_bar'] = self.action_prefs_show_status_bar.isChecked()

        if self.settings_custom['menu']['prefs']['show_status_bar']:
            self.statusBar().show()
        else:
            self.statusBar().hide()

    # Help - Citing
    def help_citing(self):
        Wl_Dialog_Citing(self).open()

    # Help - Acknowledgments
    def help_acks(self):
        Wl_Dialog_Acks(self).open()

    # Help - Need Help?
    def help_need_help(self):
        Wl_Dialog_Need_Help(self).open()

    # Help - Contributing
    def help_contributing(self):
        Wl_Msg_Box_Help(self).open()

    # Help - Donating
    def help_donating(self):
        Wl_Dialog_Donating(self).open()

    # Help - Check for Updates
    def help_check_updates(self, on_startup = False):
        dialog_check_updates = Wl_Dialog_Check_Updates(self, on_startup = on_startup)

        if not on_startup:
            dialog_check_updates.open()

    # Help - Changelog
    def help_changelog(self):
        Wl_Dialog_Changelog(self).open()

    # Help - About Wordless
    def help_about(self):
        Wl_Dialog_About(self).open()

    def init_central_widget(self):
        self.wl_file_area = wl_file_area.Wrapper_File_Area(self)
        self.init_work_area()

        # Align work area and file area
        wrapper_file_area = QWidget()

        wrapper_file_area.setLayout(wl_layouts.Wl_Layout())
        wrapper_file_area.layout().addWidget(self.wl_file_area, 0, 0)

        margins = self.wl_file_area.layout().contentsMargins()

        if platform.system() == 'Windows':
            wrapper_file_area.layout().setContentsMargins(0, 0, 2, 0)

            margins.setLeft(margins.left() + 2)
            margins.setRight(margins.right() + 2)
        elif platform.system() == 'Darwin':
            wrapper_file_area.layout().setContentsMargins(2, 0, 2, 0)
            margins.setLeft(margins.left() + 1)
            margins.setRight(margins.right() + 1)
        elif platform.system() == 'Linux':
            wrapper_file_area.layout().setContentsMargins(0, 0, 0, 0)

            margins.setRight(margins.right() + 2)

        self.wl_file_area.layout().setContentsMargins(margins)

        splitter_central_widget = wl_layouts.Wl_Splitter(Qt.Vertical, self)
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
        self.wl_work_area = QTabWidget(self)

        self.wl_work_area.addTab(
            wl_profiler.Wrapper_Profiler(self),
            self.tr('Profiler')
        )
        self.wl_work_area.addTab(
            wl_concordancer.Wrapper_Concordancer(self),
            self.tr('Concordancer')
        )
        self.wl_work_area.addTab(
            wl_concordancer_parallel.Wrapper_Concordancer_Parallel(self),
            self.tr('Parallel Concordancer')
        )
        self.wl_work_area.addTab(
            wl_wordlist_generator.Wrapper_Wordlist_Generator(self),
            self.tr('Wordlist Generator')
        )
        self.wl_work_area.addTab(
            wl_ngram_generator.Wrapper_Ngram_Generator(self),
            self.tr('N-gram Generator')
        )
        self.wl_work_area.addTab(
            wl_collocation_extractor.Wrapper_Collocation_Extractor(self),
            self.tr('Collocation Extractor')
        )
        self.wl_work_area.addTab(
            wl_colligation_extractor.Wrapper_Colligation_Extractor(self),
            self.tr('Colligation Extractor')
        )
        self.wl_work_area.addTab(
            wl_keyword_extractor.Wrapper_Keyword_Extractor(self),
            self.tr('Keyword Extractor')
        )

        self.wl_work_area.currentChanged.connect(self.work_area_changed)

        self.load_settings_work_area()

    def load_settings_work_area(self):
        # Current tab
        work_area_cur = self.settings_custom['work_area_cur']

        for i in range(self.wl_work_area.count()):
            if self.wl_work_area.tabText(i) == work_area_cur:
                self.wl_work_area.setCurrentIndex(i)

                break

        self.work_area_changed()

    def work_area_changed(self):
        # Current tab
        self.settings_custom['work_area_cur'] = self.wl_work_area.tabText(self.wl_work_area.currentIndex())

    def load_settings(self):
        settings = self.settings_custom

        # Fonts
        self.setStyleSheet(f'''
            font-family: {settings['general']['font_settings']['font_family']};
            font-size: {settings['general']['font_settings']['font_size']}px;
        ''')

        # Menu - Preferences
        self.__dict__[f"action_prefs_display_lang_{settings['menu']['prefs']['display_lang']}"].setChecked(True)
        self.action_prefs_show_status_bar.setChecked(settings['menu']['prefs']['show_status_bar'])

        self.prefs_display_lang()

        # Layouts
        self.centralWidget().setSizes(settings['layouts']['central_widget'])

    def save_settings(self):
        # Clear history of closed files
        self.settings_custom['file_area']['files_closed'].clear()

        # Layouts
        self.settings_custom['layouts']['central_widget'] = self.centralWidget().sizes()

        with open('wl_settings.pickle', 'wb') as f:
            pickle.dump(self.settings_custom, f)

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
                subprocess.Popen(['python3.8', wl_misc.get_normalized_path(__file__)])

        self.save_settings()
        sys.exit(0)

class Wl_Dialog_Citing(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = main.tr('Citing'),
            width = 450,
            no_buttons = True
        )

        self.label_citing = wl_labels.Wl_Label_Dialog(
            self.tr('''
                <div>
                    If you publish work that uses Wordless, please cite as follows.
                </div>
            '''),
            self
        )

        self.label_citation_sys = QLabel(self.tr('Citation System:'), self)
        self.combo_box_citation_sys = wl_boxes.Wl_Combo_Box(self)
        self.text_edit_citing = QTextEdit(self)

        self.button_copy = QPushButton(self.tr('Copy'), self)
        self.button_close = QPushButton(self.tr('Close'), self)

        self.combo_box_citation_sys.addItems([
            self.tr('APA (7th Edition)'),
            self.tr('MLA (8th Edition)')
        ])

        self.button_copy.setFixedWidth(100)
        self.button_close.setFixedWidth(100)

        self.text_edit_citing.setFixedHeight(100)
        self.text_edit_citing.setReadOnly(True)

        self.combo_box_citation_sys.currentTextChanged.connect(self.citation_sys_changed)

        self.button_copy.clicked.connect(self.copy)
        self.button_close.clicked.connect(self.accept)

        layout_citation_sys = wl_layouts.Wl_Layout()
        layout_citation_sys.addWidget(self.label_citation_sys, 0, 0)
        layout_citation_sys.addWidget(self.combo_box_citation_sys, 0, 1)

        layout_citation_sys.setColumnStretch(2, 1)

        self.wrapper_info.layout().addWidget(self.label_citing, 0, 0, 1, 2)
        self.wrapper_info.layout().addLayout(layout_citation_sys, 1, 0, 1, 2)
        self.wrapper_info.layout().addWidget(self.text_edit_citing, 2, 0, 1, 2)

        self.wrapper_buttons.layout().addWidget(self.button_copy, 0, 0)
        self.wrapper_buttons.layout().addWidget(self.button_close, 0, 1)

        self.load_settings()

        self.set_fixed_height()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['menu']['help']['citing'])

        self.combo_box_citation_sys.setCurrentText(settings['citation_sys'])

        self.citation_sys_changed()

    def citation_sys_changed(self):
        settings = self.main.settings_custom['menu']['help']['citing']

        settings['citation_sys'] = self.combo_box_citation_sys.currentText()

        if settings['citation_sys'] == self.tr('APA (7th Edition)'):
            self.text_edit_citing.setHtml(f'Ye, L. (2021). <i>Wordless</i> (Version {self.main.ver}) [Computer software]. Github. https://github.com/BLKSerene/Wordless')
        elif settings['citation_sys'] == self.tr('MLA (8th Edition)'):
            self.text_edit_citing.setHtml(f'Ye Lei. <i>Wordless</i>, version {self.main.ver}, 2021. <i>Github</i>, https://github.com/BLKSerene/Wordless.')

    def copy(self):
        self.text_edit_citing.setFocus()
        self.text_edit_citing.selectAll()
        self.text_edit_citing.copy()

class Wl_Dialog_Acks(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = main.tr('Acknowledgments'),
            width = 700
        )

        # Load acknowledgments
        acks = []

        with open(r'wl_acks.csv', 'r', encoding = 'utf_8', newline = '') as f:
            reader = csv.reader(f)

            for row in reader:
                name = row[0]
                home_page = row[1]
                ver = row[2]
                authors = row[3]
                license = row[4]
                license_url = row[5]

                acks.append([name, home_page, ver, authors, license, license_url])

        self.label_acks = wl_labels.Wl_Label_Dialog(
            self.tr('''
                <div>
                    I would like to extend my sincere gratitude to the following open-source projects without which this project would not have been possible:
                </div>
            '''),
            self
        )
        self.table_acks = wl_tables.Wl_Table(
            self,
            headers = [
                self.tr('Name'),
                self.tr('Version'),
                self.tr('Authors'),
                self.tr('License')
            ]
        )

        self.table_acks.setFixedHeight(400)
        self.table_acks.model().setRowCount(len(acks))

        self.table_acks.disable_updates()

        for i, (name, home_page, ver, authors, license, licence_url) in enumerate(acks):
            name = f'<a href="{home_page}">{name}</a>'
            license = f'<a href="{licence_url}">{license}</a>'

            self.table_acks.setIndexWidget(self.table_acks.model().index(i, 0), wl_labels.Wl_Label_Html(name, self))
            self.table_acks.setIndexWidget(self.table_acks.model().index(i, 1), wl_labels.Wl_Label_Html_Centered(ver, self))
            self.table_acks.setIndexWidget(self.table_acks.model().index(i, 2), wl_labels.Wl_Label_Html(authors, self))
            self.table_acks.setIndexWidget(self.table_acks.model().index(i, 3), wl_labels.Wl_Label_Html_Centered(license, self))

        self.table_acks.enable_updates()

        self.wrapper_info.layout().addWidget(self.label_acks, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_acks, 1, 0)

        self.set_fixed_height()

class Wl_Dialog_Need_Help(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = main.tr('Need Help?'),
            width = 600,
            height = 500
        )

        self.label_need_help = wl_labels.Wl_Label_Dialog(
            self.tr('''
                <div>
                    If you encounter a problem, find a bug, or require any further information, feel free to ask questions, submit bug reports, or provide feedback by <a href="https://github.com/BLKSerene/Wordless/issues/new">creating an issue</a> on Github if you fail to find the answer by searching <a href="https://github.com/BLKSerene/Wordless/issues">existing issues</a> first.
                </div>

                <div>
                    If you need to post sample texts or other information that cannot be shared or you do not want to share publicly, you may send me an email.
                </div>
            '''),
            self
        )

        self.table_need_help = wl_tables.Wl_Table(
            self,
            headers = [
                self.tr('Channel'),
                self.tr('Contact Information')
            ]
        )

        self.table_need_help.setFixedHeight(350)
        self.table_need_help.verticalHeader().setHidden(True)
        self.table_need_help.model().setRowCount(3)

        self.table_need_help.disable_updates()

        self.table_need_help.setIndexWidget(self.table_need_help.model().index(0, 0), wl_labels.Wl_Label_Html_Centered(self.tr('Documentation'), self))
        self.table_need_help.setIndexWidget(self.table_need_help.model().index(0, 1), wl_labels.Wl_Label_Html('<a href="https://github.com/BLKSerene/Wordless#documentation">https://github.com/BLKSerene/Wordless#documentation</a>', self))
        self.table_need_help.setIndexWidget(self.table_need_help.model().index(1, 0), wl_labels.Wl_Label_Html_Centered(self.tr('Email'), self))
        self.table_need_help.setIndexWidget(self.table_need_help.model().index(1, 1), wl_labels.Wl_Label_Html(self.main.email_html, self))
        self.table_need_help.setIndexWidget(self.table_need_help.model().index(2, 0), wl_labels.Wl_Label_Html_Centered(self.tr('<a href="https://www.wechat.com/en/">WeChat</a><br>Official Account'), self))
        self.table_need_help.setIndexWidget(self.table_need_help.model().index(2, 1), wl_labels.Wl_Label_Html_Centered('<img src="imgs/wechat_official_account.jpg">', self))

        self.table_need_help.enable_updates()

        self.wrapper_info.layout().addWidget(self.label_need_help, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_need_help, 1, 0)

class Wl_Msg_Box_Help(wl_msg_boxes.Wl_Msg_Box):
    def __init__(self, main):
        super().__init__(
            main,
            icon = QMessageBox.Information,
            title = main.tr('Contributing'),
            text = main.tr('''
                <div>
                    If you have an interest in helping the development of Wordless, you may contribute bug fixes, enhancements, or new features by <a href="https://github.com/BLKSerene/Wordless/pulls">creating a pull request</a> on Github.
                </div>
                <div>
                    Besides, you may contribute by submitting enhancement proposals or feature requests, write tutorials or <a href ="https://github.com/BLKSerene/Wordless/wiki">Github Wiki</a> for Wordless, or helping me translate Wordless and its documentation to other languages.
                </div>
            ''')
        )

        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)

class Wl_Dialog_Donating(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = main.tr('Donating'),
            width = 450
        )

        self.label_donating = wl_labels.Wl_Label_Dialog(
            self.tr('''
                <div>
                    If you would like to support the development of Wordless, you may donate via <a href="https://www.paypal.com/">PayPal</a>, <a href="https://global.alipay.com/">Alipay</a>, or <a href="https://pay.weixin.qq.com/index.php/public/wechatpay_en">WeChat Pay</a>.
                </div>
            '''),
            self
        )
        self.label_donating_via = QLabel(self.tr('Donating via:'), self)
        self.combo_box_donating_via = wl_boxes.Wl_Combo_Box(self)
        self.label_donating_via_img = wl_labels.Wl_Label_Html('', self)

        self.combo_box_donating_via.addItems([
            self.tr('PayPal'),
            self.tr('Alipay'),
            self.tr('WeChat Pay')
        ])

        self.combo_box_donating_via.currentTextChanged.connect(self.donating_via_changed)

        layout_donating_via = wl_layouts.Wl_Layout()
        layout_donating_via.addWidget(self.label_donating_via, 0, 0)
        layout_donating_via.addWidget(self.combo_box_donating_via, 0, 1)

        layout_donating_via.setColumnStretch(2, 1)

        self.wrapper_info.layout().addWidget(self.label_donating, 0, 0)
        self.wrapper_info.layout().addLayout(layout_donating_via, 1, 0)
        self.wrapper_info.layout().addWidget(self.label_donating_via_img, 2, 0, Qt.AlignHCenter | Qt.AlignVCenter)

        # Calculate height
        donating_via_old = self.main.settings_custom['menu']['help']['donating']['donating_via']

        self.combo_box_donating_via.setCurrentText('PayPal')
        self.donating_via_changed()

        height_donating_via_paypal = self.label_donating_via_img.sizeHint().height()
        self.height_paypal = self.heightForWidth(self.width())

        self.combo_box_donating_via.setCurrentText('Alipay')
        self.donating_via_changed()

        height_donating_via_alipay = self.label_donating_via_img.sizeHint().height()
        self.height_alipay = self.heightForWidth(self.width()) + (height_donating_via_alipay - height_donating_via_paypal)

        self.main.settings_custom['menu']['help']['donating']['donating_via'] = donating_via_old

        self.load_settings()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['menu']['help']['donating'])

        self.combo_box_donating_via.setCurrentText(settings['donating_via'])

        self.donating_via_changed()

    def donating_via_changed(self):
        settings = self.main.settings_custom['menu']['help']['donating']

        settings['donating_via'] = self.combo_box_donating_via.currentText()

        if settings['donating_via'] == self.tr('PayPal'):
            self.label_donating_via_img.setText('<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=V2V54NYE2YD32"><img src="imgs/donating_paypal.gif"></a>')
        elif settings['donating_via'] == self.tr('Alipay'):
            self.label_donating_via_img.setText('<img src="imgs/donating_alipay.png">')
        elif settings['donating_via'] == self.tr('WeChat Pay'):
            self.label_donating_via_img.setText('<img src="imgs/donating_wechat_pay.png">')

        if 'height_alipay' in self.__dict__:
            if settings['donating_via'] == self.tr('PayPal'):
                self.setFixedHeight(self.height_paypal)
            elif settings['donating_via'] in [self.tr('Alipay'), self.tr('WeChat Pay')]:
                self.setFixedHeight(self.height_alipay)

        if platform.system() in ['Windows', 'Linux']:
            self.move_to_center()

class Worker_Check_Updates(QObject):
    worker_done = pyqtSignal(str, str)

    def __init__(self, main):
        super().__init__()

        self.main = main
        self.stopped = False

    def run(self):
        ver_new = ''
        proxy_settings = self.main.settings_custom['general']['proxy_settings']

        try:
            timeout = 5

            if proxy_settings['use_proxy']:
                r = requests.get(
                    'https://raw.githubusercontent.com/BLKSerene/Wordless/main/src/VERSION',
                    timeout = timeout,
                    proxies = {
                        'http': f"http://{proxy_settings['address']}:{proxy_settings['port']}",
                        'https': f"http://{proxy_settings['address']}:{proxy_settings['port']}"
                    },
                    auth = (proxy_settings['username'], proxy_settings['password'])
                )
            else:
                r = requests.get(
                    'https://raw.githubusercontent.com/BLKSerene/Wordless/main/src/VERSION',
                    timeout = timeout
                )

            if r.status_code == 200:
                for line in r.text.splitlines():
                    if line and not line.startswith('#'):
                        ver_new = line.rstrip()

                if self.is_newer_version(ver_new):
                    updates_status = 'updates_available'
                else:
                    updates_status = 'no_updates'
            else:
                updates_status = 'network_err'
        except Exception:
            print(traceback.format_exc())

            updates_status = 'network_err'

        if self.stopped:
            updates_status == ''

        self.worker_done.emit(updates_status, ver_new)

    def is_newer_version(self, ver_new):
        ver_major_new, ver_minor_new, ver_patch_new = wl_misc.split_wl_ver(ver_new)

        if self.main.ver == '?.?.?':
            return True
        elif (
            self.main.ver_major < ver_major_new
            or self.main.ver_minor < ver_minor_new
            or self.main.ver_patch < ver_patch_new
        ):
            return True
        else:
            return False

    def stop(self):
        self.stopped = True

class Wl_Dialog_Check_Updates(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main, on_startup = False):
        super().__init__(
            main,
            title = main.tr('Check for Updates'),
            width = 500,
            no_buttons = True
        )

        self.on_startup = on_startup

        self.label_checking_status = wl_labels.Wl_Label_Dialog('', self)
        self.label_cur_ver = wl_labels.Wl_Label_Dialog(self.tr(f'Current Version: {self.main.ver}'), self)
        self.label_latest_ver = wl_labels.Wl_Label_Dialog('', self)

        self.checkbox_check_updates_on_startup = QCheckBox(self.tr('Check for updates on startup'), self)
        self.button_try_again = QPushButton(self.tr('Try Again'), self)
        self.button_cancel = QPushButton(self.tr('Cancel'), self)

        self.checkbox_check_updates_on_startup.stateChanged.connect(self.check_updates_on_startup_changed)
        self.button_try_again.clicked.connect(self.check_updates)

        self.wrapper_info.layout().addWidget(self.label_checking_status, 0, 0, 2, 1)
        self.wrapper_info.layout().addWidget(self.label_cur_ver, 2, 0)
        self.wrapper_info.layout().addWidget(self.label_latest_ver, 3, 0)

        self.wrapper_buttons.layout().addWidget(self.checkbox_check_updates_on_startup, 0, 0)
        self.wrapper_buttons.layout().addWidget(self.button_try_again, 0, 2)
        self.wrapper_buttons.layout().addWidget(self.button_cancel, 0, 3)

        self.wrapper_buttons.layout().setColumnStretch(1, 1)

        self.load_settings()

        self.set_fixed_height()

    def check_updates(self):
        self.checking_status_changed('checking')

        self.main.worker_check_updates = Worker_Check_Updates(self.main)
        thread_check_updates = wl_threading.Wl_Thread(self.main.worker_check_updates)

        self.main.threads_check_updates.append(thread_check_updates)

        thread_check_updates.destroyed.connect(lambda: self.main.threads_check_updates.remove(thread_check_updates))

        self.main.worker_check_updates.worker_done.connect(self.checking_status_changed)
        self.main.worker_check_updates.worker_done.connect(thread_check_updates.quit)
        self.main.worker_check_updates.worker_done.connect(self.main.worker_check_updates.deleteLater)

        thread_check_updates.start()

    def stop_checking(self):
        self.main.worker_check_updates.stop()

        self.reject()

    def checking_status_changed(self, status, ver_new = ''):
        # Try Again
        if status == 'network_err':
            self.button_try_again.show()
        else:
            self.button_try_again.hide()

        if status == 'checking':
            self.label_checking_status.set_text(self.tr('''
                <div>
                    Checking for updates...
                </div>
            '''))
            self.label_latest_ver.set_text(self.tr('Latest Version: Checking...'))

            self.button_cancel.setText(self.tr('Cancel'))
            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.stop_checking)
        else:
            if status in ['updates_available', 'no_updates']:
                if status == 'updates_available':
                    self.label_checking_status.set_text(self.tr(f'''
                        <div>
                            Wordless {ver_new} is out, click <a href="https://github.com/BLKSerene/Wordless#download"><b>HERE</b></a> to download the latest version of Wordless.
                        </div>
                    '''))
                    self.label_latest_ver.set_text(self.tr(f'Latest Version: {ver_new}'))
                elif status == 'no_updates':
                    self.label_checking_status.set_text(self.tr('''
                        <div>
                            Hooray, you are using the latest version of Wordless!
                        </div>
                    '''))
                    self.label_latest_ver.set_text(self.tr(f'Latest Version: {self.main.ver}'))
            elif status == 'network_err':
                self.label_checking_status.set_text(self.tr('''
                    <div>
                        A network error has occurred, please check your network settings and try again or <a href="https://github.com/BLKSerene/Wordless/releases">check for updates manually</a>.
                    </div>
                '''))
                self.label_latest_ver.set_text(self.tr('Latest Version: Network error'))

            self.button_cancel.setText(self.tr('OK'))
            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)

        # On startup
        if self.on_startup:
            if status == 'updates_available':
                self.open()
                self.setFocus()
            else:
                self.accept()

    def load_settings(self):
        settings = self.main.settings_custom['general']['update_settings']

        self.checkbox_check_updates_on_startup.setChecked(settings['check_updates_on_startup'])

        self.check_updates()

    def check_updates_on_startup_changed(self):
        settings = self.main.settings_custom['general']['update_settings']

        settings['check_updates_on_startup'] = self.checkbox_check_updates_on_startup.isChecked()

class Wl_Dialog_Changelog(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = main.tr('Changelog'),
            width = 600,
            height = 600
        )

        changelog = []

        try:
            with open('CHANGELOG.md', 'r', encoding = 'utf_8') as f:
                for line in f:
                    # Changelog headers
                    if line.startswith('## '):
                        release_ver = re.search(r'(?<=\[)[^\]]+?(?=\])', line).group()
                        release_link = re.search(r'(?<=\()[^\)]+?(?=\))', line).group()
                        release_date = re.search(r'(?<=\- )[0-9?]{2}/[0-9?]{2}/[0-9?]{4}', line).group()

                        changelog.append({
                            'release_ver': release_ver,
                            'release_link': release_link,
                            'release_date': release_date,
                            'changelog_sections': []
                        })

                    # Changelog section headers
                    elif line.startswith('### '):
                        changelog[-1]['changelog_sections'].append({
                            'section_header': line.replace('###', '').strip(),
                            'section_list': []
                        })
                    # Changelog section lists
                    elif line.startswith('- '):
                        line = re.sub(r'^- ', r'', line).strip()

                        changelog[-1]['changelog_sections'][-1]['section_list'].append(line)

            font_size_custom = main.settings_custom['general']['font_settings']['font_size']

            changelog_text = f'''
                <head>
                    <style>
                        * {{
                            outline: none;
                            margin: 0;
                            border: 0;
                            padding: 0;

                            text-align: justify;
                        }}

                        ul {{
                            line-height: 1.2;
                            margin-bottom: 10px;
                        }}

                        li {{
                            margin-left: -30px;
                        }}

                        .changelog {{
                            margin-bottom: 5px;
                        }}

                        .changelog-header {{
                            margin-bottom: 3px;
                            font-size: {font_size_custom + 2}px;
                            font-weight: bold;
                        }}

                        .changelog-section-header {{
                            margin-bottom: 5px;
                            font-size: {font_size_custom + 1}px;
                            font-weight: bold;
                        }}
                    </style>
                </head>
                <body>
            '''

            for release in changelog:
                changelog_text += f'''
                    <div class="changelog">
                        <div class="changelog-header"><a href="{release['release_link']}">{release['release_ver']}</a> - {release['release_date']}</div>
                        <hr>
                '''

                for changelog_section in release['changelog_sections']:
                    changelog_text += f'''
                        <div class="changelog-section">
                            <div class="changelog-section-header">{changelog_section['section_header']}</div>
                            <ul>
                    '''

                    for item in changelog_section['section_list']:
                        changelog_text += f'''
                            <li>{item}</li>
                        '''

                    changelog_text += '''
                            </ul>
                        </div>
                    '''

                changelog_text += '''
                    </div>
                '''

            changelog_text += '''
                </body>
            '''
        except (FileNotFoundError, PermissionError):
            changelog_text = traceback.format_exc()

        text_edit_changelog = wl_boxes.Wl_Text_Browser(self)
        text_edit_changelog.setHtml(changelog_text)

        self.wrapper_info.layout().addWidget(text_edit_changelog, 0, 0)

class Wl_Dialog_About(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, title = main.tr('About Wordless'))

        img_wl_icon = QPixmap('imgs/wl_icon_about.png')
        img_wl_icon = img_wl_icon.scaled(64, 64)

        label_about_icon = QLabel('', self)
        label_about_icon.setPixmap(img_wl_icon)

        label_about_title = wl_labels.Wl_Label_Dialog_No_Wrap(
            self.tr(f'''
                <div style="text-align: center;">
                    <h2>Wordless {main.ver}</h2>
                    <div>
                        An Integrated Corpus Tool with Multilingual Support<br>
                        for the Study of Language, Literature, and Translation
                    </div>
                </div>
            '''),
            self
        )
        label_about_copyright = wl_labels.Wl_Label_Dialog_No_Wrap(
            self.tr('''
                <hr>
                <div style="text-align: center;">
                    Copyright (C) 2018-2022&nbsp;&nbsp;Ye Lei (<span style="font-family: simsun">叶磊</span>)<br>
                    Licensed Under GNU GPLv3<br>
                    All Other Rights Reserved
                </div>
            '''),
            self
        )

        self.wrapper_info.layout().addWidget(label_about_icon, 0, 0)
        self.wrapper_info.layout().addWidget(label_about_title, 0, 1)
        self.wrapper_info.layout().addWidget(label_about_copyright, 1, 0, 1, 2)

        self.wrapper_info.layout().setColumnStretch(1, 1)
        self.wrapper_info.layout().setVerticalSpacing(0)

        self.set_fixed_size()
        self.setFixedWidth(self.width() + 10)

if __name__ == '__main__':
    wl_app = QApplication(sys.argv)

    # Translations
    if os.path.exists('wl_settings.pickle'):
        with open('wl_settings.pickle', 'rb') as f:
            settings_custom = pickle.load(f)
            display_lang = settings_custom['menu']['prefs']['display_lang']
    else:
        display_lang = 'eng_us'

    if display_lang != 'eng_us':
        translator = QTranslator()
        translator.load(f'translations/{display_lang}.qm')

        wl_app.installTranslator(translator)

    wl_loading = Wl_Loading()

    wl_loading.raise_()
    wl_loading.fade_in()

    wl_app.processEvents()

    wl_main = Wl_Main(wl_loading)

    wl_loading.fade_out()
    wl_loading.finish(wl_main)

    # Check for updates on startup
    if wl_main.settings_custom['general']['update_settings']['check_updates_on_startup']:
        wl_main.dialog_check_updates = wl_main.help_check_updates(on_startup = True)

    # Show changelog on first startup
    # * Do not do this on macOS since the popped-up changelog window cannot be closed sometimes
    if platform.system() in ['Windows', 'Linux']:
        if wl_main.settings_custom['1st_startup']:
            wl_main.help_changelog()

            wl_main.settings_custom['1st_startup'] = False

    wl_main.showMaximized()

    sys.exit(wl_app.exec_())
