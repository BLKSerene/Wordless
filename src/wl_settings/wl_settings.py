# ----------------------------------------------------------------------
# Wordless: Settings - Settings
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

import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_msg_boxes
from wl_widgets import wl_buttons, wl_layouts

class Wl_Settings_Node(QWidget):
    def __init__(self, main):
        super().__init__()

        self.main = main

    def validate_path(self, line_edit):
        if not os.path.exists(line_edit.text()):
            wl_msg_boxes.wl_msg_box_path_not_exist(self.main, line_edit.text())

            line_edit.setFocus()
            line_edit.selectAll()

            return False
        elif not os.path.isdir(line_edit.text()):
            wl_msg_boxes.wl_msg_box_path_not_dir(self.main, line_edit.text())

            line_edit.setFocus()
            line_edit.selectAll()

            return False
        else:
            return True

    def confirm_path(self, line_edit):
        if not os.path.exists(line_edit.text()):
            reply = wl_msg_boxes.wl_msg_box_path_not_exist_confirm(self.main, line_edit.text())

            if reply == QMessageBox.Yes:
                return True
            else:
                line_edit.setFocus()
                line_edit.selectAll()

                return False
        elif not os.path.isdir(line_edit.text()):
            wl_msg_boxes.wl_msg_box_path_not_dir(self.main, line_edit.text())

            line_edit.setFocus()
            line_edit.selectAll()

            return False
        else:
            return True

    def validate_settings(self):
        return True

    def apply_settings(self):
        return True

class Wl_Settings(QDialog):
    wl_settings_changed = pyqtSignal()

    def __init__(self, main):
        super().__init__(main)

        # Avoid circular imports
        from wl_settings import (
            wl_settings_general,
            wl_settings_files,
            wl_settings_data,
            wl_settings_sentence_tokenization,
            wl_settings_word_tokenization,
            wl_settings_syl_tokenization,
            wl_settings_pos_tagging,
            wl_settings_lemmatization,
            wl_settings_stop_word_lists,
            wl_settings_measures,
            wl_settings_figs
        )

        self.main = main

        self.setWindowTitle(self.tr('Settings'))
        self.setFixedSize(1024, 768)

        self.tree_settings = QTreeView(self)
        self.tree_settings.setModel(QStandardItemModel())

        self.tree_settings.setHeaderHidden(True)
        self.tree_settings.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tree_settings.header().setStretchLastSection(False)

        self.tree_settings.model().appendRow(QStandardItem(self.tr('General')))
        self.tree_settings.model().item(0).appendRow(QStandardItem(self.tr('Import')))
        self.tree_settings.model().item(0).appendRow(QStandardItem(self.tr('Export')))

        self.tree_settings.model().appendRow(QStandardItem(self.tr('Files')))
        self.tree_settings.model().item(1).appendRow(QStandardItem(self.tr('Tags')))

        self.tree_settings.model().appendRow(QStandardItem(self.tr('Data')))
        self.tree_settings.model().appendRow(QStandardItem(self.tr('Sentence Tokenization')))
        self.tree_settings.model().appendRow(QStandardItem(self.tr('Word Tokenization')))
        self.tree_settings.model().appendRow(QStandardItem(self.tr('Syllable Tokenization')))

        self.tree_settings.model().appendRow(QStandardItem(self.tr('POS Tagging')))
        self.tree_settings.model().item(6).appendRow(QStandardItem(self.tr('Tagsets')))

        self.tree_settings.model().appendRow(QStandardItem(self.tr('Lemmatization')))
        self.tree_settings.model().appendRow(QStandardItem(self.tr('Stop Word Lists')))

        self.tree_settings.model().appendRow(QStandardItem(self.tr('Measures')))
        self.tree_settings.model().item(9).appendRow(QStandardItem(self.tr('Dispersion')))
        self.tree_settings.model().item(9).appendRow(QStandardItem(self.tr('Adjusted Frequency')))
        self.tree_settings.model().item(9).appendRow(QStandardItem(self.tr('Statistical Significance')))
        self.tree_settings.model().item(9).appendRow(QStandardItem(self.tr('Effect Size')))

        self.tree_settings.model().appendRow(QStandardItem(self.tr('Figures')))

        # Calculate width
        for i in range(self.tree_settings.model().rowCount()):
            self.tree_settings.setExpanded(self.tree_settings.model().item(i, 0).index(), True)

        self.tree_settings.setFixedWidth(self.tree_settings.columnWidth(0) + 10)

        for i in range(self.tree_settings.model().rowCount()):
            self.tree_settings.setExpanded(self.tree_settings.model().item(i, 0).index(), False)

        self.tree_settings.selectionModel().selectionChanged.connect(self.selection_changed)

        self.scroll_area_settings = wl_layouts.Wl_Scroll_Area(self)

        self.stacked_widget_settings = QStackedWidget(self)

        # General
        self.settings_general = wl_settings_general.Wl_Settings_General(self.main)
        self.settings_imp = wl_settings_general.Wl_Settings_Imp(self.main)
        self.settings_exp = wl_settings_general.Wl_Settings_Exp(self.main)

        # Files
        self.settings_files = wl_settings_files.Wl_Settings_Files(self.main)
        self.settings_tags = wl_settings_files.Wl_Settings_Tags(self.main)

        self.settings_data = wl_settings_data.Wl_Settings_Data(self.main)
        self.settings_sentence_tokenization = wl_settings_sentence_tokenization.Wl_Settings_Sentence_Tokenization(self.main)
        self.settings_word_tokenization = wl_settings_word_tokenization.Wl_Settings_Word_Tokenization(self.main)
        self.settings_syl_tokenization = wl_settings_syl_tokenization.Wl_Settings_Syl_Tokenization(self.main)

        # POS Tagging
        self.settings_pos_tagging = wl_settings_pos_tagging.Wl_Settings_Pos_Tagging(self.main)
        self.settings_tagsets = wl_settings_pos_tagging.Wl_Settings_Tagsets(self.main)

        self.settings_lemmatization = wl_settings_lemmatization.Wl_Settings_Lemmatization(self.main)
        self.settings_stop_words = wl_settings_stop_word_lists.Wl_Settings_Stop_Word_Lists(self.main)

        # Measures
        self.settings_dispersion = wl_settings_measures.Wl_Settings_Dispersion(self.main)
        self.settings_adjusted_freq = wl_settings_measures.Wl_Settings_Adjusted_Freq(self.main)
        self.settings_statistical_significance = wl_settings_measures.Wl_Settings_Statistical_Significance(self.main)
        self.settings_effect_size = wl_settings_measures.Wl_Settings_Effect_Size(self.main)

        self.settings_figs = wl_settings_figs.Wl_Settings_Figs(self.main)

        self.settings_all = [
            self.settings_general,
            self.settings_imp,
            self.settings_exp,
            self.settings_files,
            self.settings_tags,
            self.settings_data,
            self.settings_sentence_tokenization,
            self.settings_word_tokenization,
            self.settings_syl_tokenization,
            self.settings_pos_tagging,
            self.settings_tagsets,
            self.settings_lemmatization,
            self.settings_stop_words,
            self.settings_dispersion,
            self.settings_adjusted_freq,
            self.settings_statistical_significance,
            self.settings_effect_size,
            self.settings_figs
        ]

        for settings in self.settings_all:
            self.stacked_widget_settings.addWidget(settings)

        self.scroll_area_settings.setWidget(self.stacked_widget_settings)

        button_reset_settings = wl_buttons.Wl_Button(self.tr('Reset all settings'), self)
        button_save = QPushButton(self.tr('Save'), self)
        button_apply = QPushButton(self.tr('Apply'), self)
        button_cancel = QPushButton(self.tr('Cancel'), self)

        button_reset_settings.setFixedWidth(180)

        button_reset_settings.clicked.connect(self.reset_all_settings)
        button_save.clicked.connect(self.save_settings)
        button_apply.clicked.connect(self.apply_settings)
        button_cancel.clicked.connect(self.reject)

        layout_buttons = wl_layouts.Wl_Layout()
        layout_buttons.addWidget(button_reset_settings, 0, 0)
        layout_buttons.addWidget(button_save, 0, 2)
        layout_buttons.addWidget(button_apply, 0, 3)
        layout_buttons.addWidget(button_cancel, 0, 4)

        layout_buttons.setColumnStretch(1, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.tree_settings, 0, 0)
        self.layout().addWidget(self.scroll_area_settings, 0, 1)
        self.layout().addLayout(layout_buttons, 1, 0, 1, 2)

        self.tree_settings.node_selected_old = self.tree_settings.model().item(0)

    def selection_changed(self):
        if self.tree_settings.selectionModel().selectedIndexes():
            i_selected = self.tree_settings.selectionModel().currentIndex()

            if self.validate_settings():
                node_selected = self.tree_settings.model().itemFromIndex(i_selected)
                node_selected_text = node_selected.text()

                # General
                if node_selected_text == self.tr('General'):
                    self.stacked_widget_settings.setCurrentIndex(0)
                elif node_selected_text == self.tr('Import'):
                    self.stacked_widget_settings.setCurrentIndex(1)
                elif node_selected_text == self.tr('Export'):
                    self.stacked_widget_settings.setCurrentIndex(2)

                # Files
                elif node_selected_text == self.tr('Files'):
                    self.stacked_widget_settings.setCurrentIndex(3)
                elif node_selected_text == self.tr('Tags'):
                    self.stacked_widget_settings.setCurrentIndex(4)

                elif node_selected_text == self.tr('Data'):
                    self.stacked_widget_settings.setCurrentIndex(5)
                elif node_selected_text == self.tr('Sentence Tokenization'):
                    self.stacked_widget_settings.setCurrentIndex(6)
                elif node_selected_text == self.tr('Word Tokenization'):
                    self.stacked_widget_settings.setCurrentIndex(7)
                elif node_selected_text == self.tr('Syllable Tokenization'):
                    self.stacked_widget_settings.setCurrentIndex(8)

                # POS Tagging
                elif node_selected_text == self.tr('POS Tagging'):
                    self.stacked_widget_settings.setCurrentIndex(9)
                elif node_selected_text == self.tr('Tagsets'):
                    self.stacked_widget_settings.setCurrentIndex(10)

                elif node_selected_text == self.tr('Lemmatization'):
                    self.stacked_widget_settings.setCurrentIndex(11)
                elif node_selected_text == self.tr('Stop Word Lists'):
                    self.stacked_widget_settings.setCurrentIndex(12)

                # Measures
                elif node_selected_text == self.tr('Dispersion'):
                    self.stacked_widget_settings.setCurrentIndex(13)
                elif node_selected_text == self.tr('Adjusted Frequency'):
                    self.stacked_widget_settings.setCurrentIndex(14)
                elif node_selected_text == self.tr('Statistical Significance'):
                    self.stacked_widget_settings.setCurrentIndex(15)
                elif node_selected_text == self.tr('Effect Size'):
                    self.stacked_widget_settings.setCurrentIndex(16)

                elif node_selected_text == self.tr('Figures'):
                    self.stacked_widget_settings.setCurrentIndex(17)

                if node_selected.hasChildren():
                    self.tree_settings.setExpanded(i_selected, True)

                self.tree_settings.node_selected_old = node_selected
                self.main.settings_custom['settings']['node_cur'] = node_selected_text

                # Delay loading of POS tag mappings
                if node_selected_text == self.tr('Tagsets') and not self.settings_tagsets.pos_tag_mappings_loaded:
                    self.settings_tagsets.combo_box_tagsets_lang.currentTextChanged.emit(self.settings_tagsets.combo_box_tagsets_lang.currentText())

                    self.settings_tagsets.pos_tag_mappings_loaded = True
            else:
                self.tree_settings.blockSignals(True)

                self.tree_settings.clearSelection()
                self.tree_settings.selectionModel().setCurrentIndex(i_selected)

                self.tree_settings.blockSignals(False)

    def load_settings(self, defaults = False):
        for settings in self.settings_all:
            settings.load_settings(defaults = defaults)

    def validate_settings(self):
        for settings in self.settings_all:
            if not settings.validate_settings():
                return False

        return True

    def reset_all_settings(self):
        if wl_msg_boxes.wl_msg_box_question(
            main = self.main,
            title = self.tr('Reset All Settings'),
            text = self.tr('''
                <div>Do you want to reset all settings to their defaults?</div>
                <div><b>Warning: This will affect settings on all pages!</b></div>
            ''')
        ):
            self.load_settings(defaults = True)

        self.activateWindow()

    def save_settings(self):
        if self.apply_settings():
            self.accept()

    def apply_settings(self):
        if self.validate_settings():
            for settings in self.settings_all:
                if not settings.apply_settings():
                    return False

            self.wl_settings_changed.emit()

            return True
        else:
            return False

    def load(self, node = None):
        self.load_settings()

        self.tree_settings.clearSelection()

        if node:
            self.tree_settings.selectionModel().setCurrentIndex(self.tree_settings.model().findItems(node, Qt.MatchRecursive)[0].index(), QItemSelectionModel.Select)
        else:
            self.tree_settings.selectionModel().setCurrentIndex(self.tree_settings.model().findItems(self.main.settings_custom['settings']['node_cur'], Qt.MatchRecursive)[0].index(), QItemSelectionModel.Select)

        # Expand current node
        node_cur = self.tree_settings.model().itemFromIndex(self.tree_settings.selectionModel().currentIndex())

        self.tree_settings.setExpanded(node_cur.index(), True)

        if node_cur.parent():
            self.tree_settings.setExpanded(node_cur.parent().index(), True)

        self.exec_()
