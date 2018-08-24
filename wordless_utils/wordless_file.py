import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import chardet
import langdetect

class Wordless_File:
    def __init__(self, parent, table, file_path, auto_detect = True):
        self.parent = parent
        self.table = table

        if auto_detect:
            self.selected = True
            self.path = os.path.normpath(file_path)

            path_name, file = os.path.split(file_path)
            self.name, self.ext = os.path.splitext(file)
            self.ext_text = self.convert_ext(self.ext)

            with open(self.path, 'rb') as f:
                encoding_detected = chardet.detect(f.read())

                encoding_code = encoding_detected['encoding']
                encoding_lang = encoding_detected.get('language')
                # chardet
                if encoding_code == None:
                    self.encoding_code = 'UTF-8'
                elif encoding_code == 'EUC-TW':
                    self.encoding_code = 'Big5'
                elif encoding_code == 'ISO-2022-CN':
                    self.encoding_code = 'GB2312'
                else:
                    self.encoding_code = encoding_code.lower().replace('-', '_')
                self.encoding_text = self.convert_encoding(self.encoding_code, encoding_lang)

            try:
                with open(self.path, 'r', encoding = self.encoding_code) as f:
                    self.lang_code = langdetect.detect(f.read())
            except UnicodeDecodeError:
                self.lang_code = 'en'
                QMessageBox.warning(self.parent,
                                    'Auto-detection Failure',
                                    'Failed to auto-detect language and encoding for the file "{}", please choose the right language and encoding manually!'.format(self.name),
                                    QMessageBox.Ok)
            finally:
                self.lang_text = self.convert_lang(self.lang_code)

            if self.lang_code in ['ja', 'ko', 'zh-cn', 'zh-tw']:
                self.delimiter = ''
            else:
                self.delimiter = ' '

    def convert_lang(self, lang):
        # Text -> Code
        if lang[0].isupper():
            lang = self.parent.file_langs[lang]
        # Code -> Text
        else:
            for lang_text, lang_code in self.parent.file_langs.items():
                if lang_code == lang:
                    lang = lang_text

                    break

        return lang

    def convert_ext(self, ext):
        # Text -> Code
        return self.parent.file_exts[ext].split(' (')[0]

    def convert_encoding(self, encoding, lang = None):
        # Text -> Code
        if encoding.find('(') > -1:
            encoding = self.parent.file_encodings[encoding]
        # Code -> Text
        else:
            for encoding_text, encoding_code in self.parent.file_encodings.items():
                if encoding == encoding_code:
                    # Distinguish between different languages
                    if lang:
                        if encoding_text.find(lang) > -1:
                            encoding = encoding_text

                            break
                    else:
                        encoding = encoding_text

                        break

        return encoding

    def write(self, row):
        if row > self.table.rowCount() - 1:
            self.table.setRowCount(self.table.rowCount() + 1)

        checkbox_name     = QTableWidgetItem(self.name)
        combobox_lang     = QComboBox()
        combobox_encoding = QComboBox()

        if self.selected:
            checkbox_name.setCheckState(Qt.Checked)
        else:
            checkbox_name.setCheckState(Qt.Unchecked)

        combobox_lang.addItems(sorted(self.parent.file_langs))
        combobox_encoding.addItems(self.parent.file_encodings)

        combobox_lang.setCurrentIndex(combobox_lang.findText(self.lang_text))
        combobox_lang.setMaxVisibleItems(30)
        combobox_encoding.setCurrentIndex(combobox_encoding.findText(self.encoding_text))
        combobox_encoding.setMaxVisibleItems(30)

        combobox_lang.currentTextChanged.connect(lambda: self.table.itemChanged.emit(self.table.item(row, 2)))
        combobox_encoding.currentTextChanged.connect(lambda: self.table.itemChanged.emit(self.table.item(row, 3)))
        
        self.table.setItem(      row, 0, checkbox_name)
        self.table.setCellWidget(row, 1, combobox_lang)
        self.table.setItem(      row, 2, QTableWidgetItem(self.path))
        self.table.setItem(      row, 3, QTableWidgetItem(self.ext_text))
        self.table.setCellWidget(row, 4, combobox_encoding)
