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

from wordless_utils import wordless_widgets

class Wordless_Table_Item(QTableWidgetItem):
    def read_data(self):
        item_text = self.text()

        if item_text:
            if self.column() in self.tableWidget().cols_pct:
                return self.raw_value
            else:
                try:
                    return float(item_text)
                except:
                    return item_text
        else:
            cell_widget = self.tableWidget().cellWidget(self.row(), self.column())

            if isinstance(cell_widget, QComboBox):
                return cell_widget.currentText()
            elif isinstance(cell_widget, QLineEdit):
                return cell_widget.text()

    def __lt__(self, other):
        return self.read_data() < other.read_data()

class Wordless_Table(QTableWidget):
    def __init__(self, parent, headers, orientation = 'Horizontal', cols_stretch = [], drag_drop_enabled = False):
        self.main = parent
        self.headers = headers
        self.orientation = orientation
        self.show_pct = True
        self.cols_pct = []
        self.filters = []

        if orientation == 'Horizontal':
            super().__init__(1, len(self.headers), self.main)

            self.setHorizontalHeaderLabels(headers)
        else:
            super().__init__(len(self.headers), 1, self.main)

            self.setVerticalHeaderLabels(self.headers)

        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)

        if drag_drop_enabled:
            self.setDragEnabled(True)
            self.setAcceptDrops(True)
            self.viewport().setAcceptDrops(True)
            self.setDragDropMode(QAbstractItemView.InternalMove)
            self.setDragDropOverwriteMode(False)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for column in cols_stretch:
            self.horizontalHeader().setSectionResizeMode(self.find_column(column), QHeaderView.Stretch)

        self.setStyleSheet('QHeaderView {color: #4169E1; font-weight: bold}')

        self.itemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self.selection_changed)
        if orientation == 'Horizontal':
            self.horizontalHeader().sortIndicatorChanged.connect(self.sorting_changed)
        else:
            self.verticalHeader().sortIndicatorChanged.connect(self.sorting_changed)

        self.button_export_selected = QPushButton(self.tr('Export Selected...'), self)
        self.button_export_all = QPushButton(self.tr('Export All...'), self)
        self.button_clear = QPushButton(self.tr('Clear'), self)

        self.button_export_selected.clicked.connect(self.export_selected)
        self.button_export_all.clicked.connect(self.export_all)
        self.button_clear.clicked.connect(lambda: self.clear_table())

        self.clear_table()

    def setCellWidget(self, row, column, widget):
        super().setCellWidget(row, column, widget)

        self.setItem(row, column, Wordless_Table_Item(''))

    def insert_column(self, i, label = ''):
        super().insertColumn(i)

        self.setHorizontalHeaderItem(i, QTableWidgetItem(label))

    def set_item_data(self, row, column, value, value_max):
        precision = self.main.settings['general']['precision']
        len_value = len('{:.{precision}f}'.format(value_max, precision = precision))

        item = Wordless_Table_Item()

        item.setText('{:>{len_value}.{precision}f}'.format(value, len_value = len_value, precision = precision))

        item.setFont(QFont(self.main.settings['general']['font_monospaced']))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        super().setItem(row, column, item)

    def set_item_with_pct(self, row, column, value, total, show_pct = True):
        precision = self.main.settings['general']['precision']
        len_value = len('{:,}'.format(total))
        len_pct = 5 + precision

        item = Wordless_Table_Item()

        item.raw_value = value
        item.raw_total = total

        if total == 0:
            ratio = value
        else:
            ratio = value / total

        if show_pct:
            item.setText('{:>{len_value},}/{:<{len_pct}.{precision}%}'.format(value, ratio,
                                                                              len_value = len_value,
                                                                              len_pct = len_pct,
                                                                              precision = precision))
        else:
            item.setText('{:>{len_value},}'.format(value, len_value = len_value))

        item.setFont(QFont(self.main.settings['general']['font_monospaced']))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        super().setItem(row, column, item)

    def item_changed(self):
        if self.item(0, 0):
            self.button_export_all.setEnabled(True)
        else:
            self.button_export_all.setEnabled(False)

        self.selection_changed()

    def selection_changed(self):
        if self.selectedIndexes() and self.item(0, 0):
            self.button_export_selected.setEnabled(True)
        else:
            self.button_export_selected.setEnabled(False)

    def dropEvent(self, event):
        rows_dragged = []

        if self.indexAt(event.pos()).row() == -1:
            row_dropped = self.rowCount()
        else:
            row_dropped = self.indexAt(event.pos()).row()

        selected_rows = self.selected_rows()

        for row in selected_rows:
            rows_dragged.append([])

            for column in range(self.columnCount()):
                item_text = self.item(row, column).text()

                if item_text:
                    rows_dragged[-1].append(self.takeItem(row, column))
                else:
                    rows_dragged[-1].append(self.cellWidget(row, column))

        for i in reversed(selected_rows):
            self.removeRow(i)

            if i < row_dropped:
                row_dropped -= 1

        for row, items in enumerate(rows_dragged):
            self.insertRow(row_dropped + row)

            for column, item in enumerate(items):
                if isinstance(item, QTableWidgetItem):
                    self.setItem(row_dropped + row, column, item)
                elif isinstance(item, QComboBox):
                    item_combo_box = wordless_widgets.Wordless_Combo_Box(self.main)
                    item_combo_box.addItems([item.itemText(i) for i in range(item.count())])
                    item_combo_box.setCurrentText(item.currentText())

                    self.setCellWidget(row_dropped + row, column, item_combo_box)

                self.item(row, column).setSelected(True)

        event.accept()

    def sorting_changed(self, logicalIndex, order):
        rank_prev = 1
        data_prev = ''

        col_rank = self.find_column(self.tr('Rank'))
        cols_cumulative = self.find_columns_cumulative()

        self.hide()
        self.blockSignals(True)
        self.setSortingEnabled(False)
        self.sortItems(logicalIndex, order)

        # Do not re-calculate rank if the sorted column itself contains rank
        if logicalIndex != col_rank:
            for row in range(self.rowCount()):
                if not self.isRowHidden(row):
                    data_cur = self.item(row, logicalIndex).read_data()

                    self.setItem(row, col_rank, Wordless_Table_Item())

                    if data_cur == data_prev:
                        self.item(row, col_rank).setData(Qt.DisplayRole, self.item(row - 1, col_rank).data(Qt.DisplayRole))
                    else:
                        self.item(row, col_rank).setData(Qt.DisplayRole, rank_prev)

                    rank_prev += 1
                    data_prev = data_cur

        # Do not re-calculate cumulative data if the sorted column itself contains cumulative data
        if logicalIndex in cols_cumulative:
            cols_cumulative.remove(logicalIndex)

        for col in cols_cumulative:
            data_cumulative_prev = 0
            data_cumulative = []

            for row in range(self.rowCount()):
                if not self.isRowHidden(row):
                    data_cumulative_prev += self.item(row, col - 1).read_data()
                    data_cumulative.append(data_cumulative_prev)

            data_total = data_cumulative_prev

            for row in range(self.rowCount()):
                if not self.isRowHidden(row):
                    self.set_item_with_pct(row, col - 1, self.item(row, col - 1).read_data(), data_total, show_pct = self.show_pct)
                    self.set_item_with_pct(row, col, data_cumulative.pop(0), data_total, show_pct = self.show_pct)

        self.blockSignals(False)
        self.setSortingEnabled(True)
        self.show()

    def selected_rows(self):
        return sorted(set([index.row() for index in self.selectedIndexes()]))

    def export_selected(self):
        pass

    def export_all(self):
        pass

    def clear_table(self, header_count = 1):
        self.clearContents()

        if self.orientation == 'Horizontal':
            self.setColumnCount(len(self.headers))
            self.setRowCount(header_count)

            self.setHorizontalHeaderLabels(self.headers)
        else:
            self.setRowCount(len(self.headers))
            self.setColumnCount(header_count)

            self.setVerticalHeaderLabels(self.headers)

        for i in range(self.rowCount()):
            self.showRow(i)

        self.setSortingEnabled(False)

        self.item_changed()

    def find_column(self, column, fuzzy_search = False):
        for i in range(self.columnCount()):
            if fuzzy_search:
                if self.horizontalHeaderItem(i).text().find(column) > -1:
                    return i
            else:
                if column == self.horizontalHeaderItem(i).text():
                    return i

    def find_columns_cumulative(self):
        return [column
                for column in range(self.columnCount())
                if self.horizontalHeaderItem(column).text().find(self.tr('Cumulative')) > -1]

    def find_columns_breakdown(self):
        return list(range(self.find_column('Rank') + 2, self.find_column('Total', fuzzy_search = True)))

class Wordless_Table_Multi_Sort(Wordless_Table):
    def __init__(self, parent, sort_table, sort_columns):
        super().__init__(parent, headers = ['Column', 'Order'], cols_stretch = ['Order'])

        self.sort_table = sort_table
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

        self.itemChanged.connect(self.sorting_item_changed)
        self.itemSelectionChanged.connect(self.sorting_selection_changed)

        self.reset_table()

        self.setFixedHeight(self.cellWidget(0, 0).sizeHint().height() * 5)

    def sorting_item_changed(self, item = None):
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
                    combobox_current.setStyleSheet(self.main.settings['general']['style_highlight'])

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

    def sorting_selection_changed(self):
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

        combobox_sort_column.currentTextChanged.connect(lambda: self.sorting_item_changed(combobox_sort_column))
        combobox_sort_order.currentTextChanged.connect(lambda: self.sorting_item_changed(combobox_sort_column))

        return (combobox_sort_column, combobox_sort_order)

    def add_row(self):
        combobox_sort_column, combobox_sort_order = self._new_row()
        
        self.setRowCount(self.rowCount() + 1)
        self.setCellWidget(self.rowCount() - 1, 0, combobox_sort_column)
        self.setCellWidget(self.rowCount() - 1, 1, combobox_sort_order)

        self.sort()

    def insert_row(self):
        row = self.selected_rows()[0]

        combobox_sort_column, combobox_sort_order = self._new_row()

        self.insertRow(row)

        self.setCellWidget(row, 0, combobox_sort_column)
        self.setCellWidget(row, 1, combobox_sort_order)

        self.sort()

    def remove_row(self):
        for i in reversed(self.selected_rows()):
            self.removeRow(i)

        self.sort()

    def reset_table(self):
        self.clearContents()
        self.setRowCount(0)

        self.add_row()
