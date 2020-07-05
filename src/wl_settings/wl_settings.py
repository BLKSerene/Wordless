#
# Wordless: Settings - Settings
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_settings import (
    wl_settings_general,
    wl_settings_auto_detection,
    wl_settings_data,
    wl_settings_tags,
    wl_settings_sentence_tokenization,
    wl_settings_word_tokenization,
    wl_settings_word_detokenization,
    wl_settings_pos_tagging,
    wl_settings_lemmatization,
    wl_settings_stop_words,
    wl_settings_measures,
    wl_settings_figs
)
from wl_widgets import wl_button, wl_layout, wl_tree

class Wl_Settings(QDialog):
    wl_settings_changed = pyqtSignal()

    def __init__(self, main):
        super().__init__(main)

        self.main = main

        self.setWindowTitle(self.tr('Settings'))
        self.setFixedSize(800, 550)

        self.tree_settings = wl_tree.Wl_Tree(self)

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('General')]))
        self.tree_settings.topLevelItem(0).addChild(QTreeWidgetItem([self.tr('Import')]))
        self.tree_settings.topLevelItem(0).addChild(QTreeWidgetItem([self.tr('Export')]))

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Auto-detection')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Data')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Tags')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Sentence Tokenization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Word Tokenization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Word Detokenization')]))

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('POS Tagging')]))
        self.tree_settings.topLevelItem(7).addChild(QTreeWidgetItem([self.tr('Tagsets')]))

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Lemmatization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Stop Words')]))

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Measures')]))
        self.tree_settings.topLevelItem(10).addChild(QTreeWidgetItem([self.tr('Dispersion')]))
        self.tree_settings.topLevelItem(10).addChild(QTreeWidgetItem([self.tr('Adjusted Frequency')]))
        self.tree_settings.topLevelItem(10).addChild(QTreeWidgetItem([self.tr('Statistical Significance')]))
        self.tree_settings.topLevelItem(10).addChild(QTreeWidgetItem([self.tr('Effect Size')]))

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Figures')]))

        self.tree_settings.itemSelectionChanged.connect(self.selection_changed)

        self.scroll_area_settings = wl_layout.Wl_Scroll_Area(self)

        self.stacked_widget_settings = QStackedWidget(self)

        self.settings_general = wl_settings_general.Wl_Settings_General(self.main)
        self.settings_import = wl_settings_general.Wl_Settings_Import(self.main)
        self.settings_export = wl_settings_general.Wl_Settings_Export(self.main)
        self.settings_auto_detection = wl_settings_auto_detection.Wl_Settings_Auto_Detection(self.main)
        self.settings_data = wl_settings_data.Wl_Settings_Data(self.main)
        self.settings_tags = wl_settings_tags.Wl_Settings_Tags(self.main)
        self.settings_sentence_tokenization = wl_settings_sentence_tokenization.Wl_Settings_Sentence_Tokenization(self.main)
        self.settings_word_tokenization = wl_settings_word_tokenization.Wl_Settings_Word_Tokenization(self.main)
        self.settings_word_detokenization = wl_settings_word_detokenization.Wl_Settings_Word_Detokenization(self.main)

        self.settings_pos_tagging = wl_settings_pos_tagging.Wl_Settings_Pos_Tagging(self.main)
        self.settings_tagsets = wl_settings_pos_tagging.Wl_Settings_Tagsets(self.main)

        self.settings_lemmatization = wl_settings_lemmatization.Wl_Settings_Lemmatization(self.main)
        self.settings_stop_words = wl_settings_stop_words.Wl_Settings_Stop_Words(self.main)

        self.settings_dispersion = wl_settings_measures.Wl_Settings_Dispersion(self.main)
        self.settings_adjusted_freq = wl_settings_measures.Wl_Settings_Adjusted_Freq(self.main)
        self.settings_statistical_significance = wl_settings_measures.Wl_Settings_Statistical_Significance(self.main)
        self.settings_effect_size = wl_settings_measures.Wl_Settings_Effect_Size(self.main)

        self.settings_figs = wl_settings_figs.Wl_Settings_Figs(self.main)

        self.settings_all = [
            self.settings_general,
            self.settings_import,
            self.settings_export,
            self.settings_auto_detection,
            self.settings_data,
            self.settings_tags,
            self.settings_sentence_tokenization,
            self.settings_word_tokenization,
            self.settings_word_detokenization,
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

        button_reset_settings = wl_button.Wl_Button_Reset_All_Settings(self)
        button_save = QPushButton(self.tr('Save'), self)
        button_apply = QPushButton(self.tr('Apply'), self)
        button_cancel = QPushButton(self.tr('Cancel'), self)

        button_save.clicked.connect(self.save_settings)
        button_apply.clicked.connect(self.apply_settings)
        button_cancel.clicked.connect(self.reject)

        button_reset_settings.setFixedWidth(150)
        button_save.setFixedWidth(80)
        button_apply.setFixedWidth(80)
        button_cancel.setFixedWidth(80)

        layout_buttons = wl_layout.Wl_Layout()
        layout_buttons.addWidget(button_reset_settings, 0, 0)
        layout_buttons.addWidget(button_save, 0, 2)
        layout_buttons.addWidget(button_apply, 0, 3)
        layout_buttons.addWidget(button_cancel, 0, 4)

        layout_buttons.setColumnStretch(1, 1)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(self.tree_settings, 0, 0)
        self.layout().addWidget(self.scroll_area_settings, 0, 1)
        self.layout().addLayout(layout_buttons, 1, 0, 1, 2)

        self.tree_settings.item_selected_old = self.tree_settings.topLevelItem(0)

    def selection_changed(self):
        settings_cur = None

        if self.tree_settings.selectedItems():
            if self.validate_settings():
                item_selected = self.tree_settings.selectedItems()[0]
                item_selected_text = item_selected.text(0)

                if item_selected_text == self.tr('General'):
                    self.stacked_widget_settings.setCurrentIndex(0)

                    item_selected.setExpanded(True)
                elif item_selected_text == self.tr('Import'):
                    self.stacked_widget_settings.setCurrentIndex(1)
                elif item_selected_text == self.tr('Export'):
                    self.stacked_widget_settings.setCurrentIndex(2)
                elif item_selected_text == self.tr('Auto-detection'):
                    self.stacked_widget_settings.setCurrentIndex(3)
                elif item_selected_text == self.tr('Data'):
                    self.stacked_widget_settings.setCurrentIndex(4)
                elif item_selected_text == self.tr('Tags'):
                    self.stacked_widget_settings.setCurrentIndex(5)
                elif item_selected_text == self.tr('Sentence Tokenization'):
                    self.stacked_widget_settings.setCurrentIndex(6)
                elif item_selected_text == self.tr('Word Tokenization'):
                    self.stacked_widget_settings.setCurrentIndex(7)
                elif item_selected_text == self.tr('Word Detokenization'):
                    self.stacked_widget_settings.setCurrentIndex(8)

                elif item_selected_text == self.tr('POS Tagging'):
                    self.stacked_widget_settings.setCurrentIndex(9)

                    item_selected.setExpanded(True)
                elif item_selected_text == self.tr('Tagsets'):
                    self.stacked_widget_settings.setCurrentIndex(10)

                elif item_selected_text == self.tr('Lemmatization'):
                    self.stacked_widget_settings.setCurrentIndex(11)
                elif item_selected_text == self.tr('Stop Words'):
                    self.stacked_widget_settings.setCurrentIndex(12)

                elif item_selected_text == self.tr('Measures'):
                    item_selected.setExpanded(True)
                elif item_selected_text == self.tr('Dispersion'):
                    self.stacked_widget_settings.setCurrentIndex(13)
                elif item_selected_text == self.tr('Adjusted Frequency'):
                    self.stacked_widget_settings.setCurrentIndex(14)
                elif item_selected_text == self.tr('Statistical Significance'):
                    self.stacked_widget_settings.setCurrentIndex(15)
                elif item_selected_text == self.tr('Effect Size'):
                    self.stacked_widget_settings.setCurrentIndex(16)

                elif item_selected_text == self.tr('Figures'):
                    self.stacked_widget_settings.setCurrentIndex(17)

                self.tree_settings.item_selected_old = item_selected
                self.main.settings_custom['settings']['tab'] = item_selected_text

                # Delay loading of POS tag mappings
                if item_selected_text == self.tr('Tagsets') and not self.settings_tagsets.pos_tag_mappings_loaded:
                    self.settings_tagsets.combo_box_tagsets_lang.currentTextChanged.emit(self.settings_tagsets.combo_box_tagsets_lang.currentText())

                    self.settings_tagsets.pos_tag_mappings_loaded = True
            else:
                self.tree_settings.blockSignals(True)

                self.tree_settings.clearSelection()
                self.tree_settings.item_selected_old.setSelected(True)

                self.tree_settings.blockSignals(False)

    def load_settings(self, defaults = False):
        for settings in self.settings_all:
            settings.load_settings(defaults = defaults)

    def validate_settings(self):
        for settings in self.settings_all:
            if not settings.validate_settings():
                return False

        return True

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

    def load(self, tab = None):
        self.load_settings()

        if tab:
            item_selected = self.tree_settings.findItems(tab, Qt.MatchRecursive)[0]

            self.tree_settings.clearSelection()
            item_selected.setSelected(True)

            if not self.tree_settings.findItems(tab, Qt.MatchExactly):
                item_selected.parent().setExpanded(True)
        else:
            item_selected = self.tree_settings.findItems(self.main.settings_custom['settings']['tab'], Qt.MatchRecursive)[0]
            item_selected.setSelected(True)

        # Calculate width
        for node in self.tree_settings.get_nodes():
            node.setExpanded(True)

        self.tree_settings.setFixedWidth(self.tree_settings.columnWidth(0) + 10)

        for node in self.tree_settings.get_nodes():
            node.setExpanded(False)

        self.exec_()
