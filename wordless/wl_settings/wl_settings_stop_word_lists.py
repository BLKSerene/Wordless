# ----------------------------------------------------------------------
# Wordless: Settings - Stop Word Lists
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

from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QCheckBox, QGroupBox, QLabel

from wordless.wl_nlp import wl_nlp_utils, wl_stop_word_lists
from wordless.wl_settings import wl_settings
from wordless.wl_utils import wl_conversion
from wordless.wl_widgets import (
    wl_boxes,
    wl_item_delegates,
    wl_layouts,
    wl_lists,
    wl_tables
)

class Wl_Settings_Stop_Word_Lists(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_global = self.main.settings_global['stop_word_lists']
        self.settings_default = self.main.settings_default['stop_word_lists']
        self.settings_custom = self.main.settings_custom['stop_word_lists']

        # Stop Word Lists Settings
        self.group_box_stop_word_list_settings = QGroupBox(self.tr('Stop Word List Settings'), self)

        self.table_stop_word_lists = wl_tables.Wl_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('Stop Word List')
            ],
            editable = True
        )
        self.checkbox_case_sensitive = QCheckBox(self.tr('Case-sensitive'), self)

        self.table_stop_word_lists.setFixedHeight(370)
        self.table_stop_word_lists.verticalHeader().setHidden(True)
        self.table_stop_word_lists.model().setRowCount(len(self.settings_global))

        self.table_stop_word_lists.model().dataChanged.connect(self.stop_word_list_changed)

        self.table_stop_word_lists.disable_updates()

        for i, lang in enumerate(self.settings_global):
            self.table_stop_word_lists.model().setItem(i, 0, QStandardItem(wl_conversion.to_lang_text(self.main, lang)))
            self.table_stop_word_lists.model().setItem(i, 1, QStandardItem())

            self.table_stop_word_lists.setItemDelegateForRow(i, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
                parent = self.table_stop_word_lists,
                items = list(wl_nlp_utils.to_lang_util_texts(
                    self.main,
                    util_type = 'stop_word_lists',
                    util_codes = self.settings_global[lang]
                )),
                col = 1
            ))

        self.table_stop_word_lists.enable_updates()

        self.group_box_stop_word_list_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_stop_word_list_settings.layout().addWidget(self.table_stop_word_lists, 0, 0)
        self.group_box_stop_word_list_settings.layout().addWidget(self.checkbox_case_sensitive, 1, 0)

        # Preview
        self.group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_preview_lang = wl_boxes.Wl_Combo_Box(self)
        self.combo_box_preview_lang.addItems(wl_conversion.to_lang_texts(self.main, self.settings_global))
        self.label_preview_num = QLabel('', self)

        self.list_preview_results = wl_lists.Wl_List_Stop_Words(self)

        self.combo_box_preview_lang.currentTextChanged.connect(self.preview_settings_changed)
        self.combo_box_preview_lang.currentTextChanged.connect(self.preview_results_changed)

        layout_preview_settings = wl_layouts.Wl_Layout()
        layout_preview_settings.addWidget(self.label_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_preview_num, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        self.group_box_preview.setLayout(wl_layouts.Wl_Layout())
        self.group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 6)
        self.group_box_preview.layout().addWidget(self.list_preview_results, 1, 0, 1, 6)
        self.group_box_preview.layout().addWidget(self.list_preview_results.button_add, 2, 0)
        self.group_box_preview.layout().addWidget(self.list_preview_results.button_ins, 2, 1)
        self.group_box_preview.layout().addWidget(self.list_preview_results.button_del, 2, 2)
        self.group_box_preview.layout().addWidget(self.list_preview_results.button_clr, 2, 3)
        self.group_box_preview.layout().addWidget(self.list_preview_results.button_imp, 2, 4)
        self.group_box_preview.layout().addWidget(self.list_preview_results.button_exp, 2, 5)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_stop_word_list_settings, 0, 0)
        self.layout().addWidget(self.group_box_preview, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(1, 1)

        self.load_settings()
        self.preview_results_changed()

    def stop_word_list_changed(self, topLeft = None, bottomRight = None): # pylint: disable=unused-argument
        if topLeft:
            lang = wl_conversion.to_lang_code(self.main, self.table_stop_word_lists.model().item(topLeft.row(), 0).text())

            if lang == self.settings_custom['preview']['preview_lang']:
                self.preview_results_changed()

    def preview_settings_changed(self):
        self.settings_custom['preview']['preview_lang'] = wl_conversion.to_lang_code(self.main, self.combo_box_preview_lang.currentText())

    def preview_results_changed(self):
        row = list(self.settings_global).index(self.settings_custom['preview']['preview_lang'])
        lang = wl_conversion.to_lang_code(self.main, self.combo_box_preview_lang.currentText())
        list_stop_words = wl_nlp_utils.to_lang_util_code(
            self.main,
            util_type = 'stop_word_lists',
            util_text = self.table_stop_word_lists.model().item(row, 1).text()
        )

        stop_words = wl_stop_word_lists.wl_get_stop_word_list(self.main, lang, stop_word_list = list_stop_words)

        self.list_preview_results.load_items(sorted(stop_words))
        self.label_preview_num.setText(self.tr('Number of stop words: ') + str(len(stop_words)))

        if list_stop_words == 'custom':
            self.list_preview_results.switch_to_custom()

            self.list_preview_results.model().dataChanged.connect(lambda: self.label_preview_num.setText(self.tr('Number of stop words: ') + str(self.list_preview_results.model().rowCount())))
        else:
            self.list_preview_results.switch_to_default()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        self.table_stop_word_lists.disable_updates()

        for i, lang in enumerate(self.settings_global):
            self.table_stop_word_lists.model().item(i, 1).setText(wl_nlp_utils.to_lang_util_text(
                self.main,
                util_type = 'stop_word_lists',
                util_code = settings['stop_word_list_settings']['stop_word_lists'][lang]
            ))

        self.table_stop_word_lists.enable_updates()

        self.checkbox_case_sensitive.setChecked(settings['stop_word_list_settings']['case_sensitive'])

        if not defaults:
            self.combo_box_preview_lang.setCurrentText(wl_conversion.to_lang_text(self.main, settings['preview']['preview_lang']))

        # Custom stop word lists
        if defaults:
            self.settings_custom['custom_lists'] = copy.deepcopy(self.settings_default['custom_lists'])

        self.combo_box_preview_lang.currentTextChanged.emit(self.combo_box_preview_lang.currentText())

    def apply_settings(self):
        for i, lang in enumerate(self.settings_global):
            self.settings_custom['stop_word_list_settings']['stop_word_lists'][lang] = wl_nlp_utils.to_lang_util_code(
                self.main,
                util_type = 'stop_word_lists',
                util_text = self.table_stop_word_lists.model().item(i, 1).text()
            )

        self.settings_custom['stop_word_list_settings']['case_sensitive'] = self.checkbox_case_sensitive.isChecked()

        # Custom stop word lists
        preview_lang = self.settings_custom['preview']['preview_lang']

        if self.settings_custom['stop_word_list_settings']['stop_word_lists'][preview_lang] == 'custom':
            self.settings_custom['custom_lists'][preview_lang] = self.list_preview_results.model().stringList()

        return True
