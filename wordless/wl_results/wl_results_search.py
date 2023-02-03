# ----------------------------------------------------------------------
# Wordless: Results - Search
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

from PyQt5.QtCore import QCoreApplication, QSize, Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QPushButton

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs, wl_dialogs_misc, wl_msg_boxes
from wordless.wl_nlp import wl_matching, wl_nlp_utils
from wordless.wl_utils import wl_misc, wl_threading
from wordless.wl_widgets import wl_buttons, wl_layouts, wl_widgets

_tr = QCoreApplication.translate

class Wl_Worker_Results_Search(wl_threading.Wl_Worker):
    def run(self):
        for table in self.dialog.tables:
            results = {}
            search_terms = set()

            for col in range(table.model().columnCount()):
                if table.indexWidget(table.model().index(0, col)):
                    for row in range(table.model().rowCount()):
                        results[(row, col)] = table.indexWidget(table.model().index(row, col)).text_search
                else:
                    for row in range(table.model().rowCount()):
                        try:
                            results[(row, col)] = table.model().item(row, col).text_raw
                        except AttributeError:
                            results[(row, col)] = [table.model().item(row, col).text()]

            items = [token for text in results.values() for token in text]

            for file in table.settings['file_area']['files_open']:
                if file['selected']:
                    search_terms_file = wl_matching.match_search_terms_ngrams(
                        self.main, items,
                        lang = file['lang'],
                        tagged = file['tagged'],
                        token_settings = table.settings[self.dialog.tab]['token_settings'],
                        search_settings = self.dialog.settings
                    )

                    search_terms |= set(search_terms_file)

            for search_term in search_terms:
                len_search_term = len(search_term)

                for (row, col), text in results.items():
                    for ngram in wl_nlp_utils.ngrams(text, len_search_term):
                        if ngram == search_term:
                            self.dialog.items_found.append([table, row, col])

        self.dialog.items_found = sorted(
            self.dialog.items_found,
            key = lambda item: (id(item[0]), item[1], item[2])
        )

        self.progress_updated.emit(self.tr('Highlighting found items...'))
        self.worker_done.emit()

class Wl_Dialog_Results_Search(wl_dialogs.Wl_Dialog):
    def __init__(self, main, tab, table):
        super().__init__(main, _tr('Wl_Dialog_Results_Search', 'Search in Results'))

        self.tab = tab
        self.tables = [table]
        self.settings = self.main.settings_custom[self.tab]['search_results']
        self.items_found = []

        self.main.wl_work_area.currentChanged.connect(self.reject)

        (
            self.label_search_term,
            self.checkbox_multi_search_mode,

            self.stacked_widget_search_term,
            self.line_edit_search_term,
            self.list_search_terms,
            self.label_delimiter,

            self.checkbox_match_case,
            self.checkbox_match_whole_words,
            self.checkbox_match_inflected_forms,
            self.checkbox_use_regex,
            self.checkbox_match_without_tags,
            self.checkbox_match_tags
        ) = wl_widgets.wl_widgets_search_settings(self, self.tab)

        self.button_find_next = QPushButton(self.tr('Find next'), self)
        self.button_find_prev = QPushButton(self.tr('Find previous'), self)
        self.button_find_all = QPushButton(self.tr('Find all'), self)
        self.button_clr_hightlights = QPushButton(self.tr('Clear highlights'), self)

        self.button_restore_defaults = wl_buttons.Wl_Button_Restore_Defaults(self, load_settings = self.load_settings)
        self.button_close = QPushButton(self.tr('Close'), self)

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.button_find_next.click)
        self.list_search_terms.model().dataChanged.connect(self.search_settings_changed)

        self.checkbox_match_case.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_whole_words.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_inflected_forms.stateChanged.connect(self.search_settings_changed)
        self.checkbox_use_regex.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_without_tags.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_tags.stateChanged.connect(self.search_settings_changed)

        self.button_find_next.clicked.connect(lambda: self.find_next()) # pylint: disable=unnecessary-lambda
        self.button_find_prev.clicked.connect(lambda: self.find_prev()) # pylint: disable=unnecessary-lambda
        self.button_find_all.clicked.connect(lambda: self.find_all()) # pylint: disable=unnecessary-lambda
        self.button_clr_hightlights.clicked.connect(self.clr_highlights)

        self.button_close.clicked.connect(self.reject)

        layout_buttons_right = wl_layouts.Wl_Layout()
        layout_buttons_right.addWidget(self.button_find_next, 0, 0)
        layout_buttons_right.addWidget(self.button_find_prev, 1, 0)
        layout_buttons_right.addWidget(self.button_find_all, 2, 0)
        layout_buttons_right.addWidget(self.button_clr_hightlights, 3, 0)

        layout_buttons_right.setRowStretch(4, 1)

        layout_buttons_bottom = wl_layouts.Wl_Layout()
        layout_buttons_bottom.addWidget(self.button_restore_defaults, 0, 0)
        layout_buttons_bottom.addWidget(self.button_close, 0, 2)

        layout_buttons_bottom.setColumnStretch(1, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.label_search_term, 0, 0)
        self.layout().addWidget(self.checkbox_multi_search_mode, 0, 1, Qt.AlignRight)
        self.layout().addWidget(self.stacked_widget_search_term, 1, 0, 1, 2)
        self.layout().addWidget(self.label_delimiter, 2, 0, 1, 2)

        self.layout().addWidget(self.checkbox_match_case, 3, 0, 1, 2)
        self.layout().addWidget(self.checkbox_match_whole_words, 4, 0, 1, 2)
        self.layout().addWidget(self.checkbox_match_inflected_forms, 5, 0, 1, 2)
        self.layout().addWidget(self.checkbox_use_regex, 6, 0, 1, 2)
        self.layout().addWidget(self.checkbox_match_without_tags, 7, 0, 1, 2)
        self.layout().addWidget(self.checkbox_match_tags, 8, 0, 1, 2)

        self.layout().addWidget(wl_layouts.Wl_Separator(self, orientation = 'vert'), 0, 2, 9, 1)
        self.layout().addLayout(layout_buttons_right, 0, 3, 9, 1)

        self.layout().addWidget(wl_layouts.Wl_Separator(self), 9, 0, 1, 4)
        self.layout().addLayout(layout_buttons_bottom, 10, 0, 1, 4)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['search_results'])
        else:
            settings = copy.deepcopy(self.settings)

        self.checkbox_multi_search_mode.setChecked(settings['multi_search_mode'])

        if not defaults:
            self.line_edit_search_term.setText(settings['search_term'])
            self.list_search_terms.load_items(settings['search_terms'])

        self.checkbox_match_case.setChecked(settings['match_case'])
        self.checkbox_match_whole_words.setChecked(settings['match_whole_words'])
        self.checkbox_match_inflected_forms.setChecked(settings['match_inflected_forms'])
        self.checkbox_use_regex.setChecked(settings['use_regex'])
        self.checkbox_match_without_tags.setChecked(settings['match_without_tags'])
        self.checkbox_match_tags.setChecked(settings['match_tags'])

        self.search_settings_changed()
        self.clr_highlights()

    def search_settings_changed(self):
        self.settings['multi_search_mode'] = self.checkbox_multi_search_mode.isChecked()
        self.settings['search_term'] = self.line_edit_search_term.text()
        self.settings['search_terms'] = self.list_search_terms.model().stringList()

        self.settings['match_case'] = self.checkbox_match_case.isChecked()
        self.settings['match_whole_words'] = self.checkbox_match_whole_words.isChecked()
        self.settings['match_inflected_forms'] = self.checkbox_match_inflected_forms.isChecked()
        self.settings['use_regex'] = self.checkbox_use_regex.isChecked()
        self.settings['match_without_tags'] = self.checkbox_match_without_tags.isChecked()
        self.settings['match_tags'] = self.checkbox_match_tags.isChecked()

        if wl_checks_work_area.check_search_terms(
            self.main,
            search_settings = self.settings,
            show_warning = False
        ):
            self.button_find_next.setEnabled(True)
            self.button_find_prev.setEnabled(True)
            self.button_find_all.setEnabled(True)
        else:
            self.button_find_next.setEnabled(False)
            self.button_find_prev.setEnabled(False)
            self.button_find_all.setEnabled(False)

        if 'size_multi' in self.__dict__:
            if self.settings['multi_search_mode']:
                self.setFixedSize(self.size_multi)
            else:
                self.setFixedSize(self.size_normal)

    @wl_misc.log_timing
    def find_next(self):
        self.find_all()

        if self.items_found:
            selected_rows = []

            for table in self.tables:
                table.disable_updates()

            for table in self.tables:
                if table.get_selected_rows():
                    selected_rows = [id(table), table.get_selected_rows()]

                    break

            # Scroll to the next found item
            if selected_rows:
                for table in self.tables:
                    table.clearSelection()

                for table, row, _ in self.items_found:
                    # Tables are sorted by their string representations
                    if (
                        id(table) > selected_rows[0]
                        or id(table) == selected_rows[0] and row > selected_rows[1][-1]
                    ):
                        table.selectRow(row)
                        table.setFocus()

                        table.scrollTo(table.model().index(row, 0))

                        break

                # Scroll to top if this is the last item
                if not any((table.selectedIndexes() for table in self.tables)):
                    self.tables[0].scrollTo(table.model().index(self.items_found[0][1], 0))
                    self.tables[0].selectRow(self.items_found[0][1])
            else:
                self.tables[0].scrollTo(table.model().index(self.items_found[0][1], 0))
                self.tables[0].selectRow(self.items_found[0][1])

            for table in self.tables:
                table.enable_updates()

    @wl_misc.log_timing
    def find_prev(self):
        self.find_all()

        if self.items_found:
            selected_rows = []

            for table in self.tables:
                table.hide()
                table.blockSignals(True)
                table.setUpdatesEnabled(False)

            for table in self.tables:
                if table.get_selected_rows():
                    selected_rows = [id(table), table.get_selected_rows()]

                    break

            # Scroll to the previous found item
            if selected_rows:
                for table in self.tables:
                    table.clearSelection()

                for table, row, _ in reversed(self.items_found):
                    # Tables are sorted by their string representations
                    if (
                        id(table) < selected_rows[0]
                        or id(table) == selected_rows[0] and row < selected_rows[1][-1]
                    ):
                        table.selectRow(row)
                        table.setFocus()

                        table.scrollTo(table.model().index(row, 0))

                        break

                # Scroll to bottom if this is the first item
                if not any((table.selectedIndexes() for table in self.tables)):
                    self.tables[-1].scrollTo(table.model().index(self.items_found[-1][1], 0))
                    self.tables[-1].selectRow(self.items_found[-1][1])
            else:
                self.tables[-1].scrollTo(table.model().index(self.items_found[-1][1], 0))
                self.tables[-1].selectRow(self.items_found[-1][1])

            for table in self.tables:
                table.blockSignals(False)
                table.setUpdatesEnabled(True)
                table.show()

    @wl_misc.log_timing
    def find_all(self):
        self.clr_highlights()

        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = self.tr('Searching in results...'))

        worker_results_search = Wl_Worker_Results_Search(
            self.main,
            dialog_progress = dialog_progress,
            update_gui = self.update_gui,
            dialog = self
        )

        wl_threading.Wl_Thread(worker_results_search).start_worker()

    def update_gui(self):
        if self.items_found:
            for table in self.tables:
                table.disable_updates()

            for table, row, col in self.items_found:
                if table.indexWidget(table.model().index(row, col)):
                    table.indexWidget(table.model().index(row, col)).setStyleSheet('border: 1px solid #E53E3A;')
                else:
                    table.model().item(row, col).setForeground(QBrush(QColor('#FFF')))
                    table.model().item(row, col).setBackground(QBrush(QColor('#E53E3A')))

            for table in self.tables:
                table.enable_updates()

            self.button_clr_hightlights.setEnabled(True)
        else:
            wl_msg_boxes.Wl_Msg_Box_Warning(
                self.main,
                title = self.tr('No Search Results'),
                text = self.tr('''
                    <div>Searching has completed successfully, but there are no results found.</div>
                    <div>You can change your settings and try again.</div>
                ''')
            ).open()

            self.button_clr_hightlights.setEnabled(False)

        len_items_found = len(self.items_found)
        msg_item = self.tr('item') if len_items_found == 1 else self.tr('items')

        self.main.statusBar().showMessage(self.tr('Found {} {}.').format(len_items_found, msg_item))

    def clr_highlights(self):
        if self.items_found:
            for table in self.tables:
                table.disable_updates()

            for table, row, col in self.items_found:
                if table.indexWidget(table.model().index(row, col)):
                    table.indexWidget(table.model().index(row, col)).setStyleSheet('border: 0')
                else:
                    table.model().item(row, col).setForeground(QBrush(QColor('#292929')))
                    table.model().item(row, col).setBackground(QBrush(QColor('#FFF')))

            for table in self.tables:
                table.enable_updates()

            self.items_found.clear()
            self.main.statusBar().showMessage(self.tr('Highlights cleared.'))

        self.button_clr_hightlights.setEnabled(False)

    def load(self):
        # Calculate size
        if 'size_multi' not in self.__dict__:
            multi_search_mode = self.settings['multi_search_mode']

            self.checkbox_multi_search_mode.setChecked(False)

            self.adjustSize()
            self.size_normal = self.size()

            self.checkbox_multi_search_mode.setChecked(True)

            self.adjustSize()
            self.size_multi = QSize(self.size_normal.width(), self.size().height())

            self.checkbox_multi_search_mode.setChecked(multi_search_mode)

        self.show()
