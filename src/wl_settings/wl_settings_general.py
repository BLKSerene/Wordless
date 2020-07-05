#
# Wordless: Settings - General
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

from wl_dialogs import wl_dialog_misc
from wl_widgets import wl_box, wl_layout, wl_tree

class Wl_Settings_General(wl_tree.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

        # Font Settings
        group_box_font_settings = QGroupBox(self.tr('Font Settings'), self)

        self.label_font_family = QLabel(self.tr('Font Family:'), self)
        self.combo_box_font_family = wl_box.Wl_Combo_Box_Font_Family(self)
        self.label_font_size = QLabel(self.tr('Font Size:'), self)
        self.combo_box_font_size = wl_box.Wl_Combo_Box_Font_Size(self)

        group_box_font_settings.setLayout(QGridLayout())
        group_box_font_settings.layout().addWidget(self.label_font_family, 0, 0)
        group_box_font_settings.layout().addWidget(self.combo_box_font_family, 0, 1)
        group_box_font_settings.layout().addWidget(self.label_font_size, 1, 0)
        group_box_font_settings.layout().addWidget(self.combo_box_font_size, 1, 1)

        group_box_font_settings.layout().setColumnStretch(2, 1)

        # Update Settings
        group_box_update_settings = QGroupBox(self.tr('Update Settings'), self)

        self.checkbox_check_updates_on_startup = QCheckBox(self.tr('Check for updates on startup'), self)

        group_box_update_settings.setLayout(wl_layout.Wl_Layout())
        group_box_update_settings.layout().addWidget(self.checkbox_check_updates_on_startup, 0, 0)

        # Miscellaneous
        group_box_misc = QGroupBox(self.tr('Miscellaneous'), self)

        self.checkbox_confirm_on_exit = QCheckBox(self.tr('Always confirm on exit'), self)

        group_box_misc.setLayout(wl_layout.Wl_Layout())
        group_box_misc.layout().addWidget(self.checkbox_confirm_on_exit, 0, 0)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(group_box_font_settings, 0, 0)
        self.layout().addWidget(group_box_update_settings, 1, 0)
        self.layout().addWidget(group_box_misc, 2, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(3, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default)
        else:
            settings = copy.deepcopy(self.main.settings_custom)

        self.combo_box_font_family.setCurrentFont(QFont(settings['general']['font_settings']['font_family']))
        self.combo_box_font_size.set_text(settings['general']['font_settings']['font_size'])

        self.checkbox_check_updates_on_startup.setChecked(settings['general']['update_settings']['check_updates_on_startup'])

        self.checkbox_confirm_on_exit.setChecked(settings['general']['misc']['confirm_on_exit'])

    def apply_settings(self):
        settings = self.main.settings_custom

        # Check font settings
        font_old = [
            settings['general']['font_settings']['font_family'],
            settings['general']['font_settings']['font_size']
        ]

        font_new = [
            self.combo_box_font_family.currentFont().family(),
            self.combo_box_font_size.get_val()
        ]

        if font_new == font_old:
            result = 'skip'
        else:
            dialog_restart_required = wl_dialog_misc.Wl_Dialog_Restart_Required(self.main)
            result = dialog_restart_required.exec_()

            if result == QDialog.Accepted:
                result = 'restart'
            elif result == QDialog.Rejected:
                result = 'cancel'

        if result in ['skip', 'restart']:
            settings['general']['font_settings']['font_family'] = self.combo_box_font_family.currentFont().family()
            settings['general']['font_settings']['font_size'] = self.combo_box_font_size.get_val()

            settings['general']['update_settings']['check_updates_on_startup'] = self.checkbox_check_updates_on_startup.isChecked()

            settings['general']['misc']['confirm_on_exit'] = self.checkbox_confirm_on_exit.isChecked()

            if result == 'restart':
                self.main.restart()

            return True
        elif result == 'cancel':
            return False
