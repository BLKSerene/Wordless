# ----------------------------------------------------------------------
# Wordless: Results - Sort
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
import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_dialogs, wl_dialogs_misc
from wl_utils import wl_misc, wl_threading
from wl_widgets import wl_buttons, wl_item_delegates, wl_labels, wl_layouts, wl_tables

_tr = QCoreApplication.translate

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

        self.table = table

        if self.table.tab == 'concordancer':
            self.cols_to_sort_default = [
                self.tr('Node'),
                self.tr('Sentiment'),
                self.tr('Token No.'),
                self.tr('File')
            ]
        elif self.table.tab == 'concordancer_parallel':
            self.cols_to_sort_default = [
                self.tr('Node'),
                self.tr('Segment No.')
            ]

        self.cols_to_sort = self.cols_to_sort_default.copy()

        self.setFixedWidth(400)
        self.setFixedHeight(200)

        self.setItemDelegateForColumn(1, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
            parent = self,
            items = [
                self.tr('Ascending'),
                self.tr('Descending')
            ]
        ))

        self.button_clr.hide()

        self.table.model().itemChanged.connect(self.table_item_changed)

    def item_changed(self, item):
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

        self.main.settings_custom[self.table.tab]['sort_results']['sorting_rules'] = sorting_rules

        if self.model().rowCount() < len(self.cols_to_sort):
            self.button_add.setEnabled(True)
        else:
            self.button_add.setEnabled(False)

        super().item_changed(item)

    def selection_changed(self, selected, deselected):
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

            if self.table.tab == 'concordancer':
                if self.table.settings['concordancer']['generation_settings']['width_unit'] == self.tr('Token'):
                    width_left = self.table.settings['concordancer']['generation_settings']['width_left_token']
                    width_right = self.table.settings['concordancer']['generation_settings']['width_right_token']
                else:
                    width_left = max([
                        len(self.table.indexWidget(self.table.model().index(row, 0)).text_raw)
                        for row in range(self.table.model().rowCount())
                    ])
                    width_right = max([
                        len(self.table.indexWidget(self.table.model().index(row, 2)).text_raw)
                        for row in range(self.table.model().rowCount())
                    ])

                self.cols_to_sort.extend([self.tr('R') + str(i + 1) for i in range(width_right)])
                self.cols_to_sort.extend([self.tr('L') + str(i + 1) for i in range(width_left)])
            elif self.table.tab == 'concordancer_parallel':
                width_left = max([
                    len(self.table.indexWidget(self.table.model().index(row, 0)).text_raw)
                    for row in range(self.table.model().rowCount())
                ])
                width_right = max([
                    len(self.table.indexWidget(self.table.model().index(row, 2)).text_raw)
                    for row in range(self.table.model().rowCount())
                ])

                self.cols_to_sort.extend([self.tr('R') + str(i + 1) for i in range(width_right)])
                self.cols_to_sort.extend([self.tr('L') + str(i + 1) for i in range(width_left)])

        self.setItemDelegateForColumn(0, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
            parent = self,
            items = self.cols_to_sort
        ))

        # Check sorting settings
        self.clr_table(0)
        self.disable_updates()

        for sorting_col, sorting_order in self.main.settings_custom[self.table.tab]['sort_results']['sorting_rules']:
            if sorting_col in self.cols_to_sort:
                self.add_row()

                self.model().item(self.model().rowCount() - 1, 0).setText(sorting_col)
                self.model().item(self.model().rowCount() - 1, 1).setText(sorting_order)

        self.enable_updates()

        if self.model().rowCount() == 0:
            self.load_settings(defaults = True)

        self.clearSelection()

    def max_left(self):
        if self.tr('L1') in self.cols_to_sort:
            max_left = max([
                int(col[1:])
                for col in self.cols_to_sort
                if re.search(self.tr(r'^L[0-9]+$'), col)
            ])
        else:
            max_left = 0

        return max_left

    def max_right(self):
        if self.tr('R1') in self.cols_to_sort:
            max_right = max([
                int(col[1:])
                for col in self.cols_to_sort
                if re.search(self.tr(r'^R[0-9]+$'), col)
            ])
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
            if re.search(self.tr(r'^L[0-9]+$'), self.model().item(i, 0).text())
        ])
        cols_right = sorted([
            int(self.model().item(i, 0).text()[1:])
            for i in range(self.model().rowCount())
            if re.search(self.tr(r'^R[0-9]+$'), self.model().item(i, 0).text())
        ])

        if sorting_col:
            item_sorting_col.setText(sorting_col)
        else:
            if cols_left and max(cols_left) < max_left:
                item_sorting_col.setText(self.tr('L') + str(cols_left[-1] + 1))
            elif cols_right and max(cols_right) < max_right:
                item_sorting_col.setText(self.tr('R') + str(cols_right[-1] + 1))
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
            settings = copy.deepcopy(self.main.settings_default[self.table.tab]['sort_results'])
        else:
            settings = copy.deepcopy(self.main.settings_custom[self.table.tab]['sort_results'])

        self.clr_table(0)

        for sorting_rule in settings['sorting_rules']:
            self._add_row(texts = sorting_rule)

class Wl_Worker_Results_Sort_Concordancer(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(list)

    def run(self):
        results = []

        max_left = self.dialog.table_sort.max_left()
        max_right = self.dialog.table_sort.max_right()

        for i in range(self.dialog.tables[0].model().rowCount()):
            left_old = self.dialog.tables[0].indexWidget(self.dialog.tables[0].model().index(i, 0))
            node_old = self.dialog.tables[0].indexWidget(self.dialog.tables[0].model().index(i, 1))
            right_old = self.dialog.tables[0].indexWidget(self.dialog.tables[0].model().index(i, 2))

            if len(left_old.text_raw) < max_left:
                left_old.text_raw = [''] * (max_left - len(left_old.text_raw)) + left_old.text_raw
            if len(right_old.text_raw) < max_right:
                right_old.text_raw.extend([''] * (max_right - len(right_old.text_raw)))

            sentiment = self.dialog.tables[0].model().item(i, 3).read_data()
            no_token = self.dialog.tables[0].model().item(i, 4).val
            no_token_pct = self.dialog.tables[0].model().item(i, 5).val
            no_sentence = self.dialog.tables[0].model().item(i, 6).val
            no_sentence_pct = self.dialog.tables[0].model().item(i, 7).val
            no_para = self.dialog.tables[0].model().item(i, 8).val
            no_para_pct = self.dialog.tables[0].model().item(i, 9).val
            file = self.dialog.tables[0].model().item(i, 10).text()

            results.append([
                left_old, node_old, right_old,
                sentiment,
                no_token, no_token_pct,
                no_sentence, no_sentence_pct,
                no_para, no_para_pct,
                file
            ])

        self.progress_updated.emit(self.tr('Updating table...'))
        self.worker_done.emit(results)

class Wl_Worker_Results_Sort_Concordancer_Parallel(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(list, list)

    def run(self):
        results_src = []
        results_tgt = []

        table_src = self.dialog.tables[0]
        table_tgt = self.dialog.tables[1]

        # Source text
        max_left = self.dialog.table_sort.max_left()
        max_right = self.dialog.table_sort.max_right()

        for i in range(table_src.model().rowCount()):
            left_old = table_src.indexWidget(table_src.model().index(i, 0))
            node_old = table_src.indexWidget(table_src.model().index(i, 1))
            right_old = table_src.indexWidget(table_src.model().index(i, 2))

            if len(left_old.text_raw) < max_left:
                left_old.text_raw = [''] * (max_left - len(left_old.text_raw)) + left_old.text_raw
            if len(right_old.text_raw) < max_right:
                right_old.text_raw.extend([''] * (max_right - len(right_old.text_raw)))

            no_seg = table_src.model().item(i, 3).val
            no_seg_pct = table_src.model().item(i, 4).val

            results_src.append([
                left_old, node_old, right_old,
                no_seg, no_seg_pct,
            ])

        # Target text
        for i in range(table_tgt.model().rowCount()):
            parallel_text_old = table_tgt.indexWidget(table_tgt.model().index(i, 0))

            no_seg = table_tgt.model().item(i, 1).val
            no_seg_pct = table_tgt.model().item(i, 2).val

            results_tgt.append([
                parallel_text_old,
                no_seg, no_seg_pct,
            ])

        self.progress_updated.emit(self.tr('Updating table...'))
        self.worker_done.emit(results_src, results_tgt)

class Wl_Dialog_Results_Sort_Concordancer(wl_dialogs.Wl_Dialog):
    def __init__(self, main, table):
        super().__init__(main, _tr('Wl_Dialog_Results_Sort_Concordancer', 'Sort Results'))

        self.tables = [table]
        self.settings = self.main.settings_custom[self.tables[0].tab]['sort_results']

        self.main.wl_work_area.currentChanged.connect(self.reject)

        self.table_sort = Wl_Table_Results_Sort_Conordancer(self, table = self.tables[0])

        self.button_restore_default_settings = wl_buttons.Wl_Button_Restore_Default_Settings(self, load_settings = self.load_settings)
        self.button_sort = QPushButton(self.tr('Sort'), self)
        self.button_close = QPushButton(self.tr('Close'), self)

        if self.tables[0].tab == 'concordancer':
            self.button_sort.clicked.connect(lambda: self.sort_results())
        elif self.tables[0].tab == 'concordancer_parallel':
            self.button_sort.clicked.connect(lambda: self.sort_results_parallel())

        self.button_close.clicked.connect(self.reject)

        layout_table_sort = wl_layouts.Wl_Layout()
        layout_table_sort.addWidget(self.table_sort, 0, 0, 5, 1)
        layout_table_sort.addWidget(self.table_sort.button_add, 0, 1)
        layout_table_sort.addWidget(self.table_sort.button_ins, 1, 1)
        layout_table_sort.addWidget(self.table_sort.button_del, 2, 1)
        layout_table_sort.addWidget(self.table_sort.button_clr, 3, 1)

        layout_table_sort.setRowStretch(4, 1)

        layout_buttons = wl_layouts.Wl_Layout()
        layout_buttons.addWidget(self.button_restore_default_settings, 0, 0)
        layout_buttons.addWidget(self.button_sort, 0, 2)
        layout_buttons.addWidget(self.button_close, 0, 3)

        layout_buttons.setColumnStretch(1, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addLayout(layout_table_sort, 0, 0)

        self.layout().addWidget(wl_layouts.Wl_Separator(self), 1, 0)
        self.layout().addLayout(layout_buttons, 2, 0)

        self.set_fixed_size()

    def add_tables(self, tables):
        self.tables.extend(tables)

    # To be called by "Restore Default Settings"
    def load_settings(self, defaults = False):
        self.table_sort.load_settings(defaults = defaults)

    @wl_misc.log_timing
    def sort_results(self):
        def update_gui(results):
            # Create new labels
            for i, (
                left_old, node_old, right_old,
                _, _, _, _, _, _, _, _
            ) in enumerate(results):
                left_new = wl_labels.Wl_Label_Html('', self.tables[0])
                node_new = wl_labels.Wl_Label_Html(node_old.text(), self.tables[0])
                right_new = wl_labels.Wl_Label_Html('', self.tables[0])

                left_new.text_raw = left_old.text_raw.copy()
                node_new.text_raw = node_old.text_raw.copy()
                right_new.text_raw = right_old.text_raw.copy()

                left_new.text_search = left_old.text_search.copy()
                node_new.text_search = node_old.text_search.copy()
                right_new.text_search = right_old.text_search.copy()

                results[i][0] = left_new
                results[i][1] = node_new
                results[i][2] = right_new

            # Sort results
            for sorting_col, sorting_order in reversed(self.settings['sorting_rules']):
                reverse = 0 if sorting_order == self.tr('Ascending') else 1

                if sorting_col == self.tr('Node'):
                    results.sort(key = lambda item: item[1].text_raw, reverse = reverse)
                # Sort first by type (strings after floats), then sort numerically or alphabetically
                elif sorting_col == self.tr('Sentiment'):
                    results.sort(key = lambda item: (str(type(item[3])), item[3]), reverse = reverse)
                elif sorting_col == self.tr('Token No.'):
                    results.sort(key = lambda item: item[4], reverse = reverse)
                elif sorting_col == self.tr('File'):
                    results.sort(key = lambda item: item[10], reverse = reverse)
                else:
                    span = int(sorting_col[1:])

                    if re.search(r'^L[0-9]+$', sorting_col):
                        results.sort(key = lambda item: item[0].text_raw[-span], reverse = reverse)
                    elif re.search(r'^R[0-9]+$', sorting_col):
                        results.sort(key = lambda item: item[2].text_raw[span - 1], reverse = reverse)

            self.tables[0].disable_updates()

            for i, (
                left, node, right,
                sentiment,
                no_token, no_token_pct,
                no_sentence, no_sentence_pct,
                no_para, no_para_pct,
                file
            ) in enumerate(results):
                # Remove empty tokens
                text_left = [token for token in left.text_raw if token]
                text_right = [token for token in right.text_raw if token]

                highlight_colors = self.main.settings_custom['concordancer']['sort_results']['highlight_colors']

                i_highlight_color_left = 1
                i_highlight_color_right = 1

                for sorting_col, _ in self.settings['sorting_rules']:
                    if re.search(self.tr(r'^L[0-9]+$'), sorting_col) and int(sorting_col[1:]) <= len(text_left):
                        hightlight_color = highlight_colors[i_highlight_color_left % len(highlight_colors)]

                        text_left[-int(sorting_col[1:])] = f'''
                            <span style="color: {hightlight_color}; font-weight: bold;">
                                {text_left[-int(sorting_col[1:])]}
                            </span>
                        '''

                        i_highlight_color_left += 1
                    elif re.search(self.tr(r'^R[0-9]+$'), sorting_col) and int(sorting_col[1:]) - 1 < len(text_right):
                        hightlight_color = highlight_colors[i_highlight_color_right % len(highlight_colors)]

                        text_right[int(sorting_col[1:]) - 1] = f'''
                            <span style="color: {hightlight_color}; font-weight: bold;">
                                {text_right[int(sorting_col[1:]) - 1]}
                            </span>
                        '''

                        i_highlight_color_right += 1

                self.tables[0].indexWidget(self.tables[0].model().index(i, 0)).setText(' '.join(text_left))
                self.tables[0].indexWidget(self.tables[0].model().index(i, 1)).setText(node.text())
                self.tables[0].indexWidget(self.tables[0].model().index(i, 2)).setText(' '.join(text_right))

                self.tables[0].indexWidget(self.tables[0].model().index(i, 0)).text_raw = [token for token in left.text_raw if token]
                self.tables[0].indexWidget(self.tables[0].model().index(i, 1)).text_raw = node.text_raw
                self.tables[0].indexWidget(self.tables[0].model().index(i, 2)).text_raw = [token for token in right.text_raw if token]

                self.tables[0].indexWidget(self.tables[0].model().index(i, 0)).text_search = left.text_search
                self.tables[0].indexWidget(self.tables[0].model().index(i, 1)).text_search = node.text_search
                self.tables[0].indexWidget(self.tables[0].model().index(i, 2)).text_search = right.text_search

                if isinstance(sentiment, float):
                    self.tables[0].set_item_num(i, 3, sentiment)
                # No Support
                else:
                    self.tables[0].set_item_error(i, 3, text = sentiment)

                self.tables[0].set_item_num_val(i, 4, no_token)
                self.tables[0].set_item_num_val(i, 5, no_token_pct)
                self.tables[0].set_item_num_val(i, 6, no_sentence)
                self.tables[0].set_item_num_val(i, 7, no_sentence_pct)
                self.tables[0].set_item_num_val(i, 8, no_para)
                self.tables[0].set_item_num_val(i, 9, no_para_pct)
                self.tables[0].model().item(i, 10).setText(file)

            self.tables[0].enable_updates(emit_signals = False)

        if not self.tables[0].is_empty():
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = self.tr('Sorting results...'))

            worker_results_sort_concordancer = Wl_Worker_Results_Sort_Concordancer(
                self.main,
                dialog_progress = dialog_progress,
                update_gui = update_gui,
                dialog = self
            )

            thread_results_sort_concordancer = wl_threading.Wl_Thread(worker_results_sort_concordancer)
            thread_results_sort_concordancer.start_worker()

        self.main.statusBar().showMessage(self.tr('The results in the table has been successfully sorted.'))

    @wl_misc.log_timing
    def sort_results_parallel(self):
        def update_gui(results_src, results_tgt):
            results = []

            # Create new labels
            for (
                (
                    left_old, node_old, right_old,
                    no_seg_src, no_seg_pct_src
                ),
                (
                    parallel_text_old,
                    no_seg_tgt, no_seg_pct_tgt
                )
            ) in zip(results_src, results_tgt):
                left_new = wl_labels.Wl_Label_Html('', self.tables[0])
                node_new = wl_labels.Wl_Label_Html(node_old.text(), self.tables[0])
                right_new = wl_labels.Wl_Label_Html('', self.tables[0])
                parallel_text_new = wl_labels.Wl_Label_Html(parallel_text_old.text(), self.tables[1])

                left_new.text_raw = left_old.text_raw.copy()
                node_new.text_raw = node_old.text_raw.copy()
                right_new.text_raw = right_old.text_raw.copy()
                parallel_text_new.text_raw = parallel_text_old.text_raw.copy()

                left_new.text_search = left_old.text_search.copy()
                node_new.text_search = node_old.text_search.copy()
                right_new.text_search = right_old.text_search.copy()
                parallel_text_new.text_search = parallel_text_old.text_search.copy()

                results.append([
                    (
                        left_new, node_new, right_new,
                        no_seg_src, no_seg_pct_src
                    ),
                    (
                        parallel_text_new,
                        no_seg_tgt, no_seg_pct_tgt
                    )
                ])

            # Sort results
            for sorting_col, sorting_order in reversed(self.settings['sorting_rules']):
                reverse = 0 if sorting_order == self.tr('Ascending') else 1

                if sorting_col == self.tr('Node'):
                    results.sort(key = lambda item: item[0][1].text_raw, reverse = reverse)
                elif sorting_col == self.tr('Segment No.'):
                    results.sort(key = lambda item: item[0][3], reverse = reverse)
                else:
                    span = int(sorting_col[1:])

                    if self.tr('L') in sorting_col:
                        results.sort(key = lambda item: item[0][0].text_raw[-span], reverse = reverse)
                    elif self.tr('R') in sorting_col:
                        results.sort(key = lambda item: item[0][2].text_raw[span - 1], reverse = reverse)

            self.tables[0].disable_updates()
            self.tables[1].disable_updates()

            for i, (
                (
                    left, node, right,
                    no_seg_src, no_seg_pct_src
                ),
                (
                    parallel_text,
                    no_seg_tgt, no_seg_pct_tgt
                )
            ) in enumerate(results):
                # Remove empty tokens
                text_left = [token for token in left.text_raw if token]
                text_right = [token for token in right.text_raw if token]

                highlight_colors = self.main.settings_custom['concordancer']['sort_results']['highlight_colors']

                i_highlight_color_left = 1
                i_highlight_color_right = 1

                for sorting_col, _ in self.settings['sorting_rules']:
                    if re.search(self.tr(r'^L[0-9]+$'), sorting_col) and int(sorting_col[1:]) <= len(text_left):
                        hightlight_color = highlight_colors[i_highlight_color_left % len(highlight_colors)]

                        text_left[-int(sorting_col[1:])] = f'''
                            <span style="color: {hightlight_color}; font-weight: bold;">
                                {text_left[-int(sorting_col[1:])]}
                            </span>
                        '''

                        i_highlight_color_left += 1
                    elif re.search(self.tr(r'^R[0-9]+$'), sorting_col) and int(sorting_col[1:]) - 1 < len(text_right):
                        hightlight_color = highlight_colors[i_highlight_color_right % len(highlight_colors)]

                        text_right[int(sorting_col[1:]) - 1] = f'''
                            <span style="color: {hightlight_color}; font-weight: bold;">
                                {text_right[int(sorting_col[1:]) - 1]}
                            </span>
                        '''

                        i_highlight_color_right += 1

                self.tables[0].indexWidget(self.tables[0].model().index(i, 0)).setText(' '.join(text_left))
                self.tables[0].indexWidget(self.tables[0].model().index(i, 1)).setText(node.text())
                self.tables[0].indexWidget(self.tables[0].model().index(i, 2)).setText(' '.join(text_right))

                self.tables[0].indexWidget(self.tables[0].model().index(i, 0)).text_raw = [token for token in left.text_raw if token]
                self.tables[0].indexWidget(self.tables[0].model().index(i, 1)).text_raw = node.text_raw
                self.tables[0].indexWidget(self.tables[0].model().index(i, 2)).text_raw = [token for token in right.text_raw if token]

                self.tables[0].indexWidget(self.tables[0].model().index(i, 0)).text_search = left.text_search
                self.tables[0].indexWidget(self.tables[0].model().index(i, 1)).text_search = node.text_search
                self.tables[0].indexWidget(self.tables[0].model().index(i, 2)).text_search = right.text_search

                self.tables[0].set_item_num_val(i, 3, no_seg_src)
                self.tables[0].set_item_num_val(i, 4, no_seg_pct_src)

                self.tables[1].indexWidget(self.tables[1].model().index(i, 0)).setText(parallel_text.text())

                self.tables[1].indexWidget(self.tables[1].model().index(i, 0)).text_raw = [token for token in parallel_text.text_raw if token]
                self.tables[1].indexWidget(self.tables[1].model().index(i, 0)).text_search = parallel_text.text_search

                self.tables[1].set_item_num_val(i, 1, no_seg_tgt)
                self.tables[1].set_item_num_val(i, 2, no_seg_pct_tgt)

            self.tables[0].enable_updates(emit_signals = False)
            self.tables[1].enable_updates(emit_signals = False)

        if not self.tables[0].is_empty():
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = self.tr('Sorting results...'))

            worker_results_sort_concordancer_parallel = Wl_Worker_Results_Sort_Concordancer_Parallel(
                self.main,
                dialog_progress = dialog_progress,
                update_gui = update_gui,
                dialog = self
            )

            thread_results_sort_concordancer_parallel = wl_threading.Wl_Thread(worker_results_sort_concordancer_parallel)
            thread_results_sort_concordancer_parallel.start_worker()

        self.main.statusBar().showMessage(self.tr('The results in the table has been successfully sorted.'))
