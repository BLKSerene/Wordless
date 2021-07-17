#
# Wordless: Dialogs - Sort Results
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_dialog, wl_dialog_misc
from wl_text import wl_word_detokenization
from wl_utils import wl_misc, wl_threading
from wl_widgets import wl_button, wl_label, wl_layout, wl_msg, wl_table

class Wl_Worker_Results_Sort_Concordancer(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(list)

    def run(self):
        results = []

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

        for i in range(self.dialog.tables[0].rowCount()):
            left_old = self.dialog.tables[0].cellWidget(i, 0)
            node_old = self.dialog.tables[0].cellWidget(i, 1)
            right_old = self.dialog.tables[0].cellWidget(i, 2)

            if len(left_old.text_raw) < len_left:
                left_old.text_raw = [''] * (len_left - len(left_old.text_raw)) + left_old.text_raw
            if len(right_old.text_raw) < len_right:
                right_old.text_raw.extend([''] * (len_right - len(right_old.text_raw)))

            no_token = self.dialog.tables[0].item(i, 3).val
            no_token_pct = self.dialog.tables[0].item(i, 4).val
            no_sentence = self.dialog.tables[0].item(i, 5).val
            no_sentence_pct = self.dialog.tables[0].item(i, 6).val
            no_para = self.dialog.tables[0].item(i, 7).val
            no_para_pct = self.dialog.tables[0].item(i, 8).val
            file = self.dialog.tables[0].item(i, 9).text()
            sentiment = self.dialog.tables[0].item(i, 10).text()

            results.append([
                left_old, node_old, right_old,
                no_token, no_token_pct,
                no_sentence, no_sentence_pct,
                no_para, no_para_pct,
                file,
                sentiment
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

        self.table_sort = wl_table.Wl_Table_Results_Sort_Conordancer(self, table = self.tables[0])

        self.button_reset_settings = wl_button.Wl_Button_Reset_Settings(self)
        self.button_sort = QPushButton(self.tr('Sort'), self)
        self.button_close = QPushButton(self.tr('Close'), self)

        self.table_sort.setFixedWidth(280)

        self.button_reset_settings.setFixedWidth(130)
        self.button_sort.setFixedWidth(80)
        self.button_close.setFixedWidth(80)

        self.table_sort.itemChanged.connect(self.sort_table_changed)

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

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addLayout(layout_table_sort, 0, 0, 1, 4)

        self.layout().addWidget(wl_layout.Wl_Separator(self), 1, 0, 1, 4)

        self.layout().addWidget(self.button_reset_settings, 2, 0)
        self.layout().addWidget(self.button_sort, 2, 2)
        self.layout().addWidget(self.button_close, 2, 3)

        self.layout().setColumnStretch(1, 1)

        self.set_fixed_size()

    def sort_table_changed(self):
        self.settings['sorting_rules'] = []

        if self.table_sort.cellWidget(0, 0):
            for i in range(self.table_sort.rowCount()):
                self.settings['sorting_rules'].append([self.table_sort.cellWidget(i, 0).currentText(),
                                                       self.table_sort.cellWidget(i, 1).currentText()])

    def load_settings(self, defaults = False):
        if defaults:
            settings = self.main.settings_default[self.tables[0].tab]['sort_results']
        else:
            settings = self.settings

        self.table_sort.clear_table(0)

        for sorting_col, sorting_order in settings['sorting_rules']:
            self.table_sort.add_row()

            self.table_sort.cellWidget(self.table_sort.rowCount() - 1, 0).setCurrentText(sorting_col)
            self.table_sort.cellWidget(self.table_sort.rowCount() - 1, 1).setCurrentText(sorting_order)

        self.table_sort.clearSelection()

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
            sorting_rules = settings['sort_results']['sorting_rules']

            for sorting_col, sorting_order in reversed(sorting_rules):
                if sorting_col == self.tr('File'):
                    if sorting_order == self.tr('Ascending'):
                        results.sort(key = lambda item: item[9])
                    elif sorting_order == self.tr('Descending'):
                        results.sort(key = lambda item: item[9], reverse = True)
                elif sorting_col == self.tr('Token No.'):
                    if sorting_order == self.tr('Ascending'):
                        results.sort(key = lambda item: item[3])
                    elif sorting_order == self.tr('Descending'):
                        results.sort(key = lambda item: item[3], reverse = True)
                elif sorting_col == self.tr('Node'):
                    if sorting_order == self.tr('Ascending'):
                        results.sort(key = lambda item: item[1].text_raw)
                    elif sorting_order == self.tr('Descending'):
                        results.sort(key = lambda item: item[1].text_raw, reverse = True)
                else:
                    span = int(sorting_col[1:])

                    if 'L' in sorting_col:
                        if sorting_order == self.tr('Ascending'):
                            results.sort(key = lambda item: item[0].text_raw[-span])
                        elif sorting_order == self.tr('Descending'):
                            results.sort(key = lambda item: item[0].text_raw[-span], reverse = True)
                    elif 'R' in sorting_col:
                        if sorting_order == self.tr('Ascending'):
                            results.sort(key = lambda item: item[2].text_raw[span - 1])
                        elif sorting_order == self.tr('Descending'):
                            results.sort(key = lambda item: item[2].text_raw[span - 1], reverse = True)

            self.tables[0].blockSignals(True)
            self.tables[0].setUpdatesEnabled(False)

            for i, (left, node, right,
                    no_token, no_token_pct,
                    no_sentence, no_sentence_pct,
                    no_para, no_para_pct,
                    file,
                    sentiment) in enumerate(results):
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
                    if 'L' in sorting_col and -int(sorting_col[1:]) <= len(text_left):
                        hightlight_color = highlight_colors[i_highlight_color_left % len(highlight_colors)]

                        text_left[-int(sorting_col[1:])] = f'''
                            <span style="color: {hightlight_color}; font-weight: bold;">
                                {text_left[-int(sorting_col[1:])]}
                            </span>
                        '''

                        i_highlight_color_left += 1
                    elif 'R' in sorting_col and int(sorting_col[1:]) - 1 < len(text_right):
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

                self.tables[0].set_item_num(i, 3, no_token)
                self.tables[0].set_item_num(i, 4, no_token_pct)
                self.tables[0].set_item_num(i, 5, no_sentence)
                self.tables[0].set_item_num(i, 6, no_sentence_pct)
                self.tables[0].set_item_num(i, 7, no_para)
                self.tables[0].set_item_num(i, 8, no_para_pct)
                self.tables[0].item(i, 9).setText(file)
                self.tables[0].item(i, 10).setText(sentiment)

            self.tables[0].setUpdatesEnabled(True)
            self.tables[0].blockSignals(False)

        settings = self.tables[0].settings['concordancer']

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
            sorting_rules = settings['sort_results']['sorting_rules']

            for sorting_col, sorting_order in reversed(sorting_rules):
                if sorting_col == self.tr('Segment No.'):
                    if sorting_order == self.tr('Ascending'):
                        results.sort(key = lambda item: item[0][3])
                    elif sorting_order == self.tr('Descending'):
                        results.sort(key = lambda item: item[0][3], reverse = True)
                elif sorting_col == self.tr('Node'):
                    if sorting_order == self.tr('Ascending'):
                        results.sort(key = lambda item: item[0][1].text_raw)
                    elif sorting_order == self.tr('Descending'):
                        results.sort(key = lambda item: item[0][1].text_raw, reverse = True)
                else:
                    span = int(sorting_col[1:])

                    if 'L' in sorting_col:
                        if sorting_order == self.tr('Ascending'):
                            results.sort(key = lambda item: item[0][0].text_raw[-span])
                        elif sorting_order == self.tr('Descending'):
                            results.sort(key = lambda item: item[0][0].text_raw[-span], reverse = True)
                    elif 'R' in sorting_col:
                        if sorting_order == self.tr('Ascending'):
                            results.sort(key = lambda item: item[0][2].text_raw[span - 1])
                        elif sorting_order == self.tr('Descending'):
                            results.sort(key = lambda item: item[0][2].text_raw[span - 1], reverse = True)

            self.tables[0].blockSignals(True)
            self.tables[1].blockSignals(True)
            self.tables[0].setUpdatesEnabled(False)
            self.tables[1].setUpdatesEnabled(False)

            for i, ((left, node, right,
                     no_seg_src, no_seg_pct_src),
                    (parallel_text,
                     no_seg_tgt, no_seg_pct_tgt)) in enumerate(results):
                src_file = settings['generation_settings']['src_file']

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
                    if 'L' in sorting_col and -int(sorting_col[1:]) <= len(text_left):
                        hightlight_color = highlight_colors[i_highlight_color_left % len(highlight_colors)]

                        text_left[-int(sorting_col[1:])] = f'''
                            <span style="color: {hightlight_color}; font-weight: bold;">
                                {text_left[-int(sorting_col[1:])]}
                            </span>
                        '''

                        i_highlight_color_left += 1
                    elif 'R' in sorting_col and int(sorting_col[1:]) - 1 < len(text_right):
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

                self.tables[0].set_item_num(i, 3, no_seg_src)
                self.tables[0].set_item_num(i, 4, no_seg_pct_src)

                self.tables[1].cellWidget(i, 0).setText(parallel_text.text())

                self.tables[1].cellWidget(i, 0).text_raw = [token for token in parallel_text.text_raw if token]
                self.tables[1].cellWidget(i, 0).text_search = parallel_text.text_search

                self.tables[1].set_item_num(i, 1, no_seg_tgt)
                self.tables[1].set_item_num(i, 2, no_seg_pct_tgt)

            self.tables[0].setUpdatesEnabled(True)
            self.tables[1].setUpdatesEnabled(True)
            self.tables[0].blockSignals(False)
            self.tables[1].blockSignals(False)

        settings = self.tables[0].settings['concordancer_parallel']

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
