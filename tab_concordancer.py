#
# Wordless: Concordancer
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import copy
import html

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk
import numpy
import matplotlib.pyplot

from wordless_widgets import *
from wordless_utils import *

class Wordless_Table_Concordancer(wordless_table.Wordless_Table_Data):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Left'),
                             main.tr('Node'),
                             main.tr('Right'),
                             main.tr('Token No.'),
                             main.tr('Sentence No.'),
                             main.tr('Paragraph No.'),
                             main.tr('File')
                         ],
                         headers_num = [
                             main.tr('Token No.'),
                             main.tr('Sentence No.'),
                             main.tr('Paragraph No.')
                         ],
                         headers_pct = [
                             main.tr('Token No.'),
                             main.tr('Sentence No.'),
                             main.tr('Paragraph No.')
                         ])

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
    def __init__(self, main, table):
        super().__init__(main,
                         headers = [
                             main.tr('Columns'),
                             main.tr('Order')
                         ],
                         cols_stretch = [
                             main.tr('Order')
                         ])

        self.table = table
        self.cols_sorting = [
            self.tr('File'),
            self.tr('Token No.')
        ]

        self.button_add = QPushButton(self.tr('Add'), self)
        self.button_insert = QPushButton(self.tr('Insert'), self)
        self.button_remove = QPushButton(self.tr('Remove'), self)
        self.button_clear = QPushButton(self.tr('Clear'), self)
        self.button_sort_results = QPushButton(self.tr('Sort Results in Table'), self)
    
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
                combo_box_sorting_col.blockSignals(True)
                combo_box_cur.blockSignals(True)

                combo_box_sorting_col.setStyleSheet(self.main.settings_custom['general']['style_highlight'])
                combo_box_cur.setStyleSheet(self.main.settings_custom['general']['style_highlight'])

                QMessageBox.warning(self.main,
                                    self.tr('Column Sorted More Than Once'),
                                    self.tr(f'''{self.main.settings_global["style_dialog"]}
                                        <body>
                                            <p>Please refrain from sorting the same column more than once!</p>
                                        </body>
                                    '''),
                                    QMessageBox.Ok)

                combo_box_sorting_col.setStyleSheet('')
                combo_box_cur.setStyleSheet('')

                combo_box_sorting_col.blockSignals(False)
                combo_box_cur.blockSignals(False)

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
                    self.tr('File'),
                    self.tr('Token No.'),
                    self.tr('Node')
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

    @ wordless_misc.log_timing
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
                for file_open in self.table.settings['file']['files_open']:
                    if file_open['selected'] and file_open['name'] == file:
                        lang_code = file_open['lang_code']

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

                self.table.cellWidget(i, 0).setText(wordless_text.wordless_word_detokenize(self.main, left, lang_code))
                self.table.cellWidget(i, 1).setText(node)
                self.table.cellWidget(i, 2).setText(wordless_text.wordless_word_detokenize(self.main, right, lang_code))

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

def init(main):
    def load_settings(defaults = False):
        if defaults:
            settings = copy.deepcopy(main.settings_default['concordancer'])
        else:
            settings = copy.deepcopy(main.settings_custom['concordancer'])

        # Token Settings
        checkbox_puncs.setChecked(settings['token_settings']['puncs'])

        # Search Settings
        checkbox_multi_search_mode.setChecked(settings['search_settings']['multi_search_mode'])

        if not defaults:
            line_edit_search_term.setText(settings['search_settings']['search_term'])

            for search_term in settings['search_settings']['search_terms']:
                list_search_terms.add_item(search_term)

        checkbox_ignore_case.setChecked(settings['search_settings']['ignore_case'])
        checkbox_match_inflected_forms.setChecked(settings['search_settings']['match_inflected_forms'])
        checkbox_match_whole_word.setChecked(settings['search_settings']['match_whole_word'])
        checkbox_use_regex.setChecked(settings['search_settings']['use_regex'])

        # Generation Settings
        spin_box_width_left_token.setValue(settings['generation_settings']['width_left_token'])
        spin_box_width_left_char.setValue(settings['generation_settings']['width_left_char'])
        spin_box_width_right_token.setValue(settings['generation_settings']['width_right_token'])
        spin_box_width_right_char.setValue(settings['generation_settings']['width_right_char'])
        combo_box_width_unit.setCurrentText(settings['generation_settings']['width_unit'])

        checkbox_number_lines.setChecked(settings['generation_settings']['number_lines_no_limit'])
        spin_box_number_lines.setValue(settings['generation_settings']['number_lines'])

        # Table Settings
        checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])

        # Plot Settings
        combo_box_sort_results_by.setCurrentText(settings['plot_settings']['sort_results_by'])

        # Sorting Settings
        table_concordancer_sorting.setRowCount(0)

        for sorting_col, sorting_order in settings['sorting_settings']['sorting_rules']:
            if sorting_col in [sorting_rule[0]
                               for sorting_rule in main.settings_default['concordancer']['sorting_settings']['sorting_rules']]:
                table_concordancer_sorting.add_row()

                table_concordancer_sorting.cellWidget(table_concordancer_sorting.rowCount() - 1, 0).setCurrentText(sorting_col)
                table_concordancer_sorting.cellWidget(table_concordancer_sorting.rowCount() - 1, 1).setCurrentText(sorting_order)

        token_settings_changed()
        search_settings_changed()
        generation_settings_changed()
        table_settings_changed()
        sorting_settings_changed()

    def token_settings_changed():
        settings = main.settings_custom['concordancer']['token_settings']

        settings['puncs'] = checkbox_puncs.isChecked()

    def search_settings_changed():
        settings = main.settings_custom['concordancer']['search_settings']

        settings['multi_search_mode'] = checkbox_multi_search_mode.isChecked()
        settings['search_term'] = line_edit_search_term.text()
        settings['search_terms'] = list_search_terms.get_items()

        settings['ignore_case'] = checkbox_ignore_case.isChecked()
        settings['match_inflected_forms'] = checkbox_match_inflected_forms.isChecked()
        settings['match_whole_word'] = checkbox_match_whole_word.isChecked()
        settings['use_regex'] = checkbox_use_regex.isChecked()

    def generation_settings_changed():
        settings = main.settings_custom['concordancer']['generation_settings']

        settings['width_left_token'] = spin_box_width_left_token.value()
        settings['width_left_char'] = spin_box_width_left_char.value()
        settings['width_right_token'] = spin_box_width_right_token.value()
        settings['width_right_char'] = spin_box_width_right_char.value()
        settings['width_unit'] = combo_box_width_unit.currentText()

        settings['number_lines_no_limit'] = checkbox_number_lines.isChecked()
        settings['number_lines'] = spin_box_number_lines.value()

        if settings['width_unit'] == main.tr('Token'):
            spin_box_width_left_token.show()
            spin_box_width_right_token.show()

            spin_box_width_left_char.hide()
            spin_box_width_right_char.hide()
        else:
            spin_box_width_left_token.hide()
            spin_box_width_right_token.hide()

            spin_box_width_left_char.show()
            spin_box_width_right_char.show()

        if settings['number_lines_no_limit']:
            spin_box_number_lines.setEnabled(False)
        else:
            spin_box_number_lines.setEnabled(True)

    def table_settings_changed():
        settings = main.settings_custom['concordancer']['table_settings']

        settings['show_pct'] = checkbox_show_pct.isChecked()

    def plot_settings_changed():
        settings = main.settings_custom['concordancer']['plot_settings']

        settings['sort_results_by'] = combo_box_sort_results_by.currentText()

    def sorting_settings_changed():
        settings = main.settings_custom['concordancer']['sorting_settings']

        settings['sorting_rules'] = table_concordancer_sorting.get_sorting_rules()

    tab_concordancer = wordless_layout.Wordless_Tab(main, load_settings)

    table_concordancer = Wordless_Table_Concordancer(main)

    tab_concordancer.layout_table.addWidget(table_concordancer, 0, 0, 1, 5)
    tab_concordancer.layout_table.addWidget(table_concordancer.button_generate_table, 1, 0)
    tab_concordancer.layout_table.addWidget(table_concordancer.button_generate_plot, 1, 1)
    tab_concordancer.layout_table.addWidget(table_concordancer.button_export_selected, 1, 2)
    tab_concordancer.layout_table.addWidget(table_concordancer.button_export_all, 1, 3)
    tab_concordancer.layout_table.addWidget(table_concordancer.button_clear, 1, 4)

    # Token Settings
    group_box_token_settings = QGroupBox(main.tr('Token Settings'), main)

    checkbox_puncs = QCheckBox(main.tr('Punctuations'), main)

    checkbox_puncs.stateChanged.connect(token_settings_changed)

    group_box_token_settings.setLayout(QGridLayout())
    group_box_token_settings.layout().addWidget(checkbox_puncs)

    # Search Settings
    group_box_search_settings = QGroupBox(main.tr('Search Settings'), main)

    (label_search_term,
     checkbox_multi_search_mode,
     line_edit_search_term,
     list_search_terms,

     checkbox_ignore_case,
     checkbox_match_inflected_forms,
     checkbox_match_whole_word,
     checkbox_use_regex) = wordless_widgets.wordless_widgets_search(main)

    button_context_settings = QPushButton(main.tr('Context Settings'), main)

    checkbox_multi_search_mode.stateChanged.connect(search_settings_changed)
    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(table_concordancer.button_generate_table.click)
    list_search_terms.itemChanged.connect(search_settings_changed)

    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_match_inflected_forms.stateChanged.connect(search_settings_changed)
    checkbox_match_whole_word.stateChanged.connect(search_settings_changed)
    checkbox_use_regex.stateChanged.connect(search_settings_changed)

    button_context_settings.clicked.connect(lambda: wordless_dialog.Wordless_Dialog_Context_Settings(main, tab = 'concordancer'))

    layout_search_terms = QGridLayout()
    layout_search_terms.addWidget(list_search_terms, 0, 0, 6, 1)
    layout_search_terms.addWidget(list_search_terms.button_add, 0, 1)
    layout_search_terms.addWidget(list_search_terms.button_insert, 1, 1)
    layout_search_terms.addWidget(list_search_terms.button_remove, 2, 1)
    layout_search_terms.addWidget(list_search_terms.button_clear, 3, 1)
    layout_search_terms.addWidget(list_search_terms.button_import, 4, 1)
    layout_search_terms.addWidget(list_search_terms.button_export, 5, 1)

    group_box_search_settings.setLayout(QGridLayout())
    group_box_search_settings.layout().addWidget(label_search_term, 0, 0)
    group_box_search_settings.layout().addWidget(checkbox_multi_search_mode, 0, 1, Qt.AlignRight)
    group_box_search_settings.layout().addWidget(line_edit_search_term, 1, 0, 1, 2)
    group_box_search_settings.layout().addLayout(layout_search_terms, 2, 0, 1, 2)

    group_box_search_settings.layout().addWidget(checkbox_ignore_case, 3, 0, 1, 2)
    group_box_search_settings.layout().addWidget(checkbox_match_inflected_forms, 4, 0, 1, 2)
    group_box_search_settings.layout().addWidget(checkbox_match_whole_word, 5, 0, 1, 2)
    group_box_search_settings.layout().addWidget(checkbox_use_regex, 6, 0, 1, 2)

    group_box_search_settings.layout().addWidget(button_context_settings, 7, 0, 1, 2)

    # Generation Settings
    group_box_generation_settings = QGroupBox(main.tr('Generation Settings'), main)

    label_width_left = QLabel(main.tr('Width (Left):'), main)
    spin_box_width_left_token = QSpinBox(main)
    spin_box_width_left_char = QSpinBox(main)
    label_width_right = QLabel(main.tr('Width (Right):'), main)
    spin_box_width_right_token = QSpinBox(main)
    spin_box_width_right_char = QSpinBox(main)
    label_width_unit = QLabel('Width Unit:', main)
    combo_box_width_unit = wordless_box.Wordless_Combo_Box(main)

    label_number_lines = QLabel(main.tr('Number of Lines:'), main)
    checkbox_number_lines = QCheckBox(main.tr('No Limit'), main)
    spin_box_number_lines = QSpinBox(main)

    combo_box_width_unit.addItems([main.tr('Token'), main.tr('Character')])

    spin_box_width_left_token.setRange(0, 100)
    spin_box_width_left_char.setRange(0, 1000)
    spin_box_width_right_token.setRange(0, 100)
    spin_box_width_right_char.setRange(0, 1000)

    spin_box_number_lines.setRange(1, 10000)

    spin_box_width_left_token.valueChanged.connect(generation_settings_changed)
    spin_box_width_left_char.valueChanged.connect(generation_settings_changed)
    spin_box_width_right_token.valueChanged.connect(generation_settings_changed)
    spin_box_width_right_char.valueChanged.connect(generation_settings_changed)
    combo_box_width_unit.currentTextChanged.connect(generation_settings_changed)

    checkbox_number_lines.stateChanged.connect(generation_settings_changed)
    spin_box_number_lines.valueChanged.connect(generation_settings_changed)

    group_box_generation_settings.setLayout(QGridLayout())
    group_box_generation_settings.layout().addWidget(label_width_left, 0, 0)
    group_box_generation_settings.layout().addWidget(spin_box_width_left_token, 0, 1)
    group_box_generation_settings.layout().addWidget(spin_box_width_left_char, 0, 1)
    group_box_generation_settings.layout().addWidget(label_width_right, 1, 0)
    group_box_generation_settings.layout().addWidget(spin_box_width_right_token, 1, 1)
    group_box_generation_settings.layout().addWidget(spin_box_width_right_char, 1, 1)
    group_box_generation_settings.layout().addWidget(label_width_unit, 2, 0)
    group_box_generation_settings.layout().addWidget(combo_box_width_unit, 2, 1)

    group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 3, 0, 1, 2)

    group_box_generation_settings.layout().addWidget(label_number_lines, 4, 0)
    group_box_generation_settings.layout().addWidget(checkbox_number_lines, 4, 1, Qt.AlignRight)
    group_box_generation_settings.layout().addWidget(spin_box_number_lines, 5, 0, 1, 2)

    # Table Settings
    group_box_table_settings = QGroupBox(main.tr('Table Settings'), main)

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table(main, table_concordancer)

    checkbox_show_cumulative.hide()
    checkbox_show_breakdown.hide()

    checkbox_show_pct.stateChanged.connect(table_settings_changed)

    group_box_table_settings.setLayout(QGridLayout())
    group_box_table_settings.layout().addWidget(checkbox_show_pct, 0, 0)

    # Plot Settings
    group_box_plot_settings = QGroupBox(main.tr('Plot Settings'), main)

    label_sort_results_by = QLabel(main.tr('Sort Results by:'), main)
    combo_box_sort_results_by = wordless_box.Wordless_Combo_Box(main)

    combo_box_sort_results_by.addItems([main.tr('File'), main.tr('Search Term')])

    combo_box_sort_results_by.currentTextChanged.connect(plot_settings_changed)

    group_box_plot_settings.setLayout(QGridLayout())
    group_box_plot_settings.layout().addWidget(label_sort_results_by, 0, 0)
    group_box_plot_settings.layout().addWidget(combo_box_sort_results_by, 0, 1)

    # Sorting Settings
    group_box_sorting_settings = QGroupBox(main.tr('Sorting Settings'), main)

    table_concordancer_sorting = Wordless_Table_Concordancer_Sorting(main, table = table_concordancer)

    table_concordancer_sorting.itemChanged.connect(sorting_settings_changed)

    group_box_sorting_settings.setLayout(QGridLayout())
    group_box_sorting_settings.layout().addWidget(table_concordancer_sorting, 0, 0, 1, 2)
    group_box_sorting_settings.layout().addWidget(table_concordancer_sorting.button_add, 1, 0)
    group_box_sorting_settings.layout().addWidget(table_concordancer_sorting.button_insert, 1, 1)
    group_box_sorting_settings.layout().addWidget(table_concordancer_sorting.button_remove, 2, 0)
    group_box_sorting_settings.layout().addWidget(table_concordancer_sorting.button_clear, 2, 1)
    group_box_sorting_settings.layout().addWidget(table_concordancer_sorting.button_sort_results, 3, 0, 1, 2)

    tab_concordancer.layout_settings.addWidget(group_box_token_settings, 0, 0)
    tab_concordancer.layout_settings.addWidget(group_box_search_settings, 1, 0)
    tab_concordancer.layout_settings.addWidget(group_box_generation_settings, 2, 0)
    tab_concordancer.layout_settings.addWidget(group_box_table_settings, 3, 0)
    tab_concordancer.layout_settings.addWidget(group_box_plot_settings, 4, 0)
    tab_concordancer.layout_settings.addWidget(group_box_sorting_settings, 5, 0)

    tab_concordancer.layout_settings.setRowStretch(6, 1)

    load_settings()

    return tab_concordancer

@ wordless_misc.log_timing
def generate_table(main, table):
    settings = main.settings_custom['concordancer']
    files = main.wordless_files.get_selected_files()

    if files:
        if (settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms'] or
            not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term']):
            table.clear_table(0)

            table.settings = main.settings_custom

            if settings['search_settings']['multi_search_mode']:
                search_terms = settings['search_settings']['search_terms']
            else:
                search_terms = [settings['search_settings']['search_term']]

            if settings['context_settings']['inclusion']:
                if settings['context_settings']['inclusion_multi_search_mode']:
                    search_terms_inclusion = settings['context_settings']['inclusion_search_terms']
                else:
                    if settings['context_settings']['inclusion_search_term']:
                        search_terms_inclusion = [settings['context_settings']['inclusion_search_term']]
                    else:
                        search_terms_inclusion = []

            if settings['context_settings']['exclusion']:
                if settings['context_settings']['exclusion_multi_search_mode']:
                    search_terms_exclusion = settings['context_settings']['exclusion_search_terms']
                else:
                    if settings['context_settings']['exclusion_search_term']:
                        search_terms_exclusion = [settings['context_settings']['exclusion_search_term']]
                    else:
                        search_terms_exclusion = []

            for file in files:
                text = wordless_text.Wordless_Text(main, file)

                search_terms_file = text.match_search_terms(search_terms,
                                                            settings['token_settings']['puncs'],
                                                            settings['search_settings']['ignore_case'],
                                                            settings['search_settings']['match_inflected_forms'],
                                                            settings['search_settings']['match_whole_word'],
                                                            settings['search_settings']['use_regex'])

                if settings['context_settings']['inclusion'] and search_terms_inclusion:
                    search_terms_inclusion_file = text.match_search_terms(search_terms_inclusion,
                                                                          settings['token_settings']['puncs'],
                                                                          settings['search_settings']['ignore_case'],
                                                                          settings['search_settings']['match_inflected_forms'],
                                                                          settings['search_settings']['match_whole_word'],
                                                                          settings['search_settings']['use_regex'])
                else:
                    search_terms_inclusion_file = []

                if settings['context_settings']['exclusion'] and search_terms_exclusion:
                    search_terms_exclusion_file = text.match_search_terms(search_terms_exclusion,
                                                                          settings['token_settings']['puncs'],
                                                                          settings['search_settings']['ignore_case'],
                                                                          settings['search_settings']['match_inflected_forms'],
                                                                          settings['search_settings']['match_whole_word'],
                                                                          settings['search_settings']['use_regex'])
                else:
                    search_terms_exclusion_file = []

                if not settings['token_settings']['puncs']:
                    text.tokens_no_puncs = [token for token in text.tokens if [char for char in token if char.isalnum()]]

                    text.para_offsets = []
                    text.sentence_offsets = []
                    text.tokens = []
                    text.token_offsets = []

                    for para in text.paras:
                        text.para_offsets.append(len(text.tokens))

                        for sentence in wordless_text.wordless_sentence_tokenize(main, para, file['lang_code']):
                            text.sentence_offsets.append(len(text.tokens))

                            for token in wordless_text.wordless_word_tokenize(main, sentence, file['lang_code']):
                                if text.tokens:
                                    if [char for char in token if char.isalnum()]:
                                        text.tokens.append(token)
                                        text.token_offsets.append(text.token_offsets[-1] + 1)
                                    else:
                                        text.tokens[-1] += token
                                        text.token_offsets.append(text.token_offsets[-1])
                                else:
                                    text.tokens.append(token)
                                    text.token_offsets.append(0)

                    if not text.tokens[0].isalnum():
                        text.tokens_no_puncs = [''] + text.tokens_no_puncs

                len_paras = len(text.paras)
                len_sentences = len(text.sentences)
                len_tokens = len(text.tokens)

                table.blockSignals(True)
                table.setUpdatesEnabled(False)

                if settings['token_settings']['puncs']:
                    tokens_text = text.tokens
                else:
                    tokens_text = text.tokens_no_puncs

                for search_term in search_terms_file:
                    len_search_term = len(search_term)

                    for i, ngram in enumerate(nltk.ngrams(tokens_text, len_search_term)):
                        if ngram == search_term:
                            if wordless_text.check_context(i, tokens_text,
                                                           context_settings = settings['context_settings'],
                                                           search_terms_inclusion = search_terms_inclusion_file,
                                                           search_terms_exclusion = search_terms_exclusion_file):
                                if not settings['token_settings']['puncs']:
                                    ngram = [text.tokens[i + j] for j in range(len(ngram))]

                                table.setRowCount(table.rowCount() + 1)

                                # Node
                                node_text = html.escape(wordless_text.wordless_word_detokenize(main, ngram, text.lang_code))

                                table.setCellWidget(table.rowCount() - 1, 1,
                                                    QLabel(f'''
                                                                <span style="color: {settings["sorting_settings"]["highlight_colors"][0]};
                                                                             font-weight: bold;">
                                                                    {node_text}
                                                                </span>
                                                            ''', main))

                                table.cellWidget(table.rowCount() - 1, 1).setTextFormat(Qt.RichText)
                                table.cellWidget(table.rowCount() - 1, 1).setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                                if settings['generation_settings']['width_unit'] == main.tr('Token'):
                                    context_left = text.tokens[max(0, i - settings['generation_settings']['width_left_token']) : i]
                                    context_right = text.tokens[i + len_search_term : min(i + len_search_term + settings['generation_settings']['width_right_token'], len_tokens)]
                                else:
                                    len_context_left = 0
                                    len_context_right = 0

                                    context_left = []
                                    context_right = []

                                    while len_context_left < settings['generation_settings']['width_left_char']:
                                        if i - 1 - len(context_left) < 0:
                                            break
                                        else:
                                            token_next = text.tokens[i - 1 - len(context_left)]

                                            if settings['token_settings']['puncs']:
                                                len_token_next = len(token_next)
                                            else:
                                                len_token_next = len(token_next) - len([char for char in token_next if not char.isalnum()])

                                        if len_context_left + len_token_next > settings['generation_settings']['width_left_char']:
                                            if settings['token_settings']['puncs']:
                                                context_left.insert(0, token_next[-(settings['generation_settings']['width_left_char'] - len_context_left):])
                                            else:
                                                for j, char in reversed(list(enumerate(token_next))):
                                                    token_next_seg = token_next[j:]

                                                    if len(token_next_seg) - len([char for char in token_next_seg if not char.isalnum()]) == settings['generation_settings']['width_left_char'] - len_context_left:
                                                        context_left.insert(0, token_next_seg)

                                                        break
                                        else:
                                            context_left.insert(0, token_next)

                                        len_context_left += len_token_next

                                    while len_context_right < settings['generation_settings']['width_right_char']:
                                        if i + 1 + len(context_right) > len(text.tokens) - 1:
                                            break
                                        else:
                                            token_next = text.tokens[i + len_search_term + len(context_right)]

                                            if settings['token_settings']['puncs']:
                                                len_token_next = len(token_next)
                                            else:
                                                len_token_next = len(token_next) - len([char for char in token_next if not char.isalnum()])

                                        if len_context_right + len_token_next > settings['generation_settings']['width_right_char']:
                                            if settings['token_settings']['puncs']:
                                                context_right.append(token_next[: settings['generation_settings']['width_right_char'] - len_context_right + 1])
                                            else:
                                                for j, char in enumerate(token_next):
                                                    token_next_seg = token_next[: j + 1]

                                                    if len(token_next_seg) - len([char for char in token_next_seg if not char.isalnum()]) == settings['generation_settings']['width_right_char'] - len_context_right:
                                                        context_right.append(token_next_seg)

                                                        break
                                        else:
                                            context_right.append(token_next)

                                        len_context_right += len(token_next)

                                context_left = [html.escape(token) for token in context_left]
                                context_right = [html.escape(token) for token in context_right]

                                context_left_text = wordless_text.wordless_word_detokenize(main, context_left, text.lang_code)
                                context_right_text = wordless_text.wordless_word_detokenize(main, context_right, text.lang_code)

                                # Left
                                table.setCellWidget(table.rowCount() - 1, 0,
                                                    QLabel(context_left_text, main))

                                table.cellWidget(table.rowCount() - 1, 0).setTextFormat(Qt.RichText)
                                table.cellWidget(table.rowCount() - 1, 0).setAlignment(Qt.AlignRight | Qt.AlignVCenter)

                                table.cellWidget(table.rowCount() - 1, 0).text_raw = context_left

                                # Right
                                table.setCellWidget(table.rowCount() - 1, 2,
                                                    QLabel(context_right_text, main))

                                table.cellWidget(table.rowCount() - 1, 2).setTextFormat(Qt.RichText)

                                table.cellWidget(table.rowCount() - 1, 2).text_raw = context_right

                                # Token
                                table.set_item_num_pct(table.rowCount() - 1, 3,
                                                       i + 1, len_tokens)
                                # Sentence
                                if text.sentence_offsets[-1] < i:
                                    table.set_item_num_pct(table.rowCount() - 1, 4, len_sentences, len_sentences)
                                else:
                                    for j, i_sentence in enumerate(text.sentence_offsets):
                                        if i_sentence > i:
                                            table.set_item_num_pct(table.rowCount() - 1, 4, j, len_sentences)

                                            break

                                # Paragraph
                                if text.para_offsets[-1] < i:
                                    table.set_item_num_pct(table.rowCount() - 1, 5, len_paras, len_paras)
                                else:
                                    for j, i_para in enumerate(text.para_offsets):
                                        if i_para > i:
                                            table.set_item_num_pct(table.rowCount() - 1, 5, j, len_paras)

                                            break

                                # File
                                table.setItem(table.rowCount() - 1, 6, QTableWidgetItem(file['name']))

                table.blockSignals(False)
                table.setUpdatesEnabled(True)

            if table.rowCount() > 0:
                table.toggle_pct()

                table.update_items_width()

                table.itemChanged.emit(table.item(0, 0))

                wordless_message.wordless_message_generate_table_success(main)
            else:
                table.setRowCount(1)

                wordless_message_box.wordless_message_box_no_results_table(main)

                wordless_message.wordless_message_generate_table_error(main)
        else:
            wordless_message_box.wordless_message_box_empty_search_term(main)

            wordless_message.wordless_message_generate_table_error(main)
    else:
        wordless_message_box.wordless_message_box_no_files_selected(main)

        wordless_message.wordless_message_generate_table_error(main)

def generate_plot(main):
    settings = main.settings_custom['concordancer']
    files = main.wordless_files.get_selected_files()

    if files:
        if (settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms'] or
            not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term']):
            texts = []
            search_terms_files = []
            search_terms_total = set()
            search_terms_labels = set()
            points = []

            if settings['search_settings']['multi_search_mode']:
                search_terms = settings['search_settings']['search_terms']
            else:
                search_terms = [settings['search_settings']['search_term']]

            files = sorted(files, key = lambda item: item['name'])

            for file in files:
                text = wordless_text.Wordless_Text(main, file)
                texts.append(wordless_text.Wordless_Text(main, file))

                search_terms_file = text.match_search_terms(search_terms,
                                                            settings['token_settings']['puncs'],
                                                            settings['search_settings']['ignore_case'],
                                                            settings['search_settings']['match_inflected_forms'],
                                                            settings['search_settings']['match_whole_word'],
                                                            settings['search_settings']['use_regex'])

                search_terms_files.append(sorted(search_terms_file, key = lambda item: [token for token in item]))

                for search_term in search_terms_file:
                    search_terms_total.add(search_term)
                    search_terms_labels.add(wordless_text.wordless_word_detokenize(main, search_term, text.lang_code))

            len_files = len(files)
            len_tokens_total = sum([len(text.tokens) for text in texts])
            len_search_terms_total = len(search_terms_total)

            if settings['plot_settings']['sort_results_by'] == main.tr('File'):
                search_terms_total = sorted(search_terms_total)
                search_terms_labels = sorted(search_terms_labels)

                for i, search_term in enumerate(search_terms_total):
                    len_search_term = len(search_term)

                    x_start = len_tokens_total * i + 1
                    y_start = len_files

                    for j, text in enumerate(texts):
                        x_start_total = x_start + sum([len(text.tokens)
                                                       for k, text in enumerate(texts)
                                                       if k < j])
                        len_tokens = len(text.tokens)

                        for k, ngram in enumerate(nltk.ngrams(text.tokens, len_search_term)):
                            if ngram == search_term:
                                points.append([x_start + k / len_tokens * len_tokens_total, y_start - j])
                                # Total
                                points.append([x_start_total + k, 0])

                if points:
                    x_ticks = [0]
                    x_tick_labels = ['']

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

                    matplotlib.pyplot.plot(numpy.array(points)[:, 0],
                                           numpy.array(points)[:, 1],
                                           'b|')

                    matplotlib.pyplot.xlabel(main.tr('Search Terms'))
                    matplotlib.pyplot.xticks(x_ticks, x_tick_labels, color = 'r')

                    matplotlib.pyplot.ylabel(main.tr('Files'))
                    matplotlib.pyplot.yticks(list(range(len(files) + 1)),
                                             [main.tr('Total')] + [file['name'] for file in reversed(files)])
                    matplotlib.pyplot.ylim(-1, len(files) + 1)
            else:
                search_terms_total = sorted(search_terms_total, reverse = True)
                search_terms_labels = sorted(search_terms_labels, reverse = True)

                for i, search_term in enumerate(search_terms_total):
                    len_search_term = len(search_term)

                    for j, text in enumerate(texts):
                        x_start = sum([len(text.tokens)
                                       for k, text in enumerate(texts)
                                       if k < j]) + j + 2

                        for k, ngram in enumerate(nltk.ngrams(text.tokens, len_search_term)):
                            if ngram == search_term:
                                points.append([x_start + k, i])

                if points:
                    x_ticks = [0]
                    x_tick_labels = ['']

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

                    matplotlib.pyplot.plot(numpy.array(points)[:, 0],
                                           numpy.array(points)[:, 1],
                                           'b|')

                    matplotlib.pyplot.xlabel(main.tr('Files'))
                    matplotlib.pyplot.xticks(x_ticks, x_tick_labels)

                    matplotlib.pyplot.ylabel(main.tr('Search Terms'))
                    matplotlib.pyplot.yticks(list(range(len_search_terms_total)),
                                             search_terms_labels,
                                             color = 'r')
                    matplotlib.pyplot.ylim(-1, len_search_terms_total)

            if points:
                matplotlib.pyplot.title(main.tr('Dispersion Plot'))
                matplotlib.pyplot.grid(True, which = 'major', axis = 'x', linestyle = 'dotted')
                matplotlib.pyplot.show()

                wordless_message.wordless_message_generate_plot_success(main)
            else:
                wordless_message_box.wordless_message_box_no_results_plot(main)

                wordless_message.wordless_message_generate_plot_error(main)
        else:
            wordless_message_box.wordless_message_box_empty_search_term(main)

            wordless_message.wordless_message_generate_plot_error(main)
    else:
        wordless_message_box.wordless_message_box_no_files_selected(main)

        wordless_message.wordless_message_generate_plot_error(main)
