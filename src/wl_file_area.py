# ----------------------------------------------------------------------
# Wordless: Files
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
import re
import traceback

import bs4
import docx
from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
import openpyxl
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_checking import wl_checking_files, wl_checking_misc
from wl_dialogs import wl_dialogs_errs, wl_dialogs_misc, wl_msg_boxes
from wl_nlp import wl_matching, wl_texts
from wl_utils import wl_conversion, wl_detection, wl_misc, wl_msgs, wl_threading
from wl_widgets import wl_boxes, wl_layouts, wl_tables

class Wl_Worker_Open_Files(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, list)

    def run(self):
        err_msg = ''
        new_files = []

        try:
            len_file_paths = len(self.file_paths)
            # Regex for headers
            re_tags_header = wl_matching.get_re_tags_with_tokens(self.main, tag_type = 'header')

            for i, file_path in enumerate(self.file_paths):
                self.progress_updated.emit(self.tr(f'Loading files... ({i + 1}/{len_file_paths})'))

                new_files_temp = []
                lines = []

                default_dir = wl_checking_misc.check_dir(self.main.settings_custom['imp']['temp_files']['default_path'])
                default_encoding = self.main.settings_custom['files']['default_settings']['encoding']

                file_path = wl_misc.get_normalized_path(file_path)
                file_name, file_ext = os.path.splitext(os.path.basename(file_path))
                file_ext = file_ext.lower()

                new_file = {'selected': True}

                # Check for duplicate file names
                file_names = [file['name'] for file in self.main.settings_custom['file_area']['files_open']]

                new_file['name'] = new_file['name_old'] = wl_checking_misc.check_new_name(file_name, file_names)

                # XML files
                if file_ext == '.xml':
                    new_file['path'] = os.path.join(default_dir, f'{file_name}.xml')

                    new_file['tokenized'] = 'Yes'
                    new_file['tagged'] = 'Yes'
                else:
                    new_file['path'] = os.path.join(default_dir, f'{file_name}.txt')

                    new_file['tokenized'] = self.main.settings_custom['files']['default_settings']['tokenized']
                    new_file['tagged'] = self.main.settings_custom['files']['default_settings']['tagged']

                # Check for duplicate files
                new_file['path'] = wl_checking_misc.check_new_path(new_file['path'])
                # Record original file paths
                new_file['path_original'] = file_path

                if file_ext in ['.docx', '.xlsx']:
                    new_file['encoding'] = default_encoding
                else:
                    # Detect encodings
                    if self.main.settings_custom['file_area']['auto_detection_settings']['detect_encodings']:
                        new_file['encoding'] = wl_detection.detect_encoding(self.main, file_path)
                    else:
                        new_file['encoding'] = default_encoding

                    with open(file_path, 'r', encoding = new_file['encoding'], errors = 'replace') as f:
                        text = f.read()

                if file_ext in ['.txt', '.xml']:
                    with open(file_path, 'r', encoding = new_file['encoding'], errors = 'replace') as f:
                        new_file['text'] = f.read()

                    new_files_temp.append(new_file)
                # CSV files
                elif file_ext == '.csv':
                    with open(file_path, 'r', encoding = new_file['encoding'], errors = 'replace', newline = '') as f:
                        # Remove NULL bytes to avoid error
                        csv_reader = csv.reader([line.replace('\0', '') for line in f])

                        for row in csv_reader:
                            lines.append('\t'.join(row))

                    new_file['text'] = '\n'.join(lines)
                    new_files_temp.append(new_file)
                # HTML pages
                elif file_ext in ['.htm', '.html']:
                    soup = bs4.BeautifulSoup(text, 'lxml')

                    new_file['text'] = soup.get_text()
                    new_files_temp.append(new_file)
                # Microsoft Word documents
                elif file_ext == '.docx':
                    doc = docx.Document(file_path)

                    for block in self.iter_block_items(doc):
                        if type(block) == docx.text.paragraph.Paragraph:
                            lines.append(block.text)
                        elif type(block) == docx.table.Table:
                            for row in self.iter_visual_cells(block):
                                cells = []

                                for cell in row:
                                    cells.append(' '.join([item.text for item in self.iter_cell_items(cell)]))

                                lines.append('\t'.join(cells))

                    new_file['text'] = '\n'.join(lines)
                    new_files_temp.append(new_file)
                # Microsoft Excel workbooks
                elif file_ext == '.xlsx':
                    workbook = openpyxl.load_workbook(file_path, data_only = True)

                    for worksheet_name in workbook.sheetnames:
                        worksheet = workbook[worksheet_name]

                        for row in worksheet.rows:
                            cells = [(cell.value if cell.value != None else '')
                                     for cell in row]

                            lines.append('\t'.join(cells))

                    new_file['text'] = '\n'.join(lines)
                    new_files_temp.append(new_file)
                # Translation memory files
                elif file_ext == '.tmx':
                    lines_src = []
                    lines_target = []

                    new_file_src = copy.deepcopy(new_file)
                    new_file_tgt = copy.deepcopy(new_file)

                    new_file_src['name'] = new_file_src['name_old'] = wl_checking_misc.check_new_name(f'{file_name}_source', file_names)
                    new_file_tgt['name'] = new_file_tgt['name_old'] = wl_checking_misc.check_new_name(f'{file_name}_target', file_names)

                    soup = bs4.BeautifulSoup(text, 'lxml-xml')

                    # Extract source and target languages
                    elements_tuv = soup.select(r'tu:first-child tuv[xml\:lang]')

                    if len(elements_tuv) == 2:
                        new_file_src['lang'] = wl_conversion.to_iso_639_3(self.main, elements_tuv[0]['xml:lang'])
                        new_file_tgt['lang'] = wl_conversion.to_iso_639_3(self.main, elements_tuv[1]['xml:lang'])
                    else:
                        new_file_src['lang'] = self.main.settings_custom['files']['default_settings']['lang']
                        new_file_tgt['lang'] = self.main.settings_custom['files']['default_settings']['lang']

                    for elements_tu in soup.select('tu'):
                        seg_src, seg_target = elements_tu.select('seg')

                        lines_src.append(seg_src.get_text().replace(r'\n', ' ').strip())
                        lines_target.append(seg_target.get_text().replace(r'\n', ' ').strip())

                    new_file_src['path'] = wl_checking_misc.check_new_path(os.path.join(default_dir, f'{file_name}_source.txt'))
                    new_file_tgt['path'] = wl_checking_misc.check_new_path(os.path.join(default_dir, f'{file_name}_target.txt'))

                    new_file_src['text'] = '\n'.join(lines_src)
                    new_file_tgt['text'] = '\n'.join(lines_target)

                    new_files_temp.append(new_file_src)
                    new_files_temp.append(new_file_tgt)

                for new_file in new_files_temp:
                    # Remove header tags
                    tags_header = []

                    for _, _, tag_opening in self.main.settings_custom['tags']['tags_header']:
                        tags_header.append(tag_opening[1:-1])

                    with open(new_file['path'], 'w', encoding = new_file['encoding']) as f:
                        text = new_file['text']

                        if new_file['tagged'] == 'Yes' and tags_header:
                            # Use regex here since BeautifulSoup will add tags including <html> and <body> to the text
                            # See: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#differences-between-parsers
                            text = re.sub(re_tags_header, '', text)

                        f.write(text)

                    # Detect languages
                    if file_ext != '.tmx':
                        if self.main.settings_custom['file_area']['auto_detection_settings']['detect_langs']:
                            new_file['lang'] = wl_detection.detect_lang(self.main, new_file)
                        else:
                            new_file['lang'] = self.main.settings_custom['files']['default_settings']['lang']

                    # Process texts
                    new_file['text'] = wl_texts.Wl_Text(self.main, new_file)

                    new_files.append(new_file)

            if self.file_paths:
                self.main.settings_custom['imp']['files']['default_path'] = wl_misc.get_normalized_dir(self.file_paths[0])
        except Exception:
            err_msg = traceback.format_exc()

        self.progress_updated.emit(self.tr('Updating table...'))
        self.worker_done.emit(err_msg, new_files)

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
        len_files = len(self.files)

        for i, file in enumerate(self.files):
            self.progress_updated.emit(self.tr(f'Reloading files... ({i + 1}/{len_files})'))

            # Re-process texts
            file['text'] = wl_texts.Wl_Text(self.main, file)
            file['text'].main = None

        self.worker_done.emit()

class Wl_Files(QObject):
    def __init__(self, table):
        super().__init__()

        self.main = table.main
        self.table = table
        self.file_names_old = []

    @wl_misc.log_timing
    def open_files(self, file_paths):
        def update_gui(err_msg, new_files):
            if not err_msg:
                len_files_old = len(self.main.settings_custom['file_area']['files_open'])

                self.main.settings_custom['file_area']['files_open'].extend(new_files)

                self.update_table()

                len_files_new = len(self.main.settings_custom['file_area']['files_open'])

                if len_files_new - len_files_old == 0:
                    self.main.statusBar().showMessage('No files are newly opened!')
                elif len_files_new - len_files_old == 1:
                    self.main.statusBar().showMessage('1 file has been successfully opened.')
                else:
                    self.main.statusBar().showMessage(f'{len_files_new - len_files_old} files have been successfully opened.')
            else:
                wl_dialogs_errs.Wl_Dialog_Err_Fatal(self.main, err_msg).open()

                wl_msgs.wl_msg_fatal_error(self.main)

        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = self.tr('Checking files...'))

        file_paths, file_paths_unsupported = wl_checking_files.check_file_paths_unsupported(self.main, file_paths)
        file_paths, file_paths_empty = wl_checking_files.check_file_paths_empty(self.main, file_paths)
        file_paths, file_paths_duplicate = wl_checking_files.check_file_paths_duplicate(self.main, file_paths)

        worker_open_files = Wl_Worker_Open_Files(
            self.main,
            dialog_progress = dialog_progress,
            update_gui = update_gui,
            file_paths = file_paths
        )

        thread_open_files = wl_threading.Wl_Thread(worker_open_files)
        thread_open_files.start_worker()

        if file_paths_empty or file_paths_unsupported or file_paths_duplicate:
            dialog_err_files = wl_dialogs_errs.Wl_Dialog_Err_Files(self.main, title = self.tr('Error Opening Files'))

            dialog_err_files.label_err.set_text(self.tr('''
                <div>
                    An error occurred while opening files, so the following file(s) are skipped and will not be added to the file table.
                </div>
            '''))

            dialog_err_files.table_err_files.model().setRowCount(len(file_paths_empty) + len(file_paths_unsupported) + len(file_paths_duplicate))

            dialog_err_files.table_err_files.disable_updates()

            for i, file_path in enumerate(file_paths_empty + file_paths_unsupported + file_paths_duplicate):
                if file_path in file_paths_empty:
                    dialog_err_files.table_err_files.model().setItem(
                        i, 0,
                        QStandardItem(self.tr('Empty File'))
                    )
                elif file_path in file_paths_unsupported:
                    dialog_err_files.table_err_files.model().setItem(
                        i, 0,
                        QStandardItem(self.tr('Unsupported File Type'))
                    )
                elif file_path in file_paths_duplicate:
                    dialog_err_files.table_err_files.model().setItem(
                        i, 0,
                        QStandardItem(self.tr('Duplicate File'))
                    )

                dialog_err_files.table_err_files.model().setItem(
                    i, 1,
                    QStandardItem(file_path)
                )

            dialog_err_files.table_err_files.enable_updates()

            dialog_err_files.open()

    @wl_misc.log_timing
    def reload_files(self, file_indexes):
        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = self.tr('Loading files...'))

        worker_reload_files = Wl_Worker_Reload_Files(
            self.main,
            dialog_progress = dialog_progress,
            files = [self.main.settings_custom['file_area']['files_open'][i] for i in file_indexes]
        )

        thread_reload_files = wl_threading.Wl_Thread(worker_reload_files)
        thread_reload_files.start_worker()

    def close_files(self, file_indexes):
        self.main.settings_custom['file_area']['files_closed'].append([])

        for i in reversed(file_indexes):
            file_removed = self.main.settings_custom['file_area']['files_open'].pop(i)

            self.main.settings_custom['file_area']['files_closed'][-1].append(file_removed)

            # Remove temporary files
            if os.path.exists(file_removed['path']):
                os.remove(file_removed['path'])

        self.update_table()

    def update_table(self):
        files = self.main.settings_custom['file_area']['files_open']

        if files:
            self.table.clr_table(len(files))

            self.table.disable_updates()

            for i, file in enumerate(files):
                item_name = QStandardItem(file['name'])
                # Record file properties
                item_name.wl_file = file
                item_name.setCheckable(True)

                if file['selected']:
                    item_name.setCheckState(Qt.Checked)
                else:
                    item_name.setCheckState(Qt.Unchecked)

                self.table.model().setItem(i, 0, item_name)
                self.table.model().setItem(i, 1, QStandardItem(wl_conversion.to_lang_text(self.main, file['lang'])))
                self.table.model().setItem(i, 2, QStandardItem(file['tokenized']))
                self.table.model().setItem(i, 3, QStandardItem(file['tagged']))
                self.table.model().setItem(i, 4, QStandardItem(file['path_original']))
                self.table.model().setItem(i, 5, QStandardItem(wl_conversion.to_encoding_text(self.main, file['encoding'])))

            self.table.enable_updates()
        else:
            self.table.clr_table(1)

    def get_selected_files(self):
        files_selected = [
            file
            for file in self.main.settings_custom['file_area']['files_open']
            if file['selected']
        ]

        return files_selected

    def get_selected_file_names(self):
        file_names_selected = [
            file['name']
            for file in self.get_selected_files()
        ]

        return file_names_selected

    def find_file_by_name(self, file_name, selected_only = False):
        if selected_only:
            files = self.get_selected_files()
        else:
            files = self.main.settings_custom['file_area']['files_open']

        for file in files:
            if file['name'] == file_name:
                return file

        return None

    def find_files_by_name(self, file_names, selected_only = False):
        files = [self.find_file_by_name(file_name, selected_only = selected_only)
                 for file_name in file_names]

        return [file for file in files if file]

    def find_file_by_path(self, file_path, selected_only = False):
        if selected_only:
            files = self.get_selected_files()
        else:
            files = self.main.settings_custom['file_area']['files_open']

        for file in files:
            if os.path.normcase(file['path']) == os.path.normcase(file_path):
                return file

        return None

class Wl_Table_Files(wl_tables.Wl_Table):
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
            editable = True,
            drag_drop = True
        )

        self.setItemDelegateForColumn(1, wl_boxes.Wl_Item_Delegate_Combo_Box_Custom(self, wl_boxes.Wl_Combo_Box_Lang))
        self.setItemDelegateForColumn(2, wl_boxes.Wl_Item_Delegate_Combo_Box_Custom(self, wl_boxes.Wl_Combo_Box_Yes_No))
        self.setItemDelegateForColumn(3, wl_boxes.Wl_Item_Delegate_Combo_Box_Custom(self, wl_boxes.Wl_Combo_Box_Yes_No))
        self.setItemDelegateForColumn(4, wl_tables.Wl_Item_Delegate_Uneditable(self))
        self.setItemDelegateForColumn(5, wl_boxes.Wl_Item_Delegate_Combo_Box_Custom(self, wl_boxes.Wl_Combo_Box_Encoding))

        self.selectionModel().selectionChanged.connect(self.selection_changed)
        self.clicked.connect(self.item_clicked)

        # Menu
        self.main.action_file_open_files.triggered.connect(self.open_files)
        self.main.action_file_open_dir.triggered.connect(self.open_dir)
        self.main.action_file_reopen.triggered.connect(self.reopen)

        self.main.action_file_reload_selected.triggered.connect(self.reload_selected)
        self.main.action_file_reload_all.triggered.connect(self.reload_all)

        self.main.action_file_select_all.triggered.connect(self.select_all)
        self.main.action_file_deselect_all.triggered.connect(self.deselect_all)
        self.main.action_file_invert_selection.triggered.connect(self.invert_selection)

        self.main.action_file_close_selected.triggered.connect(self.close_selected)
        self.main.action_file_close_all.triggered.connect(self.close_all)

    def item_changed(self, item):
        super().item_changed(item)

        if not self.is_empty():
            # Record old file names that might be useful for other slots
            self.main.wl_files.file_names_old = self.main.wl_files.get_selected_file_names()

            # Check for duplicate file names
            for row in range(self.model().rowCount()):
                file = self.model().item(row, 0).wl_file
                file_name = self.model().item(row, 0).text()

                if file_name != file['name_old']:
                    if self.main.wl_files.find_file_by_name(file_name):
                        self.disable_updates()

                        self.model().item(row, 0).setText(file['name_old'])

                        self.enable_updates()

                        wl_msg_boxes.Wl_Msg_Box_Warning(
                            self.main,
                            title = self.tr('Duplicate File Names Found'),
                            text = self.tr('''
                                <div>There is already a file with the same name in the file area.</div>
                                <div>Please specify a different file name.</div>
                            ''')
                        ).open()

                        self.setCurrentIndex(self.model().index(row, 0))
                        self.closePersistentEditor(self.model().index(row, 0))
                        self.edit(self.model().index(row, 0))

                    break

            self.main.settings_custom['file_area']['files_open'].clear()

            for row in range(self.model().rowCount()):
                file = self.model().item(row, 0).wl_file

                lang_text = self.model().item(row, 1).text()
                encoding_text = self.model().item(row, 5).text()

                file['selected'] = True if self.model().item(row, 0).checkState() == Qt.Checked else False
                file['name'] = file['name_old'] = self.model().item(row, 0).text()
                file['lang'] = wl_conversion.to_lang_code(self.main, lang_text)
                file['tokenized'] = self.model().item(row, 2).text()
                file['tagged'] = self.model().item(row, 3).text()
                file['encoding'] = wl_conversion.to_encoding_code(self.main, encoding_text)

                self.main.settings_custom['file_area']['files_open'].append(file)

        # Menu
        if not self.is_empty():
            self.main.action_file_reload_all.setEnabled(True)

            self.main.action_file_select_all.setEnabled(True)
            self.main.action_file_deselect_all.setEnabled(True)
            self.main.action_file_invert_selection.setEnabled(True)

            self.main.action_file_close_all.setEnabled(True)
        else:
            self.main.action_file_reload_all.setEnabled(False)

            self.main.action_file_select_all.setEnabled(False)
            self.main.action_file_deselect_all.setEnabled(False)
            self.main.action_file_invert_selection.setEnabled(False)

            self.main.action_file_close_all.setEnabled(False)

        if self.main.settings_custom['file_area']['files_closed']:
            self.main.action_file_reopen.setEnabled(True)
        else:
            self.main.action_file_reopen.setEnabled(False)

        self.selection_changed()

    def item_clicked(self):
        if not self.is_empty():
            for row in range(self.model().rowCount()):
                self.main.settings_custom['file_area']['files_open'][row]['selected'] = True if self.model().item(row, 0).checkState() == Qt.Checked else False

    def selection_changed(self):
        if self.get_selected_rows():
            self.main.action_file_reload_selected.setEnabled(True)
            self.main.action_file_close_selected.setEnabled(True)
        else:
            self.main.action_file_reload_selected.setEnabled(False)
            self.main.action_file_close_selected.setEnabled(False)

    def open_files(self):
        if os.path.exists(self.main.settings_custom['imp']['files']['default_path']):
            default_dir = self.main.settings_custom['imp']['files']['default_path']
        else:
            default_dir = self.main.settings_default['imp']['files']['default_path']

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
            self.main.settings_custom['imp']['files']['default_path']
        )

        if file_dir:
            if self.main.settings_custom['file_area']['folder_settings']['subfolders']:
                for dir_path, dir_names, file_names in os.walk(file_dir):
                    for file_name in file_names:
                        file_paths.append(os.path.join(dir_path, file_name))
            else:
                file_names = list(os.walk(file_dir))[0][2]

                for file_name in file_names:
                    file_paths.append(os.path.join(file_dir, file_name))

            self.main.wl_files.open_files(file_paths)

    def reopen(self):
        files = self.main.settings_custom['file_area']['files_closed'].pop()

        self.main.wl_files.open_files(list(dict.fromkeys([file['path_original'] for file in files])))

    def reload_selected(self):
        self.main.wl_files.reload_files(self.get_selected_rows())

    def reload_all(self):
        self.main.wl_files.reload_files(list(range(len(self.main.settings_custom['file_area']['files_open']))))

    def select_all(self):
        if self.model().item(0, 0):
            for i in range(self.model().rowCount()):
                if self.model().item(i, 0).checkState() == Qt.Unchecked:
                    self.model().item(i, 0).setCheckState(Qt.Checked)

    def deselect_all(self):
        if self.model().item(0, 0):
            for i in range(self.model().rowCount()):
                if self.model().item(i, 0).checkState() == Qt.Checked:
                    self.model().item(i, 0).setCheckState(Qt.Unchecked)

    def invert_selection(self):
        if self.model().item(0, 0):
            for i in range(self.model().rowCount()):
                if self.model().item(i, 0).checkState() == Qt.Checked:
                    self.model().item(i, 0).setCheckState(Qt.Unchecked)
                else:
                    self.model().item(i, 0).setCheckState(Qt.Checked)

    def close_selected(self):
        self.main.wl_files.close_files(self.get_selected_rows())

    def close_all(self):
        self.main.wl_files.close_files(list(range(len(self.main.settings_custom['file_area']['files_open']))))

class Wrapper_File_Area(wl_layouts.Wl_Wrapper_File_Area):
    def __init__(self, main):
        super().__init__(main)

        # Table
        self.table_files = Wl_Table_Files(self)

        self.wrapper_table.layout().addWidget(self.table_files, 0, 0)

        # Folder Settings
        self.group_box_folder_settings = QGroupBox(self.tr('Folder Settings'), self)

        self.checkbox_subfolders = QCheckBox(self.tr('Subfolders'), self)

        self.checkbox_subfolders.stateChanged.connect(self.folder_settings_changed)

        self.group_box_folder_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_folder_settings.layout().addWidget(self.checkbox_subfolders, 0, 0)

        # Auto-detection Settings
        self.group_box_auto_detection_settings = QGroupBox(self.tr('Auto-detection Settings'), self)

        self.checkbox_detect_langs = QCheckBox(self.tr('Detect languages'), self)
        self.checkbox_detect_encodings = QCheckBox(self.tr('Detect encodings'), self)

        self.checkbox_detect_langs.stateChanged.connect(self.auto_detection_settings_changed)
        self.checkbox_detect_encodings.stateChanged.connect(self.auto_detection_settings_changed)

        self.group_box_auto_detection_settings.setLayout(wl_layouts.Wl_Layout())
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
            settings = copy.deepcopy(self.main.settings_default['file_area'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['file_area'])

        self.checkbox_subfolders.setChecked(settings['folder_settings']['subfolders'])

        self.checkbox_detect_langs.setChecked(settings['auto_detection_settings']['detect_langs'])
        self.checkbox_detect_encodings.setChecked(settings['auto_detection_settings']['detect_encodings'])

        self.folder_settings_changed()
        self.auto_detection_settings_changed()

    def folder_settings_changed(self):
        settings = self.main.settings_custom['file_area']['folder_settings']

        settings['subfolders'] = self.checkbox_subfolders.isChecked()

    def auto_detection_settings_changed(self):
        settings = self.main.settings_custom['file_area']['auto_detection_settings']

        settings['detect_langs'] = self.checkbox_detect_langs.isChecked()
        settings['detect_encodings'] = self.checkbox_detect_encodings.isChecked()
