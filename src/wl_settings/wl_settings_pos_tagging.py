#
# Wordless: Settings - POS Tagging
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_dialog_misc, wl_msg_box
from wl_tagsets import wl_tagset_universal
from wl_text import wl_word_tokenization, wl_pos_tagging
from wl_utils import wl_conversion, wl_threading
from wl_widgets import wl_box, wl_layout, wl_table, wl_tree

class Wl_Worker_Preview_Pos_Tagger(wl_threading.Wl_Worker_No_Progress):
    worker_done = pyqtSignal(str, list)

    def run(self):
        preview_results = []

        preview_lang = self.main.settings_custom['pos_tagging']['preview_lang']
        preview_samples = self.main.settings_custom['pos_tagging']['preview_samples']

        for line in preview_samples.split('\n'):
            line = line.strip()

            if line:
                tokens = wl_word_tokenization.wl_word_tokenize(
                    self.main, line,
                    lang = preview_lang
                )

                tokens_tagged = wl_pos_tagging.wl_pos_tag(
                    self.main, tokens,
                    lang = preview_lang,
                    pos_tagger = self.pos_tagger,
                    tagset = self.tagset
                )

                preview_results.append(' '.join([f'{token}_{tag}' for token, tag in tokens_tagged]))
            else:
                preview_results.append('')

        self.worker_done.emit(preview_samples, preview_results)

class Wl_Worker_Fetch_Data_Tagsets(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(list)

    def run(self):
        settings_custom = self.main.settings_custom['tagsets']

        preview_lang = settings_custom['preview_lang']
        preview_pos_tagger = settings_custom['preview_pos_tagger'][preview_lang]
        mappings = settings_custom['mappings'][preview_lang][preview_pos_tagger]

        self.progress_updated.emit(self.tr('Updating table ...'))

        time.sleep(0.1)

        self.worker_done.emit(mappings)

# POS Tagging
class Wl_Settings_Pos_Tagging(wl_tree.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

        settings_global = self.main.settings_global['pos_taggers']

        # POS Tagger Settings
        group_box_pos_tagger_settings = QGroupBox(self.tr('POS Tagger Settings'), self)

        self.table_pos_taggers = wl_table.Wl_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('POS Taggers')
            ],
            cols_stretch = [
                self.tr('POS Taggers')
            ]
        )

        self.checkbox_to_universal_pos_tags = QCheckBox(self.tr('Convert all POS tags to universal POS tags'))

        self.table_pos_taggers.verticalHeader().setHidden(True)
        self.table_pos_taggers.setRowCount(len(settings_global))

        for i, lang in enumerate(settings_global):
            self.table_pos_taggers.setItem(i, 0, QTableWidgetItem(wl_conversion.to_lang_text(self.main, lang)))

            self.__dict__[f'combo_box_pos_tagger_{lang}'] = wl_box.Wl_Combo_Box(self)

            self.__dict__[f'combo_box_pos_tagger_{lang}'].addItems(settings_global[lang])

            self.__dict__[f'combo_box_pos_tagger_{lang}'].currentTextChanged.connect(lambda text, lang = lang: self.pos_taggers_changed(lang))

            self.table_pos_taggers.setCellWidget(i, 1, self.__dict__[f'combo_box_pos_tagger_{lang}'])

        self.checkbox_to_universal_pos_tags.stateChanged.connect(self.preview_results_changed)

        group_box_pos_tagger_settings.setLayout(wl_layout.Wl_Layout())
        group_box_pos_tagger_settings.layout().addWidget(self.table_pos_taggers, 0, 0)
        group_box_pos_tagger_settings.layout().addWidget(self.checkbox_to_universal_pos_tags, 1, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_pos_tagging_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_pos_tagging_preview_lang = wl_box.Wl_Combo_Box(self)
        self.label_pos_tagging_preview_processing = QLabel('', self)
        self.text_edit_pos_tagging_preview_samples = QTextEdit(self)
        self.text_edit_pos_tagging_preview_results = QTextEdit(self)

        self.combo_box_pos_tagging_preview_lang.addItems(wl_conversion.to_lang_text(self.main, list(settings_global)))

        self.text_edit_pos_tagging_preview_samples.setAcceptRichText(False)
        self.text_edit_pos_tagging_preview_results.setReadOnly(True)

        self.combo_box_pos_tagging_preview_lang.currentTextChanged.connect(self.preview_changed)
        self.combo_box_pos_tagging_preview_lang.currentTextChanged.connect(self.preview_results_changed)
        self.text_edit_pos_tagging_preview_samples.textChanged.connect(self.preview_changed)
        self.text_edit_pos_tagging_preview_samples.textChanged.connect(self.preview_results_changed)
        self.text_edit_pos_tagging_preview_results.textChanged.connect(self.preview_changed)

        layout_preview_settings = wl_layout.Wl_Layout()
        layout_preview_settings.addWidget(self.label_pos_tagging_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_pos_tagging_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_pos_tagging_preview_processing, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(wl_layout.Wl_Layout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        group_box_preview.layout().addWidget(self.text_edit_pos_tagging_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_pos_tagging_preview_results, 1, 1)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(group_box_pos_tagger_settings, 0, 0)
        self.layout().addWidget(group_box_preview, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(0, 3)
        self.layout().setRowStretch(1, 2)

    def pos_taggers_changed(self, lang):
        settings_custom = self.main.settings_custom['pos_tagging']

        if lang == settings_custom['preview_lang']:
            self.preview_results_changed()

    def preview_changed(self):
        settings_custom = self.main.settings_custom['pos_tagging']

        settings_custom['preview_lang'] = wl_conversion.to_lang_code(self.main, self.combo_box_pos_tagging_preview_lang.currentText())
        settings_custom['preview_samples'] = self.text_edit_pos_tagging_preview_samples.toPlainText()
        settings_custom['preview_results'] = self.text_edit_pos_tagging_preview_results.toPlainText()

    def preview_results_changed(self):
        settings_custom = self.main.settings_custom['pos_tagging']

        if settings_custom['preview_samples']:
            if self.combo_box_pos_tagging_preview_lang.isEnabled():
                self.__dict__[f"combo_box_pos_tagger_{settings_custom['preview_lang']}"].setEnabled(False)
                self.combo_box_pos_tagging_preview_lang.setEnabled(False)

                self.label_pos_tagging_preview_processing.setText(self.tr('Processing text ...'))

                pos_tagger = self.__dict__[f"combo_box_pos_tagger_{settings_custom['preview_lang']}"].currentText()

                if self.checkbox_to_universal_pos_tags.isChecked():
                    tagset = 'universal'
                else:
                    tagset = 'default'

                worker_preview_pos_tagger = Wl_Worker_Preview_Pos_Tagger(
                    self.main,
                    update_gui = self.update_gui,
                    pos_tagger = pos_tagger,
                    tagset = tagset
                )

                self.thread_preview_pos_tagger = wl_threading.Wl_Thread_No_Progress(worker_preview_pos_tagger)
                self.thread_preview_pos_tagger.start_worker()
        else:
            self.text_edit_pos_tagging_preview_results.clear()

    def update_gui(self, preview_samples, preview_results):
        self.label_pos_tagging_preview_processing.setText('')

        self.__dict__[f"combo_box_pos_tagger_{settings_custom['preview_lang']}"].setEnabled(True)
        self.combo_box_pos_tagging_preview_lang.setEnabled(True)

        if preview_samples == settings_custom['preview_samples']:
            self.text_edit_pos_tagging_preview_results.setPlainText('\n'.join(preview_results))
        else:
            self.preview_results_changed()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default)
        else:
            settings = copy.deepcopy(self.main.settings_custom)

        for lang in settings['pos_tagging']['pos_taggers']:
            self.__dict__[f'combo_box_pos_tagger_{lang}'].blockSignals(True)

            self.__dict__[f'combo_box_pos_tagger_{lang}'].setCurrentText(settings['pos_tagging']['pos_taggers'][lang])

            self.__dict__[f'combo_box_pos_tagger_{lang}'].blockSignals(False)

        self.checkbox_to_universal_pos_tags.blockSignals(True)

        self.checkbox_to_universal_pos_tags.setChecked(settings['pos_tagging']['to_universal_pos_tags'])

        self.checkbox_to_universal_pos_tags.blockSignals(False)

        if not defaults:
            self.combo_box_pos_tagging_preview_lang.blockSignals(True)
            self.text_edit_pos_tagging_preview_samples.blockSignals(True)

            self.combo_box_pos_tagging_preview_lang.setCurrentText(wl_conversion.to_lang_text(self.main, settings['pos_tagging']['preview_lang']))
            self.text_edit_pos_tagging_preview_samples.setText(settings['pos_tagging']['preview_samples'])
            self.text_edit_pos_tagging_preview_results.setText(settings['pos_tagging']['preview_results'])

            self.combo_box_pos_tagging_preview_lang.blockSignals(False)
            self.text_edit_pos_tagging_preview_samples.blockSignals(False)

    def apply_settings(self):
        settings = self.main.settings_custom

        for lang in settings['pos_tagging']['pos_taggers']:
            settings['pos_tagging']['pos_taggers'][lang] = self.__dict__[f'combo_box_pos_tagger_{lang}'].currentText()

        settings['pos_tagging']['to_universal_pos_tags'] = self.checkbox_to_universal_pos_tags.isChecked()

        return True

# POS Tagging - Tagsets
class Wl_Settings_Tagsets(wl_tree.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

        self.pos_tag_mappings_loaded = False

        settings_global = self.main.settings_global['pos_taggers']

        self.settings_tagsets = QWidget(self)

        # Preview Settings
        group_box_preview_settings = QGroupBox(self.tr('Preview Settings:'), self)

        self.label_tagsets_lang = QLabel(self.tr('Language:'), self)
        self.combo_box_tagsets_lang = wl_box.Wl_Combo_Box(self)
        self.label_tagsets_pos_tagger = QLabel(self.tr('POS Tagger:'), self)
        self.combo_box_tagsets_pos_tagger = wl_box.Wl_Combo_Box_Adjustable(self)

        self.combo_box_tagsets_lang.addItems(wl_conversion.to_lang_text(self.main, list(settings_global)))

        self.combo_box_tagsets_lang.currentTextChanged.connect(self.preview_lang_changed)
        self.combo_box_tagsets_pos_tagger.currentTextChanged.connect(self.preview_pos_tagger_changed)

        group_box_preview_settings.setLayout(wl_layout.Wl_Layout())
        group_box_preview_settings.layout().addWidget(self.label_tagsets_lang, 0, 0)
        group_box_preview_settings.layout().addWidget(self.combo_box_tagsets_lang, 0, 1, Qt.AlignLeft)
        group_box_preview_settings.layout().addWidget(self.label_tagsets_pos_tagger, 1, 0)
        group_box_preview_settings.layout().addWidget(self.combo_box_tagsets_pos_tagger, 1, 1, Qt.AlignLeft)

        group_box_preview_settings.layout().setColumnStretch(2, 1)

        # Mapping Settings
        group_box_mapping_settings = QGroupBox(self.tr('Mapping Settings'))

        self.label_tagsets_num_pos_tags = QLabel('', self)
        self.button_tagsets_reset = QPushButton(self.tr('Reset'), self)
        self.button_tagsets_reset_all = QPushButton(self.tr('Reset All'), self)
        self.table_mappings = wl_table.Wl_Table(
            self,
            headers = [
                self.tr('POS Tag'),
                self.tr('Universal POS Tag'),
                self.tr('Description'),
                self.tr('Examples')
            ]
        )

        self.button_tagsets_reset.setFixedWidth(100)
        self.button_tagsets_reset_all.setFixedWidth(100)

        self.button_tagsets_reset.clicked.connect(self.reset_mappings)
        self.button_tagsets_reset_all.clicked.connect(self.reset_all_mappings)

        group_box_mapping_settings.setLayout(wl_layout.Wl_Layout())
        group_box_mapping_settings.layout().addWidget(self.label_tagsets_num_pos_tags, 0, 0)
        group_box_mapping_settings.layout().addWidget(self.button_tagsets_reset, 0, 2)
        group_box_mapping_settings.layout().addWidget(self.button_tagsets_reset_all, 0, 3)
        group_box_mapping_settings.layout().addWidget(self.table_mappings, 1, 0, 1, 4)

        group_box_mapping_settings.layout().setColumnStretch(1, 1)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(group_box_preview_settings, 0, 0)
        self.layout().addWidget(group_box_mapping_settings, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(1, 1)

    def preview_lang_changed(self):
        settings_global = self.main.settings_global['pos_taggers']
        settings_custom = self.main.settings_custom['tagsets']

        settings_custom['preview_lang'] = wl_conversion.to_lang_code(
            self.main,
            self.combo_box_tagsets_lang.currentText()
        )

        preview_lang = settings_custom['preview_lang']

        self.combo_box_tagsets_pos_tagger.blockSignals(True)

        self.combo_box_tagsets_pos_tagger.clear()

        self.combo_box_tagsets_pos_tagger.addItems(settings_global[preview_lang])
        self.combo_box_tagsets_pos_tagger.setCurrentText(settings_custom['preview_pos_tagger'][preview_lang])

        self.combo_box_tagsets_pos_tagger.blockSignals(False)

        self.combo_box_tagsets_pos_tagger.currentTextChanged.emit('')

    def preview_pos_tagger_changed(self):
        settings_custom = self.main.settings_custom['tagsets']

        settings_custom['preview_pos_tagger'][settings_custom['preview_lang']] = self.combo_box_tagsets_pos_tagger.currentText()

        self.combo_box_tagsets_lang.setEnabled(False)
        self.combo_box_tagsets_pos_tagger.setEnabled(False)
        self.button_tagsets_reset.setEnabled(False)
        self.button_tagsets_reset_all.setEnabled(False)

        dialog_progress = wl_dialog_misc.Wl_Dialog_Progress_Fetch_Data(self.main)

        worker_fetch_data = Wl_Worker_Fetch_Data_Tagsets(
            self.main,
            dialog_progress = dialog_progress,
            update_gui = self.update_gui
        )

        thread_fetch_data = wl_threading.Wl_Thread(worker_fetch_data)
        thread_fetch_data.start()

        dialog_progress.show()
        dialog_progress.raise_()

        thread_fetch_data.quit()
        thread_fetch_data.wait()

    def update_gui(self, mappings):
        self.table_mappings.hide()
        self.table_mappings.blockSignals(True)
        self.table_mappings.setUpdatesEnabled(False)

        self.table_mappings.clear_table()
        self.table_mappings.setRowCount(len(mappings))

        for i, (tag, tag_universal, description, examples) in enumerate(mappings):
            combo_box_tag_univsersal = wl_box.Wl_Combo_Box(self.main)

            combo_box_tag_univsersal.addItems([
                'ADJ',
                'ADP',
                'ADV',
                'AUX',
                'CONJ', # Coordinating/Subordinating Conjunctions
                'CCONJ',
                'SCONJ',
                'DET',
                'INTJ',
                'NOUN',
                'PROPN',
                'NUM',
                'PART',
                'PRON',
                'VERB',

                'PUNCT',
                'SYM',
                'X'
            ])

            combo_box_tag_univsersal.setCurrentText(tag_universal)
            combo_box_tag_univsersal.setEditable(True)

            self.table_mappings.setItem(i, 0, QTableWidgetItem(tag))
            self.table_mappings.setCellWidget(i, 1, combo_box_tag_univsersal)
            self.table_mappings.setItem(i, 2, QTableWidgetItem(description))
            self.table_mappings.setItem(i, 3, QTableWidgetItem(examples))

        self.table_mappings.blockSignals(False)
        self.table_mappings.setUpdatesEnabled(True)
        self.table_mappings.show()

        self.table_mappings.itemChanged.emit(self.table_mappings.item(0, 0))

        # Disable editing if the default tagset is Universal POS tags
        if mappings == wl_tagset_universal.mappings:
            for i in range(self.table_mappings.rowCount()):
                self.table_mappings.cellWidget(i, 1).setEnabled(False)

        self.label_tagsets_num_pos_tags.setText(self.tr(f'Number of POS Tags: {self.table_mappings.rowCount()}'))

        self.combo_box_tagsets_lang.setEnabled(True)
        self.combo_box_tagsets_pos_tagger.setEnabled(True)
        self.button_tagsets_reset.setEnabled(True)
        self.button_tagsets_reset_all.setEnabled(True)

    def reset_currently_shown_table(self):
        settings_custom = self.main.settings_custom['tagsets']

        preview_lang = settings_custom['preview_lang']
        preview_pos_tagger = settings_custom['preview_pos_tagger'][preview_lang]
        mappings = copy.deepcopy(self.main.settings_default['tagsets']['mappings'][preview_lang][preview_pos_tagger])

        self.table_mappings.hide()
        self.table_mappings.blockSignals(True)
        self.table_mappings.setUpdatesEnabled(False)

        for i in range(self.table_mappings.rowCount()):
            self.table_mappings.cellWidget(i, 1).setCurrentText(mappings[i][1])

        self.table_mappings.blockSignals(False)
        self.table_mappings.setUpdatesEnabled(True)
        self.table_mappings.show()

        self.table_mappings.itemChanged.emit(self.table_mappings.item(0, 0))

        settings_custom['mappings'][preview_lang][preview_pos_tagger] = mappings

    def reset_mappings(self):
        if wl_msg_box.wl_msg_box_reset_mappings(self.main):
            self.reset_currently_shown_table()

    def reset_all_mappings(self):
        if wl_msg_box.wl_msg_box_reset_all_mappings(self.main):
            settings_custom['mappings'] = copy.deepcopy(self.main.settings_default['tagsets']['mappings'])

            self.reset_currently_shown_table()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default)
        else:
            settings = copy.deepcopy(self.main.settings_custom)

        if not defaults:
            self.combo_box_tagsets_lang.blockSignals(True)
            self.combo_box_tagsets_pos_tagger.blockSignals(True)

            self.combo_box_tagsets_lang.setCurrentText(wl_conversion.to_lang_text(self.main, settings['tagsets']['preview_lang']))
            self.combo_box_tagsets_pos_tagger.setCurrentText(settings['tagsets']['preview_pos_tagger'][settings['tagsets']['preview_lang']])

            self.combo_box_tagsets_lang.blockSignals(False)
            self.combo_box_tagsets_pos_tagger.blockSignals(False)

    def apply_settings(self):
        settings = self.main.settings_custom

        if self.pos_tag_mappings_loaded:
            preview_lang = settings['tagsets']['preview_lang']
            preview_pos_tagger = settings['tagsets']['preview_pos_tagger'][preview_lang]

            for i in range(self.table_mappings.rowCount()):
                settings['tagsets']['mappings'][preview_lang][preview_pos_tagger][i][1] = self.table_mappings.cellWidget(i, 1).currentText()

        return True
