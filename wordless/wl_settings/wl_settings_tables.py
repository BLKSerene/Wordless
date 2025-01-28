# ----------------------------------------------------------------------
# Wordless: Settings - Tables
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

from PyQt5.QtWidgets import QCheckBox, QGroupBox, QLabel

from wordless.wl_settings import wl_settings
from wordless.wl_widgets import wl_boxes, wl_buttons, wl_layouts

# Tables
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

# Tables - Concordancer
class Wl_Settings_Tables_Concordancer(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['tables']['concordancer']
        self.settings_custom = self.main.settings_custom['tables']['concordancer']

        # Sorting Settings
        self.group_box_sorting_settings = QGroupBox(self.tr('Sorting Settings'), self)

        self.label_highlight_colors = QLabel(self.tr('Highlight colors:'), self)
        self.label_lvl_1 = QLabel(self.tr('Level 1 / Node:'), self)
        self.button_lvl_1 = wl_buttons.wl_button_color(self)
        self.label_lvl_2 = QLabel(self.tr('Level 2:'), self)
        self.button_lvl_2 = wl_buttons.wl_button_color(self)
        self.label_lvl_3 = QLabel(self.tr('Level 3:'), self)
        self.button_lvl_3 = wl_buttons.wl_button_color(self)
        self.label_lvl_4 = QLabel(self.tr('Level 4:'), self)
        self.button_lvl_4 = wl_buttons.wl_button_color(self)
        self.label_lvl_5 = QLabel(self.tr('Level 5:'), self)
        self.button_lvl_5 = wl_buttons.wl_button_color(self)
        self.label_lvl_6 = QLabel(self.tr('Level 6:'), self)
        self.button_lvl_6 = wl_buttons.wl_button_color(self)

        self.group_box_sorting_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_sorting_settings.layout().addWidget(self.label_highlight_colors, 0, 0, 1, 3)
        self.group_box_sorting_settings.layout().addWidget(self.label_lvl_1, 1, 0)
        self.group_box_sorting_settings.layout().addWidget(self.button_lvl_1, 1, 1)
        self.group_box_sorting_settings.layout().addWidget(self.label_lvl_2, 2, 0)
        self.group_box_sorting_settings.layout().addWidget(self.button_lvl_2, 2, 1)
        self.group_box_sorting_settings.layout().addWidget(self.label_lvl_3, 3, 0)
        self.group_box_sorting_settings.layout().addWidget(self.button_lvl_3, 3, 1)
        self.group_box_sorting_settings.layout().addWidget(self.label_lvl_4, 4, 0)
        self.group_box_sorting_settings.layout().addWidget(self.button_lvl_4, 4, 1)
        self.group_box_sorting_settings.layout().addWidget(self.label_lvl_5, 5, 0)
        self.group_box_sorting_settings.layout().addWidget(self.button_lvl_5, 5, 1)
        self.group_box_sorting_settings.layout().addWidget(self.label_lvl_6, 6, 0)
        self.group_box_sorting_settings.layout().addWidget(self.button_lvl_6, 6, 1)

        self.group_box_sorting_settings.layout().setColumnStretch(2, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_sorting_settings, 0, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(1, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Sorting Settings
        self.button_lvl_1.set_color(settings['sorting_settings']['highlight_colors']['lvl_1'])
        self.button_lvl_2.set_color(settings['sorting_settings']['highlight_colors']['lvl_2'])
        self.button_lvl_3.set_color(settings['sorting_settings']['highlight_colors']['lvl_3'])
        self.button_lvl_4.set_color(settings['sorting_settings']['highlight_colors']['lvl_4'])
        self.button_lvl_5.set_color(settings['sorting_settings']['highlight_colors']['lvl_5'])
        self.button_lvl_6.set_color(settings['sorting_settings']['highlight_colors']['lvl_6'])

    def apply_settings(self):
        # Sorting Settings
        self.settings_custom['sorting_settings']['highlight_colors']['lvl_1'] = self.button_lvl_1.get_color()
        self.settings_custom['sorting_settings']['highlight_colors']['lvl_2'] = self.button_lvl_2.get_color()
        self.settings_custom['sorting_settings']['highlight_colors']['lvl_3'] = self.button_lvl_3.get_color()
        self.settings_custom['sorting_settings']['highlight_colors']['lvl_4'] = self.button_lvl_4.get_color()
        self.settings_custom['sorting_settings']['highlight_colors']['lvl_5'] = self.button_lvl_5.get_color()
        self.settings_custom['sorting_settings']['highlight_colors']['lvl_6'] = self.button_lvl_6.get_color()

        return True

# Tables - Parallel Concordancer
class Wl_Settings_Tables_Parallel_Concordancer(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['tables']['parallel_concordancer']
        self.settings_custom = self.main.settings_custom['tables']['parallel_concordancer']

        # Color Settings
        self.group_box_highlight_color_settings = QGroupBox(self.tr('Highlight Color Settings'), self)

        self.label_search_term_color = QLabel(self.tr('Search term color:'), self)
        self.button_search_term_color = wl_buttons.wl_button_color(self)

        self.group_box_highlight_color_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_highlight_color_settings.layout().addWidget(self.label_search_term_color, 0, 0)
        self.group_box_highlight_color_settings.layout().addWidget(self.button_search_term_color, 0, 1)

        self.group_box_highlight_color_settings.layout().setColumnStretch(2, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_highlight_color_settings, 0, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(1, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Color Settings
        self.button_search_term_color.set_color(settings['highlight_color_settings']['search_term_color'])

    def apply_settings(self):
        # Color Settings
        self.settings_custom['highlight_color_settings']['search_term_color'] = self.button_search_term_color.get_color()

        return True

# Settings - Dependency Parser
class Wl_Settings_Tables_Dependency_Parser(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['tables']['dependency_parser']
        self.settings_custom = self.main.settings_custom['tables']['dependency_parser']

        # Color Settings
        self.group_box_highlight_color_settings = QGroupBox(self.tr('Highlight Color Settings'), self)

        self.label_head_color = QLabel(self.tr('Head color:'), self)
        self.button_head_color = wl_buttons.wl_button_color(self)
        self.label_dependent_color = QLabel(self.tr('Dependent color:'), self)
        self.button_dependent_color = wl_buttons.wl_button_color(self)

        self.group_box_highlight_color_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_highlight_color_settings.layout().addWidget(self.label_head_color, 0, 0)
        self.group_box_highlight_color_settings.layout().addWidget(self.button_head_color, 0, 1)
        self.group_box_highlight_color_settings.layout().addWidget(self.label_dependent_color, 1, 0)
        self.group_box_highlight_color_settings.layout().addWidget(self.button_dependent_color, 1, 1)

        self.group_box_highlight_color_settings.layout().setColumnStretch(2, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_highlight_color_settings, 0, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(1, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Color Settings
        self.button_head_color.set_color(settings['highlight_color_settings']['head_color'])
        self.button_dependent_color.set_color(settings['highlight_color_settings']['dependent_color'])

    def apply_settings(self):
        # Color Settings
        self.settings_custom['highlight_color_settings']['head_color'] = self.button_head_color.get_color()
        self.settings_custom['highlight_color_settings']['dependent_color'] = self.button_dependent_color.get_color()

        return True
