#
# Wordless: Widgets - Button
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_msg_box
from wl_utils import wl_misc

class Wl_Button(QPushButton):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.main = wl_misc.find_wl_main(parent)

class Wl_Button_Results_Sort(Wl_Button):
    def __init__(self, parent, table):
        from wl_dialogs import wl_dialog_results_sort

        super().__init__(parent.tr('Sort Results'), parent)

        self.dialog_results_sort = wl_dialog_results_sort.Wl_Dialog_Results_Sort_Concordancer(
            self.main,
            table = table
        )

        self.setFixedWidth(150)

        self.clicked.connect(self.dialog_results_sort.show)

    def add_tables(self, tables):
        self.dialog_results_sort.add_tables(tables)

class Wl_Button_Results_Filter(Wl_Button):
    def __init__(self, parent, tab, table):
        from wl_dialogs import wl_dialog_results_filter

        super().__init__(parent.tr('Filter Results'), parent)

        if tab in ['wordlist', 'ngram']:
            dialog_results_filter = wl_dialog_results_filter.Wl_Dialog_Results_Filter_Wordlist(
                self.main,
                tab = tab,
                table = table
            )
        elif tab in ['collocation', 'colligation']:
            dialog_results_filter = wl_dialog_results_filter.Wl_Dialog_Results_Filter_Collocation(
                self.main,
                tab = tab,
                table = table
            )
        elif tab == 'keyword':
            dialog_results_filter = wl_dialog_results_filter.Wl_Dialog_Results_Filter_Keyword(
                self.main,
                tab = tab,
                table = table
            )

        self.setFixedWidth(150)

        self.clicked.connect(dialog_results_filter.show)

class Wl_Button_Results_Search(Wl_Button):
    def __init__(self, parent, tab, table):
        from wl_dialogs import wl_dialog_results_search

        super().__init__(parent.tr('Search in Results'), parent)

        self.dialog_results_search = wl_dialog_results_search.Wl_Dialog_Results_Search(
            self.main,
            tab = tab,
            table = table
        )

        self.setFixedWidth(150)

        self.clicked.connect(self.dialog_results_search.load)

    def add_tables(self, tables):
        self.dialog_results_search.add_tables(tables)

class Wl_Button_Restore_Default_Settings(Wl_Button):
    def __init__(self, parent):
        # Pad with spaces
        super().__init__(parent.tr(' Restore default settings '), parent)

        self.parent = parent

        self.clicked.connect(self.restore_default_settings)

    def restore_default_settings(self):
        if wl_msg_box.wl_msg_box_restore_default_settings(self.main):
            self.parent.load_settings(defaults = True)

        self.parent.activateWindow()

class Wl_Button_Reset_All_Settings(Wl_Button):
    def __init__(self, parent):
        # Pad with spaces
        super().__init__(parent.tr(' Reset All Settings '), parent)

        self.parent = parent

        self.clicked.connect(self.reset_settings)

    def reset_settings(self):
        if wl_msg_box.wl_msg_box_reset_all_settings(self.main):
            self.parent.load_settings(defaults = True)

        self.parent.activateWindow()
        