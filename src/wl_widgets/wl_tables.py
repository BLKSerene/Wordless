# ----------------------------------------------------------------------
# Wordless: Widgets - Tables
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
import csv
import os
import random
import re
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import docx
import nltk
import openpyxl

from wl_checking import wl_checking_misc
from wl_dialogs import wl_dialogs, wl_dialogs_misc, wl_msg_boxes
from wl_nlp import wl_matching, wl_nlp_utils, wl_word_detokenization
from wl_utils import wl_misc, wl_msgs, wl_threading
from wl_widgets import wl_boxes, wl_buttons, wl_labels, wl_layouts, wl_widgets

class Wl_Worker_Export_Table(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(bool, str)

    def run(self):
        if 'headers_int' not in self.table.__dict__:
            self.table.headers_int = []
        if 'headers_float' not in self.table.__dict__:
            self.table.headers_float = []
        if 'headers_pct' not in self.table.__dict__:
            self.table.headers_pct = []

        settings_concordancer = self.main.settings_custom['concordancer']['zapping_settings']

        # Check file permissions
        try:
            if not self.rows_export:
                self.rows_export = list(range(self.table.rowCount()))

            file_path_src = re.sub(r'\.([a-z]+?)$', r'_source.\1', self.file_path)
            file_path_tgt = re.sub(r'\.([a-z]+?)$', r'_target.\1', self.file_path)

            len_rows = len(self.rows_export)

            # CSV files
            if self.file_type == self.tr('CSV File (*.csv)'):
                encoding = self.main.settings_custom['export']['tables']['default_encoding']

                # Concordancer
                if self.table.tab == 'concordancer':
                    with open(self.file_path, 'w', encoding = encoding, newline = '') as f:
                        csv_writer = csv.writer(f)

                        # Horizontal Headers
                        csv_writer.writerow([self.table.horizontalHeaderItem(col).text().strip()
                                             for col in range(self.table.columnCount())])

                        # Cells
                        for i, row in enumerate(self.rows_export):
                            row_to_export = []

                            for col in range(self.table.columnCount()):
                                if self.table.item(row, col):
                                    cell_text = self.table.item(row, col).text()
                                else:
                                    cell_text = self.table.cellWidget(row, col).text()
                                    cell_text = wl_nlp_utils.html_to_text(cell_text)

                                row_to_export.append(cell_text)

                            csv_writer.writerow(row_to_export)

                            self.progress_updated.emit(self.tr(f'Exporting table ... ({i + 1} / {len_rows})'))
                # Concordancer (Parallel Mode)
                elif self.table.tab == 'concordancer_parallel':
                    # Source file
                    with open(file_path_src, 'w', encoding = encoding, newline = '') as f:
                        csv_writer = csv.writer(f)

                        # Horizontal Headers
                        csv_writer.writerow([self.table.linked_tables[0].horizontalHeaderItem(col).text().strip()
                                             for col in range(self.table.linked_tables[0].columnCount())])

                        # Cells
                        for i, row in enumerate(self.rows_export):
                            row_to_export = []

                            for col in range(self.table.linked_tables[0].columnCount()):
                                if self.table.linked_tables[0].item(row, col):
                                    cell_text = self.table.linked_tables[0].item(row, col).text()
                                else:
                                    cell_text = self.table.linked_tables[0].cellWidget(row, col).text()
                                    cell_text = wl_nlp_utils.html_to_text(cell_text)

                                row_to_export.append(cell_text)

                            csv_writer.writerow(row_to_export)

                            self.progress_updated.emit(self.tr(f'Exporting table ... ({i + 1} / {len_rows * 2})'))

                    # Target file
                    with open(file_path_tgt, 'w', encoding = encoding, newline = '') as f:
                        csv_writer = csv.writer(f)

                        # Horizontal Headers
                        csv_writer.writerow([self.table.horizontalHeaderItem(col).text().strip()
                                             for col in range(self.table.columnCount())])

                        # Cells
                        for i, row in enumerate(self.rows_export):
                            row_to_export = []

                            for col in range(self.table.columnCount()):
                                if self.table.item(row, col):
                                    cell_text = self.table.item(row, col).text()
                                else:
                                    cell_text = self.table.cellWidget(row, col).text()
                                    cell_text = wl_nlp_utils.html_to_text(cell_text)

                                row_to_export.append(cell_text)

                            csv_writer.writerow(row_to_export)

                            self.progress_updated.emit(self.tr(f'Exporting table ... ({len_rows + i + 1} / {len_rows * 2})'))
                else:
                    with open(self.file_path, 'w', encoding = encoding, newline = '') as f:
                        csv_writer = csv.writer(f)

                        if self.table.header_orientation == 'horizontal':
                            # Horizontal Headers
                            csv_writer.writerow([self.table.horizontalHeaderItem(col).text().strip()
                                                 for col in range(self.table.columnCount())])

                            # Cells
                            for i, row in enumerate(self.rows_export):
                                row_to_export = []

                                for col in range(self.table.columnCount()):
                                    row_to_export.append(self.table.item(row, col).text().strip())

                                csv_writer.writerow(row_to_export)

                                self.progress_updated.emit(self.tr(f'Exporting table ... ({i + 1} / {len_rows})'))
                        else:
                            # Horizontal Headers
                            csv_writer.writerow([''] +
                                                [self.table.horizontalHeaderItem(col).text().strip()
                                                 for col in range(self.table.columnCount())])

                            # Vertical Headers & Cells
                            for i, row in enumerate(self.rows_export):
                                row_to_export = [self.table.verticalHeaderItem(row).text().strip()]

                                for col in range(self.table.columnCount()):
                                    row_to_export.append(self.table.item(row, col).text().strip())

                                csv_writer.writerow(row_to_export)

                                self.progress_updated.emit(self.tr(f'Exporting table ... ({i + 1} / {len_rows})'))
            # Excel workbooks
            elif self.file_type == self.tr('Excel Workbook (*.xlsx)'):
                dpi_horizontal = QApplication.primaryScreen().logicalDotsPerInchX()
                dpi_vertical = QApplication.primaryScreen().logicalDotsPerInchY()

                # Concordancer
                if self.table.tab == 'concordancer':
                    workbook = openpyxl.Workbook()
                    worksheet = workbook.active

                    worksheet.freeze_panes = 'A2'

                    dpi_horizontal = QApplication.primaryScreen().logicalDotsPerInchX()
                    dpi_vertical = QApplication.primaryScreen().logicalDotsPerInchY()

                    # Horizontal Headers
                    for col in range(self.table.columnCount()):
                        cell = worksheet.cell(1, 1 + col)
                        cell.value = self.table.horizontalHeaderItem(col).text()

                        self.style_header_horizontal(cell, self.table.horizontalHeaderItem(col))

                        worksheet.column_dimensions[openpyxl.utils.get_column_letter(1 + col)].width = self.table.horizontalHeader().sectionSize(col) / dpi_horizontal * 13 + 3

                    # Cells
                    for row_cell, row_item in enumerate(self.rows_export):
                        for col in range(self.table.columnCount()):
                            # Left
                            if col == 0:
                                cell = worksheet.cell(2 + row_cell, 1 + col)

                                cell_val = wl_nlp_utils.html_to_text(self.table.cellWidget(row_item, col).text())
                                # Remove illegal characters
                                cell_val = re.sub(openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE, '', cell_val)
                                cell.value = cell_val

                                cell.font = openpyxl.styles.Font(
                                    name = self.table.cellWidget(row_item, col).font().family(),
                                    size = 8,
                                    color = '292929'
                                )
                                cell.alignment = openpyxl.styles.Alignment(
                                    horizontal = 'right',
                                    vertical = 'center'
                                )
                            # Node
                            elif col == 1:
                                cell = worksheet.cell(2 + row_cell, 1 + col)

                                cell_val = wl_nlp_utils.html_to_text(self.table.cellWidget(row_item, col).text())
                                # Remove illegal characters
                                cell_val = re.sub(openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE, '', cell_val)
                                cell.value = cell_val

                                self.style_cell_text(cell, self.table.cellWidget(row_item, col))

                                cell.font = openpyxl.styles.Font(
                                    name = self.table.cellWidget(row_item, col).font().family(),
                                    size = 8,
                                    bold = True,
                                    color = 'FF0000'
                                )
                                cell.alignment = openpyxl.styles.Alignment(
                                    horizontal = 'center',
                                    vertical = 'center'
                                )
                            # Right
                            elif col == 2:
                                cell = worksheet.cell(2 + row_cell, 1 + col)

                                cell_val = wl_nlp_utils.html_to_text(self.table.cellWidget(row_item, col).text())
                                # Remove illegal characters
                                cell_val = re.sub(openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE, '', cell_val)
                                cell.value = cell_val

                                cell.font = openpyxl.styles.Font(
                                    name = self.table.cellWidget(row_item, col).font().family(),
                                    size = 8,
                                    color = '292929'
                                )
                                cell.alignment = openpyxl.styles.Alignment(
                                    horizontal = 'left',
                                    vertical = 'center'
                                )
                            else:
                                cell = worksheet.cell(2 + row_cell, 1 + col)

                                cell_val = cell_text = self.table.item(row_item, col).text()
                                # Remove illegal characters
                                cell_val = re.sub(openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE, '', cell_val)
                                cell.value = cell_val

                                if (col in self.table.headers_int or
                                    col in self.table.headers_float or
                                    col in self.table.headers_pct):
                                    self.style_cell_num(cell, self.table.item(row_item, col))
                                else:
                                    self.style_cell_text(cell, self.table.item(row_item, col))

                            self.progress_updated.emit(self.tr(f'Exporting table ... ({row_cell + 1} / {len_rows})'))

                    # Row Height
                    worksheet.row_dimensions[1].height = self.table.horizontalHeader().height() / dpi_vertical * 72

                    for i, _ in enumerate(worksheet.rows):
                        worksheet.row_dimensions[2 + i].height = self.table.verticalHeader().sectionSize(0) / dpi_vertical * 72

                    self.progress_updated.emit(self.tr(f'Saving file ...'))

                    workbook.save(self.file_path)
                # Concordancer (Parallel Mode)
                elif self.table.tab == 'concordancer_parallel':
                    # Source file
                    workbook = openpyxl.Workbook()
                    worksheet = workbook.active

                    worksheet.freeze_panes = 'A2'

                    # Horizontal Headers
                    for col in range(self.table.linked_tables[0].columnCount()):
                        cell = worksheet.cell(1, 1 + col)
                        cell.value = self.table.linked_tables[0].horizontalHeaderItem(col).text()

                        self.style_header_horizontal(cell, self.table.linked_tables[0].horizontalHeaderItem(col))

                        worksheet.column_dimensions[openpyxl.utils.get_column_letter(1 + col)].width = self.table.linked_tables[0].horizontalHeader().sectionSize(col) / dpi_horizontal * 13 + 3

                    # Cells
                    for row_cell, row_item in enumerate(self.rows_export):
                        for col in range(self.table.linked_tables[0].columnCount()):
                            # Left
                            if col == 0:
                                cell = worksheet.cell(2 + row_cell, 1 + col)

                                cell_val = wl_nlp_utils.html_to_text(self.table.linked_tables[0].cellWidget(row_item, col).text())
                                # Remove illegal characters
                                cell_val = re.sub(openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE, '', cell_val)
                                cell.value = cell_val

                                cell.font = openpyxl.styles.Font(
                                    name = self.table.linked_tables[0].cellWidget(row_item, col).font().family(),
                                    size = 8,
                                    color = '292929'
                                )
                                cell.alignment = openpyxl.styles.Alignment(
                                    horizontal = 'right',
                                    vertical = 'center'
                                )
                            # Node
                            elif col == 1:
                                cell = worksheet.cell(2 + row_cell, 1 + col)

                                cell_val = wl_nlp_utils.html_to_text(self.table.linked_tables[0].cellWidget(row_item, col).text())
                                # Remove illegal characters
                                cell_val = re.sub(openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE, '', cell_val)
                                cell.value = cell_val

                                self.style_cell_text(cell, self.table.linked_tables[0].cellWidget(row_item, col))

                                cell.font = openpyxl.styles.Font(
                                    name = self.table.linked_tables[0].cellWidget(row_item, col).font().family(),
                                    size = 8,
                                    bold = True,
                                    color = 'FF0000'
                                )
                                cell.alignment = openpyxl.styles.Alignment(
                                    horizontal = 'center',
                                    vertical = 'center'
                                )
                            # Right
                            elif col == 2:
                                cell = worksheet.cell(2 + row_cell, 1 + col)

                                cell_val = wl_nlp_utils.html_to_text(self.table.linked_tables[0].cellWidget(row_item, col).text())
                                # Remove illegal characters
                                cell_val = re.sub(openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE, '', cell_val)
                                cell.value = cell_val

                                cell.font = openpyxl.styles.Font(
                                    name = self.table.linked_tables[0].cellWidget(row_item, col).font().family(),
                                    size = 8,
                                    color = '292929'
                                )
                                cell.alignment = openpyxl.styles.Alignment(
                                    horizontal = 'left',
                                    vertical = 'center'
                                )
                            else:
                                cell = worksheet.cell(2 + row_cell, 1 + col)

                                cell_val = cell_text = self.table.linked_tables[0].item(row_item, col).text()
                                # Remove illegal characters
                                cell_val = re.sub(openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE, '', cell_val)
                                cell.value = cell_val

                                if (col in self.table.linked_tables[0].headers_int or
                                    col in self.table.linked_tables[0].headers_float or
                                    col in self.table.linked_tables[0].headers_pct):
                                    self.style_cell_num(cell, self.table.linked_tables[0].item(row_item, col))
                                else:
                                    self.style_cell_text(cell, self.table.linked_tables[0].item(row_item, col))

                            self.progress_updated.emit(self.tr(f'Exporting table ... ({row_cell + 1} / {len_rows * 2})'))

                    # Row Height
                    worksheet.row_dimensions[1].height = self.table.linked_tables[0].horizontalHeader().height() / dpi_vertical * 72

                    for i, _ in enumerate(worksheet.rows):
                        worksheet.row_dimensions[2 + i].height = self.table.linked_tables[0].verticalHeader().sectionSize(0) / dpi_vertical * 72

                    self.progress_updated.emit(self.tr(f'Saving source file ...'))

                    workbook.save(file_path_src)

                    # Source file
                    workbook = openpyxl.Workbook()
                    worksheet = workbook.active

                    worksheet.freeze_panes = 'A2'

                    # Horizontal Headers
                    for col in range(self.table.columnCount()):
                        cell = worksheet.cell(1, 1 + col)
                        cell.value = self.table.horizontalHeaderItem(col).text()

                        self.style_header_horizontal(cell, self.table.horizontalHeaderItem(col))

                        worksheet.column_dimensions[openpyxl.utils.get_column_letter(1 + col)].width = self.table.horizontalHeader().sectionSize(col) / dpi_horizontal * 13 + 3

                    # Cells
                    for row_cell, row_item in enumerate(self.rows_export):
                        for col in range(self.table.columnCount()):
                            # Parallel Text
                            if col == 0:
                                cell = worksheet.cell(2 + row_cell, 1 + col)

                                cell_val = wl_nlp_utils.html_to_text(self.table.cellWidget(row_item, col).text())
                                # Remove illegal characters
                                cell_val = re.sub(openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE, '', cell_val)
                                cell.value = cell_val

                                self.style_cell_text(cell, self.table.cellWidget(row_item, col))

                                cell.font = openpyxl.styles.Font(
                                    name = self.table.cellWidget(row_item, col).font().family(),
                                    size = 8,
                                )
                                cell.alignment = openpyxl.styles.Alignment(
                                    horizontal = 'center',
                                    vertical = 'center'
                                )
                            else:
                                cell = worksheet.cell(2 + row_cell, 1 + col)

                                cell_val = cell_text = self.table.item(row_item, col).text()
                                # Remove illegal characters
                                cell_val = re.sub(openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE, '', cell_val)
                                cell.value = cell_val

                                if (col in self.table.headers_int or
                                    col in self.table.headers_float or
                                    col in self.table.headers_pct):
                                    self.style_cell_num(cell, self.table.item(row_item, col))
                                else:
                                    self.style_cell_text(cell, self.table.item(row_item, col))

                            self.progress_updated.emit(self.tr(f'Exporting table ... ({len_rows + row_cell + 1} / {len_rows * 2})'))

                    # Row Height
                    worksheet.row_dimensions[1].height = self.table.horizontalHeader().height() / dpi_vertical * 72

                    for i, _ in enumerate(worksheet.rows):
                        worksheet.row_dimensions[2 + i].height = self.table.verticalHeader().sectionSize(0) / dpi_vertical * 72

                    self.progress_updated.emit(self.tr(f'Saving target file ...'))

                    workbook.save(file_path_tgt)
                else:
                    workbook = openpyxl.Workbook()
                    worksheet = workbook.active

                    worksheet.freeze_panes = 'B2'

                    if self.table.header_orientation == 'horizontal':
                        # Horizontal Headers
                        for col in range(self.table.columnCount()):
                            cell = worksheet.cell(1, 1 + col)
                            cell.value = self.table.horizontalHeaderItem(col).text()

                            self.style_header_horizontal(cell, self.table.horizontalHeaderItem(col))

                            worksheet.column_dimensions[openpyxl.utils.get_column_letter(1 + col)].width = self.table.horizontalHeader().sectionSize(col) / dpi_horizontal * 13 + 3

                        # Cells
                        for row_cell, row_item in enumerate(self.rows_export):
                            for col in range(self.table.columnCount()):
                                cell = worksheet.cell(2 + row_cell, 1 + col)

                                cell_val = self.table.item(row_item, col).text()
                                # Remove illegal characters
                                cell_val = re.sub(openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE, '', cell_val)
                                cell.value = cell_val

                                if (col in self.table.headers_int or
                                    col in self.table.headers_float or
                                    col in self.table.headers_pct):
                                    self.style_cell_num(cell, self.table.item(row_item, col))
                                else:
                                    self.style_cell_text(cell, self.table.item(row_item, col))

                            self.progress_updated.emit(self.tr(f'Exporting table ... ({row_cell + 1} / {len_rows})'))
                    else:
                        # Horizontal Headers
                        for col in range(self.table.columnCount()):
                            cell = worksheet.cell(1, 2 + col) 
                            cell.value = self.table.horizontalHeaderItem(col).text()

                            self.style_header_horizontal(cell, self.table.horizontalHeaderItem(col))

                            worksheet.column_dimensions[openpyxl.utils.get_column_letter(2 + col)].width = self.table.horizontalHeader().sectionSize(col) / dpi_horizontal * 13 + 3

                        worksheet.column_dimensions[openpyxl.utils.get_column_letter(1)].width = self.table.verticalHeader().width() / dpi_horizontal * 13 + 3

                        # Vertical Headers
                        for row_cell, row_item in enumerate(self.rows_export):
                            cell = worksheet.cell(2 + row_cell, 1)
                            cell.value = self.table.verticalHeaderItem(row_item).text()

                            self.style_header_vertical(cell, self.table.verticalHeaderItem(row_item))

                        # Cells
                        for row_cell, row_item in enumerate(self.rows_export):
                            for col in range(self.table.columnCount()):
                                cell = worksheet.cell(2 + row_cell, 2 + col)

                                cell_val = self.table.item(row_item, col).text()
                                # Remove illegal characters
                                cell_val = re.sub(openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE, '', cell_val)
                                cell.value = cell_val

                                if (col in self.table.headers_int or
                                    col in self.table.headers_float or
                                    col in self.table.headers_pct):
                                    self.style_cell_num(cell, self.table.item(row_item, col))
                                else:
                                    self.style_cell_text(cell, self.table.item(row_item, col))

                            self.progress_updated.emit(self.tr(f'Exporting table ... ({row_cell + 1} / {len_rows})'))

                    # Row Height
                    worksheet.row_dimensions[1].height = self.table.horizontalHeader().height() / dpi_vertical * 72

                    for i, _ in enumerate(worksheet.rows):
                        worksheet.row_dimensions[2 + i].height = self.table.verticalHeader().sectionSize(0) / dpi_vertical * 72

                    self.progress_updated.emit(self.tr(f'Saving file ...'))

                    workbook.save(self.file_path)
            elif self.file_type == self.tr('Word Document (*.docx)'):
                # Concordancer
                if self.table.tab == 'concordancer':
                    outputs = []

                    doc = docx.Document()

                    for i, row in enumerate(self.rows_export):
                        output = []

                        # Zapping
                        if settings_concordancer['zapping']:
                            # Discard position information
                            if settings_concordancer['discard_position_info']:
                                for j, col in enumerate(range(3)):
                                    if self.table.item(row, col):
                                        cell_text = self.table.item(row, col).text()
                                    else:
                                        cell_text = self.table.cellWidget(row, col).text()
                                        cell_text = wl_nlp_utils.html_to_text(cell_text)

                                    output.append(cell_text)
                            else:
                                if self.table.item(row, col):
                                    cell_text = self.table.item(row, col).text()
                                else:
                                    cell_text = self.table.cellWidget(row, col).text()
                                    cell_text = wl_nlp_utils.html_to_text(cell_text)

                                output.append(cell_text)

                            output[1] = settings_concordancer['placeholder'] * settings_concordancer['replace_keywords_with']

                            if settings_concordancer['add_line_nums']:
                                output.insert(0, f'{i + 1}. ')

                            outputs.append(output)
                        else:
                            for j, col in enumerate(range(3)):
                                cell_text = self.table.cellWidget(row, col).text()
                                cell_text = wl_nlp_utils.html_to_text(cell_text)

                                output.append(cell_text)

                        if not settings_concordancer['zapping']:
                            para = doc.add_paragraph(' '.join(output))
                            para.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.JUSTIFY

                            self.progress_updated.emit(self.tr(f'Exporting table ... ({i + 1} / {len_rows})'))

                    # Randomize outputs
                    if settings_concordancer['zapping'] and settings_concordancer['randomize_outputs']:
                        random.shuffle(outputs)

                        # Re-order line numbers
                        if settings_concordancer['add_line_nums']:
                            for i, _ in enumerate(outputs):
                                outputs[i][0] = f'{i + 1}. '

                        for i, para in enumerate(outputs):
                            para = doc.add_paragraph(' '.join(para))
                            para.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.JUSTIFY

                        self.progress_updated.emit(self.tr(f'Exporting table ... ({i + 1} / {len_rows})'))

                    self.progress_updated.emit(self.tr(f'Saving file ...'))

                    doc.save(self.file_path)
                # Concordancer (Parallel Mode)
                elif self.table.tab == 'concordancer_parallel':
                    # Source file
                    doc = docx.Document()

                    for i, row in enumerate(self.rows_export):
                        output = []

                        for j, col in enumerate(range(3)):
                            cell_text = self.table.linked_tables[0].cellWidget(row, col).text()
                            cell_text = wl_nlp_utils.html_to_text(cell_text)

                            output.append(cell_text)

                        para = doc.add_paragraph(' '.join(output))
                        para.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.JUSTIFY

                        self.progress_updated.emit(self.tr(f'Exporting table ... ({i + 1} / {len_rows * 2})'))

                    doc.save(file_path_src)

                    # Target file
                    doc = docx.Document()

                    for i, row in enumerate(self.rows_export):
                        output = self.table.cellWidget(row, 0).text()

                        para = doc.add_paragraph(output)
                        para.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.JUSTIFY

                        self.progress_updated.emit(self.tr(f'Exporting table ... ({len_rows + i + 1} / {len_rows * 2})'))

                    self.progress_updated.emit(self.tr(f'Saving file ...'))

                    doc.save(file_path_tgt)
                
            self.main.settings_custom['export']['tables']['default_path'] = wl_misc.get_normalized_dir(self.file_path)
            self.main.settings_custom['export']['tables']['default_type'] = self.file_type

            export_success = True
        except PermissionError:
            export_success = False

        self.worker_done.emit(export_success, self.file_path)

    def remove_illegal_chars(self, text):
        return re.sub(openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE, '', text)

    def style_header_horizontal(self, cell, item):
        cell.font = openpyxl.styles.Font(
            name = item.font().family(),
            size = 8,
            bold = True,
            color = 'FFFFFF'
        )

        if self.table.header_orientation == 'horizontal':
            cell.fill = openpyxl.styles.PatternFill(
                fill_type = 'solid',
                fgColor = '5C88C5'
            )
        else:
            cell.fill = openpyxl.styles.PatternFill(
                fill_type = 'solid',
                fgColor = '888888'
            )

        cell.alignment = openpyxl.styles.Alignment(
            horizontal = 'center',
            vertical = 'center',
            wrap_text = True
        )

    def style_header_vertical(self, cell, item):
        cell.font = openpyxl.styles.Font(
            name = item.font().family(),
            size = 8,
            bold = True,
            color = 'FFFFFF'
        )

        if self.table.header_orientation == 'horizontal':
            cell.fill = openpyxl.styles.PatternFill(
                fill_type = 'solid',
                fgColor = '888888'
            )

            cell.alignment = openpyxl.styles.Alignment(
                horizontal = 'right',
                vertical = 'center',
                wrap_text = True
          )
        else:
            cell.fill = openpyxl.styles.PatternFill(
                fill_type = 'solid',
                fgColor = '5C88C5'
            )

            cell.alignment = openpyxl.styles.Alignment(
                horizontal = 'left',
                vertical = 'center',
                wrap_text = True
            )

    def style_cell_text(self, cell, item):
        cell.font = openpyxl.styles.Font(
            name = item.font().family(),
            size = 8,
            color = '292929'
        )

        cell.alignment = openpyxl.styles.Alignment(
            horizontal = 'left',
            vertical = 'center',
            wrap_text = True
        )

    def style_cell_num(self, cell, item):
        cell.font = openpyxl.styles.Font(
            name = item.font().family(),
            size = 8,
            color = '292929'
        )

        cell.alignment = openpyxl.styles.Alignment(
            horizontal = 'right',
            vertical = 'center',
            wrap_text = True
        )

class Wl_Table_Item(QTableWidgetItem):
    def read_data(self):
        if (self.column() in self.tableWidget().headers_int or
            self.column() in self.tableWidget().headers_float or
            self.column() in self.tableWidget().headers_pct):
            return self.val
        else:
            return self.text()

    def __lt__(self, other):
        return self.read_data() < other.read_data()

class Wl_Table_Item_Error(QTableWidgetItem):
    def read_data(self):
        return self.text()

    def __lt__(self, other):
        return self.read_data() < other.read_data()

class Wl_Table(QTableWidget):
    def __init__(
        self, parent,
        headers, header_orientation = 'horizontal',
        cols_stretch = None,
        drag_drop_enabled = False
    ):
        self.main = wl_misc.find_wl_main(parent)

        self.headers = headers
        self.header_orientation = header_orientation
        self.cols_stretch = cols_stretch or []

        self.settings = self.main.settings_custom

        if header_orientation == 'horizontal':
            super().__init__(1, len(self.headers), parent)

            self.setHorizontalHeaderLabels(self.headers)
        else:
            super().__init__(len(self.headers), 1, parent)

            self.setVerticalHeaderLabels(self.headers)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for col in self.find_col(self.cols_stretch):
            self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        if drag_drop_enabled:
            self.setDragEnabled(True)
            self.setAcceptDrops(True)
            self.viewport().setAcceptDrops(True)
            self.setDragDropMode(QAbstractItemView.InternalMove)
            self.setDragDropOverwriteMode(False)

        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().setHighlightSections(False)

        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        if self.header_orientation == 'horizontal':
            self.setStyleSheet(''' 
                QTableView {
                    outline: none;
                    color: #292929;
                }

                QTableView::item:hover {
                    background-color: #EEE;
                    color: #292929;
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
                    background-color: #3265B2;
                }

                QHeaderView::section:vertical {
                    background-color: #737373;
                }
                QHeaderView::section:vertical:hover {
                    background-color: #606060;
                }
                QHeaderView::section:vertical:pressed {
                    background-color: #606060;
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

        self.itemChanged.connect(self.item_changed)

    def dropEvent(self, event):
        if self.indexAt(event.pos()).row() == -1:
            row_dropped = self.rowCount()
        else:
            row_dropped = self.indexAt(event.pos()).row()

        selected_rows = self.get_selected_rows()

        self.blockSignals(True)

        rows_dragged = []

        for row in selected_rows:
            rows_dragged.append([])

            for col in range(self.columnCount()):
                if self.cellWidget(row, col):
                    rows_dragged[-1].append(self.cellWidget(row, col))
                else:
                    rows_dragged[-1].append(self.takeItem(row, col))

        for row in reversed(selected_rows):
            self.removeRow(row)

            if row < row_dropped:
                row_dropped -= 1

        for row, items in enumerate(rows_dragged):
            self.insertRow(row_dropped + row)

            for col, item in enumerate(items):
                if isinstance(item, QTableWidgetItem):
                    self.setItem(row_dropped + row, col, item)

                    self.item(row_dropped + row, col).setSelected(True)
                elif isinstance(item, QComboBox):
                    item_combo_box = wl_boxes.Wl_Combo_Box(self)
                    item_combo_box.addItems([item.itemText(i) for i in range(item.count())])
                    item_combo_box.setCurrentText(item.currentText())

                    self.setCellWidget(row_dropped + row, col, item_combo_box)
                elif isinstance(item, QLineEdit):
                    item_line_edit = QLineEdit(self)
                    item_line_edit.setText(item.text())

                    self.setCellWidget(row_dropped + row, col, item_line_edit)

        self.blockSignals(False)

        self.itemChanged.emit(self.item(0, 0))

        event.accept()

    def item_changed(self):
        cols_stretch = self.find_col(self.cols_stretch)

        self.resizeRowsToContents()

        for i in range(self.columnCount()):
            if i not in cols_stretch:
                self.resizeColumnToContents(i)

    def append_rows(self, labels):
        len_labels = len(labels)

        self.setRowCount(self.rowCount() + len_labels)

        for i, label in zip(range(self.rowCount() - len_labels, self.rowCount()), labels):
            self.setVerticalHeaderItem(i, QTableWidgetItem(label))

    def insert_col(self, i, label):
        super().insertColumn(i)

        self.setHorizontalHeaderItem(i, QTableWidgetItem(label))

    def export_selected(self):
        rows_export = sorted({index.row() for index in self.selectedIndexes()})

        self.export_all(rows_export = rows_export)

    def export_all(self, rows_export = None):
        def update_gui(export_success, file_path):
            self.results_exported = True

            if export_success:
                wl_msg_boxes.wl_msg_box_export_table_success(self.main, file_path)
            else:
                wl_msg_boxes.wl_msg_box_export_table_error(self.main, file_path)

        default_dir = self.main.settings_custom['export']['tables']['default_path']

        # Work Area
        if 'tab' in self.__dict__:
            if self.main.settings_custom['work_area_cur'] == 'Concordancer':
                if self.main.settings_custom['concordancer']['zapping_settings']['zapping']:
                    (file_path,
                     file_type) = QFileDialog.getSaveFileName(
                        self,
                        self.tr('Export Table'),
                        os.path.join(wl_checking_misc.check_dir(default_dir), 'Wordless_results_' + self.tab),
                        self.tr('Word Document (*.docx)'),
                        self.main.settings_custom['export']['tables']['default_type']
                    )
                else:
                    (file_path,
                     file_type) = QFileDialog.getSaveFileName(
                        self,
                        self.tr('Export Table'),
                        os.path.join(wl_checking_misc.check_dir(default_dir), 'Wordless_results_' + self.tab),
                        ';;'.join(self.main.settings_global['file_types']['export_tables_concordancer']),
                        self.main.settings_custom['export']['tables']['default_type']
                    )
            else:
                (file_path,
                 file_type) = QFileDialog.getSaveFileName(
                    self,
                    self.tr('Export Table'),
                    os.path.join(wl_checking_misc.check_dir(default_dir), 'Wordless_results_' + self.tab),
                    ';;'.join(self.main.settings_global['file_types']['export_tables']),
                    self.main.settings_custom['export']['tables']['default_type']
                )
        # Search terms, stop word lists, etc.
        else:
            (file_path,
             file_type) = QFileDialog.getSaveFileName(
                self,
                self.tr('Export Table'),
                os.path.join(wl_checking_misc.check_dir(default_dir), 'Wordless_import_error'),
                ';;'.join(self.main.settings_global['file_types']['export_tables']),
                self.main.settings_custom['export']['tables']['default_type']
            )

        if file_path:
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = self.tr('Exporting table...'))

            worker_export_table = Wl_Worker_Export_Table(
                self.main,
                dialog_progress = dialog_progress,
                update_gui = update_gui,
                table = self,
                file_path = file_path,
                file_type = file_type,
                rows_export = rows_export or []
            )

            thread_export_table = wl_threading.Wl_Thread(worker_export_table)
            thread_export_table.start_worker()

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

        self.item_changed()

    def get_selected_rows(self):
        return sorted(set([index.row() for index in self.selectedIndexes()]))

    def find_row(self, text):
        def find(text):
            for row in range(self.rowCount()):
                if self.verticalHeaderItem(row).text() == text:
                    return row

        if type(text) == list:
            return [find(text_item) for text_item in text]
        else:
            return find(text)

    def find_rows(self, text):
        return [
            row
            for row in range(self.columnCount())
            if text in self.verticalHeaderItem(row).text()
        ]

    def find_col(self, text):
        def find(text):
            for col in range(self.columnCount()):
                if self.horizontalHeaderItem(col).text() == text:
                    return col

        if type(text) == list:
            return [find(text_item) for text_item in text]
        else:
            return find(text)

    def find_cols(self, text):
        return [
            col
            for col in range(self.columnCount())
            if text in self.horizontalHeaderItem(col).text()
        ]

    def find_header(self, text):
        if self.header_orientation == 'horizontal':
            return self.find_col(text)
        else:
            return self.find_row(text)

    def find_headers(self, text):
        if self.header_orientation == 'horizontal':
            return self.find_cols(text)
        else:
            return self.find_rows(text)

class Wl_Table_Error(Wl_Table):
    def __init__(self, main, headers):
        super().__init__(main, headers)

        self.tab = 'error'

class Wl_Table_Data(Wl_Table):
    def __init__(
        self, main, tab,
        headers, header_orientation = 'horizontal',
        headers_int = None, headers_float = None,
        headers_pct = None, headers_cumulative = None, cols_breakdown = None,
        cols_stretch = None,
        sorting_enabled = False,
        linked_tables = None
    ):
        super().__init__(
            main, headers, header_orientation,
            cols_stretch,
            drag_drop_enabled = False
        )

        self.tab = tab

        self.headers_int_old = headers_int or []
        self.headers_float_old = headers_float or []
        self.headers_pct_old = headers_pct or []
        self.headers_cumulative_old = headers_cumulative or []
        self.cols_breakdown_old = cols_breakdown or []

        self.sorting_enabled = sorting_enabled
        self.linked_tables = linked_tables or []

        if sorting_enabled:
            self.setSortingEnabled(True)

            if header_orientation == 'horizontal':
                self.horizontalHeader().sortIndicatorChanged.connect(self.sorting_changed)
            else:
                self.verticalHeader().sortIndicatorChanged.connect(self.sorting_changed)

        self.itemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self.selection_changed)

        self.button_export_selected = QPushButton(self.tr('Export Selected...'), self)
        self.button_export_all = QPushButton(self.tr('Export All...'), self)
        self.button_clear = QPushButton(self.tr('Clear'), self)

        self.button_export_selected.clicked.connect(self.export_selected)
        self.button_export_all.clicked.connect(self.export_all)
        self.button_clear.clicked.connect(lambda: self.clear_table(confirm = True))

        self.clear_table()

    def item_changed(self):
        rows_visible = len([i for i in range(self.rowCount()) if not self.isRowHidden(i)])

        if [i for i in range(self.columnCount()) if self.item(0, i)] and rows_visible:
            self.button_export_all.setEnabled(True)
        else:
            self.button_export_all.setEnabled(False)

        if [i for i in range(self.columnCount()) if self.item(0, i)]:
            self.button_clear.setEnabled(True)
        else:
            self.button_clear.setEnabled(False)

        super().item_changed()

        self.selection_changed()

    def selection_changed(self):
        for table in [self] + self.linked_tables:
            if [i for i in range(table.columnCount()) if table.item(0, i)] and [i for i in range(self.rowCount()) if not self.isRowHidden(i)] and table.selectedIndexes():
                self.button_export_selected.setEnabled(True)

                break
            else:
                self.button_export_selected.setEnabled(False)

    def sorting_changed(self, logicalIndex, order):
        if [i for i in range(self.columnCount()) if self.item(0, i)]:
            self.update_ranks()

            if self.show_cumulative:
                self.toggle_cumulative()

    def append_rows(self, labels):
        headers_int = [self.verticalHeaderItem(row).text() for row in self.headers_int]
        headers_float = [self.verticalHeaderItem(row).text() for row in self.headers_float]
        headers_pct = [self.verticalHeaderItem(row).text() for row in self.headers_pct]
        headers_cumulative = [self.verticalHeaderItem(row).text() for row in self.headers_cumulative]

        super().append_rows([label for label, _, _, _, _ in labels])
        
        for label, is_int, is_float, is_pct, is_cumulative in labels:
            if is_int:
                headers_int.append(label)
            if is_float:
                headers_float.append(label)
            if is_pct:
                headers_pct.append(label)
            if is_cumulative:
                headers_cumulative.append(label)

        self.headers_int = set(self.find_row(headers_int))
        self.headers_float = set(self.find_row(headers_float))
        self.headers_pct = set(self.find_row(headers_pct))
        self.headers_cumulative = set(self.find_row(headers_cumulative))

    def insert_col(
        self, i, label,
        is_int = False, is_float = False,
        is_pct = False, is_cumulative = False, is_breakdown = False
    ):
        if self.header_orientation == 'horizontal':
            headers_int = [self.horizontalHeaderItem(col).text() for col in self.headers_int]
            headers_float = [self.horizontalHeaderItem(col).text() for col in self.headers_float]
            headers_pct = [self.horizontalHeaderItem(col).text() for col in self.headers_pct]
            headers_cumulative = [self.horizontalHeaderItem(col).text() for col in self.headers_cumulative]

        cols_breakdown = [self.horizontalHeaderItem(col).text() for col in self.cols_breakdown]

        super().insert_col(i, label)

        if is_int:
            headers_int += [label]
        if is_float:
            headers_float += [label]
        if is_pct:
            headers_pct += [label]
        if is_cumulative:
            headers_cumulative += [label]
        if is_breakdown:
            cols_breakdown += [label]

        if self.header_orientation == 'horizontal':
            self.headers_int = set(self.find_col(headers_int))
            self.headers_float = set(self.find_col(headers_float))
            self.headers_pct = set(self.find_col(headers_pct))
            self.headers_cumulative = set(self.find_col(headers_cumulative))
        
        self.cols_breakdown = set(self.find_col(cols_breakdown))

    def set_item_num(self, row, col, val, total = -1):
        if self.header_orientation == 'horizontal':
            header = col
        else:
            header = row

        # Integers
        if header in self.headers_int:
            val = int(val)

            item = Wl_Table_Item(str(val))
        # Floats
        elif header in self.headers_float:
            val = float(val)
            precision = self.main.settings_custom['data']['precision_decimal']

            item = Wl_Table_Item(f'{val:.{precision}f}')
        # Percentages
        elif header in self.headers_pct:
            if total > 0:
                val = val / total
            # Handle zero division error
            elif total == 0:
                val = 0
            # Set values directly
            elif total == -1:
                val = float(val)

            precision = self.main.settings_custom['data']['precision_pct']

            item = Wl_Table_Item(f'{val:.{precision}%}')

        item.val = val

        item.setFont(QFont('Consolas'))
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

        super().setItem(row, col, item)

    def set_item_num_val(self, row, col, val):
        if self.header_orientation == 'horizontal':
            header = col
        else:
            header = row

        item = self.item(row, col)

        # Integers
        if header in self.headers_int:
            item.setText(str(val))
        # Floats
        elif header in self.headers_float:
            val = float(val)
            precision = self.main.settings_custom['data']['precision_decimal']

            item.setText(f'{val:.{precision}f}')
        # Percentages
        elif header in self.headers_pct:
            precision = self.main.settings_custom['data']['precision_pct']

            item.setText(f'{val:.{precision}%}')

        item.val = val

    def set_item_error(self, row, col, text):
        item = Wl_Table_Item_Error(text)

        item_font = QFont('Consolas')
        item_font.setBold(True)

        item.setFont(item_font)
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

        super().setItem(row, col, item)

    def update_ranks(self):
        data_prev = ''
        rank_prev = 1
        rank_next = 1

        sort_section = self.horizontalHeader().sortIndicatorSection()
        sort_order = self.horizontalHeader().sortIndicatorOrder()

        col_rank = self.find_col(self.tr('Rank'))

        self.sortItems(sort_section, sort_order)

        if sort_section != col_rank:
            self.blockSignals(True)
            self.setSortingEnabled(False)
            self.setUpdatesEnabled(False)

            for row in range(self.rowCount()):
                if not self.isRowHidden(row):
                    data_cur = self.item(row, sort_section).read_data()

                    if self.main.settings_custom['data']['continue_numbering_after_ties']:
                        if data_cur == data_prev:
                            self.item(row, col_rank).val = rank_prev
                            self.item(row, col_rank).setText(str(rank_prev))
                        else:
                            self.item(row, col_rank).val = rank_next
                            self.item(row, col_rank).setText(str(rank_next))

                            rank_prev = rank_next
                            rank_next += 1
                            
                        data_prev = data_cur
                    else:
                        if data_cur == data_prev:
                            self.item(row, col_rank).val = rank_prev
                            self.item(row, col_rank).setText(str(rank_prev))
                        else:
                            self.item(row, col_rank).val = rank_next
                            self.item(row, col_rank).setText(str(rank_next))

                            rank_prev = rank_next

                        rank_next += 1
                        data_prev = data_cur

            self.blockSignals(False)
            self.setSortingEnabled(True)
            self.setUpdatesEnabled(True)

    def toggle_pct(self):
        self.setUpdatesEnabled(False)

        if self.header_orientation == 'horizontal':
            if self.show_pct:
                for col in self.headers_pct:
                    self.showColumn(col)
            else:
                for col in self.headers_pct:
                    self.hideColumn(col)
        else:
            if self.show_pct:
                for row in self.headers_pct:
                    self.showRow(row)
            else:
                for row in self.headers_pct:
                    self.hideRow(row)

        self.setUpdatesEnabled(True)

    def toggle_cumulative(self):
        precision_decimal = self.main.settings_custom['data']['precision_decimal']
        precision_pct = self.main.settings_custom['data']['precision_pct']

        # Boost performance
        self.sortItems(self.horizontalHeader().sortIndicatorSection(), self.horizontalHeader().sortIndicatorOrder())

        self.blockSignals(True)
        self.setSortingEnabled(False)
        self.setUpdatesEnabled(False)

        if self.header_orientation == 'horizontal':
            if self.show_cumulative:
                for col in self.headers_cumulative:
                    val_cumulative = 0

                    # Integers
                    if col in self.headers_int:
                        for row in range(self.rowCount()):
                            if not self.isRowHidden(row):
                                item = self.item(row, col)

                                val_cumulative += item.val
                                item.setText(str(val_cumulative))
                    # Floats
                    elif col in self.headers_float:
                        for row in range(self.rowCount()):
                            if not self.isRowHidden(row):
                                item = self.item(row, col)

                                val_cumulative += item.val
                                item.setText(f'{val_cumulative:.{precision_decimal}}')
                    # Percentages
                    elif col in self.headers_pct:
                        for row in range(self.rowCount()):
                            if not self.isRowHidden(row):
                                item = self.item(row, col)

                                val_cumulative += item.val
                                item.setText(f'{val_cumulative:.{precision_pct}%}')
            else:
                for col in self.headers_cumulative:
                    # Integers
                    if col in self.headers_int:
                        for row in range(self.rowCount()):
                            if not self.isRowHidden(row):
                                item = self.item(row, col)

                                item.setText(str(item.val))
                    # Floats
                    elif col in self.headers_float:
                        for row in range(self.rowCount()):
                            if not self.isRowHidden(row):
                                item = self.item(row, col)

                                item.setText(f'{item.val:.{precision_decimal}}')
                    # Percentages
                    elif col in self.headers_pct:
                        for row in range(self.rowCount()):
                            if not self.isRowHidden(row):
                                item = self.item(row, col)

                                item.setText(f'{item.val:.{precision_pct}%}')
        else:
            if self.show_cumulative:
                for row in self.headers_cumulative:
                    val_cumulative = 0

                    for col in range(self.columnCount() - 1):
                        item = self.item(row, col)

                        if not self.isColumnHidden(col) and not isinstance(item, Wl_Table_Item_Error):
                            val_cumulative += item.val

                            # Integers
                            if row in self.headers_int:
                                item.setText(str(val_cumulative))
                            # Floats
                            elif row in self.headers_float:
                                item.setText(f'{val_cumulative:.{precision_decimal}}')
                            # Percentages
                            elif row in self.headers_pct:
                                item.setText(f'{val_cumulative:.{precision_pct}%}')
            else:
                for row in self.headers_cumulative:
                    for col in range(self.columnCount() - 1):
                        item = self.item(row, col)

                        if not self.isColumnHidden(col) and not isinstance(item, Wl_Table_Item_Error):
                            # Integers
                            if row in self.headers_int:
                                item.setText(str(item.val))
                            # Floats
                            elif row in self.headers_float:
                                item.setText(f'{item.val:.{precision_decimal}}')
                            # Percentages
                            elif row in self.headers_pct:
                                item.setText(f'{item.val:.{precision_pct}%}')

        self.blockSignals(False)
        self.setUpdatesEnabled(True)

        if self.sorting_enabled:
            self.setSortingEnabled(True)

    def toggle_breakdown(self):
        self.setUpdatesEnabled(False)

        if self.show_breakdown:
            for col in self.cols_breakdown:
                self.showColumn(col)
        else:
            for col in self.cols_breakdown:
                self.hideColumn(col)

        self.setUpdatesEnabled(True)

    def filter_table(self):
        rank_prev = 1
        rank_next = 1
        data_prev = ''

        self.hide()
        self.setUpdatesEnabled(False)
        
        for i, row_filter in enumerate(self.row_filters):
            if row_filter:
                self.showRow(i)
            else:
                self.hideRow(i)

        self.setUpdatesEnabled(True)
        self.show()

        self.toggle_cumulative()
        self.update_ranks()

        self.itemChanged.emit(self.item(0, 0))

    def clear_table(self, count_headers = 1, confirm = False):
        confirmed = True

        # Ask for confirmation if results have not been exported
        if confirm:
            if not self.results_exported and (self.item(0, 0) or self.cellWidget(0, 0)):
                dialog_clear_table = wl_dialogs_misc.WL_Dialog_Clear_Table(self.main)
                result = dialog_clear_table.exec_()

                if result == QDialog.Rejected:
                    confirmed = False

        if confirmed:
            for table in [self] + self.linked_tables:
                table.clearContents()

                if table.header_orientation == 'horizontal':
                    table.horizontalHeader().blockSignals(True)

                    table.setColumnCount(len(table.headers))
                    table.setRowCount(count_headers)

                    table.setHorizontalHeaderLabels(table.headers)

                    table.horizontalHeader().blockSignals(False)

                    table.horizontalHeader().sectionCountChanged.emit(0, count_headers)
                else:
                    table.verticalHeader().blockSignals(True)

                    table.setRowCount(len(table.headers))
                    table.setColumnCount(count_headers)

                    table.setVerticalHeaderLabels(table.headers)

                    table.verticalHeader().blockSignals(False)

                    table.verticalHeader().sectionCountChanged.emit(0, count_headers)

                for i in range(table.rowCount()):
                    table.showRow(i)

                for i in range(table.columnCount()):
                    table.showColumn(i)

                table.headers_int = set(table.find_header(table.headers_int_old))
                table.headers_float = set(table.find_header(table.headers_float_old))
                table.headers_pct = set(table.find_header(table.headers_pct_old))
                table.headers_cumulative = set(table.find_header(table.headers_cumulative_old))
                table.cols_breakdown = set(table.find_col(table.cols_breakdown_old))

                table.results_exported = False

                table.itemChanged.emit(table.item(0, 0))

        return confirmed

    def add_linked_table(self, table):
        self.linked_tables.append(table)

        table.itemSelectionChanged.connect(self.selection_changed)

    def add_linked_tables(self, tables):
        for table in tables:
            self.add_linked_table(table)

class Wl_Worker_Results_Search(wl_threading.Wl_Worker):
    def run(self):
        for table in self.dialog.tables:
            results = {}
            search_terms = set()

            for col in range(table.columnCount()):
                if table.cellWidget(0, col):
                    for row in range(table.rowCount()):
                        results[(row, col)] = table.cellWidget(row, col).text_search
                else:
                    for row in range(table.rowCount()):
                        try:
                            results[(row, col)] = table.item(row, col).text_raw
                        except:
                            results[(row, col)] = [table.item(row, col).text()]

            items = [token for text in results.values() for token in text]

            for file in table.settings['file_area']['files_open']:
                if file['selected']:
                    search_terms_file = wl_matching.match_search_terms(
                        self.main, items,
                        lang = file['lang'],
                        tokenized = file['tokenized'],
                        tagged = file['tagged'],
                        token_settings = table.settings[self.dialog.tab]['token_settings'],
                        search_settings = self.dialog.settings)

                    search_terms |= set(search_terms_file)

            for search_term in search_terms:
                len_search_term = len(search_term)

                for (row, col), text in results.items():
                    for ngram in nltk.ngrams(text, len_search_term):
                        if ngram == search_term:
                            self.dialog.items_found.append([table, row, col])

        self.dialog.items_found = sorted(
            self.dialog.items_found,
            key = lambda item: (id(item[0]), item[1], item[2])
        )

        self.progress_updated.emit(self.tr('Highlighting items ...'))

        time.sleep(0.1)

        self.worker_done.emit()

class Wl_Dialog_Results_Search(wl_dialogs.Wl_Dialog):
    def __init__(self, main, tab, table):
        super().__init__(main, main.tr('Search in Results'))

        self.tab = tab
        self.tables = [table]
        self.settings = self.main.settings_custom[self.tab]['search_results']
        self.items_found = []

        (
            self.label_search_term,
            self.checkbox_multi_search_mode,

            self.stacked_widget_search_term,
            self.line_edit_search_term,
            self.list_search_terms,

            self.label_separator,

            self.checkbox_ignore_case,
            self.checkbox_match_inflected_forms,
            self.checkbox_match_whole_words,
            self.checkbox_use_regex,

            self.checkbox_ignore_tags,
            self.checkbox_match_tags
        ) = wl_widgets.wl_widgets_search_settings(self, self.tab)

        self.button_find_next = QPushButton(self.tr('Find Next'), self)
        self.button_find_prev = QPushButton(self.tr('Find Previous'), self)
        self.button_find_all = QPushButton(self.tr('Find All'), self)
        # Pad with spaces
        self.button_clear_hightlights = QPushButton(self.tr(' Clear Highlights '), self)
        
        self.button_restore_default_settings = wl_buttons.Wl_Button_Restore_Default_Settings(self)
        self.button_close = QPushButton(self.tr('Close'), self)

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.button_find_next.click)
        self.list_search_terms.model().dataChanged.connect(self.search_settings_changed)

        self.checkbox_ignore_case.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_inflected_forms.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_whole_words.stateChanged.connect(self.search_settings_changed)
        self.checkbox_use_regex.stateChanged.connect(self.search_settings_changed)

        self.checkbox_ignore_tags.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_tags.stateChanged.connect(self.search_settings_changed)

        self.button_find_next.clicked.connect(lambda: self.find_next())
        self.button_find_prev.clicked.connect(lambda: self.find_prev())
        self.button_find_all.clicked.connect(lambda: self.find_all())
        self.button_clear_hightlights.clicked.connect(self.clear_highlights)
        
        self.button_close.clicked.connect(self.reject)

        layout_buttons_right = wl_layouts.Wl_Layout()
        layout_buttons_right.addWidget(self.button_find_next, 0, 0)
        layout_buttons_right.addWidget(self.button_find_prev, 1, 0)
        layout_buttons_right.addWidget(self.button_find_all, 2, 0)
        layout_buttons_right.addWidget(self.button_clear_hightlights, 3, 0)

        layout_buttons_right.setRowStretch(4, 1)

        layout_buttons_bottom = wl_layouts.Wl_Layout()
        layout_buttons_bottom.addWidget(self.button_restore_default_settings, 0, 0)
        layout_buttons_bottom.addWidget(self.button_close, 0, 2)

        layout_buttons_bottom.setColumnStretch(1, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.label_search_term, 0, 0)
        self.layout().addWidget(self.checkbox_multi_search_mode, 0, 1, Qt.AlignRight)
        self.layout().addWidget(self.stacked_widget_search_term, 1, 0, 1, 2)
        self.layout().addWidget(self.label_separator, 2, 0, 1, 2)

        self.layout().addWidget(self.checkbox_ignore_case, 3, 0, 1, 2)
        self.layout().addWidget(self.checkbox_match_inflected_forms, 4, 0, 1, 2)
        self.layout().addWidget(self.checkbox_match_whole_words, 5, 0, 1, 2)
        self.layout().addWidget(self.checkbox_use_regex, 6, 0, 1, 2)

        self.layout().addWidget(self.checkbox_ignore_tags, 7, 0, 1, 2)
        self.layout().addWidget(self.checkbox_match_tags, 8, 0, 1, 2)

        self.layout().addWidget(wl_layouts.Wl_Separator(self, orientation = 'Vertical'), 0, 2, 9, 1)
        self.layout().addLayout(layout_buttons_right, 0, 3, 9, 1)

        self.layout().addWidget(wl_layouts.Wl_Separator(self), 9, 0, 1, 4)
        self.layout().addLayout(layout_buttons_bottom, 10, 0, 1, 4)

        self.main.wl_work_area.currentChanged.connect(self.reject)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['search_results'])
        else:
            settings = copy.deepcopy(self.settings)

        self.checkbox_multi_search_mode.setChecked(settings['multi_search_mode'])

        if not defaults:
            self.line_edit_search_term.setText(settings['search_term'])
            self.list_search_terms.load_items(settings['search_terms'])

        self.checkbox_ignore_case.setChecked(settings['ignore_case'])
        self.checkbox_match_inflected_forms.setChecked(settings['match_inflected_forms'])
        self.checkbox_match_whole_words.setChecked(settings['match_whole_words'])
        self.checkbox_use_regex.setChecked(settings['use_regex'])

        self.checkbox_ignore_tags.setChecked(settings['ignore_tags'])
        self.checkbox_match_tags.setChecked(settings['match_tags'])

        self.search_settings_changed()

    def search_settings_changed(self):
        self.settings['multi_search_mode'] = self.checkbox_multi_search_mode.isChecked()
        self.settings['search_term'] = self.line_edit_search_term.text()
        self.settings['search_terms'] = self.list_search_terms.model().stringList()

        self.settings['ignore_case'] = self.checkbox_ignore_case.isChecked()
        self.settings['match_inflected_forms'] = self.checkbox_match_inflected_forms.isChecked()
        self.settings['match_whole_words'] = self.checkbox_match_whole_words.isChecked()
        self.settings['use_regex'] = self.checkbox_use_regex.isChecked()

        self.settings['ignore_tags'] = self.checkbox_ignore_tags.isChecked()
        self.settings['match_tags'] = self.checkbox_match_tags.isChecked()

        if 'size_multi' in self.__dict__:
            if self.settings['multi_search_mode']:
                self.setFixedSize(self.size_multi)
            else:
                self.setFixedSize(self.size_normal)

    @wl_misc.log_timing
    def find_next(self):
        self.find_all()

        if self.items_found:
            selected_rows = []

            for table in self.tables:
                table.hide()
                table.blockSignals(True)
                table.setUpdatesEnabled(False)

            for table in self.tables:
                if table.get_selected_rows():
                    selected_rows = [id(table), table.get_selected_rows()]

                    break

            # Scroll to the next found item
            if selected_rows:
                for table in self.tables:
                    table.clearSelection()

                for table, row, _ in self.items_found:
                    # Tables are sorted by their string representations
                    if (id(table) > selected_rows[0] or
                        id(table) == selected_rows[0] and row > selected_rows[1][-1]):
                        table.selectRow(row)
                        table.setFocus()

                        table.scrollToItem(table.item(row, 0))

                        break

                # Scroll to top if this is the last item
                if not any([table.selectedItems() for table in self.tables]):
                    self.tables[0].scrollToItem(table.item(self.items_found[0][1], 0))
                    self.tables[0].selectRow(self.items_found[0][1])
            else:
                self.tables[0].scrollToItem(table.item(self.items_found[0][1], 0))
                self.tables[0].selectRow(self.items_found[0][1])

            for table in self.tables:
                table.blockSignals(False)
                table.setUpdatesEnabled(True)
                table.show()

    @wl_misc.log_timing
    def find_prev(self):
        self.find_all()

        if self.items_found:
            selected_rows = []

            for table in self.tables:
                table.hide()
                table.blockSignals(True)
                table.setUpdatesEnabled(False)

            for table in self.tables:
                if table.get_selected_rows():
                    selected_rows = [id(table), table.get_selected_rows()]

                    break

            # Scroll to the previous found item
            if selected_rows:
                for table in self.tables:
                    table.clearSelection()

                for table, row, _ in reversed(self.items_found):
                    # Tables are sorted by their string representations
                    if (id(table) < selected_rows[0] or
                        id(table) == selected_rows[0] and row < selected_rows[1][-1]):
                        table.selectRow(row)
                        table.setFocus()

                        table.scrollToItem(table.item(row, 0))

                        break

                # Scroll to bottom if this is the first item
                if not any([table.selectedItems() for table in self.tables]):
                    self.tables[-1].scrollToItem(table.item(self.items_found[-1][1], 0))
                    self.tables[-1].selectRow(self.items_found[-1][1])
            else:
                self.tables[-1].scrollToItem(table.item(self.items_found[-1][1], 0))
                self.tables[-1].selectRow(self.items_found[-1][1])

            for table in self.tables:
                table.blockSignals(False)
                table.setUpdatesEnabled(True)
                table.show()

    @wl_misc.log_timing
    def find_all(self):
        def update_gui():
            if self.items_found:
                for table in self.tables:
                    table.hide()
                    table.blockSignals(True)
                    table.setUpdatesEnabled(False)

                for table, row, col in self.items_found:
                    if table.cellWidget(row, col):
                        table.cellWidget(row, col).setStyleSheet('border: 1px solid #E53E3A;')
                    else:
                        table.item(row, col).setForeground(QBrush(QColor('#FFF')))
                        table.item(row, col).setBackground(QBrush(QColor('#E53E3A')))

                for table in self.tables:
                    table.blockSignals(False)
                    table.setUpdatesEnabled(True)
                    table.show()
            else:
                wl_msg_boxes.wl_msg_box_no_search_results(self.main)

            wl_msgs.wl_msg_results_search_success(self.main, self.items_found)

        if (not self.settings['multi_search_mode'] and self.settings['search_term'] or
            self.settings['multi_search_mode'] and self.settings['search_terms']):
            self.clear_highlights()

            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = self.tr('Searching in results...'))

            worker_results_search = Wl_Worker_Results_Search(
                self.main,
                dialog_progress = dialog_progress,
                update_gui = update_gui,
                dialog = self
            )

            thread_results_search = wl_threading.Wl_Thread(worker_results_search)
            thread_results_search.start_worker()
        else:
            wl_msg_boxes.wl_msg_box_missing_search_terms(self.main)

            wl_msgs.wl_msg_results_search_error(self.main)

    def clear_highlights(self):
        if self.items_found:
            for table in self.tables:
                table.hide()
                table.blockSignals(True)
                table.setUpdatesEnabled(False)

            for table, row, col in self.items_found:
                if table.cellWidget(row, col):
                    table.cellWidget(row, col).setStyleSheet('border: 0')
                else:
                    table.item(row, col).setForeground(QBrush(QColor('#292929')))
                    table.item(row, col).setBackground(QBrush(QColor('#FFF')))

            for table in self.tables:
                table.blockSignals(False)
                table.setUpdatesEnabled(True)
                table.show()

            self.items_found.clear()

    def load(self):
        # Calculate size
        if 'size_multi' not in self.__dict__:
            multi_search_mode = self.settings['multi_search_mode']

            self.checkbox_multi_search_mode.setChecked(False)

            self.adjustSize()
            self.size_normal = self.size()

            self.checkbox_multi_search_mode.setChecked(True)

            self.adjustSize()
            self.size_multi = QSize(self.size_normal.width(), self.size().height())

            self.checkbox_multi_search_mode.setChecked(multi_search_mode)

        self.show()

    def add_tables(self, tables):
        self.tables.extend(tables)

class Wl_Button_Results_Search(wl_buttons.Wl_Button):
    def __init__(self, parent, tab, table):
        super().__init__(parent.tr('Search in Results'), parent)

        self.dialog_results_search = Wl_Dialog_Results_Search(
            self.main,
            tab = tab,
            table = table
        )

        self.setFixedWidth(150)

        self.clicked.connect(self.dialog_results_search.load)

    def add_tables(self, tables):
        self.dialog_results_search.add_tables(tables)

class Wl_Table_Data_Search(Wl_Table_Data):
    def __init__(
        self, main, tab,
        headers, header_orientation = 'horizontal',
        headers_int = None, headers_float = None,
        headers_pct = None, headers_cumulative = None, cols_breakdown = None,
        cols_stretch = None,
        sorting_enabled = False
    ):
        super().__init__(
            main, tab,
            headers, header_orientation,
            headers_int, headers_float,
            headers_pct, headers_cumulative, cols_breakdown,
            cols_stretch,
            sorting_enabled
        )

        self.label_number_results = QLabel()
        self.button_results_search = wl_buttons.Wl_Button_Results_Search(
            self,
            tab = self.tab,
            table = self
        )

        self.itemChanged.connect(self.results_changed)

        self.results_changed()

    def results_changed(self):
        rows_visible = len([i for i in range(self.rowCount()) if not self.isRowHidden(i)])

        if [i for i in range(self.columnCount()) if self.item(0, i)] and rows_visible:
            self.label_number_results.setText(self.tr(f'Number of Results: {rows_visible}'))

            self.button_results_search.setEnabled(True)
        else:
            self.label_number_results.setText(self.tr('Number of Results: 0'))

            self.button_results_search.setEnabled(False)

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

class Wl_Table_Results_Sort_Conordancer(Wl_Table):
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
                    self.cellWidget(i, 1).currentIndex()
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
                self.cellWidget(self.rowCount() - 1, 1).setCurrentIndex(sorting_order)

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
        combo_box_sorting_col = wl_boxes.Wl_Combo_Box(self)
        combo_box_sorting_order = wl_boxes.Wl_Combo_Box(self)

        combo_box_sorting_col.addItems(self.cols_to_sort)
        combo_box_sorting_order.addItems([
            self.tr('Ascending'),
            self.tr('Descending')
        ])

        if combo_box_sorting_col.findText('L1') > -1:
            width_left = max([
                int(combo_box_sorting_col.itemText(i)[1:])
                for i in range(combo_box_sorting_col.count())
                if re.search(r'^L[0-9]+?$', combo_box_sorting_col.itemText(i))
            ])
        else:
            width_left = 0

        if combo_box_sorting_col.findText('R1') > -1:
            width_right = max([
                int(combo_box_sorting_col.itemText(i)[1:])
                for i in range(combo_box_sorting_col.count())
                if re.search(r'^R[0-9]+?$', combo_box_sorting_col.itemText(i))
            ])
        else:
            width_right = 0

        cols_left = [
            int(self.cellWidget(i, 0).currentText()[1:])
            for i in range(self.rowCount())
            if re.search(r'^L[0-9]+?$', self.cellWidget(i, 0).currentText())
        ]
        cols_right = [
            int(self.cellWidget(i, 0).currentText()[1:])
            for i in range(self.rowCount())
            if re.search(r'^R[0-9]+?$', self.cellWidget(i, 0).currentText())
        ]

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

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.table.tab]['sort_results'])
        else:
            settings = copy.deepcopy(self.main.settings_custom[self.table.tab]['sort_results'])

        self.clear_table(0)

        for sorting_col, sorting_order in settings['sorting_rules']:
            self.add_row()

            self.cellWidget(self.rowCount() - 1, 0).setCurrentText(sorting_col)
            self.cellWidget(self.rowCount() - 1, 1).setCurrentIndex(sorting_order)

        self.clearSelection()

class Wl_Dialog_Results_Sort_Concordancer(wl_dialogs.Wl_Dialog):
    def __init__(self, main, table):
        super().__init__(main, main.tr('Sort Results'))

        self.tables = [table]
        self.settings = self.main.settings_custom[self.tables[0].tab]['sort_results']

        self.table_sort = Wl_Table_Results_Sort_Conordancer(self, table = self.tables[0])

        self.button_restore_default_settings = wl_buttons.Wl_Button_Restore_Default_Settings(self)
        self.button_sort = QPushButton(self.tr('Sort'), self)
        self.button_close = QPushButton(self.tr('Close'), self)

        self.table_sort.setFixedWidth(350)
        self.table_sort.setFixedHeight(200)

        if self.tables[0].tab == 'concordancer':
            self.button_sort.clicked.connect(lambda: self.sort_results())
        elif self.tables[0].tab == 'concordancer_parallel':
            self.button_sort.clicked.connect(lambda: self.sort_results_parallel())

        self.button_close.clicked.connect(self.reject)

        layout_table_sort = wl_layouts.Wl_Layout()
        layout_table_sort.addWidget(self.table_sort, 0, 0, 4, 1)
        layout_table_sort.addWidget(self.table_sort.button_add, 0, 1)
        layout_table_sort.addWidget(self.table_sort.button_insert, 1, 1)
        layout_table_sort.addWidget(self.table_sort.button_remove, 2, 1)

        layout_table_sort.setRowStretch(3, 1)

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

    # To be called by "Restore Default Settings"
    def load_settings(self, defaults = False):
        self.table_sort.load_settings(defaults = defaults)

    @wl_misc.log_timing
    def sort_results(self):
        def update_gui(results):
            # Create new labels
            for i, (left_old, node_old, right_old,
                    _, _, _, _, _, _, _, _) in enumerate(results):
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
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = self.tr('Sorting results...'))

            worker_results_sort_concordancer = Wl_Worker_Results_Sort_Concordancer(
                self.main,
                dialog_progress = dialog_progress,
                update_gui = update_gui,
                dialog = self
            )

            thread_results_sort_concordancer = wl_threading.Wl_Thread(worker_results_sort_concordancer)
            thread_results_sort_concordancer.start_worker()

        wl_msgs.wl_msg_results_sort(self.main)

    @wl_misc.log_timing
    def sort_results_parallel(self):
        def update_gui(results_src, results_tgt):
            results = []

            # Create new labels
            for ((left_old, node_old, right_old,
                  no_seg_src, no_seg_pct_src),
                 (parallel_text_old,
                  no_seg_tgt, no_seg_pct_tgt)) in zip(results_src, results_tgt):
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
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = self.tr('Sorting results...'))

            worker_results_sort_concordancer_parallel = Wl_Worker_Results_Sort_Concordancer_Parallel(
                self.main,
                dialog_progress = dialog_progress,
                update_gui = update_gui,
                dialog = self
            )

            thread_results_sort_concordancer_parallel = wl_threading.Wl_Thread(worker_results_sort_concordancer_parallel)
            thread_results_sort_concordancer_parallel.start_worker()

        wl_msgs.wl_msg_results_sort(self.main)

    def add_tables(self, tables):
        self.tables.extend(tables)

class Wl_Button_Results_Sort(wl_buttons.Wl_Button):
    def __init__(self, parent, table):
        super().__init__(parent.tr('Sort Results'), parent)

        self.dialog_results_sort = Wl_Dialog_Results_Sort_Concordancer(
            self.main,
            table = table
        )

        self.setFixedWidth(150)

        self.clicked.connect(self.dialog_results_sort.show)

    def add_tables(self, tables):
        self.dialog_results_sort.add_tables(tables)

class Wl_Table_Data_Sort_Search(Wl_Table_Data):
    def __init__(
        self, main, tab,
        headers, header_orientation = 'horizontal',
        headers_int = None, headers_float = None,
        headers_pct = None, headers_cumulative = None, cols_breakdown = None,
        cols_stretch = None,
        sorting_enabled = False
    ):
        super().__init__(
            main, tab,
            headers, header_orientation,
            headers_int, headers_float,
            headers_pct, headers_cumulative, cols_breakdown,
            cols_stretch,
            sorting_enabled
        )

        self.label_number_results = QLabel()
        self.button_results_sort = Wl_Button_Results_Sort(
            self,
            table = self
        )
        self.button_results_search = Wl_Button_Results_Search(
            self,
            tab = self.tab,
            table = self
        )

        self.itemChanged.connect(self.results_changed)

        self.results_changed()

    def results_changed(self):
        rows_visible = len([i for i in range(self.rowCount()) if not self.isRowHidden(i)])

        if [i for i in range(self.columnCount()) if self.item(0, i)] and rows_visible:
            self.label_number_results.setText(self.tr(f'Number of Results: {rows_visible}'))

            self.button_results_sort.setEnabled(True)
            self.button_results_search.setEnabled(True)
        else:
            self.label_number_results.setText(self.tr('Number of Results: 0'))

            self.button_results_sort.setEnabled(False)
            self.button_results_search.setEnabled(False)

    def add_tables(self, tables):
        self.button_results_sort.add_tables(tables)
        self.button_results_search.add_tables(tables)

class Wl_Worker_Results_Filter_Wordlist(wl_threading.Wl_Worker):
    def run(self):
        text_measure_dispersion = self.dialog.table.settings[self.dialog.tab]['generation_settings']['measure_dispersion']
        text_measure_adjusted_freq = self.dialog.table.settings[self.dialog.tab]['generation_settings']['measure_adjusted_freq']

        text_dispersion = self.main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
        text_adjusted_freq =  self.main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

        if self.dialog.tab == 'wordlist':
            col_token = self.dialog.table.find_col(self.tr('Token'))
        elif self.dialog.tab == 'ngram':
            col_ngram = self.dialog.table.find_col(self.tr('N-gram'))

        if self.dialog.settings['file_to_filter'] == self.tr('Total'):
            col_freq = self.dialog.table.find_col(
                self.tr('Total\nFrequency')
            )
            col_dispersion = self.dialog.table.find_col(
                self.tr(f'Total\n{text_dispersion}')
            )
            col_adjusted_freq = self.dialog.table.find_col(
                self.tr(f'Total\n{text_adjusted_freq}')
            )
        else:
            col_freq = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\nFrequency")
            )
            col_dispersion = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_dispersion}")
            )
            col_adjusted_freq = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_adjusted_freq}")
            )

        col_num_files_found = self.dialog.table.find_col(self.tr('Number of\nFiles Found'))

        if self.dialog.tab == 'wordlist':
            len_token_min = (
                float('-inf')
                if self.dialog.settings['len_token_min_no_limit']
                else self.dialog.settings['len_token_min']
            )
            len_token_max = (
                float('inf')
                if self.dialog.settings['len_token_max_no_limit']
                else self.dialog.settings['len_token_max']
            )
        elif self.dialog.tab == 'ngram':
            len_ngram_min = (
                float('-inf')
                if self.dialog.settings['len_ngram_min_no_limit']
                else self.dialog.settings['len_ngram_min']
            )
            len_ngram_max = (
                float('inf')
                if self.dialog.settings['len_ngram_max_no_limit']
                else self.dialog.settings['len_ngram_max']
            )

        freq_min = (
            float('-inf')
            if self.dialog.settings['freq_min_no_limit']
            else self.dialog.settings['freq_min']
        )
        freq_max = (
            float('inf')
            if self.dialog.settings['freq_max_no_limit']
            else self.dialog.settings['freq_max']
        )

        dispersion_min = (
            float('-inf')
            if self.dialog.settings['dispersion_min_no_limit']
            else self.dialog.settings['dispersion_min']
        )
        dispersion_max = (
            float('inf')
            if self.dialog.settings['dispersion_max_no_limit']
            else self.dialog.settings['dispersion_max']
        )

        adjusted_freq_min = (
            float('-inf')
            if self.dialog.settings['adjusted_freq_min_no_limit']
            else self.dialog.settings['adjusted_freq_min']
        )
        adjusted_freq_max = (
            float('inf')
            if self.dialog.settings['adjusted_freq_max_no_limit']
            else self.dialog.settings['adjusted_freq_max']
        )

        num_files_found_min = (
            float('-inf')
            if self.dialog.settings['num_files_found_min_no_limit']
            else self.dialog.settings['num_files_found_min']
        )
        num_files_found_max = (
            float('inf')
            if self.dialog.settings['num_files_found_max_no_limit']
            else self.dialog.settings['num_files_found_max']
        )

        self.dialog.table.row_filters = []

        if self.dialog.tab == 'wordlist':
            for i in range(self.dialog.table.rowCount()):
                if (
                    len_token_min       <= len(self.dialog.table.item(i, col_token).text())   <= len_token_max and
                    freq_min            <= self.dialog.table.item(i, col_freq).val            <= freq_max and
                    dispersion_min      <= self.dialog.table.item(i, col_dispersion).val      <= dispersion_max and
                    adjusted_freq_min   <= self.dialog.table.item(i, col_adjusted_freq).val   <= adjusted_freq_max and
                    num_files_found_min <= self.dialog.table.item(i, col_num_files_found).val <= num_files_found_max
                ):
                    self.dialog.table.row_filters.append(True)
                else:
                    self.dialog.table.row_filters.append(False)
        elif self.dialog.tab == 'ngram':
            for i in range(self.dialog.table.rowCount()):
                if (
                    len_ngram_min       <= len(self.dialog.table.item(i, col_ngram).text())   <= len_ngram_max and
                    freq_min            <= self.dialog.table.item(i, col_freq).val            <= freq_max and
                    dispersion_min      <= self.dialog.table.item(i, col_dispersion).val      <= dispersion_max and
                    adjusted_freq_min   <= self.dialog.table.item(i, col_adjusted_freq).val   <= adjusted_freq_max and
                    num_files_found_min <= self.dialog.table.item(i, col_num_files_found).val <= num_files_found_max
                ):
                    self.dialog.table.row_filters.append(True)
                else:
                    self.dialog.table.row_filters.append(False)

        self.progress_updated.emit(self.tr('Updating table ...'))

        time.sleep(0.1)

        self.worker_done.emit()

class Wl_Worker_Results_Filter_Collocation(wl_threading.Wl_Worker):
    def run(self):
        text_test_significance = self.dialog.table.settings['collocation']['generation_settings']['test_significance']
        text_measure_effect_size = self.dialog.table.settings['collocation']['generation_settings']['measure_effect_size']

        (
            text_test_stat,
            text_p_value,
            text_bayes_factor
        ) = self.main.settings_global['tests_significance']['collocation'][text_test_significance]['cols']
        text_effect_size = self.main.settings_global['measures_effect_size']['collocation'][text_measure_effect_size]['col']

        col_collocate = self.dialog.table.find_col(self.tr('Collocate'))

        if self.dialog.settings['file_to_filter'] == self.tr('Total'):
            if self.dialog.settings['freq_position'] == self.tr('Total'):
                col_freq = self.dialog.table.find_col(
                    self.tr('Total\nFrequency')
                )
            else:
                col_freq = self.dialog.table.find_col(
                    self.tr(f'Total\n{self.dialog.settings["freq_position"]}')
                )

            col_test_stat = self.dialog.table.find_col(
                self.tr(f'Total\n{text_test_stat}')
            )
            col_p_value = self.dialog.table.find_col(
                self.tr(f'Total\n{text_p_value}')
            )
            col_bayes_factor = self.dialog.table.find_col(
                self.tr(f'Total\n{text_bayes_factor}')
            )
            col_effect_size = self.dialog.table.find_col(
                self.tr(f'Total\n{text_effect_size}')
            )
        else:
            if self.dialog.settings['freq_position'] == self.tr('Total'):
                col_freq = self.dialog.table.find_col(
                    self.tr(f"[{self.dialog.settings['file_to_filter']}]\nFrequency")
                )
            else:
                col_freq = self.dialog.table.find_col(
                    self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{self.dialog.settings['freq_position']}")
                )

            col_test_stat = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_test_stat}")
            )
            col_p_value = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_p_value}")
            )
            col_bayes_factor = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_bayes_factor}")
            )
            col_effect_size = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_effect_size}")
            )

        col_num_files_found = self.dialog.table.find_col(self.tr('Number of\nFiles Found'))

        len_collocate_min = (
            float('-inf')
            if self.dialog.settings['len_collocate_min_no_limit']
            else self.dialog.settings['len_collocate_min']
        )
        len_collocate_max = (
            float('inf')
            if self.dialog.settings['len_collocate_max_no_limit']
            else self.dialog.settings['len_collocate_max']
        )

        freq_min = (
            float('-inf')
            if self.dialog.settings['freq_min_no_limit']
            else self.dialog.settings['freq_min']
        )
        freq_max = (
            float('inf')
            if self.dialog.settings['freq_max_no_limit']
            else self.dialog.settings['freq_max']
        )

        test_stat_min = (
            float('-inf')
            if self.dialog.settings['test_stat_min_no_limit']
            else self.dialog.settings['test_stat_min']
        )
        test_stat_max = (
            float('inf')
            if self.dialog.settings['test_stat_max_no_limit']
            else self.dialog.settings['test_stat_max']
        )

        p_value_min = (
            float('-inf')
            if self.dialog.settings['p_value_min_no_limit']
            else self.dialog.settings['p_value_min']
        )
        p_value_max = (
            float('inf')
            if self.dialog.settings['p_value_max_no_limit']
            else self.dialog.settings['p_value_max']
        )

        bayes_factor_min = (
            float('-inf')
            if self.dialog.settings['bayes_factor_min_no_limit']
            else self.dialog.settings['bayes_factor_min']
        )
        bayes_factor_max = (
            float('inf')
            if self.dialog.settings['bayes_factor_max_no_limit']
            else self.dialog.settings['bayes_factor_max']
        )

        effect_size_min = (
            float('-inf')
            if self.dialog.settings['effect_size_min_no_limit']
            else self.dialog.settings['effect_size_min']
        )
        effect_size_max = (
            float('inf')
            if self.dialog.settings['effect_size_max_no_limit']
            else self.dialog.settings['effect_size_max']
        )

        num_files_found_min = (
            float('-inf')
            if self.dialog.settings['num_files_found_min_no_limit']
            else self.dialog.settings['num_files_found_min']
        )
        num_files_found_max = (
            float('inf')
            if self.dialog.settings['num_files_found_max_no_limit']
            else self.dialog.settings['num_files_found_max']
        )

        self.dialog.table.row_filters = []

        for i in range(self.dialog.table.rowCount()):
            if text_test_stat:
                filter_test_stat = test_stat_min <= self.dialog.table.item(i, col_test_stat).val <= test_stat_max
            else:
                filter_test_stat = True

            if text_bayes_factor:
                filter_bayes_factor = bayes_factor_min <= self.dialog.table.item(i, col_bayes_factor).val <= bayes_factor_max
            else:
                filter_bayes_factor = True

            if (
                len_collocate_min   <= len(self.dialog.table.item(i, col_collocate).text())  <= len_collocate_max and
                freq_min            <= self.dialog.table.item(i, col_freq).val               <= freq_max and
                filter_test_stat and
                p_value_min         <= self.dialog.table.item(i, col_p_value).val            <= p_value_max and
                filter_bayes_factor and
                effect_size_min     <= self.dialog.table.item(i, col_effect_size).val        <= effect_size_max and
                num_files_found_min <= self.dialog.table.item(i, col_num_files_found).val    <= num_files_found_max
            ):
                self.dialog.table.row_filters.append(True)
            else:
                self.dialog.table.row_filters.append(False)

        self.progress_updated.emit(self.tr('Updating table ...'))

        time.sleep(0.1)

        self.worker_done.emit()

class Wl_Worker_Results_Filter_Keyword(wl_threading.Wl_Worker):
    def run(self):
        text_test_significance = self.dialog.table.settings['keyword']['generation_settings']['test_significance']
        text_measure_effect_size = self.dialog.table.settings['keyword']['generation_settings']['measure_effect_size']

        (
            text_test_stat,
            text_p_value,
            text_bayes_factor
        ) = self.main.settings_global['tests_significance']['keyword'][text_test_significance]['cols']
        text_effect_size = self.main.settings_global['measures_effect_size']['keyword'][text_measure_effect_size]['col']

        col_keyword = self.dialog.table.find_col(self.tr('Keyword'))

        if self.dialog.settings['file_to_filter'] == self.tr('Total'):
            col_freq = self.dialog.table.find_col(
                self.tr('Total\nFrequency')
            )
            col_test_stat = self.dialog.table.find_col(
                self.tr(f'Total\n{text_test_stat}')
            )
            col_p_value = self.dialog.table.find_col(
                self.tr(f'Total\n{text_p_value}')
            )
            col_bayes_factor = self.dialog.table.find_col(
                self.tr(f'Total\n{text_bayes_factor}')
            )
            col_effect_size = self.dialog.table.find_col(
                self.tr(f'Total\n{text_effect_size}')
            )
        else:
            col_freq = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\nFrequency")
            )
            col_test_stat = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_test_stat}")
            )
            col_p_value = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_p_value}")
            )
            col_bayes_factor = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_bayes_factor}")
            )
            col_effect_size = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_effect_size}")
            )

        col_num_files_found = self.dialog.table.find_col(self.tr('Number of\nFiles Found'))

        len_keyword_min = (
            float('-inf')
            if self.dialog.settings['len_keyword_min_no_limit']
            else self.dialog.settings['len_keyword_min']
        )
        len_keyword_max = (
            float('inf')
            if self.dialog.settings['len_keyword_max_no_limit']
            else self.dialog.settings['len_keyword_max']
        )

        freq_min = (
            float('-inf')
            if self.dialog.settings['freq_min_no_limit']
            else self.dialog.settings['freq_min']
        )
        freq_max = (
            float('inf')
            if self.dialog.settings['freq_max_no_limit']
            else self.dialog.settings['freq_max']
        )

        test_stat_min = (
            float('-inf')
            if self.dialog.settings['test_stat_min_no_limit']
            else self.dialog.settings['test_stat_min']
        )
        test_stat_max = (
            float('inf')
            if self.dialog.settings['test_stat_max_no_limit']
            else self.dialog.settings['test_stat_max']
        )

        p_value_min = (
            float('-inf')
            if self.dialog.settings['p_value_min_no_limit']
            else self.dialog.settings['p_value_min']
        )
        p_value_max = (
            float('inf')
            if self.dialog.settings['p_value_max_no_limit']
            else self.dialog.settings['p_value_max']
        )

        bayes_factor_min = (
            float('-inf')
            if self.dialog.settings['bayes_factor_min_no_limit']
            else self.dialog.settings['bayes_factor_min']
        )
        bayes_factor_max = (
            float('inf')
            if self.dialog.settings['bayes_factor_max_no_limit']
            else self.dialog.settings['bayes_factor_max']
        )

        effect_size_min = (
            float('-inf')
            if self.dialog.settings['effect_size_min_no_limit']
            else self.dialog.settings['effect_size_min']
        )
        effect_size_max = (
            float('inf')
            if self.dialog.settings['effect_size_max_no_limit']
            else self.dialog.settings['effect_size_max']
        )

        num_files_found_min = (
            float('-inf')
            if self.dialog.settings['num_files_found_min_no_limit']
            else self.dialog.settings['num_files_found_min']
        )
        num_files_found_max = (
            float('inf')
            if self.dialog.settings['num_files_found_max_no_limit']
            else self.dialog.settings['nur_files_found_max']
        )

        self.dialog.table.row_filters = []

        for i in range(self.dialog.table.rowCount()):
            if text_test_stat:
                filter_test_stat = test_stat_min <= self.dialog.table.item(i, col_test_stat).val <= test_stat_max
            else:
                filter_test_stat = True

            if text_bayes_factor:
                filter_bayes_factor = bayes_factor_min <= self.dialog.table.item(i, col_bayes_factor).val <= bayes_factor_max
            else:
                filter_bayes_factor = True

            if (
                len_keyword_min     <= len(self.dialog.table.item(i, col_keyword).text())  <= len_keyword_max and
                freq_min            <= self.dialog.table.item(i, col_freq).val             <= freq_max and
                filter_test_stat and
                p_value_min         <= self.dialog.table.item(i, col_p_value).val          <= p_value_max and
                filter_bayes_factor and
                effect_size_min     <= self.dialog.table.item(i, col_effect_size).val      <= effect_size_max and
                num_files_found_min <= self.dialog.table.item(i, col_num_files_found).val  <= num_files_found_max
            ):
                self.dialog.table.row_filters.append(True)
            else:
                self.dialog.table.row_filters.append(False)

        self.progress_updated.emit(self.tr('Updating table ...'))

        time.sleep(0.1)

        self.worker_done.emit()

class Wl_Dialog_Results_Filter(wl_dialogs.Wl_Dialog):
    def __init__(self, main, tab, table):
        super().__init__(main, main.tr('Filter Results'))

        self.tab = tab
        self.table = table
        self.settings = self.main.settings_custom[self.tab]['filter_results']

        self.label_file_to_filter = QLabel(self.tr('File to Filter:'), self)
        self.combo_box_file_to_filter = wl_boxes.Wl_Combo_Box_File_To_Filter(self, self.table)
        self.button_filter = QPushButton(self.tr('Filter'), self)

        self.button_restore_default_settings = wl_buttons.Wl_Button_Restore_Default_Settings(self)
        self.button_close = QPushButton(self.tr('Close'), self)

        self.combo_box_file_to_filter.currentTextChanged.connect(self.file_to_filter_changed)
        self.button_filter.clicked.connect(lambda: self.filter_results())
        self.button_close.clicked.connect(self.reject)

        self.main.wl_work_area.currentChanged.connect(self.reject)

        layout_file_to_filter = wl_layouts.Wl_Layout()
        layout_file_to_filter.addWidget(self.label_file_to_filter, 0, 0)
        layout_file_to_filter.addWidget(self.combo_box_file_to_filter, 0, 1)
        layout_file_to_filter.addWidget(self.button_filter, 0, 2)

        layout_file_to_filter.setColumnStretch(1, 1)

        self.layout_filters = wl_layouts.Wl_Layout()

        layout_buttons = wl_layouts.Wl_Layout()
        layout_buttons.addWidget(self.button_restore_default_settings, 0, 0)
        layout_buttons.addWidget(self.button_close, 0, 2)

        layout_buttons.setColumnStretch(1, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addLayout(layout_file_to_filter, 0, 0)

        self.layout().addWidget(wl_layouts.Wl_Separator(self), 1, 0)
        self.layout().addLayout(self.layout_filters, 2, 0)

        self.layout().addWidget(wl_layouts.Wl_Separator(self), 3, 0)
        self.layout().addLayout(layout_buttons, 4, 0)

        self.set_fixed_size()

    def load_settings(self, defaults = False):
        if defaults:
            settings = self.main.settings_default[self.tab]['filter_results']
        else:
            settings = self.settings

        self.combo_box_file_to_filter.setCurrentText(settings['file_to_filter'])

    def file_to_filter_changed(self):
        self.settings['file_to_filter'] = self.combo_box_file_to_filter.currentText()

    def filter_results(self):
        pass

class Wl_Dialog_Results_Filter_Wordlist(Wl_Dialog_Results_Filter):
    def __init__(self, main, tab, table):
        super().__init__(main, tab, table)

        if self.tab == 'wordlist':
            self.label_len_token = QLabel(self.tr('Token Length:'), self)
            (
                self.label_len_token_min,
                self.spin_box_len_token_min,
                self.checkbox_len_token_min_no_limit,
                self.label_len_token_max,
                self.spin_box_len_token_max,
                self.checkbox_len_token_max_no_limit
            ) = wl_widgets.wl_widgets_filter(
                self,
                filter_min = 1,
                filter_max = 100
            )
        elif self.tab == 'ngram':
            self.label_len_ngram = QLabel(self.tr('N-gram Length:'), self)
            (
                self.label_len_ngram_min,
                self.spin_box_len_ngram_min,
                self.checkbox_len_ngram_min_no_limit,
                self.label_len_ngram_max,
                self.spin_box_len_ngram_max,
                self.checkbox_len_ngram_max_no_limit
            ) = wl_widgets.wl_widgets_filter(
                self,
                filter_min = 1,
                filter_max = 100
            )

        self.label_freq = QLabel(self.tr('Frequency:'), self)
        (
            self.label_freq_min,
            self.spin_box_freq_min,
            self.checkbox_freq_min_no_limit,
            self.label_freq_max,
            self.spin_box_freq_max,
            self.checkbox_freq_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 0,
            filter_max = 1000000
        )

        self.label_dispersion = QLabel(self.tr('Dispersion:'), self)
        (
            self.label_dispersion_min,
            self.spin_box_dispersion_min,
            self.checkbox_dispersion_min_no_limit,
            self.label_dispersion_max,
            self.spin_box_dispersion_max,
            self.checkbox_dispersion_max_no_limit
        ) = wl_widgets.wl_widgets_filter_measures(
            self,
            filter_min = 0,
            filter_max = 1
        )

        self.label_adjusted_freq = QLabel(self.tr('Adjusted Frequency:'), self)
        (
            self.label_adjusted_freq_min,
            self.spin_box_adjusted_freq_min,
            self.checkbox_adjusted_freq_min_no_limit,
            self.label_adjusted_freq_max,
            self.spin_box_adjusted_freq_max,
            self.checkbox_adjusted_freq_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 0,
            filter_max = 1000000
        )

        self.label_num_files_found = QLabel(self.tr('Number of Files Found:'), self)
        (
            self.label_num_files_found_min,
            self.spin_box_num_files_found_min,
            self.checkbox_num_files_found_min_no_limit,
            self.label_num_files_found_max,
            self.spin_box_num_files_found_max,
            self.checkbox_num_files_found_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 1,
            filter_max = 100000
        )

        if self.tab == 'wordlist':
            self.spin_box_len_token_min.valueChanged.connect(self.filters_changed)
            self.checkbox_len_token_min_no_limit.stateChanged.connect(self.filters_changed)
            self.spin_box_len_token_max.valueChanged.connect(self.filters_changed)
            self.checkbox_len_token_max_no_limit.stateChanged.connect(self.filters_changed)
        elif self.tab == 'ngram':
            self.spin_box_len_ngram_min.valueChanged.connect(self.filters_changed)
            self.checkbox_len_ngram_min_no_limit.stateChanged.connect(self.filters_changed)
            self.spin_box_len_ngram_max.valueChanged.connect(self.filters_changed)
            self.checkbox_len_ngram_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_dispersion_min.valueChanged.connect(self.filters_changed)
        self.checkbox_dispersion_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_dispersion_max.valueChanged.connect(self.filters_changed)
        self.checkbox_dispersion_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_adjusted_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_adjusted_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_adjusted_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_adjusted_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_num_files_found_min.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_num_files_found_max.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_max_no_limit.stateChanged.connect(self.filters_changed)

        self.table.itemChanged.connect(self.table_item_changed)

        if self.tab == 'wordlist':
            self.layout_filters.addWidget(self.label_len_token, 0, 0, 1, 3)
            self.layout_filters.addWidget(self.label_len_token_min, 1, 0)
            self.layout_filters.addWidget(self.spin_box_len_token_min, 1, 1)
            self.layout_filters.addWidget(self.checkbox_len_token_min_no_limit, 1, 2)
            self.layout_filters.addWidget(self.label_len_token_max, 2, 0)
            self.layout_filters.addWidget(self.spin_box_len_token_max, 2, 1)
            self.layout_filters.addWidget(self.checkbox_len_token_max_no_limit, 2, 2)
        elif self.tab == 'ngram':
            self.layout_filters.addWidget(self.label_len_ngram, 0, 0, 1, 3)
            self.layout_filters.addWidget(self.label_len_ngram_min, 1, 0)
            self.layout_filters.addWidget(self.spin_box_len_ngram_min, 1, 1)
            self.layout_filters.addWidget(self.checkbox_len_ngram_min_no_limit, 1, 2)
            self.layout_filters.addWidget(self.label_len_ngram_max, 2, 0)
            self.layout_filters.addWidget(self.spin_box_len_ngram_max, 2, 1)
            self.layout_filters.addWidget(self.checkbox_len_ngram_max_no_limit, 2, 2)

        self.layout_filters.addWidget(self.label_freq, 0, 4, 1, 3)
        self.layout_filters.addWidget(self.label_freq_min, 1, 4)
        self.layout_filters.addWidget(self.spin_box_freq_min, 1, 5)
        self.layout_filters.addWidget(self.checkbox_freq_min_no_limit, 1, 6)
        self.layout_filters.addWidget(self.label_freq_max, 2, 4)
        self.layout_filters.addWidget(self.spin_box_freq_max, 2, 5)
        self.layout_filters.addWidget(self.checkbox_freq_max_no_limit, 2, 6)

        self.layout_filters.addWidget(self.label_dispersion, 3, 0, 1, 3)
        self.layout_filters.addWidget(self.label_dispersion_min, 4, 0)
        self.layout_filters.addWidget(self.spin_box_dispersion_min, 4, 1)
        self.layout_filters.addWidget(self.checkbox_dispersion_min_no_limit, 4, 2)
        self.layout_filters.addWidget(self.label_dispersion_max, 5, 0)
        self.layout_filters.addWidget(self.spin_box_dispersion_max, 5, 1)
        self.layout_filters.addWidget(self.checkbox_dispersion_max_no_limit, 5, 2)

        self.layout_filters.addWidget(self.label_adjusted_freq, 3, 4, 1, 3)
        self.layout_filters.addWidget(self.label_adjusted_freq_min, 4, 4)
        self.layout_filters.addWidget(self.spin_box_adjusted_freq_min, 4, 5)
        self.layout_filters.addWidget(self.checkbox_adjusted_freq_min_no_limit, 4, 6)
        self.layout_filters.addWidget(self.label_adjusted_freq_max, 5, 4)
        self.layout_filters.addWidget(self.spin_box_adjusted_freq_max, 5, 5)
        self.layout_filters.addWidget(self.checkbox_adjusted_freq_max_no_limit, 5, 6)

        self.layout_filters.addWidget(self.label_num_files_found, 6, 0, 1, 3)
        self.layout_filters.addWidget(self.label_num_files_found_min, 7, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_min, 7, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_min_no_limit, 7, 2)
        self.layout_filters.addWidget(self.label_num_files_found_max, 8, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_max, 8, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_max_no_limit, 8, 2)

        self.layout_filters.addWidget(wl_layouts.Wl_Separator(self, orientation = 'Vertical'), 0, 3, 9, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        if self.tab == 'wordlist':
            self.spin_box_len_token_min.setValue(settings['len_token_min'])
            self.checkbox_len_token_min_no_limit.setChecked(settings['len_token_min_no_limit'])
            self.spin_box_len_token_max.setValue(settings['len_token_max'])
            self.checkbox_len_token_max_no_limit.setChecked(settings['len_token_max_no_limit'])
        elif self.tab == 'ngram':
            self.spin_box_len_ngram_min.setValue(settings['len_ngram_min'])
            self.checkbox_len_ngram_min_no_limit.setChecked(settings['len_ngram_min_no_limit'])
            self.spin_box_len_ngram_max.setValue(settings['len_ngram_max'])
            self.checkbox_len_ngram_max_no_limit.setChecked(settings['len_ngram_max_no_limit'])

        self.spin_box_freq_min.setValue(settings['freq_min'])
        self.checkbox_freq_min_no_limit.setChecked(settings['freq_min_no_limit'])
        self.spin_box_freq_max.setValue(settings['freq_max'])
        self.checkbox_freq_max_no_limit.setChecked(settings['freq_max_no_limit'])

        self.spin_box_dispersion_min.setValue(settings['dispersion_min'])
        self.checkbox_dispersion_min_no_limit.setChecked(settings['dispersion_min_no_limit'])
        self.spin_box_dispersion_max.setValue(settings['dispersion_max'])
        self.checkbox_dispersion_max_no_limit.setChecked(settings['dispersion_max_no_limit'])

        self.spin_box_adjusted_freq_min.setValue(settings['adjusted_freq_min'])
        self.checkbox_adjusted_freq_min_no_limit.setChecked(settings['adjusted_freq_min_no_limit'])
        self.spin_box_adjusted_freq_max.setValue(settings['adjusted_freq_max'])
        self.checkbox_adjusted_freq_max_no_limit.setChecked(settings['adjusted_freq_max_no_limit'])

        self.spin_box_num_files_found_min.setValue(settings['num_files_found_min'])
        self.checkbox_num_files_found_min_no_limit.setChecked(settings['num_files_found_min_no_limit'])
        self.spin_box_num_files_found_max.setValue(settings['num_files_found_max'])
        self.checkbox_num_files_found_max_no_limit.setChecked(settings['num_files_found_max_no_limit'])

    def filters_changed(self):
        if self.tab == 'wordlist':
            self.settings['len_token_min'] = self.spin_box_len_token_min.value()
            self.settings['len_token_min_no_limit'] = self.checkbox_len_token_min_no_limit.isChecked()
            self.settings['len_token_max'] = self.spin_box_len_token_max.value()
            self.settings['len_token_max_no_limit'] = self.checkbox_len_token_max_no_limit.isChecked()
        elif self.tab == 'ngram':
            self.settings['len_ngram_min'] = self.spin_box_len_ngram_min.value()
            self.settings['len_ngram_min_no_limit'] = self.checkbox_len_ngram_min_no_limit.isChecked()
            self.settings['len_ngram_max'] = self.spin_box_len_ngram_max.value()
            self.settings['len_ngram_max_no_limit'] = self.checkbox_len_ngram_max_no_limit.isChecked()

        self.settings['freq_min'] = self.spin_box_freq_min.value()
        self.settings['freq_min_no_limit'] = self.checkbox_freq_min_no_limit.isChecked()
        self.settings['freq_max'] = self.spin_box_freq_max.value()
        self.settings['freq_max_no_limit'] = self.checkbox_freq_max_no_limit.isChecked()

        self.settings['dispersion_min'] = self.spin_box_dispersion_min.value()
        self.settings['dispersion_min_no_limit'] = self.checkbox_dispersion_min_no_limit.isChecked()
        self.settings['dispersion_max'] = self.spin_box_dispersion_max.value()
        self.settings['dispersion_max_no_limit'] = self.checkbox_dispersion_max_no_limit.isChecked()

        self.settings['adjusted_freq_min'] = self.spin_box_adjusted_freq_min.value()
        self.settings['adjusted_freq_min_no_limit'] = self.checkbox_adjusted_freq_min_no_limit.isChecked()
        self.settings['adjusted_freq_max'] = self.spin_box_adjusted_freq_max.value()
        self.settings['adjusted_freq_max_no_limit'] = self.checkbox_adjusted_freq_max_no_limit.isChecked()

        self.settings['num_files_found_min'] = self.spin_box_num_files_found_min.value()
        self.settings['num_files_found_min_no_limit'] = self.checkbox_num_files_found_min_no_limit.isChecked()
        self.settings['num_files_found_max'] = self.spin_box_num_files_found_max.value()
        self.settings['num_files_found_max_no_limit'] = self.checkbox_num_files_found_max_no_limit.isChecked()

    def table_item_changed(self):
        settings = self.table.settings[self.tab]

        text_measure_dispersion = settings['generation_settings']['measure_dispersion']
        text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

        text_dispersion = self.main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
        text_adjusted_freq =  self.main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

        self.label_dispersion.setText(f'{text_dispersion}:')
        self.label_adjusted_freq.setText(f'{text_adjusted_freq}:')

    @wl_misc.log_timing
    def filter_results(self):
        def update_gui():
            self.table.filter_table()

            wl_msgs.wl_msg_results_filter_success(self.main)

        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = self.tr('Filtering results...'))

        worker_search_results = Wl_Worker_Results_Filter_Wordlist(
            self.main,
            dialog_progress = dialog_progress,
            update_gui = update_gui,
            dialog = self
        )

        thread_search_results = wl_threading.Wl_Thread(worker_search_results)
        thread_search_results.start_worker()

class Wl_Dialog_Results_Filter_Collocation(Wl_Dialog_Results_Filter):
    def __init__(self, main, tab, table):
        super().__init__(main, tab, table)

        self.label_len_collocate = QLabel(self.tr('Collocate Length:'), self)
        (
            self.label_len_collocate_min,
            self.spin_box_len_collocate_min,
            self.checkbox_len_collocate_min_no_limit,
            self.label_len_collocate_max,
            self.spin_box_len_collocate_max,
            self.checkbox_len_collocate_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 1,
            filter_max = 100
        )

        self.label_freq = QLabel(self.tr('Frequency:'), self)
        self.combo_box_freq_position = wl_boxes.Wl_Combo_Box(self)
        (
            self.label_freq_min,
            self.spin_box_freq_min,
            self.checkbox_freq_min_no_limit,
            self.label_freq_max,
            self.spin_box_freq_max,
            self.checkbox_freq_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 0,
            filter_max = 1000000
        )

        self.label_test_stat = QLabel(self.tr('Test Statistic:'), self)
        (
            self.label_test_stat_min,
            self.spin_box_test_stat_min,
            self.checkbox_test_stat_min_no_limit,
            self.label_test_stat_max,
            self.spin_box_test_stat_max,
            self.checkbox_test_stat_max_no_limit
        ) = wl_widgets.wl_widgets_filter_measures(self)

        self.label_p_value = QLabel(self.tr('p-value:'), self)
        (
            self.label_p_value_min,
            self.spin_box_p_value_min,
            self.checkbox_p_value_min_no_limit,
            self.label_p_value_max,
            self.spin_box_p_value_max,
            self.checkbox_p_value_max_no_limit
        ) = wl_widgets.wl_widgets_filter_p_value(self)

        self.label_bayes_factor = QLabel(self.tr('Bayes Factor:'), self)
        (
            self.label_bayes_factor_min,
            self.spin_box_bayes_factor_min,
            self.checkbox_bayes_factor_min_no_limit,
            self.label_bayes_factor_max,
            self.spin_box_bayes_factor_max,
            self.checkbox_bayes_factor_max_no_limit
        ) = wl_widgets.wl_widgets_filter_measures(self)

        self.label_effect_size = QLabel(self.tr('Effect Size:'), self)
        (
            self.label_effect_size_min,
            self.spin_box_effect_size_min,
            self.checkbox_effect_size_min_no_limit,
            self.label_effect_size_max,
            self.spin_box_effect_size_max,
            self.checkbox_effect_size_max_no_limit
        ) = wl_widgets.wl_widgets_filter_measures(self)

        self.label_num_files_found = QLabel(self.tr('Number of Files Found:'), self)
        (
            self.label_num_files_found_min,
            self.spin_box_num_files_found_min,
            self.checkbox_num_files_found_min_no_limit,
            self.label_num_files_found_max,
            self.spin_box_num_files_found_max,
            self.checkbox_num_files_found_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 1,
            filter_max = 100000
        )

        self.spin_box_len_collocate_min.valueChanged.connect(self.filters_changed)
        self.checkbox_len_collocate_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_len_collocate_max.valueChanged.connect(self.filters_changed)
        self.checkbox_len_collocate_max_no_limit.stateChanged.connect(self.filters_changed)

        self.combo_box_freq_position.currentTextChanged.connect(self.filters_changed)
        self.spin_box_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_test_stat_min.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_test_stat_max.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_p_value_min.valueChanged.connect(self.filters_changed)
        self.checkbox_p_value_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_p_value_max.valueChanged.connect(self.filters_changed)
        self.checkbox_p_value_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_bayes_factor_min.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_bayes_factor_max.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_effect_size_min.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_effect_size_max.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_num_files_found_min.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_num_files_found_max.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_max_no_limit.stateChanged.connect(self.filters_changed)

        self.table.itemChanged.connect(self.table_item_changed)

        layout_freq_position = wl_layouts.Wl_Layout()
        layout_freq_position.addWidget(self.label_freq, 0, 0)
        layout_freq_position.addWidget(self.combo_box_freq_position, 0, 1, Qt.AlignRight)

        self.layout_filters.addWidget(self.label_len_collocate, 0, 0, 1, 3)
        self.layout_filters.addWidget(self.label_len_collocate_min, 1, 0)
        self.layout_filters.addWidget(self.spin_box_len_collocate_min, 1, 1)
        self.layout_filters.addWidget(self.checkbox_len_collocate_min_no_limit, 1, 2)
        self.layout_filters.addWidget(self.label_len_collocate_max, 2, 0)
        self.layout_filters.addWidget(self.spin_box_len_collocate_max, 2, 1)
        self.layout_filters.addWidget(self.checkbox_len_collocate_max_no_limit, 2, 2)

        self.layout_filters.addLayout(layout_freq_position, 0, 4, 1, 3)
        self.layout_filters.addWidget(self.label_freq_min, 1, 4)
        self.layout_filters.addWidget(self.spin_box_freq_min, 1, 5)
        self.layout_filters.addWidget(self.checkbox_freq_min_no_limit, 1, 6)
        self.layout_filters.addWidget(self.label_freq_max, 2, 4)
        self.layout_filters.addWidget(self.spin_box_freq_max, 2, 5)
        self.layout_filters.addWidget(self.checkbox_freq_max_no_limit, 2, 6)

        self.layout_filters.addWidget(self.label_test_stat, 3, 0, 1, 3)
        self.layout_filters.addWidget(self.label_test_stat_min, 4, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_min, 4, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_min_no_limit, 4, 2)
        self.layout_filters.addWidget(self.label_test_stat_max, 5, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_max, 5, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_max_no_limit, 5, 2)

        self.layout_filters.addWidget(self.label_p_value, 3, 4, 1, 3)
        self.layout_filters.addWidget(self.label_p_value_min, 4, 4)
        self.layout_filters.addWidget(self.spin_box_p_value_min, 4, 5)
        self.layout_filters.addWidget(self.checkbox_p_value_min_no_limit, 4, 6)
        self.layout_filters.addWidget(self.label_p_value_max, 5, 4)
        self.layout_filters.addWidget(self.spin_box_p_value_max, 5, 5)
        self.layout_filters.addWidget(self.checkbox_p_value_max_no_limit, 5, 6)

        self.layout_filters.addWidget(self.label_bayes_factor, 6, 0, 1, 3)
        self.layout_filters.addWidget(self.label_bayes_factor_min, 7, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_min, 7, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_min_no_limit, 7, 2)
        self.layout_filters.addWidget(self.label_bayes_factor_max, 8, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_max, 8, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_max_no_limit, 8, 2)

        self.layout_filters.addWidget(self.label_effect_size, 6, 4, 1, 3)
        self.layout_filters.addWidget(self.label_effect_size_min, 7, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_min, 7, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_min_no_limit, 7, 6)
        self.layout_filters.addWidget(self.label_effect_size_max, 8, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_max, 8, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_max_no_limit, 8, 6)

        self.layout_filters.addWidget(self.label_num_files_found, 9, 0, 1, 3)
        self.layout_filters.addWidget(self.label_num_files_found_min, 10, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_min, 10, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_min_no_limit, 10, 2)
        self.layout_filters.addWidget(self.label_num_files_found_max, 11, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_max, 11, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_max_no_limit, 11, 2)

        self.layout_filters.addWidget(wl_layouts.Wl_Separator(self, orientation = 'Vertical'), 0, 3, 12, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        self.spin_box_len_collocate_min.setValue(settings['len_collocate_min'])
        self.checkbox_len_collocate_min_no_limit.setChecked(settings['len_collocate_min_no_limit'])
        self.spin_box_len_collocate_max.setValue(settings['len_collocate_max'])
        self.checkbox_len_collocate_max_no_limit.setChecked(settings['len_collocate_max_no_limit'])

        self.combo_box_freq_position.setCurrentText(settings['freq_position'])
        self.spin_box_freq_min.setValue(settings['freq_min'])
        self.checkbox_freq_min_no_limit.setChecked(settings['freq_min_no_limit'])
        self.spin_box_freq_max.setValue(settings['freq_max'])
        self.checkbox_freq_max_no_limit.setChecked(settings['freq_max_no_limit'])

        self.spin_box_test_stat_min.setValue(settings['test_stat_min'])
        self.checkbox_test_stat_min_no_limit.setChecked(settings['test_stat_min_no_limit'])
        self.spin_box_test_stat_max.setValue(settings['test_stat_max'])
        self.checkbox_test_stat_max_no_limit.setChecked(settings['test_stat_max_no_limit'])

        self.spin_box_p_value_min.setValue(settings['p_value_min'])
        self.checkbox_p_value_min_no_limit.setChecked(settings['p_value_min_no_limit'])
        self.spin_box_p_value_max.setValue(settings['p_value_max'])
        self.checkbox_p_value_max_no_limit.setChecked(settings['p_value_max_no_limit'])

        self.spin_box_bayes_factor_min.setValue(settings['bayes_factor_min'])
        self.checkbox_bayes_factor_min_no_limit.setChecked(settings['bayes_factor_min_no_limit'])
        self.spin_box_bayes_factor_max.setValue(settings['bayes_factor_max'])
        self.checkbox_bayes_factor_max_no_limit.setChecked(settings['bayes_factor_max_no_limit'])

        self.spin_box_effect_size_min.setValue(settings['effect_size_min'])
        self.checkbox_effect_size_min_no_limit.setChecked(settings['effect_size_min_no_limit'])
        self.spin_box_effect_size_max.setValue(settings['effect_size_max'])
        self.checkbox_effect_size_max_no_limit.setChecked(settings['effect_size_max_no_limit'])

        self.spin_box_num_files_found_min.setValue(settings['num_files_found_min'])
        self.checkbox_num_files_found_min_no_limit.setChecked(settings['num_files_found_min_no_limit'])
        self.spin_box_num_files_found_max.setValue(settings['num_files_found_max'])
        self.checkbox_num_files_found_max_no_limit.setChecked(settings['num_files_found_max_no_limit'])

    def filters_changed(self):
        self.settings['len_collocate_min'] = self.spin_box_len_collocate_min.value()
        self.settings['len_collocate_min_no_limit'] = self.checkbox_len_collocate_min_no_limit.isChecked()
        self.settings['len_collocate_max'] = self.spin_box_len_collocate_max.value()
        self.settings['len_collocate_max_no_limit'] = self.checkbox_len_collocate_max_no_limit.isChecked()

        self.settings['freq_position'] = self.combo_box_freq_position.currentText()
        self.settings['freq_min'] = self.spin_box_freq_min.value()
        self.settings['freq_min_no_limit'] = self.checkbox_freq_min_no_limit.isChecked()
        self.settings['freq_max'] = self.spin_box_freq_max.value()
        self.settings['freq_max_no_limit'] = self.checkbox_freq_max_no_limit.isChecked()

        self.settings['test_stat_min'] = self.spin_box_test_stat_min.value()
        self.settings['test_stat_min_no_limit'] = self.checkbox_test_stat_min_no_limit.isChecked()
        self.settings['test_stat_max'] = self.spin_box_test_stat_max.value()
        self.settings['test_stat_max_no_limit'] = self.checkbox_test_stat_max_no_limit.isChecked()

        self.settings['p_value_min'] = self.spin_box_p_value_min.value()
        self.settings['p_value_min_no_limit'] = self.checkbox_p_value_min_no_limit.isChecked()
        self.settings['p_value_max'] = self.spin_box_p_value_max.value()
        self.settings['p_value_max_no_limit'] = self.checkbox_p_value_max_no_limit.isChecked()

        self.settings['bayes_factor_min'] = self.spin_box_bayes_factor_min.value()
        self.settings['bayes_factor_min_no_limit'] = self.checkbox_bayes_factor_min_no_limit.isChecked()
        self.settings['bayes_factor_max'] = self.spin_box_bayes_factor_max.value()
        self.settings['bayes_factor_max_no_limit'] = self.checkbox_bayes_factor_max_no_limit.isChecked()

        self.settings['effect_size_min'] = self.spin_box_effect_size_min.value()
        self.settings['effect_size_min_no_limit'] = self.checkbox_effect_size_min_no_limit.isChecked()
        self.settings['effect_size_max'] = self.spin_box_effect_size_max.value()
        self.settings['effect_size_max_no_limit'] = self.checkbox_effect_size_max_no_limit.isChecked()

        self.settings['num_files_found_min'] = self.spin_box_num_files_found_min.value()
        self.settings['num_files_found_min_no_limit'] = self.checkbox_num_files_found_min_no_limit.isChecked()
        self.settings['num_files_found_max'] = self.spin_box_num_files_found_max.value()
        self.settings['num_files_found_max_no_limit'] = self.checkbox_num_files_found_max_no_limit.isChecked()

    def table_item_changed(self):
        settings = self.table.settings[self.tab]

        # Frequency
        freq_position_old = settings['filter_results']['freq_position']

        self.combo_box_freq_position.clear()

        for i in range(settings['generation_settings']['window_left'], settings['generation_settings']['window_right'] + 1):
            if i < 0:
                self.combo_box_freq_position.addItem(f'L{-i}')
            elif i > 0:
                self.combo_box_freq_position.addItem(f'R{i}')

        self.combo_box_freq_position.addItem(self.tr('Total'))

        if self.combo_box_freq_position.findText(freq_position_old) > -1:
            self.combo_box_freq_position.setCurrentText(freq_position_old)
        else:
            self.combo_box_freq_position.setCurrentText(self.main.settings_default['collocation']['filter_results']['freq_position'])

        # Filters
        text_test_significance = settings['generation_settings']['test_significance']
        text_measure_effect_size = settings['generation_settings']['measure_effect_size']

        (
            text_test_stat,
            text_p_value,
            text_bayes_factor
        ) = self.main.settings_global['tests_significance']['collocation'][text_test_significance]['cols']
        text_effect_size =  self.main.settings_global['measures_effect_size']['collocation'][text_measure_effect_size]['col']

        if text_test_stat:
            self.label_test_stat.setText(f'{text_test_stat}:')

            if not self.checkbox_test_stat_min_no_limit.isChecked():
                self.spin_box_test_stat_min.setEnabled(True)
            if not self.checkbox_test_stat_max_no_limit.isChecked():
                self.spin_box_test_stat_max.setEnabled(True)

            self.checkbox_test_stat_min_no_limit.setEnabled(True)
            self.checkbox_test_stat_max_no_limit.setEnabled(True)
        else:
            self.label_test_stat.setText(self.tr('Test Statistic:'))

            self.spin_box_test_stat_min.setEnabled(False)
            self.checkbox_test_stat_min_no_limit.setEnabled(False)
            self.spin_box_test_stat_max.setEnabled(False)
            self.checkbox_test_stat_max_no_limit.setEnabled(False)

        if text_bayes_factor:
            if not self.checkbox_bayes_factor_min_no_limit.isChecked():
                self.spin_box_bayes_factor_min.setEnabled(True)
            if not self.checkbox_bayes_factor_max_no_limit.isChecked():
                self.spin_box_bayes_factor_max.setEnabled(True)

            self.checkbox_bayes_factor_min_no_limit.setEnabled(True)
            self.checkbox_bayes_factor_max_no_limit.setEnabled(True)
        else:
            self.spin_box_bayes_factor_min.setEnabled(False)
            self.checkbox_bayes_factor_min_no_limit.setEnabled(False)
            self.spin_box_bayes_factor_max.setEnabled(False)
            self.checkbox_bayes_factor_max_no_limit.setEnabled(False)

        self.label_effect_size.setText(f'{text_effect_size}:')

    @wl_misc.log_timing
    def filter_results(self):
        def update_gui():
            self.table.filter_table()

            wl_msgs.wl_msg_results_filter_success(self.main)

        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = self.tr('Filtering results...'))

        worker_search_results = Wl_Worker_Results_Filter_Collocation(
            self.main,
            dialog_progress = dialog_progress,
            update_gui = update_gui,
            dialog = self
        )

        thread_search_results = wl_threading.Wl_Thread(worker_search_results)
        thread_search_results.start_worker()

class Wl_Dialog_Results_Filter_Keyword(Wl_Dialog_Results_Filter):
    def __init__(self, main, tab, table):
        super().__init__(main, tab, table)

        self.label_len_keyword = QLabel(self.tr('Keyword Length:'), self)
        (
            self.label_len_keyword_min,
            self.spin_box_len_keyword_min,
            self.checkbox_len_keyword_min_no_limit,
            self.label_len_keyword_max,
            self.spin_box_len_keyword_max,
            self.checkbox_len_keyword_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 1,
            filter_max = 100
        )

        self.label_freq = QLabel(self.tr('Frequency:'), self)
        (
            self.label_freq_min,
            self.spin_box_freq_min,
            self.checkbox_freq_min_no_limit,
            self.label_freq_max,
            self.spin_box_freq_max,
            self.checkbox_freq_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 0,
            filter_max = 1000000
        )

        self.label_test_stat = QLabel(self.tr('Test Statistic:'), self)
        (
            self.label_test_stat_min,
            self.spin_box_test_stat_min,
            self.checkbox_test_stat_min_no_limit,
            self.label_test_stat_max,
            self.spin_box_test_stat_max,
            self.checkbox_test_stat_max_no_limit
        ) = wl_widgets.wl_widgets_filter_measures(self)

        self.label_p_value = QLabel(self.tr('p-value:'), self)
        (
            self.label_p_value_min,
            self.spin_box_p_value_min,
            self.checkbox_p_value_min_no_limit,
            self.label_p_value_max,
            self.spin_box_p_value_max,
            self.checkbox_p_value_max_no_limit
        ) = wl_widgets.wl_widgets_filter_p_value(self)

        self.label_bayes_factor = QLabel(self.tr('Bayes Factor:'), self)
        (
            self.label_bayes_factor_min,
            self.spin_box_bayes_factor_min,
            self.checkbox_bayes_factor_min_no_limit,
            self.label_bayes_factor_max,
            self.spin_box_bayes_factor_max,
            self.checkbox_bayes_factor_max_no_limit
        ) = wl_widgets.wl_widgets_filter_measures(self)

        self.label_effect_size = QLabel(self.tr('Effect Size:'), self)
        (
            self.label_effect_size_min,
            self.spin_box_effect_size_min,
            self.checkbox_effect_size_min_no_limit,
            self.label_effect_size_max,
            self.spin_box_effect_size_max,
            self.checkbox_effect_size_max_no_limit
        ) = wl_widgets.wl_widgets_filter_measures(self)

        self.label_num_files_found = QLabel(self.tr('Number of Files Found:'), self)
        (
            self.label_num_files_found_min,
            self.spin_box_num_files_found_min,
            self.checkbox_num_files_found_min_no_limit,
            self.label_num_files_found_max,
            self.spin_box_num_files_found_max,
            self.checkbox_num_files_found_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 1,
            filter_max = 100000
        )

        self.spin_box_len_keyword_min.valueChanged.connect(self.filters_changed)
        self.checkbox_len_keyword_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_len_keyword_max.valueChanged.connect(self.filters_changed)
        self.checkbox_len_keyword_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_test_stat_min.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_test_stat_max.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_p_value_min.valueChanged.connect(self.filters_changed)
        self.checkbox_p_value_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_p_value_max.valueChanged.connect(self.filters_changed)
        self.checkbox_p_value_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_bayes_factor_min.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_bayes_factor_max.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_effect_size_min.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_effect_size_max.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_num_files_found_min.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_num_files_found_max.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_max_no_limit.stateChanged.connect(self.filters_changed)

        self.table.itemChanged.connect(self.table_item_changed)

        self.layout_filters.addWidget(self.label_len_keyword, 0, 0, 1, 3)
        self.layout_filters.addWidget(self.label_len_keyword_min, 1, 0)
        self.layout_filters.addWidget(self.spin_box_len_keyword_min, 1, 1)
        self.layout_filters.addWidget(self.checkbox_len_keyword_min_no_limit, 1, 2)
        self.layout_filters.addWidget(self.label_len_keyword_max, 2, 0)
        self.layout_filters.addWidget(self.spin_box_len_keyword_max, 2, 1)
        self.layout_filters.addWidget(self.checkbox_len_keyword_max_no_limit, 2, 2)

        self.layout_filters.addWidget(self.label_freq, 0, 4, 1, 3)
        self.layout_filters.addWidget(self.label_freq_min, 1, 4)
        self.layout_filters.addWidget(self.spin_box_freq_min, 1, 5)
        self.layout_filters.addWidget(self.checkbox_freq_min_no_limit, 1, 6)
        self.layout_filters.addWidget(self.label_freq_max, 2, 4)
        self.layout_filters.addWidget(self.spin_box_freq_max, 2, 5)
        self.layout_filters.addWidget(self.checkbox_freq_max_no_limit, 2, 6)

        self.layout_filters.addWidget(self.label_test_stat, 3, 0, 1, 3)
        self.layout_filters.addWidget(self.label_test_stat_min, 4, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_min, 4, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_min_no_limit, 4, 2)
        self.layout_filters.addWidget(self.label_test_stat_max, 5, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_max, 5, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_max_no_limit, 5, 2)

        self.layout_filters.addWidget(self.label_p_value, 3, 4, 1, 3)
        self.layout_filters.addWidget(self.label_p_value_min, 4, 4)
        self.layout_filters.addWidget(self.spin_box_p_value_min, 4, 5)
        self.layout_filters.addWidget(self.checkbox_p_value_min_no_limit, 4, 6)
        self.layout_filters.addWidget(self.label_p_value_max, 5, 4)
        self.layout_filters.addWidget(self.spin_box_p_value_max, 5, 5)
        self.layout_filters.addWidget(self.checkbox_p_value_max_no_limit, 5, 6)

        self.layout_filters.addWidget(self.label_bayes_factor, 6, 0, 1, 3)
        self.layout_filters.addWidget(self.label_bayes_factor_min, 7, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_min, 7, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_min_no_limit, 7, 2)
        self.layout_filters.addWidget(self.label_bayes_factor_max, 8, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_max, 8, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_max_no_limit, 8, 2)

        self.layout_filters.addWidget(self.label_effect_size, 6, 4, 1, 3)
        self.layout_filters.addWidget(self.label_effect_size_min, 7, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_min, 7, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_min_no_limit, 7, 6)
        self.layout_filters.addWidget(self.label_effect_size_max, 8, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_max, 8, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_max_no_limit, 8, 6)

        self.layout_filters.addWidget(self.label_num_files_found, 9, 0, 1, 3)
        self.layout_filters.addWidget(self.label_num_files_found_min, 10, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_min, 10, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_min_no_limit, 10, 2)
        self.layout_filters.addWidget(self.label_num_files_found_max, 11, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_max, 11, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_max_no_limit, 11, 2)

        self.layout_filters.addWidget(wl_layouts.Wl_Separator(self, orientation = 'Vertical'), 0, 3, 12, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        self.spin_box_len_keyword_min.setValue(settings['len_keyword_min'])
        self.checkbox_len_keyword_min_no_limit.setChecked(settings['len_keyword_min_no_limit'])
        self.spin_box_len_keyword_max.setValue(settings['len_keyword_max'])
        self.checkbox_len_keyword_max_no_limit.setChecked(settings['len_keyword_max_no_limit'])

        self.spin_box_freq_min.setValue(settings['freq_min'])
        self.checkbox_freq_min_no_limit.setChecked(settings['freq_min_no_limit'])
        self.spin_box_freq_max.setValue(settings['freq_max'])
        self.checkbox_freq_max_no_limit.setChecked(settings['freq_max_no_limit'])

        self.spin_box_test_stat_min.setValue(settings['test_stat_min'])
        self.checkbox_test_stat_min_no_limit.setChecked(settings['test_stat_min_no_limit'])
        self.spin_box_test_stat_max.setValue(settings['test_stat_max'])
        self.checkbox_test_stat_max_no_limit.setChecked(settings['test_stat_max_no_limit'])

        self.spin_box_p_value_min.setValue(settings['p_value_min'])
        self.checkbox_p_value_min_no_limit.setChecked(settings['p_value_min_no_limit'])
        self.spin_box_p_value_max.setValue(settings['p_value_max'])
        self.checkbox_p_value_max_no_limit.setChecked(settings['p_value_max_no_limit'])

        self.spin_box_bayes_factor_min.setValue(settings['bayes_factor_min'])
        self.checkbox_bayes_factor_min_no_limit.setChecked(settings['bayes_factor_min_no_limit'])
        self.spin_box_bayes_factor_max.setValue(settings['bayes_factor_max'])
        self.checkbox_bayes_factor_max_no_limit.setChecked(settings['bayes_factor_max_no_limit'])

        self.spin_box_effect_size_min.setValue(settings['effect_size_min'])
        self.checkbox_effect_size_min_no_limit.setChecked(settings['effect_size_min_no_limit'])
        self.spin_box_effect_size_max.setValue(settings['effect_size_max'])
        self.checkbox_effect_size_max_no_limit.setChecked(settings['effect_size_max_no_limit'])

        self.spin_box_num_files_found_min.setValue(settings['num_files_found_min'])
        self.checkbox_num_files_found_min_no_limit.setChecked(settings['num_files_found_min_no_limit'])
        self.spin_box_num_files_found_max.setValue(settings['num_files_found_max'])
        self.checkbox_num_files_found_max_no_limit.setChecked(settings['num_files_found_max_no_limit'])

    def filters_changed(self):
        self.settings['len_keyword_min'] = self.spin_box_len_keyword_min.value()
        self.settings['len_keyword_min_no_limit'] = self.checkbox_len_keyword_min_no_limit.isChecked()
        self.settings['len_keyword_max'] = self.spin_box_len_keyword_max.value()
        self.settings['len_keyword_max_no_limit'] = self.checkbox_len_keyword_max_no_limit.isChecked()

        self.settings['freq_min'] = self.spin_box_freq_min.value()
        self.settings['freq_min_no_limit'] = self.checkbox_freq_min_no_limit.isChecked()
        self.settings['freq_max'] = self.spin_box_freq_max.value()
        self.settings['freq_max_no_limit'] = self.checkbox_freq_max_no_limit.isChecked()

        self.settings['test_stat_min'] = self.spin_box_test_stat_min.value()
        self.settings['test_stat_min_no_limit'] = self.checkbox_test_stat_min_no_limit.isChecked()
        self.settings['test_stat_max'] = self.spin_box_test_stat_max.value()
        self.settings['test_stat_max_no_limit'] = self.checkbox_test_stat_max_no_limit.isChecked()

        self.settings['p_value_min'] = self.spin_box_p_value_min.value()
        self.settings['p_value_min_no_limit'] = self.checkbox_p_value_min_no_limit.isChecked()
        self.settings['p_value_max'] = self.spin_box_p_value_max.value()
        self.settings['p_value_max_no_limit'] = self.checkbox_p_value_max_no_limit.isChecked()

        self.settings['bayes_factor_min'] = self.spin_box_bayes_factor_min.value()
        self.settings['bayes_factor_min_no_limit'] = self.checkbox_bayes_factor_min_no_limit.isChecked()
        self.settings['bayes_factor_max'] = self.spin_box_bayes_factor_max.value()
        self.settings['bayes_factor_max_no_limit'] = self.checkbox_bayes_factor_max_no_limit.isChecked()

        self.settings['effect_size_min'] = self.spin_box_effect_size_min.value()
        self.settings['effect_size_min_no_limit'] = self.checkbox_effect_size_min_no_limit.isChecked()
        self.settings['effect_size_max'] = self.spin_box_effect_size_max.value()
        self.settings['effect_size_max_no_limit'] = self.checkbox_effect_size_max_no_limit.isChecked()

        self.settings['num_files_found_min'] = self.spin_box_num_files_found_min.value()
        self.settings['num_files_found_min_no_limit'] = self.checkbox_num_files_found_min_no_limit.isChecked()
        self.settings['num_files_found_max'] = self.spin_box_num_files_found_max.value()
        self.settings['num_files_found_max_no_limit'] = self.checkbox_num_files_found_max_no_limit.isChecked()

    def table_item_changed(self):
        settings = self.table.settings[self.tab]

        ref_files = settings['generation_settings']['ref_files']

        text_test_significance = settings['generation_settings']['test_significance']
        text_measure_effect_size = settings['generation_settings']['measure_effect_size']

        (
            text_test_stat,
            text_p_value,
            text_bayes_factor
        ) = self.main.settings_global['tests_significance']['keyword'][text_test_significance]['cols']
        text_effect_size = self.main.settings_global['measures_effect_size']['keyword'][text_measure_effect_size]['col']

        if text_test_stat:
            self.label_test_stat.setText(f'{text_test_stat}:')

            if not self.checkbox_test_stat_min_no_limit.isChecked():
                self.spin_box_test_stat_min.setEnabled(True)
            if not self.checkbox_test_stat_max_no_limit.isChecked():
                self.spin_box_test_stat_max.setEnabled(True)

            self.checkbox_test_stat_min_no_limit.setEnabled(True)
            self.checkbox_test_stat_max_no_limit.setEnabled(True)
        else:
            self.label_test_stat.setText(self.tr('Test Statistic:'))

            self.spin_box_test_stat_min.setEnabled(False)
            self.checkbox_test_stat_min_no_limit.setEnabled(False)
            self.spin_box_test_stat_max.setEnabled(False)
            self.checkbox_test_stat_max_no_limit.setEnabled(False)

        if text_bayes_factor:
            if not self.checkbox_bayes_factor_min_no_limit.isChecked():
                self.spin_box_bayes_factor_min.setEnabled(True)
            if not self.checkbox_bayes_factor_max_no_limit.isChecked():
                self.spin_box_bayes_factor_max.setEnabled(True)

            self.checkbox_bayes_factor_min_no_limit.setEnabled(True)
            self.checkbox_bayes_factor_max_no_limit.setEnabled(True)
        else:
            self.spin_box_bayes_factor_min.setEnabled(False)
            self.checkbox_bayes_factor_min_no_limit.setEnabled(False)
            self.spin_box_bayes_factor_max.setEnabled(False)
            self.checkbox_bayes_factor_max_no_limit.setEnabled(False)

        self.label_effect_size.setText(f'{text_effect_size}:')
        
        # Remove reference files from the file list
        for ref_file in ref_files:
            self.combo_box_file_to_filter.removeItem(self.combo_box_file_to_filter.findText(ref_file))

    @wl_misc.log_timing
    def filter_results(self):
        def update_gui():
            self.table.filter_table()

            wl_msgs.wl_msg_results_filter_success(self.main)

        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = self.tr('Filtering results...'))

        worker_search_results = Wl_Worker_Results_Filter_Keyword(
            self.main,
            dialog_progress = dialog_progress,
            update_gui = update_gui,
            dialog = self
        )

        thread_search_results = wl_threading.Wl_Thread(worker_search_results)
        thread_search_results.start_worker()

class Wl_Button_Results_Filter(wl_buttons.Wl_Button):
    def __init__(self, parent, tab, table):
        super().__init__(parent.tr('Filter Results'), parent)

        if tab in ['wordlist', 'ngram']:
            dialog_results_filter = Wl_Dialog_Results_Filter_Wordlist(self.main, tab = tab, table = table)
        elif tab in ['collocation', 'colligation']:
            dialog_results_filter = Wl_Dialog_Results_Filter_Collocation(self.main, tab = tab, table = table)
        elif tab == 'keyword':
            dialog_results_filter = Wl_Dialog_Results_Filter_Keyword(self.main, tab = tab, table = table)

        self.setFixedWidth(150)

        self.clicked.connect(dialog_results_filter.show)

class Wl_Table_Data_Filter_Search(Wl_Table_Data):
    def __init__(
        self, main, tab,
        headers, header_orientation = 'horizontal',
        headers_int = None, headers_float = None,
        headers_pct = None, headers_cumulative = None, cols_breakdown = None,
        cols_stretch = None,
        sorting_enabled = False
    ):
        super().__init__(
            main, tab,
            headers, header_orientation,
            headers_int, headers_float,
            headers_pct, headers_cumulative, cols_breakdown,
            cols_stretch,
            sorting_enabled
        )

        self.label_number_results = QLabel()
        self.button_results_filter = Wl_Button_Results_Filter(
            self,
            tab = self.tab,
            table = self
        )
        self.button_results_search = Wl_Button_Results_Search(
            self,
            tab = self.tab,
            table = self
        )

        self.itemChanged.connect(self.results_changed)

        self.results_changed()

    def results_changed(self):
        rows_visible = len([i for i in range(self.rowCount()) if not self.isRowHidden(i)])

        if [i for i in range(self.columnCount()) if self.item(0, i)]:
            self.label_number_results.setText(self.tr(f'Number of Results: {rows_visible}'))

            self.button_results_filter.setEnabled(True)
        else:
            self.label_number_results.setText(self.tr('Number of Results: 0'))

            self.button_results_filter.setEnabled(False)

        if [i for i in range(self.columnCount()) if self.item(0, i)] and rows_visible:
            self.button_results_search.setEnabled(True)
        else:
            self.button_results_search.setEnabled(False)
