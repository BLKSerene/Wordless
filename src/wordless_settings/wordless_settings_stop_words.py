#
# Wordless: Settings - Stop Words
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_text import wordless_stop_words
from wordless_utils import wordless_conversion
from wordless_widgets import (wordless_box, wordless_layout, wordless_list,
                              wordless_table, wordless_tree)

class Wordless_Settings_Stop_Words(wordless_tree.Wordless_Settings):
    def __init__(self, main):
        super().__init__(main)

        settings_global = self.main.settings_global['stop_words']

        # Stop Words Settings
        group_box_stop_words_settings = QGroupBox(self.tr('Stop Words Settings'), self)

        table_stop_words = wordless_table.Wordless_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('Lists of Stop Words')
            ],
            cols_stretch = [
                self.tr('Lists of Stop Words')
            ]
        )

        table_stop_words.verticalHeader().setHidden(True)
        table_stop_words.setRowCount(len(settings_global))

        for i, lang in enumerate(settings_global):
            table_stop_words.setItem(i, 0, QTableWidgetItem(wordless_conversion.to_lang_text(self.main, lang)))

            self.__dict__[f'combo_box_stop_words_{lang}'] = wordless_box.Wordless_Combo_Box(self)

            self.__dict__[f'combo_box_stop_words_{lang}'].addItems(settings_global[lang])

            self.__dict__[f'combo_box_stop_words_{lang}'].currentTextChanged.connect(lambda text, lang = lang: self.stop_words_changed(lang))

            table_stop_words.setCellWidget(i, 1, self.__dict__[f'combo_box_stop_words_{lang}'])

        group_box_stop_words_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_stop_words_settings.layout().addWidget(table_stop_words, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_stop_words_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_stop_words_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.combo_box_stop_words_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))
        self.label_stop_words_preview_count = QLabel('', self)

        self.list_stop_words_preview_results = wordless_list.Wordless_List_Stop_Words(self)

        self.combo_box_stop_words_preview_lang.currentTextChanged.connect(self.preview_settings_changed)
        self.combo_box_stop_words_preview_lang.currentTextChanged.connect(self.preview_results_changed)

        layout_preview_settings = wordless_layout.Wordless_Layout()
        layout_preview_settings.addWidget(self.label_stop_words_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_stop_words_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_stop_words_preview_count, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(wordless_layout.Wordless_Layout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 5)
        group_box_preview.layout().addWidget(self.list_stop_words_preview_results, 1, 0, 1, 5)
        group_box_preview.layout().addWidget(self.list_stop_words_preview_results.button_add, 2, 0)
        group_box_preview.layout().addWidget(self.list_stop_words_preview_results.button_remove, 2, 1)
        group_box_preview.layout().addWidget(self.list_stop_words_preview_results.button_clear, 2, 2)
        group_box_preview.layout().addWidget(self.list_stop_words_preview_results.button_import, 2, 3)
        group_box_preview.layout().addWidget(self.list_stop_words_preview_results.button_export, 2, 4)

        self.setLayout(wordless_layout.Wordless_Layout())
        self.layout().addWidget(group_box_stop_words_settings, 0, 0)
        self.layout().addWidget(group_box_preview, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(0, 3)
        self.layout().setRowStretch(1, 2)

        self.preview_results_changed()

    def stop_words_changed(self, lang):
        settings_custom = self.main.settings_custom['stop_words']

        if lang == settings_custom['preview_lang']:
            self.preview_results_changed()

    def preview_settings_changed(self):
        settings_custom = self.main.settings_custom['stop_words']

        settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_stop_words_preview_lang.currentText())

    def preview_results_changed(self):
        lang = wordless_conversion.to_lang_code(self.main, self.combo_box_stop_words_preview_lang.currentText())
        list_stop_words = self.__dict__[f'combo_box_stop_words_{lang}'].currentText()
        
        stop_words = wordless_stop_words.wordless_get_stop_words(self.main, lang, list_stop_words = list_stop_words)

        self.list_stop_words_preview_results.load_stop_words(stop_words)
        self.label_stop_words_preview_count.setText(self.tr(f'Count of Stop Words: {len(stop_words)}'))

        if list_stop_words == self.tr('Custom List'):
            self.list_stop_words_preview_results.switch_to_custom()

            self.list_stop_words_preview_results.itemChanged.connect(lambda: self.label_stop_words_preview_count.setText(self.tr(f'Count of Stop Words: {self.list_stop_words_preview_results.count()}')))
        else:
            self.list_stop_words_preview_results.switch_to_default()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default)
        else:
            settings = copy.deepcopy(self.main.settings_custom)

        for lang in settings['stop_words']['stop_words']:
            self.__dict__[f'combo_box_stop_words_{lang}'].setCurrentText(settings['stop_words']['stop_words'][lang])

        if not defaults:
            self.combo_box_stop_words_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['stop_words']['preview_lang']))

        if defaults:
            self.main.settings_custom['stop_words']['custom_lists'] = copy.deepcopy(self.main.settings_default['stop_words']['custom_lists'])

        self.combo_box_stop_words_preview_lang.currentTextChanged.emit(self.combo_box_stop_words_preview_lang.currentText())

    def apply_settings(self):
        settings = self.main.settings_custom

        for lang in settings['stop_words']['stop_words']:
            settings['stop_words']['stop_words'][lang] = self.__dict__[f'combo_box_stop_words_{lang}'].currentText()

        if settings['stop_words']['stop_words'][settings['stop_words']['preview_lang']] == self.tr('Custom List'):
            settings['stop_words']['custom_lists'][settings['stop_words']['preview_lang']] = self.list_stop_words_preview_results.get_items()

        return True
