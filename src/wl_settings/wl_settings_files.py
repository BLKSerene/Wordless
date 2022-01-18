# ----------------------------------------------------------------------
# Wordless: Settings - Files
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
import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_msg_boxes
from wl_utils import wl_conversion
from wl_widgets import wl_box, wl_label, wl_layout, wl_table, wl_tree, wl_widgets

class Wl_Settings_Files(wl_tree.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['files']
        self.settings_custom = self.main.settings_custom['files']

        # Default Settings
        group_box_default_settings = QGroupBox(self.tr('Default Settings'), self)

        self.label_files_lang = QLabel(self.tr('Language:'), self)
        self.combo_box_files_lang = wl_box.Wl_Combo_Box_Lang(self)
        self.label_files_tokenized = QLabel(self.tr('Tokenized:'), self)
        self.combo_box_files_tokenized = wl_box.Wl_Combo_Box_Yes_No(self)
        self.label_files_tagged = QLabel(self.tr('Tagged:'), self)
        self.combo_box_files_tagged = wl_box.Wl_Combo_Box_Yes_No(self)
        self.label_files_encoding = QLabel(self.tr('Encoding:'), self)
        self.combo_box_files_encoding = wl_box.Wl_Combo_Box_Encoding(self)

        group_box_default_settings.setLayout(wl_layout.Wl_Layout())
        group_box_default_settings.layout().addWidget(self.label_files_lang, 0, 0)
        group_box_default_settings.layout().addWidget(self.combo_box_files_lang, 0, 1)
        group_box_default_settings.layout().addWidget(self.label_files_tokenized, 1, 0)
        group_box_default_settings.layout().addWidget(self.combo_box_files_tokenized, 1, 1)
        group_box_default_settings.layout().addWidget(self.label_files_tagged, 2, 0)
        group_box_default_settings.layout().addWidget(self.combo_box_files_tagged, 2, 1)
        group_box_default_settings.layout().addWidget(self.label_files_encoding, 3, 0)
        group_box_default_settings.layout().addWidget(self.combo_box_files_encoding, 3, 1)

        group_box_default_settings.layout().setColumnStretch(3, 1)

        # Detection Settings
        group_box_auto_detection_settings = QGroupBox(self.tr('Auto-detection Settings'), self)

        self.label_files_number_lines = QLabel(self.tr('Number of lines to scan in each file:'), self)
        (self.spin_box_files_number_lines,
         self.checkbox_files_number_lines_no_limit) = wl_widgets.wl_widgets_no_limit(self)

        self.spin_box_files_number_lines.setRange(1, 1000000)

        group_box_auto_detection_settings.setLayout(wl_layout.Wl_Layout())
        group_box_auto_detection_settings.layout().addWidget(self.label_files_number_lines, 0, 0)
        group_box_auto_detection_settings.layout().addWidget(self.spin_box_files_number_lines, 0, 1)
        group_box_auto_detection_settings.layout().addWidget(self.checkbox_files_number_lines_no_limit, 0, 2)

        group_box_auto_detection_settings.layout().setColumnStretch(3, 1)

        # Miscellaneous
        group_box_misc = QGroupBox(self.tr('Miscellaneous'), self)

        self.label_read_files_in_chunks = QLabel(self.tr('Read files in chunks of'), self)
        self.spin_box_read_files_in_chunks = wl_box.Wl_Spin_Box(self)
        self.label_read_files_in_chunks_lines = QLabel(self.tr('lines'), self)

        self.spin_box_read_files_in_chunks.setRange(1, 10000)

        group_box_misc.setLayout(wl_layout.Wl_Layout())
        group_box_misc.layout().addWidget(self.label_read_files_in_chunks, 0, 0)
        group_box_misc.layout().addWidget(self.spin_box_read_files_in_chunks, 0, 1)
        group_box_misc.layout().addWidget(self.label_read_files_in_chunks_lines, 0, 2)

        group_box_auto_detection_settings.layout().setColumnStretch(3, 1)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(group_box_default_settings, 0, 0)
        self.layout().addWidget(group_box_auto_detection_settings, 1, 0)
        self.layout().addWidget(group_box_misc, 2, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(3, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Default Settings
        self.combo_box_files_lang.setCurrentText(wl_conversion.to_lang_text(self.main, settings['default_settings']['lang']))
        self.combo_box_files_tokenized.setCurrentText(settings['default_settings']['tokenized'])
        self.combo_box_files_tagged.setCurrentText(settings['default_settings']['tagged'])
        self.combo_box_files_encoding.setCurrentText(wl_conversion.to_encoding_text(self.main, settings['default_settings']['encoding']))

        # Auto-detection Settings
        self.spin_box_files_number_lines.setValue(settings['auto_detection_settings']['number_lines'])
        self.checkbox_files_number_lines_no_limit.setChecked(settings['auto_detection_settings']['number_lines_no_limit'])

        # Miscellaneous
        self.spin_box_read_files_in_chunks.setValue(settings['misc']['read_files_in_chunks'])

    def apply_settings(self):
        # Default Settings
        self.settings_custom['default_settings']['lang'] = wl_conversion.to_lang_code(self.main, self.combo_box_files_lang.currentText())
        self.settings_custom['default_settings']['tokenized'] = self.combo_box_files_tokenized.currentText()
        self.settings_custom['default_settings']['tagged'] = self.combo_box_files_tagged.currentText()
        self.settings_custom['default_settings']['encoding'] = wl_conversion.to_encoding_code(self.main, self.combo_box_files_encoding.currentText())

        # Auto-detection Settings
        self.settings_custom['auto_detection_settings']['number_lines'] = self.spin_box_files_number_lines.value()
        self.settings_custom['auto_detection_settings']['number_lines_no_limit'] = self.checkbox_files_number_lines_no_limit.isChecked()

        # Miscellaneous
        self.settings_custom['misc']['read_files_in_chunks'] = self.spin_box_read_files_in_chunks.value()

        return True

class Wl_Table_Tags(wl_table.Wl_Table):
    def __init__(self, main):
        super().__init__(
            main,
            headers = [
                main.tr('Type'),
                main.tr('Level'),
                main.tr('Opening Tag'),
                main.tr('Closing Tag'),
                main.tr('Preview')
            ],
            header_orientation = 'horizontal',
            drag_drop_enabled = True
        )

        self.verticalHeader().setHidden(True)
        self.setFixedHeight(125)

        self.itemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self.selection_changed)

        self.button_add = QPushButton(self.tr('Add'), self)
        self.button_insert = QPushButton(self.tr('Insert'), self)
        self.button_remove = QPushButton(self.tr('Remove'), self)
        self.button_clear = QPushButton(self.tr('Clear'), self)
        self.button_reset = QPushButton(self.tr('Reset'), self)

        self.button_add.clicked.connect(self.add_item)
        self.button_insert.clicked.connect(self.insert_item)
        self.button_remove.clicked.connect(self.remove_item)
        self.button_clear.clicked.connect(lambda: self.clear_table(0))
        self.button_reset.clicked.connect(self.reset_table)

        self.reset_table()

    def item_changed(self, item = None):
        self.blockSignals(True)

        for row in range(self.rowCount()):
            opening_tag_widget = self.cellWidget(row, 2)

            # Opening Tag
            if re.search(r'^\s*$', opening_tag_widget.text()):
                wl_msg_boxes.Wl_Msg_Box_Warning(
                    self.main,
                    title = self.tr('Empty Opening Tag'),
                    text = self.tr(f'''
                        <div>The opening tag should not be left empty!</div>
                    ''')
                ).open()

                opening_tag_widget.setText(opening_tag_widget.text_old)
                opening_tag_widget.setFocus()

                self.blockSignals(False)

                return

        # Check for duplicate tags
        if item:
            item_row = item.row()
            item_col = item.column()

            if item_col == 2:
                item_widget = self.cellWidget(item_row, 2)

                for row in range(self.rowCount()):
                    if row != item_row:
                        if self.cellWidget(row, 2).text() == item_widget.text():
                            wl_msg_boxes.Wl_Msg_Box_Warning(
                                self.main,
                                title = self.tr('Duplicate Tags'),
                                text = self.tr(f'''
                                    <div>The tag that you have specified already exists in the table!</div>
                                ''')
                            ).open()

                            item_widget.setText(item_widget.text_old)
                            item_widget.setFocus()

                            self.blockSignals(False)

                            return

        for row in range(self.rowCount()):
            type_text = self.cellWidget(row, 0).currentText()
            opening_tag_text = self.cellWidget(row, 2).text()
            closing_tag = self.item(row, 3)
            preview = self.item(row, 4)

            # Closing Tag
            if type_text == self.tr('Embedded'):
                closing_tag.setText(self.tr('N/A'))
            elif type_text == self.tr('Non-embedded'):
                # Add a "/" before the first non-punctuation character
                re_non_punc = re.search(r'\w|\*', opening_tag_text)

                if re_non_punc:
                    i_non_punc = re_non_punc.start()
                else:
                    i_non_punc = 1

                closing_tag.setText(f'{opening_tag_text[:i_non_punc]}/{opening_tag_text[i_non_punc:]}')

            # Preview
            if type_text == self.tr('Embedded'):
                preview.setText(self.tr(f'token{opening_tag_text}TAG'))
            elif type_text == self.tr('Non-embedded'):
                preview.setText(self.tr(f'{opening_tag_text}token{self.item(row, 3).text()}'))

        self.blockSignals(False)

        if self.rowCount():
            self.button_remove.setEnabled(True)
            self.button_clear.setEnabled(True)
        else:
            self.button_remove.setEnabled(False)
            self.button_clear.setEnabled(False)

        self.selection_changed()

    def selection_changed(self):
        if self.selectedIndexes():
            self.button_insert.setEnabled(True)

            if self.rowCount():
                self.button_remove.setEnabled(True)
            else:
                self.button_remove.setEnabled(False)
        else:
            self.button_insert.setEnabled(False)
            self.button_remove.setEnabled(False)

    def _new_item_type(self):
        new_item_type = wl_box.Wl_Combo_Box(self)

        new_item_type.addItems([
            self.tr('Embedded'),
            self.tr('Non-embedded')
        ])

        return new_item_type

    def _new_item_level(self):
        pass

    def _new_item_opening_tag(self, item_row):
        i = 1

        # Check for duplicate tag names if there are more than 1 row after the new row is added to the table
        dup = True

        while dup:
            if self.rowCount() > 1:
                for j in range(self.rowCount()):
                    if j != item_row and self.cellWidget(j, 2).text() == f'Tag_{i}':
                        i += 1

                        break
                    elif j == self.rowCount() - 1:
                        dup = False
            else:
                dup = False

        new_item = QLineEdit(f'Tag_{i}')
        new_item.text_old = new_item.text()
        
        return new_item

    def add_item(self, texts = []):
        self.blockSignals(True)

        self.setRowCount(self.rowCount() + 1)

        row = self.rowCount() - 1
        
        self.setCellWidget(row, 0, self._new_item_type())
        self.setCellWidget(row, 1, self._new_item_level())
        self.setCellWidget(row, 2, self._new_item_opening_tag(row))
        self.setItem(row, 0, QTableWidgetItem())
        self.setItem(row, 1, QTableWidgetItem())
        self.setItem(row, 2, QTableWidgetItem())

        self.setItem(row, 3, QTableWidgetItem())
        self.setItem(row, 4, QTableWidgetItem())

        if texts:
            self.cellWidget(row, 0).setCurrentText(texts[0])
            self.cellWidget(row, 1).setCurrentText(texts[1])
            self.cellWidget(row, 2).setText(texts[2])
            self.cellWidget(row, 2).text_old = texts[2]

        self.cellWidget(row, 0).currentTextChanged.connect(lambda: self.item_changed(item = self.item(row, 0)))
        self.cellWidget(row, 1).currentTextChanged.connect(lambda: self.item_changed(item = self.item(row, 1)))
        self.cellWidget(row, 2).editingFinished.connect(lambda: self.item_changed(item = self.item(row, 2)))

        self.blockSignals(False)

        self.item_changed()

    def insert_item(self):
        self.blockSignals(True)

        row = self.selectedIndexes()[0].row()

        self.insertRow(row)

        self.setCellWidget(row, 0, self._new_item_type())
        self.setCellWidget(row, 1, self._new_item_level())
        self.setCellWidget(row, 2, self._new_item_opening_tag(row))
        self.setItem(row, 0, QTableWidgetItem())
        self.setItem(row, 1, QTableWidgetItem())
        self.setItem(row, 2, QTableWidgetItem())

        self.setItem(row, 3, QTableWidgetItem())
        self.setItem(row, 4, QTableWidgetItem())

        self.cellWidget(row, 0).currentTextChanged.connect(lambda: self.item_changed(item = self.item(row, 0)))
        self.cellWidget(row, 1).currentTextChanged.connect(lambda: self.item_changed(item = self.item(row, 1)))
        self.cellWidget(row, 2).editingFinished.connect(lambda: self.item_changed(item = self.item(row, 2)))

        self.blockSignals(False)

        self.item_changed()

    def remove_item(self):
        self.blockSignals(True)

        for i in reversed(self.get_selected_rows()):
            self.removeRow(i)

        self.blockSignals(False)

        self.item_changed()

    def reset_table(self):
        pass

    def get_tags(self):
        tags = []

        for row in range(self.rowCount()):
            tags.append([
                self.cellWidget(row, 0).currentText(),
                self.cellWidget(row, 1).currentText(),
                self.cellWidget(row, 2).text(),
                self.item(row, 3).text()
            ])

            self.cellWidget(row, 2).text_old = self.cellWidget(row, 2).text()

        return tags

class Wl_Table_Tags_Header(Wl_Table_Tags):
    def _new_item_level(self, text = None):
        new_item_level = wl_box.Wl_Combo_Box(self)

        new_item_level.addItems([
            self.tr('Header')
        ])

        if text:
            new_item_level.setCurrentText(text)

        return new_item_level

    def reset_table(self):
        self.clear_table(0)

        for tags in self.main.settings_default['tags']['tags_header']:
            self.add_item(texts = tags)

class Wl_Table_Tags_Body(Wl_Table_Tags):
    def _new_item_level(self, text = None):
        new_item_level = wl_box.Wl_Combo_Box(self)

        new_item_level.addItems([
            self.tr('Part of Speech'),
            self.tr('Others')
        ])

        if text:
            new_item_level.setCurrentText(text)

        return new_item_level

    def reset_table(self):
        self.clear_table(0)

        for tags in self.main.settings_default['tags']['tags_body']:
            self.add_item(texts = tags)

class Wl_Table_Tags_Xml(Wl_Table_Tags):
    def _new_item_level(self, text = None):
        new_item_level = wl_box.Wl_Combo_Box(self)

        new_item_level.addItems([
            self.tr('Paragraph'),
            self.tr('Sentence'),
            self.tr('Word')
        ])

        if text:
            new_item_level.setCurrentText(text)

        return new_item_level

    def item_changed(self, item = None):
        self.blockSignals(True)

        for row in range(self.rowCount()):
            opening_tag_widget = self.cellWidget(row, 2)
            opening_tag_text = opening_tag_widget.text()

            # Check if the XML tags are valid
            if opening_tag_text and not re.search(r'^\<[^<>/\s]+?\>$', opening_tag_text):
                wl_msg_boxes.Wl_Msg_Box_Warning(
                    self.main,
                    title = self.tr('Invalid XML Tag'),
                    text = self.tr(f'''
                        <div>The specified XML tag is invalid!</div>
                    ''')
                ).open()

                opening_tag_widget.setText(opening_tag_widget.text_old)
                opening_tag_widget.setFocus()

                self.blockSignals(False)

                return

        self.blockSignals(False)

        super().item_changed(item = item)

    def reset_table(self):
        self.clear_table(0)

        for tags in self.main.settings_default['tags']['tags_xml']:
            self.add_item(texts = tags)

class Wl_Settings_Tags(wl_tree.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['tags']
        self.settings_custom = self.main.settings_custom['tags']

        # Header Tag Settings
        group_box_header_tag_settings = QGroupBox(self.tr('Header Tag Settings'), self)

        self.table_tags_header = Wl_Table_Tags_Header(self)
        self.label_tags_header = wl_label.Wl_Label_Important(self.tr('Note: All contents surrounded by header tags will be discarded during text processing!'), self)

        group_box_header_tag_settings.setLayout(wl_layout.Wl_Layout())
        group_box_header_tag_settings.layout().addWidget(self.table_tags_header, 0, 0, 1, 5)
        group_box_header_tag_settings.layout().addWidget(self.table_tags_header.button_add, 1, 0)
        group_box_header_tag_settings.layout().addWidget(self.table_tags_header.button_insert, 1, 1)
        group_box_header_tag_settings.layout().addWidget(self.table_tags_header.button_remove, 1, 2)
        group_box_header_tag_settings.layout().addWidget(self.table_tags_header.button_clear, 1, 3)
        group_box_header_tag_settings.layout().addWidget(self.table_tags_header.button_reset, 1, 4)
        group_box_header_tag_settings.layout().addWidget(self.label_tags_header, 2, 0, 1, 5)

        group_box_header_tag_settings.layout().setRowStretch(3, 1)

        # Body Tag Settings
        group_box_body_tag_settings = QGroupBox(self.tr('Body Tag Settings'), self)

        self.table_tags_body = Wl_Table_Tags_Body(self)
        self.label_tags_body = wl_label.Wl_Label_Hint(self.tr('Use * to indicate any number of characters'), self)

        group_box_body_tag_settings.setLayout(wl_layout.Wl_Layout())
        group_box_body_tag_settings.layout().addWidget(self.table_tags_body, 0, 0, 1, 5)
        group_box_body_tag_settings.layout().addWidget(self.table_tags_body.button_add, 1, 0)
        group_box_body_tag_settings.layout().addWidget(self.table_tags_body.button_insert, 1, 1)
        group_box_body_tag_settings.layout().addWidget(self.table_tags_body.button_remove, 1, 2)
        group_box_body_tag_settings.layout().addWidget(self.table_tags_body.button_clear, 1, 3)
        group_box_body_tag_settings.layout().addWidget(self.table_tags_body.button_reset, 1, 4)
        group_box_body_tag_settings.layout().addWidget(self.label_tags_body, 2, 0, 1, 5)

        group_box_body_tag_settings.layout().setRowStretch(3, 1)

        # XML Tag Settings
        group_box_xml_tag_settings = QGroupBox(self.tr('XML Tag Settings'), self)

        self.table_tags_xml = Wl_Table_Tags_Xml(self)

        group_box_xml_tag_settings.setLayout(wl_layout.Wl_Layout())
        group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml, 0, 0, 1, 5)
        group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml.button_add, 1, 0)
        group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml.button_insert, 1, 1)
        group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml.button_remove, 1, 2)
        group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml.button_clear, 1, 3)
        group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml.button_reset, 1, 4)

        group_box_xml_tag_settings.layout().setRowStretch(2, 1)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(group_box_header_tag_settings, 0, 0)
        self.layout().addWidget(group_box_body_tag_settings, 1, 0)
        self.layout().addWidget(group_box_xml_tag_settings, 2, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(3, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        self.table_tags_header.clear_table(0)
        self.table_tags_body.clear_table(0)
        self.table_tags_xml.clear_table(0)

        for tags in settings['tags_header']:
            self.table_tags_header.add_item(texts = tags)

        for tags in settings['tags_body']:
            self.table_tags_body.add_item(texts = tags)

        for tags in settings['tags_xml']:
            self.table_tags_xml.add_item(texts = tags)

    def apply_settings(self):
        self.settings_custom['tags_header'] = self.table_tags_header.get_tags()
        self.settings_custom['tags_body'] = self.table_tags_body.get_tags()
        self.settings_custom['tags_xml'] = self.table_tags_xml.get_tags()

        return True
