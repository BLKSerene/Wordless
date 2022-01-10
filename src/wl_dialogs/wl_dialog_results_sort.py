# ----------------------------------------------------------------------
# Wordless: Dialogs - Sort Results
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
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_dialog, wl_dialog_misc
from wl_text import wl_word_detokenization
from wl_utils import wl_misc, wl_threading
from wl_widgets import (
    wl_box, wl_button, wl_label, wl_layout, wl_msg, wl_table
)

class Wl_Combo_Box_Sorting_Col(wl_box.Wl_Combo_Box):
    def __init__(self, table_sort):
        super().__init__(table_sort)

        self.table_sort = table_sort

        self.addItems(self.table_sort.cols_to_sort)

        if self.findText('L1') > -1:
            width_left = max([
                int(self.itemText(i)[1:])
                for i in range(self.count())
                if re.search(r'^L[0-9]+?$', self.itemText(i))
            ])
        else:
            width_left = 0

        if self.findText('R1') > -1:
            width_right = max([
                int(self.itemText(i)[1:])
                for i in range(self.count())
                if re.search(r'^R[0-9]+?$', self.itemText(i))
            ])
        else:
            width_right = 0

        cols_left = [
            int(self.table_sort.cellWidget(i, 0).currentText()[1:])
            for i in range(self.table_sort.rowCount())
            if re.search(r'^L[0-9]+?$', self.table_sort.cellWidget(i, 0).currentText())
        ]
        cols_right = [
            int(self.table_sort.cellWidget(i, 0).currentText()[1:])
            for i in range(self.table_sort.rowCount())
            if re.search(r'^R[0-9]+?$', self.table_sort.cellWidget(i, 0).currentText())
        ]

        if cols_left and max(cols_left) < width_left:
            self.setCurrentText(f'L{cols_left[-1] + 1}')
        elif cols_right and max(cols_right) < width_right:
            self.setCurrentText(f'R{cols_right[-1] + 1}')
        elif cols_right and max(cols_right) and not cols_left:
            self.setCurrentText(f'L1')
        else:
            for i in range(self.count()):
                text = self.itemText(i)

                if text not in [self.table_sort.cellWidget(j, 0).currentText() for j in range(self.table_sort.rowCount())]:
                    self.setCurrentText(text)

                    break

class Wl_Combo_Box_Sorting_Order(wl_box.Wl_Combo_Box):
    def __init__(self, table_sort):
        super().__init__(table_sort)

        self.addItems([
            self.tr('Ascending'),
            self.tr('Descending')
        ])

    def get_text(self):
        return self.currentIndex()

    def set_text(self, index):
        self.setCurrentIndex(index)

class Wl_Table_Results_Sort_Conordancer(wl_table.Wl_Table):
    def __init__(self, parent, table):
        super().__init__(
            parent,
            headers = [
                parent.tr('Columns'),
                parent.tr('Order')
            ],
            cols_stretch = [
                parent.tr('Order')
            ]
        )

        self.table = table

        if self.table.tab == 'concordancer':
            self.cols_to_sort_default = [
                self.tr('Node'),
                self.tr('Token No.'),
                self.tr('File'),
                self.tr('Sentiment')
            ]
        elif self.table.tab == 'concordancer_parallel':
            self.cols_to_sort_default = [
                self.tr('Node'),
                self.tr('Segment No.')
            ]

        self.cols_to_sort = self.cols_to_sort_default.copy()

        self.button_add = QPushButton(self.tr('Add'), self)
        self.button_insert = QPushButton(self.tr('Insert'), self)
        self.button_remove = QPushButton(self.tr('Remove'), self)
    
        self.button_add.clicked.connect(self.add_row)
        self.button_insert.clicked.connect(self.insert_row)
        self.button_remove.clicked.connect(self.remove_row)

        self.itemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self.selection_changed)

        self.table.itemChanged.connect(self.table_item_changed)

    def item_changed(self):
        sorting_rules = []

        if self.cellWidget(0, 0):
            for i in range(self.rowCount()):
                sorting_rules.append([
                    self.cellWidget(i, 0).currentText(),
                    self.cellWidget(i, 1).get_text()
                ])

        self.main.settings_custom[self.table.tab]['sort_results']['sorting_rules'] = sorting_rules

        if self.rowCount() < len(self.cols_to_sort):
            self.button_add.setEnabled(True)
        else:
            self.button_add.setEnabled(False)

        for i in range(self.rowCount()):
            self.cellWidget(i, 0).text_old = self.cellWidget(i, 0).currentText()
        
        self.selection_changed()

    def selection_changed(self):
        if self.selectedIndexes() and self.rowCount() < len(self.cols_to_sort):
            self.button_insert.setEnabled(True)
        else:
            self.button_insert.setEnabled(False)

        if self.selectedIndexes() and len(self.get_selected_rows()) < self.rowCount():
            self.button_remove.setEnabled(True)
        else:
            self.button_remove.setEnabled(False)

    def table_item_changed(self):
        sorting_rules = copy.deepcopy(self.main.settings_custom[self.table.tab]['sort_results']['sorting_rules'])
        
        self.setRowCount(0)

        # Columns to sort
        self.cols_to_sort = self.cols_to_sort_default.copy()

        if [i for i in range(self.table.columnCount()) if self.table.item(0, i)]:
            if self.table.tab == 'concordancer':
                if self.table.settings['concordancer']['generation_settings']['width_unit'] == self.tr('Token'):
                    width_left = self.table.settings['concordancer']['generation_settings']['width_left_token']
                    width_right = self.table.settings['concordancer']['generation_settings']['width_right_token']
                else:
                    width_left = max([
                        len(self.table.cellWidget(row, 0).text_raw)
                        for row in range(self.table.rowCount())
                    ])
                    width_right = max([
                        len(self.table.cellWidget(row, 2).text_raw)
                        for row in range(self.table.rowCount())
                    ])

                self.cols_to_sort.extend([f'R{i + 1}' for i in range(width_right)])
                self.cols_to_sort.extend([f'L{i + 1}' for i in range(width_left)])
            elif self.table.tab == 'concordancer_parallel':
                width_left = max([
                    len(self.table.cellWidget(row, 0).text_raw)
                    for row in range(self.table.rowCount())
                ])
                width_right = max([
                    len(self.table.cellWidget(row, 2).text_raw)
                    for row in range(self.table.rowCount())
                ])

                self.cols_to_sort.extend([f'R{i + 1}' for i in range(width_right)])
                self.cols_to_sort.extend([f'L{i + 1}' for i in range(width_left)])

        # Check sorting settings
        for sorting_col, sorting_order in sorting_rules:
            if sorting_col in self.cols_to_sort:
                self.add_row()

                self.cellWidget(self.rowCount() - 1, 0).setCurrentText(sorting_col)
                self.cellWidget(self.rowCount() - 1, 1).set_text(sorting_order)

        if self.rowCount() == 0:
            self.load_settings(defaults = True)

        self.clearSelection()

        self.itemChanged.emit(self.item(0, 0))

    def sorting_col_changed(self, combo_box_sorting_col):
        for i in range(self.rowCount()):
            combo_box_cur = self.cellWidget(i, 0)

            if combo_box_sorting_col != combo_box_cur and combo_box_sorting_col.currentText() == combo_box_cur.currentText():
                QMessageBox.warning(
                    self.main,
                    self.tr('Column Sorted More Than Once'),
                    self.tr(f'''
                        {self.main.settings_global['styles']['style_dialog']}
                        <body>
                            <div>Please refrain from sorting the same column more than once!</div>
                        </body>
                    '''),
                    QMessageBox.Ok
                )

                combo_box_sorting_col.setCurrentText(combo_box_sorting_col.text_old)
                combo_box_sorting_col.showPopup()

                return

        combo_box_sorting_col.text_old = combo_box_sorting_col.currentText()

    def _new_row(self):
        combo_box_sorting_col = Wl_Combo_Box_Sorting_Col(self)
        combo_box_sorting_order = Wl_Combo_Box_Sorting_Order(self)

        combo_box_sorting_col.currentTextChanged.connect(lambda: self.sorting_col_changed(combo_box_sorting_col))
        combo_box_sorting_col.currentTextChanged.connect(lambda: self.itemChanged.emit(self.item(0, 0)))
        combo_box_sorting_order.currentTextChanged.connect(lambda: self.itemChanged.emit(self.item(0, 0)))

        return (combo_box_sorting_col, combo_box_sorting_order)

    def add_row(self):
        combo_box_sorting_col, combo_box_sorting_order = self._new_row()
        
        self.setRowCount(self.rowCount() + 1)
        self.setCellWidget(self.rowCount() - 1, 0, combo_box_sorting_col)
        self.setCellWidget(self.rowCount() - 1, 1, combo_box_sorting_order)

        self.selectRow(self.rowCount() - 1)

        self.itemChanged.emit(self.item(0, 0))

    def insert_row(self):
        row = self.get_selected_rows()[0]

        combo_box_sorting_col, combo_box_sorting_order = self._new_row()

        self.insertRow(row)

        self.setCellWidget(row, 0, combo_box_sorting_col)
        self.setCellWidget(row, 1, combo_box_sorting_order)

        self.selectRow(row)

        self.itemChanged.emit(self.item(0, 0))

    def remove_row(self):
        for i in reversed(self.get_selected_rows()):
            self.removeRow(i)

        self.itemChanged.emit(self.item(0, 0))

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.table.tab]['sort_results'])
        else:
            settings = copy.deepcopy(self.main.settings_custom[self.table.tab]['sort_results'])

        self.clear_table(0)

        for sorting_col, sorting_order in settings['sorting_rules']:
            self.add_row()

            self.cellWidget(self.rowCount() - 1, 0).setCurrentText(sorting_col)
            self.cellWidget(self.rowCount() - 1, 1).set_text(sorting_order)

        self.clearSelection()

class Wl_Worker_Results_Sort_Concordancer(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(list)

    def run(self):
        results = []

        len_left = max([
            int(self.dialog.table_sort.cellWidget(0, 0).itemText(i)[1:])
            for i in range(self.dialog.table_sort.cellWidget(0, 0).count())
            if 'L' in self.dialog.table_sort.cellWidget(0, 0).itemText(i)
        ])
        len_right = max([
            int(self.dialog.table_sort.cellWidget(0, 0).itemText(i)[1:])
            for i in range(self.dialog.table_sort.cellWidget(0, 0).count())
            if 'R' in self.dialog.table_sort.cellWidget(0, 0).itemText(i)
        ])

        for i in range(self.dialog.tables[0].rowCount()):
            left_old = self.dialog.tables[0].cellWidget(i, 0)
            node_old = self.dialog.tables[0].cellWidget(i, 1)
            right_old = self.dialog.tables[0].cellWidget(i, 2)

            if len(left_old.text_raw) < len_left:
                left_old.text_raw = [''] * (len_left - len(left_old.text_raw)) + left_old.text_raw
            if len(right_old.text_raw) < len_right:
                right_old.text_raw.extend([''] * (len_right - len(right_old.text_raw)))

            sentiment = self.dialog.tables[0].item(i, 3).read_data()
            no_token = self.dialog.tables[0].item(i, 4).val
            no_token_pct = self.dialog.tables[0].item(i, 5).val
            no_sentence = self.dialog.tables[0].item(i, 6).val
            no_sentence_pct = self.dialog.tables[0].item(i, 7).val
            no_para = self.dialog.tables[0].item(i, 8).val
            no_para_pct = self.dialog.tables[0].item(i, 9).val
            file = self.dialog.tables[0].item(i, 10).text()

            results.append([
                left_old, node_old, right_old,
                sentiment,
                no_token, no_token_pct,
                no_sentence, no_sentence_pct,
                no_para, no_para_pct,
                file
            ])

        self.progress_updated.emit(self.tr('Updating table ...'))

        time.sleep(0.1)

        self.worker_done.emit(results)

class Wl_Worker_Results_Sort_Concordancer_Parallel(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(list, list)

    def run(self):
        results_src = []
        results_tgt = []

        table_src = self.dialog.tables[0]
        table_tgt = self.dialog.tables[1]

        # Source text
        len_left = max([
            int(self.dialog.table_sort.cellWidget(0, 0).itemText(i)[1:])
            for i in range(self.dialog.table_sort.cellWidget(0, 0).count())
            if 'L' in self.dialog.table_sort.cellWidget(0, 0).itemText(i)]
        )
        len_right = max([
            int(self.dialog.table_sort.cellWidget(0, 0).itemText(i)[1:])
            for i in range(self.dialog.table_sort.cellWidget(0, 0).count())
            if 'R' in self.dialog.table_sort.cellWidget(0, 0).itemText(i)
        ])

        for i in range(table_src.rowCount()):
            left_old = table_src.cellWidget(i, 0)
            node_old = table_src.cellWidget(i, 1)
            right_old = table_src.cellWidget(i, 2)

            if len(left_old.text_raw) < len_left:
                left_old.text_raw = [''] * (len_left - len(left_old.text_raw)) + left_old.text_raw
            if len(right_old.text_raw) < len_right:
                right_old.text_raw.extend([''] * (len_right - len(right_old.text_raw)))

            no_seg = table_src.item(i, 3).val
            no_seg_pct = table_src.item(i, 4).val

            results_src.append([
                left_old, node_old, right_old,
                no_seg, no_seg_pct,
            ])

        # Target text
        for i in range(table_tgt.rowCount()):
            parallel_text_old = table_tgt.cellWidget(i, 0)

            no_seg = table_tgt.item(i, 1).val
            no_seg_pct = table_tgt.item(i, 2).val

            results_tgt.append([
                parallel_text_old,
                no_seg, no_seg_pct,
            ])

        self.progress_updated.emit(self.tr('Updating table ...'))

        time.sleep(0.1)

        self.worker_done.emit(results_src, results_tgt)

class Wl_Dialog_Results_Sort_Concordancer(wl_dialog.Wl_Dialog):
    def __init__(self, main, table):
        super().__init__(main, main.tr('Sort Results'))

        self.tables = [table]
        self.settings = self.main.settings_custom[self.tables[0].tab]['sort_results']

        self.table_sort = Wl_Table_Results_Sort_Conordancer(self, table = self.tables[0])

        self.button_restore_default_settings = wl_button.Wl_Button_Restore_Default_Settings(self)
        self.button_sort = QPushButton(self.tr('Sort'), self)
        self.button_close = QPushButton(self.tr('Close'), self)

        self.table_sort.setFixedWidth(350)
        self.table_sort.setFixedHeight(200)

        if self.tables[0].tab == 'concordancer':
            self.button_sort.clicked.connect(lambda: self.sort_results())
        elif self.tables[0].tab == 'concordancer_parallel':
            self.button_sort.clicked.connect(lambda: self.sort_results_parallel())

        self.button_close.clicked.connect(self.reject)

        layout_table_sort = wl_layout.Wl_Layout()
        layout_table_sort.addWidget(self.table_sort, 0, 0, 4, 1)
        layout_table_sort.addWidget(self.table_sort.button_add, 0, 1)
        layout_table_sort.addWidget(self.table_sort.button_insert, 1, 1)
        layout_table_sort.addWidget(self.table_sort.button_remove, 2, 1)

        layout_table_sort.setRowStretch(3, 1)

        layout_buttons = wl_layout.Wl_Layout()
        layout_buttons.addWidget(self.button_restore_default_settings, 0, 0)
        layout_buttons.addWidget(self.button_sort, 0, 2)
        layout_buttons.addWidget(self.button_close, 0, 3)

        layout_buttons.setColumnStretch(1, 1)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addLayout(layout_table_sort, 0, 0)

        self.layout().addWidget(wl_layout.Wl_Separator(self), 1, 0)
        self.layout().addLayout(layout_buttons, 2, 0)

        self.set_fixed_size()

    # To be called by "Restore Default Settings"
    def load_settings(self, defaults = False):
        self.table_sort.load_settings(defaults = defaults)

    @wl_misc.log_timing
    def sort_results(self):
        def update_gui(results):
            # Create new labels
            for i, (left_old, node_old, right_old,
                    _, _, _, _, _, _, _, _) in enumerate(results):
                left_new = wl_label.Wl_Label_Html('', self.tables[0])
                node_new = wl_label.Wl_Label_Html(node_old.text(), self.tables[0])
                right_new = wl_label.Wl_Label_Html('', self.tables[0])

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
            sorting_rules = self.settings['sorting_rules']

            # Ascending: 0, Descending: 1
            for sorting_col, sorting_order in reversed(sorting_rules):
                if sorting_col == self.tr('Node'):
                    results.sort(key = lambda item: item[1].text_raw, reverse = sorting_order)
                # Sort first by type (strings after floats), then sort numerically or alphabetically
                elif sorting_col == self.tr('Sentiment'):
                    results.sort(key = lambda item: (str(type(item[3])), item[3]), reverse = sorting_order)
                elif sorting_col == self.tr('Token No.'):
                    results.sort(key = lambda item: item[4], reverse = sorting_order)
                elif sorting_col == self.tr('File'):
                    results.sort(key = lambda item: item[10], reverse = sorting_order)
                else:
                    span = int(sorting_col[1:])

                    if 'L' in sorting_col:
                        results.sort(key = lambda item: item[0].text_raw[-span], reverse = sorting_order)
                    elif 'R' in sorting_col:
                        results.sort(key = lambda item: item[2].text_raw[span - 1], reverse = sorting_order)

            self.tables[0].blockSignals(True)
            self.tables[0].setUpdatesEnabled(False)

            for i, (left, node, right,
                    sentiment,
                    no_token, no_token_pct,
                    no_sentence, no_sentence_pct,
                    no_para, no_para_pct,
                    file) in enumerate(results):
                for file_open in self.tables[0].settings['file_area']['files_open']:
                    if file_open['selected'] and file_open['name'] == file:
                        lang = file_open['lang']

                # Remove empty tokens
                text_left = [token for token in left.text_raw if token]
                text_right = [token for token in right.text_raw if token]

                highlight_colors = self.main.settings_custom['concordancer']['sort_results']['highlight_colors']

                i_highlight_color_left = 1
                i_highlight_color_right = 1

                for sorting_col, _ in sorting_rules:
                    if re.search(r'^L[0-9]+$', sorting_col) and int(sorting_col[1:]) <= len(text_left):
                        hightlight_color = highlight_colors[i_highlight_color_left % len(highlight_colors)]

                        text_left[-int(sorting_col[1:])] = f'''
                            <span style="color: {hightlight_color}; font-weight: bold;">
                                {text_left[-int(sorting_col[1:])]}
                            </span>
                        '''

                        i_highlight_color_left += 1
                    elif re.search(r'^R[0-9]+$', sorting_col) and int(sorting_col[1:]) - 1 < len(text_right):
                        hightlight_color = highlight_colors[i_highlight_color_right % len(highlight_colors)]

                        text_right[int(sorting_col[1:]) - 1] = f'''
                            <span style="color: {hightlight_color}; font-weight: bold;">
                                {text_right[int(sorting_col[1:]) - 1]}
                            </span>
                        '''

                        i_highlight_color_right += 1

                text_left = wl_word_detokenization.wl_word_detokenize(self.main, text_left, lang)
                text_right = wl_word_detokenization.wl_word_detokenize(self.main, text_right, lang)

                self.tables[0].cellWidget(i, 0).setText(text_left)
                self.tables[0].cellWidget(i, 1).setText(node.text())
                self.tables[0].cellWidget(i, 2).setText(text_right)

                self.tables[0].cellWidget(i, 0).text_raw = [token for token in left.text_raw if token]
                self.tables[0].cellWidget(i, 1).text_raw = node.text_raw
                self.tables[0].cellWidget(i, 2).text_raw = [token for token in right.text_raw if token]

                self.tables[0].cellWidget(i, 0).text_search = left.text_search
                self.tables[0].cellWidget(i, 1).text_search = node.text_search
                self.tables[0].cellWidget(i, 2).text_search = right.text_search

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
                self.tables[0].item(i, 10).setText(file)

            self.tables[0].setUpdatesEnabled(True)
            self.tables[0].blockSignals(False)

        if [i for i in range(self.tables[0].columnCount()) if self.tables[0].item(0, i)]:
            dialog_progress = wl_dialog_misc.Wl_Dialog_Progress_Results_Sort(self.main)

            worker_results_sort_concordancer = Wl_Worker_Results_Sort_Concordancer(
                self.main,
                dialog_progress = dialog_progress,
                update_gui = update_gui,
                dialog = self
            )

            thread_results_sort_concordancer = wl_threading.Wl_Thread(worker_results_sort_concordancer)
            thread_results_sort_concordancer.start_worker()

        wl_msg.wl_msg_results_sort(self.main)

    @wl_misc.log_timing
    def sort_results_parallel(self):
        def update_gui(results_src, results_tgt):
            results = []

            # Create new labels
            for ((left_old, node_old, right_old,
                  no_seg_src, no_seg_pct_src),
                 (parallel_text_old,
                  no_seg_tgt, no_seg_pct_tgt)) in zip(results_src, results_tgt):
                left_new = wl_label.Wl_Label_Html('', self.tables[0])
                node_new = wl_label.Wl_Label_Html(node_old.text(), self.tables[0])
                right_new = wl_label.Wl_Label_Html('', self.tables[0])
                parallel_text_new = wl_label.Wl_Label_Html(parallel_text_old.text(), self.tables[1])

                left_new.text_raw = left_old.text_raw.copy()
                node_new.text_raw = node_old.text_raw.copy()
                right_new.text_raw = right_old.text_raw.copy()
                parallel_text_new.text_raw = parallel_text_old.text_raw.copy()

                left_new.text_search = left_old.text_search.copy()
                node_new.text_search = node_old.text_search.copy()
                right_new.text_search = right_old.text_search.copy()
                parallel_text_new.text_search = parallel_text_old.text_search.copy()

                results.append([(left_new, node_new, right_new,
                                 no_seg_src, no_seg_pct_src),
                                (parallel_text_new,
                                 no_seg_tgt, no_seg_pct_tgt)])

            # Sort results
            sorting_rules = self.settings['sorting_rules']

            # Ascending: 0, Descending: 1
            for sorting_col, sorting_order in reversed(sorting_rules):
                if sorting_col == self.tr('Node'):
                    results.sort(key = lambda item: item[0][1].text_raw, reverse = sorting_order)
                elif sorting_col == self.tr('Segment No.'):
                    results.sort(key = lambda item: item[0][3], reverse = sorting_order)
                else:
                    span = int(sorting_col[1:])

                    if 'L' in sorting_col:
                        results.sort(key = lambda item: item[0][0].text_raw[-span], reverse = sorting_order)
                    elif 'R' in sorting_col:
                        results.sort(key = lambda item: item[0][2].text_raw[span - 1], reverse = sorting_order)

            self.tables[0].blockSignals(True)
            self.tables[1].blockSignals(True)
            self.tables[0].setUpdatesEnabled(False)
            self.tables[1].setUpdatesEnabled(False)

            for i, ((left, node, right,
                     no_seg_src, no_seg_pct_src),
                    (parallel_text,
                     no_seg_tgt, no_seg_pct_tgt)) in enumerate(results):
                src_file = self.tables[0].settings['concordancer_parallel']['generation_settings']['src_file']

                for file_open in self.tables[0].settings['file_area']['files_open']:
                    if file_open['selected'] and file_open['name'] == src_file:
                        lang = file_open['lang']

                # Remove empty tokens
                text_left = [token for token in left.text_raw if token]
                text_right = [token for token in right.text_raw if token]

                highlight_colors = self.main.settings_custom['concordancer']['sort_results']['highlight_colors']

                i_highlight_color_left = 1
                i_highlight_color_right = 1

                for sorting_col, _ in sorting_rules:
                    if re.search(r'^L[0-9]+$', sorting_col) and int(sorting_col[1:]) <= len(text_left):
                        hightlight_color = highlight_colors[i_highlight_color_left % len(highlight_colors)]

                        text_left[-int(sorting_col[1:])] = f'''
                            <span style="color: {hightlight_color}; font-weight: bold;">
                                {text_left[-int(sorting_col[1:])]}
                            </span>
                        '''

                        i_highlight_color_left += 1
                    elif re.search(r'^R[0-9]+$', sorting_col) and int(sorting_col[1:]) - 1 < len(text_right):
                        hightlight_color = highlight_colors[i_highlight_color_right % len(highlight_colors)]

                        text_right[int(sorting_col[1:]) - 1] = f'''
                            <span style="color: {hightlight_color}; font-weight: bold;">
                                {text_right[int(sorting_col[1:]) - 1]}
                            </span>
                        '''

                        i_highlight_color_right += 1

                text_left = wl_word_detokenization.wl_word_detokenize(self.main, text_left, lang)
                text_right = wl_word_detokenization.wl_word_detokenize(self.main, text_right, lang)

                self.tables[0].cellWidget(i, 0).setText(text_left)
                self.tables[0].cellWidget(i, 1).setText(node.text())
                self.tables[0].cellWidget(i, 2).setText(text_right)

                self.tables[0].cellWidget(i, 0).text_raw = [token for token in left.text_raw if token]
                self.tables[0].cellWidget(i, 1).text_raw = node.text_raw
                self.tables[0].cellWidget(i, 2).text_raw = [token for token in right.text_raw if token]

                self.tables[0].cellWidget(i, 0).text_search = left.text_search
                self.tables[0].cellWidget(i, 1).text_search = node.text_search
                self.tables[0].cellWidget(i, 2).text_search = right.text_search

                self.tables[0].set_item_num_val(i, 3, no_seg_src)
                self.tables[0].set_item_num_val(i, 4, no_seg_pct_src)

                self.tables[1].cellWidget(i, 0).setText(parallel_text.text())

                self.tables[1].cellWidget(i, 0).text_raw = [token for token in parallel_text.text_raw if token]
                self.tables[1].cellWidget(i, 0).text_search = parallel_text.text_search

                self.tables[1].set_item_num_val(i, 1, no_seg_tgt)
                self.tables[1].set_item_num_val(i, 2, no_seg_pct_tgt)

            self.tables[0].setUpdatesEnabled(True)
            self.tables[1].setUpdatesEnabled(True)
            self.tables[0].blockSignals(False)
            self.tables[1].blockSignals(False)

        if [i for i in range(self.tables[0].columnCount()) if self.tables[0].item(0, i)]:
            dialog_progress = wl_dialog_misc.Wl_Dialog_Progress_Results_Sort(self.main)

            worker_results_sort_concordancer_parallel = Wl_Worker_Results_Sort_Concordancer_Parallel(
                self.main,
                dialog_progress = dialog_progress,
                update_gui = update_gui,
                dialog = self
            )

            thread_results_sort_concordancer_parallel = wl_threading.Wl_Thread(worker_results_sort_concordancer_parallel)
            thread_results_sort_concordancer_parallel.start_worker()

        wl_msg.wl_msg_results_sort(self.main)

    def add_tables(self, tables):
        self.tables.extend(tables)
