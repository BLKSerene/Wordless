#
# Wordless: Dialogs - Error
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_dialog
from wl_widgets import wl_label, wl_table

TABLE_ERROR_FILES_HEIGHT = 220

class Wl_Dialog_Error(wl_dialog.Wl_Dialog_Error):
    def __init__(self, main, title, width = 0, height = 0):
        super().__init__(main, title, width = 560, height = 320, no_buttons = True)

        self.button_export = QPushButton(self.tr('Export'), self)
        self.button_ok = QPushButton(self.tr('OK'), self)

        self.button_ok.clicked.connect(self.accept)

        self.wrapper_buttons.layout().addWidget(self.button_export, 0, 0, Qt.AlignLeft)
        self.wrapper_buttons.layout().addWidget(self.button_ok, 0, 1, Qt.AlignRight)

class Wl_Dialog_Error_File_Open(Wl_Dialog_Error):
    def __init__(self, main,
                 file_paths_missing,
                 file_paths_empty,
                 file_paths_unsupported,
                 file_paths_parsing_error):
        super().__init__(main, main.tr('Error Opening Files'))

        self.label_error = wl_label.Wl_Label_Dialog(
            self.tr('''
                <div>
                    An error occurred while opening files, so the following file(s) are skipped and will not be added to the file table.
                </div>
            '''),
            self
        )

        self.table_error_files = wl_table.Wl_Table_Error(
            self,
            headers = [
                self.tr('Error Type'),
                self.tr('File')
            ]
        )

        self.table_error_files.setFixedHeight(TABLE_ERROR_FILES_HEIGHT)
        self.table_error_files.setRowCount(0)

        self.button_export.clicked.connect(self.table_error_files.export_all)

        for file in file_paths_missing:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Missing File')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        for file in file_paths_empty:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Empty File')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        for file in file_paths_unsupported:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Unsupported File Type')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        for file in file_paths_parsing_error:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Parsing Error')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        self.wrapper_info.layout().addWidget(self.label_error, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_error_files, 1, 0)

def wl_dialog_error_file_open(
    main,
    file_paths_missing,
    file_paths_empty,
    file_paths_unsupported,
    file_paths_parsing_error
):
    if file_paths_missing or file_paths_empty or file_paths_unsupported or file_paths_parsing_error:
        dialog_error_file_open = Wl_Dialog_Error_File_Open(
            main,
            file_paths_missing,
            file_paths_empty,
            file_paths_unsupported,
            file_paths_parsing_error
        )

        dialog_error_file_open.open()

class Wl_Dialog_Error_File_Load_Colligation(Wl_Dialog_Error):
    def __init__(self, main, files_pos_tagging_unsupported):
        super().__init__(main, main.tr('Error Loading Files'))

        if files_pos_tagging_unsupported:
            self.label_error = wl_label.Wl_Label_Dialog(
                self.tr('''
                    <div>
                        The built-in POS taggers currently have no support for the following file(s), please check your language settings or provide copora that have already been POS-tagged.
                    </div>
                '''),
                self
            )

        self.table_error_files = wl_table.Wl_Table_Error(
            self,
            headers = [
                self.tr('Error Type'),
                self.tr('File')
            ]
        )

        self.table_error_files.setFixedHeight(TABLE_ERROR_FILES_HEIGHT)
        self.table_error_files.setRowCount(0)

        self.button_export.clicked.connect(self.table_error_files.export_all)

        for file in files_pos_tagging_unsupported:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('POS Tagging Unsupported')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        self.wrapper_info.layout().addWidget(self.label_error, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_error_files, 1, 0)

def wl_dialog_error_file_load_colligation(main, files_pos_tagging_unsupported):
    if files_pos_tagging_unsupported:
        dialog_error_file_load_colligation = Wl_Dialog_Error_File_Load_Colligation(
            main,
            files_pos_tagging_unsupported
        )

        dialog_error_file_load_colligation.open()

class Wl_Dialog_Error_Import(Wl_Dialog_Error):
    def __init__(self, main,
                 files_empty,
                 files_parsing_error):
        super().__init__(main, main.tr('Import Error'))

        self.label_error = wl_label.Wl_Label_Dialog(
            self.tr('''
                <div>
                    An error occurred during import, please check the following files and try again.
                </div>
            '''),
            self
        )

        self.table_error_files = wl_table.Wl_Table_Error(
            self,
            headers = [
                self.tr('Error Type'),
                self.tr('File')
            ]
        )

        self.table_error_files.setFixedHeight(TABLE_ERROR_FILES_HEIGHT)
        self.table_error_files.setRowCount(0)

        self.button_export.clicked.connect(self.table_error_files.export_all)

        for file in files_empty:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Empty File')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file['path']))

        for file in files_parsing_error:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Parsing Error')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file['path']))

        self.wrapper_info.layout().addWidget(self.label_error, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_error_files, 1, 0)

def wl_dialog_error_import(main,
                           files_empty,
                           files_parsing_error):
    if files_empty or files_parsing_error:
        dialog_error_import = Wl_Dialog_Error_Import(
            main,
            files_empty,
            files_parsing_error
        )

        dialog_error_import.open()

class Wl_Dialog_Error_Processing_Texts(Wl_Dialog_Error):
    def __init__(self, main, error_msg):
        super().__init__(main, main.tr('Error Processing Texts'))

        self.label_error_msg = wl_label.Wl_Label_Dialog(
            self.tr(f'''
                <div>An error occurred while processing the texts, please check your files or <b>contact the author for support</b> by emailing to {self.main.email_html}.</div>
            '''),
            self
        )
        self.text_edit_error_msg = QTextEdit(error_msg, self)

        self.text_edit_error_msg.setReadOnly(True)

        self.wrapper_info.layout().addWidget(self.label_error_msg, 0, 0)
        self.wrapper_info.layout().addWidget(self.text_edit_error_msg, 1, 0)

        self.button_export.hide()

def wl_dialog_error_processing_texts(main, error_msg):
    dialog_error_processing_texts = Wl_Dialog_Error_Processing_Texts(main, error_msg)

    dialog_error_processing_texts.open()
