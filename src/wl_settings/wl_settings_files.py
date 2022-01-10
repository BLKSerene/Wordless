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

from wl_dialogs import wl_msg_box
from wl_utils import wl_conversion
from wl_widgets import (wl_box, wl_label, wl_layout, wl_table, wl_tree,
                        wl_widgets)

class Wl_Table_Tags_Header(wl_table.Wl_Table_Tags):
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

class Wl_Table_Tags_Body(wl_table.Wl_Table_Tags):
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

class Wl_Table_Tags_Xml(wl_table.Wl_Table_Tags):
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
                wl_msg_box.wl_msg_box_invalid_xml_tag(self.main)

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
