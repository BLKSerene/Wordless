#
# Wordless: Dialogs - Sort Results
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_dialog
from wl_widgets import wl_button, wl_layout, wl_table

class Wl_Dialog_Results_Sort_Concordancer(wl_dialog.Wl_Dialog):
    def __init__(self, main, table):
        super().__init__(main, main.tr('Sort Results'))

        self.table = table
        self.settings = self.main.settings_custom['concordancer']['sort_results']

        self.table_sort = wl_table.Wl_Table_Results_Sort_Conordancer(self, self.table)

        self.button_reset_settings = wl_button.Wl_Button_Reset_Settings(self)
        self.button_sort = QPushButton(self.tr('Sort'), self)
        self.button_close = QPushButton(self.tr('Close'), self)

        self.table_sort.setFixedWidth(280)

        self.button_reset_settings.setFixedWidth(130)
        self.button_sort.setFixedWidth(80)
        self.button_close.setFixedWidth(80)

        self.table_sort.itemChanged.connect(self.sort_table_changed)

        self.button_sort.clicked.connect(lambda: self.table_sort.sort_results())
        self.button_close.clicked.connect(self.reject)

        layout_table_sort = wl_layout.Wl_Layout()
        layout_table_sort.addWidget(self.table_sort, 0, 0, 4, 1)
        layout_table_sort.addWidget(self.table_sort.button_add, 0, 1)
        layout_table_sort.addWidget(self.table_sort.button_insert, 1, 1)
        layout_table_sort.addWidget(self.table_sort.button_remove, 2, 1)

        layout_table_sort.setRowStretch(3, 1)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addLayout(layout_table_sort, 0, 0, 1, 4)

        self.layout().addWidget(wl_layout.Wl_Separator(self), 1, 0, 1, 4)

        self.layout().addWidget(self.button_reset_settings, 2, 0)
        self.layout().addWidget(self.button_sort, 2, 2)
        self.layout().addWidget(self.button_close, 2, 3)

        self.layout().setColumnStretch(1, 1)

        self.set_fixed_size()

    def sort_table_changed(self):
        self.settings['sorting_rules'] = []

        if self.table_sort.cellWidget(0, 0):
            for i in range(self.table_sort.rowCount()):
                self.settings['sorting_rules'].append([self.table_sort.cellWidget(i, 0).currentText(),
                                                       self.table_sort.cellWidget(i, 1).currentText()])

    def load_settings(self, defaults = False):
        if defaults:
            settings = self.main.settings_default['concordancer']['sort_results']
        else:
            settings = self.settings

        self.table_sort.clear_table(0)

        for sorting_col, sorting_order in settings['sorting_rules']:
            self.table_sort.add_row()

            self.table_sort.cellWidget(self.table_sort.rowCount() - 1, 0).setCurrentText(sorting_col)
            self.table_sort.cellWidget(self.table_sort.rowCount() - 1, 1).setCurrentText(sorting_order)

        self.table_sort.clearSelection()
