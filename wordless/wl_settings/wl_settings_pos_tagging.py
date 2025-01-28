# ----------------------------------------------------------------------
# Wordless: Settings - Part-of-speech Tagging
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

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QStackedWidget,
    QTextEdit
)

from wordless.wl_dialogs import wl_dialogs_misc, wl_msg_boxes
from wordless.wl_nlp import wl_nlp_utils, wl_pos_tagging
from wordless.wl_settings import wl_settings
from wordless.wl_utils import wl_conversion, wl_threading
from wordless.wl_widgets import (
    wl_boxes,
    wl_item_delegates,
    wl_labels,
    wl_layouts,
    wl_tables
)

# Part-of-speech Tagging
class Wl_Settings_Pos_Tagging(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_global = self.main.settings_global['pos_taggers']
        self.settings_default = self.main.settings_default['pos_tagging']
        self.settings_custom = self.main.settings_custom['pos_tagging']

        # Part-of-speech Tagger Settings
        self.group_box_pos_tagger_settings = QGroupBox(self.tr('Part-of-speech Tagger Settings'), self)

        self.table_pos_taggers = wl_tables.Wl_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('Part-of-speech Taggers')
            ],
            editable = True
        )

        self.checkbox_to_universal_pos_tags = QCheckBox(self.tr('Convert all part-of-speech tags to universal part-of-speech tags'))

        self.table_pos_taggers.setFixedHeight(370)
        self.table_pos_taggers.verticalHeader().setHidden(True)
        self.table_pos_taggers.model().setRowCount(len(self.settings_global))

        self.table_pos_taggers.disable_updates()

        for i, lang in enumerate(self.settings_global):
            self.table_pos_taggers.model().setItem(i, 0, QStandardItem(wl_conversion.to_lang_text(self.main, lang)))
            self.table_pos_taggers.model().setItem(i, 1, QStandardItem())

            self.table_pos_taggers.setItemDelegateForRow(i, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
                parent = self.table_pos_taggers,
                items = list(wl_nlp_utils.to_lang_util_texts(
                    self.main,
                    util_type = 'pos_taggers',
                    util_codes = self.settings_global[lang]
                )),
                col = 1
            ))

        self.table_pos_taggers.enable_updates()

        self.group_box_pos_tagger_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_pos_tagger_settings.layout().addWidget(self.table_pos_taggers, 0, 0)
        self.group_box_pos_tagger_settings.layout().addWidget(self.checkbox_to_universal_pos_tags, 1, 0)

        # Preview
        self.group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_preview_lang = wl_boxes.Wl_Combo_Box(self)
        self.button_show_preview = QPushButton(self.tr('Show preview'), self)
        self.text_edit_preview_samples = QTextEdit(self)
        self.text_edit_preview_results = QTextEdit(self)

        self.combo_box_preview_lang.addItems(wl_conversion.to_lang_texts(self.main, self.settings_global))

        self.button_show_preview.setMinimumWidth(140)
        self.text_edit_preview_samples.setAcceptRichText(False)
        self.text_edit_preview_results.setReadOnly(True)

        self.combo_box_preview_lang.currentTextChanged.connect(self.preview_changed)
        self.button_show_preview.clicked.connect(self.preview_results_changed)
        self.text_edit_preview_samples.textChanged.connect(self.preview_changed)
        self.text_edit_preview_results.textChanged.connect(self.preview_changed)

        layout_preview_settings = wl_layouts.Wl_Layout()
        layout_preview_settings.addWidget(self.label_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.button_show_preview, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        self.group_box_preview.setLayout(wl_layouts.Wl_Layout())
        self.group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        self.group_box_preview.layout().addWidget(self.text_edit_preview_samples, 1, 0)
        self.group_box_preview.layout().addWidget(self.text_edit_preview_results, 1, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_pos_tagger_settings, 0, 0)
        self.layout().addWidget(self.group_box_preview, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(1, 1)

    def preview_changed(self):
        self.settings_custom['preview']['preview_lang'] = wl_conversion.to_lang_code(self.main, self.combo_box_preview_lang.currentText())
        self.settings_custom['preview']['preview_samples'] = self.text_edit_preview_samples.toPlainText()
        self.settings_custom['preview']['preview_results'] = self.text_edit_preview_results.toPlainText()

        if self.settings_custom['preview']['preview_samples'].strip():
            self.button_show_preview.setEnabled(True)
        else:
            self.button_show_preview.setEnabled(False)

    def preview_results_changed(self):
        if self.combo_box_preview_lang.isEnabled():
            row = list(self.settings_global.keys()).index(self.settings_custom['preview']['preview_lang'])

            self.table_pos_taggers.itemDelegateForRow(row).set_enabled(False)
            self.combo_box_preview_lang.setEnabled(False)
            self.button_show_preview.setEnabled(False)
            self.text_edit_preview_samples.setEnabled(False)
            self.checkbox_to_universal_pos_tags.setEnabled(False)

            self.button_show_preview.setText(self.tr('Processing...'))

            pos_tagger = wl_nlp_utils.to_lang_util_code(
                self.main,
                util_type = 'pos_taggers',
                util_text = self.table_pos_taggers.model().item(row, 1).text()
            )

            if wl_nlp_utils.check_models(
                self.main,
                langs = [self.settings_custom['preview']['preview_lang']],
                lang_utils = [['default_word_tokenizer', pos_tagger]]
            ):
                if self.checkbox_to_universal_pos_tags.isChecked():
                    tagset = 'universal'
                else:
                    tagset = 'raw'

                worker_preview_pos_tagger = Wl_Worker_Preview_Pos_Tagger(
                    self.main,
                    update_gui = self.update_gui,
                    pos_tagger = pos_tagger,
                    tagset = tagset
                )

                self.thread_preview_pos_tagger = wl_threading.Wl_Thread_No_Progress(worker_preview_pos_tagger)
                self.thread_preview_pos_tagger.start_worker()
            else:
                self.update_gui_err()

    def update_gui(self, preview_results):
        self.text_edit_preview_results.setPlainText('\n'.join(preview_results))

        self.update_gui_err()

    def update_gui_err(self):
        self.button_show_preview.setText(self.tr('Show preview'))

        row = list(self.settings_global.keys()).index(self.settings_custom['preview']['preview_lang'])

        self.table_pos_taggers.itemDelegateForRow(row).set_enabled(True)
        self.combo_box_preview_lang.setEnabled(True)
        self.button_show_preview.setEnabled(True)
        self.text_edit_preview_samples.setEnabled(True)
        self.checkbox_to_universal_pos_tags.setEnabled(True)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Part-of-speech Tagger Settings
        self.table_pos_taggers.disable_updates()

        for i, lang in enumerate(settings['pos_tagger_settings']['pos_taggers']):
            self.table_pos_taggers.model().item(i, 1).setText(wl_nlp_utils.to_lang_util_text(
                self.main,
                util_type = 'pos_taggers',
                util_code = settings['pos_tagger_settings']['pos_taggers'][lang]
            ))

        self.table_pos_taggers.enable_updates()

        self.checkbox_to_universal_pos_tags.blockSignals(True)

        self.checkbox_to_universal_pos_tags.setChecked(settings['pos_tagger_settings']['to_universal_pos_tags'])

        self.checkbox_to_universal_pos_tags.blockSignals(False)

        # Preview
        if not defaults:
            self.combo_box_preview_lang.blockSignals(True)
            self.text_edit_preview_samples.blockSignals(True)

            self.combo_box_preview_lang.setCurrentText(wl_conversion.to_lang_text(self.main, settings['preview']['preview_lang']))
            self.text_edit_preview_samples.setText(settings['preview']['preview_samples'])
            self.text_edit_preview_results.setText(settings['preview']['preview_results'])

            self.combo_box_preview_lang.blockSignals(False)
            self.text_edit_preview_samples.blockSignals(False)

        self.preview_changed()

    def apply_settings(self):
        # Part-of-speech Tagger Settings
        for i, lang in enumerate(self.settings_custom['pos_tagger_settings']['pos_taggers']):
            self.settings_custom['pos_tagger_settings']['pos_taggers'][lang] = wl_nlp_utils.to_lang_util_code(
                self.main,
                util_type = 'pos_taggers',
                util_text = self.table_pos_taggers.model().item(i, 1).text()
            )

        self.settings_custom['pos_tagger_settings']['to_universal_pos_tags'] = self.checkbox_to_universal_pos_tags.isChecked()

        return True

class Wl_Worker_Preview_Pos_Tagger(wl_threading.Wl_Worker_No_Progress):
    worker_done = pyqtSignal(list)

    def run(self):
        preview_results = []

        preview_lang = self.main.settings_custom['pos_tagging']['preview']['preview_lang']
        preview_samples = self.main.settings_custom['pos_tagging']['preview']['preview_samples']

        for line in preview_samples.split('\n'):
            if (line := line.strip()):
                tokens = wl_pos_tagging.wl_pos_tag(
                    self.main, line,
                    lang = preview_lang,
                    pos_tagger = self.pos_tagger,
                    tagset = self.tagset
                )

                preview_results.append(' '.join([f'{str(token)}{token.tag}' for token in tokens]))
            else:
                preview_results.append('')

        self.worker_done.emit(preview_results)

# Part-of-speech Tagging - Tagsets
class Wl_Settings_Pos_Tagging_Tagsets(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_global = self.main.settings_global['pos_taggers']
        self.settings_default = self.main.settings_default['pos_tagging']['tagsets']
        self.settings_custom = self.main.settings_custom['pos_tagging']['tagsets']

        self.pos_tag_mappings_loaded = False

        # Preview Settings
        self.group_box_preview_settings = QGroupBox(self.tr('Preview Settings:'), self)

        self.label_tagsets_lang = QLabel(self.tr('Language:'), self)
        self.combo_box_tagsets_lang = wl_boxes.Wl_Combo_Box(self)
        self.label_tagsets_pos_tagger = QLabel(self.tr('Part-of-speech tagger:'), self)
        self.combo_box_tagsets_pos_tagger = wl_boxes.Wl_Combo_Box_Adjustable(self)

        self.combo_box_tagsets_lang.addItems(wl_conversion.to_lang_texts(self.main, self.settings_global))

        self.combo_box_tagsets_lang.currentTextChanged.connect(self.preview_lang_changed)
        self.combo_box_tagsets_pos_tagger.currentTextChanged.connect(self.preview_pos_tagger_changed)

        self.group_box_preview_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_preview_settings.layout().addWidget(self.label_tagsets_lang, 0, 0)
        self.group_box_preview_settings.layout().addWidget(self.combo_box_tagsets_lang, 0, 1, Qt.AlignLeft)
        self.group_box_preview_settings.layout().addWidget(self.label_tagsets_pos_tagger, 1, 0)
        self.group_box_preview_settings.layout().addWidget(self.combo_box_tagsets_pos_tagger, 1, 1, Qt.AlignLeft)

        self.group_box_preview_settings.layout().setColumnStretch(2, 1)

        # Mapping Settings
        self.group_box_mapping_settings = QGroupBox(self.tr('Mapping Settings'))

        self.stacked_widget_num_pos_tags = QStackedWidget(self)
        self.label_tagsets_num_pos_tags = QLabel('', self)
        self.label_tagsets_uneditable = wl_labels.Wl_Label_Hint(self.tr('* This part-of-speech tagger does not support custom mapping.'), self)
        self.button_tagsets_reset = QPushButton(self.tr('Reset'), self)
        self.button_tagsets_reset_all = QPushButton(self.tr('Reset all'), self)
        self.table_mappings = wl_tables.Wl_Table(
            self,
            headers = [
                self.tr('Part-of-speech Tag'),
                self.tr('Universal Part-of-speech Tag'),
                self.tr('Content/Function Words'),
                self.tr('Description'),
                self.tr('Examples')
            ],
            editable = True
        )

        self.stacked_widget_num_pos_tags.addWidget(self.label_tagsets_num_pos_tags)
        self.stacked_widget_num_pos_tags.addWidget(self.label_tagsets_uneditable)

        self.table_mappings.setItemDelegateForColumn(0, wl_item_delegates.Wl_Item_Delegate_Uneditable(self.table_mappings))
        self.table_mappings.setItemDelegateForColumn(1, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
            parent = self.table_mappings,
            items = [
                'ADJ',
                'ADP',
                'ADV',
                'AUX',
                'CONJ', # Coordinating/Subordinating conjunctions
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
            ],
            editable = True
        ))
        self.table_mappings.setItemDelegateForColumn(2, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
            parent = self.table_mappings,
            items = [
                self.tr('Content words'),
                self.tr('Function words')
            ]
        ))
        self.table_mappings.setItemDelegateForColumn(3, wl_item_delegates.Wl_Item_Delegate(self.table_mappings, QPlainTextEdit))
        self.table_mappings.setItemDelegateForColumn(4, wl_item_delegates.Wl_Item_Delegate(self.table_mappings, QPlainTextEdit))

        self.button_tagsets_reset.setMinimumWidth(100)
        self.button_tagsets_reset_all.setMinimumWidth(100)

        self.button_tagsets_reset.clicked.connect(self.reset_mappings)
        self.button_tagsets_reset_all.clicked.connect(self.reset_all_mappings)

        self.group_box_mapping_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_mapping_settings.layout().addWidget(self.stacked_widget_num_pos_tags, 0, 0)
        self.group_box_mapping_settings.layout().addWidget(self.button_tagsets_reset, 0, 2)
        self.group_box_mapping_settings.layout().addWidget(self.button_tagsets_reset_all, 0, 3)
        self.group_box_mapping_settings.layout().addWidget(self.table_mappings, 1, 0, 1, 4)

        self.group_box_mapping_settings.layout().setRowStretch(1, 1)
        self.group_box_mapping_settings.layout().setColumnStretch(1, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_preview_settings, 0, 0)
        self.layout().addWidget(self.group_box_mapping_settings, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)

    def preview_lang_changed(self):
        self.settings_custom['preview_settings']['preview_lang'] = wl_conversion.to_lang_code(
            self.main,
            self.combo_box_tagsets_lang.currentText()
        )

        preview_lang = self.settings_custom['preview_settings']['preview_lang']

        self.combo_box_tagsets_pos_tagger.blockSignals(True)
        self.combo_box_tagsets_pos_tagger.clear()

        self.combo_box_tagsets_pos_tagger.addItems(wl_nlp_utils.to_lang_util_texts(
            self.main,
            util_type = 'pos_taggers',
            util_codes = self.settings_global[preview_lang])
        )
        self.combo_box_tagsets_pos_tagger.setCurrentText(wl_nlp_utils.to_lang_util_text(
            self.main,
            util_type = 'pos_taggers',
            util_code = self.settings_custom['preview_settings']['preview_pos_tagger'][preview_lang])
        )

        self.combo_box_tagsets_pos_tagger.blockSignals(False)
        self.combo_box_tagsets_pos_tagger.currentTextChanged.emit('')

    def preview_pos_tagger_changed(self):
        preview_lang = self.settings_custom['preview_settings']['preview_lang']

        self.settings_custom['preview_settings']['preview_pos_tagger'][preview_lang] = wl_nlp_utils.to_lang_util_code(
            self.main,
            util_type = 'pos_taggers',
            util_text = self.combo_box_tagsets_pos_tagger.currentText()
        )

        preview_pos_tagger = self.settings_custom['preview_settings']['preview_pos_tagger'][preview_lang]

        if (
            (
                not preview_pos_tagger.startswith('spacy_')
                and not preview_pos_tagger.startswith('stanza_')
            )
            or preview_pos_tagger in wl_pos_tagging.UNIVERSAL_TAGSETS_SPACY
            or preview_pos_tagger in wl_pos_tagging.UNIVERSAL_TAGSETS_STANZA
        ):
            self.combo_box_tagsets_lang.setEnabled(False)
            self.combo_box_tagsets_pos_tagger.setEnabled(False)
            self.button_tagsets_reset.setEnabled(False)
            self.button_tagsets_reset_all.setEnabled(False)
            self.table_mappings.setEnabled(True)

            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = self.tr('Fetching data...'))

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
        else:
            self.stacked_widget_num_pos_tags.setCurrentIndex(1)

            self.button_tagsets_reset.setEnabled(False)
            self.button_tagsets_reset_all.setEnabled(False)

            self.table_mappings.clr_table()
            self.table_mappings.setEnabled(False)

        # Scroll to top
        self.scroll_area_settings.verticalScrollBar().setValue(0)

    def update_gui(self, mappings):
        self.table_mappings.clr_table(len(mappings))

        self.table_mappings.disable_updates()

        for i, (tag, tag_universal, content_function_words, description, examples) in enumerate(mappings):
            self.table_mappings.model().setItem(i, 0, QStandardItem(tag))
            self.table_mappings.model().setItem(i, 1, QStandardItem(tag_universal))
            self.table_mappings.model().setItem(i, 2, QStandardItem(content_function_words))
            self.table_mappings.model().setItem(i, 3, QStandardItem(description))
            self.table_mappings.model().setItem(i, 4, QStandardItem(examples))

        self.table_mappings.enable_updates()

        self.label_tagsets_num_pos_tags.setText(self.tr('Number of part-of-speech tags: ') + str(self.table_mappings.model().rowCount()))
        self.stacked_widget_num_pos_tags.setCurrentIndex(0)

        self.combo_box_tagsets_lang.setEnabled(True)
        self.combo_box_tagsets_pos_tagger.setEnabled(True)
        self.button_tagsets_reset.setEnabled(True)
        self.button_tagsets_reset_all.setEnabled(True)

    def reset_currently_shown_table(self):
        preview_lang = self.settings_custom['preview_settings']['preview_lang']
        preview_pos_tagger = self.settings_custom['preview_settings']['preview_pos_tagger'][preview_lang]
        mappings = copy.deepcopy(self.settings_default['mapping_settings'][preview_lang][preview_pos_tagger])

        self.table_mappings.disable_updates()

        for i in range(self.table_mappings.model().rowCount()):
            self.table_mappings.model().item(i, 1).setText(mappings[i][1])
            self.table_mappings.model().item(i, 2).setText(mappings[i][2])
            self.table_mappings.model().item(i, 3).setText(mappings[i][3])

        self.table_mappings.enable_updates()

        self.settings_custom['mapping_settings'][preview_lang][preview_pos_tagger] = mappings

    def reset_mappings(self):
        if wl_msg_boxes.wl_msg_box_question(
            main = self.main,
            title = self.tr('Reset Mappings'),
            text = self.tr('''
                <div>Do you want to reset all mappings to their default settings?</div>
                <br>
                <div><b>Note: This will only affect the mapping settings in the currently shown table.</b></div>
            ''')
        ):
            self.reset_currently_shown_table()

    def reset_all_mappings(self):
        if wl_msg_boxes.wl_msg_box_question(
            main = self.main,
            title = self.tr('Reset All Mappings'),
            text = self.tr('''
                <div>Do you want to reset all mappings to their default settings?</div>
                <br>
                <div><b>Warning: This will affect the mapping settings in all tables!</b></div>
            ''')
        ):
            self.settings_custom['mapping_settings'] = copy.deepcopy(self.settings_default['mapping_settings'])

            self.reset_currently_shown_table()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Preview Settings
        if not defaults:
            self.combo_box_tagsets_lang.blockSignals(True)
            self.combo_box_tagsets_pos_tagger.blockSignals(True)

            self.combo_box_tagsets_lang.setCurrentText(wl_conversion.to_lang_text(self.main, settings['preview_settings']['preview_lang']))
            self.combo_box_tagsets_pos_tagger.setCurrentText(wl_nlp_utils.to_lang_util_text(
                self.main,
                util_type = 'pos_taggers',
                util_code = settings['preview_settings']['preview_pos_tagger'][settings['preview_settings']['preview_lang']]
            ))

            self.combo_box_tagsets_lang.blockSignals(False)
            self.combo_box_tagsets_pos_tagger.blockSignals(False)

    def apply_settings(self):
        # Save only when tag mappings are editable
        if self.pos_tag_mappings_loaded and self.table_mappings.isEnabled():
            # Mapping Settings
            preview_lang = self.settings_custom['preview_settings']['preview_lang']
            preview_pos_tagger = self.settings_custom['preview_settings']['preview_pos_tagger'][preview_lang]
            mapping = self.settings_custom['mapping_settings'][preview_lang][preview_pos_tagger]

            for i in range(self.table_mappings.model().rowCount()):
                mapping[i][1] = self.table_mappings.model().item(i, 1).text()
                mapping[i][2] = self.table_mappings.model().item(i, 2).text()
                mapping[i][3] = self.table_mappings.model().item(i, 3).text()

        return True

class Wl_Worker_Fetch_Data_Tagsets(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(list)

    def run(self):
        settings_custom = self.main.settings_custom['pos_tagging']['tagsets']

        preview_lang = settings_custom['preview_settings']['preview_lang']
        preview_pos_tagger = settings_custom['preview_settings']['preview_pos_tagger'][preview_lang]
        mappings = settings_custom['mapping_settings'][preview_lang][preview_pos_tagger]

        self.progress_updated.emit(self.tr('Updating table...'))
        self.worker_done.emit(mappings)
