#
# Wordless: Concordancer
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import nltk

from wordless_widgets import *
from wordless_utils import *

class Wordless_Table_Multi_Sort_Concordancer(wordless_table.Wordless_Table_Multi_Sort):
    def sort(self, sort_by = None):
        if isinstance(self.main, QGroupBox):
            print(self)
        if sort_by:
            self.main.settings_custom['concordancer']['multi_sort_by'] = [sort_by]
        else:
            self.main.settings_custom['concordancer']['multi_sort_by'] = []

            for i in range(self.rowCount()):
                self.main.settings_custom['concordancer']['multi_sort_by'].append([self.cellWidget(i, 0).currentText(),
                                                                              self.cellWidget(i, 1).currentText()])

        if self.sort_table.item(0, 0):
            multi_sort_by = self.main.settings_custom['concordancer']['multi_sort_by']
            multi_sort_colors = self.main.settings_custom['concordancer']['multi_sort_colors']
            width_left = (len(self.sort_columns) - 2) // 2
            width_right = len(self.sort_columns) - 2 - width_left
            columns_left = []
            columns_right = []

            for i, (sort_column, sort_order) in reversed(list(enumerate(multi_sort_by))):
                # Sort by "File Name" after sorting by "Offset"
                if sort_column == 'Offset':
                    multi_sort_by.insert(i, ['File Name', 'Ascending'])

                if sort_column not in ['Offset', 'Query']:
                    if sort_column[0] == 'L':
                        columns_left.append(int(sort_column[1:]))
                    else:
                        columns_right.append(int(sort_column[1:]))

            # Insert blank columns
            column_left  = self.sort_table.find_column('Offset') + 1
            for i in range(width_left - 1):
                self.sort_table.insert_column(column_left + 1)

            column_right = self.sort_table.find_column('Query') + 1
            for i in range(width_right - 1):
                self.sort_table.insert_column(column_right)

            # Add concordance results
            column_left  = self.sort_table.find_column('Offset') + 1
            column_query = self.sort_table.find_column('Query')
            column_right = self.sort_table.find_column('Query') + 1

            for row in range(self.sort_table.rowCount()):
                tokens_left = []
                tokens_left_temp = []
                tokens_right = []
                tokens_right_temp = []

                current_column_left = column_left
                current_column_right = column_right

                # Clear previous concordance results
                for column in range(column_left, column_query):
                    if self.sort_table.item(row, column):
                        tokens_left.extend(self.sort_table.item(row, column).text().split())
                        self.sort_table.takeItem(row, column)

                for column in range(column_query + 1, self.sort_table.columnCount()):
                    if self.sort_table.item(row, column):
                        tokens_right.extend(self.sort_table.item(row, column).text().split())
                        self.sort_table.takeItem(row, column)

                if not self.sort_table.punctuations:
                    for i, token in reversed(list(enumerate(tokens_left))):
                        if not any(map(str.isalnum, token)):
                            tokens_left[i - 1] += ' ' + tokens_left[i]

                            del tokens_left[i]

                    for i, token in reversed(list(enumerate(tokens_right))):
                        if not any(map(str.isalnum, token)):
                            tokens_right[i - 1] += ' ' + tokens_right[i]

                            del tokens_right[i]
                
                for i, token in enumerate(tokens_left):
                    if width_left - i in columns_left:
                        if tokens_left_temp:
                            self.sort_table.setItem(row, current_column_left, QTableWidgetItem(' '.join(tokens_left_temp)))
                            self.sort_table.horizontalHeaderItem(current_column_left).setText('Left')

                            current_column_left += 1
                            tokens_left_temp.clear()

                        self.sort_table.setItem(row, current_column_left, QTableWidgetItem(token))
                        self.sort_table.horizontalHeaderItem(current_column_left).setText('L' + str(width_left - i))

                        current_column_left += 1
                    else:
                        tokens_left_temp.append(token)

                        if i == len(tokens_left) - 1:
                            self.sort_table.setItem(row, current_column_left, QTableWidgetItem(' '.join(tokens_left_temp)))
                            self.sort_table.horizontalHeaderItem(current_column_left).setText('Left')

                for i, token in enumerate(tokens_right):
                    if i + 1 in columns_right:
                        if tokens_right_temp:
                            self.sort_table.setItem(row, current_column_right, QTableWidgetItem(' '.join(tokens_right_temp)))
                            self.sort_table.horizontalHeaderItem(current_column_right).setText('Right')

                            current_column_right += 1
                            tokens_right_temp.clear()

                        self.sort_table.setItem(row, current_column_right, QTableWidgetItem(token))
                        self.sort_table.horizontalHeaderItem(current_column_right).setText('R' + str(i + 1))

                        current_column_right += 1
                    else:
                        tokens_right_temp.append(token)

                        if i == len(tokens_right) - 1:
                            self.sort_table.setItem(row, current_column_right, QTableWidgetItem(' '.join(tokens_right_temp)))
                            self.sort_table.horizontalHeaderItem(current_column_right).setText('Right')

            # Remove blank columns
            for i in reversed(range(self.sort_table.columnCount())):
                if self.sort_table.item(0, i) == None:
                    self.sort_table.removeColumn(i)

            # Style concordance results
            column_left = self.sort_table.find_column('Offset') + 1
            column_query = self.sort_table.find_column('Query')
            column_right = self.sort_table.find_column('Query') + 1

            for column in range(column_left, column_query):
                for row in range(self.sort_table.rowCount()):
                    self.sort_table.item(row, column).setFont(QFont('Consolas'))
                    self.sort_table.item(row, column).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            for row in range(self.sort_table.rowCount()):
                self.sort_table.item(row, column_query).setFont(QFont('Consolas'))
                self.sort_table.item(row, column_query).setForeground(QBrush(QColor(multi_sort_colors[0])))
                self.sort_table.item(row, column_query).setTextAlignment(Qt.AlignCenter)

            for column in range(column_right, self.sort_table.columnCount()):
                for row in range(self.sort_table.rowCount()):
                    self.sort_table.item(row, column).setFont(QFont('Consolas'))
                    self.sort_table.item(row, column).setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            for i, sort_column in enumerate([sort_column
                                             for sort_column, _ in multi_sort_by
                                             if sort_column    not in ['File Name', 'Offset', 'Query']]):
                for row in range(self.sort_table.rowCount()):
                    self.sort_table.item(row, self.sort_table.find_column(sort_column)).setForeground(QBrush(QColor(multi_sort_colors[(i + 1) % len(multi_sort_colors)])))

            for sort_column, sort_order in reversed(multi_sort_by):
                if sort_order == 'In Ascending Order' or sort_order == 'Ascending':
                    self.sort_table.sortByColumn(self.sort_table.find_column(sort_column), Qt.AscendingOrder)
                else:
                    self.sort_table.sortByColumn(self.sort_table.find_column(sort_column), Qt.DescendingOrder)

def init(self):
    def token_settings_changed():
        self.settings_custom['concordancer']['punctuations'] = checkbox_punctuations.isChecked()

    def search_settings_changed():
        self.settings_custom['concordancer']['search_term'] = line_edit_search_term.text()
        self.settings_custom['concordancer']['search_terms'] = list_search_terms.get_items()
        self.settings_custom['concordancer']['ignore_case'] = checkbox_ignore_case.isChecked()
        self.settings_custom['concordancer']['lemmatized_forms'] = checkbox_lemmatized_forms.isChecked()
        self.settings_custom['concordancer']['whole_word'] = checkbox_whole_word.isChecked()
        self.settings_custom['concordancer']['regex'] = checkbox_regex.isChecked()
        self.settings_custom['concordancer']['multi_search'] = checkbox_multi_search.isChecked()

        self.settings_custom['concordancer']['line_width_mode'] = combo_box_line_width.currentText()
        self.settings_custom['concordancer']['line_width_char'] = spin_box_line_width_char.value()
        self.settings_custom['concordancer']['line_width_token'] = spin_box_line_width_token.value()
        self.settings_custom['concordancer']['number_lines'] = None if checkbox_number_lines.isChecked() else spin_box_number_lines.value()
        self.settings_custom['concordancer']['number_lines_no_limit'] = checkbox_number_lines.isChecked()
        
        if self.settings_custom['concordancer']['multi_search']:
            line_edit_search_term.hide()

            list_search_terms.show()
            list_search_terms.button_add.show()
            list_search_terms.button_insert.show()
            list_search_terms.button_remove.show()
            list_search_terms.button_clear.show()
            list_search_terms.button_import.show()
            list_search_terms.button_export.show()

            if self.settings_custom['concordancer']['search_term'] and self.settings_custom['concordancer']['search_terms'] == []:
                list_search_terms.add_item()
                list_search_terms.item(0).setText(self.settings_custom['concordancer']['search_term'])
        else:
            line_edit_search_term.show()

            list_search_terms.hide()
            list_search_terms.button_add.hide()
            list_search_terms.button_insert.hide()
            list_search_terms.button_remove.hide()
            list_search_terms.button_clear.hide()
            list_search_terms.button_import.hide()
            list_search_terms.button_export.hide()

        if self.settings_custom['concordancer']['line_width_mode'] == 'Characters':
            spin_box_line_width_char.show()
            spin_box_line_width_token.hide()
        else:
            spin_box_line_width_char.hide()
            spin_box_line_width_token.show()

        if self.settings_custom['concordancer']['number_lines_no_limit']:
            spin_box_number_lines.setEnabled(False)
        else:
            spin_box_number_lines.setEnabled(True)

    def sorting_settings_changed():
        self.settings_custom['concordancer']['sort_by'][0] = combo_box_sort_column.currentText()
        self.settings_custom['concordancer']['sort_by'][1] = combo_box_sort_order.currentText()
        self.settings_custom['concordancer']['multi_sort'] = checkbox_multi_sort.isChecked()

        if self.settings_custom['concordancer']['multi_sort']:
            combo_box_sort_column.hide()
            combo_box_sort_order.hide()

            table_multi_sort.show()
            table_multi_sort.button_add.show()
            table_multi_sort.button_insert.show()
            table_multi_sort.button_remove.show()
            table_multi_sort.button_reset.show()

            table_multi_sort.sort()
        else:
            combo_box_sort_column.show()
            combo_box_sort_order.show()

            table_multi_sort.hide()
            table_multi_sort.button_add.hide()
            table_multi_sort.button_insert.hide()
            table_multi_sort.button_remove.hide()
            table_multi_sort.button_reset.hide()

            table_multi_sort.sort(sort_by = self.settings_custom['concordancer']['sort_by'])

    def restore_defaults():
        checkbox_punctuations.setChecked(self.settings_default['concordancer']['punctuations'])

        line_edit_search_term.setText(self.settings_default['concordancer']['search_term'])
        list_search_terms.clear()
        list_search_terms.addItems(self.settings_default['concordancer']['search_terms'])
        checkbox_ignore_case.setChecked(self.settings_default['concordancer']['ignore_case'])
        checkbox_lemmatized_forms.setChecked(self.settings_default['concordancer']['lemmatized_forms'])
        checkbox_whole_word.setChecked(self.settings_default['concordancer']['whole_word'])
        checkbox_regex.setChecked(self.settings_default['concordancer']['regex'])
        checkbox_multi_search.setChecked(self.settings_default['concordancer']['multi_search'])

        spin_box_line_width_char.setValue(self.settings_default['concordancer']['line_width_char'])
        spin_box_line_width_token.setValue(self.settings_default['concordancer']['line_width_token'])
        combo_box_line_width.setCurrentText(self.settings_default['concordancer']['line_width_mode'])
        spin_box_number_lines.setValue(self.settings_default['concordancer']['number_lines'])
        checkbox_number_lines.setChecked(self.settings_default['concordancer']['number_lines_no_limit'])

        combo_box_sort_column.setCurrentText(self.settings_default['concordancer']['sort_by'][0])
        combo_box_sort_order.setCurrentText(self.settings_default['concordancer']['sort_by'][1])
        checkbox_multi_sort.setChecked(self.settings_default['concordancer']['multi_sort'])

        token_settings_changed()
        search_settings_changed()
        sorting_settings_changed()

        table_multi_sort.reset_table()

    tab_concordancer = wordless_layout.Wordless_Tab(self, self.tr('Concordancer'))

    table_concordancer = wordless_table.Wordless_Table_Data(self,
                                                            headers = [
                                                                self.tr('File Name'),
                                                                self.tr('Offset'),
                                                                self.tr('Left'),
                                                                self.tr('Query'),
                                                                self.tr('Right')
                                                            ])

    table_concordancer.button_search = QPushButton(self.tr('Begin Search'), self)
    table_concordancer.button_generate_plot = QPushButton(self.tr('Generate Plot'), self)

    table_concordancer.button_search.clicked.connect(lambda: search(self, table_concordancer,
                                                                    combo_box_sort_column, table_multi_sort))
    table_concordancer.button_generate_plot.clicked.connect(lambda: generate_plot(self))

    tab_concordancer.layout_table.addWidget(table_concordancer, 0, 0, 1, 5)
    tab_concordancer.layout_table.addWidget(table_concordancer.button_search, 1, 0)
    tab_concordancer.layout_table.addWidget(table_concordancer.button_generate_plot, 1, 1)
    tab_concordancer.layout_table.addWidget(table_concordancer.button_export_selected, 1, 2)
    tab_concordancer.layout_table.addWidget(table_concordancer.button_export_all, 1, 3)
    tab_concordancer.layout_table.addWidget(table_concordancer.button_clear, 1, 4)

    # Token Settings
    group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

    checkbox_punctuations = QCheckBox(self.tr('Punctuations'), self)

    checkbox_punctuations.stateChanged.connect(token_settings_changed)

    layout_token_settings = QGridLayout()
    layout_token_settings.addWidget(checkbox_punctuations)

    group_box_token_settings.setLayout(layout_token_settings)

    # Search Settings
    group_box_search_settings = QGroupBox(self.tr('Search Settings'), self)

    label_search_term = QLabel(self.tr('Search Term(s):'), self)
    line_edit_search_term = QLineEdit(self)
    list_search_terms = wordless_list.Wordless_List(self)
    checkbox_ignore_case = QCheckBox(self.tr('Ignore Case'), self)
    checkbox_lemmatized_forms = QCheckBox(self.tr('Match All Lemmatized Forms'), self)
    checkbox_whole_word = QCheckBox(self.tr('Match Whole Word Only'), self)
    checkbox_regex = QCheckBox(self.tr('Use Regular Expression'), self)
    checkbox_multi_search = QCheckBox(self.tr('Multi-search Mode'), self)

    label_line_width = QLabel(self.tr('Line Width:'), self)
    spin_box_line_width_char = QSpinBox(self)
    spin_box_line_width_token = QSpinBox(self)
    combo_box_line_width = QComboBox(self)

    label_number_lines = QLabel(self.tr('Number of Lines:'), self)
    spin_box_number_lines = QSpinBox(self)
    checkbox_number_lines = QCheckBox(self.tr('No Limit'), self)

    combo_box_line_width.addItems([self.tr('Tokens'), self.tr('Characters')])

    spin_box_line_width_char.setRange(1, 1000)
    spin_box_line_width_token.setRange(1, 100)
    spin_box_number_lines.setRange(1, 10000)

    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(table_concordancer.button_search.click)
    list_search_terms.itemChanged.connect(search_settings_changed)
    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_lemmatized_forms.stateChanged.connect(search_settings_changed)
    checkbox_whole_word.stateChanged.connect(search_settings_changed)
    checkbox_regex.stateChanged.connect(search_settings_changed)
    checkbox_multi_search.stateChanged.connect(search_settings_changed)

    spin_box_line_width_char.valueChanged.connect(search_settings_changed)
    spin_box_line_width_token.valueChanged.connect(search_settings_changed)
    combo_box_line_width.currentTextChanged.connect(search_settings_changed)

    spin_box_number_lines.valueChanged.connect(search_settings_changed)
    checkbox_number_lines.stateChanged.connect(search_settings_changed)

    layout_search_terms = QGridLayout()
    layout_search_terms.addWidget(list_search_terms, 0, 0, 6, 1)
    layout_search_terms.addWidget(list_search_terms.button_add, 0, 1)
    layout_search_terms.addWidget(list_search_terms.button_insert, 1, 1)
    layout_search_terms.addWidget(list_search_terms.button_remove, 2, 1)
    layout_search_terms.addWidget(list_search_terms.button_clear, 3, 1)
    layout_search_terms.addWidget(list_search_terms.button_import, 4, 1)
    layout_search_terms.addWidget(list_search_terms.button_export, 5, 1)

    layout_search_settings = QGridLayout()
    layout_search_settings.addWidget(label_search_term, 0, 0, 1, 2)
    layout_search_settings.addWidget(line_edit_search_term, 1, 0, 1, 2)
    layout_search_settings.addLayout(layout_search_terms, 2, 0, 1, 2)
    layout_search_settings.addWidget(checkbox_ignore_case, 3, 0, 1, 2)
    layout_search_settings.addWidget(checkbox_lemmatized_forms, 4, 0, 1, 2)
    layout_search_settings.addWidget(checkbox_whole_word, 5, 0, 1, 2)
    layout_search_settings.addWidget(checkbox_regex, 6, 0, 1, 2)
    layout_search_settings.addWidget(checkbox_multi_search, 7, 0, 1, 2)

    layout_search_settings.addWidget(label_line_width, 8, 0, 1, 2)
    layout_search_settings.addWidget(spin_box_line_width_char, 9, 0)
    layout_search_settings.addWidget(spin_box_line_width_token, 9, 0)
    layout_search_settings.addWidget(combo_box_line_width, 9, 1)

    layout_search_settings.addWidget(label_number_lines, 10, 0, 1, 2)
    layout_search_settings.addWidget(spin_box_number_lines, 11, 0)
    layout_search_settings.addWidget(checkbox_number_lines, 11, 1)

    group_box_search_settings.setLayout(layout_search_settings)

    # Sorting Settings
    group_box_sorting_settings = QGroupBox(self.tr('Sorting Settings'), self)

    label_sort = QLabel(self.tr('Sort Results by:'), self)
    combo_box_sort_column = QComboBox(self)
    combo_box_sort_order = QComboBox(self)
    checkbox_multi_sort = QCheckBox(self.tr('Multi-column Sorting'), self)

    combo_box_sort_column.addItems(['Offset', 'Query'])
    combo_box_sort_order.addItems(['In Ascending Order', 'In Descending Order'])

    combo_box_sort_column.currentTextChanged.connect(sorting_settings_changed)
    combo_box_sort_order.currentTextChanged.connect(sorting_settings_changed)
    checkbox_multi_sort.stateChanged.connect(sorting_settings_changed)

    # Multi-sort
    table_multi_sort = Wordless_Table_Multi_Sort_Concordancer(self,
                                                              sort_table = table_concordancer,
                                                              sort_cols = ['Offset', 'Query'])

    layout_multi_sort = QGridLayout()
    layout_multi_sort.addWidget(table_multi_sort, 0, 0, 1, 2)
    layout_multi_sort.addWidget(table_multi_sort.button_add, 1, 0)
    layout_multi_sort.addWidget(table_multi_sort.button_insert, 1, 1)
    layout_multi_sort.addWidget(table_multi_sort.button_remove, 2, 0)
    layout_multi_sort.addWidget(table_multi_sort.button_reset, 2, 1)

    layout_sorting_settings = QGridLayout()
    layout_sorting_settings.addWidget(label_sort, 0, 0, 1, 2)
    layout_sorting_settings.addWidget(combo_box_sort_column, 1, 0)
    layout_sorting_settings.addWidget(combo_box_sort_order, 1, 1)
    layout_sorting_settings.addLayout(layout_multi_sort, 2, 0, 1, 2)
    layout_sorting_settings.addWidget(checkbox_multi_sort, 3, 0, 1, 2)

    group_box_sorting_settings.setLayout(layout_sorting_settings)

    tab_concordancer.layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    tab_concordancer.layout_settings.addWidget(group_box_search_settings, 1, 0, Qt.AlignTop)
    tab_concordancer.layout_settings.addWidget(group_box_sorting_settings, 2, 0, Qt.AlignTop)

    restore_defaults()

    return tab_concordancer

def search(self, table, combo_box_sort, table_multi_sort):
    if self.settings_custom['concordancer']['multi_search']:
        search_terms = self.settings_custom['concordancer']['search_terms']
    else:
        search_terms = [self.settings_custom['concordancer']['search_term']]

    if search_terms and search_terms[0]:
        files = wordless_misc.fetch_files(self)

        if files:
            table.clear_table()
            table.setRowCount(0)

            for file in files:
                text = wordless_text.Wordless_Text(file)

                if self.settings_custom['concordancer']['line_width_mode'] == 'Tokens':
                    width = self.settings_custom['concordancer']['line_width_token'] * 4
                    width_left = (self.settings_custom['concordancer']['line_width_token'] - 1) // 2
                    width_right = self.settings_custom['concordancer']['line_width_token'] - 1 - width_left
                else:
                    width = self.settings_custom['concordancer']['line_width_char']

                table.punctuations = self.settings_custom['concordancer']['punctuations']

                for search_term in text.match_tokens(search_terms,
                                                     self.settings_custom['concordancer']['ignore_case'],
                                                     self.settings_custom['concordancer']['lemmatized_forms'],
                                                     self.settings_custom['concordancer']['whole_word'],
                                                     self.settings_custom['concordancer']['regex']):
                    for concordance_line in text.concordance_list(search_term,
                                                                  width,
                                                                  self.settings_custom['concordancer']['number_lines'],
                                                                  self.settings_custom['concordancer']['punctuations']):
                        table.setRowCount(table.rowCount() + 1)
                        table.setItem(table.rowCount() - 1, 0, QTableWidgetItem(file.name))
                        table.setItem(table.rowCount() - 1, 1, QTableWidgetItem())
                        table.item(table.rowCount() - 1, 1).setData(Qt.DisplayRole, concordance_line.offset)
                        if self.settings_custom['concordancer']['line_width_mode'] == 'Tokens':
                            table.setItem(table.rowCount() - 1, 2, QTableWidgetItem(file.delimiter.join(concordance_line.left[-width_left:])))
                            table.setItem(table.rowCount() - 1, 3, QTableWidgetItem(concordance_line.query))
                            table.setItem(table.rowCount() - 1, 4, QTableWidgetItem(file.delimiter.join(concordance_line.right[:width_right])))
                        else:
                            table.setItem(table.rowCount() - 1, 2, QTableWidgetItem(concordance_line.left_print))
                            table.setItem(table.rowCount() - 1, 3, QTableWidgetItem(concordance_line.query))
                            table.setItem(table.rowCount() - 1, 4, QTableWidgetItem(concordance_line.right_print))

            if table.rowCount() > 0:
                # Update sorting settings
                sort_columns_new = ['Offset', 'Query']

                if self.settings_custom['concordancer']['line_width_mode'] == 'Tokens':
                    line_width = self.settings_custom['concordancer']['line_width_token']
                else:
                    line_width = self.settings_custom['concordancer']['line_width_char'] // 10

                for i in range(line_width - 1):
                    if i % 2 == 0:
                        sort_columns_new.append('R' + str(i // 2 + 1))
                    else:
                        sort_columns_new.append('L' + str(i // 2 + 1))

                if len(sort_columns_new) < combo_box_sort.count():
                    if combo_box_sort.currentText() in sort_columns_new:
                        for j in reversed(range(combo_box_sort.count())):
                            if j > len(sort_columns_new) - 1:
                                combo_box_sort.removeItem(j)
                    else:
                        combo_box_sort.setCurrentIndex(0)
                elif len(sort_columns_new) > combo_box_sort.count():
                    combo_box_sort.addItems(sort_columns_new[-(len(sort_columns_new) - combo_box_sort.count()):])

                table_multi_sort.update_sort_columns(sort_columns_new)

                if self.settings_custom['concordancer']['multi_sort']:
                    table_multi_sort.sort()
                else:
                    table_multi_sort.sort(self.settings_custom['concordancer']['sort_by'])
            else:
                table.clear_table()

                QMessageBox.information(self,
                                        self.tr('No Search Results'),
                                        self.tr('There are no results for your search!<br>You might want to change your search term(s) and/or settings.'),
                                        QMessageBox.Ok)
    else:
        QMessageBox.warning(self,
                            self.tr('Search Failed'),
                            self.tr('Please enter your search term(s) first!'),
                            QMessageBox.Ok)

    self.status_bar.showMessage('Done!')

def generate_plot(self):
    if self.settings_custom['concordancer']['multi_search']:
        search_terms = self.settings_custom['concordancer']['search_terms']
    else:
        search_terms = [self.settings_custom['concordancer']['search_term']]

    if search_terms:
        files = wordless_utils.fetch_files(self)

        if files:
            for file in wordless_utils.fetch_files(self):
                text = wordless_text.Wordless_Text(file)
                text.dispersion_plot(search_terms)
    else:
        QMessageBox.warning(self,
                            self.tr('Search Failed'),
                            self.tr('Please enter your search term(s) first!'),
                            QMessageBox.Ok)

    self.status_bar.showMessage('Done!')
