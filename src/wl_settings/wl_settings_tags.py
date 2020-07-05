#
# Wordless: Settings - Tags
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

from wl_widgets import wl_layout, wl_table, wl_tree

class Wl_Table_Tags_Pos(wl_table.Wl_Table_Tags):
    def reset_table(self):
        super().reset_table()

        for tags in self.main.settings_default['tags']['tags_pos']:
            self.add_item(texts = tags)

class Wl_Table_Tags_Non_Pos(wl_table.Wl_Table_Tags):
    def reset_table(self):
        super().reset_table()

        for tags in self.main.settings_default['tags']['tags_non_pos']:
            self.add_item(texts = tags)

class Wl_Settings_Tags(wl_tree.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

        # POS Tag Settings
        group_box_pos_tag_settings = QGroupBox(self.tr('POS Tag Settings'), self)

        self.table_tags_pos = Wl_Table_Tags_Pos(self)

        group_box_pos_tag_settings.setLayout(wl_layout.Wl_Layout())
        group_box_pos_tag_settings.layout().addWidget(self.table_tags_pos, 0, 0, 1, 3)
        group_box_pos_tag_settings.layout().addWidget(self.table_tags_pos.button_add, 1, 0)
        group_box_pos_tag_settings.layout().addWidget(self.table_tags_pos.button_remove, 1, 1)
        group_box_pos_tag_settings.layout().addWidget(self.table_tags_pos.button_reset, 1, 2)

        # Non-POS Tag Settings
        group_box_non_pos_tag_settings = QGroupBox(self.tr('Non-POS Tag Settings'), self)

        self.table_tags_non_pos = Wl_Table_Tags_Non_Pos(self)

        group_box_non_pos_tag_settings.setLayout(wl_layout.Wl_Layout())
        group_box_non_pos_tag_settings.layout().addWidget(self.table_tags_non_pos, 0, 0, 1, 3)
        group_box_non_pos_tag_settings.layout().addWidget(self.table_tags_non_pos.button_add, 1, 0)
        group_box_non_pos_tag_settings.layout().addWidget(self.table_tags_non_pos.button_remove, 1, 1)
        group_box_non_pos_tag_settings.layout().addWidget(self.table_tags_non_pos.button_reset, 1, 2)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(group_box_pos_tag_settings, 0, 0)
        self.layout().addWidget(group_box_non_pos_tag_settings, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(2, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default)
        else:
            settings = copy.deepcopy(self.main.settings_custom)

        self.table_tags_pos.clear_table(0)

        for tags in settings['tags']['tags_pos']:
            self.table_tags_pos.add_item(texts = tags)

        self.table_tags_non_pos.clear_table(0)

        for tags in settings['tags']['tags_non_pos']:
            self.table_tags_non_pos.add_item(texts = tags)

    def apply_settings(self):
        settings = self.main.settings_custom

        settings['tags']['tags_pos'] = self.table_tags_pos.get_tags()
        settings['tags']['tags_non_pos'] = self.table_tags_non_pos.get_tags()

        return True
