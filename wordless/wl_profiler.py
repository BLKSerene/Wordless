# ----------------------------------------------------------------------
# Wordless: Profiler
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

import collections
import copy
import traceback

import numpy
import scipy
from PyQt5.QtCore import pyqtSignal, QCoreApplication, Qt
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QPushButton, QGroupBox

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_measures import wl_measures_misc, wl_measures_readability
from wordless.wl_nlp import wl_nlp_utils, wl_texts, wl_token_processing
from wordless.wl_utils import wl_misc, wl_threading
from wordless.wl_widgets import wl_layouts, wl_tables, wl_widgets

_tr = QCoreApplication.translate

class Wl_Worker_Profiler(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, list)

    def __init__(self, main, dialog_progress, update_gui):
        super().__init__(main, dialog_progress, update_gui)

        self.err_msg = ''
        self.text_stats_files = []

    def run(self):
        try:
            texts = []

            settings = self.main.settings_custom['profiler']
            files = list(self.main.wl_file_area.get_selected_files())

            for file in files:
                text = copy.deepcopy(file['text'])
                text = wl_token_processing.wl_process_tokens_profiler(
                    self.main, text,
                    token_settings = settings['token_settings']
                )

                texts.append(text)

            # Total
            if len(files) > 1:
                text_total = wl_texts.Wl_Text_Blank()

                # Set language for the combined text only if all texts are in the same language
                if len({text.lang for text in texts}) == 1:
                    text_total.lang = texts[0].lang
                else:
                    text_total.lang = 'other'

                text_total.tokens_multilevel = [
                    copy.deepcopy(para)
                    for text in texts
                    for para in text.tokens_multilevel
                ]
                text_total.syls_tokens = [
                    syls
                    for text in texts
                    for syls in text.syls_tokens
                ]

                texts.append(text_total)

            num_tokens_section_sttr = self.main.settings_custom['tables']['profiler']['general_settings']['num_tokens_section_sttr']

            for text in texts:
                tokens = text.get_tokens_flat()

                # Readability
                readability_statistics = [
                    wl_measures_readability.automated_ara_readability_index(self.main, text),
                    wl_measures_readability.automated_readability_index(self.main, text),
                    wl_measures_readability.coleman_liau_index(self.main, text),
                    wl_measures_readability.dale_chall_readability_score(self.main, text),
                    wl_measures_readability.devereux_readability_index(self.main, text),
                    wl_measures_readability.fernandez_huertas_readability_score(self.main, text),
                    wl_measures_readability.flesch_kincaid_grade_level(self.main, text),
                    wl_measures_readability.flesch_reading_ease(self.main, text),
                    wl_measures_readability.flesch_reading_ease_simplified(self.main, text),
                    wl_measures_readability.forcast_grade_level(self.main, text),
                    wl_measures_readability.formula_de_comprensibilidad_de_gutierrez_de_polini(self.main, text),
                    wl_measures_readability.formula_de_crawford(self.main, text),
                    wl_measures_readability.gulpease_index(self.main, text),
                    wl_measures_readability.gunning_fog_index(self.main, text),
                    wl_measures_readability.legibility_mu(self.main, text),
                    wl_measures_readability.lensear_write(self.main, text),
                    wl_measures_readability.lix(self.main, text),
                    wl_measures_readability.mcalpine_eflaw(self.main, text),
                    wl_measures_readability.osman(self.main, text),
                    wl_measures_readability.rix(self.main, text),
                    wl_measures_readability.smog_grade(self.main, text),
                    wl_measures_readability.spache_grade_level(self.main, text),
                    wl_measures_readability.szigriszts_perspicuity_index(self.main, text),
                    wl_measures_readability.wiener_sachtextformel(self.main, text)
                ]

                # Paragraph length
                len_paras_sentences = [
                    len(para)
                    for para in text.tokens_multilevel
                ]
                len_paras_sentence_segs = [
                    sum((len(sentence) for sentence in para))
                    for para in text.tokens_multilevel
                ]
                len_paras_tokens = [
                    sum((len(sentence_seg) for sentence in para for sentence_seg in sentence))
                    for para in text.tokens_multilevel
                ]

                # Sentence length
                len_sentences = [
                    sum((len(sentence_seg) for sentence_seg in sentence))
                    for para in text.tokens_multilevel
                    for sentence in para
                ]
                len_sentence_segs = [
                    len(sentence_seg)
                    for para in text.tokens_multilevel
                    for sentence in para
                    for sentence_seg in sentence
                ]

                # Token length
                len_tokens_syls = [len(syls) for syls in text.syls_tokens]
                len_tokens_chars = [len(token) for token in tokens]
                # Type length
                len_types_syls = [len(syls) for syls in {tuple(syls) for syls in text.syls_tokens}]
                len_types_chars = [len(token_type) for token_type in set(tokens)]
                # Syllable length
                len_syls = [len(syl) for syls in text.syls_tokens for syl in syls]

                count_tokens = len(len_tokens_chars)
                count_types = len(len_types_chars)

                # TTR & STTR (weighted average)
                if count_tokens:
                    ttr = count_types / count_tokens

                    ttrs = [
                        len(set(token_section))
                        for token_section in wl_nlp_utils.to_sections_unequal(tokens, num_tokens_section_sttr)
                    ]
                    sttr = numpy.sum(ttrs) / count_tokens
                else:
                    ttr = sttr = 0

                self.text_stats_files.append([
                    readability_statistics,
                    len_paras_sentences,
                    len_paras_sentence_segs,
                    len_paras_tokens,
                    len_sentences,
                    len_sentence_segs,
                    len_tokens_syls,
                    len_tokens_chars,
                    len_types_syls,
                    len_types_chars,
                    len_syls,
                    ttr,
                    sttr
                ])

            if len(files) == 1:
                self.text_stats_files *= 2
        except Exception:
            self.err_msg = traceback.format_exc()

class Wl_Worker_Profiler_Table(Wl_Worker_Profiler):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering table...'))
        self.worker_done.emit(self.err_msg, self.text_stats_files)

class Wl_Table_Profiler(wl_tables.Wl_Table_Data):
    def __init__(self, parent):
        super().__init__(
            parent,
            tab = 'profiler',
            headers = [
                # Readability
                _tr('Wl_Table_Profiler', 'Automated Arabic Readability Index'),
                _tr('Wl_Table_Profiler', 'Automated Readability Index'),
                _tr('Wl_Table_Profiler', 'Coleman-Liau Index'),
                _tr('Wl_Table_Profiler', 'Dale-Chall Readability Score'),
                _tr('Wl_Table_Profiler', 'Devereaux Readability Index'),
                _tr('Wl_Table_Profiler', "Fernández Huerta's Readability Score"),
                _tr('Wl_Table_Profiler', 'Flesch-Kincaid Grade Level'),
                _tr('Wl_Table_Profiler', 'Flesch Reading Ease'),
                _tr('Wl_Table_Profiler', 'Flesch Reading Ease (Simplified)'),
                _tr('Wl_Table_Profiler', 'FORCAST Grade Level'),
                _tr('Wl_Table_Profiler', 'Fórmula de comprensibilidad de Gutiérrez de Polini'),
                _tr('Wl_Table_Profiler', 'Fórmula de Crawford'),
                _tr('Wl_Table_Profiler', 'Gulpease Index'),
                _tr('Wl_Table_Profiler', 'Gunning Fog Index'),
                _tr('Wl_Table_Profiler', 'Legibilidad μ'),
                _tr('Wl_Table_Profiler', 'Lensear Write'),
                _tr('Wl_Table_Profiler', 'Lix'),
                _tr('Wl_Table_Profiler', 'McAlpine EFLAW Readability Score'),
                _tr('Wl_Table_Profiler', 'OSMAN'),
                _tr('Wl_Table_Profiler', 'Rix'),
                _tr('Wl_Table_Profiler', 'SMOG Grade'),
                _tr('Wl_Table_Profiler', 'Spache Grade Level'),
                _tr('Wl_Table_Profiler', "Szigriszt's Perspicuity Index"),
                _tr('Wl_Table_Profiler', 'Wiener Sachtextformel'),
                # Counts
                _tr('Wl_Table_Profiler', 'Count of Paragraphs'),
                _tr('Wl_Table_Profiler', 'Count of Paragraphs %'),
                _tr('Wl_Table_Profiler', 'Count of Sentences'),
                _tr('Wl_Table_Profiler', 'Count of Sentences %'),
                _tr('Wl_Table_Profiler', 'Count of Sentence Segments'),
                _tr('Wl_Table_Profiler', 'Count of Sentence Segments %'),
                _tr('Wl_Table_Profiler', 'Count of Tokens'),
                _tr('Wl_Table_Profiler', 'Count of Tokens %'),
                _tr('Wl_Table_Profiler', 'Count of Types'),
                _tr('Wl_Table_Profiler', 'Count of Types %'),
                _tr('Wl_Table_Profiler', 'Count of Syllables'),
                _tr('Wl_Table_Profiler', 'Count of Syllables %'),
                _tr('Wl_Table_Profiler', 'Count of Characters'),
                _tr('Wl_Table_Profiler', 'Count of Characters %'),
                # TTR
                _tr('Wl_Table_Profiler', 'Type-token Ratio'),
                _tr('Wl_Table_Profiler', 'Type-token Ratio (Standardized)'),
                # Paragraph length
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Mean)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Variance)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Minimum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Median)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Maximum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Modes)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Mean)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Variance)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Minimum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Median)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Maximum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Modes)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Mean)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Variance)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Minimum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Median)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Maximum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Modes)'),
                # Sentence length
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Mean)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Variance)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Minimum)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Median)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Maximum)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Range)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Modes)'),
                # Sentence segment length
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Mean)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Variance)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Minimum)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Median)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Maximum)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Range)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Modes)'),
                # Token length
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Mean)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Variance)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Minimum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Median)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Maximum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Range)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Modes)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Mean)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Variance)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Minimum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Median)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Maximum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Range)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Modes)'),
                # Type length
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Mean)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Variance)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Minimum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Median)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Maximum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Range)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Modes)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Mean)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Variance)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Minimum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Median)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Maximum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Range)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Modes)'),
                # Syllable length
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Mean)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Variance)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Minimum)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Median)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Maximum)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Range)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Modes)')
            ],
            header_orientation = 'vert',
            headers_int = [
                # Counts
                _tr('Wl_Table_Profiler', 'Count of Paragraphs'),
                _tr('Wl_Table_Profiler', 'Count of Sentences'),
                _tr('Wl_Table_Profiler', 'Count of Sentence Segments'),
                _tr('Wl_Table_Profiler', 'Count of Tokens'),
                _tr('Wl_Table_Profiler', 'Count of Types'),
                _tr('Wl_Table_Profiler', 'Count of Syllables'),
                _tr('Wl_Table_Profiler', 'Count of Characters'),
                # Paragraph length
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Minimum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Maximum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Minimum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Maximum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Minimum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Maximum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Range)'),
                # Sentence length
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Minimum)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Maximum)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Range)'),
                # Sentence segment length
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Minimum)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Maximum)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Range)'),
                # Token length
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Minimum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Maximum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Range)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Minimum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Maximum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Range)'),
                # Type length
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Minimum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Maximum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Range)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Minimum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Maximum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Range)'),
                # Syllable length
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Minimum)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Maximum)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Range)')
            ],
            headers_float = [
                # Readability
                _tr('Wl_Table_Profiler', 'Automated Arabic Readability Index'),
                _tr('Wl_Table_Profiler', 'Automated Readability Index'),
                _tr('Wl_Table_Profiler', 'Coleman-Liau Index'),
                _tr('Wl_Table_Profiler', 'Dale-Chall Readability Score'),
                _tr('Wl_Table_Profiler', 'Devereaux Readability Index'),
                _tr('Wl_Table_Profiler', "Fernández Huerta's Readability Score"),
                _tr('Wl_Table_Profiler', 'Flesch-Kincaid Grade Level'),
                _tr('Wl_Table_Profiler', 'Flesch Reading Ease'),
                _tr('Wl_Table_Profiler', 'Flesch Reading Ease (Simplified)'),
                _tr('Wl_Table_Profiler', 'FORCAST Grade Level'),
                _tr('Wl_Table_Profiler', 'Fórmula de comprensibilidad de Gutiérrez de Polini'),
                _tr('Wl_Table_Profiler', 'Fórmula de Crawford'),
                _tr('Wl_Table_Profiler', 'Gulpease Index'),
                _tr('Wl_Table_Profiler', 'Gunning Fog Index'),
                _tr('Wl_Table_Profiler', 'Legibilidad μ'),
                _tr('Wl_Table_Profiler', 'Lensear Write'),
                _tr('Wl_Table_Profiler', 'Lix'),
                _tr('Wl_Table_Profiler', 'McAlpine EFLAW Readability Score'),
                _tr('Wl_Table_Profiler', 'OSMAN'),
                _tr('Wl_Table_Profiler', 'Rix'),
                _tr('Wl_Table_Profiler', 'SMOG Grade'),
                _tr('Wl_Table_Profiler', 'Spache Grade Level'),
                _tr('Wl_Table_Profiler', "Szigriszt's Perspicuity Index"),
                _tr('Wl_Table_Profiler', 'Wiener Sachtextformel'),
                # TTR
                _tr('Wl_Table_Profiler', 'Type-token Ratio'),
                _tr('Wl_Table_Profiler', 'Type-token Ratio (Standardized)'),
                # Paragraph length
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Mean)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Variance)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Median)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Mean)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Variance)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Median)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentence Segments (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Mean)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Variance)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Median)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Interquartile Range)'),
                # Sentence length
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Mean)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Variance)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Median)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Interquartile Range)'),
                # Sentence segment length
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Mean)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Variance)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Median)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Sentence Segment Length in Tokens (Interquartile Range)'),
                # Token length
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Mean)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Variance)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Median)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Mean)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Variance)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Median)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Interquartile Range)'),
                # Type length
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Mean)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Variance)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Median)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Mean)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Variance)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Median)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Interquartile Range)'),
                # Syllable length
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Mean)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Variance)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Median)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Interquartile Range)')
            ],
            headers_pct = [
                # Counts
                _tr('Wl_Table_Profiler', 'Count of Paragraphs %'),
                _tr('Wl_Table_Profiler', 'Count of Sentences %'),
                _tr('Wl_Table_Profiler', 'Count of Sentence Segments %'),
                _tr('Wl_Table_Profiler', 'Count of Tokens %'),
                _tr('Wl_Table_Profiler', 'Count of Types %'),
                _tr('Wl_Table_Profiler', 'Count of Syllables %'),
                _tr('Wl_Table_Profiler', 'Count of Characters %')
            ],
            headers_cumulative = [
                # Counts
                _tr('Wl_Table_Profiler', 'Count of Paragraphs'),
                _tr('Wl_Table_Profiler', 'Count of Paragraphs %'),
                _tr('Wl_Table_Profiler', 'Count of Sentences'),
                _tr('Wl_Table_Profiler', 'Count of Sentences %'),
                _tr('Wl_Table_Profiler', 'Count of Sentence Segments'),
                _tr('Wl_Table_Profiler', 'Count of Sentence Segments %'),
                _tr('Wl_Table_Profiler', 'Count of Tokens'),
                _tr('Wl_Table_Profiler', 'Count of Tokens %'),
                _tr('Wl_Table_Profiler', 'Count of Types'),
                _tr('Wl_Table_Profiler', 'Count of Types %'),
                _tr('Wl_Table_Profiler', 'Count of Syllables'),
                _tr('Wl_Table_Profiler', 'Count of Syllables %'),
                _tr('Wl_Table_Profiler', 'Count of Characters'),
                _tr('Wl_Table_Profiler', 'Count of Characters %')
            ]
        )

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self)

        self.button_generate_table.clicked.connect(lambda: self.generate_table()) # pylint: disable=unnecessary-lambda
        self.main.wl_file_area.table_files.model().itemChanged.connect(self.file_changed)

        self.main.wl_file_area.table_files.model().itemChanged.emit(QStandardItem())

    def file_changed(self, item): # pylint: disable=unused-argument
        if list(self.main.wl_file_area.get_selected_files()):
            self.button_generate_table.setEnabled(True)
        else:
            self.button_generate_table.setEnabled(False)

    def clr_table(self, num_headers = 1, confirm = False):
        if super().clr_table(num_headers = 0, confirm = confirm):
            self.ins_header_hor(0, self.tr('Total'))

    @wl_misc.log_timing
    def generate_table(self):
        worker_profiler_table = Wl_Worker_Profiler_Table(
            self.main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
            update_gui = self.update_gui_table
        )

        wl_threading.Wl_Thread(worker_profiler_table).start_worker()

    def update_gui_table(self, err_msg, text_stats_files):
        # Skip if all statistics except readability measures are 0 or empty
        text_stats = [stat for text_stats in text_stats_files for stat in text_stats[1:]]

        if wl_checks_work_area.check_results(self.main, err_msg, text_stats):
            try:
                self.settings = copy.deepcopy(self.main.settings_custom)

                self.clr_table()

                count_tokens_lens = []
                count_sentences_lens = []
                count_sentence_segs_lens = []

                # Insert column (total)
                files = list(self.main.wl_file_area.get_selected_files())

                for i, file in enumerate(files):
                    self.ins_header_hor(
                        self.find_header_hor(_tr('wl_profiler', 'Total')), file['name'],
                        is_breakdown = True
                    )

                count_paras_total = len(text_stats_files[-1][1])
                count_sentences_total = len(text_stats_files[-1][4])
                count_sentence_segs_total = len(text_stats_files[-1][5])
                count_tokens_total = len(text_stats_files[-1][7])
                count_types_total = len(text_stats_files[-1][9])
                count_syls_total = len(text_stats_files[-1][10])
                count_chars_total = sum(text_stats_files[-1][7])

                self.disable_updates()

                for i, stats in enumerate(text_stats_files):
                    if i < len(files):
                        file_lang = files[i]['lang']
                    # Total
                    else:
                        if len({file['lang'] for file in files}) == 1:
                            file_lang = files[0]['lang']
                        else:
                            file_lang = 'other'

                    readability_stats = stats[0]
                    len_paras_sentences = numpy.array(stats[1])
                    len_paras_sentence_segs = numpy.array(stats[2])
                    len_paras_tokens = numpy.array(stats[3])
                    len_sentences = numpy.array(stats[4])
                    len_sentence_segs = numpy.array(stats[5])
                    len_tokens_syls = numpy.array(stats[6])
                    len_tokens_chars = numpy.array(stats[7])
                    len_types_syls = numpy.array(stats[8])
                    len_types_chars = numpy.array(stats[9])
                    len_syls = numpy.array(stats[10])
                    ttr = stats[11]
                    sttr = stats[12]

                    count_paras = len(len_paras_sentences)
                    count_sentences = len(len_sentences)
                    count_sentence_segs = len(len_sentence_segs)
                    count_tokens = len(len_tokens_chars)
                    count_types = len(len_types_chars)
                    count_syls = len(len_syls)
                    count_chars = numpy.sum(len_tokens_chars)

                    len_readability_stats = len(readability_stats)

                    # Readability
                    for j, statistic in enumerate(readability_stats):
                        if statistic == 'no_support':
                            self.set_item_error(j, i, _tr('wl_profiler', 'No Support'))
                        elif statistic == 'text_too_short':
                            self.set_item_error(j, i, _tr('wl_profiler', 'Text is Too Short'))
                        else:
                            self.set_item_num(j, i, statistic)

                    # Count of Paragraphs
                    self.set_item_num(len_readability_stats, i, count_paras)
                    self.set_item_num(len_readability_stats + 1, i, count_paras, count_paras_total)

                    # Count of Sentences
                    self.set_item_num(len_readability_stats + 2, i, count_sentences)
                    self.set_item_num(len_readability_stats + 3, i, count_sentences, count_sentences_total)

                    # Count of Sentence Segments
                    self.set_item_num(len_readability_stats + 4, i, count_sentence_segs)
                    self.set_item_num(len_readability_stats + 5, i, count_sentence_segs, count_sentence_segs_total)

                    # Count of Tokens
                    self.set_item_num(len_readability_stats + 6, i, count_tokens)
                    self.set_item_num(len_readability_stats + 7, i, count_tokens, count_tokens_total)

                    # Count of Types
                    self.set_item_num(len_readability_stats + 8, i, count_types)
                    self.set_item_num(len_readability_stats + 9, i, count_types, count_types_total)

                    # Count of Syllables
                    if file_lang in self.main.settings_global['syl_tokenizers']:
                        self.set_item_num(len_readability_stats + 10, i, count_syls)
                        self.set_item_num(len_readability_stats + 11, i, count_syls, count_syls_total)
                    else:
                        self.set_item_error(len_readability_stats + 10, i, text = _tr('wl_profiler', 'No Support'))
                        self.set_item_error(len_readability_stats + 11, i, text = _tr('wl_profiler', 'No Support'))

                    # Count of Characters
                    self.set_item_num(len_readability_stats + 12, i, count_chars)
                    self.set_item_num(len_readability_stats + 13, i, count_chars, count_chars_total)

                    # Type-token Ratio
                    self.set_item_num(len_readability_stats + 14, i, ttr)
                    # Type-token Ratio (Standardized)
                    self.set_item_num(len_readability_stats + 15, i, sttr)

                    # Paragraph / Sentence / Sentence Segment / Token in Characters / Type in Characters Length
                    for row, lens in zip(
                        [
                            len_readability_stats + 16, len_readability_stats + 27, len_readability_stats + 38,
                            len_readability_stats + 49, len_readability_stats + 60,
                            len_readability_stats + 82, len_readability_stats + 104
                        ],
                        [
                            len_paras_sentences, len_paras_sentence_segs, len_paras_tokens,
                            len_sentences, len_sentence_segs,
                            len_tokens_chars, len_types_chars
                        ]
                    ):
                        if lens.any():
                            self.set_item_num(row, i, numpy.mean(lens))
                            self.set_item_num(row + 1, i, numpy.std(lens))
                            self.set_item_num(row + 2, i, numpy.var(lens))
                            self.set_item_num(row + 3, i, numpy.min(lens))
                            self.set_item_num(row + 4, i, numpy.percentile(lens, 25))
                            self.set_item_num(row + 5, i, numpy.median(lens))
                            self.set_item_num(row + 6, i, numpy.percentile(lens, 75))
                            self.set_item_num(row + 7, i, numpy.max(lens))
                            self.set_item_num(row + 8, i, numpy.ptp(lens))
                            self.set_item_num(row + 9, i, scipy.stats.iqr(lens))
                            self.model().setItem(row + 10, i, QStandardItem(', '.join([
                                str(mode) for mode in wl_measures_misc.modes(lens)
                            ])))
                        else:
                            self.set_item_num(row, i, 0)
                            self.set_item_num(row + 1, i, 0)
                            self.set_item_num(row + 2, i, 0)
                            self.set_item_num(row + 3, i, 0)
                            self.set_item_num(row + 4, i, 0)
                            self.set_item_num(row + 5, i, 0)
                            self.set_item_num(row + 6, i, 0)
                            self.set_item_num(row + 7, i, 0)
                            self.set_item_num(row + 8, i, 0)
                            self.set_item_num(row + 9, i, 0)
                            self.model().setItem(row + 10, i, QStandardItem('0'))

                        self.model().item(row + 10, i).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                    # Token in Syllables / Types in Syllables / Syllable Length
                    for row, lens in zip(
                        [
                            len_readability_stats + 71, len_readability_stats + 93,
                            len_readability_stats + 115
                        ],
                        [
                            len_tokens_syls, len_types_syls,
                            len_syls
                        ]
                    ):
                        if file_lang in self.main.settings_global['syl_tokenizers']:
                            if lens.any():
                                self.set_item_num(row, i, numpy.mean(lens))
                                self.set_item_num(row + 1, i, numpy.std(lens))
                                self.set_item_num(row + 2, i, numpy.var(lens))
                                self.set_item_num(row + 3, i, numpy.min(lens))
                                self.set_item_num(row + 4, i, numpy.percentile(lens, 25))
                                self.set_item_num(row + 5, i, numpy.median(lens))
                                self.set_item_num(row + 6, i, numpy.percentile(lens, 75))
                                self.set_item_num(row + 7, i, numpy.max(lens))
                                self.set_item_num(row + 8, i, numpy.ptp(lens))
                                self.set_item_num(row + 9, i, scipy.stats.iqr(lens))
                                self.model().setItem(row + 10, i, QStandardItem(', '.join([
                                    str(mode) for mode in wl_measures_misc.modes(lens)
                                ])))
                            else:
                                self.set_item_num(row, i, 0)
                                self.set_item_num(row + 1, i, 0)
                                self.set_item_num(row + 2, i, 0)
                                self.set_item_num(row + 3, i, 0)
                                self.set_item_num(row + 4, i, 0)
                                self.set_item_num(row + 5, i, 0)
                                self.set_item_num(row + 6, i, 0)
                                self.set_item_num(row + 7, i, 0)
                                self.set_item_num(row + 8, i, 0)
                                self.set_item_num(row + 9, i, 0)
                                self.model().setItem(row + 10, i, QStandardItem('0'))

                            self.model().item(row + 10, i).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        else:
                            self.set_item_error(row, i, text = _tr('wl_profiler', 'No Support'))
                            self.set_item_error(row + 1, i, text = _tr('wl_profiler', 'No Support'))
                            self.set_item_error(row + 2, i, text = _tr('wl_profiler', 'No Support'))
                            self.set_item_error(row + 3, i, text = _tr('wl_profiler', 'No Support'))
                            self.set_item_error(row + 4, i, text = _tr('wl_profiler', 'No Support'))
                            self.set_item_error(row + 5, i, text = _tr('wl_profiler', 'No Support'))
                            self.set_item_error(row + 6, i, text = _tr('wl_profiler', 'No Support'))
                            self.set_item_error(row + 7, i, text = _tr('wl_profiler', 'No Support'))
                            self.set_item_error(row + 8, i, text = _tr('wl_profiler', 'No Support'))
                            self.set_item_error(row + 9, i, text = _tr('wl_profiler', 'No Support'))
                            self.set_item_error(row + 10, i, text = _tr('wl_profiler', 'No Support'))

                    count_tokens_lens.append(collections.Counter(len_tokens_chars))
                    count_sentence_segs_lens.append(collections.Counter(len_sentence_segs))
                    count_sentences_lens.append(collections.Counter(len_sentences))

                # Count of n-length Sentences
                if any(count_sentences_lens):
                    count_sentences_lens_files = wl_misc.merge_dicts(count_sentences_lens)
                    count_sentences_lens_total = {
                        len_sentence: count_sentences_files[-1]
                        for len_sentence, count_sentences_files in count_sentences_lens_files.items()
                    }
                    count_sentences_lens = sorted(count_sentences_lens_files.keys())

                    # Append vertical headers
                    for count_sentences_len in count_sentences_lens:
                        self.add_header_vert(
                            _tr('wl_profiler', 'Count of {}-length Sentences').format(count_sentences_len),
                            is_int = True, is_cumulative = True
                        )
                        self.add_header_vert(
                            _tr('wl_profiler', 'Count of {}-length Sentences %').format(count_sentences_len),
                            is_pct = True, is_cumulative = True
                        )

                    for i, count_sentences_len in enumerate(reversed(count_sentences_lens)):
                        counts = count_sentences_lens_files[count_sentences_len]

                        for j, count in enumerate(counts):
                            self.set_item_num(
                                row = self.model().rowCount() - 2 - i * 2,
                                col = j,
                                val = count
                            )
                            self.set_item_num(
                                row = self.model().rowCount() - 1 - i * 2,
                                col = j,
                                val = count,
                                total = count_sentences_lens_total[count_sentences_len]
                            )

                # Count of n-length Sentence Segments
                if any(count_sentence_segs_lens):
                    count_sentence_segs_lens_files = wl_misc.merge_dicts(count_sentence_segs_lens)
                    count_sentence_segs_lens_total = {
                        len_sentence_seg: count_sentence_segs_files[-1]
                        for len_sentence_seg, count_sentence_segs_files in count_sentence_segs_lens_files.items()
                    }
                    count_sentence_segs_lens = sorted(count_sentence_segs_lens_files.keys())

                    # Append vertical headers
                    for count_sentence_segs_len in count_sentence_segs_lens:
                        self.add_header_vert(
                            _tr('wl_profiler', 'Count of {}-length Sentence Segment').format(count_sentence_segs_len),
                            is_int = True, is_cumulative = True
                        )
                        self.add_header_vert(
                            _tr('wl_profiler', 'Count of {}-length Sentence Segment %').format(count_sentence_segs_len),
                            is_pct = True, is_cumulative = True
                        )

                    for i, count_sentence_segs_len in enumerate(reversed(count_sentence_segs_lens)):
                        counts = count_sentence_segs_lens_files[count_sentence_segs_len]

                        for j, count in enumerate(counts):
                            self.set_item_num(
                                row = self.model().rowCount() - 2 - i * 2,
                                col = j,
                                val = count
                            )
                            self.set_item_num(
                                row = self.model().rowCount() - 1 - i * 2,
                                col = j,
                                val = count,
                                total = count_sentence_segs_lens_total[count_sentence_segs_len]
                            )

                # Count of n-length Tokens
                if any(count_tokens_lens):
                    count_tokens_lens_files = wl_misc.merge_dicts(count_tokens_lens)
                    count_tokens_lens_total = {
                        len_token: count_tokens_files[-1]
                        for len_token, count_tokens_files in count_tokens_lens_files.items()
                    }
                    count_tokens_lens = sorted(count_tokens_lens_files.keys())

                    # Append vertical headers
                    for count_tokens_len in count_tokens_lens:
                        self.add_header_vert(
                            _tr('wl_profiler', 'Count of {}-Length Tokens').format(count_tokens_len),
                            is_int = True, is_cumulative = True
                        )
                        self.add_header_vert(
                            _tr('wl_profiler', 'Count of {}-Length Tokens %').format(count_tokens_len),
                            is_pct = True, is_cumulative = True
                        )

                    for i, count_tokens_len in enumerate(reversed(count_tokens_lens)):
                        counts = count_tokens_lens_files[count_tokens_len]

                        for j, count in enumerate(counts):
                            self.set_item_num(
                                row = self.model().rowCount() - 2 - i * 2,
                                col = j,
                                val = count
                            )
                            self.set_item_num(
                                row = self.model().rowCount() - 1 - i * 2,
                                col = j,
                                val = count,
                                total = count_tokens_lens_total[count_tokens_len]
                            )

                self.enable_updates()

                self.toggle_pct()
                self.toggle_cumulative()
                self.toggle_breakdown()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

class Wrapper_Profiler(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        # Table
        self.table_profiler = Wl_Table_Profiler(self)

        self.wrapper_table.layout().addWidget(self.table_profiler, 0, 0, 1, 4)
        self.wrapper_table.layout().addWidget(self.table_profiler.button_generate_table, 1, 0)
        self.wrapper_table.layout().addWidget(self.table_profiler.button_exp_selected, 1, 1)
        self.wrapper_table.layout().addWidget(self.table_profiler.button_exp_all, 1, 2)
        self.wrapper_table.layout().addWidget(self.table_profiler.button_clr, 1, 3)

        # Token Settings
        self.group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

        (
            self.checkbox_words,
            self.checkbox_all_lowercase,
            self.checkbox_all_uppercase,
            self.checkbox_title_case,
            self.checkbox_nums,
            self.checkbox_puncs,

            self.checkbox_treat_as_all_lowercase,
            self.checkbox_lemmatize_tokens,
            self.checkbox_filter_stop_words,

            self.checkbox_ignore_tags,
            self.checkbox_use_tags
        ) = wl_widgets.wl_widgets_token_settings(self)

        self.checkbox_words.stateChanged.connect(self.token_settings_changed)
        self.checkbox_all_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_all_uppercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_title_case.stateChanged.connect(self.token_settings_changed)
        self.checkbox_nums.stateChanged.connect(self.token_settings_changed)
        self.checkbox_puncs.stateChanged.connect(self.token_settings_changed)

        self.checkbox_treat_as_all_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_lemmatize_tokens.stateChanged.connect(self.token_settings_changed)
        self.checkbox_filter_stop_words.stateChanged.connect(self.token_settings_changed)

        self.checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        self.group_box_token_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_token_settings.layout().addWidget(self.checkbox_words, 0, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_all_lowercase, 0, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_all_uppercase, 1, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_title_case, 1, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_nums, 2, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_puncs, 2, 1)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 3, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_treat_as_all_lowercase, 4, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_lemmatize_tokens, 5, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_filter_stop_words, 6, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 7, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_ignore_tags, 8, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 8, 1)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'), self)

        (
            self.checkbox_show_pct,
            self.checkbox_show_cumulative,
            self.checkbox_show_breakdown
        ) = wl_widgets.wl_widgets_table_settings(
            self,
            tables = [self.table_profiler]
        )

        self.checkbox_show_pct.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_cumulative.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_breakdown.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct, 0, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_cumulative, 1, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_breakdown, 2, 0)

        self.wrapper_settings.layout().addWidget(self.group_box_token_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 1, 0)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['profiler'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['profiler'])

        # Token Settings
        self.checkbox_words.setChecked(settings['token_settings']['words'])
        self.checkbox_all_lowercase.setChecked(settings['token_settings']['all_lowercase'])
        self.checkbox_all_uppercase.setChecked(settings['token_settings']['all_uppercase'])
        self.checkbox_title_case.setChecked(settings['token_settings']['title_case'])
        self.checkbox_nums.setChecked(settings['token_settings']['nums'])
        self.checkbox_puncs.setChecked(settings['token_settings']['puncs'])

        self.checkbox_treat_as_all_lowercase.setChecked(settings['token_settings']['treat_as_all_lowercase'])
        self.checkbox_lemmatize_tokens.setChecked(settings['token_settings']['lemmatize_tokens'])
        self.checkbox_filter_stop_words.setChecked(settings['token_settings']['filter_stop_words'])

        self.checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.checkbox_use_tags.setChecked(settings['token_settings']['use_tags'])

        # Table Settings
        self.checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])
        self.checkbox_show_cumulative.setChecked(settings['table_settings']['show_cumulative'])
        self.checkbox_show_breakdown.setChecked(settings['table_settings']['show_breakdown'])

        self.token_settings_changed()
        self.table_settings_changed()

    def token_settings_changed(self):
        settings = self.main.settings_custom['profiler']['token_settings']

        settings['words'] = self.checkbox_words.isChecked()
        settings['all_lowercase'] = self.checkbox_all_lowercase.isChecked()
        settings['all_uppercase'] = self.checkbox_all_uppercase.isChecked()
        settings['title_case'] = self.checkbox_title_case.isChecked()
        settings['nums'] = self.checkbox_nums.isChecked()
        settings['puncs'] = self.checkbox_puncs.isChecked()

        settings['treat_as_all_lowercase'] = self.checkbox_treat_as_all_lowercase.isChecked()
        settings['lemmatize_tokens'] = self.checkbox_lemmatize_tokens.isChecked()
        settings['filter_stop_words'] = self.checkbox_filter_stop_words.isChecked()

        settings['ignore_tags'] = self.checkbox_ignore_tags.isChecked()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

    def table_settings_changed(self):
        settings = self.main.settings_custom['profiler']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()
        settings['show_cumulative'] = self.checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = self.checkbox_show_breakdown.isChecked()
