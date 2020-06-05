#
# Wordless: Dialogs - Error
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_dialogs import wordless_dialog
from wordless_widgets import wordless_label, wordless_table

DIALOG_ERROR_WIDTH = 560
DIALOG_ERROR_HEIGHT = 320
DIALOG_ERROR_HEIGHT_COLLIGATION = 360
TABLE_ERROR_FILES_HEIGHT = 220

class Wordless_Dialog_Error(wordless_dialog.Wordless_Dialog_Error):
    def __init__(self, main, title, width = 0, height = 0):
        super().__init__(main, title, width, height, no_button = True)

        self.button_export = QPushButton(self.tr('Export'), self)
        self.button_ok = QPushButton(self.tr('OK'), self)

        self.button_ok.clicked.connect(self.accept)

        self.wrapper_buttons.layout().addWidget(self.button_export, 0, 0, Qt.AlignLeft)
        self.wrapper_buttons.layout().addWidget(self.button_ok, 0, 1, Qt.AlignRight)

class Wordless_Dialog_Error_File_Open(Wordless_Dialog_Error):
    def __init__(self, main,
                 files_duplicate,
                 files_empty,
                 files_unsupported,
                 files_parsing_error):
        super().__init__(main, main.tr('Error Opening File'),
                         width = DIALOG_ERROR_WIDTH)

        self.label_error = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    An error occurred while opening the files, so the following files are skipped and will not be added to the file area.
                </div>
            '''),
            self
        )

        self.table_error_files = wordless_table.Wordless_Table_Error(self,
                                                                     headers = [
                                                                         self.tr('Error Types'),
                                                                         self.tr('Files')
                                                                     ])

        self.table_error_files.setFixedHeight(TABLE_ERROR_FILES_HEIGHT)
        self.table_error_files.setRowCount(0)

        self.button_export.clicked.connect(self.table_error_files.export_all)

        for file in files_duplicate:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Duplicate File')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        for file in files_empty:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Empty File')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        for file in files_unsupported:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Unsupported File Type')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        for file in files_parsing_error:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Parsing Error')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        self.wrapper_info.layout().addWidget(self.label_error, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_error_files, 1, 0)

def wordless_dialog_error_file_open(main,
                                    files_duplicate,
                                    files_empty,
                                    files_unsupported,
                                    files_parsing_error):
    if files_duplicate or files_empty or files_unsupported or files_parsing_error:
        dialog_error_file_open = Wordless_Dialog_Error_File_Open(main,
                                                                 files_duplicate,
                                                                 files_empty,
                                                                 files_unsupported,
                                                                 files_parsing_error)

        dialog_error_file_open.open()

class Wordless_Dialog_Error_File_Load(Wordless_Dialog_Error):
    def __init__(self, main,
                 files_missing,
                 files_empty,
                 files_decoding_error):
        super().__init__(main, main.tr('Error Loading File'),
                         width = DIALOG_ERROR_WIDTH,
                         height = DIALOG_ERROR_HEIGHT)

        self.label_error = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    An error occurred while loading the following files. Please check the files and/or your settings and try again.
                </div>
            '''),
            self
        )

        self.table_error_files = wordless_table.Wordless_Table_Error(self,
                                                                     headers = [
                                                                         self.tr('Error Types'),
                                                                         self.tr('Files')
                                                                     ])

        self.table_error_files.setFixedHeight(TABLE_ERROR_FILES_HEIGHT)
        self.table_error_files.setRowCount(0)

        self.button_export.clicked.connect(self.table_error_files.export_all)

        for file in files_missing:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Missing File')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        for file in files_empty:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Empty File')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        for file in files_decoding_error:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Decoding Error')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        self.wrapper_info.layout().addWidget(self.label_error, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_error_files, 1, 0)

def wordless_dialog_error_file_load(main,
                                    files_missing,
                                    files_empty,
                                    files_decoding_error):
    if files_missing or files_empty or files_decoding_error:
        dialog_error_file_load = Wordless_Dialog_Error_File_Load(main,
                                                                 files_missing,
                                                                 files_empty,
                                                                 files_decoding_error)

        dialog_error_file_load.open()

class Wordless_Dialog_Error_File_Load_Colligation(Wordless_Dialog_Error):
    def __init__(self, main,
                 files_missing,
                 files_empty,
                 files_decoding_error,
                 files_pos_tagging_not_supported):
        if files_pos_tagging_not_supported:
            super().__init__(main, main.tr('Error Loading Files'),
                         width = DIALOG_ERROR_WIDTH,
                         height = DIALOG_ERROR_HEIGHT_COLLIGATION)
        else:
            super().__init__(main, main.tr('Error Loading Files'),
                         width = DIALOG_ERROR_WIDTH,
                         height = DIALOG_ERROR_HEIGHT)

        if files_pos_tagging_not_supported:
            self.label_error = wordless_label.Wordless_Label_Dialog(
                self.tr('''
                    <div>
                        An error occurred while loading the following files. Please check the files and/or your settings and try again.
                    </div>
                    <div>
                        The built-in POS taggers currently have no support for some of the following files, please check your language settings or provide files that have already been POS-tagged.
                    </div>
                '''),
                self
            )
        else:
            self.label_error = wordless_label.Wordless_Label_Dialog(
                self.tr('''
                    <div>
                        An error occurred while loading the following files. Please check the files and/or your settings and try again.
                    </div>
                '''),
                self
            )

        self.table_error_files = wordless_table.Wordless_Table_Error(self,
                                                                     headers = [
                                                                         self.tr('Error Types'),
                                                                         self.tr('Files')
                                                                     ])

        self.table_error_files.setFixedHeight(TABLE_ERROR_FILES_HEIGHT)
        self.table_error_files.setRowCount(0)

        self.button_export.clicked.connect(self.table_error_files.export_all)

        for file in files_missing:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Missing File')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        for file in files_empty:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Empty File')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        for file in files_decoding_error:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Decoding Error')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        for file in files_pos_tagging_not_supported:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('POS Tagging Not Supported')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        self.wrapper_info.layout().addWidget(self.label_error, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_error_files, 1, 0)

def wordless_dialog_error_file_load_colligation(main,
                                                files_missing,
                                                files_empty,
                                                files_decoding_error,
                                                files_pos_tagging_not_supported):
    if files_missing or files_empty or files_decoding_error or files_pos_tagging_not_supported:
        dialog_error_file_load_colligation = Wordless_Dialog_Error_File_Load_Colligation(main,
                                                                                         files_missing,
                                                                                         files_empty,
                                                                                         files_decoding_error,
                                                                                         files_pos_tagging_not_supported)

        dialog_error_file_load_colligation.open()

class Wordless_Dialog_Error_Detection(Wordless_Dialog_Error):
    def __init__(self, main,
                 files_detection_error_encoding,
                 files_detection_error_text_type,
                 files_detection_error_lang):
        super().__init__(main, main.tr('Detection Error'),
                         width = DIALOG_ERROR_WIDTH,
                         height = DIALOG_ERROR_HEIGHT)

        self.label_error = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    An error occurred during auto-detection. Please set the settings of the following files manually.
                </div>
            '''),
            self
        )

        self.table_error_files = wordless_table.Wordless_Table_Error(self,
                                                                     headers = [
                                                                         self.tr('Error Types'),
                                                                         self.tr('Files')
                                                                     ])

        self.table_error_files.setFixedHeight(TABLE_ERROR_FILES_HEIGHT)
        self.table_error_files.setRowCount(0)

        self.button_export.clicked.connect(self.table_error_files.export_all)

        for file in files_detection_error_encoding:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Encoding Detection')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        for file in files_detection_error_text_type:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Text Type Detection')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        for file in files_detection_error_lang:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Language Detection')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        self.wrapper_info.layout().addWidget(self.label_error, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_error_files, 1, 0)

def wordless_dialog_error_detection(main,
                                    files_detection_error_encoding,
                                    files_detection_error_text_type,
                                    files_detection_error_lang):
    if files_detection_error_encoding or files_detection_error_text_type or files_detection_error_lang:
        dialog_error_detection = Wordless_Dialog_Error_Detection(main,
                                                                 files_detection_error_encoding,
                                                                 files_detection_error_text_type,
                                                                 files_detection_error_lang)

        dialog_error_detection.open()

class Wordless_Dialog_Error_Import(Wordless_Dialog_Error):
    def __init__(self, main,
                 files_empty,
                 files_decoding_error):
        super().__init__(main, main.tr('Import Error'),
                         width = DIALOG_ERROR_WIDTH,
                         height = DIALOG_ERROR_HEIGHT)

        self.label_error = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    An error occurred during import, please check the following files and try again.
                </div>
            '''),
            self
        )

        self.table_error_files = wordless_table.Wordless_Table_Error(self,
                                                                     headers = [
                                                                         self.tr('Error Types'),
                                                                         self.tr('Files')
                                                                     ])

        self.table_error_files.setFixedHeight(TABLE_ERROR_FILES_HEIGHT)
        self.table_error_files.setRowCount(0)

        self.button_export.clicked.connect(self.table_error_files.export_all)

        for file in files_empty:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Empty File')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        for file in files_decoding_error:
            self.table_error_files.setRowCount(self.table_error_files.rowCount() + 1)

            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 0, QTableWidgetItem(self.tr('Decoding Error')))
            self.table_error_files.setItem(self.table_error_files.rowCount() - 1, 1, QTableWidgetItem(file))

        self.wrapper_info.layout().addWidget(self.label_error, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_error_files, 1, 0)

def wordless_dialog_error_import(main,
                                 files_empty,
                                 files_decoding_error):
    if files_empty or files_decoding_error:
        dialog_error_import = Wordless_Dialog_Error_Import(main,
                                                           files_empty,
                                                           files_decoding_error)

        dialog_error_import.open()
