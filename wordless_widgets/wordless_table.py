#
# Wordless: Table
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import numpy
import openpyxl

from wordless_widgets import wordless_box, wordless_dialog

class Wordless_Table_Item(QTableWidgetItem):
    def read_data(self):
        if self.column() in self.tableWidget().headers_cumulative:
            return self.val_raw
        elif self.column() in self.tableWidget().headers_num:
            return self.val
        else:
            return self.text()

    def __lt__(self, other):
        return self.read_data() < other.read_data()

class Wordless_Table(QTableWidget):
    def __init__(self, main, headers, header_orientation = 'horizontal', cols_stretch = []):
        self.main = main
        self.headers = headers
        self.header_orientation = header_orientation

        if header_orientation == 'horizontal':
            super().__init__(1, len(self.headers), self.main)

            self.setHorizontalHeaderLabels(self.headers)
        else:
            super().__init__(len(self.headers), 1, self.main)

            self.setVerticalHeaderLabels(self.headers)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for col in self.find_col(cols_stretch):
            self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().setHighlightSections(False)

        if self.header_orientation == 'horizontal':
            self.setStyleSheet(''' 
                                   QTableView {
                                       outline: none;
                                       color: #292929;
                                   }

                                   QTableView::item:hover {
                                       background-color: #EEE;
                                   }
                                   QTableView::item:selected {
                                       background-color: #EEE;
                                       color: #292929;
                                   }

                                   QHeaderView::section {
                                       color: #FFF;
                                       font-weight: bold;
                                   }

                                   QHeaderView::section:horizontal {
                                       background-color: #5C88C5;
                                   }
                                   QHeaderView::section:horizontal:hover {
                                       background-color: #3265B2;
                                   }
                                   QHeaderView::section:horizontal:pressed {
                                       background-color: #264E8C;
                                   }

                                   QHeaderView::section:vertical {
                                       background-color: #888;
                                   }
                                   QHeaderView::section:vertical:hover {
                                       background-color: #777;
                                   }
                                   QHeaderView::section:vertical:pressed {
                                       background-color: #666;
                                   }
                               ''')
        else:
            self.setStyleSheet('''

                                   QTableView {
                                       outline: none;
                                       color: #292929;
                                   }

                                   QTableView::item:hover {
                                       background-color: #EEE;
                                   }
                                   QTableView::item:selected {
                                       background-color: #EEE;
                                       color: #292929;
                                   }

                                   QHeaderView::section {
                                       color: #FFF;
                                       font-weight: bold;
                                   }

                                   QHeaderView::section:horizontal {
                                       background-color: #888;
                                   }
                                   QHeaderView::section:horizontal:hover {
                                       background-color: #777;
                                   }
                                   QHeaderView::section:horizontal:pressed {
                                       background-color: #666;
                                   }

                                   QHeaderView::section:vertical {
                                       background-color: #5C88C5;
                                   }
                                   QHeaderView::section:vertical:hover {
                                       background-color: #3265B2;
                                   }
                                   QHeaderView::section:vertical:pressed {
                                       background-color: #264E8C;
                                   }
                               ''')

    def insert_row(self, i, label):
        super().insertRow(i)

        self.setVerticalHeaderItem(i, QTableWidgetItem(label))

    def insert_col(self, i, label):
        super().insertColumn(i)

        self.setHorizontalHeaderItem(i, QTableWidgetItem(label))

    def clear_table(self, header_count = 1):
        self.clearContents()

        if self.header_orientation == 'horizontal':
            self.setColumnCount(len(self.headers))
            self.setRowCount(header_count)

            self.setHorizontalHeaderLabels(self.headers)
        else:
            self.setRowCount(len(self.headers))
            self.setColumnCount(header_count)

            self.setVerticalHeaderLabels(self.headers)

    def find_row(self, text, fuzzy_matching = False):
        def find(text):
            for row in range(self.rowCount()):
                if fuzzy_matching:
                    if self.verticalHeaderItem(row).text().find(text) > -1:
                        return row
                else:
                    if self.verticalHeaderItem(row).text() == text:
                        return row

        if type(text) == list:
            return [find(text_item) for text_item in text]
        else:
            return find(text)

    def find_rows(self, text):
        return [row
                for row in range(self.columnCount())
                if self.verticalHeaderItem(row).text().find(text) > -1]

    def find_col(self, text, fuzzy_matching = False):
        def find(text):
            for col in range(self.columnCount()):
                if fuzzy_matching:
                    if self.horizontalHeaderItem(col).text().find(text) > -1:
                        return col
                else:
                    if self.horizontalHeaderItem(col).text() == text:
                        return col

        if type(text) == list:
            return [find(text_item) for text_item in text]
        else:
            return find(text)

    def find_cols(self, text):
        return [col
                for col in range(self.columnCount())
                if self.horizontalHeaderItem(col).text().find(text) > -1]

    def find_header(self, text, fuzzy_matching = False):
        if self.header_orientation == 'horizontal':
            return self.find_col(text, fuzzy_matching)
        else:
            return self.find_row(text, fuzzy_matching)

    def find_headers(self, text):
        if self.header_orientation == 'horizontal':
            return self.find_cols(text)
        else:
            return self.find_rows(text)

class Wordless_Table_Data(Wordless_Table):
    def __init__(self, main, headers, header_orientation = 'horizontal', cols_stretch = [],
                 headers_num = [], headers_pct = [], headers_cumulative = [], cols_breakdown = [],
                 sorting_enabled = False, drag_drop_enabled = False):
        super().__init__(main, headers, header_orientation, cols_stretch)

        self.headers_num_old = headers_num
        self.headers_pct_old = headers_pct
        self.headers_cumulative_old = headers_cumulative
        self.cols_breakdown_old = cols_breakdown

        self.sorting_enabled = sorting_enabled

        if sorting_enabled:
            self.setSortingEnabled(True)

            if header_orientation == 'horizontal':
                self.horizontalHeader().sortIndicatorChanged.connect(self.sorting_changed)
            else:
                self.verticalHeader().sortIndicatorChanged.connect(self.sorting_changed)

        if drag_drop_enabled:
            self.setDragEnabled(True)
            self.setAcceptDrops(True)
            self.viewport().setAcceptDrops(True)
            self.setDragDropMode(QAbstractItemView.InternalMove)
            self.setDragDropOverwriteMode(False)

        self.itemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self.selection_changed)

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

        self.itemChanged.emit(self.item(0, 0))

        event.accept()

    def item_changed(self):
        rows_visible = len([i for i in range(self.rowCount()) if not self.isRowHidden(i)])

        if [i for i in range(self.columnCount()) if self.item(0, i)] and rows_visible:
            self.button_export_all.setEnabled(True)
        else:
            self.button_export_all.setEnabled(False)

        self.selection_changed()

    def selection_changed(self):
        if self.selectedIndexes() and [i for i in range(self.columnCount()) if self.item(0, i)]:
            self.button_export_selected.setEnabled(True)
        else:
            self.button_export_selected.setEnabled(False)

    def sorting_changed(self, logicalIndex, order):
        if [i for i in range(self.columnCount()) if self.item(0, i)]:
            self.update_ranks()

            if self.show_cumulative:
                self.toggle_cumulative()

            self.update_items_width()

    def insert_row(self, i, label, num = False, pct = False, cumulative = False):
        headers_num = [self.verticalHeaderItem(row).text() for row in self.headers_num]
        headers_pct = [self.verticalHeaderItem(row).text() for row in self.headers_pct]
        headers_cumulative = [self.verticalHeaderItem(row).text() for row in self.headers_cumulative]

        super().insert_row(i, label)

        if num:
            headers_num += [label]
        if pct:
            headers_pct += [label]
        if cumulative:
            headers_cumulative += [label]

        self.headers_num = set(self.find_row(headers_num))
        self.headers_pct = set(self.find_row(headers_pct))
        self.headers_cumulative = set(self.find_row(headers_cumulative))

    def insert_col(self, i, label, num = False, pct = False, cumulative = False, breakdown = False):
        if self.header_orientation == 'horizontal':
            headers_num = [self.horizontalHeaderItem(col).text() for col in self.headers_num]
            headers_pct = [self.horizontalHeaderItem(col).text() for col in self.headers_pct]
            headers_cumulative = [self.horizontalHeaderItem(col).text() for col in self.headers_cumulative]
        cols_breakdown = [self.horizontalHeaderItem(col).text() for col in self.cols_breakdown]

        super().insert_col(i, label)

        if num:
            headers_num += [label]
        if pct:
            headers_pct += [label]
        if cumulative:
            headers_cumulative += [label]
        if breakdown:
            cols_breakdown += [label]

        if self.header_orientation == 'horizontal':
            self.headers_num = set(self.find_col(headers_num))
            self.headers_pct = set(self.find_col(headers_pct))
            self.headers_cumulative = set(self.find_col(headers_cumulative))
        self.cols_breakdown = set(self.find_col(cols_breakdown))

    def set_item_num(self, row, col, item):
        item.setFont(QFont(self.main.settings_custom['general']['font_monospaced']))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        super().setItem(row, col, item)

    def set_item_num_int(self, row, col, val):
        item = Wordless_Table_Item()

        item.val = int(val)

        self.set_item_num(row, col, item)

    def set_item_num_float(self, row, col, val):
        item = Wordless_Table_Item()

        item.val = float(val)

        self.set_item_num(row, col, item)

    def set_item_num_pct(self, row, col, val, total = -1):
        item = Wordless_Table_Item()

        item.val = int(val)
        if total > -1:
            item.total = int(total)

        self.set_item_num(row, col, item)

    def set_item_num_cumulative(self, row, col, val):
        item = Wordless_Table_Item()

        item.val = int(val)
        item.val_raw = item.val
        item.val_cumulative = 0

        self.set_item_num(row, col, item)

    def update_items_width(self):
        precision_val = self.main.settings_custom['general']['precision_decimal']
        precision_pct = self.main.settings_custom['general']['precision_pct']
        len_pct = precision_pct + 5

        rows_hidden = [row for row in range(self.rowCount()) if self.isRowHidden(row)]

        self.hide()
        self.blockSignals(True)

        if self.sorting_enabled:
            self.setSortingEnabled(False)

        self.setUpdatesEnabled(False)

        if self.header_orientation == 'horizontal':
            for col in self.headers_num:
                max_val = max([self.item(row, col).val
                               for row in range(self.rowCount())
                               if self.item(row, col).val != float('inf')])

                # p-value
                if self.horizontalHeaderItem(col).text().find(self.tr('p-value')) > -1:
                    precision_val = self.main.settings_custom['general']['precision_p_value']
                else:
                    precision_val = self.main.settings_custom['general']['precision_decimal']

                if type(max_val) == int:
                    len_val = len(f'{max_val:,}')
                else:
                    len_val = len(f'{max_val:,.{precision_val}f}')

                if col in self.headers_pct and self.show_pct:
                    pct_max = max([self.item(row, col).pct for row in range(self.rowCount())])
                    len_pct = len(f'{pct_max:.{precision_pct}%}')

                    if type(max_val) == int:
                        for row in range(self.rowCount()):
                            if not self.isRowHidden(row):
                                item = self.item(row, col)
                                
                                item.setText(f'{item.val:>{len_val},}/{item.pct:<{len_pct}.{precision_pct}%}')
                    else:
                        for row in range(self.rowCount()):
                            if not self.isRowHidden(row):
                                item = self.item(row, col)

                                if item.val == float('inf'):
                                    item.setText('+ ∞')
                                elif item.val == float('-inf'):
                                    item.setText('- ∞')
                                else:
                                    item.setText(f'{item.val:>{len_val},.{precision_val}}/{item.pct:<{len_pct}.{precision_pct}%}')
                else:
                    if type(max_val) == int:
                        for row in range(self.rowCount()):
                            if not self.isRowHidden(row):
                                item = self.item(row, col)

                                item.setText(f'{item.val:>{len_val},}')
                    else:
                        for row in range(self.rowCount()):
                            if not self.isRowHidden(row):
                                item = self.item(row, col)

                                if item.val == float('inf'):
                                    item.setText('+ ∞')
                                elif item.val == float('-inf'):
                                    item.setText('- ∞')
                                else:
                                    item.setText(f'{item.val:>{len_val},.{precision_val}f}')
        else:
            len_vals = []

            max_vals = [max([self.item(row, col).val
                             for row in range(self.rowCount())])
                        for col in range(self.columnCount())]
            max_pcts = [max([self.item(row, col).pct
                             for row in range(self.rowCount())
                             if row in self.headers_pct])
                        for col in range(self.columnCount())]

            for max_val in max_vals:
                if type(max_val) == int:
                    len_vals.append(len(f'{max_val:,}'))
                else:
                    len_vals.append(len(f'{max_val:,.{precision_val}f}'))

            len_pcts = [len(f'{max_pct:.{precision_pct}%}') for max_pct in max_pcts]

            for row in self.headers_num:
                if row in self.headers_pct and self.show_pct:
                    if type(self.item(row, 0).val) == int:
                        for col in range(self.columnCount()):
                            if not self.isColumnHidden(col):
                                item = self.item(row, col)
                                
                                item.setText(f'{item.val:>{len_vals[col]},}/{item.pct:<{len_pcts[col]}.{precision_pct}%}')
                    else:
                        for col in range(self.columnCount()):
                            if not self.isColumnHidden(col):
                                item = self.item(row, col)

                                item.setText(f'{item.val:>{len_vals[col]},.{precision_val}}/{item.pct:<{len_pcts[col]}.{precision_pct}%}')
                else:
                    if type(self.item(row, 0).val) == int:
                        for col in range(self.columnCount()):
                            if not self.isColumnHidden(col):
                                item = self.item(row, col)

                                item.setText(f'{item.val:{len_vals[col]},}')
                    else:
                        for col in range(self.columnCount()):
                            if not self.isColumnHidden(col):
                                item = self.item(row, col)

                                item.setText(f'{item.val:{len_vals[col]},.{precision_val}f}')

        self.blockSignals(False)

        if self.sorting_enabled:
            self.setSortingEnabled(True)

        self.setUpdatesEnabled(True)
        self.show()

        self.setUpdatesEnabled(False)

        for row_hidden in rows_hidden:
            self.hideRow(row_hidden)

        self.setUpdatesEnabled(True)

    def update_ranks(self):
        data_prev = ''
        rank_prev = 1
        rank_next = 1

        sorting_section = self.horizontalHeader().sortIndicatorSection()
        col_rank = self.find_col(self.tr('Rank'))
        rows_hidden = [self.item(row, 1).text() for row in range(self.rowCount()) if self.isRowHidden(row)]

        self.sortByColumn(sorting_section, self.horizontalHeader().sortIndicatorOrder())

        rows_hidden_sorted = []

        for text in rows_hidden:
            if self.findItems(text, Qt.MatchExactly)[0].column() == 1:
                rows_hidden_sorted.append(self.findItems(text, Qt.MatchExactly)[0].row())

        for row in range(self.rowCount()):
            if row not in rows_hidden_sorted:
                data_cur = self.item(row, sorting_section).read_data()

                if data_cur == data_prev:
                    self.item(row, col_rank).val = rank_prev
                else:
                    self.item(row, col_rank).val = rank_next

                    rank_prev = rank_next

                rank_next += 1
                data_prev = data_cur

        self.setUpdatesEnabled(False)

        for row in rows_hidden_sorted:
            self.hideRow(row)

        self.setUpdatesEnabled(True)

    def toggle_pct(self):
        if self.header_orientation == 'horizontal':
            for col in self.headers_pct:
                if self.item(0, col) and not hasattr(self.item(0, col), 'total'):
                    total = sum([self.item(row, col).val_raw for row in range(self.rowCount())])

                    for row in range(self.rowCount()):
                        self.item(row, col).total = total

                for row in range(self.rowCount()):
                    item = self.item(row, col)

                    item.pct = item.val / item.total if item.total else 0
        else:
            for row in self.headers_pct:
                if self.item(row, 0) and not hasattr(self.item(row, 0), 'total'):
                    total = self.item(row, self.columnCount() - 1).val

                    for col in range(self.columnCount()):
                        self.item(row, col).total = total

                for col in range(self.columnCount()):
                    item = self.item(row, col)

                    item.pct = item.val / item.total if item.total else 0

    def toggle_cumulative(self):
        if self.header_orientation == 'horizontal':
            for col in self.headers_cumulative:
                val_cumulative = 0

                for row in range(self.rowCount()):
                    if not self.isRowHidden(row):
                        item = self.item(row, col)

                        val_cumulative += item.val
                        item.val_cumulative = val_cumulative
           
            if self.show_cumulative:
                for col in self.headers_cumulative:
                    for row in range(self.rowCount()):
                        item = self.item(row, col)

                        item.val = item.val_cumulative
                        item.pct = item.val / item.total if item.total else 0
            else:
                for col in self.headers_cumulative:
                    for row in range(self.rowCount()):
                        item = self.item(row, col)

                        item.val = item.val_raw
                        item.pct = item.val / item.total if item.total else 0
        else:
            for row in self.headers_cumulative:
                val_cumulative = 0

                for col in range(self.columnCount() - 1):
                    if not self.isColumnHidden(col):
                        item = self.item(row, col)

                        val_cumulative += item.val
                        item.val_cumulative = val_cumulative

                self.item(row, self.columnCount() - 1).val_cumulative = val_cumulative
           
            if self.show_cumulative:
                for row in self.headers_cumulative:
                    for col in range(self.columnCount()):
                        item = self.item(row, col)

                        item.val = item.val_cumulative
                        item.pct = item.val / item.total if item.total else 0
            else:
                for row in self.headers_cumulative:
                    for col in range(self.columnCount()):
                        item = self.item(row, col)

                        item.val = item.val_raw
                        item.pct = item.val / item.total if item.total else 0

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
            if [val for val in filters if not val]:
                self.hideRow(i)
            else:
                self.showRow(i)

        self.setUpdatesEnabled(True)

        self.toggle_cumulative()

        self.update_ranks()
        self.update_items_width()

        self.item_changed()

    def selected_rows(self):
        return sorted(set([index.row() for index in self.selectedIndexes()]))

    def export_selected(self):
        pass

    def export_all(self):
        def set_cell_styles(cell, item, item_type = 'item'):
            if item_type == 'header_horizontal':
                cell.font = openpyxl.styles.Font(name = self.main.font().family(),
                                                 size = 8,
                                                 bold = True,
                                                 color = 'FFFFFF')

                if self.header_orientation == 'horizontal':
                    cell.fill = openpyxl.styles.PatternFill(fill_type = 'solid', fgColor = '5C88C5')
                else:
                    cell.fill = openpyxl.styles.PatternFill(fill_type = 'solid', fgColor = '888888')
            elif item_type == 'header_vertical':
                cell.font = openpyxl.styles.Font(name = self.main.font().family(),
                                                 size = 8,
                                                 bold = True,
                                                 color = 'FFFFFF')

                cell.fill = openpyxl.styles.PatternFill(fill_type = 'solid', fgColor = '5C88C5')
            else:
                cell.font = openpyxl.styles.Font(name = self.main.font().family(),
                                                 size = 8,
                                                 color = '292929')

            cell.alignment = openpyxl.styles.Alignment(horizontal = 'center',
                                                       vertical = 'center',
                                                       wrap_text = True)

        export_path = QFileDialog.getSaveFileName(self,
                                                  self.tr('Export Table'),
                                                  self.main.settings_custom['general']['default_paths_export'],
                                                  self.tr('Excel Files (*.xlsx)'))[0]

        if export_path:
            workbook = openpyxl.Workbook()
            worksheet = workbook.active

            worksheet.freeze_panes = 'B2'

            dpi_x = QApplication.primaryScreen().logicalDotsPerInchX()
            dpi_y = QApplication.primaryScreen().logicalDotsPerInchY()

            if self.header_orientation == 'horizontal':
                # Horizontal Headers
                for col in range(self.columnCount()):
                    worksheet.cell(1, 1 + col).value = self.horizontalHeaderItem(col).text()

                    set_cell_styles(worksheet.cell(1, 1 + col), self.horizontalHeaderItem(col), item_type = 'header_horizontal')

                    worksheet.column_dimensions[openpyxl.utils.get_column_letter(1 + col)].width = self.horizontalHeader().sectionSize(col) / dpi_x * 13

                # Cells
                for row in range(self.rowCount()):
                    for col in range(self.columnCount()):
                        worksheet.cell(2 + row, 1 + col).value = self.item(row, col).text()

                        set_cell_styles(worksheet.cell(2 + row, 1 + col), self.item(row, col))
            else:
                # Horizontal Headers
                for col in range(self.columnCount()):
                    worksheet.cell(1, 2 + col).value = self.horizontalHeaderItem(col).text()

                    set_cell_styles(worksheet.cell(1, 2 + col), self.horizontalHeaderItem(col), item_type = 'header_horizontal')

                    worksheet.column_dimensions[openpyxl.utils.get_column_letter(2 + col)].width = self.horizontalHeader().sectionSize(col) / dpi_x * 13

                worksheet.column_dimensions[openpyxl.utils.get_column_letter(1)].width = max([self.verticalHeader().sectionSizeFromContents(row).width() / dpi_x * 13 for row in range(self.rowCount())])

                # Vertical Headers
                for row in range(self.rowCount()):
                    worksheet.cell(2 + row, 1).value = self.verticalHeaderItem(row).text()

                    set_cell_styles(worksheet.cell(2 + row, 1), self.verticalHeaderItem(row), item_type = 'header_vertical')

                # Cells
                for row in range(self.rowCount()):
                    for col in range(self.columnCount()):
                        worksheet.cell(2 + row, 2 + col).value = self.item(row, col).text()

                        set_cell_styles(worksheet.cell(2 + row, 2 + col), self.item(row, col))

            # Row Height
            for i, _ in enumerate(worksheet.rows):
                worksheet.row_dimensions[i + 1].height = self.verticalHeader().sectionSize(0) / dpi_y * 72

            workbook.save(export_path)

            self.main.settings_custom['general']['default_paths_export'] = os.path.split(export_path)[0]

            QMessageBox.information(self,
                                    self.tr('Export Completed'),
                                    self.tr(f'Export to file "{export_path}" completed successfully.'),
                                    QMessageBox.Ok)

    def clear_table(self, header_count = 1):
        self.clearContents()

        if self.header_orientation == 'horizontal':
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

        self.headers_num = set(self.find_header(self.headers_num_old))
        self.headers_pct = set(self.find_header(self.headers_pct_old))
        self.headers_cumulative = set(self.find_header(self.headers_cumulative_old))
        self.cols_breakdown = set(self.find_col(self.cols_breakdown_old))
        self.settings = self.main.settings_default

        self.item_changed()

class Wordless_Table_Data_Search(Wordless_Table_Data):
    def __init__(self, main, headers, header_orientation = 'horizontal', cols_stretch = [],
                 headers_num = [], headers_pct = [], headers_cumulative = [], cols_breakdown = [],
                 sorting_enabled = False, drag_drop_enabled = False):
        super().__init__(main, headers, header_orientation, cols_stretch,
                         headers_num, headers_pct, headers_cumulative, cols_breakdown,
                         sorting_enabled, drag_drop_enabled)

        self.label_number_results = QLabel()
        self.button_search_results = QPushButton(self.tr('Search in Results'), self)

        self.item_changed = self.results_changed

        self.results_changed()

    def results_changed(self):
        super().item_changed()

        rows_visible = len([i for i in range(self.rowCount()) if not self.isRowHidden(i)])

        if [i for i in range(self.columnCount()) if self.item(0, i)] and rows_visible:
            self.label_number_results.setText(self.tr(f'Number of Results: {rows_visible}'))

            self.button_search_results.setEnabled(True)
        else:
            self.label_number_results.setText(self.tr('Number of Results: 0'))

            self.button_search_results.setEnabled(False)

class Wordless_Table_Multi_Sort(Wordless_Table_Data):
    def __init__(self, main, sort_table, sort_cols):
        super().__init__(main, headers = ['Column', 'Order'], cols_stretch = ['Order'])

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

                    QMessageBox.warning(self.main,
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
