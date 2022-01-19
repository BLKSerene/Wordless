# ----------------------------------------------------------------------
# Wordless: Settings - Stop Word Lists
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

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_nlp import wl_nlp_utils, wl_stop_word_lists
from wl_utils import wl_conversion
from wl_widgets import wl_box, wl_layout, wl_list, wl_table, wl_tree

class Wl_Settings_Stop_Word_Lists(wl_tree.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

        self.settings_global = self.main.settings_global['stop_word_lists']
        self.settings_default = self.main.settings_default['stop_word_lists']
        self.settings_custom = self.main.settings_custom['stop_word_lists']

        # Stop Word Lists Settings
        group_box_stop_word_lists_settings = QGroupBox(self.tr('Stop Word Lists Settings'), self)

        table_stop_word_lists = wl_table.Wl_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('Stop Word List')
            ],
            cols_stretch = [
                self.tr('Stop Word List')
            ]
        )

        table_stop_word_lists.verticalHeader().setHidden(True)
        table_stop_word_lists.setRowCount(len(self.settings_global))

        for i, lang in enumerate(self.settings_global):
            table_stop_word_lists.setItem(i, 0, QTableWidgetItem(wl_conversion.to_lang_text(self.main, lang)))

            self.__dict__[f'combo_box_stop_word_list_{lang}'] = wl_box.Wl_Combo_Box(self)

            self.__dict__[f'combo_box_stop_word_list_{lang}'].addItems(wl_nlp_utils.to_lang_util_texts(
                self.main,
                util_type = 'stop_word_lists',
                util_codes = self.settings_global[lang]
            ))

            self.__dict__[f'combo_box_stop_word_list_{lang}'].currentTextChanged.connect(lambda text, lang = lang: self.stop_word_list_changed(lang))

            table_stop_word_lists.setCellWidget(i, 1, self.__dict__[f'combo_box_stop_word_list_{lang}'])

        group_box_stop_word_lists_settings.setLayout(wl_layout.Wl_Layout())
        group_box_stop_word_lists_settings.layout().addWidget(table_stop_word_lists, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_stop_word_list_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_stop_word_list_preview_lang = wl_box.Wl_Combo_Box(self)
        self.combo_box_stop_word_list_preview_lang.addItems(wl_conversion.to_lang_texts(self.main, self.settings_global))
        self.label_stop_word_list_preview_count = QLabel('', self)

        self.list_stop_word_list_preview_results = wl_list.Wl_List_Stop_Words(self)

        self.combo_box_stop_word_list_preview_lang.currentTextChanged.connect(self.preview_settings_changed)
        self.combo_box_stop_word_list_preview_lang.currentTextChanged.connect(self.preview_results_changed)

        layout_preview_settings = wl_layout.Wl_Layout()
        layout_preview_settings.addWidget(self.label_stop_word_list_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_stop_word_list_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_stop_word_list_preview_count, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(wl_layout.Wl_Layout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 6)
        group_box_preview.layout().addWidget(self.list_stop_word_list_preview_results, 1, 0, 1, 6)
        group_box_preview.layout().addWidget(self.list_stop_word_list_preview_results.button_add, 2, 0)
        group_box_preview.layout().addWidget(self.list_stop_word_list_preview_results.button_insert, 2, 1)
        group_box_preview.layout().addWidget(self.list_stop_word_list_preview_results.button_remove, 2, 2)
        group_box_preview.layout().addWidget(self.list_stop_word_list_preview_results.button_clear, 2, 3)
        group_box_preview.layout().addWidget(self.list_stop_word_list_preview_results.button_import, 2, 4)
        group_box_preview.layout().addWidget(self.list_stop_word_list_preview_results.button_export, 2, 5)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(group_box_stop_word_lists_settings, 0, 0)
        self.layout().addWidget(group_box_preview, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(0, 3)
        self.layout().setRowStretch(1, 2)

        self.preview_results_changed()

    def stop_word_list_changed(self, lang):
        if lang == self.settings_custom['preview_lang']:
            self.preview_results_changed()

    def preview_settings_changed(self):
        self.settings_custom['preview_lang'] = wl_conversion.to_lang_code(self.main, self.combo_box_stop_word_list_preview_lang.currentText())

    def preview_results_changed(self):
        lang = wl_conversion.to_lang_code(self.main, self.combo_box_stop_word_list_preview_lang.currentText())
        list_stop_words = wl_nlp_utils.to_lang_util_code(
            self.main,
            util_type = 'stop_word_lists',
            util_text = self.__dict__[f'combo_box_stop_word_list_{lang}'].currentText()
        )
        
        stop_words = wl_stop_word_lists.wl_get_stop_word_list(self.main, lang, stop_word_list = list_stop_words)
        
        self.list_stop_word_list_preview_results.load_stop_words(stop_words)
        self.label_stop_word_list_preview_count.setText(self.tr(f'Count of Stop Words: {len(stop_words)}'))

        if list_stop_words == 'custom':
            self.list_stop_word_list_preview_results.switch_to_custom()

            self.list_stop_word_list_preview_results.itemChanged.connect(lambda: self.label_stop_word_list_preview_count.setText(self.tr(f'Count of Stop Words: {self.list_stop_word_list_preview_results.count()}')))
        else:
            self.list_stop_word_list_preview_results.switch_to_default()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        for lang in settings['stop_word_lists']:
            self.__dict__[f'combo_box_stop_word_list_{lang}'].setCurrentText(wl_nlp_utils.to_lang_util_text(
                self.main,
                util_type = 'stop_word_lists',
                util_code = settings['stop_word_lists'][lang]
            ))

        if not defaults:
            self.combo_box_stop_word_list_preview_lang.setCurrentText(wl_conversion.to_lang_text(self.main, settings['preview_lang']))

        if defaults:
            self.settings_custom['custom_lists'] = copy.deepcopy(self.settings_default['custom_lists'])

        self.combo_box_stop_word_list_preview_lang.currentTextChanged.emit(self.combo_box_stop_word_list_preview_lang.currentText())

    def apply_settings(self):
        for lang in self.settings_custom['stop_word_lists']:
            self.settings_custom['stop_word_lists'][lang] = wl_nlp_utils.to_lang_util_code(
                self.main,
                util_type = 'stop_word_lists',
                util_text = self.__dict__[f'combo_box_stop_word_list_{lang}'].currentText()
            )

        if self.settings_custom['stop_word_lists'][self.settings_custom['preview_lang']] == self.tr('Custom List'):
            self.settings_custom['custom_lists'][self.settings_custom['preview_lang']] = self.list_stop_word_list_preview_results.get_items()

        return True
