#
# Wordless: Message
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def empty_search_term(main):
    QMessageBox.warning(main,
                        main.tr('Empty Search Term'),
                        main.tr('Please enter your search term(s) first!'),
                        QMessageBox.Ok)

def empty_results_table(main):
    QMessageBox.information(main,
                            main.tr('No Search Results'),
                            main.tr('There is nothing to be shown in the table.<br>You might want to change your search term(s) and/or your settings, and then try again.'),
                            QMessageBox.Ok)

def empty_results_plot(main):
    QMessageBox.information(main,
                            main.tr('No Search Results'),
                            main.tr('There is nothing to be shown in the figure.<br>You might want to change your search term(s) and/or your settings, and then try again.'),
                            QMessageBox.Ok)