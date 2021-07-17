#
# Wordless: Files
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import collections
import copy
import csv
import os
import re
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import bs4
import docx
from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
import openpyxl

from wl_checking import wl_checking_file, wl_checking_misc
from wl_dialogs import wl_dialog_error, wl_dialog_misc, wl_msg_box
from wl_text import wl_text
from wl_utils import wl_conversion, wl_detection, wl_misc, wl_threading
from wl_widgets import wl_box, wl_layout, wl_table

class Wl_Worker_Open_Files(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(list)

    def run(self):
        new_files = []

        if self.file_paths:
            len_file_paths = len(self.file_paths)

            for i, file_path in enumerate(self.file_paths):
                self.progress_updated.emit(self.tr(f'Loading files... ({i + 1}/{len_file_paths})'))

                default_dir = wl_checking_misc.check_dir(self.main.settings_custom['import']['temp_files']['default_path'])
                default_encoding = self.main.settings_custom['import']['temp_files']['default_encoding']

                file_path = wl_misc.get_normalized_path(file_path)
                file_name, file_ext = os.path.splitext(os.path.basename(file_path))
                file_ext = file_ext.lower()

                # Text files
                if file_ext == '.txt':
                    new_files.append(self.main.wl_files._new_file(file_path))
                else:
                    if file_ext in ['.docx', '.xlsx', '.xls']:
                        new_path = wl_checking_misc.check_new_path(os.path.join(default_dir, f'{file_name}.txt'))

                        # Word documents
                        if file_ext == '.docx':
                            lines = []

                            with open(new_path, 'w', encoding = default_encoding) as f:
                                doc = docx.Document(file_path)

                                for block in self.iter_block_items(doc):
                                    if type(block) == docx.text.paragraph.Paragraph:
                                        f.write(f'{block.text}\n')
                                    elif type(block) == docx.table.Table:
                                        for row in self.iter_visual_cells(block):
                                            cells = []

                                            for cell in row:
                                                cells.append(' '.join([item.text for item in self.iter_cell_items(cell)]))

                                            f.write('\t'.join(cells) + '\n')

                        # Excel workbooks
                        elif file_ext == '.xlsx':
                            with open(new_path, 'w', encoding = default_encoding) as f:
                                workbook = openpyxl.load_workbook(file_path, data_only = True)

                                for worksheet_name in workbook.sheetnames:
                                    worksheet = workbook[worksheet_name]

                                    for row in worksheet.rows:
                                        f.write('\t'.join([(cell.value if cell.value != None else '')
                                                           for cell in row]) + '\n')

                        new_paths = [new_path]
                    else:
                        # Detect encoding
                        if self.main.settings_custom['files']['auto_detection_settings']['detect_encodings']:
                            encoding_code = wl_detection.detect_encoding(self.main, file_path)
                        else:
                            encoding_code = self.main.settings_custom['auto_detection']['default_settings']['default_encoding']

                        # CSV files
                        if file_ext == '.csv':
                            new_path = wl_checking_misc.check_new_path(os.path.join(default_dir, f'{file_name}.txt'))

                            with open(new_path, 'w', encoding = default_encoding) as f:
                                with open(file_path, 'r', newline = '', encoding = encoding_code) as f_csv:
                                    csv_reader = csv.reader(f_csv)

                                    for row in csv_reader:
                                        f.write('\t'.join(row) + '\n')

                            new_paths = [new_path]

                        # HTML files
                        elif file_ext in ['.htm', '.html']:
                            with open(file_path, 'r', encoding = encoding_code) as f:
                                soup = bs4.BeautifulSoup(f.read(), 'lxml')

                            new_path = wl_checking_misc.check_new_path(os.path.join(default_dir, f'{file_name}.txt'))

                            with open(new_path, 'w', encoding = default_encoding) as f:
                                f.write(soup.get_text())

                            new_paths = [new_path]

                        # XML files
                        elif file_ext == '.xml':
                            with open(file_path, 'r', encoding = encoding_code) as f:
                                xml_text = f.read()

                            new_path = wl_checking_misc.check_new_path(os.path.join(default_dir, f'{file_name}.xml'))

                            with open(new_path, 'w', encoding = default_encoding) as f:
                                f.write(xml_text)

                            new_paths = [new_path]

                        # Translation memory files
                        elif file_ext == '.tmx':
                            lines_src = []
                            lines_target = []

                            with open(file_path, 'r', encoding = encoding_code) as f:
                                soup = bs4.BeautifulSoup(f.read(), 'lxml-xml')

                                for tu in soup.find_all('tu'):
                                    seg_src, seg_target = tu.find_all('seg')

                                    lines_src.append(seg_src.get_text())
                                    lines_target.append(seg_target.get_text())

                            path_src = wl_checking_misc.check_new_path(os.path.join(default_dir, f'{file_name}_source.txt'))
                            path_target = wl_checking_misc.check_new_path(os.path.join(default_dir, f'{file_name}_target.txt'))

                            with open(path_src, 'w', encoding = default_encoding) as f:
                                f.write('\n'.join(lines_src))
                                f.write('\n')

                            with open(path_target, 'w', encoding = default_encoding) as f:
                                f.write('\n'.join(lines_target))
                                f.write('\n')

                            new_paths = [path_src, path_target]

                    for new_path in new_paths:
                        new_files.append(self.main.wl_files._new_file(new_path, txt = False))

            self.main.settings_custom['import']['files']['default_path'] = wl_misc.get_normalized_dir(self.file_paths[0])

        self.progress_updated.emit(self.tr('Updating table...'))

        time.sleep(0.1)

        self.worker_done.emit(new_files)

    # python-docx/Issue #276: https://github.com/python-openxml/python-docx/issues/276
    def iter_block_items(self, parent):
        """
        Yield each paragraph and table child within *parent*, in document order.
        Each returned value is an instance of either Table or Paragraph. *parent*
        would most commonly be a reference to a main Document object, but
        also works for a _Cell object, which itself can contain paragraphs and tables.
        """
        if isinstance(parent, Document):
            parent_elm = parent.element.body
        elif isinstance(parent, _Cell):
            parent_elm = parent._tc
        else:
            raise ValueError("something's not right")

        for child in parent_elm.iterchildren():
            if isinstance(child, CT_P):
                yield Paragraph(child, parent)
            elif isinstance(child, CT_Tbl):
                yield Table(child, parent)

    def iter_cell_items(self, parent):
        parent_elm = parent._tc

        for child in parent_elm.iterchildren():
            if isinstance(child, CT_P):
                yield Paragraph(child, parent)
            elif isinstance(child, CT_Tbl):
                table = Table(child, parent)

                for row in table.rows:
                    for cell in row.cells:
                        yield from self.iter_cell_items(cell)

    # python-docx/Issue #40: https://github.com/python-openxml/python-docx/issues/40
    def iter_visual_cells(self, table):
        prior_tcs = []
        visual_cells = []

        for row in table.rows:
            visual_cells.append([])

            for cell in row.cells:
                this_tc = cell._tc

                if this_tc in prior_tcs:  # skip cells pointing to same `<w:tc>` element
                    continue
                else:
                    prior_tcs.append(this_tc)

                    visual_cells[-1].append(cell)

        return visual_cells

class Wl_Worker_Reload_Files(wl_threading.Wl_Worker_No_Callback):
    def run(self):
        files_reloaded = []

        len_files = len(self.files)

        for i, file in enumerate(self.files):
            self.progress_updated.emit(self.tr(f'Reloading files... ({i + 1}/{len_files})'))

            # Re-process texts
            file['text'] = wl_text.Wl_Text(self.main, file)
            file['text'].main = None

        self.worker_done.emit()

class Wl_Files():
    def __init__(self, table):
        self.main = table.main
        self.table = table

    def _new_file(self, file_path, txt = True):
        new_file = {}

        detect_pass_encoding = True
        detect_pass_lang = True

        new_file['selected'] = True

        new_file['path'] = file_path

        if new_file['path'].endswith('.xml'):
            new_file['tokenized'] = 'Yes'
            new_file['tagged'] = 'Yes'
        else:
            new_file['tokenized'] = 'No'
            new_file['tagged'] = 'No'

        new_file['name'], _ = os.path.splitext(os.path.basename(new_file['path']))
        new_file['name_old'] = new_file['name']

        # Detect encodings
        if self.main.settings_custom['files']['auto_detection_settings']['detect_encodings']:
            new_file['encoding'] = wl_detection.detect_encoding(self.main, new_file['path'])
        else:
            new_file['encoding'] = self.main.settings_custom['auto_detection']['default_settings']['default_encoding']

        # Detect languages
        if self.main.settings_custom['files']['auto_detection_settings']['detect_langs']:
            new_file['lang'] = wl_detection.detect_lang(self.main, new_file)
        else:
            new_file['lang'] = self.main.settings_custom['auto_detection']['default_settings']['default_lang']

        if txt:
            default_dir = wl_checking_misc.check_dir(self.main.settings_custom['import']['temp_files']['default_path'])

            new_file['path'] = os.path.join(default_dir, re.split(r'[/\\]', file_path)[-1])
            new_file['path'] = wl_checking_misc.check_new_path(new_file['path'])

        # Remove header tags
        tags_header = []

        for _, _, tag_opening, _ in self.main.settings_custom['tags']['tags_header']:
            tags_header.append(tag_opening[1:-1])

        text = ''

        with open(file_path, 'r', encoding = new_file['encoding']) as f:
            for line in f:
                text += line

        # The "lxml" parser will add <html><body> to the text, which is undesirable
        with open(new_file['path'], 'w', encoding = 'utf_8') as f:
            soup = bs4.BeautifulSoup(text, features = 'html.parser')

            for tag_header in tags_header:
                for header_element in soup.select(tag_header):
                    header_element.decompose()

            f.write(str(soup))

        # Check for duplicate file names
        file_names = [file['name'] for file in self.main.settings_custom['files']['files_open']]
        new_file['name'] = new_file['name_old'] = wl_checking_misc.check_new_name(new_file['name'], file_names)

        # Process texts
        new_file['text'] = wl_text.Wl_Text(self.main, new_file)
        # Remove the main object from all texts
        new_file['text'].main = None

        return new_file

    @wl_misc.log_timing
    def open_files(self, file_paths):
        def update_gui(new_files):
            len_files_old = len(self.main.settings_custom['files']['files_open'])

            self.main.settings_custom['files']['files_open'].extend(new_files)

            self.update_table()

            len_files_new = len(self.main.settings_custom['files']['files_open'])

            if len_files_new - len_files_old == 0:
                self.main.statusBar().showMessage('No files are newly opened!')
            elif len_files_new - len_files_old == 1:
                self.main.statusBar().showMessage('1 file has been successfully opened.')
            else:
                self.main.statusBar().showMessage(f'{len_files_new - len_files_old} files have been successfully opened.')

        file_paths, file_paths_missing = wl_checking_file.check_file_paths_missing(self.main, file_paths)
        file_paths, file_paths_empty = wl_checking_file.check_file_paths_empty(self.main, file_paths)
        file_paths, file_paths_unsupported = wl_checking_file.check_file_paths_unsupported(self.main, file_paths)
        file_paths, file_paths_parsing_error = wl_checking_file.check_file_paths_parsing_error(self.main, file_paths)

        dialog_progress = wl_dialog_misc.Wl_Dialog_Progress_Open_Files(self.main)

        worker_open_files = Wl_Worker_Open_Files(
            self.main,
            dialog_progress = dialog_progress,
            update_gui = update_gui,
            file_paths = file_paths
        )

        thread_open_files = wl_threading.Wl_Thread(worker_open_files)
        thread_open_files.start_worker()

        wl_dialog_error.wl_dialog_error_file_open(
            self.main,
            file_paths_missing = file_paths_missing,
            file_paths_empty = file_paths_empty,
            file_paths_unsupported = file_paths_unsupported,
            file_paths_parsing_error = file_paths_parsing_error
        )

    @wl_misc.log_timing
    def reload_files(self, file_indexes):
        dialog_progress = wl_dialog_misc.Wl_Dialog_Progress_Open_Files(self.main)
        
        worker_reload_files = Wl_Worker_Reload_Files(
            self.main,
            dialog_progress = dialog_progress,
            files = [self.main.settings_custom['files']['files_open'][i] for i in file_indexes]
        )
        
        thread_reload_files = wl_threading.Wl_Thread(worker_reload_files)
        thread_reload_files.start_worker()

    def close_files(self, file_indexes):
        self.main.settings_custom['files']['files_closed'].append([])

        for i in reversed(file_indexes):
            self.main.settings_custom['files']['files_closed'][-1].append(self.main.settings_custom['files']['files_open'].pop(i))

        self.update_table()

    def update_table(self):
        self.table.blockSignals(True)
        self.table.setUpdatesEnabled(False)

        files = self.main.settings_custom['files']['files_open']
        
        if files:
            self.table.clear_table(len(files))

            for i, file in enumerate(files):
                checkbox_name = QTableWidgetItem(file['name'])
                combo_box_lang = wl_box.Wl_Combo_Box_Lang(self.table)
                combo_box_tokenized = wl_box.Wl_Combo_Box_Yes_No(self.table)
                combo_box_tagged = wl_box.Wl_Combo_Box_Yes_No(self.table)
                combo_box_encoding = wl_box.Wl_Combo_Box_Encoding(self.table)

                if file['selected']:
                    checkbox_name.setCheckState(Qt.Checked)
                else:
                    checkbox_name.setCheckState(Qt.Unchecked)

                combo_box_lang.setCurrentText(wl_conversion.to_lang_text(self.main, file['lang']))
                combo_box_tokenized.setCurrentText(file['tokenized'])
                combo_box_tagged.setCurrentText(file['tagged'])
                combo_box_encoding.setCurrentText(wl_conversion.to_encoding_text(self.main, file['encoding']))

                combo_box_lang.currentTextChanged.connect(lambda: self.table.itemChanged.emit(self.table.item(i, 1)))
                combo_box_tokenized.currentTextChanged.connect(lambda: self.table.itemChanged.emit(self.table.item(i, 2)))
                combo_box_tagged.currentTextChanged.connect(lambda: self.table.itemChanged.emit(self.table.item(i, 3)))
                combo_box_encoding.currentTextChanged.connect(lambda: self.table.itemChanged.emit(self.table.item(i, 5)))

                self.table.setItem(i, 0, checkbox_name)
                self.table.setCellWidget(i, 1, combo_box_lang)
                self.table.setCellWidget(i, 2, combo_box_tokenized)
                self.table.setCellWidget(i, 3, combo_box_tagged)
                self.table.setItem(i, 4, QTableWidgetItem(file['path']))
                self.table.setCellWidget(i, 5, combo_box_encoding)
        else:
            self.table.clear_table(1)

        self.table.blockSignals(False)
        self.table.setUpdatesEnabled(True)

        self.table.itemChanged.emit(self.table.item(0, 0))

    def get_selected_files(self):
        files_selected = [file for file in self.main.settings_custom['files']['files_open'] if file['selected']]
        
        return files_selected

    def find_file_by_name(self, file_name, selected_only = False):
        if selected_only:
            files = self.get_selected_files()
        else:
            files = self.main.settings_custom['files']['files_open']

        for file in files:
            if file['name'] == file_name:
                return file

        return None

    def find_file_by_path(self, file_path, selected_only = False):
        if selected_only:
            files = self.get_selected_files()
        else:
            files = self.main.settings_custom['files']['files_open']
            
        for file in files:
            if os.path.normcase(file['path']) == os.path.normcase(file_path):
                return file

        return None

class Wl_Table_Files(wl_table.Wl_Table):
    def __init__(self, parent):
        super().__init__(
            parent,
            headers = [
                parent.tr('Name'),
                parent.tr('Language'),
                parent.tr('Tokenized'),
                parent.tr('Tagged'),
                parent.tr('Path'),
                parent.tr('Encoding')
            ],
            drag_drop_enabled = True
        )

        self.name = 'file_area'

        self.itemChanged.connect(self.file_item_changed)
        self.itemClicked.connect(self.file_item_changed)
        self.itemSelectionChanged.connect(self.file_selection_changed)
        self.cellDoubleClicked.connect(self.cell_double_clicked)

        self.button_open_files = QPushButton(self.tr('Open File(s)...'))
        self.button_open_dir = QPushButton(self.tr('Open Folder...'))
        self.button_reload_selected = QPushButton(self.tr('Reload Selected'))
        self.button_reload_all = QPushButton(self.tr('Reload All'))
        self.button_close_selected = QPushButton(self.tr('Close Selected'))
        self.button_close_all = QPushButton(self.tr('Close All'))

        self.button_open_files.clicked.connect(self.open_files)
        self.button_open_dir.clicked.connect(self.open_dir)
        self.button_reload_selected.clicked.connect(self.reload_selected)
        self.button_reload_all.clicked.connect(self.reload_all)
        self.button_close_selected.clicked.connect(self.close_selected)
        self.button_close_all.clicked.connect(self.close_all)

        # Menu
        self.main.find_menu_item(self.tr('Open File(s)...')).triggered.connect(self.open_files)
        self.main.find_menu_item(self.tr('Open Folder...')).triggered.connect(self.open_dir)
        self.main.find_menu_item(self.tr('Reopen Closed Files')).triggered.connect(self.reopen)

        self.main.find_menu_item(self.tr('Reload Selected')).triggered.connect(self.reload_selected)
        self.main.find_menu_item(self.tr('Reload All')).triggered.connect(self.reload_all)

        self.main.find_menu_item(self.tr('Select All')).triggered.connect(self.select_all)
        self.main.find_menu_item(self.tr('Deselect All')).triggered.connect(self.deselect_all)
        self.main.find_menu_item(self.tr('Invert Selection')).triggered.connect(self.invert_selection)

        self.main.find_menu_item(self.tr('Close Selected')).triggered.connect(self.close_selected)
        self.main.find_menu_item(self.tr('Close All')).triggered.connect(self.close_all)

        self.file_item_changed()

    def file_item_changed(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            # Check for duplicate file names
            for row in range(self.rowCount()):
                file_name = self.item(row, 0).text()
                file_path = self.item(row, 4).text()

                file = self.main.wl_files.find_file_by_path(file_path)

                if file_name != file['name_old']:
                    if self.main.wl_files.find_file_by_name(file_name):
                        self.blockSignals(True)

                        self.item(row, 0).setText(file['name_old'])
                        
                        self.blockSignals(False)

                        wl_msg_box.wl_msg_box_duplicate_file_name(self.main)

                        self.closePersistentEditor(self.item(row, 0))
                        self.editItem(self.item(row, 0))

                    break

            file_texts = {file['path']: file['text'] for file in self.main.settings_custom['files']['files_open']}

            self.main.settings_custom['files']['files_open'].clear()

            for row in range(self.rowCount()):
                new_file = {}

                lang_text = self.cellWidget(row, 1).currentText()
                encoding_text = self.cellWidget(row, 5).currentText()

                new_file['selected'] = True if self.item(row, 0).checkState() == Qt.Checked else False
                new_file['name'] = new_file['name_old'] = self.item(row, 0).text()
                new_file['lang'] = wl_conversion.to_lang_code(self.main, lang_text)
                new_file['tokenized'] = self.cellWidget(row, 2).currentText()
                new_file['tagged'] = self.cellWidget(row, 3).currentText()
                new_file['path'] = self.item(row, 4).text()
                new_file['encoding'] = wl_conversion.to_encoding_code(self.main, encoding_text)
                new_file['text'] = file_texts[new_file['path']]

                self.main.settings_custom['files']['files_open'].append(new_file)

            self.button_close_all.setEnabled(True)
        else:
            self.button_close_all.setEnabled(False)

        # Menu
        if any([self.item(0, i) for i in range(self.columnCount())]):
            self.main.find_menu_item(self.tr('Reload All')).setEnabled(True)

            self.main.find_menu_item(self.tr('Select All')).setEnabled(True)
            self.main.find_menu_item(self.tr('Deselect All')).setEnabled(True)
            self.main.find_menu_item(self.tr('Invert Selection')).setEnabled(True)

            self.main.find_menu_item(self.tr('Close All')).setEnabled(True)
        else:
            self.main.find_menu_item(self.tr('Reload All')).setEnabled(False)

            self.main.find_menu_item(self.tr('Select All')).setEnabled(False)
            self.main.find_menu_item(self.tr('Deselect All')).setEnabled(False)
            self.main.find_menu_item(self.tr('Invert Selection')).setEnabled(False)

            self.main.find_menu_item(self.tr('Close All')).setEnabled(False)

        if self.main.settings_custom['files']['files_closed']:
            self.main.find_menu_item(self.tr('Reopen Closed Files')).setEnabled(True)
        else:
            self.main.find_menu_item(self.tr('Reopen Closed Files')).setEnabled(False)

        if self.rowCount() == 0:
            self.setRowCount(1)

        self.file_selection_changed()

    def file_selection_changed(self):
        if any([self.item(0, i) for i in range(self.columnCount())]) and self.selectedIndexes():
            self.button_reload_selected.setEnabled(True)
            self.button_close_selected.setEnabled(True)

            # Menu
            self.main.find_menu_item(self.tr('Reload Selected')).setEnabled(True)
            self.main.find_menu_item(self.tr('Close Selected')).setEnabled(True)
        else:
            self.button_reload_selected.setEnabled(False)
            self.button_close_selected.setEnabled(False)

            # Menu
            self.main.find_menu_item(self.tr('Reload Selected')).setEnabled(False)
            self.main.find_menu_item(self.tr('Close Selected')).setEnabled(False)

    def cell_double_clicked(self, row, col):
        if col == self.find_col(self.tr('File Name')):
            self.editItem(self.item(row, col))

    def open_files(self):
        if os.path.exists(self.main.settings_custom['import']['files']['default_path']):
            default_dir = self.main.settings_custom['import']['files']['default_path']
        else:
            default_dir = self.main.settings_default['import']['files']['default_path']

        file_paths = QFileDialog.getOpenFileNames(
            self.main,
            self.tr('Open File(s)'),
            wl_checking_misc.check_dir(default_dir),
            ';;'.join(self.main.settings_global['file_types']['files']),
            self.main.settings_global['file_types']['files'][-1]
        )[0]

        if file_paths:
            self.main.wl_files.open_files(file_paths)

    def open_dir(self):
        file_paths = []

        file_dir = QFileDialog.getExistingDirectory(
            self.main,
            self.tr('Open Folder'),
            self.main.settings_custom['import']['files']['default_path']
        )

        if file_dir:
            if self.main.settings_custom['files']['folder_settings']['subfolders']:
                for dir_path, dir_names, file_names in os.walk(file_dir):
                    for file_name in file_names:
                        file_paths.append(os.path.join(dir_path, file_name))
            else:
                file_names = list(os.walk(file_dir))[0][2]

                for file_name in file_names:
                    file_paths.append(os.path.join(file_dir, file_name))

            self.main.wl_files.open_files(file_paths)

    def reopen(self):
        files = self.main.settings_custom['files']['files_closed'].pop()

        self.main.wl_files.open_files([file['path'] for file in files])

    def reload_selected(self):
        self.main.wl_files.reload_files(self.get_selected_rows())

    def reload_all(self):
        self.main.wl_files.reload_files(list(range(len(self.main.settings_custom['files']['files_open']))))

    def select_all(self):
        if self.item(0, 0):
            for i in range(self.rowCount()):
                if self.item(i, 0).checkState() == Qt.Unchecked:
                    self.item(i, 0).setCheckState(Qt.Checked)

    def deselect_all(self):
        if self.item(0, 0):
            for i in range(self.rowCount()):
                if self.item(i, 0).checkState() == Qt.Checked:
                    self.item(i, 0).setCheckState(Qt.Unchecked)

    def invert_selection(self):
        if self.item(0, 0):
            for i in range(self.rowCount()):
                if self.item(i, 0).checkState() == Qt.Checked:
                    self.item(i, 0).setCheckState(Qt.Unchecked)
                else:
                    self.item(i, 0).setCheckState(Qt.Checked)

    def close_selected(self):
        self.main.wl_files.close_files(self.get_selected_rows())

    def close_all(self):
        self.main.wl_files.close_files(list(range(len(self.main.settings_custom['files']['files_open']))))

class Wrapper_File_Area(wl_layout.Wl_Wrapper_File_Area):
    def __init__(self, main):
        super().__init__(main)

        # Table
        self.table_files = Wl_Table_Files(self)

        self.wrapper_table.layout().addWidget(self.table_files, 0, 0, 1, 6)
        self.wrapper_table.layout().addWidget(self.table_files.button_open_files, 1, 0)
        self.wrapper_table.layout().addWidget(self.table_files.button_open_dir, 1, 1)
        self.wrapper_table.layout().addWidget(self.table_files.button_reload_selected, 1, 2)
        self.wrapper_table.layout().addWidget(self.table_files.button_reload_all, 1, 3)
        self.wrapper_table.layout().addWidget(self.table_files.button_close_selected, 1, 4)
        self.wrapper_table.layout().addWidget(self.table_files.button_close_all, 1, 5)

        # Folder Settings
        self.group_box_folder_settings = QGroupBox(self.tr('Folder Settings'), self)

        self.checkbox_subfolders = QCheckBox(self.tr('Subfolders'), self)

        self.checkbox_subfolders.stateChanged.connect(self.folder_settings_changed)

        self.group_box_folder_settings.setLayout(wl_layout.Wl_Layout())
        self.group_box_folder_settings.layout().addWidget(self.checkbox_subfolders, 0, 0)

        # Auto-detection Settings
        self.group_box_auto_detection_settings = QGroupBox(self.tr('Auto-detection Settings'), self)

        self.checkbox_detect_langs = QCheckBox(self.tr('Detect languages'), self)
        self.checkbox_detect_encodings = QCheckBox(self.tr('Detect encodings'), self)

        self.checkbox_detect_langs.stateChanged.connect(self.auto_detection_settings_changed)
        self.checkbox_detect_encodings.stateChanged.connect(self.auto_detection_settings_changed)

        self.group_box_auto_detection_settings.setLayout(wl_layout.Wl_Layout())
        self.group_box_auto_detection_settings.layout().addWidget(self.checkbox_detect_langs, 0, 0)
        self.group_box_auto_detection_settings.layout().addWidget(self.checkbox_detect_encodings, 0, 1)

        self.wrapper_settings.layout().addWidget(self.group_box_folder_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_auto_detection_settings, 1, 0)

        self.wrapper_settings.layout().setRowStretch(2, 1)

        self.load_settings()

        # Load files
        self.main.wl_files = Wl_Files(self.table_files)
        self.main.wl_files.update_table()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['files'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['files'])

        self.checkbox_subfolders.setChecked(settings['folder_settings']['subfolders'])

        self.checkbox_detect_langs.setChecked(settings['auto_detection_settings']['detect_langs'])
        self.checkbox_detect_encodings.setChecked(settings['auto_detection_settings']['detect_encodings'])

        self.folder_settings_changed()
        self.auto_detection_settings_changed()

    def folder_settings_changed(self):
        settings = self.main.settings_custom['files']['folder_settings']

        settings['subfolders'] = self.checkbox_subfolders.isChecked()

    def auto_detection_settings_changed(self):
        settings = self.main.settings_custom['files']['auto_detection_settings']

        settings['detect_langs'] = self.checkbox_detect_langs.isChecked()
        settings['detect_encodings'] = self.checkbox_detect_encodings.isChecked()
