# ----------------------------------------------------------------------
# Wordless: Settings - Measures
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

from PyQt5.QtWidgets import QCheckBox, QGroupBox, QLabel

from wl_settings import wl_settings
from wl_widgets import wl_boxes, wl_layouts, wl_widgets

# Measures - Dispersion
class Wl_Settings_Dispersion(wl_settings.Wl_Settings_Node):
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
        self.spin_box_dispersion_num_sub_sections.setValue(settings['general_settings']['num_sub_sections'])

    def apply_settings(self):
        # General Settings
        self.settings_custom['general_settings']['num_sub_sections'] = self.spin_box_dispersion_num_sub_sections.value()

        return True

# Measures - Adjusted Frequency
class Wl_Settings_Adjusted_Freq(wl_settings.Wl_Settings_Node):
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
class Wl_Settings_Statistical_Significance(wl_settings.Wl_Settings_Node):
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

        layout_students_t_test_2_sample_num_sub_sections = wl_layouts.Wl_Layout()
        layout_students_t_test_2_sample_num_sub_sections.addWidget(self.label_students_t_test_2_sample_divide_each_file_into, 0, 0)
        layout_students_t_test_2_sample_num_sub_sections.addWidget(self.spin_box_students_t_test_2_sample_num_sub_sections, 0, 1)
        layout_students_t_test_2_sample_num_sub_sections.addWidget(self.label_students_t_test_2_sample_sub_sections, 0, 2)

        layout_students_t_test_2_sample_num_sub_sections.setColumnStretch(3, 1)

        self.group_box_students_t_test_2_sample.setLayout(wl_layouts.Wl_Layout())
        self.group_box_students_t_test_2_sample.layout().addLayout(layout_students_t_test_2_sample_num_sub_sections, 0, 0, 1, 3)
        self.group_box_students_t_test_2_sample.layout().addWidget(self.label_students_t_test_2_sample_use_data, 1, 0)
        self.group_box_students_t_test_2_sample.layout().addWidget(self.combo_box_students_t_test_2_sample_use_data, 1, 1)

        self.group_box_students_t_test_2_sample.layout().setColumnStretch(2, 1)

        # Welch's t-test
        self.group_box_welchs_t_test = QGroupBox(self.tr("Welch's t-test"), self)

        (
            self.label_welchs_t_test_divide_each_file_into,
            self.spin_box_welchs_t_test_num_sub_sections,
            self.label_welchs_t_test_sub_sections
        ) = wl_widgets.wl_widgets_num_sub_sections(self)

        (
            self.label_welchs_t_test_use_data,
            self.combo_box_welchs_t_test_use_data
        ) = wl_widgets.wl_widgets_use_data_freq(self)

        layout_welchs_t_test_num_sub_sections = wl_layouts.Wl_Layout()
        layout_welchs_t_test_num_sub_sections.addWidget(self.label_welchs_t_test_divide_each_file_into, 0, 0)
        layout_welchs_t_test_num_sub_sections.addWidget(self.spin_box_welchs_t_test_num_sub_sections, 0, 1)
        layout_welchs_t_test_num_sub_sections.addWidget(self.label_welchs_t_test_sub_sections, 0, 2)

        layout_welchs_t_test_num_sub_sections.setColumnStretch(3, 1)

        self.group_box_welchs_t_test.setLayout(wl_layouts.Wl_Layout())
        self.group_box_welchs_t_test.layout().addLayout(layout_welchs_t_test_num_sub_sections, 0, 0, 1, 3)
        self.group_box_welchs_t_test.layout().addWidget(self.label_welchs_t_test_use_data, 1, 0)
        self.group_box_welchs_t_test.layout().addWidget(self.combo_box_welchs_t_test_use_data, 1, 1)

        self.group_box_welchs_t_test.layout().setColumnStretch(2, 1)

        # z-score
        self.group_box_z_score = QGroupBox(self.tr('z-score'), self)

        (
            self.label_z_score_direction,
            self.combo_box_z_score_direction
        ) = wl_widgets.wl_widgets_direction(self)

        self.group_box_z_score.setLayout(wl_layouts.Wl_Layout())
        self.group_box_z_score.layout().addWidget(self.label_z_score_direction, 0, 0)
        self.group_box_z_score.layout().addWidget(self.combo_box_z_score_direction, 0, 1)

        self.group_box_z_score.layout().setColumnStretch(2, 1)

        # z-score (Berry-Rogghe)
        self.group_box_z_score_berry_rogghe = QGroupBox(self.tr('z-score (Berry-Rogghe)'), self)

        (
            self.label_z_score_berry_rogghe_direction,
            self.combo_box_z_score_berry_rogghe_direction
        ) = wl_widgets.wl_widgets_direction(self)

        self.group_box_z_score_berry_rogghe.setLayout(wl_layouts.Wl_Layout())
        self.group_box_z_score_berry_rogghe.layout().addWidget(self.label_z_score_berry_rogghe_direction, 0, 0)
        self.group_box_z_score_berry_rogghe.layout().addWidget(self.combo_box_z_score_berry_rogghe_direction, 0, 1)

        self.group_box_z_score_berry_rogghe.layout().setColumnStretch(2, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_fishers_exact_test, 0, 0)
        self.layout().addWidget(self.group_box_log_likelihood_ratio_test, 1, 0)
        self.layout().addWidget(self.group_box_mann_whitney_u_test, 2, 0)
        self.layout().addWidget(self.group_box_pearsons_chi_squared_test, 3, 0)
        self.layout().addWidget(self.group_box_students_t_test_2_sample, 4, 0)
        self.layout().addWidget(self.group_box_welchs_t_test, 5, 0)
        self.layout().addWidget(self.group_box_z_score, 6, 0)
        self.layout().addWidget(self.group_box_z_score_berry_rogghe, 7, 0)

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

        # Student's t-test (2-sample)
        self.spin_box_students_t_test_2_sample_num_sub_sections.setValue(settings['students_t_test_2_sample']['num_sub_sections'])
        self.combo_box_students_t_test_2_sample_use_data.setCurrentText(settings['students_t_test_2_sample']['use_data'])

        # Welch's t-test
        self.spin_box_welchs_t_test_num_sub_sections.setValue(settings['welchs_t_test']['num_sub_sections'])
        self.combo_box_welchs_t_test_use_data.setCurrentText(settings['welchs_t_test']['use_data'])

        # z-score
        self.combo_box_z_score_direction.setCurrentText(settings['z_score']['direction'])

        # z-score (Berry-Rogghe)
        self.combo_box_z_score_berry_rogghe_direction.setCurrentText(settings['z_score_berry_rogghe']['direction'])

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

        # Student's t-test (2-sample)
        self.settings_custom['students_t_test_2_sample']['num_sub_sections'] = self.spin_box_students_t_test_2_sample_num_sub_sections.value()
        self.settings_custom['students_t_test_2_sample']['use_data'] = self.combo_box_students_t_test_2_sample_use_data.currentText()

        # Welch's t-test
        self.settings_custom['welchs_t_test']['num_sub_sections'] = self.spin_box_welchs_t_test_num_sub_sections.value()
        self.settings_custom['welchs_t_test']['use_data'] = self.combo_box_welchs_t_test_use_data.currentText()

        # z-score
        self.settings_custom['z_score']['direction'] = self.combo_box_z_score_direction.currentText()

        # z-score (Berry-Rogghe)
        self.settings_custom['z_score_berry_rogghe']['direction'] = self.combo_box_z_score_berry_rogghe_direction.currentText()

        return True

# Measures - Effect Size
class Wl_Settings_Effect_Size(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['measures']['effect_size']
        self.settings_custom = self.main.settings_custom['measures']['effect_size']

        # Kilgarriff's Ratio
        self.group_box_kilgarriffs_ratio = QGroupBox(self.tr("Kilgarriff's Ratio"), self)

        self.label_kilgarriffs_ratio_smoothing_param = QLabel(self.tr('Smoothing Parameter:'), self)
        self.spin_box_kilgarriffs_ratio_smoothing_param = wl_boxes.Wl_Double_Spin_Box(self)

        self.spin_box_kilgarriffs_ratio_smoothing_param.setRange(0.01, 10000)

        self.group_box_kilgarriffs_ratio.setLayout(wl_layouts.Wl_Layout())
        self.group_box_kilgarriffs_ratio.layout().addWidget(self.label_kilgarriffs_ratio_smoothing_param, 0, 0)
        self.group_box_kilgarriffs_ratio.layout().addWidget(self.spin_box_kilgarriffs_ratio_smoothing_param, 0, 1)

        self.group_box_kilgarriffs_ratio.layout().setColumnStretch(2, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_kilgarriffs_ratio, 0, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(1, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Kilgarriff's Ratio
        self.spin_box_kilgarriffs_ratio_smoothing_param.setValue(settings['kilgarriffs_ratio']['smoothing_param'])

    def apply_settings(self):
        # Kilgarriff's Ratio
        self.settings_custom['kilgarriffs_ratio']['smoothing_param'] = self.spin_box_kilgarriffs_ratio_smoothing_param.value()

        return True
