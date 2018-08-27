#
# Wordless: Utility Functions for Tables
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Wordless_Table_Item(QTableWidgetItem):
    def fetch_text(self, item):
        if item.text():
            return item.text()
        else:
            cell_widget = item.tableWidget().cellWidget(item.row(), item.column())
            if isinstance(cell_widget, QComboBox):
                return cell_widget.currentText()
            elif isinstance(cell_widget, QLineEdit):
                return cell_widget.text()

    def __lt__(self, other):
        return self.fetch_text(self) < self.fetch_text(other)

class Wordless_Table(QTableWidget):
    def __init__(self, parent, headers, vertical_headers = False, stretch_columns = []):
        self.parent = parent
        self.headers = headers
        self.vertical_headers = vertical_headers

        if vertical_headers:
            super().__init__(len(self.headers), 1, self.parent)

            self.setVerticalHeaderLabels(self.headers)
        else:
            super().__init__(1, len(self.headers), self.parent)

            self.setHorizontalHeaderLabels(headers)

        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for column in stretch_columns:
            self.horizontalHeader().setSectionResizeMode(self.find_column(column), QHeaderView.Stretch)

        self.setStyleSheet('QHeaderView {color: #4169E1; font-weight: bold}')

        self.itemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self.selection_changed)

        self.button_export_selected = QPushButton(self.tr('Export Selected...'), self)
        self.button_export_all = QPushButton(self.tr('Export All...'), self)
        self.button_clear = QPushButton(self.tr('Clear'), self)

        self.button_export_selected.clicked.connect(self.export_selected)
        self.button_export_all.clicked.connect(self.export_all)
        self.button_clear.clicked.connect(self.clear_table)

    def insert_column(self, i, label = ''):
        super().insertColumn(i)

        self.setHorizontalHeaderItem(i, QTableWidgetItem(label))

    def setCellWidget(self, row, column, widget):
        super().setCellWidget(row, column, widget)

        self.setItem(row, column, Wordless_Table_Item(''))

    def item_changed(self):
        if self.item(0, 0) or self.cellWidget(0, 0):
            self.button_export_all.setEnabled(True)
        else:
            self.button_export_all.setEnabled(False)

        self.selection_changed()

    def selection_changed(self):
        if self.selectedIndexes() and (self.item(0, 0) or self.cellWidget(0, 0)):
            self.button_export_selected.setEnabled(True)
        else:
            self.button_export_selected.setEnabled(False)

    def fetch_selected_rows(self, descending = False):
        selected_rows = set([index.row() for index in self.selectedIndexes()])

        if descending:
            return sorted(selected_rows, reverse = True)
        else:
            return sorted(selected_rows)

    def import_table(self):
        pass

    def export_selected(self):
        pass

    def export_all(self):
        pass

    def clear_table(self):
        self.clearContents()

        if self.vertical_headers:
            self.setRowCount(len(self.headers))
            self.setColumnCount(1)

            self.setVerticalHeaderLabels(self.headers)
        else:
            self.setColumnCount(len(self.headers))
            self.setRowCount(1)

            self.setHorizontalHeaderLabels(self.headers)

        self.item_changed()

    def find_column(self, column):
        for i in range(self.columnCount()):
            if column == self.horizontalHeaderItem(i).text():
                return i

class Wordless_Table_Multi_Sort(Wordless_Table):
    def __init__(self, parent, sort_columns):
        super().__init__(parent, headers = ['Column', 'Order'], stretch_columns = ['Order'])

        self.sort_columns = sort_columns

        self.button_add = QPushButton('Add')
        self.button_insert = QPushButton('Insert')
        self.button_remove = QPushButton('Remove')
        self.button_reset = QPushButton('Reset')
    
        self.button_clear.hide()
        self.button_export_selected.hide()
        self.button_export_all.hide()
    
        self.button_add.clicked.connect(self.add_row)
        self.button_insert.clicked.connect(self.insert_row)
        self.button_remove.clicked.connect(self.remove_row)
        self.button_reset.clicked.connect(self.reset_table)

        self.reset_table()

        self.setFixedHeight(self.cellWidget(0, 0).sizeHint().height() * 5)

    def item_changed(self, item = None):
        super().item_changed()

        if self.rowCount() < len(self.sort_columns):
            self.button_add.setEnabled(True)
        else:
            self.button_add.setEnabled(False)

        if type(item) == QComboBox and item.currentText() not in ['Ascending', 'Descending']:
            for i in range(self.rowCount()):
                combobox_current = self.cellWidget(i, 0)

                if item != combobox_current and item.currentText() == combobox_current.currentText():
                    item.setStyleSheet(self.settings['general']['style_highlight'])
                    combobox_current.setStyleSheet(self.parent.settings['general']['style_highlight'])

                    QMessageBox.warning(self.parent,
                                        'Column Sorted More Than Once',
                                        'Please refrain from sorting the same column more than once.',
                                        QMessageBox.Ok)

                    item.setStyleSheet('')
                    combobox_current.setStyleSheet('')

                    item.setCurrentText(item.old_text)
                    item.showPopup()

                    return

            item.old_text = item.currentText()

        if type(item) == QComboBox:
            self.sort()

    def selection_changed(self):
        if self.selectedIndexes() and self.rowCount() < len(self.sort_columns):
            self.button_insert.setEnabled(True)
        else:
            self.button_insert.setEnabled(False)

        if self.selectedIndexes() and self.rowCount() > 1:
            self.button_remove.setEnabled(True)
        else:
            self.button_remove.setEnabled(False)

    def update_sort_columns(self, sort_columns_new):
        sort_columns_old = self.sort_columns
        self.sort_columns = sort_columns_new

        for i in reversed(range(self.rowCount())):
            sort_column = self.cellWidget(i, 0)

            if len(sort_columns_new) < len(sort_columns_old):
                if sort_column.currentText() in sort_columns_new:
                    for j in reversed(range(sort_column.count())):
                        if j > len(sort_columns_new) - 1:
                            sort_column.removeItem(j)
                else:
                    self.removeRow(i)
            elif len(sort_columns_new) > len(sort_columns_old):
                sort_column.addItems(sort_columns_new[-(len(sort_columns_new) - len(sort_columns_old)):])

        if self.rowCount() == 0:
            self.reset_table()

    def sort(self):
        pass

    def _new_row(self):
        combobox_sort_column = QComboBox(self)
        combobox_sort_order = QComboBox(self)

        combobox_sort_column.addItems(self.sort_columns)
        combobox_sort_order.addItems(['Ascending', 'Descending'])

        for i in range(combobox_sort_column.count()):
            text = combobox_sort_column.itemText(i)

            if text not in [self.cellWidget(j, 0).currentText() for j in range(self.rowCount())]:
                combobox_sort_column.setCurrentText(text)
                combobox_sort_column.old_text = text

                break

        combobox_sort_column.currentTextChanged.connect(lambda: self.item_changed(combobox_sort_column))
        combobox_sort_order.currentTextChanged.connect(lambda: self.item_changed(combobox_sort_column))

        return (combobox_sort_column, combobox_sort_order)

    def add_row(self):
        combobox_sort_column, combobox_sort_order = self._new_row()
        
        self.setRowCount(self.rowCount() + 1)
        self.setCellWidget(self.rowCount() - 1, 0, combobox_sort_column)
        self.setCellWidget(self.rowCount() - 1, 1, combobox_sort_order)

        self.sort()

    def insert_row(self):
        row = self.fetch_selected_rows()[0]

        combobox_sort_column, combobox_sort_order = self._new_row()

        self.insertRow(row)

        self.setCellWidget(row, 0, combobox_sort_column)
        self.setCellWidget(row, 1, combobox_sort_order)

        self.sort()

    def remove_row(self):
        for i in self.fetch_selected_rows(descending = True):
            self.removeRow(i)

        self.sort()

    def reset_table(self):
        self.clearContents()
        self.setRowCount(0)

        self.add_row()
