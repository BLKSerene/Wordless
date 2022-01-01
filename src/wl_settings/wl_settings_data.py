#
# Wordless: Settings - Data
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_widgets import wl_box, wl_layout, wl_tree

class Wl_Settings_Data(wl_tree.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['data']
        self.settings_custom = self.main.settings_custom['data']

        # Rank Settings
        group_box_rank_settings = QGroupBox(self.tr('Rank Settings'), self)

        self.checkbox_continue_numbering_after_ties = QCheckBox(self.tr('Continue numbering after ties'), self)

        group_box_rank_settings.setLayout(wl_layout.Wl_Layout())
        group_box_rank_settings.layout().addWidget(self.checkbox_continue_numbering_after_ties, 0, 0)

        group_box_rank_settings.layout().setRowStretch(1, 0)

        # Precision Settings
        group_box_precision_settings = QGroupBox(self.tr('Precision Settings'), self)

        self.label_precision_decimal = QLabel(self.tr('Decimal:'), self)
        self.spin_box_precision_decimal = wl_box.Wl_Spin_Box(self)
        self.label_precision_pct = QLabel(self.tr('Percentage:'), self)
        self.spin_box_precision_pct = wl_box.Wl_Spin_Box(self)
        self.label_precision_p_value = QLabel(self.tr('p-value:'), self)
        self.spin_box_precision_p_value = wl_box.Wl_Spin_Box(self)

        self.spin_box_precision_decimal.setRange(0, 10)
        self.spin_box_precision_pct.setRange(0, 10)
        self.spin_box_precision_p_value.setRange(0, 15)

        group_box_precision_settings.setLayout(wl_layout.Wl_Layout())
        group_box_precision_settings.layout().addWidget(self.label_precision_decimal, 0, 0)
        group_box_precision_settings.layout().addWidget(self.spin_box_precision_decimal, 0, 1)
        group_box_precision_settings.layout().addWidget(self.label_precision_pct, 1, 0)
        group_box_precision_settings.layout().addWidget(self.spin_box_precision_pct, 1, 1)
        group_box_precision_settings.layout().addWidget(self.label_precision_p_value, 2, 0)
        group_box_precision_settings.layout().addWidget(self.spin_box_precision_p_value, 2, 1)

        group_box_precision_settings.layout().setColumnStretch(2, 1)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(group_box_rank_settings, 0, 0)
        self.layout().addWidget(group_box_precision_settings, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(2, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        self.checkbox_continue_numbering_after_ties.setChecked(settings['continue_numbering_after_ties'])

        self.spin_box_precision_decimal.setValue(settings['precision_decimal'])
        self.spin_box_precision_pct.setValue(settings['precision_pct'])
        self.spin_box_precision_p_value.setValue(settings['precision_p_value'])

    def apply_settings(self):
        self.settings_custom['continue_numbering_after_ties'] = self.checkbox_continue_numbering_after_ties.isChecked()

        self.settings_custom['precision_decimal'] = self.spin_box_precision_decimal.value()
        self.settings_custom['precision_pct'] = self.spin_box_precision_pct.value()
        self.settings_custom['precision_p_value'] = self.spin_box_precision_p_value.value()

        return True
