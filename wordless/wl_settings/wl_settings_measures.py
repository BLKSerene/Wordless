# ----------------------------------------------------------------------
# Wordless: Settings - Measures
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
import math

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QCheckBox, QGroupBox, QLabel

from wordless.wl_settings import wl_settings
from wordless.wl_widgets import wl_boxes, wl_layouts, wl_widgets

_tr = QCoreApplication.translate

# Measures - Readability
class Wl_Settings_Measures_Readability(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['measures']['readability']
        self.settings_custom = self.main.settings_custom['measures']['readability']

        # Al-Heeti's Readability Formula
        self.group_box_rd = QGroupBox(self.tr("Al-Heeti's Readability Formula"), self)

        self.label_rd_variant = QLabel(self.tr('Variant:'), self)
        self.combo_box_rd_variant = wl_boxes.Wl_Combo_Box(self)

        self.combo_box_rd_variant.addItems([
            self.tr('Policy One'),
            self.tr('Policy Two')
        ])

        self.group_box_rd.setLayout(wl_layouts.Wl_Layout())
        self.group_box_rd.layout().addWidget(self.label_rd_variant, 0, 0)
        self.group_box_rd.layout().addWidget(self.combo_box_rd_variant, 0, 1)

        self.group_box_rd.layout().setColumnStretch(2, 1)

        # Automated Readability Index
        self.group_box_ari = QGroupBox(self.tr('Automated Readability Index'), self)

        self.checkbox_use_navy_variant = QCheckBox(self.tr('Use Navy variant'), self)

        self.group_box_ari.setLayout(wl_layouts.Wl_Layout())
        self.group_box_ari.layout().addWidget(self.checkbox_use_navy_variant, 0, 0)

        # Bormuth's Grade Placement
        self.group_box_bormuths_gp = QGroupBox(self.tr("Bormuth's Grade Placement"), self)

        self.label_cloze_criterion_score = QLabel(self.tr('Cloze criterion score:'), self)
        self.spin_box_cloze_criterion_score = wl_boxes.Wl_Spin_Box(self)

        self.spin_box_cloze_criterion_score.setRange(0, 100)
        self.spin_box_cloze_criterion_score.setSuffix('%')

        self.group_box_bormuths_gp.setLayout(wl_layouts.Wl_Layout())
        self.group_box_bormuths_gp.layout().addWidget(self.label_cloze_criterion_score, 0, 0)
        self.group_box_bormuths_gp.layout().addWidget(self.spin_box_cloze_criterion_score, 0, 1)

        self.group_box_bormuths_gp.layout().setColumnStretch(2, 1)

        # Coleman's Readability Formula
        self.group_box_colemans_readability_formula = QGroupBox(self.tr("Coleman's Readability Formula"), self)

        self.label_colemans_readability_formula_variant = QLabel(self.tr('Variant:'), self)
        self.combo_box_colemans_readability_formula_variant = wl_boxes.Wl_Combo_Box(self)

        self.combo_box_colemans_readability_formula_variant.addItems(['1', '2', '3', '4'])

        self.group_box_colemans_readability_formula.setLayout(wl_layouts.Wl_Layout())
        self.group_box_colemans_readability_formula.layout().addWidget(self.label_colemans_readability_formula_variant, 0, 0)
        self.group_box_colemans_readability_formula.layout().addWidget(self.combo_box_colemans_readability_formula_variant, 0, 1)

        self.group_box_colemans_readability_formula.layout().setColumnStretch(2, 1)

        # Dale-Chall Readability Formula
        self.group_box_x_c50 = QGroupBox(self.tr('Dale-Chall Readability Formula'), self)
        self.label_x_c50_variant = QLabel(self.tr('Variant:'), self)
        self.combo_box_x_c50_variant = wl_boxes.Wl_Combo_Box(self)

        self.combo_box_x_c50_variant.addItems([
            self.tr('Original'),
            'Powers-Sumner-Kearl',
            self.tr('New')
        ])

        self.group_box_x_c50.setLayout(wl_layouts.Wl_Layout())
        self.group_box_x_c50.layout().addWidget(self.label_x_c50_variant, 0, 0)
        self.group_box_x_c50.layout().addWidget(self.combo_box_x_c50_variant, 0, 1)

        self.group_box_x_c50.layout().setColumnStretch(2, 1)

        # Danielson-Bryan's Readability Formula
        self.group_box_danielson_bryans_readability_formula = QGroupBox(self.tr("Danielson-Bryan's Readability Formula"), self)

        self.label_danielson_bryans_readability_formula_variant = QLabel(self.tr('Variant:'), self)
        self.combo_box_danielson_bryans_readability_formula_variant = wl_boxes.Wl_Combo_Box(self)

        self.combo_box_danielson_bryans_readability_formula_variant.addItems(['1', '2'])

        self.group_box_danielson_bryans_readability_formula.setLayout(wl_layouts.Wl_Layout())
        self.group_box_danielson_bryans_readability_formula.layout().addWidget(self.label_danielson_bryans_readability_formula_variant, 0, 0)
        self.group_box_danielson_bryans_readability_formula.layout().addWidget(self.combo_box_danielson_bryans_readability_formula_variant, 0, 1)

        self.group_box_danielson_bryans_readability_formula.layout().setColumnStretch(2, 1)

        # Flesch Reading Ease
        self.group_box_re = QGroupBox(self.tr('Flesch Reading Ease'), self)

        self.checkbox_use_powers_sumner_kearl_variant_for_all_langs = QCheckBox(self.tr('Use Powers-Sumner-Kearl variant for all languages'), self)
        self.label_re_variant_nld = QLabel(self.tr('Dutch variant:'), self)
        self.combo_box_re_variant_nld = wl_boxes.Wl_Combo_Box(self)
        self.label_re_variant_spa = QLabel(self.tr('Spanish variant:'), self)
        self.combo_box_re_variant_spa = wl_boxes.Wl_Combo_Box(self)

        self.combo_box_re_variant_nld.addItems([
            "Brouwer's Leesindex A",
            'Douma',
        ])
        self.combo_box_re_variant_spa.addItems([
            'Fernández Huerta',
            'Szigriszt Pazos'
        ])

        self.checkbox_use_powers_sumner_kearl_variant_for_all_langs.stateChanged.connect(self.re_changed)

        self.group_box_re.setLayout(wl_layouts.Wl_Layout())
        self.group_box_re.layout().addWidget(self.checkbox_use_powers_sumner_kearl_variant_for_all_langs, 0, 0, 1, 3)
        self.group_box_re.layout().addWidget(self.label_re_variant_nld, 1, 0)
        self.group_box_re.layout().addWidget(self.combo_box_re_variant_nld, 1, 1)
        self.group_box_re.layout().addWidget(self.label_re_variant_spa, 2, 0)
        self.group_box_re.layout().addWidget(self.combo_box_re_variant_spa, 2, 1)

        self.group_box_re.layout().setColumnStretch(2, 1)

        # Flesch Reading Ease (Farr-Jenkins-Paterson)
        self.group_box_re_farr_jenkins_paterson = QGroupBox(self.tr('Flsch Reading Ease (Farr-Jenkins-Paterson)'), self)

        self.checkbox_use_powers_sumner_kearl_variant = QCheckBox(self.tr('Use Powers-Sumner-Kearl variant'), self)

        self.group_box_re_farr_jenkins_paterson.setLayout(wl_layouts.Wl_Layout())
        self.group_box_re_farr_jenkins_paterson.layout().addWidget(self.checkbox_use_powers_sumner_kearl_variant, 0, 0)

        # Gunning Fog Index
        self.group_box_fog_index = QGroupBox(self.tr('Gunning Fog Index'), self)

        self.label_fog_index_variant_eng = QLabel(self.tr('English variant:'), self)
        self.combo_box_fog_index_variant_eng = wl_boxes.Wl_Combo_Box(self)

        self.combo_box_fog_index_variant_eng.addItems([
            self.tr('Original'),
            'Powers-Sumner-Kearl',
            self.tr('Navy')
        ])

        self.group_box_fog_index.setLayout(wl_layouts.Wl_Layout())
        self.group_box_fog_index.layout().addWidget(self.label_fog_index_variant_eng, 0, 0)
        self.group_box_fog_index.layout().addWidget(self.combo_box_fog_index_variant_eng, 0, 1)

        self.group_box_fog_index.layout().setColumnStretch(2, 1)

        # Lorge Readability Index
        self.group_box_lorge_readability_index = QGroupBox(self.tr('Lorge Readability Index'), self)

        self.checkbox_use_corrected_formula = QCheckBox(self.tr('Use corrected formula'), self)

        self.group_box_lorge_readability_index.setLayout(wl_layouts.Wl_Layout())
        self.group_box_lorge_readability_index.layout().addWidget(self.checkbox_use_corrected_formula, 0, 0)

        # neue Wiener Literaturformeln
        self.group_box_nwl = QGroupBox(self.tr('neue Wiener Literaturformeln'), self)

        self.label_nwl_variant = QLabel(self.tr('Variant:'), self)
        self.combo_box_nwl_variant = wl_boxes.Wl_Combo_Box(self)

        self.combo_box_nwl_variant.addItems(['1', '2', '3'])

        self.group_box_nwl.setLayout(wl_layouts.Wl_Layout())
        self.group_box_nwl.layout().addWidget(self.label_nwl_variant, 0, 0)
        self.group_box_nwl.layout().addWidget(self.combo_box_nwl_variant, 0, 1)

        self.group_box_nwl.layout().setColumnStretch(2, 1)

        # neue Wiener Sachtextformel
        self.group_box_nws = QGroupBox(self.tr('neue Wiener Sachtextformel'), self)

        self.label_nws_variant = QLabel(self.tr('Variant:'), self)
        self.combo_box_nws_variant = wl_boxes.Wl_Combo_Box(self)

        self.combo_box_nws_variant.addItems(['1', '2', '3'])

        self.group_box_nws.setLayout(wl_layouts.Wl_Layout())
        self.group_box_nws.layout().addWidget(self.label_nws_variant, 0, 0)
        self.group_box_nws.layout().addWidget(self.combo_box_nws_variant, 0, 1)

        self.group_box_nws.layout().setColumnStretch(2, 1)

        # Spache Readability Formula
        self.group_box_spache_readability_formula = QGroupBox(self.tr('Spache Readability Formula'), self)

        self.checkbox_use_rev_formula = QCheckBox(self.tr('Use revised formula'), self)

        self.group_box_spache_readability_formula.setLayout(wl_layouts.Wl_Layout())
        self.group_box_spache_readability_formula.layout().addWidget(self.checkbox_use_rev_formula, 0, 0)

        # Tränkle-Bailer's Readability Formula
        self.group_box_trankle_bailers_readability_formula = QGroupBox(self.tr("Tränkle-Bailer's Readability Formula"), self)

        self.label_trankle_bailers_readability_formula_variant = QLabel(self.tr('Variant:'), self)
        self.combo_box_trankle_bailers_readability_formula_variant = wl_boxes.Wl_Combo_Box(self)

        self.combo_box_trankle_bailers_readability_formula_variant.addItems(['1', '2'])

        self.group_box_trankle_bailers_readability_formula.setLayout(wl_layouts.Wl_Layout())
        self.group_box_trankle_bailers_readability_formula.layout().addWidget(self.label_trankle_bailers_readability_formula_variant, 0, 0)
        self.group_box_trankle_bailers_readability_formula.layout().addWidget(self.combo_box_trankle_bailers_readability_formula_variant, 0, 1)

        self.group_box_trankle_bailers_readability_formula.layout().setColumnStretch(2, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_rd, 0, 0)
        self.layout().addWidget(self.group_box_ari, 1, 0)
        self.layout().addWidget(self.group_box_bormuths_gp, 2, 0)
        self.layout().addWidget(self.group_box_colemans_readability_formula, 3, 0)
        self.layout().addWidget(self.group_box_x_c50, 4, 0)
        self.layout().addWidget(self.group_box_danielson_bryans_readability_formula, 5, 0)
        self.layout().addWidget(self.group_box_re, 6, 0)
        self.layout().addWidget(self.group_box_re_farr_jenkins_paterson, 7, 0)
        self.layout().addWidget(self.group_box_fog_index, 8, 0)
        self.layout().addWidget(self.group_box_lorge_readability_index, 9, 0)
        self.layout().addWidget(self.group_box_nwl, 10, 0)
        self.layout().addWidget(self.group_box_nws, 11, 0)
        self.layout().addWidget(self.group_box_spache_readability_formula, 12, 0)
        self.layout().addWidget(self.group_box_trankle_bailers_readability_formula, 13, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(14, 1)

    def re_changed(self):
        if self.checkbox_use_powers_sumner_kearl_variant_for_all_langs.isChecked():
            self.combo_box_re_variant_nld.setEnabled(False)
            self.combo_box_re_variant_spa.setEnabled(False)
        else:
            self.combo_box_re_variant_nld.setEnabled(True)
            self.combo_box_re_variant_spa.setEnabled(True)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Al-Heeti's Readability Formula
        self.combo_box_rd_variant.setCurrentText(settings['rd']['variant'])

        # Automated Readability Index
        self.checkbox_use_navy_variant.setChecked(settings['ari']['use_navy_variant'])

        # Bormuth's Grade Placement
        self.spin_box_cloze_criterion_score.setValue(settings['bormuths_gp']['cloze_criterion_score'])

        # Coleman's Readability Formula
        self.combo_box_colemans_readability_formula_variant.setCurrentText(settings['colemans_readability_formula']['variant'])

        # Dale-Chall Readability Formula
        self.combo_box_x_c50_variant.setCurrentText(settings['x_c50']['variant'])

        # Danielson-Bryan's Readability Formula
        self.combo_box_danielson_bryans_readability_formula_variant.setCurrentText(settings['danielson_bryans_readability_formula']['variant'])

        # Flesch Reading Ease
        self.checkbox_use_powers_sumner_kearl_variant_for_all_langs.setChecked(settings['re']['use_powers_sumner_kearl_variant_for_all_langs'])
        self.combo_box_re_variant_nld.setCurrentText(settings['re']['variant_nld'])
        self.combo_box_re_variant_spa.setCurrentText(settings['re']['variant_spa'])

        # Flesch Reading Ease (Farr-Jenkins-Paterson)
        self.checkbox_use_powers_sumner_kearl_variant.setChecked(settings['re_farr_jenkins_paterson']['use_powers_sumner_kearl_variant'])

        # Gunning Fog Index
        self.combo_box_fog_index_variant_eng.setCurrentText(settings['fog_index']['variant_eng'])

        # Lorge Readability Index
        self.checkbox_use_corrected_formula.setChecked(settings['lorge_readability_index']['use_corrected_formula'])

        # neue Wiener Literaturformeln
        self.combo_box_nwl_variant.setCurrentText(settings['nwl']['variant'])

        # neue Wiener Sachtextformel
        self.combo_box_nws_variant.setCurrentText(settings['nws']['variant'])

        # Spache Readability Formula
        self.checkbox_use_rev_formula.setChecked(settings['spache_readability_formula']['use_rev_formula'])

        # Tränkle-Bailer's Readability Formula
        self.combo_box_trankle_bailers_readability_formula_variant.setCurrentText(settings['trankle_bailers_readability_formula']['variant'])

    def apply_settings(self):
        # Al-Heeti's Readability Formula
        self.settings_custom['rd']['variant'] = self.combo_box_rd_variant.currentText()

        # Automated Readability Index
        self.settings_custom['ari']['use_navy_variant'] = self.checkbox_use_navy_variant.isChecked()

        # Bormuth's Grade Placement
        self.settings_custom['bormuths_gp']['cloze_criterion_score'] = self.spin_box_cloze_criterion_score.value()

        # Coleman's Readability Formula
        self.settings_custom['colemans_readability_formula']['variant'] = self.combo_box_colemans_readability_formula_variant.currentText()

        # Dale-Chall Readability Formula
        self.settings_custom['x_c50']['variant'] = self.combo_box_x_c50_variant.currentText()

        # Danielson-Bryan's Readability Formula
        self.settings_custom['danielson_bryans_readability_formula']['variant'] = self.combo_box_danielson_bryans_readability_formula_variant.currentText()

        # Flesch Reading Ease
        self.settings_custom['re']['use_powers_sumner_kearl_variant_for_all_langs'] = self.checkbox_use_powers_sumner_kearl_variant_for_all_langs.isChecked()
        self.settings_custom['re']['variant_nld'] = self.combo_box_re_variant_nld.currentText()
        self.settings_custom['re']['variant_spa'] = self.combo_box_re_variant_spa.currentText()

        # Flesch Reading Ease (Farr-Jenkins-Paterson)
        self.settings_custom['re_farr_jenkins_paterson']['use_powers_sumner_kearl_variant'] = self.checkbox_use_powers_sumner_kearl_variant.isChecked()

        # Gunning Fog Index
        self.settings_custom['fog_index']['variant_eng'] = self.combo_box_fog_index_variant_eng.currentText()

        # Lorge Readability Index
        self.settings_custom['lorge_readability_index']['use_corrected_formula'] = self.checkbox_use_corrected_formula.isChecked()

        # neue Wiener Literaturformeln
        self.settings_custom['nwl']['variant'] = self.combo_box_nwl_variant.currentText()

        # neue Wiener Sachtextformel
        self.settings_custom['nws']['variant'] = self.combo_box_nws_variant.currentText()

        # Spache Readability Formula
        self.settings_custom['spache_readability_formula']['use_rev_formula'] = self.checkbox_use_rev_formula.isChecked()

        # Tränkle-Bailer's Readability Formula
        self.settings_custom['trankle_bailers_readability_formula']['variant'] = self.combo_box_trankle_bailers_readability_formula_variant.currentText()

        return True

# Measures - Lexical Density/Diversity
class Wl_Settings_Measures_Lexical_Density_Diversity(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['measures']['lexical_density_diversity']
        self.settings_custom = self.main.settings_custom['measures']['lexical_density_diversity']

        # HD-D
        self.group_box_hdd = QGroupBox('HD-D', self)

        self.label_sample_size = QLabel(self.tr('Sample size:'), self)
        self.spin_box_sample_size = wl_boxes.Wl_Spin_Box(self)

        self.spin_box_sample_size.setRange(35, 50)

        self.group_box_hdd.setLayout(wl_layouts.Wl_Layout())
        self.group_box_hdd.layout().addWidget(self.label_sample_size, 0, 0)
        self.group_box_hdd.layout().addWidget(self.spin_box_sample_size, 0, 1)

        self.group_box_hdd.layout().setColumnStretch(2, 1)

        # LogTTR
        self.group_box_logttr = QGroupBox(self.tr('LogTTR'), self)

        self.label_variant = QLabel(self.tr('Sample size:'), self)
        self.combo_box_variant = wl_boxes.Wl_Combo_Box(self)

        self.combo_box_variant.addItems([
            'Herdan',
            'Somers',
            'Rubet',
            'Maas',
            'Dugast'
        ])

        self.group_box_logttr.setLayout(wl_layouts.Wl_Layout())
        self.group_box_logttr.layout().addWidget(self.label_variant, 0, 0)
        self.group_box_logttr.layout().addWidget(self.combo_box_variant, 0, 1)

        self.group_box_logttr.layout().setColumnStretch(2, 1)

        # Mean Segmental TTR
        self.group_box_msttr = QGroupBox(self.tr('Mean Segmental TTR'), self)

        self.label_num_tokens_in_each_seg = QLabel(self.tr('Number of tokens in each segment:'), self)
        self.spin_box_num_tokens_in_each_seg = wl_boxes.Wl_Spin_Box(self)

        self.spin_box_num_tokens_in_each_seg.setRange(1, 1000000)

        self.group_box_msttr.setLayout(wl_layouts.Wl_Layout())
        self.group_box_msttr.layout().addWidget(self.label_num_tokens_in_each_seg, 0, 0)
        self.group_box_msttr.layout().addWidget(self.spin_box_num_tokens_in_each_seg, 0, 1)

        self.group_box_msttr.layout().setColumnStretch(2, 1)

        # Measure of Textual Lexical Diversity
        self.group_box_mtld = QGroupBox(self.tr('Measure of Textual Lexical Diversity'), self)

        self.label_factor_size = QLabel(self.tr('Factor size:'), self)
        self.spin_box_factor_size = wl_boxes.Wl_Double_Spin_Box(self)

        self.spin_box_factor_size.setDecimals(3)
        self.spin_box_factor_size.setSingleStep(.001)

        self.group_box_mtld.setLayout(wl_layouts.Wl_Layout())
        self.group_box_mtld.layout().addWidget(self.label_factor_size, 0, 0)
        self.group_box_mtld.layout().addWidget(self.spin_box_factor_size, 0, 1)

        self.group_box_mtld.layout().setColumnStretch(2, 1)

        # Moving-average TTR
        self.group_box_mattr = QGroupBox(self.tr('Moving-average TTR'), self)

        self.label_window_size = QLabel(self.tr('Window size:'), self)
        self.spin_box_window_size = wl_boxes.Wl_Spin_Box(self)

        self.spin_box_window_size.setRange(1, 1000000)

        self.group_box_mattr.setLayout(wl_layouts.Wl_Layout())
        self.group_box_mattr.layout().addWidget(self.label_window_size, 0, 0)
        self.group_box_mattr.layout().addWidget(self.spin_box_window_size, 0, 1)

        self.group_box_mattr.layout().setColumnStretch(2, 1)

        # Repeat Rate
        self.group_box_repeat_rate = QGroupBox(self.tr('Repeat Rate'), self)

        self.label_use_data_repeat_rate = QLabel(self.tr('Use data:'), self)
        self.combo_box_use_data_repeat_rate = wl_boxes.Wl_Combo_Box(self)

        self.combo_box_use_data_repeat_rate.addItems([
            self.tr('Rank-frequency distribution'),
            self.tr('Frequency spectrum')
        ])

        self.group_box_repeat_rate.setLayout(wl_layouts.Wl_Layout())
        self.group_box_repeat_rate.layout().addWidget(self.label_use_data_repeat_rate, 0, 0)
        self.group_box_repeat_rate.layout().addWidget(self.combo_box_use_data_repeat_rate, 0, 1)

        self.group_box_repeat_rate.layout().setColumnStretch(2, 1)

        # Shannon Entropy
        self.group_box_shannon_entropy = QGroupBox(self.tr('Shannon Entropy'), self)

        self.label_use_data_shannon_entropy = QLabel(self.tr('Use data:'), self)
        self.combo_box_use_data_shannon_entropy = wl_boxes.Wl_Combo_Box(self)

        self.combo_box_use_data_shannon_entropy.addItems([
            self.tr('Rank-frequency distribution'),
            self.tr('Frequency spectrum')
        ])

        self.group_box_shannon_entropy.setLayout(wl_layouts.Wl_Layout())
        self.group_box_shannon_entropy.layout().addWidget(self.label_use_data_shannon_entropy, 0, 0)
        self.group_box_shannon_entropy.layout().addWidget(self.combo_box_use_data_shannon_entropy, 0, 1)

        self.group_box_shannon_entropy.layout().setColumnStretch(2, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_hdd, 0, 0)
        self.layout().addWidget(self.group_box_logttr, 1, 0)
        self.layout().addWidget(self.group_box_msttr, 2, 0)
        self.layout().addWidget(self.group_box_mtld, 3, 0)
        self.layout().addWidget(self.group_box_mattr, 4, 0)
        self.layout().addWidget(self.group_box_repeat_rate, 5, 0)
        self.layout().addWidget(self.group_box_shannon_entropy, 6, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(7, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # HD-D
        self.spin_box_sample_size.setValue(settings['hdd']['sample_size'])

        # LogTTR
        self.combo_box_variant.setCurrentText(settings['logttr']['variant'])

        # Mean Segmental TTR
        self.spin_box_num_tokens_in_each_seg.setValue(settings['msttr']['num_tokens_in_each_seg'])

        # Measure of Textual Lexical Diversity
        self.spin_box_factor_size.setValue(settings['mtld']['factor_size'])

        # Moving-average TTR
        self.spin_box_window_size.setValue(settings['mattr']['window_size'])

        # Repeat Rate
        self.combo_box_use_data_repeat_rate.setCurrentText(settings['repeat_rate']['use_data'])

        # Shannon Entropy
        self.combo_box_use_data_shannon_entropy.setCurrentText(settings['shannon_entropy']['use_data'])

    def apply_settings(self):
        # HD-D
        self.settings_custom['hdd']['sample_size'] = self.spin_box_sample_size.value()

        # LogTTR
        self.settings_custom['logttr']['variant'] = self.combo_box_variant.currentText()

        # Mean Segmental TTR
        self.settings_custom['msttr']['num_tokens_in_each_seg'] = self.spin_box_num_tokens_in_each_seg.value()

        # Measure of Textual Lexical Diversity
        self.settings_custom['mtld']['factor_size'] = self.spin_box_factor_size.value()

        # Moving-average TTR
        self.settings_custom['mattr']['window_size'] = self.spin_box_window_size.value()

        # Repeat Rate
        self.settings_custom['repeat_rate']['use_data'] = self.combo_box_use_data_repeat_rate.currentText()

        # Shannon Entropy
        self.settings_custom['shannon_entropy']['use_data'] = self.combo_box_use_data_shannon_entropy.currentText()

        return True

# Measures - Dispersion
class Wl_Settings_Measures_Dispersion(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['measures']['dispersion']
        self.settings_custom = self.main.settings_custom['measures']['dispersion']

        # General Settings
        self.group_box_general_settings = QGroupBox(self.tr('General Settings'), self)

        (
            self.label_dispersion_divide_each_file_into,
            self.spin_box_dispersion_num_sub_sections,
            self.label_dispersion_sub_sections
        ) = wl_widgets.wl_widgets_num_sub_sections(self)

        self.group_box_general_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_general_settings.layout().addWidget(self.label_dispersion_divide_each_file_into, 0, 0)
        self.group_box_general_settings.layout().addWidget(self.spin_box_dispersion_num_sub_sections, 0, 1)
        self.group_box_general_settings.layout().addWidget(self.label_dispersion_sub_sections, 0, 2)

        self.group_box_general_settings.layout().setColumnStretch(3, 1)

        self.group_box_griess_dp = QGroupBox(self.tr("Gries's DP"), self)

        self.checkbox_griess_dp_apply_normalization = QCheckBox(self.tr('Apply normalization'), self)

        self.group_box_griess_dp.setLayout(wl_layouts.Wl_Layout())
        self.group_box_griess_dp.layout().addWidget(self.checkbox_griess_dp_apply_normalization, 0, 0)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_general_settings, 0, 0)
        self.layout().addWidget(self.group_box_griess_dp, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(2, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # General Settings
        self.spin_box_dispersion_num_sub_sections.setValue(settings['general_settings']['num_sub_sections'])

        # Gries's DP
        self.checkbox_griess_dp_apply_normalization.setChecked(settings['griess_dp']['apply_normalization'])

    def apply_settings(self):
        # General Settings
        self.settings_custom['general_settings']['num_sub_sections'] = self.spin_box_dispersion_num_sub_sections.value()

        # Gries's DP
        self.settings_custom['griess_dp']['apply_normalization'] = self.checkbox_griess_dp_apply_normalization.isChecked()

        return True

# Measures - Adjusted Frequency
class Wl_Settings_Measures_Adjusted_Freq(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['measures']['adjusted_freq']
        self.settings_custom = self.main.settings_custom['measures']['adjusted_freq']

        # General Settings
        self.group_box_general_settings = QGroupBox(self.tr('General Settings'), self)

        (
            self.label_adjusted_freq_divide_each_file_into,
            self.spin_box_adjusted_freq_num_sub_sections,
            self.label_adjusted_freq_sub_sections
        ) = wl_widgets.wl_widgets_num_sub_sections(self)

        self.group_box_general_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_general_settings.layout().addWidget(self.label_adjusted_freq_divide_each_file_into, 0, 0)
        self.group_box_general_settings.layout().addWidget(self.spin_box_adjusted_freq_num_sub_sections, 0, 1)
        self.group_box_general_settings.layout().addWidget(self.label_adjusted_freq_sub_sections, 0, 2)

        self.group_box_general_settings.layout().setColumnStretch(3, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_general_settings, 0, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(1, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # General Settings
        self.spin_box_adjusted_freq_num_sub_sections.setValue(settings['general_settings']['num_sub_sections'])

    def apply_settings(self):
        # General Settings
        self.settings_custom['general_settings']['num_sub_sections'] = self.spin_box_adjusted_freq_num_sub_sections.value()

        return True

# Measures - Statistical Significance
class Wl_Settings_Measures_Statistical_Significance(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['measures']['statistical_significance']
        self.settings_custom = self.main.settings_custom['measures']['statistical_significance']

        # Fisher's Exact Test
        self.group_box_fishers_exact_test = QGroupBox(self.tr("Fisher's Exact Test"), self)

        (
            self.label_fishers_exact_test_direction,
            self.combo_box_fishers_exact_test_direction
        ) = wl_widgets.wl_widgets_direction(self)

        self.group_box_fishers_exact_test.setLayout(wl_layouts.Wl_Layout())
        self.group_box_fishers_exact_test.layout().addWidget(self.label_fishers_exact_test_direction, 0, 0)
        self.group_box_fishers_exact_test.layout().addWidget(self.combo_box_fishers_exact_test_direction, 0, 1)

        self.group_box_fishers_exact_test.layout().setColumnStretch(2, 1)

        # Log-likelihood Ratio Test
        self.group_box_log_likelihood_ratio_test = QGroupBox(self.tr('Log-likelihood Ratio Test'), self)

        self.checkbox_log_likelihood_ratio_test_apply_correction = QCheckBox(self.tr("Apply Yates's correction for continuity"))

        self.group_box_log_likelihood_ratio_test.setLayout(wl_layouts.Wl_Layout())
        self.group_box_log_likelihood_ratio_test.layout().addWidget(self.checkbox_log_likelihood_ratio_test_apply_correction, 0, 0)

        # Mann-Whitney U Test
        self.group_box_mann_whitney_u_test = QGroupBox(self.tr('Mann-Whitney U Test'), self)

        (
            self.label_mann_whitney_u_test_divide_each_file_into,
            self.spin_box_mann_whitney_u_test_num_sub_sections,
            self.label_mann_whitney_u_test_sub_sections
        ) = wl_widgets.wl_widgets_num_sub_sections(self)

        (
            self.label_mann_whitney_u_test_use_data,
            self.combo_box_mann_whitney_u_test_use_data
        ) = wl_widgets.wl_widgets_use_data_freq(self)
        (
            self.label_mann_whitney_u_test_direction,
            self.combo_box_mann_whitney_u_test_direction
        ) = wl_widgets.wl_widgets_direction(self)
        self.checkbox_mann_whitney_u_test_apply_correction = QCheckBox(self.tr('Apply continuity correction'), self)

        layout_mann_whitney_u_test_num_sub_sections = wl_layouts.Wl_Layout()
        layout_mann_whitney_u_test_num_sub_sections.addWidget(self.label_mann_whitney_u_test_divide_each_file_into, 0, 0)
        layout_mann_whitney_u_test_num_sub_sections.addWidget(self.spin_box_mann_whitney_u_test_num_sub_sections, 0, 1)
        layout_mann_whitney_u_test_num_sub_sections.addWidget(self.label_mann_whitney_u_test_sub_sections, 0, 2)

        layout_mann_whitney_u_test_num_sub_sections.setColumnStretch(3, 1)

        self.group_box_mann_whitney_u_test.setLayout(wl_layouts.Wl_Layout())
        self.group_box_mann_whitney_u_test.layout().addLayout(layout_mann_whitney_u_test_num_sub_sections, 0, 0, 1, 3)
        self.group_box_mann_whitney_u_test.layout().addWidget(self.label_mann_whitney_u_test_use_data, 1, 0)
        self.group_box_mann_whitney_u_test.layout().addWidget(self.combo_box_mann_whitney_u_test_use_data, 1, 1)
        self.group_box_mann_whitney_u_test.layout().addWidget(self.label_mann_whitney_u_test_direction, 2, 0)
        self.group_box_mann_whitney_u_test.layout().addWidget(self.combo_box_mann_whitney_u_test_direction, 2, 1)
        self.group_box_mann_whitney_u_test.layout().addWidget(self.checkbox_mann_whitney_u_test_apply_correction, 3, 0, 1, 3)

        self.group_box_mann_whitney_u_test.layout().setColumnStretch(3, 1)

        # Pearson's Chi-squared Test
        self.group_box_pearsons_chi_squared_test = QGroupBox(self.tr("Pearson's Chi-squared Test"), self)

        self.checkbox_pearsons_chi_squared_test_apply_correction = QCheckBox(self.tr("Apply Yates's correction for continuity"))

        self.group_box_pearsons_chi_squared_test.setLayout(wl_layouts.Wl_Layout())
        self.group_box_pearsons_chi_squared_test.layout().addWidget(self.checkbox_pearsons_chi_squared_test_apply_correction, 0, 0)

        # Student's t-test (1-sample)
        self.group_box_students_t_test_1_sample = QGroupBox(self.tr("Student's t-test (1-sample)"), self)

        (
            self.label_students_t_test_1_sample_direction,
            self.combo_box_students_t_test_1_sample_direction
        ) = wl_widgets.wl_widgets_direction(self)

        self.group_box_students_t_test_1_sample.setLayout(wl_layouts.Wl_Layout())
        self.group_box_students_t_test_1_sample.layout().addWidget(self.label_students_t_test_1_sample_direction, 0, 0)
        self.group_box_students_t_test_1_sample.layout().addWidget(self.combo_box_students_t_test_1_sample_direction, 0, 1)

        self.group_box_students_t_test_1_sample.layout().setColumnStretch(2, 1)

        # Student's t-test (2-sample)
        self.group_box_students_t_test_2_sample = QGroupBox(self.tr("Student's t-test (2-sample)"), self)

        (
            self.label_students_t_test_2_sample_divide_each_file_into,
            self.spin_box_students_t_test_2_sample_num_sub_sections,
            self.label_students_t_test_2_sample_sub_sections
        ) = wl_widgets.wl_widgets_num_sub_sections(self)
        (
            self.label_students_t_test_2_sample_use_data,
            self.combo_box_students_t_test_2_sample_use_data
        ) = wl_widgets.wl_widgets_use_data_freq(self)
        (
            self.label_students_t_test_2_sample_direction,
            self.combo_box_students_t_test_2_sample_direction
        ) = wl_widgets.wl_widgets_direction(self)

        layout_students_t_test_2_sample_num_sub_sections = wl_layouts.Wl_Layout()
        layout_students_t_test_2_sample_num_sub_sections.addWidget(self.label_students_t_test_2_sample_divide_each_file_into, 0, 0)
        layout_students_t_test_2_sample_num_sub_sections.addWidget(self.spin_box_students_t_test_2_sample_num_sub_sections, 0, 1)
        layout_students_t_test_2_sample_num_sub_sections.addWidget(self.label_students_t_test_2_sample_sub_sections, 0, 2)

        layout_students_t_test_2_sample_num_sub_sections.setColumnStretch(3, 1)

        self.group_box_students_t_test_2_sample.setLayout(wl_layouts.Wl_Layout())
        self.group_box_students_t_test_2_sample.layout().addLayout(layout_students_t_test_2_sample_num_sub_sections, 0, 0, 1, 3)
        self.group_box_students_t_test_2_sample.layout().addWidget(self.label_students_t_test_2_sample_use_data, 1, 0)
        self.group_box_students_t_test_2_sample.layout().addWidget(self.combo_box_students_t_test_2_sample_use_data, 1, 1)
        self.group_box_students_t_test_2_sample.layout().addWidget(self.label_students_t_test_2_sample_direction, 2, 0)
        self.group_box_students_t_test_2_sample.layout().addWidget(self.combo_box_students_t_test_2_sample_direction, 2, 1)

        self.group_box_students_t_test_2_sample.layout().setColumnStretch(2, 1)

        # Z-test
        self.group_box_z_test = QGroupBox(self.tr('Z-test'), self)

        (
            self.label_z_test_direction,
            self.combo_box_z_test_direction
        ) = wl_widgets.wl_widgets_direction(self)

        self.group_box_z_test.setLayout(wl_layouts.Wl_Layout())
        self.group_box_z_test.layout().addWidget(self.label_z_test_direction, 0, 0)
        self.group_box_z_test.layout().addWidget(self.combo_box_z_test_direction, 0, 1)

        self.group_box_z_test.layout().setColumnStretch(2, 1)

        # Z-test (Berry-Rogghe)
        self.group_box_z_test_berry_rogghe = QGroupBox(self.tr('Z-test (Berry-Rogghe)'), self)

        (
            self.label_z_test_berry_rogghe_direction,
            self.combo_box_z_test_berry_rogghe_direction
        ) = wl_widgets.wl_widgets_direction(self)

        self.group_box_z_test_berry_rogghe.setLayout(wl_layouts.Wl_Layout())
        self.group_box_z_test_berry_rogghe.layout().addWidget(self.label_z_test_berry_rogghe_direction, 0, 0)
        self.group_box_z_test_berry_rogghe.layout().addWidget(self.combo_box_z_test_berry_rogghe_direction, 0, 1)

        self.group_box_z_test_berry_rogghe.layout().setColumnStretch(2, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_fishers_exact_test, 0, 0)
        self.layout().addWidget(self.group_box_log_likelihood_ratio_test, 1, 0)
        self.layout().addWidget(self.group_box_mann_whitney_u_test, 2, 0)
        self.layout().addWidget(self.group_box_pearsons_chi_squared_test, 3, 0)
        self.layout().addWidget(self.group_box_students_t_test_1_sample, 4, 0)
        self.layout().addWidget(self.group_box_students_t_test_2_sample, 5, 0)
        self.layout().addWidget(self.group_box_z_test, 6, 0)
        self.layout().addWidget(self.group_box_z_test_berry_rogghe, 7, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(8, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Fisher's Exact Test
        self.combo_box_fishers_exact_test_direction.setCurrentText(settings['fishers_exact_test']['direction'])

        # Log-likelihood Ratio Test
        self.checkbox_log_likelihood_ratio_test_apply_correction.setChecked(settings['log_likelihood_ratio_test']['apply_correction'])

        # Mann-Whitney U Test
        self.spin_box_mann_whitney_u_test_num_sub_sections.setValue(settings['mann_whitney_u_test']['num_sub_sections'])
        self.combo_box_mann_whitney_u_test_use_data.setCurrentText(settings['mann_whitney_u_test']['use_data'])
        self.combo_box_mann_whitney_u_test_direction.setCurrentText(settings['mann_whitney_u_test']['direction'])
        self.checkbox_mann_whitney_u_test_apply_correction.setChecked(settings['mann_whitney_u_test']['apply_correction'])

        # Pearson's Chi-squared Test
        self.checkbox_pearsons_chi_squared_test_apply_correction.setChecked(settings['pearsons_chi_squared_test']['apply_correction'])

        # Student's t-test (1-sample)
        self.combo_box_students_t_test_1_sample_direction.setCurrentText(settings['students_t_test_1_sample']['direction'])

        # Student's t-test (2-sample)
        self.spin_box_students_t_test_2_sample_num_sub_sections.setValue(settings['students_t_test_2_sample']['num_sub_sections'])
        self.combo_box_students_t_test_2_sample_use_data.setCurrentText(settings['students_t_test_2_sample']['use_data'])
        self.combo_box_students_t_test_2_sample_direction.setCurrentText(settings['students_t_test_2_sample']['direction'])

        # Z-test
        self.combo_box_z_test_direction.setCurrentText(settings['z_test']['direction'])

        # Z-test (Berry-Rogghe)
        self.combo_box_z_test_berry_rogghe_direction.setCurrentText(settings['z_test_berry_rogghe']['direction'])

    def apply_settings(self):
        # Fisher's Exact Test
        self.settings_custom['fishers_exact_test']['direction'] = self.combo_box_fishers_exact_test_direction.currentText()

        # Log-likelihood Ratio Test
        self.settings_custom['log_likelihood_ratio_test']['apply_correction'] = self.checkbox_log_likelihood_ratio_test_apply_correction.isChecked()

        # Mann-Whitney U Test
        self.settings_custom['mann_whitney_u_test']['num_sub_sections'] = self.spin_box_mann_whitney_u_test_num_sub_sections.value()
        self.settings_custom['mann_whitney_u_test']['use_data'] = self.combo_box_mann_whitney_u_test_use_data.currentText()
        self.settings_custom['mann_whitney_u_test']['direction'] = self.combo_box_mann_whitney_u_test_direction.currentText()
        self.settings_custom['mann_whitney_u_test']['apply_correction'] = self.checkbox_mann_whitney_u_test_apply_correction.isChecked()

        # Pearson's Chi-squared Test
        self.settings_custom['pearsons_chi_squared_test']['apply_correction'] = self.checkbox_pearsons_chi_squared_test_apply_correction.isChecked()

        # Student's t-test (1-sample)
        self.settings_custom['students_t_test_1_sample']['direction'] = self.combo_box_students_t_test_1_sample_direction.currentText()

        # Student's t-test (2-sample)
        self.settings_custom['students_t_test_2_sample']['num_sub_sections'] = self.spin_box_students_t_test_2_sample_num_sub_sections.value()
        self.settings_custom['students_t_test_2_sample']['use_data'] = self.combo_box_students_t_test_2_sample_use_data.currentText()
        self.settings_custom['students_t_test_2_sample']['direction'] = self.combo_box_students_t_test_2_sample_direction.currentText()

        # Z-test
        self.settings_custom['z_test']['direction'] = self.combo_box_z_test_direction.currentText()

        # Z-test (Berry-Rogghe)
        self.settings_custom['z_test_berry_rogghe']['direction'] = self.combo_box_z_test_berry_rogghe_direction.currentText()

        return True

# Measures - Bayes Factor
class Wl_Settings_Measures_Bayes_Factor(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['measures']['bayes_factor']
        self.settings_custom = self.main.settings_custom['measures']['bayes_factor']

        # Log-likelihood Ratio Test
        self.group_box_log_likelihood_ratio_test = QGroupBox(self.tr('Log-likelihood Ratio Test'), self)

        self.checkbox_log_likelihood_ratio_test_apply_correction = QCheckBox(self.tr("Apply Yates's correction for continuity"))

        self.group_box_log_likelihood_ratio_test.setLayout(wl_layouts.Wl_Layout())
        self.group_box_log_likelihood_ratio_test.layout().addWidget(self.checkbox_log_likelihood_ratio_test_apply_correction, 0, 0)

        # Student's t-test (2-sample)
        self.group_box_students_t_test_2_sample = QGroupBox(self.tr("Student's t-test (2-sample)"), self)

        (
            self.label_students_t_test_2_sample_divide_each_file_into,
            self.spin_box_students_t_test_2_sample_num_sub_sections,
            self.label_students_t_test_2_sample_sub_sections
        ) = wl_widgets.wl_widgets_num_sub_sections(self)
        (
            self.label_students_t_test_2_sample_use_data,
            self.combo_box_students_t_test_2_sample_use_data
        ) = wl_widgets.wl_widgets_use_data_freq(self)
        (
            self.label_students_t_test_2_sample_direction,
            self.combo_box_students_t_test_2_sample_direction
        ) = wl_widgets.wl_widgets_direction(self)

        layout_students_t_test_2_sample_num_sub_sections = wl_layouts.Wl_Layout()
        layout_students_t_test_2_sample_num_sub_sections.addWidget(self.label_students_t_test_2_sample_divide_each_file_into, 0, 0)
        layout_students_t_test_2_sample_num_sub_sections.addWidget(self.spin_box_students_t_test_2_sample_num_sub_sections, 0, 1)
        layout_students_t_test_2_sample_num_sub_sections.addWidget(self.label_students_t_test_2_sample_sub_sections, 0, 2)

        layout_students_t_test_2_sample_num_sub_sections.setColumnStretch(3, 1)

        self.group_box_students_t_test_2_sample.setLayout(wl_layouts.Wl_Layout())
        self.group_box_students_t_test_2_sample.layout().addLayout(layout_students_t_test_2_sample_num_sub_sections, 0, 0, 1, 3)
        self.group_box_students_t_test_2_sample.layout().addWidget(self.label_students_t_test_2_sample_use_data, 1, 0)
        self.group_box_students_t_test_2_sample.layout().addWidget(self.combo_box_students_t_test_2_sample_use_data, 1, 1)
        self.group_box_students_t_test_2_sample.layout().addWidget(self.label_students_t_test_2_sample_direction, 2, 0)
        self.group_box_students_t_test_2_sample.layout().addWidget(self.combo_box_students_t_test_2_sample_direction, 2, 1)

        self.group_box_students_t_test_2_sample.layout().setColumnStretch(2, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_log_likelihood_ratio_test, 0, 0)
        self.layout().addWidget(self.group_box_students_t_test_2_sample, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(2, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Log-likelihood Ratio Test
        self.checkbox_log_likelihood_ratio_test_apply_correction.setChecked(settings['log_likelihood_ratio_test']['apply_correction'])

        # Student's t-test (2-sample)
        self.spin_box_students_t_test_2_sample_num_sub_sections.setValue(settings['students_t_test_2_sample']['num_sub_sections'])
        self.combo_box_students_t_test_2_sample_use_data.setCurrentText(settings['students_t_test_2_sample']['use_data'])
        self.combo_box_students_t_test_2_sample_direction.setCurrentText(settings['students_t_test_2_sample']['direction'])

    def apply_settings(self):
        # Log-likelihood Ratio Test
        self.settings_custom['log_likelihood_ratio_test']['apply_correction'] = self.checkbox_log_likelihood_ratio_test_apply_correction.isChecked()

        # Student's t-test (2-sample)
        self.settings_custom['students_t_test_2_sample']['num_sub_sections'] = self.spin_box_students_t_test_2_sample_num_sub_sections.value()
        self.settings_custom['students_t_test_2_sample']['use_data'] = self.combo_box_students_t_test_2_sample_use_data.currentText()
        self.settings_custom['students_t_test_2_sample']['direction'] = self.combo_box_students_t_test_2_sample_direction.currentText()

        return True

# Measures - Effect Size
class Wl_Combo_Box_Base_Log(wl_boxes.Wl_Combo_Box):
    # pylint: disable=inconsistent-return-statements

    def __init__(self, parent):
        super().__init__(parent)

        self.addItems([
            '2',
            '10',
            _tr('wl_settings_measures', 'Base of natural logarithm')
        ])

    def get_base_log(self):
        if self.currentText() == '2':
            return 2
        elif self.currentText() == '10':
            return 10
        elif self.currentText() == _tr('wl_settings_measures', 'Base of natural logarithm'):
            return math.e

    def set_base_log(self, base_log):
        if base_log == 2:
            self.setCurrentText('2')
        elif base_log == 10:
            self.setCurrentText('10')
        elif base_log == math.e:
            self.setCurrentText(_tr('wl_settings_measures', 'Base of natural logarithm'))

class Wl_Settings_Measures_Effect_Size(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['measures']['effect_size']
        self.settings_custom = self.main.settings_custom['measures']['effect_size']

        # Kilgarriff's Ratio
        self.group_box_kilgarriffs_ratio = QGroupBox(self.tr("Kilgarriff's Ratio"), self)

        self.label_kilgarriffs_ratio_smoothing_param = QLabel(self.tr('Smoothing parameter:'), self)
        self.spin_box_kilgarriffs_ratio_smoothing_param = wl_boxes.Wl_Double_Spin_Box(self)

        self.spin_box_kilgarriffs_ratio_smoothing_param.setRange(0.01, 10000)

        self.group_box_kilgarriffs_ratio.setLayout(wl_layouts.Wl_Layout())
        self.group_box_kilgarriffs_ratio.layout().addWidget(self.label_kilgarriffs_ratio_smoothing_param, 0, 0)
        self.group_box_kilgarriffs_ratio.layout().addWidget(self.spin_box_kilgarriffs_ratio_smoothing_param, 0, 1)

        self.group_box_kilgarriffs_ratio.layout().setColumnStretch(2, 1)

        # Mutual Information
        self.group_box_mi = QGroupBox(self.tr('Mutual Information'), self)

        self.label_mi_base_log = QLabel(self.tr('Base of logarithm:'), self)
        self.combo_box_mi_base_log = Wl_Combo_Box_Base_Log(self)

        self.group_box_mi.setLayout(wl_layouts.Wl_Layout())
        self.group_box_mi.layout().addWidget(self.label_mi_base_log, 0, 0)
        self.group_box_mi.layout().addWidget(self.combo_box_mi_base_log, 0, 1)

        self.group_box_mi.layout().setColumnStretch(2, 1)

        # Mutual Information (Normalized)
        self.group_box_nmi = QGroupBox(self.tr('Mutual Information (Normalized)'), self)

        self.label_nmi_base_log = QLabel(self.tr('Base of logarithm:'), self)
        self.combo_box_nmi_base_log = Wl_Combo_Box_Base_Log(self)

        self.group_box_nmi.setLayout(wl_layouts.Wl_Layout())
        self.group_box_nmi.layout().addWidget(self.label_nmi_base_log, 0, 0)
        self.group_box_nmi.layout().addWidget(self.combo_box_nmi_base_log, 0, 1)

        self.group_box_nmi.layout().setColumnStretch(2, 1)

        # Pointwise Mutual Information
        self.group_box_pmi = QGroupBox(self.tr('Pointwise Mutual Information'), self)

        self.label_pmi_base_log = QLabel(self.tr('Base of logarithm:'), self)
        self.combo_box_pmi_base_log = Wl_Combo_Box_Base_Log(self)

        self.group_box_pmi.setLayout(wl_layouts.Wl_Layout())
        self.group_box_pmi.layout().addWidget(self.label_pmi_base_log, 0, 0)
        self.group_box_pmi.layout().addWidget(self.combo_box_pmi_base_log, 0, 1)

        self.group_box_pmi.layout().setColumnStretch(2, 1)

        # Pointwise Mutual Information (Cubic)
        self.group_box_im3 = QGroupBox(self.tr('Pointwise Mutual Information (Cubic)'), self)

        self.label_im3_base_log = QLabel(self.tr('Base of logarithm:'), self)
        self.combo_box_im3_base_log = Wl_Combo_Box_Base_Log(self)

        self.group_box_im3.setLayout(wl_layouts.Wl_Layout())
        self.group_box_im3.layout().addWidget(self.label_im3_base_log, 0, 0)
        self.group_box_im3.layout().addWidget(self.combo_box_im3_base_log, 0, 1)

        self.group_box_im3.layout().setColumnStretch(2, 1)

        # Pointwise Mutual Information (Normalized)
        self.group_box_npmi = QGroupBox(self.tr('Pointwise Mutual Information (Normalized)'), self)

        self.label_npmi_base_log = QLabel(self.tr('Base of logarithm:'), self)
        self.combo_box_npmi_base_log = Wl_Combo_Box_Base_Log(self)

        self.group_box_npmi.setLayout(wl_layouts.Wl_Layout())
        self.group_box_npmi.layout().addWidget(self.label_npmi_base_log, 0, 0)
        self.group_box_npmi.layout().addWidget(self.combo_box_npmi_base_log, 0, 1)

        self.group_box_npmi.layout().setColumnStretch(2, 1)

        # Pointwise Mutual Information (Squared)
        self.group_box_im2 = QGroupBox(self.tr('Pointwise Mutual Information (Squared)'), self)

        self.label_im2_base_log = QLabel(self.tr('Base of logarithm:'), self)
        self.combo_box_im2_base_log = Wl_Combo_Box_Base_Log(self)

        self.group_box_im2.setLayout(wl_layouts.Wl_Layout())
        self.group_box_im2.layout().addWidget(self.label_im2_base_log, 0, 0)
        self.group_box_im2.layout().addWidget(self.combo_box_im2_base_log, 0, 1)

        self.group_box_im2.layout().setColumnStretch(2, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_kilgarriffs_ratio, 0, 0)
        self.layout().addWidget(self.group_box_mi, 1, 0)
        self.layout().addWidget(self.group_box_nmi, 2, 0)
        self.layout().addWidget(self.group_box_pmi, 3, 0)
        self.layout().addWidget(self.group_box_im3, 4, 0)
        self.layout().addWidget(self.group_box_npmi, 5, 0)
        self.layout().addWidget(self.group_box_im2, 6, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(7, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Kilgarriff's Ratio
        self.spin_box_kilgarriffs_ratio_smoothing_param.setValue(settings['kilgarriffs_ratio']['smoothing_param'])

        # Mutual Information
        self.combo_box_mi_base_log.set_base_log(settings['mi']['base_log'])

        # Mutual Information (Normalized)
        self.combo_box_nmi_base_log.set_base_log(settings['nmi']['base_log'])

        # Pointwise Mutual Information
        self.combo_box_pmi_base_log.set_base_log(settings['pmi']['base_log'])

        # Pointwise Mutual Information (Cubic)
        self.combo_box_im3_base_log.set_base_log(settings['im3']['base_log'])

        # Pointwise Mutual Information (Normalized)
        self.combo_box_npmi_base_log.set_base_log(settings['npmi']['base_log'])

        # Pointwise Mutual Information (Squared)
        self.combo_box_im2_base_log.set_base_log(settings['im2']['base_log'])

    def apply_settings(self):
        # Kilgarriff's Ratio
        self.settings_custom['kilgarriffs_ratio']['smoothing_param'] = self.spin_box_kilgarriffs_ratio_smoothing_param.value()

        # Mutual Information
        self.settings_custom['mi']['base_log'] = self.combo_box_mi_base_log.get_base_log()

        # Mutual Information (Normalized)
        self.settings_custom['nmi']['base_log'] = self.combo_box_nmi_base_log.get_base_log()

        # Pointwise Mutual Information
        self.settings_custom['pmi']['base_log'] = self.combo_box_pmi_base_log.get_base_log()

        # Pointwise Mutual Information (Cubic)
        self.settings_custom['im3']['base_log'] = self.combo_box_im3_base_log.get_base_log()

        # Pointwise Mutual Information (Normalized)
        self.settings_custom['npmi']['base_log'] = self.combo_box_npmi_base_log.get_base_log()

        # Pointwise Mutual Information (Squared)
        self.settings_custom['im2']['base_log'] = self.combo_box_im2_base_log.get_base_log()

        return True
