# ----------------------------------------------------------------------
# Wordless: Settings - Tables
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

from wordless.wl_settings import wl_settings
from wordless.wl_widgets import wl_boxes, wl_layouts

class Wl_Settings_Tables(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['tables']
        self.settings_custom = self.main.settings_custom['tables']

        # Rank Settings
        self.group_box_rank_settings = QGroupBox(self.tr('Rank Settings'), self)

        self.checkbox_continue_numbering_after_ties = QCheckBox(self.tr('Continue numbering after ties'), self)

        self.group_box_rank_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_rank_settings.layout().addWidget(self.checkbox_continue_numbering_after_ties, 0, 0)

        # Precision Settings
        self.group_box_precision_settings = QGroupBox(self.tr('Precision Settings'), self)

        self.label_precision_decimals = QLabel(self.tr('Decimals:'), self)
        self.spin_box_precision_decimals = wl_boxes.Wl_Spin_Box(self)
        self.label_precision_pcts = QLabel(self.tr('Percentages:'), self)
        self.spin_box_precision_pcts = wl_boxes.Wl_Spin_Box(self)
        self.label_precision_p_vals = QLabel(self.tr('p-values:'), self)
        self.spin_box_precision_p_vals = wl_boxes.Wl_Spin_Box(self)

        self.spin_box_precision_decimals.setRange(0, 10)
        self.spin_box_precision_pcts.setRange(0, 10)
        self.spin_box_precision_p_vals.setRange(0, 15)

        self.group_box_precision_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_precision_settings.layout().addWidget(self.label_precision_decimals, 0, 0)
        self.group_box_precision_settings.layout().addWidget(self.spin_box_precision_decimals, 0, 1)
        self.group_box_precision_settings.layout().addWidget(self.label_precision_pcts, 1, 0)
        self.group_box_precision_settings.layout().addWidget(self.spin_box_precision_pcts, 1, 1)
        self.group_box_precision_settings.layout().addWidget(self.label_precision_p_vals, 2, 0)
        self.group_box_precision_settings.layout().addWidget(self.spin_box_precision_p_vals, 2, 1)

        self.group_box_precision_settings.layout().setColumnStretch(2, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_rank_settings, 0, 0)
        self.layout().addWidget(self.group_box_precision_settings, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(2, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Rank Settings
        self.checkbox_continue_numbering_after_ties.setChecked(settings['rank_settings']['continue_numbering_after_ties'])

        # Precision Settings
        self.spin_box_precision_decimals.setValue(settings['precision_settings']['precision_decimals'])
        self.spin_box_precision_pcts.setValue(settings['precision_settings']['precision_pcts'])
        self.spin_box_precision_p_vals.setValue(settings['precision_settings']['precision_p_vals'])

    def apply_settings(self):
        # Rank Settings
        self.settings_custom['rank_settings']['continue_numbering_after_ties'] = self.checkbox_continue_numbering_after_ties.isChecked()

        # Precision Settings
        self.settings_custom['precision_settings']['precision_decimals'] = self.spin_box_precision_decimals.value()
        self.settings_custom['precision_settings']['precision_pcts'] = self.spin_box_precision_pcts.value()
        self.settings_custom['precision_settings']['precision_p_vals'] = self.spin_box_precision_p_vals.value()

        return True

class Wl_Settings_Tables_Profiler(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['tables']['profiler']
        self.settings_custom = self.main.settings_custom['tables']['profiler']

        # General Settings
        self.group_box_general_settings = QGroupBox(self.tr('General Settings'), self)

        self.label_num_tokens_section_sttr = QLabel(self.tr('Number of tokens in each section when calculating standardized type-token ratio:'), self)
        self.spin_num_tokens_section_sttr = wl_boxes.Wl_Spin_Box(self)

        self.spin_num_tokens_section_sttr.setRange(100, 10000)

        self.group_box_general_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_general_settings.layout().addWidget(self.label_num_tokens_section_sttr, 0, 0)
        self.group_box_general_settings.layout().addWidget(self.spin_num_tokens_section_sttr, 0, 1)

        self.group_box_general_settings.layout().setColumnStretch(2, 1)

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
        self.spin_num_tokens_section_sttr.setValue(settings['general_settings']['num_tokens_section_sttr'])

    def apply_settings(self):
        # General Settings
        self.settings_custom['general_settings']['num_tokens_section_sttr'] = self.spin_num_tokens_section_sttr.value()

        return True
