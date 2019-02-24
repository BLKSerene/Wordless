#
# Wordless: Concordancer
#
# Copyright (C) 2018-2019  Ye Lei (叶磊))
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import html

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk
import numpy
import matplotlib.pyplot

from wordless_checking import *
from wordless_dialogs import *
from wordless_text import *
from wordless_utils import *
from wordless_widgets import *

class Wordless_Table_Concordancer(wordless_table.Wordless_Table_Data_Search):
    def __init__(self, parent):
        super().__init__(parent,
                         headers = [
                             parent.tr('Left'),
                             parent.tr('Node'),
                             parent.tr('Right'),
                             parent.tr('Token No.'),
                             parent.tr('Sentence No.'),
                             parent.tr('Paragraph No.'),
                             parent.tr('File')
                         ],
                         headers_num = [
                             parent.tr('Token No.'),
                             parent.tr('Sentence No.'),
                             parent.tr('Paragraph No.')
                         ],
                         headers_pct = [
                             parent.tr('Token No.'),
                             parent.tr('Sentence No.'),
                             parent.tr('Paragraph No.')
                         ])

        dialog_search_results = wordless_dialog_search_results.Wordless_Dialog_Search_Results(
            self.main,
            tab = 'concordancer',
            table = self
        )

        self.button_search_results.clicked.connect(dialog_search_results.load)

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self)
        self.button_generate_plot = QPushButton(self.tr('Generate Plot'), self)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_plot.clicked.connect(lambda: generate_plot(self.main))

class Wordless_Combo_Box_Sorting_Col(wordless_box.Wordless_Combo_Box):
    def __init__(self, parent, table):
        super().__init__(parent)

        self.addItems(table.cols_sorting)

class Wordless_Combo_Box_Sorting_Order(wordless_box.Wordless_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems([
            self.tr('Ascending'),
            self.tr('Descending')
        ])

class Wordless_Table_Concordancer_Sorting(wordless_table.Wordless_Table):
    def __init__(self, parent, table):
        super().__init__(parent,
                         headers = [
                             parent.tr('Columns'),
                             parent.tr('Order')
                         ],
                         cols_stretch = [
                             parent.tr('Order')
                         ])

        self.table = table
        self.cols_sorting = [
            self.tr('Node'),
            self.tr('Token No.'),
            self.tr('File')
        ]

        self.button_add = QPushButton(self.tr('Add'), self)
        self.button_insert = QPushButton(self.tr('Insert'), self)
        self.button_remove = QPushButton(self.tr('Remove'), self)
        self.button_clear = QPushButton(self.tr('Clear'), self)
        self.button_sort_results = QPushButton(self.tr('Sort Results'), self)
    
        self.button_add.clicked.connect(self.add_row)
        self.button_insert.clicked.connect(self.insert_row)
        self.button_remove.clicked.connect(self.remove_row)
        self.button_clear.clicked.connect(self.clear_table)
        self.button_sort_results.clicked.connect(lambda: self.sort_results())

        self.itemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self.selection_changed)

        self.table.itemChanged.connect(self.table_item_changed)

        self.setFixedHeight(160)

        self.clear_table()

    def item_changed(self):
        if self.rowCount() < self.cellWidget(0, 0).count():
            self.button_add.setEnabled(True)
        else:
            self.button_add.setEnabled(False)

        for i in range(self.rowCount()):
            self.cellWidget(i, 0).text_old = self.cellWidget(i, 0).currentText()

    def sorting_col_changed(self, combo_box_sorting_col):
        for i in range(self.rowCount()):
            combo_box_cur = self.cellWidget(i, 0)

            if combo_box_sorting_col != combo_box_cur and combo_box_sorting_col.currentText() == combo_box_cur.currentText():
                QMessageBox.warning(self.main,
                                    self.tr('Column Sorted More Than Once'),
                                    self.tr(f'''
                                        {self.main.settings_global['styles']['style_dialog']}
                                        <body>
                                            <div>Please refrain from sorting the same column more than once!</div>
                                        </body>
                                    '''),
                                    QMessageBox.Ok)

                combo_box_sorting_col.setCurrentText(combo_box_sorting_col.text_old)
                combo_box_sorting_col.showPopup()

                return

        combo_box_sorting_col.text_old = combo_box_sorting_col.currentText()

    def selection_changed(self):
        if self.selectedIndexes() and self.rowCount() < self.cellWidget(0, 0).count():
            self.button_insert.setEnabled(True)
        else:
            self.button_insert.setEnabled(False)

        if self.selectedIndexes() and self.rowCount() > 1:
            self.button_remove.setEnabled(True)
        else:
            self.button_remove.setEnabled(False)

    def table_item_changed(self):
        sorting_rules = copy.deepcopy(self.main.settings_custom['concordancer']['sorting_settings']['sorting_rules'])

        self.setRowCount(0)

        for sorting_col, sorting_order in sorting_rules:
            if sorting_col in [sorting_rule[0]
                               for sorting_rule in self.main.settings_default['concordancer']['sorting_settings']['sorting_rules']]:
                self.cols_sorting = [
                    self.tr('Node'),
                    self.tr('Token No.'),
                    self.tr('File')
                ]

                if [i for i in range(self.table.columnCount()) if self.table.item(0, i)]:
                    if self.table.settings['concordancer']['generation_settings']['width_unit'] == self.tr('Token'):
                        width_left = self.table.settings['concordancer']['generation_settings']['width_left_token']
                        width_right = self.table.settings['concordancer']['generation_settings']['width_right_token']
                    else:
                        col_left = self.table.find_col(self.tr('Left'))
                        col_right = self.table.find_col(self.tr('Right'))

                        width_left = max([len(self.table.cellWidget(row, col_left).text_raw)
                                          for row in range(self.table.rowCount())])
                        width_right = max([len(self.table.cellWidget(row, col_right).text_raw)
                                           for row in range(self.table.rowCount())])

                    self.cols_sorting.extend([f'R{i + 1}' for i in range(width_right)])
                    self.cols_sorting.extend([f'L{i + 1}' for i in range(width_left)])

                self.add_row()

                self.cellWidget(self.rowCount() - 1, 0).setCurrentText(sorting_col)
                self.cellWidget(self.rowCount() - 1, 1).setCurrentText(sorting_order)

        self.itemChanged.emit(self.item(0, 0))

    def _new_row(self):
        combo_box_sorting_col = Wordless_Combo_Box_Sorting_Col(self, self)
        combo_box_sorting_order = Wordless_Combo_Box_Sorting_Order(self)

        if combo_box_sorting_col.findText('L1') > -1:
            width_left = max([int(combo_box_sorting_col.itemText(i)[1:])
                              for i in range(combo_box_sorting_col.count())
                              if 'L' in combo_box_sorting_col.itemText(i)])
        else:
            width_left = 0

        if combo_box_sorting_col.findText('R1') > -1:
            width_right = max([int(combo_box_sorting_col.itemText(i)[1:])
                               for i in range(combo_box_sorting_col.count())
                               if 'R' in combo_box_sorting_col.itemText(i)])
        else:
            width_right = 0

        cols_left = [int(self.cellWidget(i, 0).currentText()[1:])
                     for i in range(self.rowCount())
                     if 'L' in self.cellWidget(i, 0).currentText()]
        cols_right = [int(self.cellWidget(i, 0).currentText()[1:])
                      for i in range(self.rowCount())
                      if 'R' in self.cellWidget(i, 0).currentText()]

        if cols_left and max(cols_left) < width_left:
            combo_box_sorting_col.setCurrentText(f'L{cols_left[-1] + 1}')
        elif cols_right and max(cols_right) < width_right:
            combo_box_sorting_col.setCurrentText(f'R{cols_right[-1] + 1}')
        elif cols_right and max(cols_right) and not cols_left:
            combo_box_sorting_col.setCurrentText(f'L1')
        else:
            for i in range(combo_box_sorting_col.count()):
                text = combo_box_sorting_col.itemText(i)

                if text not in [self.cellWidget(j, 0).currentText() for j in range(self.rowCount())]:
                    combo_box_sorting_col.setCurrentText(text)

                    break

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

    def clear_table(self):
        super().clear_table(0)

        self.add_row()

        self.itemChanged.emit(self.item(0, 0))

    @wordless_misc.log_timing
    def sort_results(self):
        def key_concordancer(item):
            keys = []

            for key in sorting_keys:
                if type(key) == int:
                    keys.append(item[key])
                else:
                    keys.append(item[key[0]][key[1]])

            return keys

        results = []
        sorting_keys = []

        settings = self.table.settings['concordancer']

        if [i for i in range(self.table.columnCount()) if self.table.item(0, i)]:
            len_left = max([int(self.cellWidget(0, 0).itemText(i)[1:])
                            for i in range(self.cellWidget(0, 0).count())
                            if 'L' in self.cellWidget(0, 0).itemText(i)])
            len_right = max([int(self.cellWidget(0, 0).itemText(i)[1:])
                             for i in range(self.cellWidget(0, 0).count())
                             if 'R' in self.cellWidget(0, 0).itemText(i)])

            for i in range(self.table.rowCount()):
                left = self.table.cellWidget(i, 0).text_raw
                node = self.table.cellWidget(i, 1).text()
                right = self.table.cellWidget(i, 2).text_raw

                if len(left) < len_left:
                    left = [''] * (len_left - len(left)) + left
                if len(right) < len_right:
                    right.extend([''] * (len_right - len(right)))

                token_no = self.table.item(i, 3).val
                sentence_no = self.table.item(i, 4).val
                para_no = self.table.item(i, 5).val
                file = self.table.item(i, 6).text()

                results.append([left, node, right, token_no, sentence_no, para_no, file])

            for sorting_col, sorting_order in settings['sorting_settings']['sorting_rules']:
                if sorting_col == self.tr('File'):
                    sorting_keys.append(6)
                elif sorting_col == self.tr('Token No.'):
                    sorting_keys.append(3)
                elif sorting_col == self.tr('Node'):
                    sorting_keys.append(1)
                elif 'R' in sorting_col:
                    sorting_keys.append([2, int(sorting_col[1:]) - 1])
                elif 'L' in sorting_col:
                    sorting_keys.append([0, -int(sorting_col[1:])])

            self.table.hide()
            self.table.blockSignals(True)
            self.table.setUpdatesEnabled(False)

            for i, (left, node, right,
                    token_no, sentence_no, para_no, file) in enumerate(sorted(results, key = key_concordancer)):
                for file_open in self.table.settings['files']['files_open']:
                    if file_open['selected'] and file_open['name'] == file:
                        lang = file_open['lang']

                # Remove empty tokens
                left = [token for token in left if token]
                right = [token for token in right if token]

                self.table.cellWidget(i, 0).text_raw = left
                self.table.cellWidget(i, 2).text_raw = right

                highlight_colors = self.main.settings_custom['concordancer']['sorting_settings']['highlight_colors']

                i_highlight_color_left = 1
                i_highlight_color_right = 1

                for j, key in enumerate([key for key in sorting_keys if type(key) != int]):
                    if key[0] == 0 and -key[1] <= len(left):
                        hightlight_color = highlight_colors[i_highlight_color_left % len(highlight_colors)]

                        left[key[1]] = f'''
                                           <span style="color: {hightlight_color}; font-weight: bold;">
                                               {left[key[1]]}
                                           </span>
                                       '''

                        i_highlight_color_left += 1
                    elif key[0] == 2 and key[1] < len(right):
                        hightlight_color = highlight_colors[i_highlight_color_right % len(highlight_colors)]

                        right[key[1]] = f'''
                                            <span style="color: {hightlight_color}; font-weight: bold;">
                                                {right[key[1]]}
                                            </span>
                                        '''

                        i_highlight_color_right += 1

                self.table.cellWidget(i, 0).setText(wordless_text_processing.wordless_word_detokenize(self.main, left, lang))
                self.table.cellWidget(i, 1).setText(node)
                self.table.cellWidget(i, 2).setText(wordless_text_processing.wordless_word_detokenize(self.main, right, lang))

                self.table.item(i, 3).val = token_no
                self.table.item(i, 4).val = sentence_no
                self.table.item(i, 5).val = para_no
                self.table.item(i, 6).setText(file)

            self.table.show()
            self.table.blockSignals(False)
            self.table.setUpdatesEnabled(True)

            self.table.toggle_pct()

            self.table.update_items_width()

        wordless_message.wordless_message_sort_results(self.main)

    def get_sorting_rules(self):
        if self.cellWidget(0, 0):
            return [[self.cellWidget(i, 0).currentText(),
                     self.cellWidget(i, 1).currentText()] for i in range(self.rowCount())]
        else:
            return []

class Wrapper_Concordancer(wordless_layout.Wordless_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        self.table_concordancer = Wordless_Table_Concordancer(self)

        self.wrapper_table.layout().addWidget(self.table_concordancer.label_number_results, 0, 0)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_search_results, 0, 4, Qt.AlignRight)
        self.wrapper_table.layout().addWidget(self.table_concordancer, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_generate_plot, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_export_selected, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_export_all, 2, 3)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_clear, 2, 4)

        # Token Settings
        self.group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

        (self.checkbox_puncs,

         self.token_stacked_widget_ignore_tags,
         self.token_stacked_widget_ignore_tags_type,
         self.label_ignore_tags,
         self.checkbox_use_tags) = wordless_widgets.wordless_widgets_token_settings_concordancer(self)

        self.checkbox_puncs.stateChanged.connect(self.token_settings_changed)

        self.token_stacked_widget_ignore_tags.checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.token_stacked_widget_ignore_tags.checkbox_ignore_tags_tags.stateChanged.connect(self.token_settings_changed)
        self.token_stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentTextChanged.connect(self.token_settings_changed)
        self.token_stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentTextChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        layout_ignore_tags = QGridLayout()
        layout_ignore_tags.addWidget(self.token_stacked_widget_ignore_tags, 0, 0)
        layout_ignore_tags.addWidget(self.token_stacked_widget_ignore_tags_type, 0, 1)
        layout_ignore_tags.addWidget(self.label_ignore_tags, 0, 2)

        layout_ignore_tags.setColumnStretch(3, 1)

        self.group_box_token_settings.setLayout(QGridLayout())
        self.group_box_token_settings.layout().addWidget(self.checkbox_puncs, 0, 0)

        self.group_box_token_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 1, 0)

        self.group_box_token_settings.layout().addLayout(layout_ignore_tags, 2, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 3, 0)

        # Search Settings
        self.group_box_search_settings = QGroupBox(self.tr('Search Settings'), self)

        (self.label_search_term,
         self.checkbox_multi_search_mode,
         self.line_edit_search_term,
         self.list_search_terms,
         self.label_separator,

         self.checkbox_ignore_case,
         self.checkbox_match_inflected_forms,
         self.checkbox_match_whole_word,
         self.checkbox_use_regex,

         self.search_stacked_widget_ignore_tags,
         self.search_stacked_widget_ignore_tags_type,
         self.search_label_ignore_tags,
         self.checkbox_match_tags) = wordless_widgets.wordless_widgets_search_settings(self,
                                                                                       tab = 'concordancer')

        (self.label_context_settings,
         self.button_context_settings) = wordless_widgets.wordless_widgets_context_settings(self,
                                                                                            tab = 'concordancer')

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.table_concordancer.button_generate_table.click)
        self.list_search_terms.itemChanged.connect(self.search_settings_changed)

        self.checkbox_ignore_case.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_inflected_forms.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_whole_word.stateChanged.connect(self.search_settings_changed)
        self.checkbox_use_regex.stateChanged.connect(self.search_settings_changed)

        self.search_stacked_widget_ignore_tags.checkbox_ignore_tags.stateChanged.connect(self.search_settings_changed)
        self.search_stacked_widget_ignore_tags.checkbox_ignore_tags_tags.stateChanged.connect(self.search_settings_changed)
        self.search_stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentTextChanged.connect(self.search_settings_changed)
        self.search_stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentTextChanged.connect(self.search_settings_changed)
        self.checkbox_match_tags.stateChanged.connect(self.search_settings_changed)

        layout_search_terms = QGridLayout()
        layout_search_terms.addWidget(self.list_search_terms, 0, 0, 5, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_add, 0, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_remove, 1, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_clear, 2, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_import, 3, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_export, 4, 1)

        layout_ignore_tags = QGridLayout()
        layout_ignore_tags.addWidget(self.search_stacked_widget_ignore_tags, 0, 0)
        layout_ignore_tags.addWidget(self.search_stacked_widget_ignore_tags_type, 0, 1)
        layout_ignore_tags.addWidget(self.search_label_ignore_tags, 0, 2)

        layout_ignore_tags.setColumnStretch(3, 1)

        layout_context_settings = QGridLayout()
        layout_context_settings.addWidget(self.label_context_settings, 0, 0)
        layout_context_settings.addWidget(self.button_context_settings, 0, 1)

        layout_context_settings.setColumnStretch(1, 1)

        self.group_box_search_settings.setLayout(QGridLayout())
        self.group_box_search_settings.layout().addWidget(self.label_search_term, 0, 0)
        self.group_box_search_settings.layout().addWidget(self.checkbox_multi_search_mode, 0, 1, Qt.AlignRight)
        self.group_box_search_settings.layout().addWidget(self.line_edit_search_term, 1, 0, 1, 2)
        self.group_box_search_settings.layout().addLayout(layout_search_terms, 2, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.label_separator, 3, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(self.checkbox_ignore_case, 4, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_inflected_forms, 5, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_whole_word, 6, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_use_regex, 7, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_ignore_tags, 8, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_tags, 9, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 10, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_context_settings, 11, 0, 1, 2)

        # Generation Settings
        self.group_box_generation_settings = QGroupBox(self.tr('Generation Settings'), self)

        self.label_width_left = QLabel(self.tr('Width (Left):'), self)
        self.spin_box_width_left_token = QSpinBox(self)
        self.spin_box_width_left_char = QSpinBox(self)
        self.label_width_right = QLabel(self.tr('Width (Right):'), self)
        self.spin_box_width_right_token = QSpinBox(self)
        self.spin_box_width_right_char = QSpinBox(self)
        self.label_width_unit = QLabel(self.tr('Width Unit:'), self)
        self.combo_box_width_unit = wordless_box.Wordless_Combo_Box(self)

        self.label_number_lines = QLabel(self.tr('Limit number of lines in each file:'), self)
        (self.spin_box_number_lines,
         self.checkbox_number_lines) = wordless_widgets.wordless_widgets_no_limit(self)
        self.label_every_nth_line = QLabel(self.tr('Only show every nth line in each file:'), self)
        (self.spin_box_every_nth_line,
         self.checkbox_every_nth_line) = wordless_widgets.wordless_widgets_no_limit(self)

        self.combo_box_width_unit.addItems([
            self.tr('Token'),
            self.tr('Character')
        ])

        self.spin_box_width_left_token.setRange(0, 100)
        self.spin_box_width_left_char.setRange(0, 500)
        self.spin_box_width_right_token.setRange(0, 100)
        self.spin_box_width_right_char.setRange(0, 500)

        self.spin_box_number_lines.setRange(1, 100000)
        self.spin_box_every_nth_line.setRange(2, 100000)

        self.spin_box_width_left_token.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_width_left_char.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_width_right_token.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_width_right_char.valueChanged.connect(self.generation_settings_changed)
        self.combo_box_width_unit.currentTextChanged.connect(self.generation_settings_changed)

        self.spin_box_number_lines.valueChanged.connect(self.generation_settings_changed)
        self.checkbox_number_lines.stateChanged.connect(self.generation_settings_changed)
        self.spin_box_every_nth_line.valueChanged.connect(self.generation_settings_changed)
        self.checkbox_every_nth_line.stateChanged.connect(self.generation_settings_changed)

        layout_width = QGridLayout()
        layout_width.addWidget(self.label_width_left, 0, 0)
        layout_width.addWidget(self.spin_box_width_left_token, 0, 1)
        layout_width.addWidget(self.spin_box_width_left_char, 0, 1)
        layout_width.addWidget(self.label_width_right, 1, 0)
        layout_width.addWidget(self.spin_box_width_right_token, 1, 1)
        layout_width.addWidget(self.spin_box_width_right_char, 1, 1)
        layout_width.addWidget(self.label_width_unit, 2, 0)
        layout_width.addWidget(self.combo_box_width_unit, 2, 1)

        layout_width.setColumnStretch(1, 1)

        self.group_box_generation_settings.setLayout(QGridLayout())
        self.group_box_generation_settings.layout().addLayout(layout_width, 0, 0, 1, 2)

        self.group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 1, 0, 1, 2)

        self.group_box_generation_settings.layout().addWidget(self.label_number_lines, 2, 0, 1, 2)
        self.group_box_generation_settings.layout().addWidget(self.spin_box_number_lines, 3, 0)
        self.group_box_generation_settings.layout().addWidget(self.checkbox_number_lines, 3, 1)
        self.group_box_generation_settings.layout().addWidget(self.label_every_nth_line, 4, 0, 1, 2)
        self.group_box_generation_settings.layout().addWidget(self.spin_box_every_nth_line, 5, 0)
        self.group_box_generation_settings.layout().addWidget(self.checkbox_every_nth_line, 5, 1)

        self.group_box_generation_settings.layout().setColumnStretch(0, 1)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'), self)

        (self.checkbox_show_pct,
         self.checkbox_show_cumulative,
         self.checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table_settings(self,
                                                                                          table = self.table_concordancer)

        self.checkbox_show_cumulative.hide()
        self.checkbox_show_breakdown.hide()

        self.checkbox_show_pct.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(QGridLayout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct, 0, 0)

        # Plot Settings
        self.group_box_plot_settings = QGroupBox(self.tr('Plot Settings'), self)

        self.label_sort_results_by = QLabel(self.tr('Sort Results by:'), self)
        self.combo_box_sort_results_by = wordless_box.Wordless_Combo_Box(self)

        self.combo_box_sort_results_by.addItems([
            self.tr('File'),
            self.tr('Search Term')
        ])

        self.combo_box_sort_results_by.currentTextChanged.connect(self.plot_settings_changed)

        self.group_box_plot_settings.setLayout(QGridLayout())
        self.group_box_plot_settings.layout().addWidget(self.label_sort_results_by, 0, 0)
        self.group_box_plot_settings.layout().addWidget(self.combo_box_sort_results_by, 0, 1)

        self.group_box_plot_settings.layout().setColumnStretch(1, 1)

        # Sorting Settings
        self.group_box_sorting_settings = QGroupBox(self.tr('Sorting Settings'), self)

        self.table_concordancer_sorting = Wordless_Table_Concordancer_Sorting(self,
                                                                              table = self.table_concordancer)

        self.table_concordancer_sorting.itemChanged.connect(self.sorting_settings_changed)

        self.group_box_sorting_settings.setLayout(QGridLayout())
        self.group_box_sorting_settings.layout().addWidget(self.table_concordancer_sorting, 0, 0, 1, 2)
        self.group_box_sorting_settings.layout().addWidget(self.table_concordancer_sorting.button_add, 1, 0)
        self.group_box_sorting_settings.layout().addWidget(self.table_concordancer_sorting.button_insert, 1, 1)
        self.group_box_sorting_settings.layout().addWidget(self.table_concordancer_sorting.button_remove, 2, 0)
        self.group_box_sorting_settings.layout().addWidget(self.table_concordancer_sorting.button_clear, 2, 1)
        self.group_box_sorting_settings.layout().addWidget(self.table_concordancer_sorting.button_sort_results, 3, 0, 1, 2)

        self.wrapper_settings.layout().addWidget(self.group_box_token_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_search_settings, 1, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_generation_settings, 2, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 3, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_plot_settings, 4, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_sorting_settings, 5, 0)

        self.wrapper_settings.layout().setRowStretch(6, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['concordancer'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['concordancer'])

        # Token Settings
        self.checkbox_puncs.setChecked(settings['token_settings']['puncs'])

        self.token_stacked_widget_ignore_tags.checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.token_stacked_widget_ignore_tags.checkbox_ignore_tags_tags.setChecked(settings['token_settings']['ignore_tags_tags'])
        self.token_stacked_widget_ignore_tags_type.combo_box_ignore_tags.setCurrentText(settings['token_settings']['ignore_tags_type'])
        self.token_stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.setCurrentText(settings['token_settings']['ignore_tags_type_tags'])
        self.checkbox_use_tags.setChecked(settings['token_settings']['use_tags'])

        # Search Settings
        self.checkbox_multi_search_mode.setChecked(settings['search_settings']['multi_search_mode'])

        if not defaults:
            self.line_edit_search_term.setText(settings['search_settings']['search_term'])
            self.list_search_terms.load_items(settings['search_settings']['search_terms'])

        self.checkbox_ignore_case.setChecked(settings['search_settings']['ignore_case'])
        self.checkbox_match_inflected_forms.setChecked(settings['search_settings']['match_inflected_forms'])
        self.checkbox_match_whole_word.setChecked(settings['search_settings']['match_whole_word'])
        self.checkbox_use_regex.setChecked(settings['search_settings']['use_regex'])

        self.search_stacked_widget_ignore_tags.checkbox_ignore_tags.setChecked(settings['search_settings']['ignore_tags'])
        self.search_stacked_widget_ignore_tags.checkbox_ignore_tags_tags.setChecked(settings['search_settings']['ignore_tags_tags'])
        self.search_stacked_widget_ignore_tags_type.combo_box_ignore_tags.setCurrentText(settings['search_settings']['ignore_tags_type'])
        self.search_stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.setCurrentText(settings['search_settings']['ignore_tags_type_tags'])
        self.checkbox_match_tags.setChecked(settings['search_settings']['match_tags'])

        # Context Settings
        if defaults:
            self.main.wordless_context_settings_concordancer.load_settings(defaults = True)

        # Generation Settings
        self.spin_box_width_left_token.setValue(settings['generation_settings']['width_left_token'])
        self.spin_box_width_left_char.setValue(settings['generation_settings']['width_left_char'])
        self.spin_box_width_right_token.setValue(settings['generation_settings']['width_right_token'])
        self.spin_box_width_right_char.setValue(settings['generation_settings']['width_right_char'])
        self.combo_box_width_unit.setCurrentText(settings['generation_settings']['width_unit'])

        self.spin_box_number_lines.setValue(settings['generation_settings']['number_lines'])
        self.checkbox_number_lines.setChecked(settings['generation_settings']['number_lines_no_limit'])
        self.spin_box_every_nth_line.setValue(settings['generation_settings']['every_nth_line'])
        self.checkbox_every_nth_line.setChecked(settings['generation_settings']['every_nth_line_no_limit'])

        # Table Settings
        self.checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])

        # Plot Settings
        self.combo_box_sort_results_by.setCurrentText(settings['plot_settings']['sort_results_by'])

        # Sorting Settings
        self.table_concordancer_sorting.setRowCount(0)

        for sorting_col, sorting_order in settings['sorting_settings']['sorting_rules']:
            if sorting_col in [sorting_rule[0]
                               for sorting_rule in self.main.settings_default['concordancer']['sorting_settings']['sorting_rules']]:
                self.table_concordancer_sorting.add_row()

                self.table_concordancer_sorting.cellWidget(self.table_concordancer_sorting.rowCount() - 1, 0).setCurrentText(sorting_col)
                self.table_concordancer_sorting.cellWidget(self.table_concordancer_sorting.rowCount() - 1, 1).setCurrentText(sorting_order)

        self.token_settings_changed()
        self.search_settings_changed()
        self.generation_settings_changed()
        self.table_settings_changed()
        self.sorting_settings_changed()

    def token_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['token_settings']

        settings['puncs'] = self.checkbox_puncs.isChecked()

        settings['ignore_tags'] = self.token_stacked_widget_ignore_tags.checkbox_ignore_tags.isChecked()
        settings['ignore_tags_tags'] = self.token_stacked_widget_ignore_tags.checkbox_ignore_tags_tags.isChecked()
        settings['ignore_tags_type'] = self.token_stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentText()
        settings['ignore_tags_type_tags'] = self.token_stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentText()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

        self.checkbox_match_tags.token_settings_changed()
        self.main.wordless_context_settings_concordancer.token_settings_changed()

    def search_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['search_settings']

        settings['multi_search_mode'] = self.checkbox_multi_search_mode.isChecked()
        settings['search_term'] = self.line_edit_search_term.text()
        settings['search_terms'] = self.list_search_terms.get_items()

        settings['ignore_case'] = self.checkbox_ignore_case.isChecked()
        settings['match_inflected_forms'] = self.checkbox_match_inflected_forms.isChecked()
        settings['match_whole_word'] = self.checkbox_match_whole_word.isChecked()
        settings['use_regex'] = self.checkbox_use_regex.isChecked()

        settings['ignore_tags'] = self.search_stacked_widget_ignore_tags.checkbox_ignore_tags.isChecked()
        settings['ignore_tags_tags'] = self.search_stacked_widget_ignore_tags.checkbox_ignore_tags_tags.isChecked()
        settings['ignore_tags_type'] = self.search_stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentText()
        settings['ignore_tags_type_tags'] = self.search_stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentText()
        settings['match_tags'] = self.checkbox_match_tags.isChecked()

    def generation_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['generation_settings']

        settings['width_left_token'] = self.spin_box_width_left_token.value()
        settings['width_left_char'] = self.spin_box_width_left_char.value()
        settings['width_right_token'] = self.spin_box_width_right_token.value()
        settings['width_right_char'] = self.spin_box_width_right_char.value()
        settings['width_unit'] = self.combo_box_width_unit.currentText()

        settings['number_lines'] = self.spin_box_number_lines.value()
        settings['number_lines_no_limit'] = self.checkbox_number_lines.isChecked()
        settings['every_nth_line'] = self.spin_box_every_nth_line.value()
        settings['every_nth_line_no_limit'] = self.checkbox_every_nth_line.isChecked()

        if settings['width_unit'] == self.tr('Token'):
            self.spin_box_width_left_token.show()
            self.spin_box_width_right_token.show()

            self.spin_box_width_left_char.hide()
            self.spin_box_width_right_char.hide()
        else:
            self.spin_box_width_left_token.hide()
            self.spin_box_width_right_token.hide()

            self.spin_box_width_left_char.show()
            self.spin_box_width_right_char.show()

    def table_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()

    def plot_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['plot_settings']

        settings['sort_results_by'] = self.combo_box_sort_results_by.currentText()

    def sorting_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['sorting_settings']

        settings['sorting_rules'] = self.table_concordancer_sorting.get_sorting_rules()

class Worker_Process_Data_Table(wordless_threading.Worker_Process_Data):
    processing_finished = pyqtSignal(list)

    def process_data(self):
        concordance_lines = []

        settings = self.main.settings_custom['concordancer']
        files = self.main.wordless_files.get_selected_files()

        self.progress_updated.emit(self.tr('Searching ...'))

        for file in files:
            number_lines = 0
            number_lines_nth = 0

            text = wordless_text.Wordless_Text(self.main, file, tokens_only = False)

            tokens = wordless_token_processing.wordless_process_tokens_concordancer(text,
                                                                                    token_settings = settings['token_settings'])

            len_paras = len(text.para_offsets)
            len_sentences = len(text.sentence_offsets)
            len_tokens = len(text.tokens)

            search_terms = wordless_matching.match_search_terms(self.main, tokens,
                                                                lang = text.lang,
                                                                text_type = text.text_type,
                                                                token_settings = settings['token_settings'],
                                                                search_settings = settings['search_settings'])

            (search_terms_inclusion,
             search_terms_exclusion) = wordless_matching.match_search_terms_context(self.main, tokens,
                                                                                    lang = text.lang,
                                                                                    text_type = text.text_type,
                                                                                    token_settings = settings['token_settings'],
                                                                                    context_settings = settings['context_settings'])

            if search_terms:
                len_search_term_min = min([len(search_term) for search_term in search_terms])
                len_search_term_max = max([len(search_term) for search_term in search_terms])
            else:
                len_search_term_min = 0
                len_search_term_max = 0

            for len_search_term in range(len_search_term_min, len_search_term_max + 1):
                # Check number of lines
                if not settings['generation_settings']['number_lines_no_limit']:
                    if number_lines >= settings['generation_settings']['number_lines']:
                        break

                for i, ngram in enumerate(nltk.ngrams(tokens, len_search_term)):
                    if (ngram in search_terms and
                        wordless_matching.check_context(i, tokens,
                                                        context_settings = settings['context_settings'],
                                                        search_terms_inclusion = search_terms_inclusion,
                                                        search_terms_exclusion = search_terms_exclusion)):
                        concordance_line = []

                        # Check number of lines
                        if not settings['generation_settings']['number_lines_no_limit']:
                            if number_lines < settings['generation_settings']['number_lines']:
                                number_lines += 1
                            else:
                                break

                        # Check every nth line
                        if not settings['generation_settings']['every_nth_line_no_limit']:
                            number_lines_nth += 1

                            if (number_lines_nth - 1) % settings['generation_settings']['every_nth_line'] > 0:
                                continue

                        # Search Results
                        text_search = ngram

                        if not settings['token_settings']['puncs']:
                            ngram = text.tokens[i : i + len_search_term]

                        node_text = html.escape(wordless_text_processing.wordless_word_detokenize(self.main, ngram, text.lang))

                        # Width Unit
                        if settings['generation_settings']['width_unit'] == self.tr('Token'):
                            context_left = text.tokens[max(0, i - settings['generation_settings']['width_left_token']) : i]
                            context_right = text.tokens[i + len_search_term : min(i + len_search_term + settings['generation_settings']['width_right_token'], len_tokens)]

                            # Search Results
                            if settings['token_settings']['puncs']:
                                text_search_left = copy.deepcopy(context_left)
                                text_search_right = copy.deepcopy(context_right)
                            else:
                                text_search_left = tokens[max(0, i - settings['generation_settings']['width_left_token']) : i]
                                text_search_right = tokens[i + len_search_term : min(i + len_search_term + settings['generation_settings']['width_right_token'], len_tokens)]
                        elif settings['generation_settings']['width_unit'] == self.tr('Character'):
                            len_context_left = 0
                            len_context_right = 0

                            context_left = []
                            context_right = []

                            while len_context_left < settings['generation_settings']['width_left_char']:
                                if i - 1 - len(context_left) < 0:
                                    break
                                else:
                                    token_next = tokens[i - 1 - len(context_left)]
                                    len_token_next = len(token_next)

                                if len_context_left + len_token_next > settings['generation_settings']['width_left_char']:
                                    context_left.insert(0, token_next[-(settings['generation_settings']['width_left_char'] - len_context_left):])
                                else:
                                    context_left.insert(0, token_next)

                                len_context_left += len_token_next

                            while len_context_right < settings['generation_settings']['width_right_char']:
                                if i + 1 + len(context_right) > len(text.tokens) - 1:
                                    break
                                else:
                                    token_next = tokens_text[i + len_search_term + len(context_right)]
                                    len_token_next = len(token_next)

                                if len_context_right + len_token_next > settings['generation_settings']['width_right_char']:
                                    context_right.append(token_next[: settings['generation_settings']['width_right_char'] - len_context_right])
                                else:
                                    context_right.append(token_next)

                                len_context_right += len(token_next)

                            # Search Results
                            text_search_left = copy.deepcopy(context_left)
                            text_search_right = copy.deepcopy(context_right)

                            if not settings['token_settings']['puncs']:
                                context_left_first_puncs = text.tokens[i - len(context_left)]
                                context_right_last_puncs = text.tokens[i + len_search_term + len(context_right) - 1]
                                context_left_first = ''
                                context_right_last = ''

                                len_context_left_first = 0
                                len_context_right_last = 0

                                while len_context_left_first < len(context_left[0]):
                                    char_next = context_left_first_puncs[-(len(context_left_first) + 1)]

                                    context_left_first = char_next + context_left_first

                                    if char_next.isalnum():
                                        len_context_left_first += 1

                                while len_context_right_last < len(context_right[-1]):
                                    char_next = context_right_last_puncs[len(context_right_last)]

                                    context_right_last += char_next

                                    if char_next.isalnum():
                                        len_context_right_last += 1

                                context_left = ([context_left_first] +
                                                text.tokens[i - len(context_left) + 1: i])
                                context_right = (text.tokens[i + len_search_term : i + len_search_term + len(context_right) - 1] +
                                                 [context_right_last])

                        context_left = [html.escape(token) for token in context_left]
                        context_right = [html.escape(token) for token in context_right]

                        context_left_text = wordless_text_processing.wordless_word_detokenize(self.main, context_left, text.lang)
                        context_right_text = wordless_text_processing.wordless_word_detokenize(self.main, context_right, text.lang)

                        # Left
                        concordance_line.append([context_left_text, context_left, text_search_left])

                        # Node
                        concordance_line.append([node_text, ngram, text_search])

                        # Right
                        concordance_line.append([context_right_text, context_right, text_search_right])

                        # Token
                        concordance_line.append([i + 1, len_tokens])

                        # Sentence
                        if text.sentence_offsets[-1] < i:
                            sentence_no = len_sentences
                        else:
                            for j, i_sentence in enumerate(text.sentence_offsets):
                                if i_sentence > i:
                                    sentence_no = j

                                    break

                        concordance_line.append([sentence_no, len_sentences])

                        # Paragraph
                        if text.para_offsets[-1] < i:
                            para_no = len_paras
                        else:
                            for j, i_para in enumerate(text.para_offsets):
                                if i_para > i:
                                    para_no = j

                                    break

                        concordance_line.append([para_no, len_paras])

                        # File
                        concordance_line.append(file['name'])

                        concordance_lines.append(concordance_line)

        self.processing_finished.emit(concordance_lines)

@wordless_misc.log_timing
def generate_table(main, table):
    def data_received(concordance_lines):
        node_color = settings['sorting_settings']['highlight_colors'][0]

        if concordance_lines:
            table.clear_table(0)

            table.settings = main.settings_custom

            table.hide()
            table.blockSignals(True)
            table.setUpdatesEnabled(False)

            for concordance_line in concordance_lines:
                left_text, left_text_raw, left_text_search = concordance_line[0]
                node_text, node_text_raw, node_text_search = concordance_line[1]
                right_text, right_text_raw, right_text_search = concordance_line[2]

                token_no, len_tokens = concordance_line[3]
                sentence_no, len_sentences = concordance_line[4]
                para_no, len_paras = concordance_line[5]
                file_name = concordance_line[6]

                table.setRowCount(table.rowCount() + 1)

                # Node
                label_node = wordless_label.Wordless_Label_Html(
                    f'''
                        <span style="color: {node_color}; font-weight: bold;">
                            {node_text}
                        </span>
                    ''',
                    main
                )

                table.setCellWidget(table.rowCount() - 1, 1, label_node)

                table.cellWidget(table.rowCount() - 1, 1).setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                table.cellWidget(table.rowCount() - 1, 1).text_raw = node_text_raw
                table.cellWidget(table.rowCount() - 1, 1).text_search = node_text_search

                # Left
                table.setCellWidget(table.rowCount() - 1, 0,
                                    wordless_label.Wordless_Label_Html(left_text, main))

                table.cellWidget(table.rowCount() - 1, 0).setAlignment(Qt.AlignRight | Qt.AlignVCenter)

                table.cellWidget(table.rowCount() - 1, 0).text_raw = left_text_raw
                table.cellWidget(table.rowCount() - 1, 0).text_search = left_text_search

                # Right
                table.setCellWidget(table.rowCount() - 1, 2,
                                    wordless_label.Wordless_Label_Html(right_text, main))

                table.cellWidget(table.rowCount() - 1, 2).text_raw = right_text_raw
                table.cellWidget(table.rowCount() - 1, 2).text_search = right_text_search

                # Token
                table.set_item_num_pct(table.rowCount() - 1, 3, token_no, len_tokens)

                # Sentence
                table.set_item_num_pct(table.rowCount() - 1, 4, sentence_no, len_sentences)

                # Paragraph
                table.set_item_num_pct(table.rowCount() - 1, 5, para_no, len_paras)

                # File
                table.setItem(table.rowCount() - 1, 6, QTableWidgetItem(file_name))

            table.blockSignals(False)
            table.setUpdatesEnabled(True)
            table.show()

            table.toggle_pct()
            table.update_items_width()

            table.itemChanged.emit(table.item(0, 0))

            wordless_message.wordless_message_generate_table_success(main)
        else:
            wordless_message_box.wordless_message_box_no_results(main)

            wordless_message.wordless_message_generate_table_error(main)

        dialog_processing.accept()

    settings = main.settings_custom['concordancer']
    files = main.wordless_files.get_selected_files()

    if wordless_checking_file.check_files_on_loading(main, files):
        if (not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term'] or
            settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms']):
            dialog_processing = wordless_dialog_misc.Wordless_Dialog_Processing_Generate_Data(main)

            worker_process_data = Worker_Process_Data_Table(main, dialog_processing, data_received)
            thread_process_data = wordless_threading.Thread_Process_Data(worker_process_data)

            thread_process_data.start()

            dialog_processing.exec_()

            thread_process_data.quit()
            thread_process_data.wait()
        else:
            wordless_message_box.wordless_message_box_missing_search_term(main)

            wordless_message.wordless_message_generate_table_error(main)
    else:
        wordless_message.wordless_message_generate_table_error(main)

class Worker_Process_Data_Plot(wordless_threading.Worker_Process_Data):
    processing_finished = pyqtSignal(list, list)

    def process_data(self):
        texts = []
        search_terms_files = []
        search_terms_total = set()
        search_terms_labels = set()

        points = []
        labels = []

        settings = self.main.settings_custom['concordancer']
        files = sorted(self.main.wordless_files.get_selected_files(), key = lambda item: item['name'])

        for file in files:
            text = wordless_text.Wordless_Text(self.main, file)

            text.tokens = wordless_token_processing.wordless_process_tokens_concordancer(text,
                                                                                         token_settings = settings['token_settings'])

            search_terms_file = wordless_matching.match_search_terms(self.main, text.tokens,
                                                                     lang = text.lang,
                                                                     text_type = text.text_type,
                                                                     token_settings = settings['token_settings'],
                                                                     search_settings = settings['search_settings'])

            search_terms_files.append(sorted(search_terms_file))

            for search_term in search_terms_file:
                search_terms_total.add(search_term)
                search_terms_labels.add(wordless_text_processing.wordless_word_detokenize(self.main, search_term,
                                                                                          lang = text.lang))

            texts.append(text)

        len_files = len(files)
        len_tokens_total = sum([len(text.tokens) for text in texts])
        len_search_terms_total = len(search_terms_total)

        if settings['plot_settings']['sort_results_by'] == self.tr('File'):
            search_terms_total = sorted(search_terms_total)
            search_terms_labels = sorted(search_terms_labels)

            for i, search_term in enumerate(search_terms_total):
                len_search_term = len(search_term)

                x_start = len_tokens_total * i + 1
                y_start = len_files

                for j, text in enumerate(texts):
                    if search_term in search_terms_files[j]:
                        x_start_total = x_start + sum([len(text.tokens)
                                                       for k, text in enumerate(texts)
                                                       if k < j])
                        len_tokens = len(text.tokens)

                        for k, ngram in enumerate(nltk.ngrams(text.tokens, len_search_term)):
                            if ngram == search_term:
                                points.append([x_start + k / len_tokens * len_tokens_total, y_start - j])
                                # Total
                                points.append([x_start_total + k, 0])
        elif settings['plot_settings']['sort_results_by'] == self.tr('Search Term'):
            search_terms_total = sorted(search_terms_total, reverse = True)
            search_terms_labels = sorted(search_terms_labels, reverse = True)

            for i, search_term in enumerate(search_terms_total):
                len_search_term = len(search_term)

                for j, text in enumerate(texts):
                    if search_term in search_terms_files[j]:
                        x_start = sum([len(text.tokens)
                                       for k, text in enumerate(texts)
                                       if k < j]) + j + 2

                        for k, ngram in enumerate(nltk.ngrams(text.tokens, len_search_term)):
                            if ngram == search_term:
                                points.append([x_start + k, i])

        if points:
            x_ticks = [0]
            x_tick_labels = ['']

            if settings['plot_settings']['sort_results_by'] == self.tr('File'):
                len_tokens_total = sum([len(text.tokens) for text in texts])

                for i, search_term in enumerate(search_terms_total):
                    x_tick_start = len_tokens_total * i + i + 1

                    # 1/2
                    x_ticks.append(x_tick_start + len_tokens_total / 2)
                    # Divider
                    x_ticks.append(x_tick_start + len_tokens_total + 1)

                for search_term in search_terms_labels:
                    # 1/2
                    x_tick_labels.append(search_term)
                    # Divider
                    x_tick_labels.append('')

                labels.append(x_ticks)
                labels.append(x_tick_labels)
                labels.append(list(range(len(files) + 1)))
                labels.append([self.tr('Total')] + [file['name'] for file in reversed(files)])
                labels.append(len(files) + 1)

            elif settings['plot_settings']['sort_results_by'] == self.tr('Search Term'):
                len_search_terms_total = len(search_terms_total)

                for i, text in enumerate(texts):
                    x_tick_start = sum([len(text.tokens)
                                        for j, text in enumerate(texts)
                                        if j < i]) + j + 1

                    # 1/2
                    x_ticks.append(x_tick_start + len(text.tokens) / 2)
                    # Divider
                    x_ticks.append(x_tick_start + len(text.tokens) + 1)

                for file in files:
                    # 1/2
                    x_tick_labels.append(file['name'])
                    # Divider
                    x_tick_labels.append('')

                labels.append(x_ticks)
                labels.append(x_tick_labels)
                labels.append(list(range(len_search_terms_total)))
                labels.append(search_terms_labels)
                labels.append(len_search_terms_total)

        self.processing_finished.emit(points, labels)

@wordless_misc.log_timing
def generate_plot(main):
    def data_received(points, labels):
        if labels:
            x_ticks = labels[0]
            x_tick_labels = labels[1]
            y_ticks = labels[2]
            y_tick_labels = labels[3]
            y_max = labels[4]

        if points:
            if settings['plot_settings']['sort_results_by'] == main.tr('File'):
                matplotlib.pyplot.plot(numpy.array(points)[:, 0],
                                       numpy.array(points)[:, 1],
                                       'b|')

                matplotlib.pyplot.xlabel(main.tr('Search Terms'))
                matplotlib.pyplot.xticks(x_ticks, x_tick_labels, color = 'r')

                matplotlib.pyplot.ylabel(main.tr('Files'))
                matplotlib.pyplot.yticks(y_ticks, y_tick_labels)
                matplotlib.pyplot.ylim(-1, y_max)
            elif settings['plot_settings']['sort_results_by'] == main.tr('Search Term'):
                matplotlib.pyplot.plot(numpy.array(points)[:, 0],
                                       numpy.array(points)[:, 1],
                                       'b|')

                matplotlib.pyplot.xlabel(main.tr('Files'))
                matplotlib.pyplot.xticks(x_ticks, x_tick_labels)

                matplotlib.pyplot.ylabel(main.tr('Search Terms'))
                matplotlib.pyplot.yticks(y_ticks, y_tick_labels, color = 'r')
                matplotlib.pyplot.ylim(-1, y_max)

            matplotlib.pyplot.title(main.tr('Dispersion Plot'))
            matplotlib.pyplot.grid(True, which = 'major', axis = 'x', linestyle = 'dotted')

            wordless_message.wordless_message_generate_plot_success(main)
        else:
            wordless_message_box.wordless_message_box_no_results(main)

            wordless_message.wordless_message_generate_plot_error(main)

        dialog_processing.accept()

        if points:
            matplotlib.pyplot.get_current_fig_manager().window.showMaximized()

    settings = main.settings_custom['concordancer']
    files = main.wordless_files.get_selected_files()

    if wordless_checking_file.check_files_on_loading(main, files):
        if (not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term'] or
            settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms']):
            dialog_processing = wordless_dialog_misc.Wordless_Dialog_Processing_Generate_Data(main)

            worker_process_data = Worker_Process_Data_Plot(main, dialog_processing, data_received)
            thread_process_data = wordless_threading.Thread_Process_Data(worker_process_data)

            thread_process_data.start()

            dialog_processing.exec_()

            thread_process_data.quit()
            thread_process_data.wait()
        else:
            wordless_message_box.wordless_message_box_missing_search_term(main)

            wordless_message.wordless_message_generate_plot_error(main)
    else:
        wordless_message.wordless_message_generate_plot_error(main)
