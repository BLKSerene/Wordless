#
# Wordless: Settings - Data
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
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

from wordless_widgets import wordless_box, wordless_layout, wordless_tree

class Wordless_Settings_Data(wordless_tree.Wordless_Settings):
    def __init__(self, main):
        super().__init__(main)

        # Precision Settings
        group_box_precision_settings = QGroupBox(self.tr('Precision Settings'), self)

        self.label_precision_decimal = QLabel(self.tr('Decimal:'), self)
        self.spin_box_precision_decimal = wordless_box.Wordless_Spin_Box(self)
        self.label_precision_pct = QLabel(self.tr('Percentage:'), self)
        self.spin_box_precision_pct = wordless_box.Wordless_Spin_Box(self)
        self.label_precision_p_value = QLabel(self.tr('p-value:'), self)
        self.spin_box_precision_p_value = wordless_box.Wordless_Spin_Box(self)

        self.spin_box_precision_decimal.setRange(0, 10)
        self.spin_box_precision_pct.setRange(0, 10)
        self.spin_box_precision_p_value.setRange(0, 15)

        group_box_precision_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_precision_settings.layout().addWidget(self.label_precision_decimal, 0, 0)
        group_box_precision_settings.layout().addWidget(self.spin_box_precision_decimal, 0, 1)
        group_box_precision_settings.layout().addWidget(self.label_precision_pct, 1, 0)
        group_box_precision_settings.layout().addWidget(self.spin_box_precision_pct, 1, 1)
        group_box_precision_settings.layout().addWidget(self.label_precision_p_value, 2, 0)
        group_box_precision_settings.layout().addWidget(self.spin_box_precision_p_value, 2, 1)

        group_box_precision_settings.layout().setColumnStretch(2, 1)

        self.setLayout(wordless_layout.Wordless_Layout())
        self.layout().addWidget(group_box_precision_settings, 0, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(1, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default)
        else:
            settings = copy.deepcopy(self.main.settings_custom)

        self.spin_box_precision_decimal.setValue(settings['data']['precision_decimal'])
        self.spin_box_precision_pct.setValue(settings['data']['precision_pct'])
        self.spin_box_precision_p_value.setValue(settings['data']['precision_p_value'])

    def apply_settings(self):
        settings = self.main.settings_custom

        settings['data']['precision_decimal'] = self.spin_box_precision_decimal.value()
        settings['data']['precision_pct'] = self.spin_box_precision_pct.value()
        settings['data']['precision_p_value'] = self.spin_box_precision_p_value.value()

        return True
