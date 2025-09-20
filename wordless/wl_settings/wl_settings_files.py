# ----------------------------------------------------------------------
# Wordless: Settings - Files
# Copyright (C) 2018-2025  Ye Lei (叶磊)
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import copy
import re

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from wordless.wl_checks import wl_checks_misc
from wordless.wl_dialogs import wl_dialogs
from wordless.wl_nlp import wl_matching
from wordless.wl_settings import wl_settings
from wordless.wl_utils import (
    wl_conversion,
    wl_misc
)
from wordless.wl_widgets import (
    wl_boxes,
    wl_item_delegates,
    wl_labels,
    wl_layouts,
    wl_tables
)

_tr = QtCore.QCoreApplication.translate

# Files
class Wl_Settings_Files(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['files']
        self.settings_custom = self.main.settings_custom['files']

        # Default Settings
        self.group_box_default_settings = QtWidgets.QGroupBox(self.tr('Default Settings'), self)

        self.label_encoding = QtWidgets.QLabel(self.tr('Encoding:'), self)
        self.combo_box_encoding = wl_boxes.Wl_Combo_Box_Encoding(self)
        self.label_lang = QtWidgets.QLabel(self.tr('Language:'), self)
        self.combo_box_lang = wl_boxes.Wl_Combo_Box_Lang(self)
        self.label_tokenized = QtWidgets.QLabel(self.tr('Tokenized:'), self)
        self.combo_box_tokenized = wl_boxes.Wl_Combo_Box_Yes_No(self)
        self.label_tagged = QtWidgets.QLabel(self.tr('Tagged:'), self)
        self.combo_box_tagged = wl_boxes.Wl_Combo_Box_Yes_No(self)

        self.group_box_default_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_default_settings.layout().addWidget(self.label_encoding, 0, 0)
        self.group_box_default_settings.layout().addWidget(self.combo_box_encoding, 0, 1)
        self.group_box_default_settings.layout().addWidget(self.label_lang, 1, 0)
        self.group_box_default_settings.layout().addWidget(self.combo_box_lang, 1, 1)
        self.group_box_default_settings.layout().addWidget(self.label_tokenized, 2, 0)
        self.group_box_default_settings.layout().addWidget(self.combo_box_tokenized, 2, 1)
        self.group_box_default_settings.layout().addWidget(self.label_tagged, 3, 0)
        self.group_box_default_settings.layout().addWidget(self.combo_box_tagged, 3, 1)

        self.group_box_default_settings.layout().setColumnStretch(3, 1)

        # Detection Settings
        self.group_box_auto_detection_settings = QtWidgets.QGroupBox(self.tr('Auto-detection Settings'), self)

        self.label_num_lines = QtWidgets.QLabel(self.tr('Number of lines to scan in each file:'), self)
        (
            self.spin_box_num_lines,
            self.checkbox_num_lines_no_limit
        ) = wl_boxes.wl_spin_box_no_limit(self)

        self.spin_box_num_lines.setRange(1, 1000000)

        self.group_box_auto_detection_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_auto_detection_settings.layout().addWidget(self.label_num_lines, 0, 0)
        self.group_box_auto_detection_settings.layout().addWidget(self.spin_box_num_lines, 0, 1)
        self.group_box_auto_detection_settings.layout().addWidget(self.checkbox_num_lines_no_limit, 0, 2)

        self.group_box_auto_detection_settings.layout().setColumnStretch(3, 1)

        # Miscellaneous Settings
        self.group_box_misc_settings = QtWidgets.QGroupBox(self.tr('Miscellaneous Settings'), self)

        self.checkbox_display_warning_when_opening_nontext_files = QtWidgets.QCheckBox(self.tr('Display warning when opening non-text files'), self)
        self.label_read_files_in_chunks = QtWidgets.QLabel(self.tr('Read files in chunks of'), self)
        self.spin_box_read_files_in_chunks = wl_boxes.Wl_Spin_Box(self)
        self.label_read_files_in_chunks_chars = QtWidgets.QLabel(self.tr('characters'), self)

        self.spin_box_read_files_in_chunks.setRange(100, 1000000)

        self.group_box_misc_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_misc_settings.layout().addWidget(self.checkbox_display_warning_when_opening_nontext_files, 0, 0, 1, 3)
        self.group_box_misc_settings.layout().addWidget(self.label_read_files_in_chunks, 1, 0)
        self.group_box_misc_settings.layout().addWidget(self.spin_box_read_files_in_chunks, 1, 1)
        self.group_box_misc_settings.layout().addWidget(self.label_read_files_in_chunks_chars, 1, 2)

        self.group_box_misc_settings.layout().setColumnStretch(3, 1)

        self.layout().addWidget(self.group_box_default_settings, 0, 0)
        self.layout().addWidget(self.group_box_auto_detection_settings, 1, 0)
        self.layout().addWidget(self.group_box_misc_settings, 2, 0)

        self.layout().setRowStretch(3, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Default Settings
        self.combo_box_encoding.setCurrentText(wl_conversion.to_encoding_text(self.main, settings['default_settings']['encoding']))
        self.combo_box_lang.setCurrentText(wl_conversion.to_lang_text(self.main, settings['default_settings']['lang']))
        self.combo_box_tokenized.set_yes_no(settings['default_settings']['tokenized'])
        self.combo_box_tagged.set_yes_no(settings['default_settings']['tagged'])

        # Auto-detection Settings
        self.spin_box_num_lines.setValue(settings['auto_detection_settings']['num_lines'])
        self.checkbox_num_lines_no_limit.setChecked(settings['auto_detection_settings']['num_lines_no_limit'])

        # Miscellaneous Settings
        self.checkbox_display_warning_when_opening_nontext_files.setChecked(settings['misc_settings']['display_warning_when_opening_nontext_files'])
        self.spin_box_read_files_in_chunks.setValue(settings['misc_settings']['read_files_in_chunks_chars'])

    def apply_settings(self):
        # Default Settings
        self.settings_custom['default_settings']['encoding'] = wl_conversion.to_encoding_code(self.main, self.combo_box_encoding.currentText())
        self.settings_custom['default_settings']['lang'] = wl_conversion.to_lang_code(self.main, self.combo_box_lang.currentText())
        self.settings_custom['default_settings']['tokenized'] = self.combo_box_tokenized.get_yes_no()
        self.settings_custom['default_settings']['tagged'] = self.combo_box_tagged.get_yes_no()

        # Auto-detection Settings
        self.settings_custom['auto_detection_settings']['num_lines'] = self.spin_box_num_lines.value()
        self.settings_custom['auto_detection_settings']['num_lines_no_limit'] = self.checkbox_num_lines_no_limit.isChecked()

        # Miscellaneous Settings
        self.settings_custom['misc_settings']['display_warning_when_opening_nontext_files'] = self.checkbox_display_warning_when_opening_nontext_files.isChecked()
        self.settings_custom['misc_settings']['read_files_in_chunks_chars'] = self.spin_box_read_files_in_chunks.value()

        return True

# Files - Tags
class Wl_Settings_Files_Tags(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['files']['tags']
        self.settings_custom = self.main.settings_custom['files']['tags']

        # Header Tag Settings
        self.group_box_header_tag_settings = QtWidgets.QGroupBox(self.tr('Header Tag Settings'), self)

        self.table_tags_header = Wl_Table_Tags_Header(self)
        self.label_tags_header_note = wl_labels.Wl_Label_Html(self.tr('<b>Warning:</b> All contents enclosed by header tags will be discarded during corpus analysis.'), self)

        self.group_box_header_tag_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_header_tag_settings.layout().addWidget(self.table_tags_header, 0, 0, 1, 5)
        self.group_box_header_tag_settings.layout().addWidget(self.table_tags_header.button_add, 1, 0)
        self.group_box_header_tag_settings.layout().addWidget(self.table_tags_header.button_ins, 1, 1)
        self.group_box_header_tag_settings.layout().addWidget(self.table_tags_header.button_del, 1, 2)
        self.group_box_header_tag_settings.layout().addWidget(self.table_tags_header.button_clr, 1, 3)
        self.group_box_header_tag_settings.layout().addWidget(self.table_tags_header.button_reset, 1, 4)
        self.group_box_header_tag_settings.layout().addWidget(self.label_tags_header_note, 2, 0, 1, 5)

        # Body Tag Settings
        self.group_box_body_tag_settings = QtWidgets.QGroupBox(self.tr('Body Tag Settings'), self)

        self.table_tags_body = Wl_Table_Tags_Body(self)
        self.label_tags_body_wildcard = wl_labels.Wl_Label_Hint(self.tr('Tip: Use the asterisk character * to indicate any number of characters'), self)

        self.group_box_body_tag_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_body_tag_settings.layout().addWidget(self.table_tags_body, 0, 0, 1, 5)
        self.group_box_body_tag_settings.layout().addWidget(self.table_tags_body.button_add, 1, 0)
        self.group_box_body_tag_settings.layout().addWidget(self.table_tags_body.button_ins, 1, 1)
        self.group_box_body_tag_settings.layout().addWidget(self.table_tags_body.button_del, 1, 2)
        self.group_box_body_tag_settings.layout().addWidget(self.table_tags_body.button_clr, 1, 3)
        self.group_box_body_tag_settings.layout().addWidget(self.table_tags_body.button_reset, 1, 4)
        self.group_box_body_tag_settings.layout().addWidget(self.label_tags_body_wildcard, 2, 0, 1, 5)

        # XML Tag Settings
        self.group_box_xml_tag_settings = QtWidgets.QGroupBox(self.tr('XML Tag Settings'), self)

        self.table_tags_xml = Wl_Table_Tags_Xml(self)

        self.group_box_xml_tag_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml, 0, 0, 1, 5)
        self.group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml.button_add, 1, 0)
        self.group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml.button_ins, 1, 1)
        self.group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml.button_del, 1, 2)
        self.group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml.button_clr, 1, 3)
        self.group_box_xml_tag_settings.layout().addWidget(self.table_tags_xml.button_reset, 1, 4)

        self.layout().addWidget(self.group_box_header_tag_settings, 0, 0)
        self.layout().addWidget(self.group_box_body_tag_settings, 1, 0)
        self.layout().addWidget(self.group_box_xml_tag_settings, 2, 0)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        self.table_tags_header.clr_table(0)
        self.table_tags_body.clr_table(0)
        self.table_tags_xml.clr_table(0)

        for tag in settings['header_tag_settings']:
            self.table_tags_header._add_row(texts = tag)

        for tag in settings['body_tag_settings']:
            self.table_tags_body._add_row(texts = tag)

        for tag in settings['xml_tag_settings']:
            self.table_tags_xml._add_row(texts = tag)

    def apply_settings(self):
        self.settings_custom['header_tag_settings'] = self.table_tags_header.get_tags()
        self.settings_custom['body_tag_settings'] = self.table_tags_body.get_tags()
        self.settings_custom['xml_tag_settings'] = self.table_tags_xml.get_tags()

        return True

RE_TAG_EMBEDDED = re.compile(r'^([^\w\s*]|_)+\S*$')
RE_TAG_NONEMBEDDED = re.compile(r'^([^\w\s]|_)+\S*([^\w\s]|_)+$')
RE_TAG_NONEMBEDDED_BODY = re.compile(r'^([^\w\s*]|_)+\S*([^\w\s*]|_)+$')
RE_TAG_HTML_BRACKETS = re.compile(r'(^<)|(>$)')
RE_TAG_HTML_PARENTHESES = re.compile(r'\s\((\d+)\)')

# Reference: https://www.w3.org/TR/REC-xml/#NT-NameStartChar
NameStartChar = r'[A-Za-z:_\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\u10000-\uEFFFF]'
NameChar = fr'{NameStartChar[:-1]}0-9\-.\u00B7\u0300-\u036F\u203F-\u2040]'
RE_TAG_XML = re.compile(fr'^<{NameStartChar}{NameChar}*>$')

# self.tr() may not work in inherited classes
# See: https://www.riverbankcomputing.com/static/Docs/PyQt5/i18n.html#differences-between-pyqt5-and-qt
class Wl_Table_Tags(wl_tables.Wl_Table_Add_Ins_Del_Clr):
    def __init__(self, parent, settings_tags, defaults_row):
        super().__init__(
            parent = parent,
            headers = [
                _tr('Wl_Table_Tags', 'Type'),
                _tr('Wl_Table_Tags', 'Level'),
                _tr('Wl_Table_Tags', 'Opening Tag'),
                _tr('Wl_Table_Tags', 'Closing Tag'),
                _tr('Wl_Table_Tags', 'Preview')
            ],
            col_edit = 2
        )

        self.settings_tags = settings_tags
        self.tag_type = self.settings_tags.split('_', 1)[0]
        self.defaults_row = defaults_row

        self.setItemDelegateForColumn(0, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
            parent = self,
            items = [
                _tr('Wl_Table_Tags', 'Embedded'),
                _tr('Wl_Table_Tags', 'Nonembedded')
            ]
        ))
        self.setItemDelegateForColumn(3, wl_item_delegates.Wl_Item_Delegate_Uneditable(self))
        self.setItemDelegateForColumn(4, wl_item_delegates.Wl_Item_Delegate_Uneditable(self))

        self.button_reset = QtWidgets.QPushButton(_tr('Wl_Table_Tags', 'Reset'), self)

        self.button_reset.clicked.connect(lambda: self.reset_table()) # pylint: disable=unnecessary-lambda

        self.reset_table()

    def check_empty_duplicate_tags(self, item):
        if not self.is_empty() and item.column() == 2:
            # Check for empty tags
            if wl_misc.RE_EMPTY_ITEM.search(item.text()):
                item.setText(item.text_old)

                return False

            # Check duplicate tags
            for row in range(self.model().rowCount()):
                if row != item.row() and self.model().item(row, 2).text() == item.text():
                    # Use exec() instead of open() here to allow editing
                    wl_dialogs.Wl_Dialog_Info_Simple(
                        self.main,
                        title = _tr('Wl_Table_Tags', 'Duplicate Tags'),
                        text = _tr('Wl_Table_Tags', '''
                            <div>The tag that you have specified already exists in the table.</div>
                            <br>
                            <div>Please specify another tag.</div>
                        '''),
                        icon = 'warning'
                    ).exec()

                    item.setText(item.text_old)

                    # Allow the editor to be closed properly after editing is started
                    self.setCurrentIndex(item.index())

                    # Only work when the editor is closed by clicking areas outside the table
                    self.closePersistentEditor(item.index())
                    self.edit(item.index())

                    return False

        return True

    def check_invalid_tags(self, item):
        if not self.is_empty() and item.column() == 2:
            # Check for invalid opening tags
            if self.model().item(item.row(), 0).text() == _tr('Wl_Table_Tags', 'Embedded'):
                re_validation = RE_TAG_EMBEDDED.search(item.text())
                warning_text = _tr('Wl_Table_Tags', '''
                    <div>Embedded tags must begin with punctuation marks, e.g. an underscore _ or a slash /.</div>
                ''')
            else:
                if self.tag_type == 'body':
                    re_validation = RE_TAG_NONEMBEDDED_BODY.search(item.text())
                else:
                    re_validation = RE_TAG_NONEMBEDDED.search(item.text())

                warning_text = _tr('Wl_Table_Tags', '''
                    <div>Nonembedded tags must begin and end with punctuation marks, e.g. angle brackets <>.</div>
                ''')

            if re_validation is None:
                # Use exec() instead of open() here to allow editing to be started
                wl_dialogs.Wl_Dialog_Info_Simple(
                    self.main,
                    title = _tr('Wl_Table_Tags', 'Invalid Opening Tag'),
                    text = warning_text,
                    icon = 'warning'
                ).exec()

                item.setText(item.text_old)

                # Allow the editor to be closed properly after editing is started
                self.setCurrentIndex(item.index())

                self.closeEditor(self.findChild(QtWidgets.QLineEdit), QtWidgets.QAbstractItemDelegate.NoHint)
                self.edit(item.index())

                return False

        return True

    def check_invalid_tags_xml(self, item):
        if not self.is_empty() and item.column() == 2 and not RE_TAG_XML.search(item.text()):
            wl_dialogs.Wl_Dialog_Info_Simple(
                self.main,
                title = _tr('Wl_Table_Tags', 'Invalid XML Tag'),
                text = _tr('Wl_Table_Tags', '''
                    <div>The specified XML tag is invalid.</div>
                    <br>
                    <div>Please check your settings or specify another XML tag.</div>
                '''),
                icon = 'warning'
            ).exec()

            item.setText(item.text_old)

            self.setCurrentIndex(item.index())

            self.closeEditor(self.findChild(QtWidgets.QLineEdit), QtWidgets.QAbstractItemDelegate.NoHint)
            self.edit(item.index())

            return False
        else:
            return True

    def update_tags(self, item):
        if not self.is_empty():
            if item.column() == 2:
                item.text_old = item.text()

            # Update closing tags and preview
            if item.column() in (0, 1, 2):
                self.disable_updates()

                for row in range(self.model().rowCount()):
                    tag_type = self.model().item(row, 0).text()
                    tag_opening = self.model().item(row, 2).text()

                    item_tag_closing = self.model().item(row, 3)
                    item_preview = self.model().item(row, 4)

                    if tag_type == _tr('Wl_Table_Tags', 'Embedded'):
                        tag_separator, tag_name = wl_matching.split_tag_embedded(tag_opening)
                        tag_name = wl_matching.replace_wildcards_in_tag_name(
                            tag_name,
                            _tr('Wl_Table_Tags', 'TAG'),
                            self.tag_type,
                            escape = False
                        )

                        item_tag_closing.setText(_tr('Wl_Table_Tags', 'N/A'))
                        item_preview.setText(_tr('Wl_Table_Tags', 'token') + tag_separator + tag_name)
                    elif tag_type == _tr('Wl_Table_Tags', 'Nonembedded'):
                        # Add a slash / before the tag name
                        tag_start, tag_name, tag_end = wl_matching.split_tag_nonembedded(tag_opening, self.tag_type)
                        item_tag_closing.setText(f'{tag_start}/{tag_name}{tag_end}')

                        tag_name = wl_matching.replace_wildcards_in_tag_name(
                            tag_name,
                            _tr('Wl_Table_Tags', 'TAG'),
                            self.tag_type,
                            escape = False)

                        item_preview.setText(
                            f'{tag_start}{tag_name}{tag_end}'
                            + _tr('Wl_Table_Tags', 'token')
                            + f'{tag_start}/{tag_name}{tag_end}'
                        )

                self.enable_updates()

    def _add_row(self, row = None, texts = None):
        if texts is None:
            type_, level, opening_tag, _ = self.defaults_row

            # HTML tags
            if opening_tag.startswith('<') and opening_tag.endswith('>'):
                opening_tags = [
                    RE_TAG_HTML_BRACKETS.sub(r'', self.model().item(i, 2).text())
                    for i in range(self.model().rowCount())
                ]
                opening_tag = f"<{wl_checks_misc.check_new_name(opening_tag[1:-1], opening_tags, separator = '')}>"
            else:
                opening_tags = [self.model().item(i, 2).text() for i in range(self.model().rowCount())]
                opening_tag = wl_checks_misc.check_new_name(opening_tag, opening_tags, separator = '')

            opening_tag = RE_TAG_HTML_PARENTHESES.sub(r'\1', opening_tag)
        else:
            type_, level, opening_tag, _ = texts

        item_opening_tag = QtGui.QStandardItem(opening_tag)
        item_opening_tag.text_old = opening_tag

        if row is None:
            self.model().appendRow([
                QtGui.QStandardItem(type_),
                QtGui.QStandardItem(level),
                item_opening_tag,
                QtGui.QStandardItem(),
                QtGui.QStandardItem()
            ])
        else:
            self.model().insertRow(row, [
                QtGui.QStandardItem(type_),
                QtGui.QStandardItem(level),
                item_opening_tag,
                QtGui.QStandardItem(),
                QtGui.QStandardItem()
            ])

        self.model().itemChanged.emit(item_opening_tag)

    def reset_table(self):
        self.clr_table(0)

        for defaults in self.main.settings_default['files']['tags'][self.settings_tags]:
            self._add_row(texts = defaults)

    def get_tags(self):
        tags = []

        for row in range(self.model().rowCount()):
            tags.append([
                self.model().item(row, 0).text(),
                self.model().item(row, 1).text(),
                self.model().item(row, 2).text(),
                self.model().item(row, 3).text()
            ])

        return tags

# pylint: disable=arguments-differ
class Wl_Table_Tags_Header(Wl_Table_Tags):
    def __init__(self, parent):
        super().__init__(
            parent,
            settings_tags = 'header_tag_settings',
            defaults_row = [
                _tr('Wl_Table_Tags_Header', 'Nonembedded'),
                _tr('Wl_Table_Tags_Header', 'Header'),
                _tr('Wl_Table_Tags_Header', '<TAG>'),
                ''
            ]
        )

        self.setItemDelegateForColumn(1, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
            parent = self,
            items = [
                self.tr('Header')
            ]
        ))

    def item_changed(self, item):
        super().item_changed()

        if not self.check_empty_duplicate_tags(item):
            return

        if not self.check_invalid_tags(item):
            return

        self.update_tags(item)

class Wl_Table_Tags_Body(Wl_Table_Tags):
    def __init__(self, parent):
        super().__init__(
            parent,
            settings_tags = 'body_tag_settings',
            defaults_row = [
                _tr('Wl_Table_Tags_Body', 'Nonembedded'),
                _tr('Wl_Table_Tags_Body', 'Others'),
                _tr('Wl_Table_Tags_Body', '<TAG>'),
                ''
            ]
        )

        self.setItemDelegateForColumn(1, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
            parent = self,
            items = [
                self.tr('Part of speech'),
                self.tr('Others')
            ]
        ))

    def item_changed(self, item):
        super().item_changed()

        if not self.check_empty_duplicate_tags(item):
            return

        if not self.check_invalid_tags(item):
            return

        self.update_tags(item)

class Wl_Table_Tags_Xml(Wl_Table_Tags):
    def __init__(self, parent):
        super().__init__(
            parent,
            settings_tags = 'xml_tag_settings',
            defaults_row = [
                _tr('Wl_Table_Tags_Xml', 'Nonembedded'),
                _tr('Wl_Table_Tags_Xml', 'Paragraph'),
                _tr('Wl_Table_Tags_Xml', '<TAG>'),
                ''
            ]
        )

        self.setItemDelegateForColumn(0, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
            parent = self,
            items = [
                self.tr('Nonembedded')
            ]
        ))
        self.setItemDelegateForColumn(1, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
            parent = self,
            items = [
                self.tr('Paragraph'),
                self.tr('Sentence'),
                self.tr('Word')
            ]
        ))

    def item_changed(self, item):
        super().item_changed()

        if not self.check_empty_duplicate_tags(item):
            return

        if not self.check_invalid_tags_xml(item):
            return

        self.update_tags(item)
