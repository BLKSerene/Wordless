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

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from wordless.wl_dialogs import wl_dialogs
from wordless.wl_nlp import (
    wl_nlp_utils,
    wl_stop_word_lists
)
from wordless.wl_settings import wl_settings
from wordless.wl_utils import wl_conversion
from wordless.wl_widgets import (
    wl_boxes,
    wl_item_delegates,
    wl_layouts,
    wl_lists,
    wl_tables
)

_tr = QtCore.QCoreApplication.translate

class Dialog_Preview_Imp(wl_dialogs.Wl_Dialog_Settings):
    def __init__(self, parent):
        super().__init__(
            parent,
            title = _tr('Dialog_Imp', 'Import')
        )

        self.settings_custom = self.main.settings_custom['stop_word_lists']['preview']
        self.settings_default = self.main.settings_default['stop_word_lists']['preview']
        self.preview_lang = self.settings_custom['preview_lang']

        self.radio_button_imp_from_default = QtWidgets.QRadioButton(self.tr('Import from default stop word list:'), self)
        self.combo_box_imp_from_default = wl_boxes.Wl_Combo_Box(self)
        self.radio_button_imp_from_files = QtWidgets.QRadioButton(self.tr('Import from files'), self)

        # Exclude custom stop word lists
        self.combo_box_imp_from_default.addItems(tuple(wl_nlp_utils.to_lang_util_texts(
            self.main,
            util_type = 'stop_word_lists',
            util_codes = self.main.settings_global['stop_word_lists'][self.preview_lang][:-1]
        )))

        self.wrapper_settings.layout().addWidget(self.radio_button_imp_from_default, 0, 0)
        self.wrapper_settings.layout().addWidget(self.combo_box_imp_from_default, 0, 1)
        self.wrapper_settings.layout().addWidget(self.radio_button_imp_from_files, 1, 0, 1, 2)

        self.button_save.setText(self.tr('Import'))

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        if settings['imp'][self.preview_lang] == 'files':
            self.radio_button_imp_from_files.setChecked(True)
        else:
            self.radio_button_imp_from_default.setChecked(True)
            self.combo_box_imp_from_default.setCurrentText(wl_nlp_utils.to_lang_util_text(
                self.main,
                util_type = 'stop_word_lists',
                util_code = settings['imp'][self.preview_lang]
            ))

    def save_settings(self):
        if self.radio_button_imp_from_default.isChecked():
            self.settings_custom['imp'][self.preview_lang] = wl_nlp_utils.to_lang_util_code(
                self.main,
                util_type = 'stop_word_lists',
                util_text = self.combo_box_imp_from_default.currentText()
            )
        else:
            self.settings_custom['imp'][self.preview_lang] = 'files'

class Wl_List_Stop_Words(wl_lists.Wl_List_Add_Ins_Del_Clr_Imp_Exp):
    def __init__(self, parent):
        super().__init__(
            parent,
            new_item_text = _tr('Wl_Settings_Stop_Word_Lists', 'New stop word'),
            settings = 'stop_words',
            exp_file_name = 'wordless_stop_words.txt'
        )

    def data_changed_default(self):
        super().data_changed()

        self.button_clr.setEnabled(False)

    def selection_changed_default(self):
        super().selection_changed()

        self.button_ins.setEnabled(False)
        self.button_del.setEnabled(False)

    def switch_to_custom(self):
        self.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked | QtWidgets.QAbstractItemView.SelectedClicked | QtWidgets.QAbstractItemView.EditKeyPressed)
        self.setDragEnabled(True)

        self.button_add.setEnabled(True)
        self.button_imp.setEnabled(True)

        self.model().dataChanged.disconnect()
        self.selectionModel().selectionChanged.disconnect()

        self.model().dataChanged.connect(self.data_changed)
        self.selectionModel().selectionChanged.connect(self.selection_changed)

        self.model().dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def switch_to_default(self):
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setDragEnabled(False)

        self.button_add.setEnabled(False)
        self.button_imp.setEnabled(False)

        self.model().dataChanged.disconnect()
        self.selectionModel().selectionChanged.disconnect()

        self.model().dataChanged.connect(self.data_changed)
        self.model().dataChanged.connect(self.data_changed_default)
        self.selectionModel().selectionChanged.connect(self.selection_changed)
        self.selectionModel().selectionChanged.connect(self.selection_changed_default)

        self.model().dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def imp_list(self):
        preview_lang = self.main.settings_custom['stop_word_lists']['preview']['preview_lang']

        if tuple(wl_nlp_utils.to_lang_util_texts(
            self.main,
            util_type = 'stop_word_lists',
            util_codes = self.main.settings_global['stop_word_lists'][preview_lang][:-1]
        )):
            if Dialog_Preview_Imp(self).load():
                preview_imp = self.main.settings_custom['stop_word_lists']['preview']['imp'][preview_lang]

                if preview_imp == 'files':
                    super().imp_list()
                else:
                    stop_words = wl_stop_word_lists.wl_get_stop_word_list(self.main, preview_lang, stop_word_list = preview_imp)

                    self.load_items(sorted(stop_words))
        # Do not show options if there are no default stop word lists to import from
        else:
            super().imp_list()

class Wl_Settings_Stop_Word_Lists(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_global = self.main.settings_global['stop_word_lists']
        self.settings_default = self.main.settings_default['stop_word_lists']
        self.settings_custom = self.main.settings_custom['stop_word_lists']

        # Stop Word Lists Settings
        self.group_box_stop_word_list_settings = QtWidgets.QGroupBox(self.tr('Stop Word List Settings'), self)

        self.table_stop_word_lists = wl_tables.Wl_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('Stop Word List')
            ],
            editable = True
        )
        self.checkbox_case_sensitive = QtWidgets.QCheckBox(self.tr('Case-sensitive'), self)

        self.table_stop_word_lists.setFixedHeight(370)
        self.table_stop_word_lists.verticalHeader().setHidden(True)
        self.table_stop_word_lists.model().setRowCount(len(self.settings_global))

        self.table_stop_word_lists.model().dataChanged.connect(self.stop_word_list_changed)

        self.table_stop_word_lists.disable_updates()

        for i, lang in enumerate(self.settings_global):
            self.table_stop_word_lists.model().setItem(i, 0, QtGui.QStandardItem(wl_conversion.to_lang_text(self.main, lang)))
            self.table_stop_word_lists.model().setItem(i, 1, QtGui.QStandardItem())

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
        self.group_box_preview = QtWidgets.QGroupBox(self.tr('Preview'), self)

        self.label_preview_lang = QtWidgets.QLabel(self.tr('Select language:'), self)
        self.combo_box_preview_lang = wl_boxes.Wl_Combo_Box(self)
        self.combo_box_preview_lang.addItems(wl_conversion.to_lang_texts(self.main, self.settings_global))
        self.label_preview_num = QtWidgets.QLabel('', self)

        self.list_preview_results = Wl_List_Stop_Words(self)

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

        self.layout().addWidget(self.group_box_stop_word_list_settings, 0, 0)
        self.layout().addWidget(self.group_box_preview, 1, 0)

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
        self.label_preview_num.setText(self.tr('Number of stop words: ') + f'{len(stop_words):,}')

        if list_stop_words == 'custom':
            self.list_preview_results.switch_to_custom()

            self.list_preview_results.model().dataChanged.connect(lambda: self.label_preview_num.setText(self.tr('Number of stop words: ') + f'{self.list_preview_results.model().rowCount():,}'))
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
