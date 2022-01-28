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

from wl_checking import wl_checking_misc
from wl_dialogs import wl_msg_boxes
from wl_settings import wl_settings
from wl_utils import wl_conversion
from wl_widgets import wl_boxes, wl_labels, wl_layouts, wl_tables, wl_widgets

class Wl_Settings_Files(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['files']
        self.settings_custom = self.main.settings_custom['files']

        # Default Settings
        group_box_default_settings = QGroupBox(self.tr('Default Settings'), self)

        self.label_files_lang = QLabel(self.tr('Language:'), self)
        self.combo_box_files_lang = wl_boxes.Wl_Combo_Box_Lang(self)
        self.label_files_tokenized = QLabel(self.tr('Tokenized:'), self)
        self.combo_box_files_tokenized = wl_boxes.Wl_Combo_Box_Yes_No(self)
        self.label_files_tagged = QLabel(self.tr('Tagged:'), self)
        self.combo_box_files_tagged = wl_boxes.Wl_Combo_Box_Yes_No(self)
        self.label_files_encoding = QLabel(self.tr('Encoding:'), self)
        self.combo_box_files_encoding = wl_boxes.Wl_Combo_Box_Encoding(self)

        group_box_default_settings.setLayout(wl_layouts.Wl_Layout())
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

        group_box_auto_detection_settings.setLayout(wl_layouts.Wl_Layout())
        group_box_auto_detection_settings.layout().addWidget(self.label_files_number_lines, 0, 0)
        group_box_auto_detection_settings.layout().addWidget(self.spin_box_files_number_lines, 0, 1)
        group_box_auto_detection_settings.layout().addWidget(self.checkbox_files_number_lines_no_limit, 0, 2)

        group_box_auto_detection_settings.layout().setColumnStretch(3, 1)

        # Miscellaneous
        group_box_misc = QGroupBox(self.tr('Miscellaneous'), self)

        self.label_read_files_in_chunks = QLabel(self.tr('Read files in chunks of'), self)
        self.spin_box_read_files_in_chunks = wl_boxes.Wl_Spin_Box(self)
        self.label_read_files_in_chunks_lines = QLabel(self.tr('lines'), self)

        self.spin_box_read_files_in_chunks.setRange(1, 10000)

        group_box_misc.setLayout(wl_layouts.Wl_Layout())
        group_box_misc.layout().addWidget(self.label_read_files_in_chunks, 0, 0)
        group_box_misc.layout().addWidget(self.spin_box_read_files_in_chunks, 0, 1)
        group_box_misc.layout().addWidget(self.label_read_files_in_chunks_lines, 0, 2)

        group_box_auto_detection_settings.layout().setColumnStretch(3, 1)

        self.setLayout(wl_layouts.Wl_Layout())
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

class Wl_Table_Tags(wl_tables.Wl_Table):
    def __init__(self, parent, settings_tags, default_type, default_level):
        super().__init__(
            parent,
            headers = [
                parent.tr('Type'),
                parent.tr('Level'),
                parent.tr('Opening Tag'),
                parent.tr('Closing Tag'),
                parent.tr('Preview')
            ],
            header_orientation = 'horizontal',
            editable = True,
            drag_drop = True
        )

        self.settings_tags = settings_tags
        self.default_type = default_type
        self.default_level = default_level

        self.verticalHeader().setHidden(True)
        self.setFixedHeight(125)

        self.setItemDelegateForColumn(0, wl_boxes.Wl_Item_Delegate_Combo_Box(
            parent = self,
            items = [
                self.tr('Embedded'),
                self.tr('Non-embedded')
            ]
        ))
        self.setItemDelegateForColumn(3, wl_tables.Wl_Item_Delegate_Uneditable(self))
        self.setItemDelegateForColumn(4, wl_tables.Wl_Item_Delegate_Uneditable(self))

        self.model().itemChanged.connect(self.item_changed)
        self.selectionModel().selectionChanged.connect(self.selection_changed)

        self.button_add = QPushButton(self.tr('Add'), self)
        self.button_ins = QPushButton(self.tr('Insert'), self)
        self.button_del = QPushButton(self.tr('Remove'), self)
        self.button_clr = QPushButton(self.tr('Clear'), self)
        self.button_reset = QPushButton(self.tr('Reset'), self)

        self.button_add.clicked.connect(self.add_row)
        self.button_ins.clicked.connect(self.ins_row)
        self.button_del.clicked.connect(self.del_row)
        self.button_clr.clicked.connect(lambda: self.clr_table(0))
        self.button_reset.clicked.connect(self.reset_table)

        self.reset_table()

    def item_changed(self, item):
        super().item_changed(item)

        if not self.is_empty():
            for row in range(self.model().rowCount()):
                item_opening_tag = self.model().item(row, 2)

                # Opening Tag
                if re.search(r'^\s*$', item_opening_tag.text()):
                    wl_msg_boxes.Wl_Msg_Box_Warning(
                        self.main,
                        title = self.tr('Empty Opening Tag'),
                        text = self.tr('''
                            <div>The opening tag should not be left empty!</div>
                        ''')
                    ).exec_()

                    item_opening_tag.setText(item_opening_tag.text_old)

                    self.closePersistentEditor(item_opening_tag.index())
                    self.edit(item_opening_tag.index())

                    return

            # Check for duplicate tags
            if item.column() == 2:
                for row in range(self.model().rowCount()):
                    if row != item.row() and self.model().item(row, 2).text() == item.text():
                        wl_msg_boxes.Wl_Msg_Box_Warning(
                            self.main,
                            title = self.tr('Duplicate Tags'),
                            text = self.tr('''
                                <div>The tag that you have specified already exists in the table!</div>
                            ''')
                        ).exec_()

                        item.setText(item.text_old)

                        self.closePersistentEditor(item.index())
                        self.edit(item.index())

                        break

                item.text_old = item.text()

            if item.column() in [0, 1, 2]:
                self.disable_updates()

                for row in range(self.model().rowCount()):
                    type_text = self.model().item(row, 0).text()
                    opening_tag_text = self.model().item(row, 2).text()
                    closing_tag = self.model().item(row, 3)
                    preview = self.model().item(row, 4)

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
                        preview.setText(self.tr(f'{opening_tag_text}token{self.model().item(row, 3).text()}'))

                self.enable_updates()

        if self.model().rowCount():
            self.button_del.setEnabled(True)
            self.button_clr.setEnabled(True)
        else:
            self.button_del.setEnabled(False)
            self.button_clr.setEnabled(False)

        self.selection_changed()

    def selection_changed(self):
        if self.selectionModel().selectedIndexes():
            self.button_ins.setEnabled(True)

            if self.model().rowCount():
                self.button_del.setEnabled(True)
            else:
                self.button_del.setEnabled(False)
        else:
            self.button_ins.setEnabled(False)
            self.button_del.setEnabled(False)

    def _add_row(self, row = None, type_ = '', level = '', opening_tag = ''):
        if not type_:
            type_ = self.default_type
        if not level:
            level = self.default_level
        if not opening_tag:
            opening_tags = [self.model().item(i, 2).text() for i in range(self.model().rowCount())]
            opening_tag = wl_checking_misc.check_new_name(self.tr('Tag'), opening_tags)

        item_opening_tag = QStandardItem(opening_tag)
        item_opening_tag.text_old = opening_tag

        if row is None:
            self.model().appendRow([
                QStandardItem(type_),
                QStandardItem(level),
                item_opening_tag,
                QStandardItem(),
                QStandardItem()
            ])
        else:
            self.model().insertRow(row, [
                QStandardItem(type_),
                QStandardItem(level),
                item_opening_tag,
                QStandardItem(),
                QStandardItem()
            ])

        self.model().itemChanged.emit(item_opening_tag)

    def add_row(self, type_ = '', level = '', opening_tag = ''):
        self._add_row(type_, level, opening_tag)
        self.setCurrentIndex(self.model().index(self.model().rowCount(), 0))

    def ins_row(self, type_ = '', level = '', opening_tag = ''):
        row = self.get_selected_rows()[0]

        self._add_row(row = row, type_ = type_, level = level, opening_tag = opening_tag)
        self.setCurrentIndex(self.model().index(row, 0))

    def del_row(self):
        for i in reversed(self.get_selected_rows()):
            self.model().removeRow(i)

        self.model().itemChanged.emit(QStandardItem())

    def reset_table(self):
        self.clr_table(0)

        for type_, level, opening_tag in self.main.settings_default['tags'][self.settings_tags]:
            self._add_row(type_ = type_, level = level, opening_tag = opening_tag)

    def get_tags(self):
        tags = []

        for row in range(self.model().rowCount()):
            tags.append([
                self.model().item(row, 0).text(),
                self.model().item(row, 1).text(),
                self.model().item(row, 2).text()
            ])

        return tags

class Wl_Table_Tags_Header(Wl_Table_Tags):
    def __init__(self, parent):
        super().__init__(
            parent,
            settings_tags = 'tags_header',
            default_type = parent.tr('Non-embedded'),
            default_level = parent.tr('Header')
        )

        self.setItemDelegateForColumn(1, wl_boxes.Wl_Item_Delegate_Combo_Box(
            parent = self,
            items = [
                self.tr('Header')
            ]
        ))

class Wl_Table_Tags_Body(Wl_Table_Tags):
    def __init__(self, parent):
        super().__init__(
            parent,
            settings_tags = 'tags_body',
            default_type = parent.tr('Embedded'),
            default_level = parent.tr('Part of Speech')
        )

        self.setItemDelegateForColumn(1, wl_boxes.Wl_Item_Delegate_Combo_Box(
            parent = self,
            items = [
                self.tr('Part of Speech'),
                self.tr('Others')
            ]
        ))

class Wl_Table_Tags_Xml(Wl_Table_Tags):
    def __init__(self, parent):
        super().__init__(
            parent,
            settings_tags = 'tags_xml',
            default_type = parent.tr('Non-embedded'),
            default_level = parent.tr('Paragraph')
        )

        self.setItemDelegateForColumn(1, wl_boxes.Wl_Item_Delegate_Combo_Box(
            parent = self,
            items = [
                self.tr('Paragraph'),
                self.tr('Sentence'),
                self.tr('Word')
            ]
        ))

    def item_changed(self, item):
        for row in range(self.model().rowCount()):
            opening_tag_item = self.model().item(row, 2)
            opening_tag_text = opening_tag_item.text()

            # Check if the XML tags are valid
            if opening_tag_text and not re.search(r'^\<[^<>/\s]+?\>$', opening_tag_text):
                wl_msg_boxes.Wl_Msg_Box_Warning(
                    self.main,
                    title = self.tr('Invalid XML Tag'),
                    text = self.tr('''
                        <div>The specified XML tag is invalid!</div>
                    ''')
                ).open()

                self.closePersistentEditor(opening_tag_item.index())
                self.edit(opening_tag_item.index())

                return

        super().item_changed(item = item)

class Wl_Settings_Tags(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['tags']
        self.settings_custom = self.main.settings_custom['tags']

        # Header Tag Settings
        group_box_header_tag_settings = QGroupBox(self.tr('Header Tag Settings'), self)

        self.table_tags_header = Wl_Table_Tags_Header(self)
        self.label_tags_header = wl_labels.Wl_Label_Important(self.tr('Note: All contents surrounded by header tags will be discarded during text processing!'), self)

        group_box_header_tag_settings.setLayout(wl_layouts.Wl_Layout())
        group_box_header_tag_settings.layout().addWidget(self.table_tags_header, 0, 0, 1, 5)
        group_box_header_tag_settings.layout().addWidget(self.table_tags_header.button_add, 1, 0)
        group_box_header_tag_settings.layout().addWidget(self.table_tags_header.button_ins, 1, 1)
        group_box_header_tag_settings.layout().addWidget(self.table_tags_header.button_del, 1, 2)
        group_box_header_tag_settings.layout().addWidget(self.table_tags_header.button_clr, 1, 3)
        group_box_header_tag_settings.layout().addWidget(self.table_tags_header.button_reset, 1, 4)
        group_box_header_tag_settings.layout().addWidget(self.label_tags_header, 2, 0, 1, 5)

        group_box_header_tag_settings.layout().setRowStretch(3, 1)

        # Body Tag Settings
        group_box_body_tag_settings = QGroupBox(self.tr('Body Tag Settings'), self)

        self.table_tags_body = Wl_Table_Tags_Body(self)
        self.label_tags_body = wl_labels.Wl_Label_Hint(self.tr('Use * to indicate any number of characters'), self)

        group_box_body_tag_settings.setLayout(wl_layouts.Wl_Layout())
        group_box_body_tag_settings.layout().addWidget(self.table_tags_body, 0, 0, 1, 5)
        group_box_body_tag_settings.layout().addWidget(self.table_tags_body.button_add, 1, 0)
        group_box_body_tag_settings.layout().addWidget(self.table_tags_body.button_ins, 1, 1)
        group_box_body_tag_settings.layout().addWidget(self.table_tags_body.button_del, 1, 2)
        group_box_body_tag_settings.layout().addWidget(self.table_tags_body.button_clr, 1, 3)
        group_box_body_tag_settings.layout().addWidget(self.table_tags_body.button_reset, 1, 4)
        group_box_body_tag_settings.layout().addWidget(self.label_tags_body, 2, 0, 1, 5)

        group_box_body_tag_settings.layout().setRowStretch(3, 1)

        # XML Tag Settings
        group_box_xml_tag_settings = QGroupBox(self.tr('XML Tag Settings'), self)

        self.table_tags_xml = Wl_Table_Tags_Xml(self)

        group_box_xml_tag_settings.setLayout(wl_layouts.Wl_Layout())
        group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml, 0, 0, 1, 5)
        group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml.button_add, 1, 0)
        group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml.button_ins, 1, 1)
        group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml.button_del, 1, 2)
        group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml.button_clr, 1, 3)
        group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml.button_reset, 1, 4)

        group_box_xml_tag_settings.layout().setRowStretch(2, 1)

        self.setLayout(wl_layouts.Wl_Layout())
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

        self.table_tags_header.clr_table(0)
        self.table_tags_body.clr_table(0)
        self.table_tags_xml.clr_table(0)

        for type_, level, opening_tag in settings['tags_header']:
            self.table_tags_header._add_row(type_ = type_, level = level, opening_tag = opening_tag)

        for type_, level, opening_tag in settings['tags_body']:
            self.table_tags_body._add_row(type_ = type_, level = level, opening_tag = opening_tag)

        for type_, level, opening_tag in settings['tags_xml']:
            self.table_tags_xml._add_row(type_ = type_, level = level, opening_tag = opening_tag)

    def apply_settings(self):
        self.settings_custom['tags_header'] = self.table_tags_header.get_tags()
        self.settings_custom['tags_body'] = self.table_tags_body.get_tags()
        self.settings_custom['tags_xml'] = self.table_tags_xml.get_tags()

        return True
