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

from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (
    QAbstractItemView, QDialog, QHeaderView, QMessageBox, QPushButton,
    QStackedWidget, QTreeView, QWidget
)

from wordless.wl_checking import wl_checking_misc
from wordless.wl_dialogs import wl_msg_boxes
from wordless.wl_widgets import wl_buttons, wl_layouts

class Wl_Settings_Node(QWidget):
    def __init__(self, main):
        super().__init__()

        self.main = main

    def wl_msg_box_path_empty(self):
        wl_msg_boxes.Wl_Msg_Box_Warning(
            self.main,
            title = self.tr('Empty Path'),
            text = self.tr('''
                <div>The path should not be left empty!</div>
            '''),
        ).open()

    def wl_msg_box_path_not_found(self, path):
        wl_msg_boxes.Wl_Msg_Box_Warning(
            self.main,
            title = self.tr('Path not Found'),
            text = self.tr('''
                <div>The specified path "{}" could not be found!</div>
                <div>Please check your settings and try again.</div>
            ''').format(path),
        ).open()

    def wl_msg_box_path_is_dir(self, path):
        wl_msg_boxes.Wl_Msg_Box_Warning(
            self.main,
            title = self.tr('Invalid File Path'),
            text = self.tr('''
                <div>The specified path "{}" should be a file, not a directory!</div>
                <div>Please check your settings and try again.</div>
            ''').format(path),
        ).open()

    def wl_msg_box_path_not_dir(self, path):
        wl_msg_boxes.Wl_Msg_Box_Warning(
            self.main,
            title = self.tr('Invalid Directory Path'),
            text = self.tr('''
                <div>The specified path "{}" should be a directory, not a file!</div>
                <div>Please check your settings and try again.</div>
            ''').format(path),
        ).open()

    def validate_path_file(self, line_edit):
        path = line_edit.text().strip()
        path_ok = True

        if path:
            if not os.path.exists(path):
                self.wl_msg_box_path_not_found(path)

                path_ok = False
            elif os.path.isdir(path):
                self.wl_msg_box_path_is_dir(path)

                path_ok = False
        else:
            self.wl_msg_box_path_empty()

            path_ok = False

        if not path_ok:
            line_edit.setFocus()
            line_edit.selectAll()

        return path_ok

    def validate_path_dir(self, line_edit):
        path = line_edit.text().strip()
        path_ok = True

        if path:
            if not os.path.exists(path):
                self.wl_msg_box_path_not_found(path)

                path_ok = False
            elif not os.path.isdir(path):
                self.wl_msg_box_path_not_dir(path)

                path_ok = False
        else:
            self.wl_msg_box_path_empty()

            path_ok = False

        if not path_ok:
            line_edit.setFocus()
            line_edit.selectAll()

        return path_ok

    def confirm_path(self, line_edit):
        path = line_edit.text().strip()
        path_ok = True

        if path:
            if not os.path.exists(path):
                reply = QMessageBox.question(
                    self.main,
                    self.tr('Path Not Exist'),
                    self.tr('''
                        {}
                        <body>
                            <div>The specified path "{}" does not exist.</div>
                            <div>Do you want to create the directory?</div>
                        </body>
                    ''').format(self.main.settings_global['styles']['style_dialog'], path),
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    wl_checking_misc.check_dir(path)
                else:
                    path_ok = False
            elif not os.path.isdir(path):
                self.wl_msg_box_path_not_dir(path)

                path_ok = False
        else:
            self.wl_msg_box_path_empty()

            path_ok = False

        if not path_ok:
            line_edit.setFocus()
            line_edit.selectAll()

        return path_ok

    def validate_settings(self):
        return True

    def apply_settings(self):
        return True

class Wl_Settings(QDialog):
    wl_settings_changed = pyqtSignal()

    def __init__(self, main):
        super().__init__(main)

        # Avoid circular imports
        from wordless.wl_settings import (
            wl_settings_general,
            wl_settings_files,
            wl_settings_sentence_tokenization,
            wl_settings_word_tokenization,
            wl_settings_syl_tokenization,
            wl_settings_pos_tagging,
            wl_settings_lemmatization,
            wl_settings_stop_word_lists,
            wl_settings_measures,
            wl_settings_tables,
            wl_settings_figs
        )

        self.main = main

        self.setWindowTitle(self.tr('Settings'))
        self.resize(QSize(1024, 768))

        self.tree_settings = QTreeView(self)
        self.tree_settings.setModel(QStandardItemModel())
        self.tree_settings.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tree_settings.setHeaderHidden(True)
        self.tree_settings.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tree_settings.header().setStretchLastSection(False)

        self.tree_settings.model().appendRow(QStandardItem(self.tr('General')))
        self.tree_settings.model().item(0).appendRow(QStandardItem(self.tr('Import')))
        self.tree_settings.model().item(0).appendRow(QStandardItem(self.tr('Export')))

        self.tree_settings.model().appendRow(QStandardItem(self.tr('Files')))
        self.tree_settings.model().item(1).appendRow(QStandardItem(self.tr('Tags')))

        self.tree_settings.model().appendRow(QStandardItem(self.tr('Sentence Tokenization')))
        self.tree_settings.model().appendRow(QStandardItem(self.tr('Word Tokenization')))
        self.tree_settings.model().appendRow(QStandardItem(self.tr('Syllable Tokenization')))

        self.tree_settings.model().appendRow(QStandardItem(self.tr('Part-of-speech Tagging')))
        self.tree_settings.model().item(5).appendRow(QStandardItem(self.tr('Tagsets')))

        self.tree_settings.model().appendRow(QStandardItem(self.tr('Lemmatization')))
        self.tree_settings.model().appendRow(QStandardItem(self.tr('Stop Word Lists')))

        self.tree_settings.model().appendRow(QStandardItem(self.tr('Measures')))
        self.tree_settings.model().item(8).appendRow(QStandardItem(self.tr('Dispersion')))
        self.tree_settings.model().item(8).appendRow(QStandardItem(self.tr('Adjusted Frequency')))
        self.tree_settings.model().item(8).appendRow(QStandardItem(self.tr('Statistical Significance')))
        self.tree_settings.model().item(8).appendRow(QStandardItem(self.tr('Bayes Factor')))
        self.tree_settings.model().item(8).appendRow(QStandardItem(self.tr('Effect Size')))

        self.tree_settings.model().appendRow(QStandardItem(self.tr('Tables')))
        self.tree_settings.model().item(9).appendRow(QStandardItem(self.tr('Profiler')))

        self.tree_settings.model().appendRow(QStandardItem(self.tr('Figures')))

        # Calculate width
        for i in range(self.tree_settings.model().rowCount()):
            self.tree_settings.setExpanded(self.tree_settings.model().item(i, 0).index(), True)

        self.tree_settings.setFixedWidth(self.tree_settings.columnWidth(0) + 10)

        for i in range(self.tree_settings.model().rowCount()):
            self.tree_settings.setExpanded(self.tree_settings.model().item(i, 0).index(), False)

        self.tree_settings.selectionModel().selectionChanged.connect(self.selection_changed)

        self.stacked_widget_settings = QStackedWidget(self)

        # General
        self.settings_general = wl_settings_general.Wl_Settings_General(self.main)
        self.settings_general_imp = wl_settings_general.Wl_Settings_General_Imp(self.main)
        self.settings_general_exp = wl_settings_general.Wl_Settings_General_Exp(self.main)

        # Files
        self.settings_files = wl_settings_files.Wl_Settings_Files(self.main)
        self.settings_files_tags = wl_settings_files.Wl_Settings_Files_Tags(self.main)

        self.settings_sentence_tokenization = wl_settings_sentence_tokenization.Wl_Settings_Sentence_Tokenization(self.main)
        self.settings_word_tokenization = wl_settings_word_tokenization.Wl_Settings_Word_Tokenization(self.main)
        self.settings_syl_tokenization = wl_settings_syl_tokenization.Wl_Settings_Syl_Tokenization(self.main)

        # POS Tagging
        self.settings_pos_tagging = wl_settings_pos_tagging.Wl_Settings_Pos_Tagging(self.main)
        self.settings_pos_tagging_tagsets = wl_settings_pos_tagging.Wl_Settings_Pos_Tagging_Tagsets(self.main)

        self.settings_lemmatization = wl_settings_lemmatization.Wl_Settings_Lemmatization(self.main)
        self.settings_stop_words = wl_settings_stop_word_lists.Wl_Settings_Stop_Word_Lists(self.main)

        # Measures
        self.settings_measures_dispersion = wl_settings_measures.Wl_Settings_Measures_Dispersion(self.main)
        self.settings_measures_adjusted_freq = wl_settings_measures.Wl_Settings_Measures_Adjusted_Freq(self.main)
        self.settings_measures_statistical_significance = wl_settings_measures.Wl_Settings_Measures_Statistical_Significance(self.main)
        self.settings_measures_bayes_factor = wl_settings_measures.Wl_Settings_Measures_Bayes_Factor(self.main)
        self.settings_measures_effect_size = wl_settings_measures.Wl_Settings_Measures_Effect_Size(self.main)

        # Tables
        self.settings_tables = wl_settings_tables.Wl_Settings_Tables(self.main)
        self.settings_tables_profiler = wl_settings_tables.Wl_Settings_Tables_Profiler(self.main)

        self.settings_figs = wl_settings_figs.Wl_Settings_Figs(self.main)

        self.settings_all = [
            self.settings_general,
            self.settings_general_imp,
            self.settings_general_exp,
            self.settings_files,
            self.settings_files_tags,
            self.settings_sentence_tokenization,
            self.settings_word_tokenization,
            self.settings_syl_tokenization,
            self.settings_pos_tagging,
            self.settings_pos_tagging_tagsets,
            self.settings_lemmatization,
            self.settings_stop_words,
            self.settings_measures_dispersion,
            self.settings_measures_adjusted_freq,
            self.settings_measures_statistical_significance,
            self.settings_measures_bayes_factor,
            self.settings_measures_effect_size,
            self.settings_tables,
            self.settings_tables_profiler,
            self.settings_figs
        ]

        for settings in self.settings_all:
            scroll_area_settings = wl_layouts.Wl_Scroll_Area(self)
            scroll_area_settings.setWidget(settings)

            settings.scroll_area_settings = scroll_area_settings

            self.stacked_widget_settings.addWidget(scroll_area_settings)

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
        self.layout().addWidget(self.stacked_widget_settings, 0, 1)
        self.layout().addLayout(layout_buttons, 1, 0, 1, 2)

        self.tree_settings.node_selected_old = self.tree_settings.model().item(0)

    def selection_changed(self, selected, deselected): # pylint: disable=unused-argument
        if self.tree_settings.selectionModel().selectedIndexes():
            if self.validate_settings():
                i_selected = self.tree_settings.selectionModel().currentIndex()
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
                elif node_selected_text == self.tr('Sentence Tokenization'):
                    self.stacked_widget_settings.setCurrentIndex(5)
                elif node_selected_text == self.tr('Word Tokenization'):
                    self.stacked_widget_settings.setCurrentIndex(6)
                elif node_selected_text == self.tr('Syllable Tokenization'):
                    self.stacked_widget_settings.setCurrentIndex(7)
                # POS Tagging
                elif node_selected_text == self.tr('Part-of-speech Tagging'):
                    self.stacked_widget_settings.setCurrentIndex(8)
                elif node_selected_text == self.tr('Tagsets'):
                    self.stacked_widget_settings.setCurrentIndex(9)
                elif node_selected_text == self.tr('Lemmatization'):
                    self.stacked_widget_settings.setCurrentIndex(10)
                elif node_selected_text == self.tr('Stop Word Lists'):
                    self.stacked_widget_settings.setCurrentIndex(11)
                # Measures
                elif node_selected_text == self.tr('Dispersion'):
                    self.stacked_widget_settings.setCurrentIndex(12)
                elif node_selected_text == self.tr('Adjusted Frequency'):
                    self.stacked_widget_settings.setCurrentIndex(13)
                elif node_selected_text == self.tr('Statistical Significance'):
                    self.stacked_widget_settings.setCurrentIndex(14)
                elif node_selected_text == self.tr('Bayes Factor'):
                    self.stacked_widget_settings.setCurrentIndex(15)
                elif node_selected_text == self.tr('Effect Size'):
                    self.stacked_widget_settings.setCurrentIndex(16)
                # Tables
                elif node_selected_text == self.tr('Tables'):
                    self.stacked_widget_settings.setCurrentIndex(17)
                elif node_selected_text == self.tr('Profiler'):
                    self.stacked_widget_settings.setCurrentIndex(18)
                elif node_selected_text == self.tr('Figures'):
                    self.stacked_widget_settings.setCurrentIndex(19)

                if node_selected.hasChildren():
                    self.tree_settings.setExpanded(i_selected, True)

                self.tree_settings.node_selected_old = node_selected
                self.main.settings_custom['settings']['node_cur'] = node_selected_text

                # Delay loading of POS tag mappings
                if node_selected_text == self.tr('Tagsets') and not self.settings_pos_tagging_tagsets.pos_tag_mappings_loaded:
                    self.settings_pos_tagging_tagsets.combo_box_tagsets_lang.currentTextChanged.emit(self.settings_pos_tagging_tagsets.combo_box_tagsets_lang.currentText())

                    self.settings_pos_tagging_tagsets.pos_tag_mappings_loaded = True
            else:
                self.tree_settings.selectionModel().blockSignals(True)

                self.tree_settings.clearSelection()
                self.tree_settings.setCurrentIndex(self.tree_settings.model().findItems(self.main.settings_custom['settings']['node_cur'], Qt.MatchRecursive)[0].index())

                self.tree_settings.selectionModel().blockSignals(False)

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
            self.tree_settings.setCurrentIndex(self.tree_settings.model().findItems(node, Qt.MatchRecursive)[0].index())
        else:
            self.tree_settings.setCurrentIndex(self.tree_settings.model().findItems(self.main.settings_custom['settings']['node_cur'], Qt.MatchRecursive)[0].index())

        # Expand current node
        node_cur = self.tree_settings.model().itemFromIndex(self.tree_settings.selectionModel().currentIndex())

        self.tree_settings.setExpanded(node_cur.index(), True)

        if node_cur.parent():
            self.tree_settings.setExpanded(node_cur.parent().index(), True)

        self.exec_()
