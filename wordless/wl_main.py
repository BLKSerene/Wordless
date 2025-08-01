# ----------------------------------------------------------------------
# Wordless: Main window
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

import multiprocessing

# Prevent Wordless from relaunching itself on macOS
multiprocessing.freeze_support()

# pylint: disable=wrong-import-position
import copy
import glob
import os
import pickle
import platform
import re
import subprocess
import sys
import time

# Fix working directory on macOS
if getattr(sys, '_MEIPASS', False) and platform.system() == 'Darwin':
    os.chdir(sys._MEIPASS) # pylint: disable=no-member

# Fake sys.stdout and sys.stderr when frozen
# See: https://github.com/pyinstaller/pyinstaller/issues/7334#issuecomment-1357447176
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w') # pylint: disable=unspecified-encoding, consider-using-with
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w') # pylint: disable=unspecified-encoding, consider-using-with

import botok
import matplotlib
import nltk
import packaging.version
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import pythainlp
import spacy_pkuseg
import underthesea.file_utils

# Use Qt backend for Matplotlib
matplotlib.use('Qt5Agg')

from wordless import (
    wl_file_area,
    wl_profiler,
    wl_concordancer,
    wl_concordancer_parallel,
    wl_dependency_parser,
    wl_wordlist_generator,
    wl_ngram_generator,
    wl_collocation_extractor,
    wl_colligation_extractor,
    wl_keyword_extractor
)
from wordless.wl_checks import wl_checks_misc
from wordless.wl_dialogs import (
    wl_dialogs,
    wl_dialogs_misc
)
from wordless.wl_settings import (
    wl_settings,
    wl_settings_default,
    wl_settings_global
)
from wordless.wl_utils import (
    wl_misc,
    wl_paths,
    wl_threading
)
from wordless.wl_widgets import (
    wl_boxes,
    wl_editors,
    wl_labels,
    wl_layouts,
    wl_tables
)

# Modify paths of data files when frozen
if getattr(sys, '_MEIPASS', False):
    # botok
    botok.config.DEFAULT_BASE_PATH = wl_paths.get_path_file('pybo', 'dialect_packs')
    # NLTK
    nltk.data.path = [wl_paths.get_path_file('nltk_data')]
    # PyThaiNLP
    PYTHAINLP_DEFAULT_DATA_DIR = os.path.realpath(pythainlp.tools.PYTHAINLP_DEFAULT_DATA_DIR)
    pythainlp.corpus._CORPUS_DB_PATH = wl_paths.get_path_file(pythainlp.tools.PYTHAINLP_DEFAULT_DATA_DIR, pythainlp.corpus._CORPUS_DB_FILENAME)
    pythainlp.tools.path.get_pythainlp_data_path = lambda: PYTHAINLP_DEFAULT_DATA_DIR
    # spacy-pkuseg
    spacy_pkuseg.config.pkuseg_home = wl_paths.get_path_file('.pkuseg')
    # Underthesea
    underthesea.file_utils.UNDERTHESEA_FOLDER = wl_paths.get_path_file('.underthesea')

_tr = QtCore.QCoreApplication.translate
is_windows, is_macos, is_linux = wl_misc.check_os()

class Wl_Loading(QtWidgets.QSplashScreen):
    def __init__(self):
        super().__init__(QtGui.QPixmap(wl_paths.get_path_img('wl_loading.png')))

        self.setFont(
            QtGui.QFont(global_font_family,
            pointSize = global_font_size - 1)
        )
        self.show_message(self.tr('Initializing Wordless...'))

    def show_message(self, message):
        self.showMessage(
            f' {message}',
            color = QtCore.Qt.white,
            alignment = QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom
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

class Wl_Dialog_Confirm_Exit(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = _tr('Wl_Dialog_Confirm_Exit', 'Exit Wordless'),
            width = 450,
            icon = 'question',
            no_buttons = True
        )

        self.label_confirm_exit = wl_labels.Wl_Label_Dialog(
            self.tr('''
                <div>Do you want to exit <i>Wordless</i>?</div>
                <br>
                <div><b>Note:</b> All unsaved data and figures will be lost.</div>
            '''),
            self
        )

        self.checkbox_always_confirm_on_exit = QtWidgets.QCheckBox(self.tr('Always confirm on exit'), self)
        self.button_exit = QtWidgets.QPushButton(self.tr('Exit'), self)
        self.button_cancel = QtWidgets.QPushButton(self.tr('Cancel'), self)

        self.checkbox_always_confirm_on_exit.stateChanged.connect(self.always_confirm_on_exit_changed)
        self.button_exit.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)

        self.layout_info.addWidget(self.label_confirm_exit, 0, 0)

        self.layout_buttons.addWidget(self.checkbox_always_confirm_on_exit, 0, 0)
        self.layout_buttons.addWidget(self.button_exit, 0, 2)
        self.layout_buttons.addWidget(self.button_cancel, 0, 3)

        self.layout_buttons.setColumnStretch(1, 1)

        self.load_settings()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['general']['misc_settings'])

        self.checkbox_always_confirm_on_exit.setChecked(settings['always_confirm_on_exit'])

    def always_confirm_on_exit_changed(self):
        settings = self.main.settings_custom['general']['misc_settings']

        settings['always_confirm_on_exit'] = self.checkbox_always_confirm_on_exit.isChecked()

class Wl_Main(QtWidgets.QMainWindow):
    def __init__(self, loading_window):
        super().__init__()

        self.loading_window = loading_window
        self.threads_check_updates = []
        # Version number
        self.ver = wl_misc.get_wl_ver()
        self.copyright_year = '2025'
        # Email
        self.email = 'blkserene@gmail.com'
        self.email_html = '<a href="mailto:blkserene@gmail.com">blkserene@gmail.com</a>'

        # Icon
        self.setWindowIcon(QtGui.QIcon(wl_paths.get_path_img('wl_icon.ico')))
        # Title
        self.setWindowTitle(f'Wordless {self.ver}')

        self.loading_window.show_message(self.tr('Loading settings...'))

        # Global and default settings
        self.settings_global = wl_settings_global.init_settings_global()
        self.settings_default = wl_settings_default.init_settings_default(self)

        # Custom settings
        if os.path.exists(file_settings):
            with open(file_settings, 'rb') as f:
                try:
                    settings_custom = pickle.load(f)

                    if wl_checks_misc.check_custom_settings(settings_custom, self.settings_default):
                        self.settings_custom = settings_custom
                    else:
                        self.settings_custom = copy.deepcopy(self.settings_default)
                # Use default settings if the pickle file is empty
                except EOFError:
                    self.settings_custom = copy.deepcopy(self.settings_default)

                    os.remove(file_settings)
        else:
            self.settings_custom = copy.deepcopy(self.settings_default)

        if os.path.exists(file_settings_display_lang):
            with open(file_settings_display_lang, 'rb') as f:
                self.settings_custom['menu']['prefs']['display_lang'] = pickle.load(f)

        self.loading_window.show_message(self.tr('Initializing main window...'))

        # Font
        self.setStyleSheet(f'''
            font-family: {self.settings_custom['general']['ui_settings']['font_family']};
            font-size: {self.settings_custom['general']['ui_settings']['font_size']}pt;
        ''')

        # Menu - Preferences - Settings
        self.wl_settings = wl_settings.Wl_Settings(self)
        # Menu
        self.init_menu()

        # Work Area & File Area
        self.init_central_widget()

        # Status bar
        self.statusBar().showMessage(self.tr('Ready!'))

        self.statusBar().setFixedHeight(30)
        self.statusBar().setStyleSheet('''
            QStatusBar {
                background-color: #D0D0D0;
            }
        ''')

        self.loading_window.show_message(self.tr('Starting Wordless...'))

        self.load_settings()

    def closeEvent(self, event):
        if self.settings_custom['general']['misc_settings']['always_confirm_on_exit']:
            if Wl_Dialog_Confirm_Exit(self).exec():
                self.save_settings()

                event.accept()
            else:
                event.ignore()
        else:
            self.save_settings()

            event.accept()

    def init_menu(self):
        self.menu_file = self.menuBar().addMenu(self.tr('&File'))
        self.menu_edit = self.menuBar().addMenu(self.tr('&Edit'))
        self.menu_prefs = self.menuBar().addMenu(self.tr('&Preferences'))
        self.menu_help = self.menuBar().addMenu(self.tr('&Help'))

        # File
        self.action_file_open_corpora = self.menu_file.addAction(self.tr('&Open Corpora...'))
        self.action_file_open_corpora.setShortcut(QtGui.QKeySequence('Ctrl+O'))
        self.action_file_open_corpora.setStatusTip(self.tr('Add corpora to the File Area'))
        self.action_file_reopen = self.menu_file.addAction(self.tr('&Reopen'))
        self.action_file_reopen.setStatusTip(self.tr('Add corpora which have just been closed back to the File Area'))

        self.menu_file.addSeparator()

        self.action_file_select_all = self.menu_file.addAction(self.tr('S&elect All'))
        self.action_file_select_all.setShortcut(QtGui.QKeySequence('Ctrl+A'))
        self.action_file_select_all.setStatusTip(self.tr('Select all corpora in the File Area'))
        self.action_file_deselect_all = self.menu_file.addAction(self.tr('&Deselect All'))
        self.action_file_deselect_all.setShortcut(QtGui.QKeySequence('Ctrl+D'))
        self.action_file_deselect_all.setStatusTip(self.tr('Deselect all corpora in the File Area'))
        self.action_file_invert_selection = self.menu_file.addAction(self.tr('&Invert Selection'))
        self.action_file_invert_selection.setShortcut(QtGui.QKeySequence('Ctrl+Shift+I'))
        self.action_file_invert_selection.setStatusTip(self.tr('Invert corpora selection in the File Area'))

        self.menu_file.addSeparator()

        self.action_file_close_selected = self.menu_file.addAction(self.tr('&Close Selected'))
        self.action_file_close_selected.setShortcut(QtGui.QKeySequence('Ctrl+W'))
        self.action_file_close_selected.setStatusTip(self.tr('Remove selected corpora from the File Area'))
        self.action_file_close_all = self.menu_file.addAction(self.tr('C&lose All'))
        self.action_file_close_all.setShortcut(QtGui.QKeySequence('Ctrl+Shift+W'))
        self.action_file_close_all.setStatusTip(self.tr('Remove all corpora from the File Area'))

        self.menu_file.addSeparator()

        self.action_file_exit = self.menu_file.addAction(self.tr('&Exit...'))
        self.action_file_exit.setShortcut(QtGui.QKeySequence('Ctrl+Q'))
        self.action_file_exit.setStatusTip(self.tr('Exit Wordless'))
        self.action_file_exit.triggered.connect(self.close)

        # Edit
        self.action_edit_results_search = self.menu_edit.addAction(self.tr('&Search in Results...'))
        self.action_edit_results_search.setShortcut(QtGui.QKeySequence('Ctrl+F'))
        self.action_edit_results_search.setStatusTip(self.tr('Search in results displayed in the table'))
        self.action_edit_results_search.triggered.connect(self.edit_results_search)
        self.action_edit_results_filter = self.menu_edit.addAction(self.tr('&Filter Results...'))
        self.action_edit_results_filter.setShortcut(QtGui.QKeySequence('Ctrl+Shift+L'))
        self.action_edit_results_filter.setStatusTip(self.tr('Filter results displayed in the table'))
        self.action_edit_results_filter.triggered.connect(self.edit_results_filter)
        self.action_edit_results_sort = self.menu_edit.addAction(self.tr('S&ort Results...'))
        self.action_edit_results_sort.setStatusTip(self.tr('Sort results displayed in the table'))
        self.action_edit_results_sort.triggered.connect(self.edit_results_sort)

        # Preferences
        self.action_prefs_settings = self.menu_prefs.addAction(self.tr('&Settings'))
        self.action_prefs_settings.setStatusTip(self.tr('Change settings'))
        self.action_prefs_settings.triggered.connect(self.wl_settings.load)
        self.menu_prefs_display_lang = self.menu_prefs.addMenu(self.tr('&Display Language'))

        self.action_group_prefs_display_lang = QtWidgets.QActionGroup(self.menu_prefs_display_lang)
        self.action_group_prefs_display_lang.setExclusive(True)

        for action_lang, action_text, action_status_tip in (
            ('zho_cn', '汉语（简体）', '修改显示语言为汉语（简体）'),
            ('zho_tw', '漢語（繁體）', '修改顯示語言為漢語（繁體）'),
            ('eng_us', 'English (United States)', 'Change display language to English (United States)')
        ):
            self.__dict__[f'action_prefs_display_lang_{action_lang}'] = self.menu_prefs_display_lang.addAction(action_text)
            self.__dict__[f'action_prefs_display_lang_{action_lang}'].lang = action_lang
            self.__dict__[f'action_prefs_display_lang_{action_lang}'].setCheckable(True)
            self.__dict__[f'action_prefs_display_lang_{action_lang}'].setStatusTip(action_status_tip)
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
        self.action_help_need_help = self.menu_help.addAction(self.tr('&Need Help?'))
        self.action_help_need_help.setShortcut(QtGui.QKeySequence('F1'))
        self.action_help_need_help.setStatusTip(self.tr('Show help information'))
        self.action_help_need_help.triggered.connect(self.help_need_help)
        self.action_help_citing = self.menu_help.addAction(self.tr('&Citing'))
        self.action_help_citing.setStatusTip(self.tr('Show information about citing'))
        self.action_help_citing.triggered.connect(self.help_citing)

        self.menu_help.addSeparator()

        self.action_help_donating = self.menu_help.addAction(self.tr('&Donating'))
        self.action_help_donating.setStatusTip(self.tr('Show information about donating'))
        self.action_help_donating.triggered.connect(self.help_donating)
        self.action_help_acks = self.menu_help.addAction(self.tr('&Acknowledgments'))
        self.action_help_acks.setStatusTip(self.tr('Show acknowledgments'))
        self.action_help_acks.triggered.connect(self.help_acks)

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

    def init_central_widget(self):
        self.tabs_file_area = wl_layouts.Wl_Tab_Widget(self)

        self.wl_file_area = wl_file_area.Wrapper_File_Area(self)
        self.wl_file_area_ref = wl_file_area.Wrapper_File_Area(self, file_type = 'ref')

        # File Area
        self.tabs_file_area.addTab(self.wl_file_area, self.tr('Observed Corpora'))
        self.tabs_file_area.addTab(self.wl_file_area_ref, self.tr('Reference Corpora'))

        self.tabs_file_area.currentChanged.connect(self.file_area_changed)

        # Work Area
        self.init_work_area()

        # Splitter
        self.splitter_central_widget = wl_layouts.Wl_Splitter(QtCore.Qt.Vertical, self)
        self.splitter_central_widget.addWidget(self.wl_work_area)
        self.splitter_central_widget.addWidget(self.tabs_file_area)

        self.splitter_central_widget.setStretchFactor(0, 1)

        self.setCentralWidget(self.splitter_central_widget)

    def init_work_area(self):
        self.wl_work_area = wl_layouts.Wl_Tab_Widget(self)

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
            wl_dependency_parser.Wrapper_Dependency_Parser(self),
            self.tr('Dependency Parser')
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

    def load_settings(self):
        settings = self.settings_custom

        # Menu - Preferences
        self.__dict__[f"action_prefs_display_lang_{settings['menu']['prefs']['display_lang']}"].setChecked(True)
        self.action_prefs_show_status_bar.setChecked(settings['menu']['prefs']['show_status_bar'])

        self.prefs_display_lang()
        self.prefs_show_status_bar()

        # Layouts
        self.centralWidget().setSizes(settings['menu']['prefs']['layouts']['main_window'])
        self.wl_work_area.widget(0).splitter.setSizes(settings['menu']['prefs']['layouts']['profiler'])
        self.wl_work_area.widget(1).splitter.setSizes(settings['menu']['prefs']['layouts']['concordancer'])
        self.wl_work_area.widget(2).splitter.setSizes(settings['menu']['prefs']['layouts']['concordancer_parallel'])
        self.wl_work_area.widget(3).splitter.setSizes(settings['menu']['prefs']['layouts']['dependency_parser'])
        self.wl_work_area.widget(4).splitter.setSizes(settings['menu']['prefs']['layouts']['wordlist_generator'])
        self.wl_work_area.widget(5).splitter.setSizes(settings['menu']['prefs']['layouts']['ngram_generator'])
        self.wl_work_area.widget(6).splitter.setSizes(settings['menu']['prefs']['layouts']['collocation_extractor'])
        self.wl_work_area.widget(7).splitter.setSizes(settings['menu']['prefs']['layouts']['colligation_extractor'])
        self.wl_work_area.widget(8).splitter.setSizes(settings['menu']['prefs']['layouts']['keyword_extractor'])

        # File Area
        for i in range(self.tabs_file_area.count()):
            if self.tabs_file_area.widget(i).tab == self.settings_custom['tab_file_area']:
                self.tabs_file_area.setCurrentIndex(i)

                break

        self.tabs_file_area.currentWidget().table_files.model().itemChanged.emit(QtGui.QStandardItem())

        # Work Area
        for i in range(self.wl_work_area.count()):
            if self.wl_work_area.widget(i).tab == self.settings_custom['tab_work_area']:
                self.wl_work_area.setCurrentIndex(i)

                break

        self.work_area_changed()

    def file_area_changed(self):
        # Current tab
        self.settings_custom['tab_file_area'] = self.tabs_file_area.currentWidget().tab

    def work_area_changed(self):
        # Current tab
        self.settings_custom['tab_work_area'] = self.wl_work_area.currentWidget().tab

        # File Area
        if self.settings_custom['tab_work_area'] == 'keyword_extractor':
            self.tabs_file_area.tabBar().show()
        else:
            self.tabs_file_area.setCurrentIndex(0)

            # Hide single tab
            self.tabs_file_area.tabBar().hide()

        # Menu - Edit
        match self.wl_work_area.currentWidget().tab:
            case 'concordancer':
                table = self.wl_work_area.currentWidget().table_concordancer
            case 'concordancer_parallel':
                table = self.wl_work_area.currentWidget().table_concordancer_parallel
            case 'dependency_parser':
                table = self.wl_work_area.currentWidget().table_dependency_parser
            case 'wordlist_generator':
                table = self.wl_work_area.currentWidget().table_wordlist_generator
            case 'ngram_generator':
                table = self.wl_work_area.currentWidget().table_ngram_generator
            case 'collocation_extractor':
                table = self.wl_work_area.currentWidget().table_collocation_extractor
            case 'colligation_extractor':
                table = self.wl_work_area.currentWidget().table_colligation_extractor
            case 'keyword_extractor':
                table = self.wl_work_area.currentWidget().table_keyword_extractor
            case _:
                table = None

        if table:
            table.results_changed_menu_edit()

    def edit_results_search(self):
        match self.wl_work_area.currentWidget().tab:
            case 'concordancer':
                button_results_search = self.wl_work_area.currentWidget().table_concordancer.button_results_search
            case 'concordancer_parallel':
                button_results_search = self.wl_work_area.currentWidget().table_concordancer_parallel.button_results_search
            case 'dependency_parser':
                button_results_search = self.wl_work_area.currentWidget().table_dependency_parser.button_results_search
            case 'wordlist_generator':
                button_results_search = self.wl_work_area.currentWidget().table_wordlist_generator.button_results_search
            case 'ngram_generator':
                button_results_search = self.wl_work_area.currentWidget().table_ngram_generator.button_results_search
            case 'collocation_extractor':
                button_results_search = self.wl_work_area.currentWidget().table_collocation_extractor.button_results_search
            case 'colligation_extractor':
                button_results_search = self.wl_work_area.currentWidget().table_colligation_extractor.button_results_search
            case 'keyword_extractor':
                button_results_search = self.wl_work_area.currentWidget().table_keyword_extractor.button_results_search
            case _:
                button_results_search = None

        if button_results_search and button_results_search.isEnabled():
            button_results_search.click()

    def edit_results_filter(self):
        match self.wl_work_area.currentWidget().tab:
            case 'dependency_parser':
                button_results_filter = self.wl_work_area.currentWidget().table_dependency_parser.button_results_filter
            case 'wordlist_generator':
                button_results_filter = self.wl_work_area.currentWidget().table_wordlist_generator.button_results_filter
            case 'ngram_generator':
                button_results_filter = self.wl_work_area.currentWidget().table_ngram_generator.button_results_filter
            case 'collocation_extractor':
                button_results_filter = self.wl_work_area.currentWidget().table_collocation_extractor.button_results_filter
            case 'colligation_extractor':
                button_results_filter = self.wl_work_area.currentWidget().table_colligation_extractor.button_results_filter
            case 'keyword_extractor':
                button_results_filter = self.wl_work_area.currentWidget().table_keyword_extractor.button_results_filter
            case _:
                button_results_filter = None

        if button_results_filter and button_results_filter.isEnabled():
            button_results_filter.click()

    def edit_results_sort(self):
        match self.wl_work_area.currentWidget().tab:
            case 'concordancer':
                button_results_sort = self.wl_work_area.currentWidget().table_concordancer.button_results_sort
            case _:
                button_results_sort = None

        if button_results_sort and button_results_sort.isEnabled():
            button_results_sort.click()

    def prefs_display_lang(self):
        for action in self.action_group_prefs_display_lang.actions():
            if action.isChecked():
                if action.lang != self.settings_custom['menu']['prefs']['display_lang']:
                    if wl_dialogs_misc.Wl_Dialog_Restart_Required(self).exec():
                        with open(file_settings_display_lang, 'wb') as f:
                            pickle.dump(action.lang, f)

                        # Remove settings file
                        if os.path.exists(file_settings):
                            os.remove(file_settings)

                        # Remove file caches
                        for file in glob.glob(os.path.join(
                            self.settings_custom['general']['imp']['temp_files']['default_path'], '*.*'
                        )):
                            os.remove(file)

                        self.restart(save_settings = False)
                    else:
                        self.__dict__[f"action_prefs_display_lang_{self.settings_custom['menu']['prefs']['display_lang']}"].setChecked(True)

                break

    def prefs_reset_layouts(self):
        if wl_dialogs.Wl_Dialog_Question(
            self,
            title = self.tr('Reset Layouts'),
            text = self.tr('''
                <div>Do you want to reset all layouts to their default settings?</div>
            ''')
        ).exec():
            settings = self.settings_default['menu']['prefs']['layouts']

            self.centralWidget().setSizes(settings['main_window'])
            self.wl_work_area.widget(0).splitter.setSizes(settings['profiler'])
            self.wl_work_area.widget(1).splitter.setSizes(settings['concordancer'])
            self.wl_work_area.widget(2).splitter.setSizes(settings['concordancer_parallel'])
            self.wl_work_area.widget(3).splitter.setSizes(settings['dependency_parser'])
            self.wl_work_area.widget(4).splitter.setSizes(settings['wordlist_generator'])
            self.wl_work_area.widget(5).splitter.setSizes(settings['ngram_generator'])
            self.wl_work_area.widget(6).splitter.setSizes(settings['collocation_extractor'])
            self.wl_work_area.widget(7).splitter.setSizes(settings['colligation_extractor'])
            self.wl_work_area.widget(8).splitter.setSizes(settings['keyword_extractor'])

    def prefs_show_status_bar(self):
        self.settings_custom['menu']['prefs']['show_status_bar'] = self.action_prefs_show_status_bar.isChecked()

        if self.settings_custom['menu']['prefs']['show_status_bar']:
            self.statusBar().show()
        else:
            self.statusBar().hide()

    def help_need_help(self):
        Wl_Dialog_Need_Help(self).show()

    def help_citing(self):
        Wl_Dialog_Citing(self).show()

    def help_donating(self):
        Wl_Dialog_Donating(self).show()

    def help_acks(self):
        Wl_Dialog_Acks(self).show()

    def help_check_updates(self, on_startup = False):
        dialog_check_updates = Wl_Dialog_Check_Updates(self, on_startup = on_startup)

        if not on_startup:
            dialog_check_updates.show()

    def help_changelog(self):
        Wl_Dialog_Changelog(self).show()

    def help_about(self):
        Wl_Dialog_About(self).show()

    def save_settings(self):
        # Clear history of closed files
        self.settings_custom['file_area']['files_closed'].clear()
        self.settings_custom['file_area']['files_closed_ref'].clear()

        # Activate each tab to save layouts
        tab_work_area = self.settings_custom['tab_work_area']

        for i in range(self.wl_work_area.count()):
            self.wl_work_area.setCurrentIndex(i)

        self.settings_custom['tab_work_area'] = tab_work_area

        # Layouts
        self.settings_custom['menu']['prefs']['layouts']['main_window'] = self.centralWidget().sizes()
        self.settings_custom['menu']['prefs']['layouts']['profiler'] = self.wl_work_area.widget(0).splitter.sizes()
        self.settings_custom['menu']['prefs']['layouts']['concordancer'] = self.wl_work_area.widget(1).splitter.sizes()
        self.settings_custom['menu']['prefs']['layouts']['concordancer_parallel'] = self.wl_work_area.widget(2).splitter.sizes()
        self.settings_custom['menu']['prefs']['layouts']['dependency_parser'] = self.wl_work_area.widget(3).splitter.sizes()
        self.settings_custom['menu']['prefs']['layouts']['wordlist_generator'] = self.wl_work_area.widget(4).splitter.sizes()
        self.settings_custom['menu']['prefs']['layouts']['ngram_generator'] = self.wl_work_area.widget(5).splitter.sizes()
        self.settings_custom['menu']['prefs']['layouts']['collocation_extractor'] = self.wl_work_area.widget(6).splitter.sizes()
        self.settings_custom['menu']['prefs']['layouts']['colligation_extractor'] = self.wl_work_area.widget(7).splitter.sizes()
        self.settings_custom['menu']['prefs']['layouts']['keyword_extractor'] = self.wl_work_area.widget(8).splitter.sizes()

        with open(file_settings, 'wb') as f:
            pickle.dump(self.settings_custom, f)

    def restart(self, save_settings = True):
        # pylint: disable=consider-using-with
        # Save settings before restarting
        if save_settings:
            self.save_settings()

        if getattr(sys, '_MEIPASS', False):
            if is_windows:
                subprocess.Popen([wl_paths.get_path_file('Wordless.exe', internal = False)])
            elif is_macos or is_linux:
                subprocess.Popen([wl_paths.get_path_file('Wordless', internal = False)])
        else:
            if is_windows:
                subprocess.Popen(['python', '-m', 'wordless.wl_main'])
            elif is_macos:
                subprocess.Popen(['python3', '-m', 'wordless.wl_main'])
            elif is_linux:
                subprocess.Popen(['python3.11', '-m', 'wordless.wl_main'])

        sys.exit(0)

class Wl_Dialog_Need_Help(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = _tr('Wl_Dialog_Need_Help', 'Need Help?'),
            width = 600,
            height = 600,
            icon = 'info'
        )

        self.label_need_help = wl_labels.Wl_Label_Dialog(
            self.tr('''
                <div>If you have any questions, find software bugs, need to provide feedback, or want to submit feature requests, you may seek support from the open-source community or contact me directly via any of the support channels listed below.</div>
            '''),
            self
        )

        self.table_need_help = wl_tables.Wl_Table(
            self,
            headers = (
                self.tr('Support Channel'),
                self.tr('Information')
            )
        )

        self.table_need_help.verticalHeader().setHidden(True)
        self.table_need_help.model().setRowCount(6)

        self.table_need_help.disable_updates()

        self.table_need_help.setIndexWidget(
            self.table_need_help.model().index(0, 0),
            wl_labels.Wl_Label_Html(self.tr('Official documentation'), self)
        )
        self.table_need_help.setIndexWidget(
            self.table_need_help.model().index(0, 1),
            wl_labels.Wl_Label_Html(
                self.tr(
                    f'<a href="https://github.com/BLKSerene/Wordless/blob/{self.main.ver}/doc/doc.md">Stable Version</a> | <a href="https://github.com/BLKSerene/Wordless/blob/main/doc/doc.md">Development Version</a>'
                ),
                self
            )
        )

        self.table_need_help.setIndexWidget(
            self.table_need_help.model().index(1, 0),
            wl_labels.Wl_Label_Html(self.tr('Tutorial videos'), self)
        )
        self.table_need_help.setIndexWidget(
            self.table_need_help.model().index(1, 1),
            wl_labels.Wl_Label_Html(
                self.tr(
                    '<a href="https://www.youtube.com/@BLKSerene">YouTube</a> | <a href="https://space.bilibili.com/34963752/video">bilibili</a>'
                ),
                self
            )
        )

        self.table_need_help.setIndexWidget(
            self.table_need_help.model().index(2, 0),
            wl_labels.Wl_Label_Html(self.tr('Bug reports'), self)
        )
        self.table_need_help.setIndexWidget(
            self.table_need_help.model().index(2, 1),
            wl_labels.Wl_Label_Html(
                '<a href="https://github.com/BLKSerene/Wordless/issues">GitHub Issues</a>',
                self
            )
        )

        self.table_need_help.setIndexWidget(
            self.table_need_help.model().index(3, 0),
            wl_labels.Wl_Label_Html(self.tr('Usage questions'), self)
        )
        self.table_need_help.setIndexWidget(
            self.table_need_help.model().index(3, 1),
            wl_labels.Wl_Label_Html(
                '<a href="https://github.com/BLKSerene/Wordless/discussions">GitHub Discussions</a>',
                self
            )
        )

        self.table_need_help.setIndexWidget(
            self.table_need_help.model().index(4, 0),
            wl_labels.Wl_Label_Html(self.tr('Email support'), self)
        )
        self.table_need_help.setIndexWidget(
            self.table_need_help.model().index(4, 1),
            wl_labels.Wl_Label_Html(self.main.email_html, self)
        )

        self.table_need_help.setIndexWidget(
            self.table_need_help.model().index(5, 0),
            wl_labels.Wl_Label_Html(
                self.tr(
                    '<a href="https://www.wechat.com/en/">WeChat</a> official account'
                ),
                self
            )
        )
        self.table_need_help.setIndexWidget(
            self.table_need_help.model().index(5, 1),
            wl_labels.Wl_Label_Html_Centered(
                f'''<img src="{wl_paths.get_path_img('wechat_official_account.jpg')}">''',
                self
            )
        )

        self.table_need_help.enable_updates()

        self.layout_info.addWidget(self.label_need_help, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_need_help, 1, 0)

class Wl_Dialog_Citing(wl_dialogs.Wl_Dialog_Info_Copy):
    def __init__(self, main):
        super().__init__(
            main,
            title = _tr('Wl_Dialog_Citing', 'Citing'),
            width = 500,
            icon = 'info'
        )

        self.label_citing = wl_labels.Wl_Label_Dialog(
            self.tr('''
                <div>If you are going to publish a work that uses <i>Wordless</i>, please cite <i>Wordless</i> as a journal article or a piece of computer software.</div>
            '''),
            self
        )

        self.label_citation_style = QtWidgets.QLabel(self.tr('Citation style:'), self)
        self.combo_box_citation_style = wl_boxes.Wl_Combo_Box(self)
        self.label_cite_as = QtWidgets.QLabel(self.tr('Cite as:'), self)
        self.combo_box_cite_as = wl_boxes.Wl_Combo_Box(self)

        self.combo_box_citation_style.addItems([
            self.tr('APA (7th edition)'),
            self.tr('Chicago (18th edition)'),
            self.tr('MLA (9th edition)')
        ])
        self.combo_box_cite_as.addItems([
            self.tr('A journal article'),
            self.tr('A piece of computer software')
        ])

        self.combo_box_citation_style.currentTextChanged.connect(self.citation_changed)
        self.combo_box_cite_as.currentTextChanged.connect(self.citation_changed)

        layout_citation = wl_layouts.Wl_Layout()
        layout_citation.addWidget(self.label_citation_style, 0, 0)
        layout_citation.addWidget(self.combo_box_citation_style, 0, 1)
        layout_citation.addWidget(self.label_cite_as, 1, 0)
        layout_citation.addWidget(self.combo_box_cite_as, 1, 1)
        layout_citation.addWidget(self.text_edit_info, 2, 0, 1, 2)

        layout_citation.setColumnStretch(1, 1)

        self.layout_info.addWidget(self.label_citing, 0, 0)
        self.wrapper_info.layout().addLayout(layout_citation, 1, 0)

        self.load_settings()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['menu']['help']['citing'])

        self.combo_box_citation_style.setCurrentText(settings['citation_style'])
        self.combo_box_cite_as.setCurrentText(settings['cite_as'])

        self.citation_changed()

    def citation_changed(self):
        settings = self.main.settings_custom['menu']['help']['citing']

        settings['citation_style'] = self.combo_box_citation_style.currentText()
        settings['cite_as'] = self.combo_box_cite_as.currentText()

        if settings['citation_style'].startswith('APA'):
            if settings['cite_as'] == self.tr('A journal article'):
                self.set_info(
                    'Ye, L. (2024). Wordless: An integrated corpus tool with multilingual support for the study of language, literature, and translation. <i>SoftwareX</i>, <i>28</i>, Article 101931. https://doi.org/10.1016/j.softx.2024.101931'
                )
            elif settings['cite_as'] == self.tr('A piece of computer software'):
                self.set_info(
                    f'Ye, L. ({self.main.copyright_year}). <i>Wordless</i> (Version {self.main.ver}) [Computer software]. GitHub. https://github.com/BLKSerene/Wordless'
                )
        elif settings['citation_style'].startswith(self.tr('Chicago')):
            if settings['cite_as'] == self.tr('A journal article'):
                self.set_info(
                    'Ye, Lei. “Wordless: An Integrated Corpus Tool with Multilingual Support for the Study of Language, Literature, and Translation.” <i>SoftwareX</i> 28 (December 2024): 101931. https://doi.org/10.1016/j.softx.2024.101931.'
                )
            elif settings['cite_as'] == self.tr('A piece of computer software'):
                self.set_info(
                    f'Ye, Lei. <i>Wordless</i>. V. {self.main.ver}. Released July 27, {self.main.copyright_year}. PC. https://github.com/BLKSerene/Wordless.'
                )
        elif settings['citation_style'].startswith('MLA'):
            if settings['cite_as'] == self.tr('A journal article'):
                self.set_info(
                    'Ye Lei. “Wordless: An Integrated Corpus Tool with Multilingual Support for the Study of Language, Literature, and Translation.” <i>SoftwareX</i>, vol. 28, Dec. 2024, https://doi.org/10.1016/j.softx.2024.101931.'
                )
            elif settings['cite_as'] == self.tr('A piece of computer software'):
                self.set_info(
                    f'Ye Lei. <i>Wordless</i>. Version {self.main.ver}, <i>GitHub</i>, 27 Jul. {self.main.copyright_year}, https://github.com/BLKSerene/Wordless.'
                )

class Wl_Dialog_Donating(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = _tr('Wl_Dialog_Donating', 'Donating'),
            width = 450,
            icon = 'info'
        )

        self.label_donating = wl_labels.Wl_Label_Dialog(
            self.tr('''
                <div>If you would like to support the development of <i>Wordless</i>, you may donate via <a href="https://www.paypal.com/">PayPal</a>, <a href="https://global.alipay.com/">Alipay</a>, or <a href="https://pay.weixin.qq.com/index.php/public/wechatpay_en">WeChat Pay</a>.</div>
            '''),
            self
        )
        self.label_donating_via = QtWidgets.QLabel(self.tr('Donating via:'), self)
        self.combo_box_donating_via = wl_boxes.Wl_Combo_Box(self)
        self.label_donating_via_img = wl_labels.Wl_Label_Html('', self)

        self.combo_box_donating_via.addItems([
            'PayPal',
            self.tr('Alipay'),
            self.tr('WeChat Pay')
        ])

        self.combo_box_donating_via.currentTextChanged.connect(self.donating_via_changed)

        layout_donating_via = wl_layouts.Wl_Layout()
        layout_donating_via.addWidget(self.label_donating_via, 0, 0)
        layout_donating_via.addWidget(self.combo_box_donating_via, 0, 1)

        layout_donating_via.setColumnStretch(2, 1)

        self.layout_info.addWidget(self.label_donating, 0, 0)
        self.wrapper_info.layout().addLayout(layout_donating_via, 1, 0)
        self.wrapper_info.layout().addWidget(self.label_donating_via_img, 2, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.wrapper_info.layout().setRowStretch(2, 1)

        self.load_settings()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['menu']['help']['donating'])

        self.combo_box_donating_via.setCurrentText(settings['donating_via'])

        self.donating_via_changed()

    def donating_via_changed(self):
        settings = self.main.settings_custom['menu']['help']['donating']

        settings['donating_via'] = self.combo_box_donating_via.currentText()

        if settings['donating_via'] == 'PayPal':
            self.label_donating_via_img.setText(
                f'''<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=V2V54NYE2YD32"><img src="{wl_paths.get_path_img('donating_paypal.gif')}"></a>'''
            )
        elif settings['donating_via'] == self.tr('Alipay'):
            self.label_donating_via_img.setText(
                f'''<img src="{wl_paths.get_path_img('donating_alipay.png')}">'''
            )
        elif settings['donating_via'] == self.tr('WeChat Pay'):
            self.label_donating_via_img.setText(
                f'''<img src="{wl_paths.get_path_img('donating_wechat_pay.png')}">'''
            )

        self.label_donating_via_img.adjustSize()
        self.adjust_size()

class Wl_Dialog_Acks(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = _tr('Wl_Dialog_Acks', 'Acknowledgments'),
            width = 700,
            height = 600,
            icon = 'info'
        )

        # Load acknowledgments
        acks = []

        with open(wl_paths.get_path_file(self.tr('ACKS.md')), 'r', encoding = 'utf_8') as f:
            for line in f:
                if re.search(r'^[1-9]\d*\s*\|', line):
                    _, proj_name, proj_ver, proj_authors, proj_license = line.split('|')

                    proj_name = re.sub(r'^\[(.+)\]\((.+)\)$', r'<a href="\2">\1</a>', proj_name.strip())
                    proj_ver = proj_ver.strip()
                    proj_authors = proj_authors.strip()
                    proj_license = re.sub(r'^\[(.+)\]\((.+)\)$', r'<a href="\2">\1</a>', proj_license.strip())

                    acks.append([proj_name, proj_ver, proj_authors, proj_license])

        self.label_acks = wl_labels.Wl_Label_Dialog(
            self.tr('''
                <div>As <i>Wordless</i> stands on the shoulders of giants, I hereby extend my sincere gratitude to the following open-source projects without which this project would not have been possible:</div>
            '''),
            self
        )
        self.table_acks = wl_tables.Wl_Table(
            self,
            headers = (
                self.tr('Name'),
                self.tr('Version'),
                self.tr('Authors'),
                self.tr('License')
            )
        )

        self.table_acks.model().setRowCount(len(acks))
        self.table_acks.disable_updates()

        for i, (name, ver, authors, proj_license) in enumerate(acks):
            self.table_acks.setIndexWidget(self.table_acks.model().index(i, 0), wl_labels.Wl_Label_Html(name, self))
            self.table_acks.setIndexWidget(self.table_acks.model().index(i, 1), wl_labels.Wl_Label_Html_Centered(ver, self))
            self.table_acks.setIndexWidget(self.table_acks.model().index(i, 2), wl_labels.Wl_Label_Html(authors, self))
            self.table_acks.setIndexWidget(self.table_acks.model().index(i, 3), wl_labels.Wl_Label_Html_Centered(proj_license, self))

        self.table_acks.enable_updates()

        self.layout_info.addWidget(self.label_acks, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_acks, 1, 0)

class Wl_Dialog_Check_Updates(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main, on_startup = False):
        super().__init__(
            main,
            title = _tr('Wl_Dialog_Check_Updates', 'Check for Updates'),
            width = 550,
            no_buttons = True
        )

        self.on_startup = on_startup

        self.label_checking_status = wl_labels.Wl_Label_Dialog('<div></div>', self)
        self.label_cur_ver = wl_labels.Wl_Label_Dialog(self.tr('<div>Current version: </div>') + str(self.main.ver), self)
        self.label_latest_ver = wl_labels.Wl_Label_Dialog('<div></div>', self)

        self.checkbox_check_updates_on_startup = QtWidgets.QCheckBox(self.tr('Check for updates on startup'), self)
        self.button_try_again = QtWidgets.QPushButton(self.tr('Try again'), self)
        self.button_cancel = QtWidgets.QPushButton(self.tr('Cancel'), self)

        self.checkbox_check_updates_on_startup.stateChanged.connect(self.check_updates_on_startup_changed)
        self.button_try_again.clicked.connect(self.check_updates)

        self.layout_info.addWidget(self.label_checking_status, 0, 0, 2, 1)
        self.layout_info.addWidget(self.label_cur_ver, 2, 0)
        self.layout_info.addWidget(self.label_latest_ver, 3, 0)

        self.layout_buttons.addWidget(self.checkbox_check_updates_on_startup, 0, 0)
        self.layout_buttons.addWidget(self.button_try_again, 0, 2)
        self.layout_buttons.addWidget(self.button_cancel, 0, 3)

        self.layout_buttons.setColumnStretch(1, 1)

        self.load_settings()

    def check_updates(self):
        self.checking_status_changed('checking')

        self.main.worker_check_updates = Worker_Check_Updates(self.main)
        thread_check_updates = QtCore.QThread()

        self.main.threads_check_updates.append(thread_check_updates)

        thread_check_updates.destroyed.connect(lambda: self.main.threads_check_updates.remove(thread_check_updates))

        wl_threading.start_worker_in_thread(
            self.main.worker_check_updates,
            thread_check_updates,
            self.checking_status_changed
        )

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
            self.label_checking_status.set_text(self.tr('<div>Checking for updates...</div>'))
            self.label_latest_ver.set_text(self.tr('<div>Latest version: Checking...</div>'))

            self.button_cancel.setText(self.tr('Cancel'))
            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.stop_checking)
        else:
            match status:
                case 'updates_available':
                    self.label_checking_status.set_text(self.tr('''
                        <div><i>Wordless</i> {} is out. Click <a href="https://github.com/BLKSerene/Wordless#download"><b>HERE</b></a> to download the latest version of <i>Wordless</i>.</div>
                    ''').format(ver_new))
                    self.label_latest_ver.set_text(self.tr('<div>Latest version: </div>') + ver_new)
                case 'no_updates':
                    self.label_checking_status.set_text(self.tr('''
                        <div>Hooray! You are using the latest version of <i>Wordless</i>!</div>
                    '''))
                    self.label_latest_ver.set_text(self.tr('<div>Latest version: </div>') + str(self.main.ver))
                case 'network_err':
                    self.label_checking_status.set_text(self.tr('''
                        <div>A network error has occurred. Please check your network settings and try again or <a href="https://github.com/BLKSerene/Wordless/releases">check for updates manually</a>.</div>
                    '''))
                    self.label_latest_ver.set_text(self.tr('<div>Latest version: Network error</div>'))

            self.button_cancel.setText(self.tr('OK'))
            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)

        # On startup
        if self.on_startup:
            if status == 'updates_available':
                self.exec()
            else:
                self.accept()

    def load_settings(self):
        settings = self.main.settings_custom['general']['update_settings']

        self.checkbox_check_updates_on_startup.setChecked(settings['check_updates_on_startup'])

        self.check_updates()

    def check_updates_on_startup_changed(self):
        settings = self.main.settings_custom['general']['update_settings']

        settings['check_updates_on_startup'] = self.checkbox_check_updates_on_startup.isChecked()

class Worker_Check_Updates(QtCore.QObject):
    finished = QtCore.pyqtSignal(str, str)

    def __init__(self, main):
        super().__init__()

        self.main = main
        self.stopped = False

    def run(self):
        ver_new = ''

        r, err_msg = wl_misc.wl_download(self.main, 'https://raw.githubusercontent.com/BLKSerene/Wordless/main/VERSION')

        if not err_msg:
            for line in r.text.splitlines():
                if line and not line.startswith('#'):
                    ver_new = line.rstrip()

            if self.main.ver < packaging.version.Version(ver_new):
                updates_status = 'updates_available'
            else:
                updates_status = 'no_updates'
        else:
            updates_status = 'network_err'

        if self.stopped:
            updates_status = ''

        self.finished.emit(updates_status, ver_new)

    def stop(self):
        self.stopped = True

class Wl_Dialog_Changelog(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = _tr('Wl_Dialog_Changelog', 'Changelog'),
            width = 600,
            height = 600
        )

        changelog = []

        with open(wl_paths.get_path_file('CHANGELOG.md'), 'r', encoding = 'utf_8') as f:
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

        font_size_custom = main.settings_custom['general']['ui_settings']['font_size']

        changelog_text = f'''
            <head><style>
                * {{
                    margin: 0;
                    line-height: 120%;
                }}

                ul {{
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
                    font-size: {font_size_custom}pt;
                    font-weight: bold;
                }}

                .changelog-section-header {{
                    margin-bottom: 5px;
                    font-size: {font_size_custom}pt;
                    font-weight: bold;
                }}
            </style></head>
            <body align="justify">
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

        text_edit_changelog = wl_editors.Wl_Text_Browser(self)
        text_edit_changelog.setHtml(changelog_text)

        self.layout_info.addWidget(text_edit_changelog, 0, 0)

class Wl_Dialog_About(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(
            main,
            title = _tr('Wl_Dialog_About', 'About Wordless')
        )

        img_wl_icon = QtGui.QPixmap(wl_paths.get_path_img('wl_icon_about.png'))

        label_about_icon = QtWidgets.QLabel('', self)
        label_about_icon.setPixmap(img_wl_icon)

        label_about_title = wl_labels.Wl_Label_Dialog_No_Wrap(
            self.tr('''
                <div align="center">
                    <h2>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Wordless</h2>
                    <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Version {}</div>
                </div>
            ''').format(main.ver),
            self
        )

        label_about_info = wl_labels.Wl_Label_Dialog_No_Wrap(
            self.tr('''
                <div align="center">
                    An Integrated Corpus Tool with Multilingual Support<br>
                    for the Study of Language, Literature, and Translation
                </div>
                <hr>
                <div align="center">
                    Copyright (C) 2018-{}&nbsp;&nbsp;Ye Lei (叶磊)<br>
                    Licensed Under GNU GPLv3<br>
                    All Other Rights Reserved
                </div>
            ''').format(self.main.copyright_year),
            self
        )

        self.layout_info.addWidget(label_about_icon, 0, 0, QtCore.Qt.AlignHCenter)
        self.layout_info.addWidget(label_about_title, 0, 0, 1, 2)
        self.layout_info.addWidget(label_about_info, 1, 0, 1, 2)

        self.layout_info.setColumnStretch(0, 9)
        self.layout_info.setColumnStretch(1, 5)

if __name__ == '__main__':
    file_settings = wl_paths.get_path_file('wl_settings.pickle', internal = False)
    file_settings_display_lang = wl_paths.get_path_file('wl_settings_display_lang.pickle', internal = False)

    first_startup = not os.path.exists(file_settings)
    corrupt_settings_file = False
    ui_scaling = wl_settings_default.DEFAULT_INTERFACE_SCALING
    global_font_family = wl_settings_default.DEFAULT_FONT_FAMILY
    global_font_size = wl_settings_default.DEFAULT_FONT_SIZE

    if not first_startup:
        with open(file_settings, 'rb') as f:
            try:
                settings_custom = pickle.load(f)

                ui_scaling = settings_custom['general']['ui_settings']['interface_scaling']
                global_font_family = settings_custom['general']['ui_settings']['font_family']
                global_font_size = settings_custom['general']['ui_settings']['font_size']
            # Empty pickle file
            except EOFError:
                corrupt_settings_file = True

    # Remove the empty pickle file
    if corrupt_settings_file:
        os.remove(file_settings)

    # Environment variables for QT should be set before QApplication is created
    os.environ['QT_SCALE_FACTOR'] = re.sub(r'([0-9]{2})%$', r'.\1', ui_scaling)

    wl_app = QtWidgets.QApplication(sys.argv)

    # Translations
    if os.path.exists(file_settings_display_lang):
        with open(file_settings_display_lang, 'rb') as f:
            display_lang = pickle.load(f)
    else:
        display_lang = 'eng_us'

    if display_lang != 'eng_us':
        translator = QtCore.QTranslator()
        translator.load(wl_paths.get_path_file('trs', f'{display_lang}.qm'))

        wl_app.installTranslator(translator)

    wl_loading = Wl_Loading()

    wl_loading.raise_()
    wl_loading.fade_in()

    wl_app.processEvents()

    wl_main = Wl_Main(wl_loading)

    wl_loading.fade_out()
    wl_loading.finish(wl_main)

    wl_main.showMaximized()

    # Show changelog on first startup
    if first_startup:
        dialog_changelog = Wl_Dialog_Changelog(wl_main)
        dialog_changelog.move_to_center()
        dialog_changelog.show()

    if corrupt_settings_file:
        dialog_corrupt_settings_file = wl_dialogs.Wl_Dialog_Info_Simple(
            wl_main,
            title = _tr('wl_main', 'Corrupt Settings File'),
            text = _tr('wl_main', '''
                <div>The settings file might be corrupt since an error occurred when loading it.</div>
                <br>
                <div>All settings have been automatically reset to their default values to fix the problem.</div>
            '''),
            icon = 'critical'
        )

        dialog_corrupt_settings_file.move_to_center()
        dialog_corrupt_settings_file.exec()

    # Check for updates on startup
    if wl_main.settings_custom['general']['update_settings']['check_updates_on_startup']:
        wl_main.help_check_updates(on_startup = True)

    sys.exit(wl_app.exec())
