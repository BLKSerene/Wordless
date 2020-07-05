#
# Wordless: Settings - Auto-detection
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

from wl_utils import wl_conversion
from wl_widgets import wl_box, wl_layout, wl_tree, wl_widgets

class Wl_Settings_Auto_Detection(wl_tree.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

        # Detection Settings
        group_box_detection_settings = QGroupBox(self.tr('Detection Settings'), self)

        self.label_auto_detection_number_lines = QLabel(self.tr('Number of lines to scan in each file:'), self)
        (self.spin_box_auto_detection_number_lines,
         self.checkbox_auto_detection_number_lines_no_limit) = wl_widgets.wl_widgets_no_limit(self)

        self.spin_box_auto_detection_number_lines.setRange(1, 1000000)

        group_box_detection_settings.setLayout(wl_layout.Wl_Layout())
        group_box_detection_settings.layout().addWidget(self.label_auto_detection_number_lines, 0, 0)
        group_box_detection_settings.layout().addWidget(self.spin_box_auto_detection_number_lines, 0, 1)
        group_box_detection_settings.layout().addWidget(self.checkbox_auto_detection_number_lines_no_limit, 0, 2)

        group_box_detection_settings.layout().setColumnStretch(3, 1)

        # Default Settings
        group_box_default_settings = QGroupBox(self.tr('Default Settings'), self)

        self.label_auto_detection_default_lang = QLabel(self.tr('Default Language:'), self)
        self.combo_box_auto_detection_default_lang = wl_box.Wl_Combo_Box_Lang(self)
        self.label_auto_detection_default_text_type = QLabel(self.tr('Default Text Type:'), self)
        self.combo_box_auto_detection_default_text_type = wl_box.Wl_Combo_Box_Text_Type(self)
        self.label_auto_detection_default_encoding = QLabel(self.tr('Default Encoding:'), self)
        self.combo_box_auto_detection_default_encoding = wl_box.Wl_Combo_Box_Encoding(self)

        group_box_default_settings.setLayout(wl_layout.Wl_Layout())
        group_box_default_settings.layout().addWidget(self.label_auto_detection_default_lang, 0, 0)
        group_box_default_settings.layout().addWidget(self.combo_box_auto_detection_default_lang, 0, 1)
        group_box_default_settings.layout().addWidget(self.label_auto_detection_default_text_type, 1, 0)
        group_box_default_settings.layout().addWidget(self.combo_box_auto_detection_default_text_type, 1, 1)
        group_box_default_settings.layout().addWidget(self.label_auto_detection_default_encoding, 2, 0)
        group_box_default_settings.layout().addWidget(self.combo_box_auto_detection_default_encoding, 2, 1)

        group_box_default_settings.layout().setColumnStretch(3, 1)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(group_box_detection_settings, 0, 0)
        self.layout().addWidget(group_box_default_settings, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(2, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default)
        else:
            settings = copy.deepcopy(self.main.settings_custom)

        self.spin_box_auto_detection_number_lines.setValue(settings['auto_detection']['detection_settings']['number_lines'])
        self.checkbox_auto_detection_number_lines_no_limit.setChecked(settings['auto_detection']['detection_settings']['number_lines_no_limit'])

        self.combo_box_auto_detection_default_lang.setCurrentText(wl_conversion.to_lang_text(self.main, settings['auto_detection']['default_settings']['default_lang']))
        self.combo_box_auto_detection_default_text_type.setCurrentText(wl_conversion.to_text_type_text(self.main, settings['auto_detection']['default_settings']['default_text_type']))
        self.combo_box_auto_detection_default_encoding.setCurrentText(wl_conversion.to_encoding_text(self.main, settings['auto_detection']['default_settings']['default_encoding']))

    def apply_settings(self):
        settings = self.main.settings_custom

        settings['auto_detection']['detection_settings']['number_lines'] = self.spin_box_auto_detection_number_lines.value()
        settings['auto_detection']['detection_settings']['number_lines_no_limit'] = self.checkbox_auto_detection_number_lines_no_limit.isChecked()

        settings['auto_detection']['default_settings']['default_lang'] = wl_conversion.to_lang_code(self.main, self.combo_box_auto_detection_default_lang.currentText())
        settings['auto_detection']['default_settings']['default_text_type'] = wl_conversion.to_text_type_code(self.main, self.combo_box_auto_detection_default_text_type.currentText())
        settings['auto_detection']['default_settings']['default_encoding'] = wl_conversion.to_encoding_code(self.main, self.combo_box_auto_detection_default_encoding.currentText())

        return True
