#
# Wordless: Table
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_widgets import wordless_box

class Wordless_Table_Item(QTableWidgetItem):
    def read_data(self):
        try:
            item_text = self.text()

            try:
                return self.val_raw
            except:
                return item_text
        except:
            cell_widget = self.tableWidget().cellWidget(self.row(), self.column())

            if isinstance(cell_widget, QComboBox):
                return cell_widget.currentText()
            elif isinstance(cell_widget, QLineEdit):
                return cell_widget.text()

    def __lt__(self, other):
        return self.read_data() < other.read_data()

class Wordless_Table(QTableWidget):
    def __init__(self, parent, headers = [], orientation = 'Horizontal',
                 cols_stretch = [], cols_pct = [], cols_cumulative = [], cols_breakdown = [],
                 sorting_enabled = False, drag_drop_enabled = False):
        self.main = parent
        self.headers = headers
        self.orientation = orientation

        self.cols_pct_old = cols_pct
        self.cols_cumulative_old = cols_cumulative
        self.cols_breakdown_old = cols_breakdown

        if orientation == 'Horizontal':
            super().__init__(1, len(self.headers), self.main)

            self.setHorizontalHeaderLabels(headers)
        else:
            super().__init__(len(self.headers), 1, self.main)

            self.setVerticalHeaderLabels(self.headers)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        if sorting_enabled:
            self.setSortingEnabled(True)

            if orientation == 'Horizontal':
                self.horizontalHeader().sortIndicatorChanged.connect(self.sorting_changed)
            else:
                self.verticalHeader().sortIndicatorChanged.connect(self.sorting_changed)

        if drag_drop_enabled:
            self.setDragEnabled(True)
            self.setAcceptDrops(True)
            self.viewport().setAcceptDrops(True)
            self.setDragDropMode(QAbstractItemView.InternalMove)
            self.setDragDropOverwriteMode(False)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for col in self.find_col(cols_stretch):
            self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)

        self.itemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self.selection_changed)

        self.setStyleSheet('QHeaderView {color: #4169E1; font-weight: bold}')

        self.button_export_selected = QPushButton(self.tr('Export Selected...'), self)
        self.button_export_all = QPushButton(self.tr('Export All...'), self)
        self.button_clear = QPushButton(self.tr('Clear'), self)

        self.button_export_selected.clicked.connect(self.export_selected)
        self.button_export_all.clicked.connect(self.export_all)
        self.button_clear.clicked.connect(lambda: self.clear_table())

        self.clear_table()

    def setCellWidget(self, row, col, widget):
        super().setCellWidget(row, col, widget)

        self.setItem(row, col, Wordless_Table_Item(''))

    def dropEvent(self, event):
        rows_dragged = []

        if self.indexAt(event.pos()).row() == -1:
            row_dropped = self.rowCount()
        else:
            row_dropped = self.indexAt(event.pos()).row()

        selected_rows = self.selected_rows()

        self.blockSignals(True)

        for row in selected_rows:
            rows_dragged.append([])

            for col in range(self.columnCount()):
                item_text = self.item(row, col).text()

                if item_text:
                    rows_dragged[-1].append(self.takeItem(row, col))
                else:
                    rows_dragged[-1].append(self.cellWidget(row, col))

        for i in reversed(selected_rows):
            self.removeRow(i)

            if i < row_dropped:
                row_dropped -= 1

        for row, items in enumerate(rows_dragged):
            self.insertRow(row_dropped + row)

            for col, item in enumerate(items):
                if isinstance(item, QTableWidgetItem):
                    self.setItem(row_dropped + row, col, item)
                elif isinstance(item, QComboBox):
                    item_combo_box = wordless_box.Wordless_Combo_Box(self.main)
                    item_combo_box.addItems([item.itemText(i) for i in range(item.count())])
                    item_combo_box.setCurrentText(item.currentText())

                    self.setCellWidget(row_dropped + row, col, item_combo_box)

                self.item(row, col).setSelected(True)

        self.blockSignals(False)

        event.accept()

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

    def sorting_changed(self, logicalIndex, order):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            self.update_ranks()

            if self.show_cumulative:
                self.toggle_cumulative()

    def insert_col(self, i, label, pct = False, cumulative = False, breakdown = False):
        cols_pct = [self.horizontalHeaderItem(col).text() for col in self.cols_pct]
        cols_cumulative = [self.horizontalHeaderItem(col).text() for col in self.cols_cumulative]
        cols_breakdown = [self.horizontalHeaderItem(col).text() for col in self.cols_breakdown]

        super().insertColumn(i)

        self.setHorizontalHeaderItem(i, QTableWidgetItem(label))

        if pct:
            cols_pct += [label]
        if cumulative:
            cols_cumulative += [label]
        if breakdown:
            cols_breakdown += [label]

        self.cols_pct = set(self.find_col(cols_pct))
        self.cols_cumulative = set(self.find_col(cols_cumulative))
        self.cols_breakdown = set(self.find_col(cols_breakdown))

    def set_item_num(self, row, col, val, val_max):
        precision = self.main.settings_custom['general']['precision']
        len_val = len(f'{val_max:.{precision}f}')

        item = Wordless_Table_Item()

        item.val = val

        item.setText(f'{val:>{len_val}.{precision}f}')

        item.setFont(QFont(self.main.settings_custom['general']['font_monospaced']))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        super().setItem(row, col, item)

    def set_item_pct(self, row, col, val, total):
        item = Wordless_Table_Item()

        item.val = val
        item.val_raw = val
        item.val_cumulative = 0
        item.total = total

        item.setFont(QFont(self.main.settings_custom['general']['font_monospaced']))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        super().setItem(row, col, item)

    def update_ranks(self):
        data_prev = ''
        rank_prev = 1
        rank_next = 1

        sort_section = self.horizontalHeader().sortIndicatorSection()
        col_rank = self.find_col(self.tr('Rank'))
        rows_hidden = [self.item(row, 1).text() for row in range(self.rowCount()) if self.isRowHidden(row)]

        self.blockSignals(True)
        self.setSortingEnabled(False)
        self.sortByColumn(sort_section, self.horizontalHeader().sortIndicatorOrder())

        rows_hidden_sorted = []

        for text in rows_hidden:
            if self.findItems(text, Qt.MatchExactly)[0].column() == 1:
                rows_hidden_sorted.append(self.findItems(text, Qt.MatchExactly)[0].row())

        for row in range(self.rowCount()):
            if row not in rows_hidden_sorted:
                data_cur = self.item(row, sort_section).read_data()

                if data_cur == data_prev:
                    self.item(row, col_rank).setData(Qt.DisplayRole, rank_prev)
                else:
                    self.item(row, col_rank).setData(Qt.DisplayRole, rank_next)

                    rank_prev = rank_next

                rank_next += 1
                data_prev = data_cur

        self.blockSignals(False)
        self.setSortingEnabled(True)

        self.setUpdatesEnabled(False)

        for row in rows_hidden_sorted:
            self.hideRow(row)

        self.setUpdatesEnabled(True)

    def toggle_pct(self):
        precision = self.main.settings_custom['general']['precision']
        len_pct = 5 + precision

        rows_hidden = [row for row in range(self.rowCount()) if self.isRowHidden(row)]

        self.hide()
        self.blockSignals(True)
        self.setSortingEnabled(False)

        for col in self.cols_pct:
            len_val = len(f'{self.item(0, col).total:,}')

            if self.show_pct:
                for row in range(self.rowCount()):
                    item = self.item(row, col)

                    pct = item.val / item.total if item.total else 0

                    if not self.isRowHidden(row):
                        item.setText(f'{item.val:>{len_val},}/{pct:<{len_pct}.{precision}%}')
            else:
                for row in range(self.rowCount()):
                    item = self.item(row, col)

                    pct = item.val / item.total if item.total else 0

                    if not self.isRowHidden(row):
                        item.setText(f'{item.val:>{len_val},}')

        self.show()
        self.blockSignals(False)
        self.setSortingEnabled(True)

        self.setUpdatesEnabled(False)

        for i in rows_hidden:
            self.hideRow(i)

        self.setUpdatesEnabled(True)

    def toggle_cumulative(self):
        for col in self.cols_cumulative:
            val_cumulative = 0

            for row in range(self.rowCount()):
                if not self.isRowHidden(row):
                    item = self.item(row, col)

                    val_cumulative += item.val
                    item.val_cumulative = val_cumulative

        if self.show_cumulative:
            for col in self.cols_cumulative:
                for row in range(self.rowCount()):
                    item.val = item.val_cumulative
        else:
            for col in self.cols_cumulative:
                for row in range(self.rowCount()):
                    item.val = item.val_raw

        self.toggle_pct()

    def toggle_breakdown(self):
        self.setUpdatesEnabled(False)

        for col in self.cols_breakdown:
            if self.show_breakdown:
                self.showColumn(col)
            else:
                self.hideColumn(col)

        self.setUpdatesEnabled(True)

    def filter_table(self):
        rank_prev = 1
        rank_next = 1
        data_prev = ''

        self.setUpdatesEnabled(False)
        
        for i, filters in enumerate(self.row_filters):
            if [val for val in filters.values() if not val]:
                self.hideRow(i)
            else:
                self.showRow(i)

        self.setUpdatesEnabled(True)

        self.update_ranks()
        self.toggle_cumulative()

    def selected_rows(self):
        return sorted(set([index.row() for index in self.selectedIndexes()]))

    def find_col(self, text, fuzzy_matching = False):
        def find(text):
            for col in range(self.columnCount()):
                if fuzzy_matching:
                    if self.horizontalHeaderItem(col) and self.horizontalHeaderItem(col).text().find(text) > -1:
                        return col
                else:
                    if self.horizontalHeaderItem(col) and self.horizontalHeaderItem(col).text() == text:
                        return col

        if type(text) == list:
            return [find(text_item)
                    for text_item in text]
        else:
            return find(text)

    def find_cols(self, text):
        return [col
                for col in range(self.columnCount())
                if self.horizontalHeaderItem(col) and self.horizontalHeaderItem(col).text().find(text) > -1]

    def export_selected(self):
        pass

    def export_all(self):
        pass

    def clear_table(self, header_count = 1):
        self.clearContents()

        if self.orientation == 'Horizontal':
            self.horizontalHeader().blockSignals(True)

            self.setColumnCount(len(self.headers))
            self.setRowCount(header_count)

            self.setHorizontalHeaderLabels(self.headers)

            self.horizontalHeader().blockSignals(False)

            self.horizontalHeader().sectionCountChanged.emit(0, header_count)
        else:
            self.verticalHeader().blockSignals(True)

            self.setRowCount(len(self.headers))
            self.setColumnCount(header_count)

            self.setVerticalHeaderLabels(self.headers)

            self.verticalHeader().blockSignals(False)

            self.verticalHeader().sectionCountChanged.emit(0, header_count)

        for i in range(self.rowCount()):
            self.showRow(i)
        for i in range(self.columnCount()):
            self.showColumn(i)

        self.cols_pct = set(self.find_col(self.cols_pct_old))
        self.cols_cumulative = set(self.find_col(self.cols_cumulative_old))
        self.cols_breakdown = set(self.find_col(self.cols_breakdown_old))
        self.files = []

        self.item_changed()

class Wordless_Table_Multi_Sort(Wordless_Table):
    def __init__(self, parent, sort_table, sort_cols):
        super().__init__(parent, headers = ['Column', 'Order'], cols_stretch = ['Order'])

        self.sort_table = sort_table
        self.sort_cols = sort_cols

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

        if self.rowCount() < len(self.sort_cols):
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
        if self.selectedIndexes() and self.rowCount() < len(self.sort_cols):
            self.button_insert.setEnabled(True)
        else:
            self.button_insert.setEnabled(False)

        if self.selectedIndexes() and self.rowCount() > 1:
            self.button_remove.setEnabled(True)
        else:
            self.button_remove.setEnabled(False)

    def update_sort_cols(self, sort_cols_new):
        sort_cols_old = self.sort_cols
        self.sort_cols = sort_cols_new

        for i in reversed(range(self.rowCount())):
            sort_col = self.cellWidget(i, 0)

            if len(sort_cols_new) < len(sort_cols_old):
                if sort_col.currentText() in sort_cols_new:
                    for j in reversed(range(sort_col.count())):
                        if j > len(sort_cols_new) - 1:
                            sort_col.removeItem(j)
                else:
                    self.removeRow(i)
            elif len(sort_cols_new) > len(sort_cols_old):
                sort_col.addItems(sort_cols_new[-(len(sort_cols_new) - len(sort_cols_old)):])

        if self.rowCount() == 0:
            self.reset_table()

    def sort(self):
        pass

    def _new_row(self):
        combobox_sort_col = QComboBox(self)
        combobox_sort_order = QComboBox(self)

        combobox_sort_col.addItems(self.sort_cols)
        combobox_sort_order.addItems(['Ascending', 'Descending'])

        for i in range(combobox_sort_col.count()):
            text = combobox_sort_col.itemText(i)

            if text not in [self.cellWidget(j, 0).currentText() for j in range(self.rowCount())]:
                combobox_sort_col.setCurrentText(text)
                combobox_sort_col.old_text = text

                break

        combobox_sort_col.currentTextChanged.connect(lambda: self.sorting_item_changed(combobox_sort_col))
        combobox_sort_order.currentTextChanged.connect(lambda: self.sorting_item_changed(combobox_sort_col))

        return (combobox_sort_col, combobox_sort_order)

    def add_row(self):
        combobox_sort_col, combobox_sort_order = self._new_row()
        
        self.setRowCount(self.rowCount() + 1)
        self.setCellWidget(self.rowCount() - 1, 0, combobox_sort_col)
        self.setCellWidget(self.rowCount() - 1, 1, combobox_sort_order)

        self.sort()

    def insert_row(self):
        row = self.selected_rows()[0]

        combobox_sort_col, combobox_sort_order = self._new_row()

        self.insertRow(row)

        self.setCellWidget(row, 0, combobox_sort_col)
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
