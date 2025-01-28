# ----------------------------------------------------------------------
# Wordless: Results - Sort results
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

# pylint: disable=broad-exception-caught

import copy
import re
import traceback

from PyQt5.QtCore import pyqtSignal, QCoreApplication
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import (
    QAbstractItemDelegate,
    QComboBox,
    QMessageBox,
    QPushButton
)

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs, wl_dialogs_misc
from wordless.wl_utils import wl_misc, wl_threading
from wordless.wl_widgets import (
    wl_buttons,
    wl_item_delegates,
    wl_labels,
    wl_layouts,
    wl_tables
)

_tr = QCoreApplication.translate

RE_SORTING_COL_L = re.compile(_tr('Wl_Dialog_Results_Sort_Concordancer', r'^L[1-9][0-9]*$'))
RE_SORTING_COL_R = re.compile(_tr('Wl_Dialog_Results_Sort_Concordancer', r'^R[1-9][0-9]*$'))

class Wl_Dialog_Results_Sort_Concordancer(wl_dialogs.Wl_Dialog):
    def __init__(self, main, table):
        super().__init__(
            main,
            title = _tr('Wl_Dialog_Results_Sort_Concordancer', 'Sort Results'),
            width = 550,
            height = 300
        )

        self.tab = table.tab
        self.table = table
        self.settings = self.main.settings_custom[self.tab]['sort_results']

        self.main.wl_work_area.currentChanged.connect(self.reject)

        self.table_sort = Wl_Table_Results_Sort_Conordancer(self, table = self.table)

        self.button_restore_defaults = wl_buttons.Wl_Button_Restore_Defaults(self, load_settings = self.load_settings)
        self.button_sort = QPushButton(self.tr('Sort'), self)
        self.button_close = QPushButton(self.tr('Close'), self)

        self.button_sort.clicked.connect(lambda: self.sort_results()) # pylint: disable=unnecessary-lambda
        self.button_close.clicked.connect(self.reject)

        layout_table_sort = wl_layouts.Wl_Layout()
        layout_table_sort.addWidget(self.table_sort, 0, 0, 4, 1)
        layout_table_sort.addWidget(self.table_sort.button_add, 0, 1)
        layout_table_sort.addWidget(self.table_sort.button_ins, 1, 1)
        layout_table_sort.addWidget(self.table_sort.button_del, 2, 1)
        layout_table_sort.addWidget(self.table_sort.button_clr, 3, 1)

        layout_table_sort.setRowStretch(0, 1)
        layout_table_sort.setColumnStretch(0, 1)

        layout_buttons = wl_layouts.Wl_Layout()
        layout_buttons.addWidget(self.button_restore_defaults, 0, 0)
        layout_buttons.addWidget(self.button_sort, 0, 2)
        layout_buttons.addWidget(self.button_close, 0, 3)

        layout_buttons.setColumnStretch(1, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addLayout(layout_table_sort, 0, 0)
        self.layout().addLayout(layout_buttons, 1, 0)

        self.layout().setRowStretch(0, 1)

        self.load_settings()

    # To be called by Restore defaults
    def load_settings(self, defaults = False):
        self.table_sort.load_settings(defaults = defaults)

    @wl_misc.log_time
    def sort_results(self):
        if not self.table.is_empty():
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = self.tr('Sorting results...'))

            worker_results_sort_concordancer = Wl_Worker_Results_Sort_Concordancer(
                self.main,
                dialog_progress = dialog_progress,
                update_gui = self.update_gui,
                dialog = self
            )

            thread_results_sort_concordancer = wl_threading.Wl_Thread(worker_results_sort_concordancer)
            thread_results_sort_concordancer.start_worker()

    def update_gui(self, err_msg, results):
        if wl_checks_work_area.check_postprocessing(self.main, err_msg):
            try:
                # Create new labels
                for i, (
                    left_old, node_old, right_old,
                    _, _, _, _, _, _, _, _, _, _
                ) in enumerate(results):
                    left_new = wl_labels.Wl_Label_Html('', self.table)
                    node_new = wl_labels.Wl_Label_Html(node_old.text(), self.table)
                    right_new = wl_labels.Wl_Label_Html('', self.table)

                    left_new.tokens_raw = left_old.tokens_raw.copy()
                    node_new.tokens_raw = node_old.tokens_raw.copy()
                    right_new.tokens_raw = right_old.tokens_raw.copy()

                    left_new.tokens_search = left_old.tokens_search.copy()
                    node_new.tokens_search = node_old.tokens_search.copy()
                    right_new.tokens_search = right_old.tokens_search.copy()

                    results[i][0] = left_new
                    results[i][1] = node_new
                    results[i][2] = right_new

                # Sort results
                for sorting_col, sorting_order in reversed(self.settings['sorting_rules']):
                    reverse = 0 if sorting_order == self.tr('Ascending') else 1

                    if sorting_col == self.tr('Node'):
                        results.sort(key = lambda item: item[1].tokens_raw, reverse = reverse)
                    # Sort first by type (strings after floats), then sort numerically or alphabetically
                    elif sorting_col == self.tr('Sentiment'):
                        results.sort(key = lambda item: (str(type(item[3])), item[3]), reverse = reverse)
                    elif sorting_col == self.tr('Token No.'):
                        results.sort(key = lambda item: item[4], reverse = reverse)
                    elif sorting_col == self.tr('Sentence Segment No.'):
                        results.sort(key = lambda item: item[6], reverse = reverse)
                    elif sorting_col == self.tr('Sentence No.'):
                        results.sort(key = lambda item: item[8], reverse = reverse)
                    elif sorting_col == self.tr('Paragraph No.'):
                        results.sort(key = lambda item: item[10], reverse = reverse)
                    elif sorting_col == self.tr('File'):
                        results.sort(key = lambda item: item[12], reverse = reverse)
                    else:
                        span = int(sorting_col[1:])

                        if RE_SORTING_COL_L.search(sorting_col):
                            results.sort(key = lambda item, span = span: item[0].tokens_raw[-span], reverse = reverse)
                        elif RE_SORTING_COL_R.search(sorting_col):
                            results.sort(key = lambda item, span = span: item[2].tokens_raw[span - 1], reverse = reverse)

                # Clear highlights before sorting the results
                self.table.dialog_results_search.clr_highlights()

                self.table.disable_updates()

                color_settings = self.main.settings_custom['tables']['concordancer']['sorting_settings']['highlight_colors']
                highlight_colors = [
                    color_settings['lvl_1'],
                    color_settings['lvl_2'],
                    color_settings['lvl_3'],
                    color_settings['lvl_4'],
                    color_settings['lvl_5'],
                    color_settings['lvl_6']
                ]

                re_node_color = re.compile(r'(?<=color: )#[0-9A-Za-z]{6}(?=;)')

                for row, (
                    left, node, right, sentiment,
                    no_token, no_token_pct,
                    no_sentence_seg, no_sentence_seg_pct,
                    no_sentence, no_sentence_pct,
                    no_para, no_para_pct,
                    file
                ) in enumerate(results):
                    # Remove empty tokens
                    text_left = [token for token in left.tokens_raw if token]
                    text_right = [token for token in right.tokens_raw if token]

                    # Re-apply node color
                    node_text = re_node_color.sub(color_settings['lvl_1'], node.text())

                    # Start from level 2 (level 1 applies to nodes)
                    i_highlight_color_left = 1
                    i_highlight_color_right = 1

                    for sorting_col, _ in self.settings['sorting_rules']:
                        if RE_SORTING_COL_L.search(sorting_col) and int(sorting_col[1:]) <= len(text_left):
                            hightlight_color = highlight_colors[i_highlight_color_left % len(highlight_colors)]

                            text_left[-int(sorting_col[1:])] = f'''
                                <span style="color: {hightlight_color}; font-weight: bold;">
                                    {text_left[-int(sorting_col[1:])]}
                                </span>
                            '''

                            i_highlight_color_left += 1
                        elif RE_SORTING_COL_R.search(sorting_col) and int(sorting_col[1:]) - 1 < len(text_right):
                            hightlight_color = highlight_colors[i_highlight_color_right % len(highlight_colors)]

                            text_right[int(sorting_col[1:]) - 1] = f'''
                                <span style="color: {hightlight_color}; font-weight: bold;">
                                    {text_right[int(sorting_col[1:]) - 1]}
                                </span>
                            '''

                            i_highlight_color_right += 1

                    self.table.indexWidget(self.table.model().index(row, 0)).setText(' '.join(text_left))
                    self.table.indexWidget(self.table.model().index(row, 1)).setText(node_text)
                    self.table.indexWidget(self.table.model().index(row, 2)).setText(' '.join(text_right))

                    self.table.indexWidget(self.table.model().index(row, 0)).tokens_raw = [token for token in left.tokens_raw if token]
                    self.table.indexWidget(self.table.model().index(row, 1)).tokens_raw = node.tokens_raw
                    self.table.indexWidget(self.table.model().index(row, 2)).tokens_raw = [token for token in right.tokens_raw if token]

                    self.table.indexWidget(self.table.model().index(row, 0)).tokens_search = left.tokens_search
                    self.table.indexWidget(self.table.model().index(row, 1)).tokens_search = node.tokens_search
                    self.table.indexWidget(self.table.model().index(row, 2)).tokens_search = right.tokens_search

                    if sentiment is not None:
                        if isinstance(sentiment, float):
                            self.table.set_item_num(row, 3, sentiment)
                        # No language support
                        else:
                            self.table.set_item_err(row, 3, text = sentiment, alignment_hor = 'right')

                        col_no_token = 4
                    else:
                        col_no_token = 3

                    self.table.set_item_num_val(row, col_no_token, no_token)
                    self.table.set_item_num_val(row, col_no_token + 1, no_token_pct)
                    self.table.set_item_num_val(row, col_no_token + 2, no_sentence_seg)
                    self.table.set_item_num_val(row, col_no_token + 3, no_sentence_seg_pct)
                    self.table.set_item_num_val(row, col_no_token + 4, no_sentence)
                    self.table.set_item_num_val(row, col_no_token + 5, no_sentence_pct)
                    self.table.set_item_num_val(row, col_no_token + 6, no_para)
                    self.table.set_item_num_val(row, col_no_token + 7, no_para_pct)
                    self.table.model().item(row, col_no_token + 8).setText(file)

                self.table.enable_updates(emit_signals = False)

                self.main.statusBar().showMessage(self.tr('The results in the data table has been successfully sorted.'))
            except Exception:
                wl_checks_work_area.check_err(self.main, traceback.format_exc())

class Wl_Table_Results_Sort_Conordancer(wl_tables.Wl_Table_Add_Ins_Del_Clr):
    def __init__(self, parent, table):
        super().__init__(
            parent = parent,
            headers = [
                _tr('Wl_Table_Results_Sort_Conordancer', 'Column'),
                _tr('Wl_Table_Results_Sort_Conordancer', 'Order')
            ],
            col_edit = 0
        )

        self.tab = table.tab
        self.table = table
        self.settings = self.table.settings[self.tab]

        self.cols_to_sort_default = [
            self.tr('Node'),
            self.tr('Token No.'),
            self.tr('Sentence Segment No.'),
            self.tr('Sentence No.'),
            self.tr('Paragraph No.'),
            self.tr('File')
        ]

        self.cols_to_sort = self.cols_to_sort_default.copy()

        self.setItemDelegateForColumn(1, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
            parent = self,
            items = [
                self.tr('Ascending'),
                self.tr('Descending')
            ]
        ))

        self.button_clr.hide()

        self.table.model().itemChanged.connect(self.table_item_changed)

    def item_changed(self, item): # pylint: disable=arguments-differ
        # Check for duplicates
        if item.column() == 0:
            for i in range(self.model().rowCount()):
                if i != item.row() and self.model().item(i, 0).text() == item.text():
                    QMessageBox.warning(
                        self.main,
                        self.tr('Column Sorted More Than Once'),
                        self.main.settings_global['styles']['style_dialog']
                        + self.tr('''
                            <body>
                                <div>Please refrain from sorting the same column more than once!</div>
                            </body>
                        '''),
                        QMessageBox.Ok
                    )

                    item.setText(item.text_old)

                    self.closeEditor(self.findChild(QComboBox), QAbstractItemDelegate.NoHint)
                    self.edit(item.index())

                    break

            item.text_old = item.text()

        if not self.is_empty():
            sorting_rules = [
                [
                    self.model().item(i, 0).text(),
                    self.model().item(i, 1).text()
                ]
                for i in range(self.model().rowCount())
            ]
        else:
            sorting_rules = []

        self.main.settings_custom[self.tab]['sort_results']['sorting_rules'] = sorting_rules

        if self.model().rowCount() < len(self.cols_to_sort):
            self.button_add.setEnabled(True)
        else:
            self.button_add.setEnabled(False)

        super().item_changed()

    def selection_changed(self):
        if self.selectionModel().selectedIndexes() and self.model().rowCount() < len(self.cols_to_sort):
            self.button_ins.setEnabled(True)
        else:
            self.button_ins.setEnabled(False)

        if self.selectionModel().selectedIndexes() and len(self.get_selected_rows()) < self.model().rowCount():
            self.button_del.setEnabled(True)
        else:
            self.button_del.setEnabled(False)

    def table_item_changed(self):
        # Columns to sort
        if not self.table.is_empty():
            self.cols_to_sort = self.cols_to_sort_default.copy()

            if self.settings['generation_settings']['calc_sentiment_scores']:
                self.cols_to_sort.insert(1, self.tr('Sentiment'))

            if self.settings['generation_settings']['context_len_unit'] == self.tr('Token'):
                context_len_left = self.settings['generation_settings']['context_len_left_token']
                context_len_right = self.settings['generation_settings']['context_len_right_token']
            else:
                context_len_left = max((
                    len(self.table.indexWidget(self.table.model().index(row, 0)).tokens_raw)
                    for row in range(self.table.model().rowCount())
                ))
                context_len_right = max((
                    len(self.table.indexWidget(self.table.model().index(row, 2)).tokens_raw)
                    for row in range(self.table.model().rowCount())
                ))

            # List right context before left context
            self.cols_to_sort.extend([self.tr('R{}').format(i + 1) for i in range(context_len_right)])
            self.cols_to_sort.extend([self.tr('L{}').format(i + 1) for i in range(context_len_left)])

            self.setItemDelegateForColumn(0, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
                parent = self,
                items = self.cols_to_sort
            ))

            # Check sorting settings
            sorting_rules_old = copy.deepcopy(self.main.settings_custom[self.tab]['sort_results']['sorting_rules'])

            self.clr_table(0)

            for sorting_col, sorting_order in sorting_rules_old:
                if sorting_col in self.cols_to_sort:
                    self._add_row(texts = [sorting_col, sorting_order])

            if self.model().rowCount() == 0:
                self.load_settings(defaults = True)

            self.clearSelection()

    def max_left(self):
        if self.tr('L1') in self.cols_to_sort:
            max_left = max((
                int(col[1:])
                for col in self.cols_to_sort
                if RE_SORTING_COL_L.search(col)
            ))
        else:
            max_left = 0

        return max_left

    def max_right(self):
        if self.tr('R1') in self.cols_to_sort:
            max_right = max((
                int(col[1:])
                for col in self.cols_to_sort
                if RE_SORTING_COL_R.search(col)
            ))
        else:
            max_right = 0

        return max_right

    def _add_row(self, row = None, texts = None):
        if texts is None:
            sorting_col = ''
            sorting_order = ''
        else:
            sorting_col = texts[0]
            sorting_order = texts[1]

        # Column
        item_sorting_col = QStandardItem()

        max_left = self.max_left()
        max_right = self.max_right()

        cols_left = sorted([
            int(self.model().item(i, 0).text()[1:])
            for i in range(self.model().rowCount())
            if RE_SORTING_COL_L.search(self.model().item(i, 0).text())
        ])
        cols_right = sorted([
            int(self.model().item(i, 0).text()[1:])
            for i in range(self.model().rowCount())
            if RE_SORTING_COL_R.search(self.model().item(i, 0).text())
        ])

        if sorting_col:
            item_sorting_col.setText(sorting_col)
        else:
            if cols_left and max(cols_left) < max_left:
                item_sorting_col.setText(self.tr('L{}').format(cols_left[-1] + 1))
            elif cols_right and max(cols_right) < max_right:
                item_sorting_col.setText(self.tr('R{}').format(cols_right[-1] + 1))
            elif cols_right and max(cols_right) == max_right and not cols_left:
                item_sorting_col.setText(self.tr('L1'))
            else:
                sorting_cols = [self.model().item(i, 0).text() for i in range(self.model().rowCount())]

                for col in self.cols_to_sort:
                    if col not in sorting_cols:
                        item_sorting_col.setText(col)

                        break

        # Order
        item_sorting_order = QStandardItem()

        if sorting_order:
            item_sorting_order.setText(sorting_order)
        else:
            item_sorting_order.setText(self.tr('Ascending'))

        item_sorting_col.text_old = item_sorting_col.text()
        item_sorting_order.text_old = item_sorting_order.text()

        if row is None:
            self.model().appendRow([
                item_sorting_col,
                item_sorting_order
            ])
        else:
            self.model().insertRow(row, [
                item_sorting_col,
                item_sorting_order
            ])

        self.model().itemChanged.emit(QStandardItem())

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['sort_results'])
        else:
            settings = copy.deepcopy(self.main.settings_custom[self.tab]['sort_results'])

        self.clr_table(0)

        for sorting_rule in settings['sorting_rules']:
            self._add_row(texts = sorting_rule)

class Wl_Worker_Results_Sort_Concordancer(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, list)

    def run(self):
        err_msg = ''
        results = []

        try:
            max_left = self.dialog.table_sort.max_left()
            max_right = self.dialog.table_sort.max_right()

            calc_sentiment_scores = self.dialog.table.settings['concordancer']['generation_settings']['calc_sentiment_scores']

            for row in range(self.dialog.table.model().rowCount()):
                left_old = self.dialog.table.indexWidget(self.dialog.table.model().index(row, 0))
                node_old = self.dialog.table.indexWidget(self.dialog.table.model().index(row, 1))
                right_old = self.dialog.table.indexWidget(self.dialog.table.model().index(row, 2))

                if len(left_old.tokens_raw) < max_left:
                    left_old.tokens_raw = [''] * (max_left - len(left_old.tokens_raw)) + left_old.tokens_raw
                if len(right_old.tokens_raw) < max_right:
                    right_old.tokens_raw.extend([''] * (max_right - len(right_old.tokens_raw)))

                if calc_sentiment_scores:
                    sentiment = self.dialog.table.model().item(row, 3).read_data()

                    i_no_token = 4
                else:
                    sentiment = None

                    i_no_token = 3

                no_token = self.dialog.table.model().item(row, i_no_token).val
                no_token_pct = self.dialog.table.model().item(row, i_no_token + 1).val
                no_sentence_seg = self.dialog.table.model().item(row, i_no_token + 2).val
                no_sentence_seg_pct = self.dialog.table.model().item(row, i_no_token + 3).val
                no_sentence = self.dialog.table.model().item(row, i_no_token + 4).val
                no_sentence_pct = self.dialog.table.model().item(row, i_no_token + 5).val
                no_para = self.dialog.table.model().item(row, i_no_token + 6).val
                no_para_pct = self.dialog.table.model().item(row, i_no_token + 7).val
                file = self.dialog.table.model().item(row, i_no_token + 8).text()

                results.append([
                    left_old, node_old, right_old, sentiment,
                    no_token, no_token_pct,
                    no_sentence_seg, no_sentence_seg_pct,
                    no_sentence, no_sentence_pct,
                    no_para, no_para_pct,
                    file
                ])

                self.progress_updated.emit(self.tr('Updating table...'))
        except Exception:
            err_msg = traceback.format_exc()
        finally:
            self.worker_done.emit(err_msg, results)
